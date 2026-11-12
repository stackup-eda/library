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

## `ESP32-C6-MINI-1U`

Footprint for the ESP32-C6-MINI-1U, the MINI-1 with an external antenna socket instead of the PCB
antenna: a 13.2 × 12.5 mm body on the MINI-1's land pattern, pad for pad (ESP32-C6-MINI-1 &
MINI-1U datasheet v1.5, figures 11-1 and 11-2). The pads sit where they do on the MINI-1, with the
body's bottom edge at y = 5.6 mm, so the body runs to y = −6.9 mm and the socket end is the top.
There is no antenna keepout. No 3D model is referenced.

Source: KiCad's `RF_Module:ESP32-C6-MINI-1` (CC BY-SA 4.0 with the KiCad libraries' exception),
with the antenna keepout zone, its courtyard wings, the antenna-area text and the model removed,
and the silkscreen, fabrication outline and courtyard shortened to the 12.5 mm body.

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

## `Maxim_T1633-4_TQFN-16-1EP_3x3mm_P0.5mm_EP1.23x1.23mm`

MAX98357A footprint for Maxim's T1633+4 package. It is derived from KiCad's
`Package_DFN_QFN:TQFN-16-1EP_3x3mm_P0.5mm_EP1.23x1.23mm`, which is drawn for the T1633-5 on the
same outline (21-0136). The two share the 3 × 3 mm body, the 0.5 mm pitch and the exposed pad
(1.10 mm nominal, 1.25 mm at most), but the T1633-4's terminals are 0.1 mm longer: L is 0.45 mm
nominal and 0.55 mm at most, against 0.35 and 0.45 mm (MAX98357A data sheet Rev 7, p. 37).

KiCad's terminal pads end 1.025 mm from the centre, short of a nominal T1633-4 terminal's inner
end at 1.05 mm and 0.075 mm inside a longest one's at 0.95 mm, leaving no heel. The pads are
lengthened inward, keeping their outer ends at 1.85 mm: the two mid-side pads on each side by
0.1 mm, to 0.925 × 0.25 mm, and the corner pads by 0.04 mm, to 0.865 × 0.25 mm. Corner pads on
adjacent sides meet diagonally, and 0.04 mm keeps them 0.207 mm apart, over a 0.2 mm clearance;
0.1 mm would close that to 0.12 mm. The gap to the exposed pad is at least 0.31 mm. Maxim's land
pattern 90-0031 was not consulted. Pad numbers, the exposed pad, its paste apertures and the STEP
reference are unchanged.

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

## `RotaryEncoder_Bourns_Vertical_PEL12T-4xxxx-S1024`

Bourns PEL12T-4 illuminated rotary encoder (`@stackup/switch/pel12t`), shaft perpendicular to the
board, origin at the shaft. The five LED and switch pins (common anode on 5, push switch 3 to 5),
the three encoder pins and the tab positions follow the PEL12T data sheet's suggested layout
(REV. 09/19). The tab slots are copied from KiCad's `RotaryEncoder_Bourns_Vertical_PEL12D-4`,
the same 12 mm body, so the footprint carries that library's licence. No 3D model.

## `ST_VL53L4CD`

ST VL53L4CD time-of-flight sensor (`@stackup/sensor/tof/vl53l4cd`), optical LGA12, 4.4 × 2.4 ×
1.0 mm. Twelve 0.5 mm square pads on a 0.8 mm grid, from DS13812 Rev 8, Figure 19, which is drawn
from below; the footprint is that view mirrored for the top. Pad 1 is the corner under the Tx
aperture. F.Fab marks the body, its pin-1 corner and both apertures (Rx 0.665 mm and Tx 3.665 mm
from the end away from pad 1, Figure 17), for placing a cover window. The VL53L4CX and VL53L3CX
use the same package. Original, MIT licensed. No 3D model.

## `Thumbstick_Alps_RKJXV`

