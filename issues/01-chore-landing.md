## Replace create-next-app boilerplate with a minimal Decisor landing page

The freshly created Next.js app ships with the default `create-next-app` landing page (Next logo, Vercel/deploy links, getting-started instructions). We need to replace it with a clean landing for the **Decisor** app.

### Requirements

- `app/page.tsx` should render a centered layout with:
  - A large heading: **Decisor**
  - A short subtitle: "El sorteador de opciones cuando no podés decidir"
  - An empty card placeholder (`<div>` with rounded corners and a subtle border) where the rest of the UI will live in future issues. No content inside yet.
- Remove unused boilerplate assets in `public/` that came from `create-next-app` (e.g. `next.svg`, `vercel.svg`, etc.).
- `app/layout.tsx`: update the `metadata` export with `title: "Decisor"` and a short description.
- Keep Tailwind. Keep the existing font setup. No new dependencies.

### Out of scope

- Functionality. This is purely the empty landing.
- Dark mode (separate issue).
