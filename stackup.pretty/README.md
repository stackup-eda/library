# Custom KiCad footprints

This directory contains footprints with geometry or pin mappings unavailable in KiCad's standard
libraries. Parts use standard footprints where those are suitable.

Footprints extracted from boards have their placement, UUIDs, net assignments, and component
properties removed. Descriptions and tags describe the reusable footprint. Model references are
removed or replaced as needed. Sources and modifications are recorded below; see
[../NOTICE.md](../NOTICE.md) for the complete licence inventory.

## `C_0402_1005Metric_Wide`

0402 capacitor footprint with 0.47 × 0.55 mm pads centred at ±0.515 mm. The gap between pads is
0.56 mm, compared with 0.40 mm for `Capacitor_SMD:C_0402_1005Metric`. Both footprints have a
1.5 mm outer span.

The wider gap accommodates the RP2350 regulator's `VREG_LX` trace between the terminals of
C<sub>IN</sub> and C<sub>OUT</sub> (RP2350 datasheet §6.3.8.1, Figure 23). The retained per-pad
`(clearance 0.125)` permits a trace about 0.3 mm wide through the gap.

Use this footprint where a trace must pass between the pads. Otherwise use the standard pattern,
as the reference design does for C<sub>FILT</sub>.

Source: Raspberry Pi's `RPI-RP2350A-MINIMAL_R4-S1` reference design, MIT licensed; see the
`LICENSE.txt` included in that download.

## `L_Abracon_AOTA-B201610`

Footprint for the AOTA-B201610S3R3-101-T, the 3.3 µH, 2.0 × 1.6 × 1.0 mm inductor specified
for the RP2350 regulator (§6.3.8.2). Pads are 0.7 × 1.7 mm, centred at ±0.7 mm.

**Connect pad 1 to the output and pad 2 to the switch node.** The silkscreen dot at −1.4 mm
marks pad 1. Orientation matters: the inductor's leakage field couples into the
`VREG_LX`/L/C<sub>OUT</sub> loop. Reversing it degrades transient response and high-load
regulation (§6.3.8.3).

Source: the same Raspberry Pi reference design and MIT licence as the capacitor footprint above.

## `RPI_Hat_B+`

Raspberry Pi HAT footprint containing the board outline, mounting holes, and 40-pin header.
These positions are fixed together by the HAT mechanical specification, so placing the footprint
also supplies the board's `Edge.Cuts`.

The bundled geometry is 65.0 × 56.5 mm, with 3 mm corner radii and relief at the connector end.
Four 3 mm mounting holes sit at (±29, 0) and (±29, 49). The header uses a 2×20 grid at 2.54 mm
pitch, with a rectangular pad 1 and oval remaining pads. Pad numbers match symbol pin numbers.

The footprint must accompany the exported board: an unresolved library reference would omit the
outline and mounting holes as well as the header.

Source: Dave Vandenbout's `RPI_Hat.pretty` library in osdev-hat, MIT licensed
(© 2015–2021 Dave Vandenbout). Removed 103 UUIDs and updated `generator`; geometry is unchanged.

## `Texas_RGY0020G_VQFN-20-1EP_3.5x4.5mm_P0.5mm_EP1.7x2.7mm`

LM5146 footprint for TI's RGY0020G package. It is derived from KiCad's
`Package_DFN_QFN:Texas_RGY_R-PVQFN-N20_EP2.05x3.05mm`, which represents the RGY0020A package
used by the TXB0108. The packages share terminal geometry but have different exposed pads:
2.05 × 3.05 mm for A, 1.7 × 2.7 mm for G.

The unchanged terminal geometry was checked against the RGY0020G outline: eight pads per side
at 0.5 mm pitch, centred on ±1.65 mm, and two per end at (±0.75, ±2.15) mm. Each pad is
0.6 × 0.25 mm.

Using the larger A pad reduces the gap to adjacent terminals from 0.5 mm to 0.325 mm. Those
terminals include SW, BST, and VIN on a controller rated to 100 V, so the correct exposed-pad
size matters.

