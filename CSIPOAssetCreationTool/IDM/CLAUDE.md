# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Folder Purpose

This folder is designated for Infor Document Management (IDM) integrations, scripts, and configurations. IDM is Infor's document storage and management system integrated across Infor OS.

**Current Status**: Newly initialized. Awaiting first project or implementation.

## Phased Execution Rule (CRITICAL - NEVER SKIP)

**When work is divided into phases, complete ONE phase at a time and STOP for user validation before proceeding.** Infor OS is NOT a typical local development stack - there is no local runtime, domain knowledge gaps cause frequent errors, and only the user can validate results in the live environment. Do NOT batch multiple phases together. After each phase: summarize what was done, what needs testing, and WAIT for user confirmation before continuing. See root `CLAUDE.md` for full details.

## Git Commits (CRITICAL - NEVER SKIP)

**ALWAYS make an atomic git commit at the end of every session.** Stage only files changed during the session, write a clear `<type>: <summary>` commit message, and commit before ending. See root `CLAUDE.md` for full details.

## IDM Overview

### What is IDM?

Infor Document Management (IDM) is the centralized document repository for Infor CloudSuite applications:
- Stores documents attached to business entities (invoices, purchase orders, items, etc.)
- Provides REST API for upload, download, search, and metadata management
- Integrates with ERP systems via entity attachments
- Supports versioning and document lifecycle management

### Integration Context

IDM is frequently used across other areas of this repository:

**RPA Projects**:
- Multiple RPA workflows upload documents to IDM
- Invoice processing workflows attach PDFs to suppliers/invoices
- Document processing workflows retrieve and process IDM documents
- See `RPA/CLAUDE.md` for IDM integration patterns in workflows

**GenAI Agents**:
- Agents may retrieve documents from IDM for AI processing
- Tools can upload extracted data or results back to IDM
- Document search and retrieval as part of agent workflows

## IDM API Patterns

### Common Operations

**Document Upload**:
```
POST /IDM/api/documents
Headers: Authorization, Content-Type: multipart/form-data
Body: Document file + metadata
```

**Document Download**:
```
GET /IDM/api/documents/{documentId}
Headers: Authorization
```

**Document Search**:
```
GET /IDM/api/documents/search?{parameters}
Headers: Authorization
Query Params: entity type, entity key, date range
```

**Entity Attachment**:
```
POST /IDM/api/documents/{documentId}/attach
Headers: Authorization
Body: Entity type (e.g., "Invoice"), Entity key (e.g., "INV-12345")
```

### Authentication

IDM uses same OAuth 2.0 authentication as other Infor APIs:
- Bearer token in Authorization header
- Token generation: See `Agents&Tools/CLAUDE.md`
- 2-hour token expiry

### Base URL Pattern
```
https://mingle-ionapi.inforcloudsuite.com/<YOUR_TENANT>/IDM
```

## Expected Use Cases

Based on patterns in other folders, this folder may contain:

### Scripts and Utilities
- Document upload automation scripts
- Bulk document processing utilities
- IDM search and retrieval helpers
- Document metadata management tools

### Integration Implementations
- Python/Node.js libraries for IDM operations
- Reusable functions called by RPA or Agents
- Document transformation pipelines
- Error handling and retry logic

### Configuration Files
- IDM endpoint configurations
- Entity type mappings
- Metadata schemas
- Document type definitions

## Development Guidelines

### When Creating IDM Scripts

1. **Reusability**: Create modular functions that can be called from multiple projects
2. **Error Handling**: IDM operations can fail (network, permissions, storage limits)
3. **Metadata**: Always include relevant metadata (entity type, business context)
4. **File Size**: Be aware of document size limits (check tenant configuration)
5. **Cleanup**: Consider document lifecycle and archival strategies

### Common IDM Patterns from RPA

Examples from `RPA/CLAUDE.md`:

**Pattern 1: Upload and Attach**
```
1. Upload document to IDM → Get documentId
2. Attach documentId to entity (Supplier, Invoice, etc.)
3. Store documentId in Data Lake for audit trail
```

**Pattern 2: Search and Process**
```
1. Search IDM by entity key or date range
2. Download document(s)
3. Process content (OCR, extraction, validation)
4. Update business records in ERP
```

**Pattern 3: Document Retrieval for AI**
```
1. Agent receives entity reference
2. Search IDM for associated documents
3. Download document for AI processing
4. Return extracted data to agent
```

## Cross-Project Integration

### RPA + IDM
RPA workflows extensively use IDM:
- See `RPA/CSIInvoiceProcessingGenAIV2/SendToWidgetIDM.xaml`
- See `RPA/CustomerOrderCreation_V2/SendAttachmentsToIDM.xaml`
- Common workflow: Email → Extract attachment → Upload to IDM → Attach to entity

### Agents&Tools + IDM
GenAI agents may:
- Create tools that search/retrieve IDM documents
- Upload AI-generated documents (summaries, reports)
- Attach supporting documents to ERP records

### ION + IDM
ION workflows may:
- Trigger document processing based on IDM events
- Route documents between systems
- Manage document approval workflows

## Maintaining Documentation

### log.md
When working with IDM, update log.md with:
- API endpoint discoveries and response formats
- Authentication issues and resolutions
- Document size/format limitations encountered
- Integration patterns that work well
- Performance observations (upload/download times)

### CLAUDE.md
Update this file when:
- New IDM API patterns are established
- Reusable utilities are created
- Integration approaches are validated
- Common errors and solutions are identified
- Configuration patterns emerge

## Getting Started

When beginning IDM development in this folder:

1. **Determine Scope**: What IDM operations need automation?
2. **Check Existing Patterns**: Review RPA workflows for IDM integration examples
3. **Authentication Setup**: Use token generation from Agents&Tools
4. **Test Endpoint**: Start with document search or simple upload
5. **Build Reusable**: Create utilities that other projects can leverage
6. **Document Progress**: Update log.md as you develop

---

**Note**: This folder is newly initialized. First implementation will establish patterns and structure. Refer to RPA folder for existing IDM integration examples.

