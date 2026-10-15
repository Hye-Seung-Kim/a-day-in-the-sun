# Interaction verification — 2026-10-15

Checked in the Codex in-app browser against the running local site.

- Viewports: 1440 × 900, 786 × 848, 390 × 844. No horizontal overflow.
- Desktop and tablet chapter links select the corresponding pinned scene. The active label follows scrolling.
- Face/other skin switch: 31.1% / 27.6%; 31 / 28 highlighted marks.
- Grid/group toggle preserves all 100 marks and changes their positions.
- Illustration Spray label selects the matching chart row and 37.6% explanation.
- Association switch: 19.3% / 35.1% vs. 80.7% / 64.9%; fixed 0–100% axis. Settled bar transforms match 0.807 / 0.649.
- Prediction 70% gives a 38.9 percentage-point difference; keyboard End + Enter at 100% gives 68.9 points. The revealed array contains 31 colored marks.
- Pause motion sets transition durations to 0 and scrolling to auto. Enable motion restores it. Keyboard interaction disables motion during the action.
- Browser error log: none during tested flows.

System reduced motion is handled with CSS and matchMedia; no device preference was changed during testing. Mobile was checked with an emulated viewport, not a physical phone.
