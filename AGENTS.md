# Working in the stackup parts library

This repository holds reusable KDL definitions and their supporting assets. Use this file for collaboration and workflow. Keep device data, modeling decisions, and examples in the library files and project documentation.

## Read first

- `README.md` explains the library layout, conventions, and validation commands.
- Read the relevant KDL file and nearby definitions before changing a part or block. Consult its source material when changing a device claim.
- `PORTING_GAPS.md` records known migration gaps; check it before adding a workaround or declaring a gap resolved.

## Working together

- Check `git status` and the files you plan to edit. Other agents may be changing this checkout at the same time.
- Divide parallel work by file or family. Coordinate before editing a file another agent owns; preserve unrelated changes and avoid broad formatting or resets.
- Record a device-specific reason or limitation beside its definition. Put reusable guidance and usage examples in `README.md` or `examples/`, rather than accumulating technical notes here.
- Run `stackup check` on an affected example or design. For broader library changes, check all `examples/*.kdl`; use the symbol and footprint checks described in `README.md` when those mappings change. Report the checks run and any remaining gap.

Changes here can affect sibling `stackup` and `arc-kdl` checkouts. Coordinate interface changes and verify affected consumers.
