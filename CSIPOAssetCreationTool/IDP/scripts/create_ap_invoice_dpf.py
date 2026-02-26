"""
Create AP Invoice DPF configuration by modifying the CSI_COCreation_Extract template.
This script takes the exported backup and creates a new DPF for AP Invoice extraction.
"""
import json
import uuid
from pathlib import Path

# Load the backup file
backup_path = Path(__file__).parent.parent / "exports" / "CSI_COCreation_Extract_backup.json"
with open(backup_path, 'r') as f:
    dpf_list = json.load(f)

# We only need the first (v1) DPF structure - it has Entity Classification only
# which is what we want for AP Invoice extraction
template = dpf_list[0]

# Create new DPF based on template
new_dpf = {
    "documetFlowID": 0,  # Will be assigned by system
    "documentFlowName": "CSI_APInvoice_Extract",
    "documentFlowDescription": "Extracts vendor, PO header, and line item data from AP invoices for automated processing by InvoiceAutomation_Agent_v2",
    "activities": [
        {
            "activityId": 0,
            "activityTypeId": 2,  # Entity Classification
            "activityName": "Entity Classification",
            "activityDescription": "Entity Classification",
            "activityProviders": [
                {
                    "providerId": 10,
                    "providerName": "GenAI",
                    "providerDescription": "GenAI Model",
                    "providerGuid": None
                }
            ],
            "seqNo": 0,
            "activityProviderId": 10,
            "status": 0,
            "activityGuild": str(uuid.uuid4()),
            "configurations": None,
            "base_model_guid": "",
            "autoSplit": False,
            "testCount": 20,
            "trainCount": 80,
            "expectedAccuracy": 0,
            "ephocCount": 0
        }
    ],
    "trainingCount": 0,
    "testCount": 0,
    "modelAccuracy": 0,
    "guidID": str(uuid.uuid4()),  # New GUID
    "status": "Active",
    "documentClasses": [
        {
            "documentClassGuid": str(uuid.uuid4()),
            "documentTypeId": 0,
            "documentName": "AP_Invoice_Extraction",
            "documentFields": [
                {
                    "fieldName": "Vendor Name",
                    "description": "The name of the vendor/supplier company that issued this invoice. Look for the company name in the invoice header, From, Sold By, Supplier, or Vendor sections.",
                    "fieldType": "text",
                    "isRequired": False,
                    "idmattributeName": "None"
                },
                {
                    "fieldName": "Vendor Address Line 1",
                    "description": "The primary street address of the vendor/supplier. Look in the vendors company details section.",
                    "fieldType": "text",
                    "isRequired": False,
                    "idmattributeName": "None"
                },
                {
                    "fieldName": "Vendor City",
                    "description": "The city where the vendor/supplier is located. Extract from the vendors address block.",
                    "fieldType": "text",
                    "isRequired": False,
                    "idmattributeName": "None"
                },
                {
                    "fieldName": "Vendor State",
                    "description": "The state or province code (2 characters) where the vendor is located. Convert full state names to 2-character codes.",
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
                    "description": "The vendors business phone number. If no phone number is found, return null.",
                    "fieldType": "text",
                    "isRequired": False,
                    "idmattributeName": "None"
                },
                {
                    "fieldName": "Vendor Email",
                    "description": "The vendors business email address. Extract only valid email addresses. If no email is found, return null.",
                    "fieldType": "text",
                    "isRequired": False,
                    "idmattributeName": "None"
                },
                {
                    "fieldName": "Invoice Number",
                    "description": "The unique invoice number or ID. This will be used as the PO number in SyteLine.",
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
                    "description": "The payment terms code. Common values: N30, N45, N60, COD. Convert descriptive terms to codes.",
                    "fieldType": "text",
                    "isRequired": False,
                    "idmattributeName": "None"
                },
                {
                    "fieldName": "Currency Code",
                    "description": "The 3-letter ISO currency code (USD, EUR, GBP). Default to USD if not specified.",
                    "fieldType": "text",
                    "isRequired": False,
                    "idmattributeName": "None"
                },
                {
                    "fieldName": "PO Reference",
                    "description": "If this invoice references a customer PO number. Look for Your PO, PO Reference.",
                    "fieldType": "text",
                    "isRequired": False,
                    "idmattributeName": "None"
                },
                {
                    "fieldName": "Notes",
                    "description": "Any special instructions, notes, or comments on the invoice. Return null if none.",
                    "fieldType": "text",
                    "isRequired": False,
                    "idmattributeName": "None"
                }
            ],
            "tableHeaders": [
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
                            "description": "The line number or sequence number. If not explicitly shown, assign sequential numbers."
                        },
                        {
                            "fieldId": 0,
                            "documentClassId": 0,
                            "fieldName": "Item Code",
                            "isRequired": False,
                            "dataType": "text",
                            "idmAttributeName": "",
                            "expectedConfidence": 0,
                            "description": "The product code, SKU, part number, or item identifier."
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
                            "description": "The quantity ordered. Provide as a decimal number with 2 decimal places."
                        },
                        {
                            "fieldId": 0,
                            "documentClassId": 0,
                            "fieldName": "Unit of Measure",
                            "isRequired": False,
                            "dataType": "text",
                            "idmAttributeName": "",
                            "expectedConfidence": 0,
                            "description": "The unit of measure. Common values: EA, LB, KG, BOX, CS. Default to EA if not specified."
                        },
                        {
                            "fieldId": 0,
                            "documentClassId": 0,
                            "fieldName": "Unit Price",
                            "isRequired": False,
                            "dataType": "text",
                            "idmAttributeName": "",
                            "expectedConfidence": 0,
                            "description": "The price per unit. Extract numeric value only."
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
            ],
            "baseModelID": "",
            "status": None,
            "idmDocumentType": "",
            "description": "Accounts Payable Invoice document for extraction",
            "documentClassID": 0
        }
    ],
    "configurationAndPrompt": {
        "ocrType": None,
        "dcPrompt": None,
        "ecPrompt": [
            {
                "AP_Invoice_Extraction": """$Entity Classification Prompt Start$User: You are an expert Document-Based Question-Answering tool assigned to extract specified entities from AP (Accounts Payable) invoice documents. Analyze the provided invoice document carefully. The document includes layout details, and the OCR text is provided page by page within <Page {Page Number}> tags. Entities to be detected are marked within <entities></entities> tags. Think step by step and use the clues to consider what information is potentially relevant for an entity.

<entities>
Vendor Name,Vendor Address Line 1,Vendor City,Vendor State,Vendor Zip,Vendor Phone,Vendor Email,Invoice Number,Invoice Date,Payment Terms,Currency Code,PO Reference,Notes
</entities>

Clues:
Vendor Name - The name of the vendor/supplier company that issued this invoice. This is the company we are purchasing goods or services from. Look for the company name in the invoice header, From, Sold By, Supplier, or Vendor sections.
Vendor Address Line 1 - The primary street address of the vendor/supplier. Look in the vendors company details section, typically near the top of the invoice.
Vendor City - The city where the vendor/supplier is located. Extract from the vendors address block.
Vendor State - The state or province code (2 characters) where the vendor is located. Extract the abbreviated state code like IL, CA, NY. If only the full state name is provided, convert to 2-character code.
Vendor Zip - The postal/ZIP code of the vendors address. Include the full ZIP code if available.
Vendor Phone - The vendors business phone number. Look in the vendors contact information section. If no phone number is found, return null.
Vendor Email - The vendors business email address. Extract only valid email addresses. Do not extract website URLs. If no email is found, return null.
Invoice Number - The unique invoice number or ID. This will be used as the PO number in SyteLine (limited to 10 characters). Look for Invoice #, Invoice No., Inv #, or similar labels.
Invoice Date - The date the invoice was issued. Provide in YYYY-MM-DD format. Look for Invoice Date, Date, or Issued Date labels.
Payment Terms - The payment terms code. Common values: N30 (Net 30 days), N45 (Net 45 days), N60 (Net 60 days), COD (Cash on Delivery). If terms are described in words like Net 30 days, convert to N30. If Due upon receipt return COD.
Currency Code - The 3-letter ISO currency code (e.g., USD, EUR, GBP, CAD). Extract from currency symbols or text. $ = USD, Euro = EUR, Pound = GBP. Default to USD if not specified.
PO Reference - If this invoice references a customer PO number (our PO that prompted this invoice), extract it here. Look for Your PO #, PO Reference, Customer PO. This is optional.
Notes - Any special instructions, notes, or comments on the invoice. Include delivery instructions verbatim. Return null if none.

<instructions>
1. There are 13 entities in <entities></entities> tag, be diligent in ensuring to capture all entities value completely upfront without missing any.
2. Go through the clues one by one and understand the meaning of each entity type and extract correct values with less false positive.
3. Avoid calculating any entity value and do not include any other entity outside <entities></entities> tag.
4. If there are multiple instances of one entity type present in the document, extract the primary/first value.
5. Format your output as a JSON object for each type-value pair you extract, in this format: <format> {"entity": <entity selected from <entities> list>, "value": <value text from input document>, "confidence": <confidence in entity match>, "PageNo": <Comma separated all page numbers where the entity is present>}</format>
6. Your response should include text from only document and wrapped in <result></result> tags. Do not include any other explanatory text
7. If an entity appears on multiple pages, list all the corresponding page numbers in the PageNo field as a comma-separated string, e.g., 1,2,4.
8. For Payment Terms, always convert to standard code format (N30, N45, N60, COD, etc.)
9. For Vendor State, always provide 2-character state code.
</instructions>

Return the result as JSON:
<result>
{
    "entities":
    [
        {"entity":"Vendor Name","value":"ACME Supplies Inc", "confidence": 98, "PageNo":"1"},
        {"entity":"Vendor Address Line 1","value":"456 Industrial Blvd", "confidence": 95, "PageNo":"1"},
        {"entity":"Vendor City","value":"Chicago", "confidence": 95, "PageNo":"1"},
        {"entity":"Vendor State","value":"IL", "confidence": 95, "PageNo":"1"},
        {"entity":"Vendor Zip","value":"60601", "confidence": 95, "PageNo":"1"},
        {"entity":"Vendor Phone","value":"312-555-8900", "confidence": 90, "PageNo":"1"},
        {"entity":"Vendor Email","value":"ap@acmesupplies.com", "confidence": 90, "PageNo":"1"},
        {"entity":"Invoice Number","value":"INV2026003", "confidence": 99, "PageNo":"1"},
        {"entity":"Invoice Date","value":"2026-01-28", "confidence": 98, "PageNo":"1"},
        {"entity":"Payment Terms","value":"N30", "confidence": 95, "PageNo":"1"},
        {"entity":"Currency Code","value":"USD", "confidence": 90, "PageNo":"1"},
        {"entity":"PO Reference","value":null, "confidence": 0, "PageNo":""},
        {"entity":"Notes","value":null, "confidence": 0, "PageNo":""}
    ]
}
</result>

Before giving the response, please make sure you return all entities present in <entities></entities> tag. Provide your final response within <result></result> tags.

Expert:$Entity Classification Prompt End$

$Table Detection Prompt Start$
User:
You are an expert document-based table extractor assigned to extract tables from AP invoice documents.
You are given with the document for layout understanding and the complete OCR of document page by page enclosed in <Page {Page Number}> OCR of Page </Page {Page Number}>
Your task is to extract the Line Items Table from all pages of provided document referring the Columns List and Clues.

Tables to Extract: [Line Items]

Task:
1. Analyze the table information thoroughly from the provided OCR text.
2. Refer to the provided image to understand the layout structure of the tables.
3. Extract only the tables mentioned in the Tables to Extract section. Organize the extracted tables into a tabular format.
4. Ensure that all columns from the Column List are included and provide appropriate and correct values.
5. Provide the column headers in the output as Columnname from Columns List.
6. After extracting each table, provide Table Confidence.

Columns List:
Line Items - [Line Number, Item Code, Description, Quantity, Unit of Measure, Unit Price, Due Date]

Clues:
Line Items Table:
Line Number - The line number or sequence number. If not explicitly shown, assign sequential numbers (1, 2, 3...) based on order of appearance in the table.
Item Code - The product code, SKU, part number, or item identifier. Look for columns labeled Item #, SKU, Part No., Product Code, Material, or Item.
Description - The item description or product name. Capture the full description of the product or service.
Quantity - The quantity ordered. Provide as a decimal number with 2 decimal places (e.g., 25.00, 1.50, 100.00). Look for Qty, Quantity, Ordered, Units columns.
Unit of Measure - The unit of measure. Common values: EA (Each), LB (Pound), KG (Kilogram), BOX, CS (Case), FT (Foot), M (Meter), GAL (Gallon), PK (Pack), DZ (Dozen). If each or unit is written, use EA. Default to EA if not specified.
Unit Price - The price per unit. Extract the numeric value only, without currency symbols. Format as decimal (e.g., 25.99, 100.00).
Due Date - The required delivery date for this line item. Provide in YYYY-MM-DD format. Look for Delivery Date, Ship Date, Due Date, Required By. If not specified per line, leave empty.

Guidelines:
1. Ensure that the table has a proper table name matching with the table in Tables to Extract Section.
2. For extra columns, provide them separately under Other with their actual column names from the OCR.
3. For Quantity, always format as decimal with 2 places (e.g., 25 becomes 25.00).
4. For Unit of Measure, convert common variations to standard codes (each/unit -> EA, pound -> LB, etc.).

Output Format:
<result>
{"Table Name": {"rows": [["ColumnName1", "ColumnName2", "ColumnName3", "PageNo"],["cellvalue", "cellvalue", "cellvalue", "1"],["cellvalue", "cellvalue", "cellvalue", "1"]],"Table_Confidence": "Confidence of the Table in float"}}
</result>

Guidelines:
Response should not contain any comments and new lines.
The table structure should be in above format, with proper table names, column names and column values with Page number under column PageNo.
Strictly provide the response containing only valid XML in the above provided structure enclosed in <result></result> and do not use code block formatting or any other text formatting. The json inside result tags should be valid and without any error.
If no table is present in the document or if the document contains an empty table, the output format should be <result></result>.
$Table Detection Prompt End$"""
            }
        ]
    },
    "createtime": None,
    "updatedtime": None,
    "errormsg": "",
    "dpfVersionId": 0,
    "versionID": "1",
    "versionName": "v1",
    "versionStatus": "Active",
    "promptStructure": None,
    "is_default": False,
    "is_base_df": False,
    "t2vNamespace": "",
    "t2vNamespaceCode": "",
    "isImported": 0
}

# Wrap in array like the export format
output = [new_dpf]

# Save to configs directory
output_path = Path(__file__).parent.parent / "configs" / "AP_Invoice_Extract_final.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"[SUCCESS] AP Invoice DPF configuration created: {output_path}")
print(f"\nNew DPF GUID: {new_dpf['guidID']}")
print(f"Document Class GUID: {new_dpf['documentClasses'][0]['documentClassGuid']}")
print(f"\nTo import, run: python import_dpf.py AP_Invoice_Extract_final.json")
