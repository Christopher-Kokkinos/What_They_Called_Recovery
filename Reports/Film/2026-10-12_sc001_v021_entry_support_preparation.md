# SC001 v0.21 entry and built support preparation

Author authorised entry opening/threshold and landing. Last desktop evidence remains v0.20.

## Geometry and judgement calls

Old marker was a solid slab at X=7.5 and outside arrival lacked a floor. Retained diagonal route crosses Y=0.05 near X=6.591. Opening is centred X=6.6, clear width 1.6 m and height 2.3 m, formed by jambs/lintel. A leaf is parked open along the landing side, outside passage. Threshold top is flush Z=0; landing X=5.4–9.2/Y=-2–0 meets flat floor at Y=0. Arrival stays (7.5,-0.7). Diagnostic dimensions and parked door are layout choices; no final canonical architectural or door-use performance claim.

New sc001_entry.py separates pure bounds/support plan from Blender geometry and validation. Late camera framing now includes jamb/lintel bounds instead of the removed slab. Nine helpers hashed.

## Validation implementation

Blender evaluates body children, mug, keys and jacket through every source frame of the final segment. Cube edges are clipped against the opening's depth slab and checked against clear X/Z bounds. Conservative world AABB overlap with parked leaf rejects possible collision. These are proxy geometry checks, not skinned body collision simulation.

Each sole corner casts down against actual flat-floor, threshold and landing meshes. A support hit is required; stance gap must be below 0.00001 m and feet cannot penetrate support. Swing feet may have height above support. Ray distance is transformed for object scale. Validation reports crossing interval, minimum opening clearance, checked frames and maximum stance support gap. This adds built-surface evidence beyond the former Z=0 reference-plane checks.

## Results and desktop gate

Pure route-alignment and sole-plan floor/landing coverage PASS, along with anatomy, reach, packet volume, seated clearance, stance and camera-plan checks. Film workspace, AST syntax and diff checks PASS. Blender evaluated passage/support and visuals remain pending; no local runtime.

Run full --render-shot-review --render-motion-preview; inspect full diagonal passage, leaf/jamb clearance, prop clearance, threshold/landing foot support and arrival composition. Include whole ZIP and validation. No timing, route, custody, pigeon cut or publication prose changes. Door handle/opening/closing action, final gait, cloth, fingers and audio remain open. No final gate advance.
