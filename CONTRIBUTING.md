# About FrontierPhysics
FrontierPhysics evaluates how agents help with Physics research. Specifically, we turn day-to-day work in physics labs into tasks for agents. By observing agents' performance in tackling these tasks, with and without skills, we can get insights into agents' capability and shortcomings in solving Physics research tasks, and the data can be used to improve agents' ability. 

To achieve this, we need contributors from the broad Physics community to add diverse, authetic, challenging, and well-tested task packages. 

**Links**: 

# Authorship policy
Contribution credit is tracked in points, and **12 points earns co-authorship**
on the FrontierPhysics paper and dataset.

| Contribution | Points |
|---|---:|
| A task you authored is merged | 4 |
| A task you reviewed is merged | 1 |

Points accumulate across both kinds of work, so three merged tasks reaches 12,
and so does any mix that adds up — two merged tasks plus four reviews, for
example.

Points are awarded on merge, not on submission: a review earns its point only
once the task it reviewed is merged. Quality beats quantity — one excellent task
is worth more than many mediocre ones, and a submission that does not clear the
bar in [What makes a good task](#what-makes-a-good-task) earns nothing.

# What makes a good task
A good task must satisfy three requirements:
1. Representative
It must come from workflows used in real Physics research. 

2. Complex
Require substantial domain expertise and effort. An agent without mentoring skills have to use at least 80 tool calls and over 100 steps, and is very likely to fail the task.

3. Verifiable
The task should have deliverables that can be deterministically graded. 

# How to contribute
1. **Ideate**: Pick a domain where you have real expertise and choose a project you have done before that satisfy the above three requirements for a good task.
2. **Create**: Implement a task package. You can refer to .. for examples of a good task, and you can refer to the `Task Package` section below for the strcture of a task.
3. **Test**: Run the oracle and at least one agent with and without skills.
4. **Submit**: Open a PR using the required checklist below.

# Task Package
Technically, a task consists of:

```text
tasks/<task-id>/
├── task.md
├── environment/
│   ├── Dockerfile
│   ├── <bundled inputs>
│   └── skills/
│       └── <skill-name>/
│           ├── SKILL.md
│           ├── references/
│           └── scripts/
├── oracle/
│   └── solve.sh
└── verifier/
    ├── test.sh
    └── test_outputs.py
```
## task.md
Usually the first file that you write. `task.md` starts with YAML frontmatter, followed by the human-written prompt body.
The frontmatter carries metadata, timeouts, and resource requirements. The body is the instructions (prompt) for the agents. 

Here are some rules for writing the prompt:
- Write by hand in clear, imperative prose.
- Describe the desired end state, not the solution steps.
- Use explicit absolute paths for inputs and outputs.
- Do not mention skill names or tell the agent which skills to use.
- Anchor a date when the correct answer depends on time-sensitive data.

## environment/
As shown above, an `environment/` folder contains the Dockerfile, inputs, and skills. The Dockerfiles create a Docker environment for agents in which it'll work to solve the task. If the task requires inputs (e.g., data, reference, examples, etc.), put these under the environment/inputs/ folder. `environment/skills` contain mentoring skills for agents that help them with the task.

Guidelines for Dockerfile:

- Use Python 3.12+ unless a task has a documented reason not to.
- Pin Python packages to exact versions.
- Bundle reproducible inputs in `environment/`.

Guidelines for skills:
- Skills should contain reusable domain guidance, not task-specific answers.
- Explain non-obvious workflow knowledge, schemas, formulas, standards, or tools.
- Reuse scripts and references that would help on more than one task.
- Stay focused; split long details into `references/`.
- Avoid mentioning the exact output answer or task-specific filenames unless the
  filename is a real reusable interface.
- Do not bake skills into agent home directories. BenchFlow injects skills at
  runtime when `--skill-mode with-skill --skills-dir ...` is used.

## oracle/
`oracle/solve.sh` is the held-out reference solution. It must be human-written
and derive the answer through computation rather than hardcoding final values.

For tasks where a hand-authored binary artifact is unavoidable, explain that
tradeoff in the PR description and keep the artifact in `oracle/`.

## verifier/
The verifier checks outcomes and writes a scalar reward to
`/logs/verifier/reward.txt`.

Verifier rules:

- Test the result, not the process.
- Use 4-10 focused test functions; parametrize related cases.
- Every test should check something distinct.
- Copy important output artifacts into `/logs/verifier/` for review.
- Oracle and verifier must not require paid API keys.

# Task Quality Rubric

Every PR is evaluated against the [task-review skill](.agents/skills/task-review/).
Reviewers look for:

- **Authenticity**: real scenario, real data where possible, human-authored task
  prompt and oracle.
- **Skill quality**: accurate, reusable, useful beyond this task.
- **Verification**: deterministic, outcome-based, anti-cheat aware.
- **Instructions**: concise, fair, no skill hints.
- **Environment**: reproducible Docker image, pinned deps, no leaked skills.
- **Complexity**: 
the agents use over 100 steps + over 80 tool calls to solve the task + have a high chance of failing agents without skills.

# PR Requirements

Before opening a PR:

1. `bench tasks check tasks/<task-id>` passes.
2. `bench eval run --tasks-dir tasks/<task-id> --agent oracle --sandbox docker`
   passes with reward 1.0.
3. At least one agent has been tested with and without skills.
4. The PR description includes pass rates, failure analysis, and artifacts for
   multimodal outputs.
5. The task prompt, oracle, skills, tests, and metadata are ready for human review.
