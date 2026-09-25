# The stackup library

[stackup](https://github.com/stackup-eda/stackup) is an electronics design tool for defining PCB
schematics in [KDL](https://kdl.dev). Designs combine parts and reusable circuits, such as supply
decoupling, pull-ups, and sensors with their support components. The engine checks the complete
design, reports errors and warnings together, and exports it to KiCad. The format supports
programmatic edits, including writing pin swaps from the PCB editor back to the source.

This repository contains stackup's core parts, application blocks, and shared types, imported
as `@stackup/…`. All definitions are KDL. It also includes custom KiCad footprints and 3D models.
The library uses the same import mechanism as other stackup libraries and is maintained and
released separately from the Rust engine.

## Using it in a design

Declare the library in your project's `manifest.kdl`, pinned to an exact commit:

```kdl
stackup "0.1"
library stackup git="https://github.com/stackup-eda/library" rev="a1b2c3d4e5f6…"
```

Replace the example revision with a full commit hash. Any file in the project can then import
library definitions:

```kdl
use "@stackup/connector/power-jack"
use "@stackup/timer/ne555"

design oscillator {
    stock {
        packages imperial="0603"
    }
    place power-jack V5 voltage="5V"
    place ne555-astable timer freq="2Hz" vcc=V5.out
}
```

`@stackup/<path>` resolves to `<path>.kdl` at the repository root. An import makes the parts,
blocks, and types declared in that file available to the caller; it does not re-export the
file's own imports. See [examples/](examples/) for complete designs using the library. The
[isolated supply example](examples/isolated-supply.kdl) shows how an output load contributes input
draw without joining the converter's two returns.

Application blocks take the values that determine their components as placement arguments.
For example, `lm5146-buck` takes a rated load and a selected output bank. Its assertions then
compare the connected board's actual load and input voltage with those design inputs. Adding a
load can produce an error, but it does not silently change the parts in the netlist.
Blocks can also take a part definition as an argument. `vom1271-ac-switch` uses DMN3404L by
default; a board that imports another MOSFET can write `fet=nfet-2n7002`. The block requires
that part to expose `gate`, `source`, and `drain` ports. See
[examples/mosfet-selection.kdl](examples/mosfet-selection.kdl) for both selections on one board.

Revisions must be commits, not branches or tags. This makes library versions reproducible
without a separate lockfile. `stackup update @stackup` updates the manifest to the library's
current head commit.

## Editing the library alongside a design

To use a local checkout, add a `manifest.local.kdl` beside the project's manifest:

```kdl
library stackup path="../stackup-parts"
```

This file overrides an existing library declaration for your machine. It cannot introduce a
library absent from the main manifest. Keep it out of version control; `stackup init` adds it
to `.gitignore`.

Each run reports active overrides:

```text
@stackup: ../stackup-parts (manifest.local.kdl)
```

Use `--locked` for CI and release builds to ignore local overrides.

`stackup check` reports when the checkout is dirty or its head differs from the pinned commit.
After pushing your library changes, run `stackup pin @stackup` to update the project's manifest.
It rejects dirty checkouts, unpushed commits, and checkouts whose origin differs from the
manifest's URL. Use `stackup pin --check` in a pre-commit hook to reject a mismatched pin.

## Layout

Generic components and shared types live at the root. Part families are grouped by function.

| Path | Contents |
|---|---|
| `passives` | Generic resistors, capacitors, and inductors; decouple, bypass, bulk, filter, pull-up, and pull-down blocks |
| `passive/` | Fuses and ferrite beads |
| `types` | Shared types such as `usb`, and bus support blocks such as `i2c-pull-ups` |
| `mechanical` | Mounting holes, fiducials, test points, and 2–4-net copper ties |
| `bus/can`, `bus/lin`, `bus/rs485`, `bus/usb` | Transceivers and bridges |
| `clock/` | Oscillators |
| `audio/` | Audio amplifiers |
| `connector/` | Headers, power jacks, Qwiic, SWD, and USB-C |
| `discrete/fet`, `discrete/bjt`, `discrete/diode`, `discrete/led` | Transistors, diodes, TVS protection, and LEDs |
| `driver/led`, `driver/motor` | LED and motor drivers |
| `interface/expander` | GPIO expanders |
| `isolator/` | Digital isolators and optocouplers |
| `logic/` | Gates and buffers |
| `micro/` | Microcontrollers and modules |
| `power/` | Regulators, converter modules, chargers, eFuses, ideal diodes, isolated supplies, and USB-PD controllers |
| `radio/` | Radio modules |
| `rf/nfc` | NFC controllers |
| `sensor/current`, `sensor/hall`, `sensor/accel`, `sensor/temp` | Sensors grouped by measurement |
| `storage/flash`, `storage/eeprom` | Flash and EEPROM memory |
| `switch/` | Push buttons |
| `timer/` | 555 timers |
| `examples/` | Complete designs used to test the library |
| `stackup.pretty/`, `stackup.3dshapes/` | Custom footprints and 3D models |

Use subdirectories for distinct functions, such as CAN and LIN transceivers or buck regulators
and chargers. Microcontrollers remain together in `micro/`.

Keep related parts in one file named for their family. For example, `power/brick/r78e.kdl`
defines `r78e5v0-1a` and `r78e5v0-0a5`; another voltage variant belongs in that file. Keep
application blocks with their parts: `sensor/current/ina226.kdl` defines both `ina226` and the
`ina226-sense` circuit built around it.

File headers should identify the device and explain relevant constraints, defaults, and modeling
limitations. Examples import parts from the library rather than declaring their own.

## Footprints and 3D models

Use KiCad's standard symbol and footprint names where available, such as
`Package_TO_SOT_SMD:SOT-23`. Custom footprints live in `stackup.pretty/` and use the
`stackup:<footprint>` prefix. These include a wide-pad-gap 0402 capacitor, a polarity-marked
inductor, and a Raspberry Pi HAT outline.

The `pcb` command copies required custom footprint libraries into the board project and
registers them in `fp-lib-table`. It also copies the associated models from `stackup.3dshapes/`.
The exported project can resolve these assets without a library checkout; standard assets come
from the local KiCad installation.

See [stackup.pretty/README.md](stackup.pretty/README.md) for sources, dimensions, and modifications.

## Conventions

- **Separate pin definitions from package mappings.** A part lists its logical pins; each
  `package` maps the pins available in that package to pads. The first package is the default.
  Select another with `package=` on a placement.
- **Declare requirements and provide useful defaults.** Use pin requirements, strap roles, and
  default support blocks to describe the device's needs. A board can disable a default with
  `without`. The board declares unused pins with `nc` and supplies stock rules for generic
  passive packages.
- **Calculate behavior from component values.** Block parameters set values with explicit
  defaults. Derived expressions calculate the resulting voltage, current, or timing; assertions
  check whether those values suit the connected circuit. An incompatible supply produces an
  error without silently changing the BOM.
- **Use valid KDL names.** Prefix part names that would start with a digit, such as `nfet-2n7002`.
- **Keep definitions independent of KiCad files.** Symbol and footprint names are export
  metadata and inputs to correspondence checks. Building a design does not read KiCad symbols.

## Checking the library

The examples serve as integration tests. Each should build with no errors or warnings:

```sh
for e in examples/*.kdl; do stackup check "$e"; done
```

With KiCad installed, `stackup check --symbols` compares part definitions with their symbols and
package pad mappings with their `.kicad_mod` files. It reports all mismatches in one run.

## Adding a part

1. Generate a pin table with `stackup import Lib:SYMBOL`, or write one from the datasheet.
   Verify it against the datasheet in either case.
2. Put it in a file named for the family, under the appropriate functional directory. Add a
   directory only when no existing one fits; use the function rather than the vendor name.
3. Add reusable support circuits in the same file. Mark blocks `default` when every placement
   needs them, and make application-specific circuits optional.
4. Write a short header covering the device, important constraints, and any unverified details.
   Extend an example when the part adds behavior not already covered.

The root `manifest.kdl` declares the library name and required stackup version.

## Licence

The KDL library and original assets are [MIT licensed](LICENSE). Four footprints derived from
KiCad and three models from SnapMagic retain their CC BY-SA 4.0 licences. [NOTICE.md](NOTICE.md)
lists the files, sources, attribution requirements, and design-use exceptions.
