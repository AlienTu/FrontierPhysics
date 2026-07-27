# FrontierPhysics website

The public site for [FrontierPhysics](https://github.com/benchflow-ai/FrontierPhysics),
built with Next.js and Tailwind. The design follows the
[SkillsBench site](https://github.com/benchflow-ai/skillsbench/tree/main/website):
same tokens, navbar, and animated canvas hero — with the drifting lattice made
of atoms rather than grid squares — cut down to the two pages this benchmark
needs while it is still work in progress.

## Run locally

```bash
cd website
npm install
npm run dev
# open http://localhost:3000
```

`npm run build` produces the production build; `npm start` serves it.

## Pages

| Route | Purpose |
|---|---|
| `/` | Hero, how the paired evaluation works, task anatomy, live task list, contribution CTA |
| `/contribute` | What makes a good task, the four steps, the AI-delegation boundary, pre-PR checks |

## Layout

```text
src/
  app/
    layout.tsx        # navbar + footer + theme provider
    page.tsx          # landing page
    contribute/       # contributor guide
    globals.css       # design tokens
  components/
    Navbar.tsx        # floating pill nav with theme switcher
    Footer.tsx
    HeroBackground.tsx # animated atom field + vignette behind the hero
    Atoms.tsx         # canvas atom lattice, drifting diagonally
    ui/button.tsx
  lib/
    site.ts           # every external link the site points at
    tasks.ts          # reads ../tasks/*/task.md at build time
```

## Editing notes

- **Colours and radii** are CSS custom properties in `globals.css`. Both light
  and dark are defined; the navbar switcher writes `class="dark"` on `<html>`.
- **Task cards are generated**, not hand-written. `lib/tasks.ts` reads
  `../tasks/*/task.md` frontmatter at build time, so the list cannot drift out
  of sync with the repository the way a hand-maintained list would.
- **All outbound links live in `lib/site.ts`.** Change them in one place.
- **No benchmark results are published yet.** There is deliberately no
  leaderboard and no performance claim anywhere on the site — add those only
  when the task set is large enough to support them.

## Deploy

For Netlify / Vercel / Cloudflare Pages: point the project at this repository,
set the base directory to `website`, and use the default Next.js build.

Note that the build reads `../tasks/`, so the deploy needs the whole repository
checked out, not just this directory.
