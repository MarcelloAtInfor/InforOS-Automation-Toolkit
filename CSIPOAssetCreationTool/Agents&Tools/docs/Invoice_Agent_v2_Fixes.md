# Invoice Automation Agent v2 - Fixes Applied

## Date: 2026-01-28

## Issues Identified from Manual UI Test

### 1. VendorSearch_Tool_v2 - Invalid Property Names ❌
**Error**: "Property VadPhone not found on SLVendors IDO"

**Root Cause**: Used incorrect field names from assumption rather than querying the IDO schema.

**Fix Applied**:
- Removed: `VadPhone`, `VadEmail`
- Added: `Phone`, `ExternalEmailAddr`

**Status**: ✅ FIXED

---

### 2. ItemSearch_Tool_v2 - Bad URL Construction ❌
**Error**: 404 Not Found

**Actual URL Generated**:
```
/ido/<YOUR_TENANT>/<YOUR_SITE>/load/SLItems
```

**Correct URL Should Be**:
```
/ido/load/SLItems
```

**Root Cause**: LLM was inserting tenant/config names into URL path (reason unclear - tools had correct servicePath)

**Fix Applied**:
- Simplified api_docs format to match old working tools exactly
- Removed verbose explanations and extra sections
- Used minimal format: Method, Endpoint, Headers, Parameters, Examples

**Status**: ✅ FIXED (needs testing to confirm)

---

### 3. ItemInsert_Tool_v2 - Bad URL Construction ❌
**Error**: 404 Not Found

**Actual URL Generated**:
```
/ido/<YOUR_SITE>/api/v2/update/SLItems
```

**Correct URL Should Be**:
```
/ido/update/SLItems
```

**Root Cause**: Same as ItemSearch - LLM misinterpreting api_docs

**Fix Applied**:
- Completely rewrote api_docs in minimal format
- Matches old working ItemInsert_Tool format
- Removed all verbose text ("CRITICAL", "IMPORTANT", field definitions)

**Status**: ✅ FIXED (needs testing to confirm)

---

### 4. PoSearch_Tool_v2 - Filter Syntax Error ❌
**Error**: "Error processing LoadCollection request: IllegalFilterException"

**Wrong Filter**:
```
filter=PoNum = "INV2026002"
```

**Correct Filter**:
```
filter=PoNum = 'INV2026002'
```

**Root Cause**: Used double quotes instead of single quotes in filter syntax

**Fix Applied**:
- Updated all filter examples to use single quotes
- Simplified api_docs format

**Status**: ✅ FIXED

---

### 5. PoInsert_Tool_v2 - Overly Verbose Format ⚠️
**Issue**: Same verbose format as Item tools that caused URL issues

**Fix Applied**:
- Simplified api_docs to minimal format
- Matches working tool patterns

**Status**: ✅ FIXED (preventative)

---

## Summary of All Fixes

| Tool | Issue | Fix |
|------|-------|-----|
| VendorSearch_Tool_v2 | Wrong field names | Use Phone, ExternalEmailAddr |
| ItemSearch_Tool_v2 | Bad URL construction | Simplified api_docs format |
| ItemInsert_Tool_v2 | Bad URL construction | Simplified api_docs format |
| PoSearch_Tool_v2 | Filter syntax error | Use single quotes |
| PoInsert_Tool_v2 | Preventative | Simplified api_docs format |

## Key Learnings

### 1. Always Query IDO Schema First
Use the `/info/{ido}` endpoint to discover correct property names:
```
GET /ido/info/SLVendors
```

**SyteLine API Documentation**: `APIs/SyteLineRESTv2.json` contains the Swagger spec with all endpoint details.

### 2. Filter Syntax Rules
- ✅ Use **single quotes**: `Item = 'WIDGET-A'`
- ❌ NOT double quotes: `Item = "WIDGET-A"` (causes IllegalFilterException)
- LIKE operator: `Name LIKE '%text%'`

### 3. Tool api_docs Format
**Keep it simple!** Verbose explanations confuse the LLM:

