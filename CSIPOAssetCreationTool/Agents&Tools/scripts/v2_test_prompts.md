# InvoiceAutomation_Agent_v2 Test Prompts

Copy/paste each prompt exactly as shown (entire block including the CRITICAL instruction).

**Logical ID for testing**: `lid://infor.syteline.invoice-automation-v2`

---

## Test 1: Baseline (2 line items)
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Zephyr Industrial 7391','address':'100 Mountain View Dr, Denver, CO 80201','phone':'(303) 555-0100','email':'orders@zephyr7391.com'},'purchaseOrder':{'poNumber':'PO-2026-7391','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'ZEP7391-A1','description':'Zephyr Component Alpha','quantity':'50','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'ZEP7391-B2','description':'Zephyr Component Beta','quantity':'25','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 2: Short Vendor Name (VendNum Padding Test)
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'QX 8452','address':'200 Short St, Phoenix, AZ 85001','phone':'(602) 555-0200','email':'ap@qx8452.com'},'purchaseOrder':{'poNumber':'PO-2026-8452','orderDate':'20260201','warehouse':'MAIN','terms':'N15'},'lineItems':[{'lineNumber':'1','itemCode':'QX8452-WDG01','description':'QX Premium Widget Model 8452','quantity':'100','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 3: Multiple Line Items (5 lines)
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Nexus Parts Corp 3647','address':'500 Harbor Blvd, Long Beach, CA 90802','phone':'(562) 555-0500','email':'sales@nexus3647.com'},'purchaseOrder':{'poNumber':'PO-2026-3647','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'NXS3647-BLT-A','description':'Nexus Steel Bolt Grade A','quantity':'500','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'NXS3647-BLT-B','description':'Nexus Steel Bolt Grade B','quantity':'500','unitOfMeasure':'EA'},{'lineNumber':'3','itemCode':'NXS3647-NUT-A','description':'Nexus Hex Nut Grade A','quantity':'1000','unitOfMeasure':'EA'},{'lineNumber':'4','itemCode':'NXS3647-WSHR','description':'Nexus Flat Washer Standard','quantity':'2000','unitOfMeasure':'EA'},{'lineNumber':'5','itemCode':'NXS3647-SCRW','description':'Nexus Machine Screw Small','quantity':'750','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 4: Long Vendor Name
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Meridian Global Manufacturing Solutions 5128','address':'1200 Corporate Center Dr, Chicago, IL 60601','phone':'(312) 555-1200','email':'procurement@mgms5128.com'},'purchaseOrder':{'poNumber':'PO-2026-5128','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'MGM5128-MTR01','description':'Meridian Electric Motor 5HP','quantity':'10','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'MGM5128-PMP02','description':'Meridian Hydraulic Pump Assy','quantity':'5','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 5: Large Quantities
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Titan Fastener Intl 9273','address':'900 Supply Chain Ave, Detroit, MI 48201','phone':'(313) 555-0900','email':'bulk@titan9273.com'},'purchaseOrder':{'poNumber':'PO-2026-9273','orderDate':'20260201','warehouse':'MAIN','terms':'N60'},'lineItems':[{'lineNumber':'1','itemCode':'TFI9273-RVT-S','description':'Titan Pop Rivet Small Alum','quantity':'50000','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'TFI9273-RVT-M','description':'Titan Pop Rivet Medium Steel','quantity':'25000','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 6: Single Line Item (Minimal)
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Rapid Source 4816','address':'50 Express Lane, Atlanta, GA 30301','phone':'(404) 555-0050','email':'quick@rapidsrc4816.com'},'purchaseOrder':{'poNumber':'PO-2026-4816','orderDate':'20260201','warehouse':'MAIN','terms':'N15'},'lineItems':[{'lineNumber':'1','itemCode':'RS4816-TAPE3','description':'Rapid Industrial Tape 3 inch','quantity':'24','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 7: Electronics with Special Descriptions
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Volt Circuit Systems 6039','address':'700 Circuit Dr, San Jose, CA 95101','phone':'(408) 555-0700','email':'sales@voltcs6039.com'},'purchaseOrder':{'poNumber':'PO-2026-6039','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'VCS6039-R1K','description':'Volt Resistor 1K Ohm 1/4W','quantity':'1000','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'VCS6039-C10U','description':'Volt Capacitor 10uF 50V','quantity':'500','unitOfMeasure':'EA'},{'lineNumber':'3','itemCode':'VCS6039-LED5','description':'Volt LED Red 5mm 20mA','quantity':'2000','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 8: Different Terms (N45)
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Forge Metal Works 2784','address':'1500 Foundry Rd, Pittsburgh, PA 15201','phone':'(412) 555-1500','email':'orders@forgemw2784.com'},'purchaseOrder':{'poNumber':'PO-2026-2784','orderDate':'20260201','warehouse':'MAIN','terms':'N45'},'lineItems':[{'lineNumber':'1','itemCode':'FMW2784-STPL','description':'Forge Steel Plate 4x8 1/4in','quantity':'20','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'FMW2784-ALBR','description':'Forge Aluminum Bar 2x2 inch','quantity':'50','unitOfMeasure':'EA'},{'lineNumber':'3','itemCode':'FMW2784-BRRD','description':'Forge Brass Rod 1 inch Dia','quantity':'100','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 9: Automation Parts (4 lines)
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Automate Pro Supply 1593','address':'3505 Hutchinson Rd, Cumming, GA 30040','phone':'(770) 555-8800','email':'orders@autops1593.com'},'purchaseOrder':{'poNumber':'PO-2026-1593','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'APS1593-PLC24','description':'AutoPro PLC M221 24IO','quantity':'5','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'APS1593-HMI7','description':'AutoPro HMI Touch 7in Color','quantity':'5','unitOfMeasure':'EA'},{'lineNumber':'3','itemCode':'APS1593-VFD5','description':'AutoPro VFD 5HP 480V','quantity':'3','unitOfMeasure':'EA'},{'lineNumber':'4','itemCode':'APS1593-SRV1','description':'AutoPro Servo Motor 1KW','quantity':'4','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 10: Office Supplies
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Workspace Solutions 8165','address':'6600 N Military Trail, Boca Raton, FL 33496','phone':'(561) 555-2200','email':'commercial@wkspc8165.com'},'purchaseOrder':{'poNumber':'PO-2026-8165','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'WS8165-PAPER','description':'Workspace Copy Paper Letter','quantity':'50','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'WS8165-TNR26','description':'Workspace Toner HP 26A Blk','quantity':'20','unitOfMeasure':'EA'},{'lineNumber':'3','itemCode':'WS8165-PEN12','description':'Workspace Pens Black Box 12','quantity':'100','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Expected Response Format

Each test should return a JSON object like:
```json
{
  "status": "success",
  "vendor": {"vendorNumber": "ZEPHYR1", "name": "Zephyr Industrial 7391"},
  "items": {"created": 2, "details": [{"itemCode": "ZEP7391-A1"}, {"itemCode": "ZEP7391-B2"}]},
  "purchaseOrder": {"poNumber": "PO20267391"},
  "errors": [],
  "notes": "New vendor created. 2 new items created. PO and 2 lines created."
}
```

---

## Verification Checklist

After each test, verify:
- [ ] Response is valid JSON (no markdown formatting)
- [ ] Status is "success", "partial", or "failed"
- [ ] Vendor number is exactly 7 characters
- [ ] PO number is exactly 10 characters
- [ ] No 404 errors or URL malformation in errors array
- [ ] Items count matches expected

---

## Test Data Reference (all unique)

| Test | PO Number | Vendor Name | Item Prefix |
|------|-----------|-------------|-------------|
| 1 | PO-2026-7391 | Zephyr Industrial 7391 | ZEP7391- |
| 2 | PO-2026-8452 | QX 8452 | QX8452- |
| 3 | PO-2026-3647 | Nexus Parts Corp 3647 | NXS3647- |
| 4 | PO-2026-5128 | Meridian Global Mfg 5128 | MGM5128- |
| 5 | PO-2026-9273 | Titan Fastener Intl 9273 | TFI9273- |
| 6 | PO-2026-4816 | Rapid Source 4816 | RS4816- |
| 7 | PO-2026-6039 | Volt Circuit Systems 6039 | VCS6039- |
| 8 | PO-2026-2784 | Forge Metal Works 2784 | FMW2784- |
| 9 | PO-2026-1593 | Automate Pro Supply 1593 | APS1593- |
| 10 | PO-2026-8165 | Workspace Solutions 8165 | WS8165- |

---

*Created: 2026-01-31 (All vendors, items, and PO numbers are unique)*
