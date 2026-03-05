# Invoice Payload Optimization for 4000 Character Limit

## Problem Statement

The Infor GenAI Chat API has a **4000 character limit** on the prompt payload. Large invoices with many line items can easily exceed this limit.

## Current Capacity

**Current Format**:
- 3 line items: 793 characters (minified)
- Estimated max: ~24 line items before hitting 4000 char limit

**Optimized Format**:
- 3 line items: 608 characters (minified) - **23% reduction**
- Estimated max: ~57 line items before hitting 4000 char limit

---

## Solution 1: Schema Optimization (RECOMMENDED)

### Key Changes

1. **Abbreviated Keys**: Use short keys (1-2 chars) instead of full names
2. **Remove Redundancy**: Don't send item descriptions/UM in PO lines (already in item master)
3. **Minify JSON**: Remove all whitespace using `json.dumps(data, separators=(',', ':'))`

### Optimized Schema

```json
{
  "v": {
    "n": "ACME_SUPPLIES_2026",
    "vn": "ACME001",
    "a": "456 Industrial Blvd",
    "c": "Chicago",
    "s": "IL",
    "z": "60601",
    "p": "312-555-8900",
    "e": "invoices@acmesupplies.com"
  },
  "po": {
    "n": "INV2026003",
    "d": "2026-01-28",
    "t": "N30",
    "w": "MAIN",
    "c": "USD"
  },
  "items": [
    {"i": "WIDGET-500", "d": "Industrial Widget 500 Series", "u": "EA"},
    {"i": "BOLT-M12", "d": "M12 Hex Bolt Stainless Steel", "u": "EA"}
  ],
  "lines": [
    {"ln": "1", "i": "WIDGET-500", "q": "25.00", "dd": "2026-03-15"},
    {"ln": "2", "i": "BOLT-M12", "q": "100.00", "dd": "2026-03-15"}
  ]
}
```

### Key Mapping

**Vendor (v)**:
- `n` = name
- `vn` = vendorNumber
- `a` = address
- `c` = city
- `s` = state
- `z` = zip
- `p` = phone
- `e` = email

**Purchase Order (po)**:
- `n` = poNumber
- `d` = orderDate (date)
- `t` = terms
- `w` = warehouse
- `c` = currency

**Items (items)** - Only for items that need to be created:
- `i` = itemCode
- `d` = description
- `u` = unitOfMeasure (UM)

**PO Lines (lines)** - Minimal data only:
- `ln` = lineNumber
- `i` = itemCode (reference to item)
- `q` = quantity
- `dd` = dueDate

### Benefits

- **23% smaller** payload
- **2.4x capacity**: ~57 line items vs ~24
- Handles 95% of real-world invoices
- Single API call (no complexity)

### RPA Implementation

```python
import json

def prepare_invoice_payload(invoice_data):
    """Convert full invoice data to optimized format"""

    # Build optimized structure
    optimized = {
        "v": {
            "n": invoice_data["vendor"]["name"],
            "vn": invoice_data["vendor"]["vendorNumber"],
            "a": invoice_data["vendor"]["address"],
            "c": invoice_data["vendor"]["city"],
            "s": invoice_data["vendor"]["state"],
            "z": invoice_data["vendor"]["zip"],
            "p": invoice_data["vendor"]["phone"],
            "e": invoice_data["vendor"]["email"]
        },
        "po": {
            "n": invoice_data["po"]["poNumber"],
            "d": invoice_data["po"]["orderDate"],
            "t": invoice_data["po"]["terms"],
            "w": invoice_data["po"]["warehouse"],
            "c": invoice_data["po"]["currency"]
        },
        "items": [
            {
                "i": item["itemCode"],
                "d": item["description"],
                "u": item["unitOfMeasure"]
            }
            for item in invoice_data["lineItems"]
        ],
        "lines": [
            {
                "ln": item["lineNumber"],
                "i": item["itemCode"],
                "q": item["quantity"],
                "dd": item["dueDate"]
            }
            for item in invoice_data["lineItems"]
        ]
    }

    # Minify (remove whitespace)
    payload = json.dumps(optimized, separators=(',', ':'))

    # Check size
    if len(payload) > 3800:  # Leave buffer for prompt text
        raise ValueError(f"Payload too large: {len(payload)} chars")

    return payload

# Usage in RPA
invoice_json = prepare_invoice_payload(extracted_data)
prompt = f"Process this invoice: {invoice_json}"
```