❌ **Too Verbose** (caused URL issues):
```
Method: POST
ENDPOINT: /update/SLItems

Headers:
X-Infor-MongooseConfig: <YOUR_SITE>
Content-Type: application/json

Request Body Format (JSON):

CRITICAL: This endpoint uses the IDOName/Changes structure...

Field Definitions:
Item: STRING, item code (unique identifier, use ItemSearch_Tool_v2 first!)
Description: STRING, item description (CRITICAL for demo visibility!)
...
IMPORTANT:
- Item must be unique - always use ItemSearch_Tool_v2 first
- Description is CRITICAL for identifying items in demos
...
```

✅ **Simple Format** (works correctly):
```
Method: POST
Endpoint: /update/SLItems

Headers:

X-Infor-MongooseConfig: <YOUR_SITE>

Body:
{
  "IDOName": "SLItems",
  "RefreshAfterSave": true,
  "Changes": [...]
}

NOTE: Action 1 means insert. All properties above are required.
```

### 4. Common Field Names (Case-Sensitive)

**Vendors (SLVendors)**:
- Phone (NOT VadPhone)
- ExternalEmailAddr (NOT VadEmail)

**Items (SLItems)**:
- Item, Description, UM
- MatlType, PMTCode, ProductCode
- AbcCode, CostType, CostMethod, Stat

**POs (SLPOs)**:
- PoNum (exactly 10 characters)
- VendNum (links to vendor)
- TermsCode, Stat, Type, Whse, PoCurrCode

## Testing Required

### Test Case: Same Invoice Data
Use the same test input that revealed these issues:

```json
{
  "vendor": {
    "name": "TESTCO_DEMO_2026",
    "address": "456 Test Avenue",
    "city": "Demo City",
    "state": "OH",
    "zip": "43215",
    "phone": "614-555-0200",
    "email": "invoice@testco.com"
  },
  "purchaseOrder": {
    "poNumber": "INV2026002",
    "orderDate": "20260128",
    "warehouse": "MAIN",
    "terms": "N30"
  },
  "lineItems": [
    {
      "lineNumber": "1",
      "itemCode": "DEMO-ITEM-X",
      "description": "Demo Item X for Testing 2026",
      "quantity": "15",
      "unitOfMeasure": "EA"
    },
    {
      "lineNumber": "2",
      "itemCode": "DEMO-ITEM-Y",
      "description": "Demo Item Y for Testing 2026",
      "quantity": "8",
      "unitOfMeasure": "EA"
    }
  ]
}
```

### Expected Results After Fixes

1. ✅ VendorSearch should work (no more VadPhone error)
2. ✅ VendorInsert should work (already worked before)
3. ✅ ItemSearch should return correct URL: `/ido/load/SLItems`
4. ✅ ItemInsert should return correct URL: `/ido/update/SLItems`
5. ✅ PoSearch should work with proper filter syntax
6. ✅ PoInsert should work if PO search succeeds

### What to Check
- All API URLs should be: `{base}/CSI/IDORequestService/ido/{action}/{IDOName}`
- No extra path segments like tenant name or config name
- No `/api/v2/` in the path
- All filters use single quotes

## Files Modified

- `VendorSearch_Tool_v2` - Updated properties and filter syntax
- `ItemSearch_Tool_v2` - Simplified api_docs format
- `ItemInsert_Tool_v2` - Simplified api_docs format
- `PoSearch_Tool_v2` - Fixed filter syntax and simplified format
- `PoInsert_Tool_v2` - Simplified api_docs format

## Scripts Created

- `fix_all_tools_v2.py` - Script that applied all fixes
- `debug_tool_comparison.py` - Analysis script for investigating the issues

## Documentation Updated

- `CLAUDE.md` - Added section on discovering IDO properties via /info endpoint
- `CLAUDE.md` - Added common field names reference
- `CLAUDE.md` - Added filter syntax rules
- This document - Complete fix summary

## Next Steps

1. **Test the agent** with the same invoice data in the UI
2. **Verify URLs** are constructed correctly for all tools
3. **Confirm** no more 404 errors or filter exceptions
4. If successful: **Document success** in log.md
5. If issues remain: **Capture new error logs** and investigate further

---

**Status**: All fixes applied and ready for testing
**Last Updated**: 2026-01-28
