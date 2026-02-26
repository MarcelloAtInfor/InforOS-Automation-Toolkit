"""
Create AP Invoice DPF by modifying a copy of the CSI_COCreation_Extract template.
Uses deep copy and only changes essential fields to ensure format compatibility.
"""
import json
import uuid
import copy
from pathlib import Path
from datetime import datetime

# Load the backup file
backup_path = Path(__file__).parent.parent / "exports" / "CSI_COCreation_Extract_backup.json"
with open(backup_path, 'r', encoding='utf-8') as f:
    dpf_list = json.load(f)

# Use first version (v1) as template - it has just Entity Classification
template = copy.deepcopy(dpf_list[0])

# Generate new GUIDs
new_dpf_guid = str(uuid.uuid4())
new_activity_guid = str(uuid.uuid4())
new_doc_class_guid = str(uuid.uuid4())

# Update basic info
template['documetFlowID'] = 0
template['documentFlowName'] = "CSI_APInvoice_Extract"
template['documentFlowDescription'] = "Extracts vendor, PO header, and line item data from AP invoices"
template['guidID'] = new_dpf_guid
template['dpfVersionId'] = 0
template['versionID'] = "1"
template['versionName'] = "v1"
template['versionStatus'] = "Active"
template['createtime'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
template['updatedtime'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

# Update activity
template['activities'][0]['activityId'] = 0
template['activities'][0]['activityGuild'] = new_activity_guid

# Update document class
doc_class = template['documentClasses'][0]
doc_class['documentClassGuid'] = new_doc_class_guid
doc_class['documentTypeId'] = 0
doc_class['documentName'] = "AP_Invoice_Extraction"
doc_class['description'] = "Accounts Payable Invoice document for extraction"

# Update document fields for AP Invoice
doc_class['documentFields'] = [
    {
        "fieldName": "Vendor Name",
        "description": "The name of the vendor/supplier company that issued this invoice.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    },
    {
        "fieldName": "Vendor Address Line 1",
        "description": "The primary street address of the vendor/supplier.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    },
    {
        "fieldName": "Vendor City",
        "description": "The city where the vendor/supplier is located.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    },
    {
        "fieldName": "Vendor State",
        "description": "The state or province code (2 characters) where the vendor is located.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    },
    {
        "fieldName": "Vendor Zip",
        "description": "The postal/ZIP code of the vendors address.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    },
    {
        "fieldName": "Vendor Phone",
        "description": "The vendors business phone number. Return null if not found.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    },
    {
        "fieldName": "Vendor Email",
        "description": "The vendors business email address. Return null if not found.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    },
    {
        "fieldName": "Invoice Number",
        "description": "The unique invoice number or ID.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    },
    {
        "fieldName": "Invoice Date",
        "description": "The date the invoice was issued. Provide in YYYY-MM-DD format.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    },
    {
        "fieldName": "Payment Terms",
        "description": "The payment terms code such as N30, N45, N60, COD.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    },
    {
        "fieldName": "Currency Code",
        "description": "The 3-letter ISO currency code such as USD, EUR, GBP.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    },
    {
        "fieldName": "PO Reference",
        "description": "If this invoice references a customer PO number.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    },
    {
        "fieldName": "Notes",
        "description": "Any special instructions, notes, or comments on the invoice.",
        "fieldType": "text",
        "isRequired": False,
        "idmattributeName": "None"
    }
]

# Update table headers for line items
doc_class['tableHeaders'] = [
    {
        "tableId": 0,
        "documentClassId": 0,
        "tableName": "Line Items",
        "tableFields": [
            {
                "fieldId": 0,
                "documentClassId": 0,
                "fieldName": "Line Number",
                "isRequired": False,
                "dataType": "text",
                "idmAttributeName": "",
                "expectedConfidence": 0,
                "description": "The line number or sequence number."
            },
            {
                "fieldId": 0,
                "documentClassId": 0,
                "fieldName": "Item Code",
                "isRequired": False,
                "dataType": "text",
                "idmAttributeName": "",
                "expectedConfidence": 0,
                "description": "The product code, SKU, part number."
            },
            {
                "fieldId": 0,
                "documentClassId": 0,
                "fieldName": "Description",
                "isRequired": False,
                "dataType": "text",
                "idmAttributeName": "",
                "expectedConfidence": 0,
                "description": "The item description or product name."
            },
            {
                "fieldId": 0,
                "documentClassId": 0,
                "fieldName": "Quantity",
                "isRequired": False,
                "dataType": "text",
                "idmAttributeName": "",
                "expectedConfidence": 0,
                "description": "The quantity ordered."
            },
            {
                "fieldId": 0,
                "documentClassId": 0,
                "fieldName": "Unit of Measure",
                "isRequired": False,
                "dataType": "text",
                "idmAttributeName": "",
                "expectedConfidence": 0,
                "description": "The unit of measure such as EA, LB, KG, BOX."
            },
            {
                "fieldId": 0,
                "documentClassId": 0,
                "fieldName": "Unit Price",
                "isRequired": False,
                "dataType": "text",
                "idmAttributeName": "",
                "expectedConfidence": 0,
                "description": "The price per unit."
            },
            {
                "fieldId": 0,
                "documentClassId": 0,
                "fieldName": "Due Date",
                "isRequired": False,
                "dataType": "text",
                "idmAttributeName": "",
                "expectedConfidence": 0,
                "description": "The required delivery date in YYYY-MM-DD format."
            }
        ],
        "isRequired": False,
        "idmAttributeName": "None",
        "expectedConfidence": 0,
        "description": ""
    }
]

# Update the prompts - use the same structure but update for AP Invoice
entity_prompt = """$Entity Classification Prompt Start$User: You are an expert Document-Based Question-Answering tool assigned to extract specified entities from AP invoice documents. The OCR text is provided page by page within <Page {Page Number}> tags.

<entities>
Vendor Name,Vendor Address Line 1,Vendor City,Vendor State,Vendor Zip,Vendor Phone,Vendor Email,Invoice Number,Invoice Date,Payment Terms,Currency Code,PO Reference,Notes
</entities>

Clues:
Vendor Name - The vendor/supplier company name that issued this invoice.
Vendor Address Line 1 - The primary street address of the vendor.
Vendor City - The city where the vendor is located.
Vendor State - The state code (2 characters) where the vendor is located.
Vendor Zip - The postal/ZIP code of the vendors address.
Vendor Phone - The vendors phone number. Return null if not found.
Vendor Email - The vendors email address. Return null if not found.
Invoice Number - The unique invoice number or ID.
Invoice Date - The date the invoice was issued. Provide in YYYY-MM-DD format.
Payment Terms - The payment terms code (N30, N45, N60, COD).
Currency Code - The 3-letter ISO currency code (USD, EUR, GBP).
PO Reference - If this invoice references a customer PO number.
Notes - Any special instructions or comments. Return null if none.

<instructions>
1. Extract all 13 entities completely.
2. Format your output as JSON: {"entity": <entity name>, "value": <value>, "confidence": <confidence>, "PageNo": <page numbers>}
3. Wrap response in <result></result> tags.
</instructions>

Return the result as JSON:
<result>
{
    "entities":
    [
        {"entity":"Vendor Name","value":"Example Corp", "confidence": 98, "PageNo":"1"}
    ]
}
</result>

Expert:$Entity Classification Prompt End$

$Table Detection Prompt Start$
User:
You are an expert table extractor. Extract the Line Items Table.

Tables to Extract: [Line Items]

Columns List:
Line Items - [Line Number, Item Code, Description, Quantity, Unit of Measure, Unit Price, Due Date]

Output Format:
<result>
{"Table Name": {"rows": [["Col1", "Col2", "PageNo"],["val", "val", "1"]],"Table_Confidence": "90"}}
</result>
$Table Detection Prompt End$"""

template['configurationAndPrompt']['ecPrompt'] = [
    {"AP_Invoice_Extraction": entity_prompt}
]

# Output as array (same as export format)
output = [template]

# Save to configs directory
output_path = Path(__file__).parent.parent / "configs" / "AP_Invoice_Extract_v3.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"[SUCCESS] AP Invoice DPF configuration created: {output_path}")
print(f"\nNew DPF GUID: {new_dpf_guid}")
print(f"Document Class GUID: {new_doc_class_guid}")
print(f"\nTo import, run: python import_dpf.py AP_Invoice_Extract_v3.json")