The exposed-pad corner radius remains 0.05 mm, using `roundrect_rratio` 0.0294 instead of
0.0244. The original STEP reference is removed. As in the source footprint, the exposed pad
has no `F.Paste`; the datasheet specifies four stencil apertures with 80% total coverage, to be
provided in the stencil design.

## `Arduino_UNO_R3_Shield`

Arduino Uno R3 shield header pattern: four 2.54 mm stacking headers with 8 power, 6 analog,
8 digital, and 10 digital positions. The 32 plated holes use 1.6 mm pads and 1.0 mm drills.
Pin 1 is rectangular at the power header's NC position. Rows are 48.26 mm apart; the digital
headers include the 0.16 in (4.06 mm) offset. Pad numbers match `MCU_Module:Arduino_UNO_R3`.

KiCad's `Module:Arduino_UNO_R3` uses the opposite orientation, suitable for a carrier that mounts
an Uno as a module. Its digital row is at +48.26 mm in KiCad's downward-positive Y coordinates.
This shield footprint uses the host's top view: digital row at −48.26 mm, D0 at the right, and
SCL at the left. It was drawn independently from the header positions.

All 32 positions were checked against the DCC-EX EX-CSB1 layout and agree to 0.01 mm. The
footprint omits the board outline and mounting holes because Uno-compatible hosts can differ
mechanically. For example, the EX-CSB1 is 65.9 × 52.9 mm and uses different mounting-hole
positions. Define those features for the intended host board.

## `RJ11_Stewart_SS-90000-006_Horizontal`

Stewart SS-90000-006 four-contact, six-position jack. Derived from KiCad's Amphenol `54601-x06`
footprint by removing the outer contacts and renumbering the remaining four as 1–4, corresponding
to plug positions 2–5.

Stewart drawing CT900006 uses the same contact positions: 1.27 mm stagger, 2.54 mm rows, and
8.89 mm from the 10.16 mm peg pair. Contact drills are changed from 0.76 to 0.90 mm and peg
holes from 3.25 to 3.18 mm.

The Stewart STEP model uses Y-up coordinates with the peg pair at its origin. Contact tips
extend 3.7 mm below the board, in rows 6.35 and 8.89 mm ahead of the pegs, at the footprint's
±0.635/±1.905 mm stagger. The model is rotated −90° about X and offset +3.18 mm in X and
−8.89 mm in Y to align it with the footprint.

**The inherited Fab and courtyard outlines do not include the full panel stop.** They retain
the Amphenol widths of 13.62 and 14.42 mm and extend 7.9 mm ahead of the pegs. Stewart specifies
a 13.08 mm body, a 15.80 mm panel stop, and a face 10.34 mm ahead of the pegs. Adjacent jacks
on a pitch below 15.8 mm collide at the stops even if the courtyards do not overlap.

## 3D models

Standard footprints reference KiCad's models. When a model is missing, a part may specify a
substitute. Additional models live in `stackup.3dshapes/`; `pcb` copies them into the exported
project with the custom footprints.

Two models are simple shapes for checking occupied space: a 2.0 × 2.0 × 0.9 mm block for the
WS2812B-2020 and a Ø10 × 16.5 mm cylinder for the capacitor. Both were exported as STEP from
board outlines of the required dimensions. Other models include a generated JST connector and
three SnapMagic downloads; their sources and licences are listed in [../NOTICE.md](../NOTICE.md).
Downloaded models have adjacent `.LICENSE.txt` files.

Bundled footprints use `(model …)` references like standard KiCad footprints. `CP_Elec_10x16.5`
uses the cylinder, `Converter_DCDC_RECOM_R-78K-0.5_THT` uses KiCad's R-78E model, and the RJ11
footprint uses the Stewart model with the alignment described above.

Only include models whose licences permit redistribution. Models licensed solely for use in
individual designs must remain with the project that obtained them.

## Maintenance

Correspondence checks compare part pad mappings with these footprints just as they do with
standard KiCad footprints. If an upstream footprint changes, update the bundled copy and record
the source revision and modifications here.
