import { Button } from "@/components/ui/button";
import { credit, site, tasksForAuthorship } from "@/lib/site";
import {
  ArrowUpRight,
  Award,
  Check,
  FlaskConical,
  Layers,
  ShieldCheck,
  X,
} from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Contribute a task",
  description:
    "How to turn physics research you have already done into a FrontierPhysics benchmark task.",
};

const CRITERIA = [
  {
    title: "Representative",
    body: "It comes from a workflow used in real physics research — something you or your group actually had to do.",
    check: "Have I done this myself?",
    icon: FlaskConical,
    accent: "text-chart-1",
    tint: "bg-chart-1/10",
  },
  {
    title: "Complex",
    body: "It needs substantial domain expertise. An agent without mentor skills should need 100+ steps and 80+ tool calls, and should be likely to fail.",
    check: "Would this take a new student days?",
    icon: Layers,
    accent: "text-chart-2",
    tint: "bg-chart-2/10",
  },
  {
    title: "Verifiable",
    body: "The deliverables can be graded deterministically — numbers, files, and artifacts a test can check without a human in the loop.",
    check: "Can a script tell right from wrong?",
    icon: ShieldCheck,
    accent: "text-chart-3",
    tint: "bg-chart-3/10",
  },
];

const STEPS = [
  {
    step: "01",
    title: "Ideate",
    body: "Pick a domain where you have real expertise and a project you have already done that meets the three criteria above.",
  },
  {
    step: "02",
    title: "Create",
    body: "Write the task package: the prompt and metadata in task.md, a pinned Docker environment, mentor skills, the oracle solution, and the verifier.",
  },
  {
    step: "03",
    title: "Test",
    body: "Run the oracle, then run at least one agent both with and without skills so the PR carries real evidence.",
  },
  {
    step: "04",
    title: "Submit",
    body: "Open a PR with pass rates, failure analysis, and artifacts for any multimodal outputs.",
  },
];

const YOUR_JOB = [
  "The prompt body — written by hand, in imperative prose",
  "The oracle solution, deriving the answer by computation",
  "The scientific judgement about what counts as correct",
  "The claim that this reflects real research practice",
];

const AI_CAN_HELP = [
  "Dockerfile scaffolding and pinning dependencies",
  "Boilerplate for the verifier test harness",
  "Formatting metadata and frontmatter",
  "Tidying prose you have already written",
];

const CHECKS = [
  "bench tasks check tasks/<task-id>",
  "bench eval run --tasks-dir tasks/<task-id> --agent oracle --sandbox docker",
];

