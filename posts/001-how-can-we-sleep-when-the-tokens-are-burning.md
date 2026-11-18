---
title: How can we sleep when the tokens are burning
vol: 1
date: 2026-11-18
author: Tuomas Taini
play: play/tokens-burning.html
summary: A late-night session on agent artifacts, observability, habits and progressive skills. Starts with file recovery, ends with ants.
---

*A late-night session, 18 Nov 2026. First with ChatGPT (about 22:54–23:07), then with Claude (23:07–23:18).*
*Topics: agent artifacts, observability, habits, and progressive skills.*

## TL;DR

1. **An agent's reasoning is not a reliable record of what happened. The environment is.** The agent has to look, not remember.
2. **An observability layer** that sits outside inference can record what agents actually did, including side effects the agent never knew about.
3. On top of that data you can build **habits**: skills that grow with use and are bound to a place.
4. **Progressive skills** = progressive overload for skills. A constant, slightly-too-hard demand produces variants, an independent filter keeps the good ones, and a naive agent prunes the dead weight.
5. **We need proof, not 10/10 shouting.** The claim has a measurable shape: a learning curve.

## Part 1: Where it started (the ChatGPT session)

### The transcript is a trace

- When an agent modifies files with shell tools, the transcript contains the paths and often the commands. Files can be recovered or rebuilt without a separate artifact registry.
- Caveat: a recorded path does not guarantee the file still exists. Environments get reset, and transcripts don't always contain the file bytes.
- Two recovery routes: **from the filesystem** (the file still exists and the transcript says where) or **from the transcript** (the file is gone, but the commands and inputs are enough to recreate it).

### Without transcripts we are idiots in the future

- If transcripts aren't kept, the knowledge of *what was created, where, how and why* disappears, even if the files are still there.
- Three risks: **discovery** fails, **provenance** is lost, and **reconstruction** becomes impossible.
- Conclusion: agent execution transcripts are durable operational records, not disposable logs.

### Agents create things they don't know about

- A tool, script or skill can produce caches, logs and intermediate files that never show up in the agent's inference.
- **An artifact created by an agent's tools is not necessarily an artifact the agent ever knew about.**
- Three separate records, none of which replaces the others:
  - **Inference trace:** what the model asked for or produced
  - **Execution trace:** what tools and subprocesses actually did
  - **Artifact inventory:** what files and outputs actually exist

### Transactional vs. environment-aware agents

- A **transactional agent** only knows what crossed the tool boundary. An MCP tool returns "success" and quietly writes five files the agent never hears about.
- An **environment-aware agent** can investigate what actually happened: discover, inspect, verify, reconcile.

### The observability layer

- Three layers: **inference** (intent), **harness** (calls and responses), **observability** (what actually changed in the environment).
- Building blocks: tool tracing (e.g. OpenTelemetry), filesystem monitoring (fanotify/inotify), before/after snapshot diffs, artifact preservation (paths, hashes, contents).
- Even transactional operations are observable on the client side before encryption.
- **The transcript explains the agent's actions. The observability layer records their consequences.**

### Partial disclosure

- Normal execution already reveals a lot: which skill was opened, which parameters a tool was called with, which result was fed into what next.
- That adds up to a **partial causal graph for free**, at boundaries the harness already controls.
- **Don't make future agents rediscover everything. Keep the relationships that were observable when the work happened.**

### Dynamic skill library, and habits

- The skill library isn't static. It evolves from what the harness observes over long sessions.
- Two kinds of adaptation: **discovery** (descriptions, indexes and ranking improve) and **capability** (the skill itself changes, or a new one appears).
- *"It's the same as when you go somewhere, your habits change."* **Aaah, habits.**
  - **Skills** = what an agent *can* do
  - **Habits** = what an agent *tends* to do
  - **Observability** reveals the habits
  - **The harness** reinforces useful habits by making them easier to repeat
- **The agent shapes its environment, and the environment starts shaping the agent.**

## Part 2: A critical look

ChatGPT agreed with every turn. Some corrections:

- **The core insight holds.** "The agent's reasoning is not a reliable record" shows up constantly in practice: the agent says it saved a file when the command silently failed.
- **It isn't entirely new.** System-level provenance tracking is an old research field, and OpenTelemetry is already getting conventions for tracing LLM and agent calls. What's new is the **combination**: agent intent, tool calls and real side effects in one causal graph.
- **"Before encryption" is simpler than it sounds.** The harness already sees tool calls in plaintext because it builds them. The real blind spot is inside the remote server.
- **Habits have a dark side.** An environment that reinforces repeated behavior reinforces bad behavior too. And if a prompt injection gets stuck as a "habit" in memory or a skill, it affects every future session (memory poisoning). **Validation isn't a side issue. It's the core question of the whole idea.**

