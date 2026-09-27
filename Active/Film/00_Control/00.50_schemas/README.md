# Schema policy

This folder is reserved for versioned, testable machine-readable schemas when a production exchange format becomes real. The existing CSV headers and `production_manifest.json` remain the current interfaces. Do not create speculative JSON schemas or duplicate the registers before a concrete producer and consumer exist.

When a schema is added, document version, owning artifact, required fields, ID references, migration rules and a validator invocation here. Schema changes require a decision-log entry if they break existing data.
