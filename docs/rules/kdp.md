# Kindle/KDP rules

- Target: Amazon KDP reflowable Kindle ebook unless explicitly changed.
- `Active/Production/` contains the Kindle-facing source.
- Conversion must never silently become rewriting.
- Preserve semantic chapter headings and intentional scene breaks.
- Avoid print-only dependencies: headers, footers, page numbers, fixed page references, tab-based indents and spacing hacks.
- Cover work is a separate controlled step; do not embed a cover into the manuscript source unless the active KDP workflow requires it.
- Kindle Create / Kindle Previewer results are publication-render evidence and belong in `Reports/`.
- Do not claim Kindle Create or Previewer validation unless the actual application/output was used.