export default function Contribute() {
  return (
    <main className="max-w-3xl mx-auto px-4 md:px-8 pt-32 pb-8">
      <header className="space-y-5 mb-16">
        <p className="font-mono text-xs uppercase tracking-widest text-muted-foreground">
          Contribute
        </p>
        <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-[1.05]">
          Turn research you have already done into a benchmark task
        </h1>
        <p className="text-lg text-muted-foreground leading-relaxed">
          No AI background required. The hard part is the physics, and you have
          already done that part.
        </p>

        <div className="flex items-start gap-4 rounded-2xl border border-chart-2/40 bg-chart-2/5 p-6">
          <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-chart-2/15 text-chart-2">
            <Award className="h-5 w-5" aria-hidden="true" />
          </span>
          <div className="space-y-3">
            <h2 className="font-semibold tracking-tight">
              Earn {credit.authorship} points, become a co-author
            </h2>
            <p className="text-sm text-muted-foreground leading-relaxed">
              A task you authored is worth{" "}
              <strong className="font-semibold text-foreground">
                {credit.task} points
              </strong>{" "}
              when it merges; a task you reviewed is worth{" "}
              <strong className="font-semibold text-foreground">
                {credit.review}
              </strong>
              . At{" "}
              <strong className="font-semibold text-foreground">
                {credit.authorship} points
              </strong>{" "}
              you are a co-author on the FrontierPhysics paper and the released
              dataset — {tasksForAuthorship} authored tasks, or any mix of
              authoring and reviewing that adds up.
            </p>
            <p className="text-sm text-muted-foreground leading-relaxed">
              <em>Merged</em> is the operative word. Points land on merge, not on
              submission, and each task has to clear the bar below.
            </p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 pt-2">
          <Button asChild>
            <a href={site.contributing} target="_blank" rel="noopener noreferrer">
              Full contributor guide
              <ArrowUpRight className="h-4 w-4" aria-hidden="true" />
            </a>
          </Button>
          <Button asChild variant="secondary" className="border border-border">
            <a href={site.discord} target="_blank" rel="noopener noreferrer">
              Ask a maintainer first
            </a>
          </Button>
        </div>
      </header>

      <section className="space-y-6 mb-20">
        <div className="space-y-3">
          <h2 className="text-2xl font-bold tracking-tight">
            What makes a good task
          </h2>
          <p className="text-muted-foreground leading-relaxed">
            All three at once. A task that misses any one of them will not
            merge.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
          {CRITERIA.map((item) => (
            <div
              key={item.title}
              className="flex flex-col rounded-2xl border border-border bg-card p-6"
            >
              <span
                className={`inline-flex h-10 w-10 items-center justify-center rounded-xl ${item.tint} ${item.accent} mb-4`}
              >
                <item.icon className="h-5 w-5" aria-hidden="true" />
              </span>
              <h3 className="font-semibold tracking-tight mb-2">
                {item.title}
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed grow">
                {item.body}
              </p>
              <p className="mt-4 pt-4 border-t border-border text-sm font-medium">
                {item.check}
              </p>
            </div>
          ))}
        </div>

        <p className="border-l-2 border-border pl-4 text-sm text-muted-foreground leading-relaxed">
          Quality beats quantity — one excellent task is worth more than many
          mediocre ones.
        </p>
      </section>

      <section className="space-y-6 mb-20">
        <h2 className="text-2xl font-bold tracking-tight">The four steps</h2>
        <ol className="space-y-6">
          {STEPS.map((item) => (
            <li key={item.step} className="flex gap-5">
              <span className="font-mono text-sm text-muted-foreground pt-0.5 shrink-0">
                {item.step}
              </span>
              <div className="space-y-1.5">
                <h3 className="font-semibold tracking-tight">{item.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {item.body}
                </p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section className="space-y-6 mb-20">
        <div className="space-y-3">
          <h2 className="text-2xl font-bold tracking-tight">
            What you must write yourself
          </h2>
          <p className="text-muted-foreground leading-relaxed">
            You can use an AI assistant for the software plumbing. The science
            has to be yours — a benchmark built from generated physics measures
            nothing.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div className="rounded-2xl border border-border bg-card p-6 space-y-4">
            <h3 className="font-semibold tracking-tight text-sm">
              Never delegate
            </h3>
            <ul className="space-y-2.5">
              {YOUR_JOB.map((item) => (
                <li key={item} className="flex gap-2.5 text-sm">
                  <X
                    className="h-4 w-4 shrink-0 mt-0.5 text-chart-1"
                    aria-hidden="true"
                  />
                  <span className="text-muted-foreground leading-relaxed">
                    {item}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          <div className="rounded-2xl border border-border bg-card p-6 space-y-4">
            <h3 className="font-semibold tracking-tight text-sm">
              Fine to delegate
            </h3>
            <ul className="space-y-2.5">
              {AI_CAN_HELP.map((item) => (
                <li key={item} className="flex gap-2.5 text-sm">
                  <Check
                    className="h-4 w-4 shrink-0 mt-0.5 text-chart-2"
                    aria-hidden="true"
                  />
                  <span className="text-muted-foreground leading-relaxed">
                    {item}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      <section className="space-y-6 mb-20">
        <div className="space-y-3">
          <h2 className="text-2xl font-bold tracking-tight">
            Before you open the PR
          </h2>
          <p className="text-muted-foreground leading-relaxed">
            Both commands have to pass, and the oracle has to come back with
            reward 1.0.
          </p>
        </div>
        <pre className="rounded-2xl border border-border bg-card p-6 overflow-x-auto text-xs sm:text-sm font-mono leading-loose text-muted-foreground">
          {CHECKS.join("\n")}
        </pre>
        <p className="text-sm text-muted-foreground">
          Then run at least one agent with and without skills, and put the pass
          rates and failure analysis in the PR description. The prompt must
          never mention a skill by name, and the verifier must check the
          science, not which tools the agent reached for.
        </p>
      </section>

      <section className="rounded-2xl border border-border bg-card p-8 text-center space-y-5">
        <h2 className="text-2xl font-bold tracking-tight">
          Ten minutes of triage can save a weekend
        </h2>
        <p className="text-muted-foreground max-w-lg mx-auto leading-relaxed">
          Bring your task idea to Discord before you build it. A maintainer will
          tell you quickly whether it clears the bar.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Button asChild>
            <a href={site.discord} target="_blank" rel="noopener noreferrer">
              Join Discord
            </a>
          </Button>
          <Button asChild variant="secondary" className="border border-border">
            <Link href="/#tasks">See existing tasks</Link>
          </Button>
        </div>
      </section>
    </main>
  );
}
