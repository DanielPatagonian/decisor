# Feature: Decidir button with spin animation

**Issue**: #3
**Type**: feature

## Context
Decisor currently lets users build a list of options but has no way to pick one. This feature adds a "Decidir" button that, when clicked, rapidly cycles through the option labels for ~1.5 seconds then settles on a randomly chosen result, giving the app its core purpose. All logic lives inside the existing `OptionsList` component — no new files needed.

## Files to create
_(none)_

## Files to modify
- `components/OptionsList.tsx` — add `spinning`, `displayLabel`, and `result` state; implement the spin animation with `setInterval`/`setTimeout`; render the Decidir button (visible only when `options.length >= 2`), the cycling display area, and the final result; clear result when options change.

## Implementation steps

1. **Add state variables** inside `OptionsList`:
   - `const [spinning, setSpinning] = useState(false)` — true while the animation runs
   - `const [displayLabel, setDisplayLabel] = useState<string | null>(null)` — the label shown during cycling
   - `const [result, setResult] = useState<string | null>(null)` — the settled winner

2. **Clear result on option-list changes.** In `addOption`, after `setOptions(...)`, add `setResult(null)`. In `removeOption`, after `setOptions(...)`, add `setResult(null)`.

3. **Implement `handleDecide`** function:
   ```ts
   function handleDecide() {
     if (options.length < 2 || spinning) return
     const winner = options[Math.floor(Math.random() * options.length)]
     setResult(null)
     setSpinning(true)
     const interval = setInterval(() => {
       setDisplayLabel(options[Math.floor(Math.random() * options.length)])
     }, 80)
     setTimeout(() => {
       clearInterval(interval)
       setSpinning(false)
       setDisplayLabel(null)
       setResult(winner)
     }, 1500)
   }
   ```
   Pick `winner` before the interval starts so it is fixed regardless of any concurrent state updates.

4. **Render the spin display area** — below the options `<ul>` (or empty-state `<p>`), when `spinning || result`:
   ```tsx
   {(spinning || result) && (
     <div className="mt-2 flex items-center justify-center rounded-xl bg-zinc-100 py-6 text-2xl font-bold dark:bg-zinc-800">
       {spinning ? (
         <span className="text-zinc-700 dark:text-zinc-200">{displayLabel}</span>
       ) : (
         <span className="text-zinc-900 dark:text-zinc-50">🎯 {result}</span>
       )}
     </div>
   )}
   ```

5. **Render the Decidir button** — below the display area, visible only when `options.length >= 2`:
   ```tsx
   {options.length >= 2 && (
     <button
       onClick={handleDecide}
       disabled={spinning}
       className="mt-2 w-full rounded-xl bg-zinc-900 py-3 text-base font-semibold text-white hover:bg-zinc-700 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-300"
     >
       Decidir
     </button>
   )}
   ```
   The `disabled` attribute + `disabled:opacity-50 disabled:cursor-not-allowed` classes visually and functionally prevent double-clicks during the animation.

6. **No imports needed** — `setInterval`/`setTimeout` are browser globals; all state is handled by existing `useState` import.

## Acceptance criteria
- [ ] With ≥ 2 options, the "Decidir" button is visible below the list.
- [ ] With < 2 options, the "Decidir" button is not rendered.
- [ ] Clicking "Decidir" starts the cycling animation (labels change rapidly every ~80 ms).
- [ ] The button is visually disabled and non-clickable during the animation.
- [ ] After ~1.5 seconds the animation stops and the result is displayed as "🎯 <option>".
- [ ] The result is picked uniformly at random using `Math.random()`.
- [ ] Adding or removing an option after a result is shown clears the result.
- [ ] After the animation completes the button is re-enabled and can be clicked again.

## Out of scope
- History of past decisions.
- Weighted options.
- Third-party animation libraries.
