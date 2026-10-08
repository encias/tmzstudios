# TEMİZ STUDIO — tmzstudios.com

Portfolio site of **TEMİZ STUDIO**, a spatial and brand experience design studio run by Süleyman Temiz.

Live: https://tmzstudios.com

## What's inside

- `public/index.html` — single-page, bilingual (EN/TR) portfolio. Ten selected cases across events, exhibitions, brand experiences and interiors.
- Scroll-scrubbed hero video (`scene_1_kling25_correct_landscape_seek.mp4`) driven by GSAP ScrollTrigger (`lib/`).
- `selected_work_final/` and `gratis_final/` — optimised desktop (JPG) and mobile (WebP) renders.

## How it's built

The studio runs on **Hermes**, its own AI agent operating system (Claude + local models). The same agents that handle research, visual exploration and production tracking wrote and maintain this site: Codex and Claude Code built the page, Claude Code added the studio-system section and set up the domain, mail routing and deployment.

Static site — no build step. Deployed on Cloudflare Workers (static assets) via `npx wrangler deploy`.

```bash
npx http-server public -p 8080
```

## Contact

suleyman@tmzstudios.com

© 2026 TEMİZ STUDIO. Renders and video are the studio's work; please do not reuse them without permission.
