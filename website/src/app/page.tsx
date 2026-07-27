import { HeroBackground } from "@/components/HeroBackground";
import { Button } from "@/components/ui/button";
import { credit, site, tasksForAuthorship } from "@/lib/site";
import { getTasks } from "@/lib/tasks";
import { ArrowRight, ArrowUpRight, Award } from "lucide-react";
import Link from "next/link";

const PACKAGE_TREE = `tasks/<task-id>/
  task.md            # prompt + metadata
  environment/
    Dockerfile       # frozen environment
    skills/          # mentor skills
  oracle/
    solve.sh         # must reach reward 1.0
  verifier/
    test.sh
    test_outputs.py  # checks the science`;

export default function Home() {
  const tasks = getTasks();

  return (
    <div className="flex flex-col min-h-screen relative text-foreground overflow-x-hidden">
      <main className="flex-1">
        <section className="flex flex-col items-center justify-center min-h-[78vh] text-center space-y-8 relative z-10 px-4 pt-20 overflow-hidden">
          <HeroBackground />
          {/* Softens the grid directly behind the headline so the type stays legible. */}
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-3xl h-full max-h-128 bg-background/60 blur-hero -z-10 rounded-full pointer-events-none" />

          <div className="space-y-6">
            <Link
              href="/contribute"
              className="inline-flex items-center rounded-full border border-chart-2/50 px-4 py-1.5 text-xs font-medium bg-chart-2/10 text-foreground backdrop-blur-md hover:bg-chart-2/20 hover:border-chart-2 transition-[background-color,border-color] duration-300 group"
            >
              <span className="w-2 h-2 rounded-full bg-chart-2 mr-2 animate-pulse shadow-glow" />
              Work in progress · accepting task contributions
              <ArrowRight className="ml-1.5 h-3 w-3 transition-transform group-hover:translate-x-0.5" />
            </Link>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight leading-[1.05] max-w-3xl mx-auto">
              Are AI agents good physicists?
            </h1>

            <p className="max-w-xl mx-auto text-lg text-foreground/80 leading-relaxed">
              FrontierPhysics: Benchmark how AI agents do frontier physics
              research.
            </p>
          </div>

          <div className="flex flex-col items-center gap-5 pt-2">
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <Button asChild>
                <Link href="/contribute">Contribute a task</Link>
              </Button>
              <Button
                asChild
                variant="secondary"
                className="border border-border hover:bg-accent transition-colors"
              >
                <a href={site.repo} target="_blank" rel="noopener noreferrer">
                  View on GitHub
                </a>
              </Button>
            </div>

            <p className="max-w-lg text-sm text-muted-foreground leading-relaxed">
              <Award
                className="inline-block h-4 w-4 -mt-0.5 mr-1.5 text-chart-2"
                aria-hidden="true"
              />
              A merged task earns{" "}
              <strong className="font-semibold text-foreground">
                {credit.task} points
              </strong>
              , a review earns{" "}
              <strong className="font-semibold text-foreground">
                {credit.review}
              </strong>
              . At{" "}
              <strong className="font-semibold text-foreground">
                {credit.authorship}
              </strong>{" "}
              you are a{" "}
              <strong className="font-semibold text-foreground">
                co-author
              </strong>
              .
            </p>
          </div>
        </section>

        <div className="max-w-5xl mx-auto px-4 md:px-8 py-12 space-y-28">
          <section id="anatomy" className="scroll-mt-28">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-start">
              <div className="space-y-4">
                <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">
                  What a task looks like
                </h2>
                <p className="text-muted-foreground leading-relaxed">
                  A task is a native BenchFlow <code className="font-mono text-sm">task.md</code>{" "}
                  package. The prompt describes an outcome and never names a
                  skill. The oracle has to pass with reward 1.0 before any agent
                  is run.
                </p>
                <p className="text-muted-foreground leading-relaxed">
                  Prompt bodies and oracle logic are human-authored — that rule
                  is what keeps the benchmark grounded in real research rather
                  than in generated exercises.
                </p>
                <Button
                  asChild
                  variant="secondary"
                  size="sm"
                  className="border border-border"
                >
                  <a
                    href={site.contributing}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Read the contributor guide
                    <ArrowUpRight className="h-4 w-4" aria-hidden="true" />
                  </a>
                </Button>
              </div>

              <pre className="rounded-2xl border border-border bg-card p-6 overflow-x-auto text-xs sm:text-sm font-mono leading-relaxed text-muted-foreground">
                {PACKAGE_TREE}
              </pre>
            </div>
          </section>

          <section id="tasks" className="scroll-mt-28">
            <div className="mb-10 space-y-3">
              <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">
                Tasks in the repository
              </h2>
              <p className="text-muted-foreground max-w-2xl leading-relaxed">
                The public set is small and early — these are the tasks merged
                so far. There is no leaderboard yet; results are published once
                the task set is large enough to mean something.
              </p>
            </div>

            {tasks.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {tasks.map((task) => (
                  <a
                    key={task.id}
                    href={`${site.tasksTree}/${task.id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="group rounded-2xl border border-border bg-card p-6 space-y-3 hover:border-foreground/25 transition-colors"
                  >
                    <div className="flex items-start justify-between gap-3">
                      <h3 className="font-mono text-sm font-semibold tracking-tight">
                        {task.id}
                      </h3>
                      <ArrowUpRight
                        className="h-4 w-4 shrink-0 text-muted-foreground transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
                        aria-hidden="true"
                      />
                    </div>

                    <div className="flex flex-wrap gap-1.5">
                      {[task.difficulty, task.subcategory, ...task.taskTypes]
                        .filter(Boolean)
                        .map((tag) => (
                          <span
                            key={tag}
                            className="rounded-full border border-border bg-muted px-2.5 py-0.5 text-xxs font-medium text-muted-foreground"
                          >
                            {tag}
                          </span>
                        ))}
                    </div>

                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {task.summary}
                    </p>
                  </a>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                No task packages found in this checkout.
              </p>
            )}
          </section>

          <section className="rounded-2xl border border-border bg-card p-8 sm:p-10 text-center space-y-5">
            <span className="inline-flex items-center gap-2 rounded-full border border-chart-2/50 bg-chart-2/10 px-4 py-1.5 text-xs font-medium">
              <Award className="h-3.5 w-3.5 text-chart-2" aria-hidden="true" />
              What you get
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">
              Earn {credit.authorship} points, become a co-author
            </h2>
            <p className="text-muted-foreground max-w-xl mx-auto leading-relaxed">
              Credit is tracked in points, and {credit.authorship} of them earns
              co-authorship on the FrontierPhysics paper and the released
              dataset. Reviewing counts too, so you can get there by authoring{" "}
              {tasksForAuthorship} tasks, by reviewing, or by any mix that adds
              up.
            </p>

            <dl className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl mx-auto pt-2 text-left">
              {[
                {
                  points: `+${credit.task}`,
                  label: "A task you authored is merged",
                },
                {
                  points: `+${credit.review}`,
                  label: "A task you reviewed is merged",
                },
                {
                  points: credit.authorship,
                  label: "Co-authorship on the paper and dataset",
                },
              ].map((row) => (
                <div
                  key={row.label}
                  className="rounded-xl border border-border bg-background p-4"
                >
                  <dt className="text-2xl font-bold tracking-tight tabular-nums">
                    {row.points}
                  </dt>
                  <dd className="mt-1 text-sm text-muted-foreground leading-relaxed">
                    {row.label}
                  </dd>
                </div>
              ))}
            </dl>

            <p className="text-muted-foreground max-w-xl mx-auto leading-relaxed">
              No AI background required — if you can explain your analysis to a
              new graduate student, you can author a task, and a maintainer will
              walk you through the rest.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-1">
              <Button asChild>
                <Link href="/contribute">Start your first task</Link>
              </Button>
              <Button
                asChild
                variant="secondary"
                className="border border-border"
              >
                <a href={site.discord} target="_blank" rel="noopener noreferrer">
                  Ask on Discord
                </a>
              </Button>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
