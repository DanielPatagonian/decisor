## Add and list options

Users need to be able to type options into the Decisor and see them in a list.

### Requirements

- Inside the placeholder card on `app/page.tsx`, render:
  - A text input with placeholder "Agregar una opción..."
  - An "Agregar" button to the right of the input.
- Pressing **Enter** in the input OR clicking **Agregar** adds the trimmed value to a list of options stored in React state.
- Empty / whitespace-only inputs must NOT be added.
- Duplicate values must NOT be added (case-insensitive comparison). Show a brief inline message "ya existe" for ~2 seconds when a duplicate is attempted.
- Below the input, render the list of options. Each item shows the text plus a small `✕` button on the right to remove that single option.
- When the list is empty, show a muted helper text: "Agregá al menos dos opciones para empezar."

### Acceptance

- I can type "pizza" + Enter and see it appear in the list.
- I can add "Pizza" again and get the "ya existe" feedback (no duplicate).
- I can click ✕ on an item and it disappears.
- The "Agregá al menos dos opciones..." text appears only when the list is empty.

### Out of scope

- Persistence across page reloads (separate issue).
- The actual decision/spin logic (separate issue).

### Implementation hint

A new component `components/OptionsList.tsx` is fine, but inlining in `page.tsx` is also fine if it stays under ~120 lines. Use `useState<string[]>([])`.