ALPS RKJXV thumbstick (`@stackup/switch/rkjxv`), origin at the lever. Every hole is from the RKJXV
catalog's Drawing No. 1 (Update 2510), which is viewed from the mounting side, so it is drawn as
it is: VR1's three Ø1.0 holes at x = 8.73 mm, VR2's at y = −8.73 mm, both on 2.5 mm; the switch's
four Ø1.2 holes at x = ±3.25 mm, y = 5.75 and 10.25 mm; the four Ø1.5 legs at (±6.325, ±5) mm as
`MP`; and unplated Ø1.6 holes at (±4.3, 0) for the two 0.75 mm locating bosses. The drawing's
prohibited wiring areas (Ø4 at the lever, Ø3.5 at y = 8 mm joined to it by a 2.2 mm channel, and
Ø2.6 at (±3.5, ±3.5) mm) are keepouts on F.Cu. F.Fab marks the 13.15 mm frame and the 18.2 ×
21.7 mm envelope, placed by scaling the outline drawing, which gives the overall sizes but not
their offsets. Pads are numbered for the generic connector symbol the part borrows: 1–3 VR1, 4–6
VR2 (the drawing's circled 1–3), 7–10 the switch's a, b, c, d. Hall-effect and TMR drop-in sticks
use the same land. Original, MIT licensed. No 3D model.

## `Kingbright_DA08-11`

Kingbright DA08-11 dual-digit 0.8 inch seven-segment display (`@stackup/display/da08`), from the
DA08-11EWA spec's package drawing and recommended PCB layout (DSAP8270, Rev V.1A): two rows of
nine 1.0 mm holes in 1.5 mm pads at 2.54 mm, the rows 22.0 mm apart. Drawn from the top with the
digits upright: pin 1 (square) at the origin, bottom left, pins 1–9 left to right along the bottom
and 10–18 right to left along the top, at y = −22.0 mm. F.Fab and the silkscreen mark the
35.8 × 25.85 mm body, centred on the pin field; the drawing dimensions the body's half width
(18 mm) and the row spacing but not the pins' offset from the body's edges, so the centring is
read from the drawing, not dimensioned. A tick below pad 1 marks it outside the body. The DC08-11
(common cathode) uses the same land. Original, MIT licensed. No 3D model.

## Footprints from the Snips controller

These came from the Snips controller boards (github.com/thePunderWoman/SnipsControllers), whose
layouts use them, with their placement removed and their model references pointed at
`stackup.3dshapes/` or KiCad's library. Pad numbers are unchanged, so a Snips board and a design
using the library part share the same pads. Licences are in [../NOTICE.md](../NOTICE.md).

- `GuliKit_HallStick` — the GuliKit hall stick (`@stackup/switch/rkjxv`, package `gulikit`) on the
  RKJXV holes, adapted from Daniel Benoy's thumbstick-breakout. Pads 1–3 and 1′–3′ are the two
  axes, a–d the switch legs; the four mounting legs are unnumbered. Larger pads than
  `Thumbstick_Alps_RKJXV`, and no locating-boss holes or keepouts. The model is the ALPS
  RKJXV1224005 body as a stand-in, raised 11.4 mm onto its standoffs.
- `QMA6100P` — QST QMA6100P LGA-12 (`@stackup/sensor/accel/qma6100p`), pad geometry from LCSC's
  EasyEDA land for C2887190. Pin 1 top left, numbered anticlockwise.
- `IC_BQ25185DLHR` — TI BQ25185 WSON-10 (`@stackup/power/charger/bq25185`), SnapMagic's land: ten
  signal pads, exposed pad 11 and two thermal vias numbered 12 and 13. Its model is Y-up and the
  land rotates it −90° about X.
- `SK6812MINI-HS-012` — top-mount SK6812MINI-HS (`@stackup/discrete/led/sk6812mini-hs`), from the
  datasheet's section 6 top-view land: 1.5 × 1.0 mm pads. Pad 1 (GND) is the chamfered corner,
  lower right. KiCad's 3535 WS2812B-Mini body stands in, rotated to put its pin-1 corner on pad 1.
- `SW_Alps_SKRP` — Alps SKRP 4.2 × 3.2 mm tact switch (`@stackup/switch/push-button`, package
  `skrp`), from the SKRP land dimensions. Terminals 1–2 and 3–4 are joined inside, so pad 1 is the
  top pair and pad 2 the bottom pair. KiCad's same-size C&K PTS810 body stands in.
- `ESP32-S3-MINI-1U` — Espressif's footprint for the module (`@stackup/micro/esp32s3`), which
  matches the datasheet's Figure 11-2, with Espressif's model.
- `XB3-24Z8UM` — XBee 3 Micro, 34-pad castellated (`@stackup/radio/xbee3`, `xbee3-micro`), from
  Digi 90001543 p. 98 with pad numbers from p. 42. Rule areas keep copper from under the module
  and its RF test points (p. 58). Digi's model is not redistributable, so none is referenced.
- `XB324Z8UTJ` — XBee 3 through-hole (`@stackup/radio/xbee3`, `xbee3-zigbee`), from the Amidala
  shield, on two KiCad 2.00 mm 1×10 socket bodies. Its original source is not recorded.

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
uses a can drawn with build123d, `Converter_DCDC_RECOM_R-78K-0.5_THT` uses KiCad's R-78E model, and the RJ11
footprint uses the Stewart model with the alignment described above.

Only include models whose licences permit redistribution. Models licensed solely for use in
individual designs must remain with the project that obtained them.

## Maintenance

Correspondence checks compare part pad mappings with these footprints just as they do with
standard KiCad footprints. If an upstream footprint changes, update the bundled copy and record
the source revision and modifications here.