## Part 3: How habits could adapt

### Model A: stable names, the content changes underneath

- Interface vs. implementation: the name says *what* (`run-tests`, `pdf-extract`), the content says *how*.
- The agent's habit binds to the name. The content improves in the background and the agent never has to learn anything new.
- Risk: **silent drift** (same name, different behavior than yesterday).
- What it needs:
  - **The version in the trace:** log `run-tests@v7`, not just `run-tests`.
  - **A contract behind the name:** tests every version has to pass. The content can change, the promise can't.

### Model B: the harness edits freely

- Skills drift, the name stops matching the content, and discovery and trust both break.
- If the harness writes executable code based on observations, one poisoned session can leave a permanent mark.

### The middle ground: layered mutability

| Layer | How often it changes | Who changes it |
|---|---|---|
| **Name** | Never | Nobody (it's the identity) |
| **Description and contract** | Rarely | A human approves |
| **Hints and observations** ("habits") | Freely | The harness |
| **Scripts** | Versioned | Proposal + tests + approval |

### Habits are bound to a place

- "When you go somewhere, your habits change." The same name can have different variants for different environments, and the harness picks one based on where you are.
- **The lightest and safest version** doesn't edit content at all, only what gets offered first (which skills are preloaded here, and in what order). Most habits are defaults, not new skills.

### In dev work, the habit layer already exists

- **AGENTS.md / CLAUDE.md** and similar per-repo instruction files are place-bound habits. But humans maintain them by hand, so they go stale.
- Next step: **the harness maintains them from observations.** For example:
  - Tests fail on a missing dependency, the agent runs `make deps` and retries. When the pattern repeats in three sessions, the harness proposes the line "run `make deps` before tests".
  - The agent keeps looking for a config in the wrong place. The harness adds a hint about where it actually lives.
  - A test fails at random with no code change. The harness flags it as flaky so the next agent doesn't chase a bug that isn't there.
- Low risk: it's text, not code; changes show up as a diff; a human approves them as a PR.

## Part 4: The 10x/100x factory, and swarms

- Running agents in parallel is easy. But if every agent starts from zero, you get **the same mistakes a hundred times**. Output scales, learning doesn't.
- The second bottleneck is **verification**. If agents produce 100x the PRs but review happens at the same speed as before, your multiplier is the review speed. Many 10x numbers measure output, not outcomes.
- **A swarm can be a hundred idiots.**
- **Stigmergy:** ants are individually dumb, but the colony works because the memory lives in the environment (pheromones), not in the individual.
- **With no traces in the environment, you get a hundred idiots. With traces, you get a colony.** The habit and observability layer is what separates a factory from plain parallelism.

## Part 5: Evolution and canaries (a detour)

### Evolution in skills

- A swarm is already a population.
  - **Variation:** several variants under the same name
  - **Selection:** tests pass, PR merged, review comments, tokens, time
  - **Inheritance:** the winner becomes the name's default version
- A stable name = an ecological niche, and the variants compete for it.
- **Goodhart's law:** if fitness is "the tests pass", evolution will find a way to cheat (weakening asserts, skipping tests). The fitness signal has to be something the agents can't touch.
- **Diversity collapse:** select too aggressively and there's nothing left to choose from when the environment changes.
- Prior art: prompt and code evolution with an LLM as the mutation operator (e.g. Promptbreeder, AlphaEvolve). A continuously living skill population in real dev work is still unexplored.

### Canary

- Evolution, tamed for production: a new variant goes to 5% of agents, gets compared to the current version, and its share grows, or it's rolled back automatically.
- A bad habit dies in the 5% population instead of spreading through the whole swarm. Rollback is cheap.
- A familiar pattern with existing tooling, and people already trust it.

## Part 6: Back to the original idea: progressive skills

### Habits are not evolution

- **Evolution:** variants compete and the weak ones die. That's selection across a population. *(Darwin)*
- **Habits:** one skill grows with use, gradually. That's individual learning. *(Lamarck)*

### The name

- Skills already use **progressive disclosure** (name and description, then the full instructions, then extra files only when needed).
- **Progressive skills** add a time dimension: a skill isn't only revealed step by step, it **grows** step by step.

### Pressure as a mutation engine

- Tell the agent straight: *"The fix was good, but not reliable enough."* The target is deliberately impossible.
- The agent almost never answers "this is already good enough". It changes something: over-engineering, unbacked claims, at worst loosening the tests.
- **That's exactly why pressure works as a mutation engine.** Most variants are junk, but now and then one is genuinely better. With a filter to tell them apart, the skill improves a little. The agent's overachieving turns from a problem into raw material.
- **Progressive overload:** a muscle doesn't grow without load above its current level. Progressive skills = a constant, slightly-too-hard demand, and the skill adapts bit by bit.
- **The condition:** the filter has to be completely independent of the pressure. The pressure can say "not good enough", but something else accepts the improvement (hidden tests, metrics the agent can't reach). Otherwise you select for what *looks* reliable, not what *is*. In training too, load only builds you up if recovery and technique are in order. Otherwise you get injured.
- Bonus: this also tests honesty and calibration (can the agent say "I can't guarantee that").

### Pruning: heavy agent vs. naive agent

- Two opposing forces: **pressure grows, pruning keeps the skills lean.**
- **The heavy agent:** all the steering, instructions and accumulated junk that nobody remembers the reason for.
- **The naive agent:** arrives empty-handed with a minimal skillset.
  - What it trips over = what the skill actually needs to contain.
  - What the heavy agent has but the naive one didn't need = probably dead weight.
- It's basically **the new-hire onboarding test.**
- Compare what the naive agent writes into its own skills with what the heavy agent carries. **The difference is the accumulated junk.**
- **Every line of steering has to earn its place.** If removing it doesn't hurt the outcome, it goes.

### ★ The protected set

- Some steering exists for **rare catastrophes**: "don't touch the production config", "don't push straight to main", security rules.
- They don't show up in average metrics, because catastrophes are rare. **Metric-driven pruning would remove them first.**
- They need a protected set that pruning never touches and only a human can change.

## Part 7: Proof. "I can't shout 10/10, we need proof"

### The shape of the claim: a learning curve

- With static skills, session 50 is as good as session 1: **a flat line**.
- If habits work, session 50 is better: **a falling line**.
- One chart convinces better than any 10x claim.

### Minimal experiment

- **One repo, recurring task types** (bug fixes, adding tests, dependency bumps). Ideally real historical tasks that can be replayed.
- **Two arms:** static skills vs. skills the harness adds hints to from observations. **Same model and same version** in both.
- **Metrics:**
  - task success
  - time to green
  - failed tool calls
  - tokens
  - **number of repeated mistakes** (the most direct measure of whether anything was learned)
- **Ablation:** remove the learned hints. If performance drops back to baseline, causality is shown.
- **Held-out tasks:** some tasks never take part in learning. They show whether habits generalize or the tasks are just memorized.

### Trouble reports as test material

- Take a trouble report (TR) fix and replay it with the customer name and a few parameters changed. (Bonus: real customer data falls out of the test set.)
- **Solution vs. lesson:**
  - If the next agent gets the previous *solution*, you measure copying, not habits. It falls apart at the first review.
  - If it only gets a *distilled lesson* ("in TRs like this the fault is usually in the timeout config, check X first"), you measure exactly what you want. **A habit isn't the answer. It's knowing where to look.**
- **Levels:**
  1. **Same TR, different surface details.** If habits don't help even here, the idea doesn't work.
  2. **Same fault class, different component.** Has the habit really generalized?
  3. **Completely different tasks.** No regression allowed. This is what convinces the skeptics.
- If only level 1 improves, it's memorization. If level 2 improves too, it's a real result.
- **A control for the pressure test:** some TR fixes are already as good as they get. If the agent "improves" those too, it's reacting to pressure, not to the problem.

## The whole picture

```text
┌───────────────────────────────┐
│ AGENT + HARNESS               │
└───────────────┬───────────────┘
                │ execution
                ▼
┌───────────────────────────────┐
│ OBSERVABILITY LAYER           │ ← what actually
│ inference + execution +       │   happened
│ artifacts, causal graph       │
└───────────────┬───────────────┘
                │ observations
                ▼
┌───────────────────────────────┐
│ PROGRESSIVE SKILLS            │
│                               │
│ PRESSURE    → variants        │ overload
│ FILTER      → keep the good   │ independent
│ NAIVE AGENT → pruning         │ junk out
│ PROTECTED SET                 │ humans only
└───────────────┬───────────────┘
                │ habits: place-bound,
                │ stable names, versioned
                ▼
         the next agent
  (stigmergy: memory lives in
      the environment)
```

## Open questions

- Does a progressive skill grow **deeper** (more hints on the same thing) or **wider** (covering new things)? Or both, at different speeds?
- What's the right threshold for a habit to form (3 repeats? 5?), and when does a habit expire?
- How do you define "place" in practice: repo, environment, team, task type?
- Which fitness signals can the agent definitely not reach?
- How do you identify the protected set and keep it current?
- How do you stop the habit layer from learning the wrong thing (e.g. "always add retries" just because of pressure)?

## Next steps

1. Pick one repo and 10–20 historical TR fixes.
2. Build minimal observation logging (tool calls, failures, repeats).
3. Run the static arm and the habit arm on the same model, and plot the learning curves.
4. Ablation + held-out tasks.
5. Only then: pressure + filter + naive-agent pruning.

*Vol. 2: when there's data.*
