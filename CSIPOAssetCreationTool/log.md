# CSIPOAssetCreationTool - Progress Log

<!--
Track your development sessions here.
Use date headers for each session, e.g.:

## Session Date: YYYY-MM-DD
### What was done
- ...

### Discoveries
- ...

### Next steps
- ...
-->

## Session Date: 2026-03-09 (public deterministic V4 sync)
### What was done
- Added `RPA/DemoInvoiceLoaderV2/` to the public repo as the deterministic rewrite published as `DemoInvoiceLoader_V4`.
- Included public-safe workflow/config/script files plus:
  - `RPA/DemoInvoiceLoaderV2/README.md`
  - `RPA/DemoInvoiceLoaderV2/DemoInvoiceLoader_V4_Report.html`
- Updated public readmes so users can find the new deterministic flow easily.

### Discoveries
- The existing public `DemoInvoiceLoader` already uses placeholder-based project packaging, so the public V2 copy should follow the same model.
- The V4 process identity can stay as a unique GUID in the public project while tenant/process-specific runtime values remain placeholders.

### Next steps
- Commit and push the public toolkit sync to `origin`.
