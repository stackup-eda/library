# JST S08B-PASK-2: eight-position side-entry PA header with locating bosses.
# Modeled from JST ePA-F pages 3 and 9 because no redistributable JST model was available.
# Install build123d (`pip install build123d`) and run this script to regenerate the adjacent STEP.
# Frame is KiCad's model frame with the origin at the centre of the pin row on the board face:
# X along the row (pins at ±1, ±3, ±5, ±7), +Y toward the mating face, +Z off the board.
from build123d import *

W, WALL = 18.0, 0.9
# Side profile in (Y, Z): rear foot and latch ramp, the shrouded body, the floor lip at the face.
profile = [(-3.5, 0), (-3.5, 1.8), (-2.8, 1.8), (0.5, 4.2), (0.5, 5.4), (2.2, 5.4),
           (2.2, 6.5), (6.5, 6.5), (6.5, 2.8), (8.2, 2.8), (8.2, 0)]
with BuildPart() as housing:
    with BuildSketch(Plane.YZ):
        Polygon(*profile, align=None)
    extrude(amount=W / 2, both=True)
    # Mating cavity above the front lip, with a 1.5 mm roof.
    with Locations((0, (1.0 + 6.6) / 2, (2.8 + 5.0) / 2)):
        Box(W - 2 * WALL, 6.6 - 1.0, 5.0 - 2.8, mode=Mode.SUBTRACT)
    # Roof opening for the plug latch.
    with Locations((0, 4.4, 6.0)):
        Box(4.0, 2.4, 1.2, mode=Mode.SUBTRACT)

PIN = 0.5
with BuildPart() as pins:
    for x in (-7, -5, -3, -1, 1, 3, 5, 7):
        # Vertical pin extends 3.4 mm below the board and to the bend above it.
        # The bend fits below the housing ramp, which is 3.8 mm high at the pin row.
        with Locations((x, 0, (3.4 - 3.4) / 2)):
            Box(PIN, PIN, 3.4 + 3.4)
        # Horizontal contact extends into the mating cavity.
        with Locations((x, 5.5 / 2, 3.4)):
            Box(PIN, 5.5, PIN)

with BuildPart() as bosses:
    with Locations((-8.5, 2.1, -0.4), (8.5, 2.1, -0.4)):
        Cylinder(0.5, 0.8)

h = housing.part; h.color = Color(0.93, 0.90, 0.82)   # natural PBT
p = pins.part;    p.color = Color(0.80, 0.80, 0.78)   # tin
b = bosses.part;  b.color = h.color
asm = Compound(children=[h, p, b], label="JST_PA_S08B-PASK-2_1x08_P2.00mm_Horizontal")
export_step(asm, __file__.replace(".py", ".step"))
bb = asm.bounding_box(); print("bbox", bb.min, bb.max)
