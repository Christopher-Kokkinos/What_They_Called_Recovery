# Front supporting grip correction

## Root cause and scope

Prior regrip pinch at packet(-80,-30)mm selected a rear wrist and a hand-aligned posterior elbow. Jacket concealment amplified the visual ambiguity but was not its cause. Restaging the support at the forward edge(+110,-50)mm allows a cross-body hand direction and outward/downward elbow without altering the held packet path.

Changed only diagnostic left arm/hand17–156 in the joined provider. All397 prop positions/bases and right hand are exactly equal to prior committed provider; all complete poses1–16 and157–397 are exactly equal. Accepted standalone pocket157–226 and mug pickup remain intact.

## Deterministic evidence

verify_elias_pocket_handover.py passes397 poses/50 fixed bones, regrip pad gaps, rigid held packet transform, accepted pocket/mug equivalence and continuity. Maximum wrist angle60degrees; maximum left elbow frame step reduced from60.030mm to40.310mm. Support torso proxy score minimum1.311425 across140 transition poses, required>=1.

At55, torso-local left elbow(width,height,forward)=(.359682,.276460,.159045)m and wrist=(.025341,.332673,.184656)m. The elbow is now forward/outward and below the shoulder. Legacy recorded frame55 posterior-arm fixture is explicitly rejected by the new gate.

The clearance solver minimises an ellipse quadratic analytically over each arm segment clipped to the torso height interval, rather than sampling a few points. Expanded central core dimensions and exclusions are documented in elias_torso_clearance.py and DEC-0096. It does not certify full skin/garment collision. Blender builder runs the same gate on evaluated left upper-arm/forearm bones for17–156 and writes minimum score/count into validation.json. Regrip support-plane gate now uses the shared forward-edge constants.

Python compilation, verify_film_workspace.py and git diff --check pass. Blender unavailable locally: runtime and visual confirmation pending. Same focused397-pose/134-image command; new pocket_handover_... folder. No new camera/full-scene bake or manuscript/checkpoint changes.
