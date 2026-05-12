# Bug fix: dark theme does not persist on refresh

**Issue**: #11
**Type**: bug

## Symptom
After toggling to dark mode and refreshing the page, the page renders in light mode while the toggle button shows the sun icon (indicating dark mode is active). Theme and toggle are out of sync.

## Root cause
`app/layout.tsx:27–30` — the `<html>` element is rendered on the server **without** the `dark` class. The inline `<script>` in `<head>` correctly adds `dark` to `document.documentElement` before paint, but React hydration then reconciles the DOM against the server-rendered VDOM (which has no `dark` class) and **removes** it.

Sequence on refresh with dark mode in localStorage:
1. Server renders `<html className="[fonts] h-full antialiased">` — no `dark`.
2. Browser parses `<head>`, inline script runs synchronously, `dark` added to `<html>`.
3. `ThemeToggle` client init: `document.documentElement.classList.contains('dark')` → `true`, so `isDark = true` (sun icon).
4. React hydration detects className mismatch (`[fonts] h-full antialiased dark` vs server's `[fonts] h-full antialiased`) and removes `dark` to match the server state.
5. Result: `isDark = true` (sun icon) but no `dark` class → page is light.

The localStorage key is consistent between the inline script and `ThemeToggle` (`'decisor:theme:v1'`), so that is not the issue. The Tailwind `@variant dark` rule is also correct.

## Files to modify
- `app/layout.tsx` — add `suppressHydrationWarning` to the `<html>` element so React does not reconcile the `dark` class injected by the inline script.

## Fix steps
1. In `app/layout.tsx`, add the `suppressHydrationWarning` prop to the `<html>` element:
   ```tsx
   <html
     lang="en"
     suppressHydrationWarning
     className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
   >
   ```

## Verification
- [ ] Toggle to dark mode, refresh — page renders dark with no flash of light theme.
- [ ] Toggle to light mode, refresh — page renders light.
- [ ] Toggle icon stays in sync with the applied theme after each refresh.
- [ ] Regression: font variables (`--font-geist-sans`, `--font-geist-mono`) and base classes (`h-full antialiased`) still applied after refresh.
