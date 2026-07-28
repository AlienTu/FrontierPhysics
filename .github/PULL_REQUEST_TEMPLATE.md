## Motivation

What advanced physics workflow does this task represent, and who performs this
work?

## Task history

This task must come from research you personally carried out, and which took
you two weeks or more. Give real dates and an honest hour count.

| Field | Value |
|---|---|
| What the original work was | |
| Start date | YYYY-MM-DD |
| End date | YYYY-MM-DD |
| Working hours spent | |
| Did an LLM agent help, and where? | |
| Your background | PhD / PhD candidate / lab or industry experience |

## Task

| Field | Value |
|---|---|
| Task ID | `your-task-id` |
| Physics area | |
| Difficulty | Easy / Medium / Hard |
| Source and provenance | |
| Mentor skills | |

## Checklist

- [ ] `task.md` prompt body is human-authored and outcome-focused
- [ ] `oracle/solve.sh` and oracle logic are human-authored
- [ ] Metadata follows `taxonomy.yaml`
- [ ] `bench tasks check tasks/<task-id>` passes
- [ ] Oracle reaches reward `1.0`
- [ ] Verifier checks outcomes, not implementation or skill usage
- [ ] Mentor skills are included and may be task-specific
- [ ] Mentor skills contain no hardcoded final answers or verifier internals
- [ ] Dockerfile does not bake skills into the agent image
- [ ] Source, data, code, and license provenance are documented
- [ ] No-skill and with-skill runs use the same task commit and model settings
- [ ] At least one strong agent passes the with-skill solvability control
- [ ] Trajectories and output artifacts were inspected
- [ ] The task comes from my own research and took two weeks or more
- [ ] This PR is from a fork and touches only `tasks/<task-id>/`

## Local test results

Report multiple trials per condition, not a single run. If a trial set was cut
short, say so and report what finished.

| Agent | Model | Reasoning | No skill (primary) | With skills (control) | Time |
|---|---|---|---:|---:|---:|
| | | | | | |

## Failure analysis

Explain whether failures came from scientific reasoning, environment/tooling,
instructions, formatting, or verifier behavior.

## What you learned building it

Anything a reviewer or future contributor should know — a leaky environment, a
brittle tolerance, a metric that turned out uninformative.

## Artifacts

Include oracle output, verifier logs, trajectories, and any visual or binary
artifacts needed for human review.

## Credit

Merging awards 4 points to the task author and 1 point to each reviewer who
signed off; 12 points earns co-authorship on the FrontierPhysics paper and
dataset. See the [authorship policy](https://github.com/benchflow-ai/FrontierPhysics/blob/main/CONTRIBUTING.md#authorship-policy).

| Role | GitHub handle(s) |
|---|---|
| Author | |
| Reviewers | |
