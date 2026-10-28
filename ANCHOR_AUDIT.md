# Passive placement anchor audit

The audit covers every KDL library definition outside examples and caches:
325 placements of resistors, capacitors, inductors, shunt helpers, ferrite beads,
and crystals. Generic root passives and `as=self` helper roots are excluded
from the count; all six shunt helpers are separately checked for nullable anchor
parameters and forwarding. Library-owned support components now have 316
explicit physical anchors, with nine reviewed exceptions. This adds 291 anchors
to the 25 already present.

## Findings and fixes

Only `decouple` previously exposed and forwarded an anchor. `bypass`, `bulk`,
`filter`, `pull-up`, and `pull-down` now support the same optional reference.
Their wiring, values, packages, and reference parameters are retained.

Missing anchors occurred across MCU supplies/reset/reference circuits,
transceivers, isolators, logic, sensors, memory, radio, audio, LEDs, converter
banks, feedback/enable networks, charge pumps, timing, and NFC support circuits.
Anchors use the existing pin/package definitions; no device electrical claims or
pin maps were changed. Multi-pad pins have explicit pad selections. Distinct
input/output nets retain their wiring. Buck output banks target the output side
of the inductor; NFC matching stages target the corresponding passive pads.
Anchors provide a starting position, not a verified analog/RF/power layout.

The ARC TRK-LED-02 symptom was its LIN filter capacitor: the library now exports
`node/sbc/supply/Clin` as `Stackup Anchor = XLIN.4`. Its input/output capacitors
and reset pull-up also have physical anchors. Board-local buck/MCU components
and ARC's shared pixel block were updated alongside the library so all 20
passives on that design can be placed by the action.

Passive-to-passive anchors exposed an ordering issue in the KiCad plugin. Both
fresh-footprint sync and selected-footprint placement now process hosts before
their dependents. Cyclic chains and their dependents are reported and left in
place. Existing footprint placement remains unchanged during sync.

## Reviewed exceptions

| Definition | Placements | Reason |
| --- | --- | --- |
| `types.kdl` | `sda`, `scl` | Generic I2C contract cannot choose a controller/device physical pin. The board chooses placement. |
| `sensor/current/ina226`, `ina237`, `ina240` | `Rshunt` in each | High-current copper and Kelvin routing determine shunt location; placing it automatically at the IC would be misleading. |
| `power/buck/lm5146` | `Cin1`, `Cin2`, `Cin-hf1`, `Cin-hf2` | Selectable power FET determines the input hot loop and physical drain pad; the controller's VIN is behind a separate RC filter. The board chooses placement at the power stage. |

These are explicit exceptions in the audit script. Missing anchors elsewhere
fail the audit. A board can supply `anchor=` to generic pull helpers directly;
these compound circuits still need a board-specific layout decision.

## Validation

- `python3 scripts/audit_anchors.py`: 325 placements, 316 anchors, nine reviewed
  exceptions, zero errors. Checks host physical pins and uniqueness/existence in
  all applicable package maps, including package-gated support blocks. `--json`
  emits a full per-placement inventory. This is a source audit of the KDL subset
  used by the library; Stackup elaboration remains authoritative.
- All seven `examples/*.kdl` pass `stackup check --lib ../stackup-parts`.
- All 16 ARC `board.kdl` files pass `stackup check` using the local library.
- TRK-LED-02 netlist exports with all 20 passive anchors. In-memory KiCad sync
  preserves every saved footprint position, rotation, and lock state; each
  anchor resolves to an actual pad on the saved host footprint. Selecting and
  snapping all 20 passives succeeds with no placement problems. No saved PCB
  was written, as the PCB is open in KiCad.
- `cargo test --workspace` passes all 77 Rust tests.
- Five plugin regression tests cover reversed host/dependent order during snap
  and fresh sync, unselected hosts, independent order, and cyclic chains.

Symbol/footprint correspondence and PCB DRC are outside this metadata change.
Manual placement/routing of TRK-LED-02 remains unfinished. Existing library and
ARC worktree changes were preserved; this audit does not change the pinned
library revision.