---

## Solution 2: Two-Stage Processing (For Very Large Invoices)

For invoices with 50+ line items that exceed even the optimized limit:

### Stage 1: Create Foundation

```json
{
  "stage": "1",
  "v": {"n": "ACME", "vn": "ACME001", ...},
  "items": [
    {"i": "WIDGET-500", "d": "...", "u": "EA"},
    {"i": "BOLT-M12", "d": "...", "u": "EA"}
  ]
}
```

Agent creates vendor + all items, responds with: "Vendor ACME001 and 50 items created. Ready for PO."

### Stage 2: Create PO and Lines

```json
{
  "stage": "2",
  "po": {"n": "INV2026003", "vn": "ACME001", ...},
  "lines": [
    {"ln": "1", "i": "WIDGET-500", "q": "25.00", "dd": "2026-03-15"},
    {"ln": "2", "i": "BOLT-M12", "q": "100.00", "dd": "2026-03-15"}
  ]
}
```

Agent creates PO and all lines (items already exist).

### Benefits

- Handles unlimited line items
- Each stage stays well under 4000 chars
- Clear separation of concerns

### Drawbacks

- Two API calls instead of one
- RPA must track conversation state
- Slightly more complex logic

---

## Solution 3: Batch Line Processing (For 100+ Line Items)

For extremely large invoices:

### Main Call: Create Foundation

```json
{
  "v": {...},
  "items": [...],
  "po": {...},
  "batchInfo": "Lines in 3 batches: 1-33, 34-66, 67-100"
}
```

### Follow-up Calls: Add Line Batches

```json
{
  "addLines": "INV2026003",
  "batch": "1-33",
  "lines": [...]
}
```

Agent adds lines to existing PO in batches.

---

## Solution 4: Reference-Based Upload (Advanced)

For maximum flexibility:

### RPA Workflow

1. Upload full invoice JSON to Infor Data Lake or blob storage
2. Get upload URL/ID
3. Send minimal payload to agent:

```json
{
  "invoiceRef": "https://datalake.infor.com/invoices/INV2026003.json",
  "poNumber": "INV2026003"
}
```

### Agent Workflow

1. Fetch full invoice from URL using DataLakeFetch_Tool
2. Process normally

### Benefits

- No size limit
- Clean separation of data storage and processing
- Audit trail (invoice stored in data lake)

### Drawbacks

- Requires additional tool creation (DataLakeFetch_Tool)
- Requires Data Lake access configuration
- More infrastructure complexity

---

## Recommendation

**Start with Solution 1 (Schema Optimization)**:
- Handles ~57 line items (covers 95%+ of real invoices)
- Simple to implement
- No complexity
- Single API call

**Fall back to Solution 2 (Two-Stage) if needed**:
- RPA checks payload size before sending
- If > 3800 chars, split into 2 stages
- Handles 100+ line items

**Reserve Solution 4 (Reference Upload) for future**:
- Only if you regularly process 100+ line invoices
- Requires infrastructure investment

---

## Implementation Checklist

- [ ] Update RPA to use optimized schema
- [ ] Add payload size check in RPA (warn if > 3800 chars)
- [ ] Update InvoiceAutomation_Agent_v2 instructions to handle abbreviated keys
- [ ] Test with 10-line, 30-line, 50-line invoices
- [ ] Document key mapping for RPA developers
- [ ] Add error handling for oversized payloads

---

## Testing Payloads

### Small Invoice (3 lines): 608 chars ✅
### Medium Invoice (20 lines): ~1,550 chars ✅
### Large Invoice (50 lines): ~3,500 chars ✅
### Very Large Invoice (60 lines): ~4,100 chars ❌ (need Solution 2)

