# Library licences

The KDL definitions and original assets are MIT licensed; see [LICENSE](LICENSE). Assets from
MIT-licensed sources retain that licence. Four footprints derived from KiCad and three models
from SnapMagic are distributed under CC BY-SA 4.0, as listed below.

KiCad and SnapMagic provide design-use exceptions: using these assets in a board does not impose
attribution or ShareAlike requirements on the design or its generated files. The redistribution
requirements below apply to copies of the library assets themselves.

## Footprints (`stackup.pretty/`)

| File | Source | Licence |
|---|---|---|
| `Arduino_UNO_R3_Pins` | Created here, positions measured from a produced Uno-format host | MIT |
| `Arduino_UNO_R3_Shield` | Created here, as above | MIT |
| `Arduino_UNO_R3_Socket` | Created here, as above | MIT |
| `C_0402_1005Metric_Wide` | Raspberry Pi `RPI-RP2350A-MINIMAL_R4-S1` reference design, MIT (© Raspberry Pi Ltd) | MIT |
| `L_Abracon_AOTA-B201610` | Raspberry Pi `RPI-RP2350A-MINIMAL_R4-S1` reference design, MIT (© Raspberry Pi Ltd) | MIT |
| `RPI_Hat_B+` | `RPI_Hat.pretty` from Dave Vandenbout's osdev-hat, MIT (© 2015–2021 Dave Vandenbout) | MIT |
| `FlexTail_1x06_P0.5mm` | Created here from the Hirose FH12 drawing | MIT |
| `JST_PA_B08B-PASK_1x08_P2.00mm_Vertical` | Created here from JST's ePA-F drawing | MIT |
| `JST_PA_S08B-PASK-2_1x08_P2.00mm_Horizontal` | Created here from JST's ePA-F drawing | MIT |
| `Converter_DCDC_RECOM_R-78K-0.5_THT` | KiCad footprint generator output, derived from the KiCad library's R-78E footprint | **CC BY-SA 4.0** |
| `CP_Elec_10x16.5` | KiCad `CP_Elec_10x*` pad geometry with a taller body | **CC BY-SA 4.0** |
| `RJ11_Stewart_SS-90000-006_Horizontal` | the KiCad library's Amphenol `54601-x06` footprint, two contacts removed, drills changed | **CC BY-SA 4.0** |
| `Texas_RGY0020G_VQFN-20-1EP_3.5x4.5mm_P0.5mm_EP1.7x2.7mm` | the KiCad library's `Texas_RGY_R-PVQFN-N20_EP2.05x3.05mm`, thermal pad resized | **CC BY-SA 4.0** |

The KiCad libraries are © the KiCad developers and contributors, distributed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) with
[KiCad's design exception](https://www.kicad.org/libraries/license/). Under that exception,
designs and files generated from them are not Adapted Material. The four derived footprints
retain the same licence. The table records their modifications;
[stackup.pretty/README.md](stackup.pretty/README.md) provides further details.

## 3D models (`stackup.3dshapes/`)

| File | Source | Licence |
|---|---|---|
| `CP_Elec_10x16.5.step` | a Ø10 × 16.5 mm cylinder, exported here | MIT |
| `LED_WS2812B-2020_PLCC4_2.0x2.0mm.step` | a 2.0 × 2.0 × 0.9 mm block, exported here | MIT |
| `JST_PA_S08B-PASK-2_1x08_P2.00mm_Horizontal.step` | output of the `.py` beside it, drawn here to JST's ePA-F drawing | MIT |
| `JST_PA_S08B-PASK-2_1x08_P2.00mm_Horizontal.py` | written here | MIT |
| `JST_PA_B08B-PASK_1x08_P2.00mm_Vertical.step` | SnapMagic download 56544, unmodified | **CC BY-SA 4.0** |
| `RJ11_Stewart_SS-90000-006_Horizontal.step` | SnapMagic download 510211, unmodified | **CC BY-SA 4.0** |
| `Texas_B3QFN-14-1EP_5x5.5mm.step` | SnapMagic, TPSM53603RDAR, unmodified | **CC BY-SA 4.0** |

SnapMagic (formerly SnapEDA) distributes its design files under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) with a design-use exception
similar to KiCad's. Each downloaded model has an adjacent `.LICENSE.txt` recording its source
and attribution.

SnapMagic's terms §5.1(g) limit public redistribution to ten files in one location without
written permission. This repository includes three; account for that limit when adding more.
Do not include manufacturer models licensed only for use in designs without redistribution
rights. Keep those files with the project that downloaded them.

## Distributing the library in an executable

When embedding this library, include the MIT notice for MIT-licensed files and the attribution
and a reference to this notice for the unmodified CC BY-SA assets. The latter are included as a
collection; their ShareAlike terms apply to the assets.

To distribute a version without CC BY-SA content, redraw the four derived footprints from their
datasheets and replace the three SnapMagic models with original models.
