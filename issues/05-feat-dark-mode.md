## Dark mode toggle

A clean light/dark theme toggle.

### Requirements

- Add a small toggle button in the top-right corner of the page. Sun icon when in dark mode (so the user knows clicking switches to light), moon icon when in light mode. Use inline SVG icons; do not add a new icon library.
- On mount, the theme should be:
  1. Whatever is stored in `localStorage` under `decisor:theme:v1`, if set.
  2. Otherwise, follow the user's OS preference via `prefers-color-scheme: dark`.
- Toggling persists the new value to localStorage under the same key.
- Use Tailwind's `dark:` variants. Configure `darkMode: 'class'` in `tailwind.config.ts` (or `.js`) and toggle the `dark` class on `<html>`.
- Update all existing UI (landing text, card, input, list items, Decidir button, result display) to have appropriate dark-mode colors. Backgrounds should not be pure black; use a slate or zinc shade.

### Acceptance

- Page respects OS dark mode on first visit.
- Clicking the toggle flips colors instantly with no page reload.
- The choice survives reload (no flash of wrong theme on initial paint — a small inline script in `layout.tsx` to set the class before hydration is acceptable).

### Out of scope

- A "system / light / dark" three-way toggle. Just two states.

### Implementation hint

The classic "no flash" trick is a small synchronous `<script>` in `<head>` (via `app/layout.tsx`) that reads localStorage and adds the `dark` class to `<html>` before React hydrates.
