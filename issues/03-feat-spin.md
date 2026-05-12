## Decidir button with spin animation

The core feature: pick one of the options at random with a short visual effect.

### Requirements

- Below the options list (when there are **2 or more** options), show a big **"Decidir"** button.
- When clicked:
  1. Disable the button.
  2. Show a "spinning" effect — cycle through the option labels rapidly (one every ~80ms) in a large display area for about 1.5 seconds. The values cycled through can be picked randomly from the current options list each tick.
  3. Settle on the final chosen option (picked uniformly at random from the list using `Math.random()`).
  4. Show the result prominently, e.g. "**🎯 Pizza**".
  5. Re-enable the button so the user can spin again.
- When there are fewer than 2 options, the button should not appear at all (the helper text from issue #2 already handles that case).
- After a result is shown, adding/removing options should clear the previous result.

### Acceptance

- With ≥2 options, the Decidir button appears.
- Clicking it shows a brief shuffle, then a stable result.
- The button is disabled during the animation so I can't double-click.
- Editing the option list after a result clears the displayed result.

### Out of scope

- History of past decisions.
- Weighting options.

### Implementation hint

`setInterval` cleared by `setTimeout`, or a small `useEffect` with a tick counter. Keep the animation simple — no third-party animation library needed.
