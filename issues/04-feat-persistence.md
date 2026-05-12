## Persist options in localStorage

Options should survive a page reload.

### Requirements

- On mount (client-side only), read options from `localStorage` under key `decisor:options:v1`. If parsing fails or the key is missing, fall back to an empty array.
- Whenever the options list changes, write the new list back to `localStorage` under the same key.
- Make sure this is safe for Next.js: localStorage is only available in the browser, so the read must happen inside `useEffect` (not during render) to avoid hydration mismatches.

### Acceptance

- Add "pizza", "sushi", "empanadas". Reload the page. The three options are still there.
- Remove "sushi", reload. Only "pizza" and "empanadas" remain.
- No hydration-mismatch warnings in the browser console.

### Out of scope

- Sync across tabs.
- Versioned migrations beyond the `:v1` suffix.

### Implementation hint

Two `useEffect`s: one for read-on-mount (empty dep array), one for write-on-change (dep on the options array). Or one custom `useLocalStorage` hook in `lib/use-local-storage.ts`.
