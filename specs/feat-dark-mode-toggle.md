# Feature: Dark Mode Toggle

**Issue**: #5
**Type**: feature

## Context

Decisor needs a light/dark theme toggle so users can choose their preferred color scheme. The toggle must respect OS preference on first visit, persist the choice in `localStorage`, and avoid a flash of the wrong theme on reload via an inline script before React hydrates.

## Files to create

- `components/ThemeToggle.tsx` — client component rendering a fixed-position button (top-right) with inline SVG sun/moon icons; reads initial state from the `<html>` class set by the inline script, and on click toggles the `dark` class on `document.documentElement` while persisting to `localStorage` under `decisor:theme:v1`.

## Files to modify

- `app/globals.css` — Add `@variant dark (&:is(.dark, .dark *));` after the `@import "tailwindcss"` line. This switches Tailwind v4 from media-query-based dark mode to class-based dark mode (there is no `tailwind.config.ts` in this project — Tailwind v4 is configured via CSS). Also remove the `@media (prefers-color-scheme: dark)` block that sets CSS vars since theme is now class-driven.
- `app/layout.tsx` — (1) Add an explicit `<head>` element containing a synchronous inline `<script dangerouslySetInnerHTML>` that reads `localStorage.getItem('decisor:theme:v1')` and falls back to `window.matchMedia('(prefers-color-scheme: dark)').matches`, then adds the `dark` class to `document.documentElement` before paint. (2) Import and render `<ThemeToggle />` as a sibling to `{children}` inside `<body>`.
- `app/page.tsx` — Change `dark:bg-black` on the outer `<div>` to `dark:bg-zinc-900` so the background is not pure black.

## Implementation steps

1. **`app/globals.css`**: On line 1 (right after `@import "tailwindcss"`), add:
   ```css
   @variant dark (&:is(.dark, .dark *));
   ```
   Then delete the `@media (prefers-color-scheme: dark)` block (lines ~9-13). The CSS custom properties (`--background`, `--foreground`) can be removed entirely since no component uses `var(--background)` or `var(--foreground)` directly — all colours are Tailwind utilities. Remove the `body { background: var(--background); color: var(--foreground); }` rule too, or replace it with `body { font-family: Arial, Helvetica, sans-serif; }` (the font-family is the only useful line there).

2. **`components/ThemeToggle.tsx`**: Create as a `'use client'` component.
   - State: `const [isDark, setIsDark] = useState(false)`.
   - `useEffect(() => { setIsDark(document.documentElement.classList.contains('dark')) }, [])` — initialises from the class already set by the inline script; avoids SSR mismatch.
   - `toggle()`: compute `next = !isDark`, call `document.documentElement.classList.toggle('dark', next)`, `localStorage.setItem('decisor:theme:v1', next ? 'dark' : 'light')`, `setIsDark(next)`.
   - Button classes: `fixed top-4 right-4 z-50 rounded-full p-2 bg-zinc-100 text-zinc-800 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-100 dark:hover:bg-zinc-700 transition-colors`.
   - When `isDark` is `true` render the **sun** SVG (so clicking switches to light); when `false` render the **moon** SVG (so clicking switches to dark). Use inline SVG, `width="20" height="20"`, `viewBox="0 0 24 24"`, `fill="none"`, `stroke="currentColor"`, `strokeWidth="2"`.
     - Moon path: `<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />` (crescent).
     - Sun: circle `cx="12" cy="12" r="5"` plus 8 ray lines (use the standard Feather sun icon paths).
   - Add `aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}`.

3. **`app/layout.tsx`**: 
   - Add `<head>` block before `<body>` containing the no-flash inline script:
     ```tsx
     <head>
       <script
         dangerouslySetInnerHTML={{
           __html: `(function(){try{var t=localStorage.getItem('decisor:theme:v1');if(t==='dark'||(!t&&window.matchMedia('(prefers-color-scheme: dark)').matches)){document.documentElement.classList.add('dark')}}catch(e){}})();`,
         }}
       />
     </head>
     ```
   - Import `ThemeToggle` from `'@/components/ThemeToggle'` and render it inside `<body>` before `{children}`:
     ```tsx
     <body className="min-h-full flex flex-col">
       <ThemeToggle />
       {children}
     </body>
     ```

4. **`app/page.tsx`**: Change the outer `<div>`'s `dark:bg-black` to `dark:bg-zinc-900`.

5. **Verify**: All existing `dark:` variants in `OptionsList.tsx` and `page.tsx` already use appropriate zinc shades and require no further changes. Confirm the `dark:` prefix works with class-based mode by checking one or two classes manually.

## Acceptance criteria

- [ ] First visit with OS dark mode preference active → page renders dark without flash.
- [ ] First visit with OS light mode preference → page renders light.
- [ ] Clicking the toggle button flips the theme instantly, no page reload.
- [ ] The chosen theme is saved: a hard reload preserves the selection.
- [ ] The button shows a moon icon in light mode and a sun icon in dark mode.
- [ ] No pure-black backgrounds: the page background in dark mode uses `zinc-900` or a similar non-black shade.
- [ ] No new icon library is added to `package.json`.
- [ ] All existing UI elements (card border, input, list items, Decidir button, result display) render correctly in both modes.

## Out of scope

- A three-way system/light/dark toggle.
- Theming beyond what is already present in the existing Tailwind `dark:` utility classes.
- Animating the theme transition.
