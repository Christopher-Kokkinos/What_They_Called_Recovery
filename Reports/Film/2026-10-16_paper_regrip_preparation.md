# Paper regrip preparation

Root cause: initial target frame rotated rigidly through180 degrees with folding half. Evaluated contact passed but visible palm/forearm action rolled excessively. Separate contact face from palm orientation; allow declared release/regrip while other hand supports the fixed half.

New tests:120 poses,50 bones/fixed lengths, normalized weights, explicit active contacts, paused fold during regrip, continuous right support, wrist-axis bend <45 degrees left and <65 degrees right, stable folding-phase palm orientation, bounded wrist steps, exact fold trajectory. Maximum wrist step0.01584219 m. Pure paper PASS; existing353-pose table verifier PASS. Python compile, workspace, whitespace PASS. No Blender installed locally: evaluated plane/bone checks and visual review pending desktop run. Two41-image clips, same builder/checkpoint. No whole-scene or envelope acceptance.
