# Table reach resting-arm correction

Inspected first/second clip starting samples and later cup poses from table_reach_20261016_071133_9b46f9e6.zip. Author findings match visible bent resting arms. Corrected resting target construction and forward elbow pole; preserved cup arm exactly during established contact intervals. Both arms down at initial first pose; free arm down in second clip. Key proxy follows lowered hand; final key contact/pocket remains open.

Validation: verify_elias_table_reach.py checks353 poses, fixed arm/leg/finger lengths, forward resting elbows, low resting wrists, unchanged passed cup-arm targets, mug/table support and bounded wrist steps. Film workspace, Python compilation and whitespace checks pass. No local Blender runtime available. Rerun same --table-reach-review command;119 images/two clips. No full bake requested.
