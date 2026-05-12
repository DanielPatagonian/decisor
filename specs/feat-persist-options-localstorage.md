# Feature: Persist options in localStorage

**Issue**: #4
**Type**: feature

## Context

Options added by the user are currently held only in React state and are lost on page reload. This feature persists the `options` array to `localStorage` under the key `decisor:options:v1` so that the list survives a full page reload. The read must happen inside a `useEffect` (not during render) to avoid Next.js hydration mismatches, since `localStorage` is browser-only.

## Files to create

- `lib/use-local-storage.ts` — Custom hook `useLocalStorage<T>(key: string, initialValue: T): [T, Dispatch<SetStateAction<T>>]` that:
  1. Initializes state with `initialValue` (used during SSR/first render).
  2. Reads from `localStorage` on mount via a `useEffect` with an empty dependency array; if parsing fails or the key is missing, keeps `initialValue`.
  3. Writes back to `localStorage` on every state change via a second `useEffect` that depends on the state value.
  4. Returns the same `[value, setValue]` tuple as `useState` so callers are a drop-in swap.

## Files to modify

- `components/OptionsList.tsx` — Replace `useState<string[]>([])` for `options` with `useLocalStorage<string[]>('decisor:options:v1', [])` imported from `lib/use-local-storage`. No other logic changes.

## Implementation steps

1. Create `lib/use-local-storage.ts` with the following signature:
   ```ts
   export function useLocalStorage<T>(
     key: string,
     initialValue: T
   ): [T, React.Dispatch<React.SetStateAction<T>>]
   ```
2. Inside the hook, initialize state with `initialValue`:
   ```ts
   const [storedValue, setStoredValue] = useState<T>(initialValue)
   ```
3. Add a read-on-mount `useEffect` (empty dep array) that calls `localStorage.getItem(key)`, parses the JSON, and calls `setStoredValue` with the result. Wrap in try/catch; on any error keep `initialValue`.
4. Add a write-on-change `useEffect` that depends on `[key, storedValue]` and calls `localStorage.setItem(key, JSON.stringify(storedValue))`. Wrap in try/catch and silently swallow errors (storage full, private mode, etc.).
5. Return `[storedValue, setStoredValue]`.
6. In `components/OptionsList.tsx`:
   - Add import: `import { useLocalStorage } from '../lib/use-local-storage'`
   - Change line 6 from:
     ```ts
     const [options, setOptions] = useState<string[]>([])
     ```
     to:
     ```ts
     const [options, setOptions] = useLocalStorage<string[]>('decisor:options:v1', [])
     ```
   - Remove `useState` from the React import if it is no longer used elsewhere (it is still used for `inputValue`, `showDuplicate`, `spinning`, `displayLabel`, and `result`, so keep it).

## Acceptance criteria

- [ ] Adding "pizza", "sushi", "empanadas" and reloading the page shows all three options.
- [ ] Removing "sushi" and reloading shows only "pizza" and "empanadas".
- [ ] No hydration-mismatch warnings appear in the browser console.
- [ ] A corrupt or missing `decisor:options:v1` key in localStorage results in an empty list (no crash).
- [ ] The hook is typed generically and the `OptionsList` component type-checks cleanly (`tsc --noEmit`).

## Out of scope

- Syncing options across browser tabs.
- Versioned data migrations beyond the `:v1` key suffix.
- Persisting any other state (e.g. `result`, `spinning`).
