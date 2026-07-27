export const site = {
  name: "FrontierPhysics",
  tagline: "Are AI agents good physicists?",
  description:
    "FrontierPhysics is an open benchmark measuring whether AI agents can carry out authentic, specialist-level physics research.",
  repo: "https://github.com/benchflow-ai/FrontierPhysics",
  discord: "https://discord.gg/G9dg3EfSva",
  contributing:
    "https://github.com/benchflow-ai/FrontierPhysics/blob/main/CONTRIBUTING.md",
  protocol:
    "https://github.com/benchflow-ai/FrontierPhysics/blob/main/docs/benchmark-protocol.md",
  taxonomy:
    "https://github.com/benchflow-ai/FrontierPhysics/blob/main/taxonomy.md",
  tasksTree: "https://github.com/benchflow-ai/FrontierPhysics/tree/main/tasks",
  benchflow: "https://github.com/benchflow-ai/benchflow",
} as const;

/**
 * The authorship policy, mirrored from CONTRIBUTING.md#authorship-policy.
 * Everything the site says about credit is derived from these three numbers,
 * so the copy cannot drift out of step with itself.
 */
export const credit = {
  /** Points for a task you authored being merged. */
  task: 4,
  /** Points for a task you reviewed being merged. */
  review: 1,
  /** Points that earn co-authorship on the paper and dataset. */
  authorship: 12,
} as const;

/** Merged tasks needed to reach co-authorship on authoring alone. */
export const tasksForAuthorship = credit.authorship / credit.task;

export const navItems = [
  { href: "/#anatomy", label: "Task format" },
  { href: "/#tasks", label: "Tasks" },
  { href: "/contribute", label: "Contribute" },
] as const;
