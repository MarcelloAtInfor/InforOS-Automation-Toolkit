# InvoiceAutomation_Agent_v2 EXTREME Test Prompts

Edge cases designed to break the system. Copy/paste each prompt exactly.

**Logical ID**: `lid://infor.syteline.invoice-automation-v2`

---

## Test 11: Special Characters in Names (& ' " /)
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'O\'Brien & Sons / Mfg Co','address':'100 Rock & Roll Blvd, Nashville, TN 37201','phone':'(615) 555-0101','email':'orders@obrien-sons.com'},'purchaseOrder':{'poNumber':'PO-2026-4471','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'OBS4471-AMP1','description':'O\'Brien 50W Amp "Deluxe"','quantity':'10','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'OBS4471-CAB2','description':'Speaker Cabinet 2x12 / 200W','quantity':'5','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 12: Unicode/International Characters (Accents, Umlauts)
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Müller Präzision GmbH 3892','address':'123 Königstraße, München, DE 80331','phone':'+49-89-555-0200','email':'bestellung@muller3892.de'},'purchaseOrder':{'poNumber':'PO-2026-3892','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'MPG3892-FRÄS','description':'Präzisions-Fräskopf 50mm','quantity':'25','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'MPG3892-BOHR','description':'Bohrmaschine Größe L','quantity':'10','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 13: Maximum Line Items (10 lines)
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Mega Order Corp 5567','address':'999 Bulk Purchase Ave, Houston, TX 77001','phone':'(713) 555-0999','email':'bulk@megaorder5567.com'},'purchaseOrder':{'poNumber':'PO-2026-5567','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'MOC5567-IT01','description':'Mega Item Type 01','quantity':'100','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'MOC5567-IT02','description':'Mega Item Type 02','quantity':'200','unitOfMeasure':'EA'},{'lineNumber':'3','itemCode':'MOC5567-IT03','description':'Mega Item Type 03','quantity':'300','unitOfMeasure':'EA'},{'lineNumber':'4','itemCode':'MOC5567-IT04','description':'Mega Item Type 04','quantity':'400','unitOfMeasure':'EA'},{'lineNumber':'5','itemCode':'MOC5567-IT05','description':'Mega Item Type 05','quantity':'500','unitOfMeasure':'EA'},{'lineNumber':'6','itemCode':'MOC5567-IT06','description':'Mega Item Type 06','quantity':'600','unitOfMeasure':'EA'},{'lineNumber':'7','itemCode':'MOC5567-IT07','description':'Mega Item Type 07','quantity':'700','unitOfMeasure':'EA'},{'lineNumber':'8','itemCode':'MOC5567-IT08','description':'Mega Item Type 08','quantity':'800','unitOfMeasure':'EA'},{'lineNumber':'9','itemCode':'MOC5567-IT09','description':'Mega Item Type 09','quantity':'900','unitOfMeasure':'EA'},{'lineNumber':'10','itemCode':'MOC5567-IT10','description':'Mega Item Type 10','quantity':'1000','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 14: Extremely Long Vendor Name (50+ chars) and Long Descriptions
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'International Advanced Manufacturing Technology Solutions Corporation 6623','address':'12345 Super Long Industrial Boulevard Suite 999, Los Angeles, CA 90001','phone':'(213) 555-0888','email':'purchasing@iamtsc6623.com'},'purchaseOrder':{'poNumber':'PO-2026-6623','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'IAM6623-LONGITEM01','description':'Advanced High-Precision Industrial Manufacturing Component Assembly Unit Model XL-5000','quantity':'15','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'IAM6623-LONGITEM02','description':'Ultra-Premium Quality Control Inspection System with Integrated Sensors','quantity':'8','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 15: All Numeric Vendor Name
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'123456789 Corp','address':'100 Numbers Only St, Boston, MA 02101','phone':'(617) 555-0123','email':'numbers@123456789corp.com'},'purchaseOrder':{'poNumber':'PO-2026-7789','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'N7789-000001','description':'Numeric Part 000001','quantity':'111','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'N7789-999999','description':'Numeric Part 999999','quantity':'222','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 16: SQL-Like Strings in Data (Injection Test)
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Select Star LLC 2248','address':'100 DROP TABLE St, DELETE, WA 98001','phone':'(206) 555-0000','email':'test@selectstar2248.com'},'purchaseOrder':{'poNumber':'PO-2026-2248','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'SS2248-UNION','description':'Part WHERE 1=1','quantity':'50','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'SS2248-INSERT','description':'Component OR TRUE','quantity':'25','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 17: HTML/Script-Like Content
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Bold Tag Industries 9934','address':'100 HTML Lane, Markup City, CA 90210','phone':'(310) 555-0404','email':'contact@boldtag9934.com'},'purchaseOrder':{'poNumber':'PO-2026-9934','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'BTI9934-DIV01','description':'Widget with greater than sign','quantity':'40','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'BTI9934-SPAN2','description':'Part less than expected','quantity':'30','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 18: Single Character Vendor Name (Minimum Data)
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'X 1134','address':'1 A St, B, CA 90001','phone':'(000) 000-0001','email':'x@x1134.com'},'purchaseOrder':{'poNumber':'PO-2026-1134','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'X1134-A','description':'A','quantity':'1','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 19: Extreme Quantities (Millions)
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'Bulk Millions Supply 8821','address':'1 Warehouse Way, Memphis, TN 38101','phone':'(901) 555-0001','email':'millions@bulkms8821.com'},'purchaseOrder':{'poNumber':'PO-2026-8821','orderDate':'20260201','warehouse':'MAIN','terms':'N60'},'lineItems':[{'lineNumber':'1','itemCode':'BMS8821-MICRO','description':'Micro Component Bulk','quantity':'5000000','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'BMS8821-NANO','description':'Nano Component Bulk','quantity':'10000000','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Test 20: Mixed Case and Unusual PO Format
```
(RPA Generated) Process this invoice data and create the vendor, items, and purchase order in SyteLine: {'vendor':{'name':'cRaZy CaSe Co 4456','address':'123 UPPERCASE lowercase MiXeD, WeIrD, OH 44101','phone':'(216) 555-CASE','email':'CrAzY@CaSeCo4456.COM'},'purchaseOrder':{'poNumber':'po-2026-4456','orderDate':'20260201','warehouse':'MAIN','terms':'N30'},'lineItems':[{'lineNumber':'1','itemCode':'ccc4456-UPPER','description':'UPPERCASE DESCRIPTION HERE','quantity':'50','unitOfMeasure':'EA'},{'lineNumber':'2','itemCode':'CCC4456-lower','description':'lowercase description here','quantity':'50','unitOfMeasure':'EA'},{'lineNumber':'3','itemCode':'CcC4456-MiXeD','description':'MiXeD CaSe DeScRiPtIoN','quantity':'50','unitOfMeasure':'EA'}]} CRITICAL: Your final response MUST output ONLY a valid JSON object with this structure: {'status':'success|partial|failed','vendor':{'vendorNumber':'...','name':'...'},'items':{'created':N,'details':[{'itemCode':'...'}]},'purchaseOrder':{'poNumber':'...'},'errors':[],'notes':'...'} STATUS VALUES: 'success' = all operations completed, 'partial' = some operations failed (e.g., vendor created but items failed), 'failed' = critical failure. ERRORS: array of error strings from failed operations, include ---DEBUG--- information from failed tools. (empty [] if none). NOTES: additional context (e.g., 'Vendor already existed, used existing VendNum').
```

---

## Edge Case Summary

| Test | Edge Case | Risk |
|------|-----------|------|
| 11 | Special chars: & ' " / | JSON/SQL parsing issues |
| 12 | Unicode: ü ä ö ß ö | Encoding problems |
| 13 | 10 line items | Batch size limits |
| 14 | 50+ char vendor name | Field truncation |
| 15 | All numeric vendor | VendNum generation |
| 16 | SQL keywords | Injection vulnerability |
| 17 | HTML-like content | XSS or parsing issues |
| 18 | Single char name | Minimum validation |
| 19 | Millions qty | Numeric overflow |
| 20 | Mixed case + lowercase PO | Case sensitivity |

---

## What to Watch For

1. **Test 11**: Do special characters get escaped properly?
2. **Test 12**: Does Unicode survive the API round-trip?
3. **Test 13**: Can it handle 10 items in one batch?
4. **Test 14**: Is the vendor name truncated? Description truncated?
5. **Test 15**: What VendNum is generated for "123456789 Corp"?
6. **Test 16**: Are SQL keywords handled safely?
7. **Test 17**: Does < > content cause issues?
8. **Test 18**: What's the minimum viable data?
9. **Test 19**: Can quantities be 5-10 million?
10. **Test 20**: Is PO number case-sensitive?

---

*Created: 2026-01-31 - Extreme edge case tests*
