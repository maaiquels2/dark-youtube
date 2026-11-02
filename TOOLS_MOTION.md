# TOOLS_MOTION.md â€” HyperFrames + Impeccable (Claude Code)

Updated: 2026-10-24 (America/Sao_Paulo)

## HyperFrames (end cards / packaging motion)

**What:** HTML â†’ deterministic MP4. Free, local, no Grok tokens.
**Install path (skills):** `C:\Users\Admin\.claude\skills\hyperframes` (+ cli, registry, media-use)
**Also:** `C:\Users\Admin\.agents\skills\hyperframes*`
**Sample project:** `Dark YouTube\tools\hyperframes\endcard-walt\`
**Smoke test output:** `projects\grandpa-walt\out\hyperframes_endcard_test.mp4` (1920Ã—1080, 3s)

### Commands (from Dark YouTube)

```bat
cd tools\hyperframes\endcard-walt
npx --yes hyperframes@0.8.191 check
npx --yes hyperframes@0.8.191 render --output ..\..\projects\grandpa-walt\out\hyperframes_endcard_test.mp4
```

New project:

```bat
cd tools\hyperframes
npx --yes hyperframes init my-card
cd my-card
REM edit index.html then:
npm run check
npm run render
```

Refresh skills: `npx --yes hyperframes skills update`

**Use for:** Walt end cards, episode title cards, Cracked Ledger short packaging, thumbnails-as-video.
**Also use for (testado 28/10/2026):** cenas de explicação dos vídeos longos do Ledger (diagramas, contas, barras, listas; ver PADRAO_VIDEOS.md > Motion). **Do not use for:** porch clips of Walt face (keep Grok), or long era footage (ComfyUI / Wan).

## Impeccable (web UI anti-slop)

**What:** Claude/Cursor skill + 62 detector rules. No API key for `detect`.
**Global Claude skill:** `C:\Users\Admin\.claude\skills\impeccable`
**Creche project:** `Documents\Codex\2026-09-10\creche-arya-main\.claude\skills\impeccable` and `.cursor\skills\impeccable`
**Smoke detect JSON:** `Dark YouTube\tools\impeccable_creche_detect.json`

### Commands

In Claude Code chat (inside Creche or any project with the skill):

```
/impeccable init
/impeccable audit
/impeccable critique
```

CLI (no redesign, just findings):

```bat
cd C:\Users\Admin\Documents\Codex\2026-09-10\creche-arya-main
npx --yes impeccable detect index.html style.css
npx --yes impeccable detect --json .
```

Install elsewhere:

```bat
npx --yes impeccable install --providers=claude,cursor --scope=project --no-hooks
```

See also: `creche-arya-main\CRECHE_IMPECCABLE.md`

## Remotion (not installed)

HyperFrames alone covered the end-card smoke test, so Remotion was **not** installed.
npm unpacked sizes checked 2026-10-24 (packages only, not a full project): remotion@4.0.538 ~1.9 MB, @remotion/cli ~0.47 MB, @remotion/renderer ~2.8 MB. A real Remotion app still pulls Chromium/bundler deps and is much larger on disk. Prefer HyperFrames for HTML cards; revisit Remotion only for React template pipelines.

## Rules

- Spend nothing (no Grok video for these cards).
- Never touch Chrome profiles or `.env`.
- Nothing posts without user approval.