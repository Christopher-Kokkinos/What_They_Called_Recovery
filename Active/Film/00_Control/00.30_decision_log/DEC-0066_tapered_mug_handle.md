# DEC-0066 — Tapered mug handle trial

2026-10-15. Author reports big improvement, asks to remove/drastically shorten lower edge and make handle more triangular so ring/little can sit closer beneath. Trial handle first; tighten contact only if convincing.

Keep DEC-0065 hand/arm poses exactly unchanged for comparison. Shorten outer rail from78 to51 mm, lifting its lower end to z=-12 mm. Replace horizontal lower bar with diagonal return from x=-105,z=-12 mm to x=-57,z=-33 mm; retain top rail. This produces a tapered lower loop rather than a closed rectangular bottom. Diagonal Y rotation is atan2(21,48); nominal rail thickness12 mm/depth18 mm retained. Geometry is provisional and confined to copied mug diagnostic.

Shared HANDLE contract now includes local Y rotation. Pure signed-distance clearance transforms samples into each oriented rail frame; Blender sets dimensions before applying identical rotation. No axis-aligned-box approximation for the diagonal. Existing500-micron nominal skin-radius clearance threshold retained.

Six-pose comparison against DEC-0065 confirms hand plan, arm joints, wrist origins, mug basis/root/route exactly unchanged. Pure246-frame checks PASS; wrist maximum51.1343 degrees. Syntax, film workspace and diff checks PASS. Original checkpoint untouched. Fourteen-image desktop review remains pending. Ring/little spacing, thumb/crease contact and skin/wrist seams are still open; handle-only trial does not claim to fix them automatically.
