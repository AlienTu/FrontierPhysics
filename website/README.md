# FrontierPhysics website

A static marketing + onboarding site for FrontierPhysics, aimed at practising physicists
who may never have used an AI agent. It lives in this repository so the site and the
benchmark it describes stay in sync.

No build step, no framework, no dependencies. Plain HTML, one CSS file, one JS file.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Landing page: plain-language glossary, paired-evaluation explainer, why contribute, task anatomy, example tasks, SkillsBench paper, FAQ |
| `contribute.html` | The hands-on task-authoring guide — eight steps, with an explicit "what to delegate to AI / what never to delegate" boundary |
| `tasks.html` | Task registry with per-task detail, the wanted-subfields list, and the metadata taxonomy |
| `assets/css/style.css` | All styles (design tokens at the top) |
| `assets/js/main.js` | Mobile nav, copy buttons, scroll reveal, TOC scroll-spy |
| `assets/paper/skillsbench.pdf` | The SkillsBench paper, linked from the landing page |

## Run locally

```bash
cd website
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy

Any static host works — there is nothing to build, so the deploy is a file copy.

For Netlify / Vercel / Cloudflare Pages: point the project at this repository, leave
the build command empty, and set the publish directory to `website`.

For GitHub Pages: the branch-based source only serves `/` or `/docs`, so publishing
from `website/` needs a workflow that uploads this directory as the Pages artifact
(`actions/upload-pages-artifact` with `path: website`). No such workflow is wired up
yet.

## Editing notes

- **Colours, spacing, radii** are CSS custom properties in the `:root` block at the top of
  `style.css`. Change `--accent` to restyle the whole site.
- **The header and footer are duplicated** in each HTML file (deliberate — it keeps the site
  buildless). If you change one, change all three.
- **Task cards** on `index.html` and `tasks.html` are hand-written from the `task.md` front matter
  in [`../tasks/`](../tasks). When a task is added, add a card in both places and update the counts in the
  hero stat strip and the two "four tasks" mentions.
- **Numbers cited from the paper**: 87 tasks / 8 domains, 33.9% → 50.5% (+16.6 pp) across 18
  model–harness configurations, +28.8 pp in natural science, 142 contributors. Keep these in sync
  with the current version of `skillsbench.pdf`.
- **Accessibility**: skip link, focus-visible outlines, `prefers-reduced-motion` respected,
  colour contrast checked against WCAG AA for body text.
