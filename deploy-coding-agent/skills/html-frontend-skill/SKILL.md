---
name: html-frontend-skill
description: Build a polished, good-looking HTML/CSS (and optional JS) frontend page and write it to files. Use when the user asks for an HTML page, landing page, dashboard mock, static site, or “make it look good” UI work without a framework.
---

# HTML Frontend Skill

Use this skill when the user asks you to create **a frontend page using plain HTML/CSS/JS** (no React/Vue unless explicitly requested), especially when the user wants it to look **beautiful** and be **ready to open in a browser**.

## What to Produce

Prefer a small, clear file set:

- `index.html` (required)
- `styles.css` (required)
- `app.js` (optional; only if interaction is requested)
- `assets/` (optional; only if you generate or download assets)

Keep the page self-contained and runnable by opening `index.html` directly unless the user asks for a build tool.

## When to Use Tools

### 1) Plan if the request is non-trivial

If the page has multiple sections, interactions, or a specific aesthetic, first call `write_todos` to outline:
- file list to create
- layout/components (hero, nav, cards, etc.)
- typography/color/motion decisions
- test/preview steps

### 2) Explore existing repo patterns (only if needed)

If the user wants the page integrated into an existing app, use:
- `glob` / `grep` to find existing frontend folders, routing, or static hosting
- `read_file` to match existing style and conventions

If it’s a standalone page, skip repo exploration.

### 3) Write real files (don’t just paste code)

Use `write_file` to create:
- `index.html`
- `styles.css`
- `app.js` (if needed)

Then use `edit_file` for quick iterations (spacing, colors, animations, copy).

### 4) Preview locally

Default preview guidance (safe, non-blocking):
- Tell the user they can open `index.html` directly in a browser.

If a local server is needed (relative imports, fetch, SPA routing, etc.):
- Prefer to **print** the command the user should run in their own terminal rather than running it yourself, because `python -m http.server ...` is a long-running process and will block `execute`.
- Provide the exact command and port, e.g. `python -m http.server 5173`, and instruct the user to open `http://localhost:5173/`.

Only run a server via `execute` if the user explicitly asks you to start it. If you do start it, warn that it will keep running until stopped (Ctrl+C) and may appear “stuck” by design.

## Design & Implementation Guidelines

- **Commit to an aesthetic**: pick a strong direction (editorial, brutalist, retro-futuristic, luxury, playful, etc.) and execute it consistently.
- **Typography**: choose distinctive fonts via Google Fonts (link in `index.html`), pair display + body fonts, and tune sizes/line-heights carefully.
- **Color system**: define CSS variables (`:root { --bg: ... }`) and use them consistently.
- **Layout**: use modern CSS (flex/grid), intentional spacing scale, responsive breakpoints.
- **Motion**: add a few high-impact animations (page-load reveal, hover states) using CSS only unless JS is required.
- **Accessibility basics**: semantic HTML, proper contrast, focus states for interactive elements.
- **Avoid “generic AI look”**: no default centered-card stack with bland gradients; make intentional choices.

## Output Requirements

When finished:
- Ensure files are written to disk (via `write_file`/`edit_file`), not only shown in chat.
- Provide the relative paths you created.
- Provide a short “how to run / preview” instruction (open file or `http.server`).

