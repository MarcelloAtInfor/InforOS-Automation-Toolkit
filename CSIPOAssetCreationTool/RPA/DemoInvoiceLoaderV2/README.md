# DemoInvoiceLoaderV2

Deterministic RPA-based rewrite of the invoice loader, published as `DemoInvoiceLoader_V4`.

What it does:
- watches an input folder for invoice PDFs
- uses Infor OCR/IDP to extract invoice data
- performs deterministic vendor, item, PO, and PO-line logic directly against CSI IDOs
- writes tax to the visible PO tax field
- sends ION notifications with created asset details

What is intentionally different from the older `DemoInvoiceLoader`:
- the transactional path does not rely on GenAI chat/tool orchestration
- vendor reuse is deterministic and fail-closed on ambiguity
- item and PO verification are explicit after writes

Public-safe setup model:
- tracked source uses placeholders/generic defaults
- tenant-specific values should be materialized through `scripts/prepare_deploy.py`
- live OCR still needs Studio rebind in the generated `.deploy` copy for the target tenant

Main files:
- `project.json`
- `MainPage.xaml`
- `ProcessDocumentBatch.xaml`
- `SingleDocumentController.xaml`
- `scripts/prepare_deploy.py`
- `deploy.local.example.json`

See `DemoInvoiceLoader_V4_Report.html` for the delivery summary and validation report.
