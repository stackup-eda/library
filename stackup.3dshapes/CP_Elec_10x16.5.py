# CP_Elec_10x16.5: a Ø10 × 16.5 mm SMD aluminium or polymer can on its resin base plate.
# Base plate, leads, bead and top radius follow KiCad's own CP_Elec_10x10.5 body, with the can
# carried up to 16.5 mm, so the part reads like the rest of the CP_Elec family.
# Install build123d (`pip install build123d`) and run this script to regenerate the adjacent STEP.
# Frame is KiCad's model frame with the origin at the land's centre on the board face:
# pad 1 (+) on −X, +Z off the board.
from build123d import *

H = 16.5                    # seated height, base plate included
R = 5.0                     # can radius
PLATE, PLATE_H, CHAMFER = 10.3, 1.15, 1.0
BEAD_Z, BEAD_H, BEAD_R = 2.4, 1.0, 4.75
TOP_RADIUS = 0.67

# Resin base plate, its two + side corners chamfered as on the part.
with BuildPart() as plate:
    with BuildSketch():
        s = PLATE / 2
        c = s - CHAMFER
        Polygon((-c, -s), (s, -s), (s, s), (-c, s), (-s, c), (-s, -c), align=None)
    extrude(amount=PLATE_H)

# Can, with the sealing bead rolled into it and a rounded top edge.
with BuildPart() as can:
    with Locations((0, 0, PLATE_H)):
        Cylinder(R, H - PLATE_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    fillet(can.edges().group_by(Axis.Z)[-1], TOP_RADIUS)
    with Locations((0, 0, BEAD_Z)):
        Cylinder(R, BEAD_H, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
        Cylinder(BEAD_R, BEAD_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Pressure-vent cross scored in the lid.
    with Locations((0, 0, H)):
        Box(6.0, 0.3, 0.3, mode=Mode.SUBTRACT)
        Box(0.3, 6.0, 0.3, mode=Mode.SUBTRACT)

# Flat leads, folded under the plate and out past its edges to ±6.0 mm.
with BuildPart() as leads:
    for x0, x1 in ((-6.0, -4.333), (4.333, 6.0)):
        with Locations(((x0 + x1) / 2, 0, 0.075)):
            Box(x1 - x0, 0.9, 0.15)

p = plate.part; p.color = Color(0.148, 0.145, 0.145)   # black resin
c = can.part;   c.color = Color(0.824, 0.820, 0.781)   # aluminium
l = leads.part; l.color = Color(0.824, 0.820, 0.781)   # tinned leads
asm = Compound(children=[p, c, l], label="CP_Elec_10x16.5")
export_step(asm, __file__.replace(".py", ".step"))
bb = asm.bounding_box(); print("bbox", bb.min, bb.max)
