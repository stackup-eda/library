# Rust-to-KDL porting gaps

The device definitions from the Rust `stackup-parts` crate have KDL counterparts. The cases
below need language or engine support before the KDL library can enforce the same behavior.
The circuits are usable now, but a successful `stackup check` does not check these details.

| Needed support | Affected definitions | What is missing |
|---|---|---|
| Conditional power transfer through series devices | `power/efuse/tps26631`, `power/ideal_diode/ltc4359` | Describe conduction, current direction, and reverse blocking without shorting the input and output nets. The TRI 20 isolated converter already transfers its output load into input draw through an expression while keeping its input and output returns separate; `examples/isolated-supply.kdl` checks that behavior. |
| Explicit ties between returns | `power/buck/lmr36510` and other converters with separate analog and power grounds | `mechanical.kdl` supplies 2-, 3-, and 4-pad net ties that join copper at a defined PCB location. KDL cannot yet require a particular tie or check that the board placed it between the correct returns. |
| Computed component sizing | `power/buck/lm5146` | The KDL block now takes an explicit design envelope, selects a two- or three-capacitor output bank with `when`, and checks output capacitance, current limit, inductor saturation, input voltage, and actual load. It still needs the Rust helper's full input-bank and compensation calculations. The TLC59116 rounds its current-setting resistor to E96, and the computed value reaches the KiCad netlist. |
| PCB geometry and placement constraints | `micro/rp2350`, `power/buck/lmr36510` | Express required copper pours, cutouts, local placement, and routing constraints alongside the schematic. The RP2350 regulator circuit is connected, but its layout must be checked manually. |
| Structured part-selection constraints | `rf/nfc/pn532`, `sensor/current/ina226`, `micro/rp2350` | Check capacitor dielectric and voltage rating, resistor/inductor tolerance, and capacitor ESR/ESL against selected stock. These requirements are currently in comments or notes. |
| Multi-unit KiCad symbol mapping | `logic/` parts with multi-unit symbols | Associate a logical pin with its KiCad symbol unit so exported schematics place each gate or section in the intended unit. |
| Parametric or generated parts | `connector/header`, `discrete/led/ws2812b` | Generate a numbered connector and a repeated LED chain from a count. The library spells out stocked connector sizes through 40 pins; longer generic connectors and repeated pixel chains need manual definitions or wiring. |
| Differential input voltage facts | `isolator/fodm214` | Derive optocoupler input current from the voltage between its LED terminals. The KDL block currently takes the input swing as a parameter. |

The `stackup check` used for this port does not accept `--symbols`, so these definitions still
need a KiCad symbol and footprint correspondence check when that command is available.
