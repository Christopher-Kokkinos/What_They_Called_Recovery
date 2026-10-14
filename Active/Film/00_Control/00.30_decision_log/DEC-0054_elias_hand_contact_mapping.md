# DEC-0054 — Elias palm mapping and articulated hands

Author authorises reusable hand/contact refinement after SC001 rig run. Date 2026-10-14.

Root cause: previous hand bone used wrist centre and ground-forward orientation, but accepted proxy palm targets have action-specific offsets/bases for drawer, shower and paper. Map the new hand bone origin to those palm centres and orient along their local negative Z; forearm wrist targets and all accepted choreography remain unchanged. Add five three-segment digits per hand, driven by a reusable pure hand module. Relaxed, drawer, shower, mug, paper and keys presets use fixed phalange lengths and bounded curls. These are provisional shape/pose choices, not approved character anatomy or physical grasp certification.

Rig now has 48 bones (18 existing plus 30 digit bones). Mesh components remain closed/disconnected; palm-to-wrist and shoulder/hip topology refinement remains open. Do not claim skin/prop collision clearance from palm centre checks. Fingers may require retargeting after the first close-up readback. Add twelve dedicated hand stills and all-frame evaluated palm-centre assertions, alongside existing movement validation.
