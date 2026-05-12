# Feature: Add and list options

**Issue**: #2
**Type**: feature

## Context

Users need a way to enter options into the Decisor before a decision can be made. This feature adds a text input and button to the placeholder card on the home page, plus a live-updating list below the input where entered options appear. It is the foundational data-entry step before any spin/decision logic.

## Files to create

- `components/OptionsList.tsx` — `"use client"` component that owns `options`, `inputValue`, and `duplicateError` state; renders the input row, the options list, and the empty-state helper text.

## Files to modify

- `app/page.tsx` — import and render `<OptionsList />` inside the placeholder card div; remove the fixed `h-48` height class (replace with `min-h-48` or `p-4`) so the card grows with the list.

## Implementation steps

1. **Read** `node_modules/next/dist/docs/` for any breaking-change notes relevant to client components and `"use client"` in this version of Next.js before writing any code.

2. **Create `components/OptionsList.tsx`** as a client component (`"use client"` at the top).

3. **Declare state** at the top of the component:
   ```ts
   const [options, setOptions] = useState<string[]>([]);
   const [inputValue, setInputValue] = useState('');
   const [showDuplicate, setShowDuplicate] = useState(false);
   ```

4. **Implement `addOption`** function:
   - Trim `inputValue`; do nothing if empty/whitespace.
   - Check for duplicate: `options.some(o => o.toLowerCase() === trimmed.toLowerCase())`.
     - If duplicate: set `showDuplicate(true)`, schedule `setShowDuplicate(false)` after 2000 ms (use `setTimeout`; clear it on cleanup to avoid state updates on unmounted component).
     - If not duplicate: `setOptions(prev => [...prev, trimmed])`, clear `inputValue`.

5. **Implement `removeOption`** function:
   - Filter out the option at the given index: `setOptions(prev => prev.filter((_, i) => i !== index))`.

6. **Render the input row**:
   ```tsx
   <div className="flex gap-2">
     <input
       type="text"
       value={inputValue}
       onChange={e => setInputValue(e.target.value)}
       onKeyDown={e => e.key === 'Enter' && addOption()}
       placeholder="Agregar una opción..."
       className="flex-1 rounded-lg border border-zinc-200 px-3 py-2 text-sm outline-none focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100"
     />
     <button
       onClick={addOption}
       className="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white hover:bg-zinc-700 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-300"
     >
       Agregar
     </button>
   </div>
   ```

7. **Render the duplicate error** (conditional, below the input row):
   ```tsx
   {showDuplicate && (
     <p className="text-xs text-red-500">ya existe</p>
   )}
   ```

8. **Render the options list** (below the input/error):
   - If `options.length === 0`: render `<p className="text-sm text-zinc-400 dark:text-zinc-500">Agregá al menos dos opciones para empezar.</p>`
   - If `options.length > 0`: render a `<ul>` where each `<li>` shows the option text and a `✕` button:
     ```tsx
     <ul className="flex flex-col gap-1 w-full">
       {options.map((opt, i) => (
         <li key={i} className="flex items-center justify-between rounded-lg bg-zinc-100 px-3 py-2 text-sm dark:bg-zinc-800">
           <span className="text-zinc-800 dark:text-zinc-100">{opt}</span>
           <button
             onClick={() => removeOption(i)}
             className="text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200"
             aria-label={`Eliminar ${opt}`}
           >
             ✕
           </button>
         </li>
       ))}
     </ul>
     ```

9. **Update `app/page.tsx`**:
   - Add `import OptionsList from '@/components/OptionsList'`.
   - Replace the self-closing placeholder `<div className="mt-4 h-48 w-96 rounded-2xl border border-zinc-200 dark:border-zinc-800" />` with:
     ```tsx
     <div className="mt-4 w-96 rounded-2xl border border-zinc-200 p-4 dark:border-zinc-800">
       <OptionsList />
     </div>
     ```
   - `page.tsx` itself stays a server component (no `"use client"` needed there).

10. **Cleanup**: ensure the `setTimeout` reference in `addOption` is properly handled. Because `addOption` is not called inside a `useEffect`, use a `useRef` to store the timer and call `clearTimeout` at the start of each `addOption` invocation to prevent overlapping timers.

## Acceptance criteria

- [ ] Typing "pizza" and pressing Enter adds "pizza" to the list.
- [ ] Clicking "Agregar" with text in the input adds the option to the list.
- [ ] Pressing Enter or clicking "Agregar" with empty/whitespace input does nothing.
- [ ] Adding "Pizza" when "pizza" already exists shows "ya existe" inline and does NOT add the duplicate.
- [ ] The "ya existe" message disappears after ~2 seconds.
- [ ] Clicking ✕ on a list item removes only that item.
- [ ] "Agregá al menos dos opciones para empezar." appears when the list is empty.
- [ ] The helper text disappears as soon as at least one option is added.
- [ ] The card height grows naturally with the list (no fixed height clipping content).

## Out of scope

- Persistence across page reloads.
- Decision/spin logic.
- Drag-to-reorder or editing existing options.
