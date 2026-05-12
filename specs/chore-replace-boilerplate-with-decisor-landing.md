# Chore: Replace boilerplate with Decisor landing

**Issue**: #1
**Type**: chore

## Context

The Next.js app was bootstrapped with `create-next-app` and still ships its default landing page (Next.js logo, Vercel deploy links, getting-started copy) plus five boilerplate SVGs in `public/`. These need to be replaced with the minimal Decisor landing before any feature work begins.

## Files to create / modify / delete

- `app/page.tsx` — replace boilerplate hero with Decisor heading, subtitle, and empty card placeholder
- `app/layout.tsx` — update `metadata` to `title: "Decisor"` and a short Spanish description
- `public/next.svg` — delete (unused boilerplate asset)
- `public/vercel.svg` — delete (unused boilerplate asset)
- `public/file.svg` — delete (unused boilerplate asset)
- `public/globe.svg` — delete (unused boilerplate asset)
- `public/window.svg` — delete (unused boilerplate asset)

## Steps

1. Read `app/layout.tsx` and update the `metadata` export:
   - `title`: `"Decisor"`
   - `description`: `"El sorteador de opciones cuando no podés decidir"`
2. Rewrite `app/page.tsx` with a full-height centered layout (Tailwind):
   - `<h1>` with the text **Decisor**
   - `<p>` subtitle: "El sorteador de opciones cuando no podés decidir"
   - An empty `<div>` styled with rounded corners and a subtle border as a card placeholder
   - Keep the existing Geist font variables that come from `layout.tsx` (no new font imports)
3. Delete all five boilerplate SVGs from `public/` (`next.svg`, `vercel.svg`, `file.svg`, `globe.svg`, `window.svg`).
4. Verify no remaining imports or references to the deleted SVGs exist in the codebase.

## Verification

- [ ] `app/layout.tsx` `metadata.title` is `"Decisor"` and `metadata.description` matches the subtitle copy
- [ ] `app/page.tsx` renders a heading "Decisor", the subtitle, and an empty card `<div>` with no other content
- [ ] None of the five deleted SVGs are referenced anywhere in the codebase
- [ ] `public/` contains only `favicon.ico` (no boilerplate SVGs remain)
- [ ] `npm run build` completes without errors
- [ ] No new dependencies were added to `package.json`
