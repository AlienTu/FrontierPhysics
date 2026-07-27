import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

export interface Task {
  id: string;
  difficulty?: string;
  subcategory?: string;
  taskTypes: string[];
  /** First paragraph of the prompt body, used as the card summary. */
  summary: string;
}

interface TaskFrontmatter {
  metadata?: {
    difficulty?: string;
    subcategory?: string;
    task_type?: string[];
  };
}

/**
 * Task cards are read from the repository's own `tasks/` directory at build
 * time rather than hand-written, so the site cannot drift out of sync with
 * what is actually published.
 */
export function getTasks(): Task[] {
  const tasksDir = path.join(process.cwd(), "..", "tasks");
  if (!fs.existsSync(tasksDir)) return [];

  const tasks: Task[] = [];

  for (const entry of fs.readdirSync(tasksDir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;

    const taskFile = path.join(tasksDir, entry.name, "task.md");
    if (!fs.existsSync(taskFile)) continue;

    const { data, content } = matter(fs.readFileSync(taskFile, "utf8"));
    const metadata = (data as TaskFrontmatter).metadata ?? {};

    const firstParagraph =
      content
        .split("\n\n")
        .map((block) => block.trim())
        .find((block) => block.length > 0 && !block.startsWith("#")) ?? "";

    tasks.push({
      id: entry.name,
      difficulty: metadata.difficulty,
      subcategory: metadata.subcategory,
      taskTypes: metadata.task_type ?? [],
      summary: truncate(firstParagraph.replace(/\s+/g, " "), 220),
    });
  }

  return tasks.sort((a, b) => a.id.localeCompare(b.id));
}

function truncate(text: string, max: number): string {
  if (text.length <= max) return text;
  return `${text.slice(0, text.lastIndexOf(" ", max))}…`;
}
