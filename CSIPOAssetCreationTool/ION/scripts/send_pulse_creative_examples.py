"""
Creative Pulse Examples - Showcasing different text formats, emojis, trees, and properties.

Demonstrates:
    1. ALERT: Security Incident - Deep tree hierarchy with subLevels
    2. NOTIFICATION: Manufacturing Production Report - Rich parameters and formatting
    3. TASK: Quality Control Hold - Multiple action buttons with translations

Usage:
    python send_pulse_creative_examples.py
    python send_pulse_creative_examples.py --alert       # Only alert
    python send_pulse_creative_examples.py --notification # Only notification
    python send_pulse_creative_examples.py --task        # Only task

Prerequisites:
    - Generate token first: python -m shared.auth ION/scripts
"""
import sys
from pathlib import Path
import argparse

# Add parent to path for shared module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import requests
import json
from shared.auth import get_auth_headers
from shared.config import get_base_url
from shared.tenant import get_users

# Configuration
LOGICAL_ID = "lid://infor.rpa.claudecode"
USER_IDENTITY = get_users().get('user1', {}).get('guid', '<USER_GUID>')

# API endpoints
ION_PROCESS_URL = get_base_url('IONSERVICES/process/application')
ALERT_URL = f"{ION_PROCESS_URL}/v1/pulse/alert/create"
NOTIFICATION_URL = f"{ION_PROCESS_URL}/v1/pulse/notification/create"
TASK_URL = f"{ION_PROCESS_URL}/v1/pulse/task/create"


def get_distribution():
    """Return standard distribution list."""
    return [
        {
            "identifier": USER_IDENTITY,
            "type": "USER",
            "sendMail": False
        }
    ]


def send_request(url: str, payload: dict, item_type: str):
    """Send a Pulse request and handle response."""
    headers = get_auth_headers()
    params = {"logicalId": LOGICAL_ID}

    print(f"\n{'='*70}")
    print(f"Sending {item_type}")
    print(f"{'='*70}")
    print(f"URL: {url}")
    print(f"Payload:\n{json.dumps(payload, indent=2)}")

    response = requests.post(url, headers=headers, json=payload, params=params)

    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        result = response.json()
        print(f"\n[SUCCESS] {item_type} created with ID: {result.get('id')}")
        return result
    else:
        print(f"\n[FAILED] {item_type} failed")
        return None


def send_security_alert():
    """
    ALERT: Security Incident Report

    Demonstrates:
    - Deep tree hierarchy with multiple subLevels (3 levels deep)
    - All dataTypes: STRING, INTEGER, DECIMAL, BOOLEAN, DATE, DATETIME
    - Long multiline message with emoji sections
    - Technical formatting with ASCII art tables
    """
    message = """
====================================================
        SECURITY INCIDENT ALERT
        Severity: CRITICAL
====================================================

An anomalous activity pattern has been detected that
requires immediate security review.

INCIDENT SUMMARY
----------------
Incident ID:    SEC-2026-00847
Detection Time: 2026-01-30 14:23:47 UTC
Source System:  ERP-PROD-CLUSTER-01
Classification: Potential Data Exfiltration

THREAT INDICATORS
-----------------
Unusual API call volume detected from service account
'svc_integration_01' accessing customer master data.

   Baseline calls/hour:    150
   Current calls/hour:   4,892 (+3,161%)

Geographic anomaly detected:
   Normal locations: US-EAST, US-WEST, EU-CENTRAL
   Current request:  RU-MOSCOW-DC

IMMEDIATE ACTIONS REQUIRED
--------------------------
1. Review service account permissions
2. Check API gateway logs for full request payload
3. Verify no data has left the perimeter
4. Consider temporary account suspension

This alert was generated automatically by the
Security Operations Center (SOC) monitoring system.

Reference: MITRE ATT&CK T1530 - Data from Cloud Storage
"""

    payload = {
        "message": message,
        "category": "Security Incident",
        "dueDate": "2026-01-30T15:00:00Z",
        "distribution": get_distribution(),
        "details": {
            "name": "Incident Details",
            "properties": [
                {"name": "Incident ID", "value": "SEC-2026-00847", "dataType": "STRING"},
                {"name": "Severity", "value": "CRITICAL", "dataType": "STRING"},
                {"name": "Detection Time", "value": "2026-01-30T14:23:47Z", "dataType": "DATETIME"},
                {"name": "Auto-Escalated", "value": "true", "dataType": "BOOLEAN"},
                {"name": "Risk Score", "value": "94.7", "dataType": "DECIMAL"},
                {"name": "Affected Records", "value": "127834", "dataType": "INTEGER"}
            ],
            "subLevels": [
                {
                    "name": "Threat Intelligence",
                    "properties": [
                        {"name": "Threat Type", "value": "Data Exfiltration Attempt", "dataType": "STRING"},
                        {"name": "Confidence", "value": "87.5", "dataType": "DECIMAL"},
                        {"name": "MITRE ATT&CK", "value": "T1530", "dataType": "STRING"},
                        {"name": "IOC Match", "value": "true", "dataType": "BOOLEAN"}
                    ],
                    "subLevels": [
                        {
                            "name": "Attack Vector Details",
                            "properties": [
                                {"name": "Entry Point", "value": "API Gateway - /api/v2/customers/export", "dataType": "STRING"},
                                {"name": "Protocol", "value": "HTTPS/TLS 1.3", "dataType": "STRING"},
                                {"name": "User Agent", "value": "python-requests/2.28.1", "dataType": "STRING"},
                                {"name": "Request Size (KB)", "value": "2847", "dataType": "INTEGER"}
                            ]
                        }
                    ]
                },
                {
                    "name": "Source Analysis",
                    "properties": [
                        {"name": "Service Account", "value": "svc_integration_01", "dataType": "STRING"},
                        {"name": "Account Age (days)", "value": "847", "dataType": "INTEGER"},
                        {"name": "Last Password Change", "value": "2025-06-15", "dataType": "DATE"},
                        {"name": "MFA Enabled", "value": "false", "dataType": "BOOLEAN"}
                    ],
                    "subLevels": [
                        {
                            "name": "Geographic Analysis",
                            "properties": [
                                {"name": "Source IP", "value": "185.xxx.xxx.47", "dataType": "STRING"},
                                {"name": "Country", "value": "Russian Federation", "dataType": "STRING"},
                                {"name": "City", "value": "Moscow", "dataType": "STRING"},
                                {"name": "ISP", "value": "Digital Ocean Droplet", "dataType": "STRING"},
                                {"name": "Known Bad Actor", "value": "true", "dataType": "BOOLEAN"}
                            ]
                        },
                        {
                            "name": "Activity Comparison",
                            "properties": [
                                {"name": "Baseline Calls/Hr", "value": "150", "dataType": "INTEGER"},
                                {"name": "Current Calls/Hr", "value": "4892", "dataType": "INTEGER"},
                                {"name": "Deviation %", "value": "3161.33", "dataType": "DECIMAL"},
                                {"name": "First Anomaly", "value": "2026-01-30T13:47:22Z", "dataType": "DATETIME"}
                            ]
                        }
                    ]
                },
                {
                    "name": "Affected Assets",
                    "properties": [
                        {"name": "Database", "value": "CUSTMASTER-PROD", "dataType": "STRING"},
                        {"name": "Tables Accessed", "value": "3", "dataType": "INTEGER"},
                        {"name": "Columns Exposed", "value": "47", "dataType": "INTEGER"},
                        {"name": "PII Fields", "value": "12", "dataType": "INTEGER"}
                    ],
                    "subLevels": [
                        {
                            "name": "Data Classification",
                            "properties": [
                                {"name": "Highest Classification", "value": "CONFIDENTIAL", "dataType": "STRING"},
                                {"name": "Contains PII", "value": "true", "dataType": "BOOLEAN"},
                                {"name": "Contains PCI", "value": "false", "dataType": "BOOLEAN"},
                                {"name": "Contains PHI", "value": "false", "dataType": "BOOLEAN"},
                                {"name": "Regulatory Impact", "value": "GDPR, CCPA", "dataType": "STRING"}
                            ]
                        }
                    ]
                },
                {
                    "name": "Response Actions",
                    "properties": [
                        {"name": "Auto-Block Applied", "value": "true", "dataType": "BOOLEAN"},
                        {"name": "Account Suspended", "value": "false", "dataType": "BOOLEAN"},
                        {"name": "SOC Ticket", "value": "SOC-2026-4521", "dataType": "STRING"},
                        {"name": "Escalation Level", "value": "2", "dataType": "INTEGER"}
                    ]
                }
            ]
        }
    }

    return send_request(ALERT_URL, payload, "ALERT (Security Incident)")


def send_production_notification():
    """
    NOTIFICATION: Manufacturing Production Report

    Demonstrates:
    - Rich emoji formatting throughout
    - Many parameters with all dataTypes
    - retention setting (60 days)
    - contextId and subContextId
    - Box drawing characters for tables
    - Progress bars with Unicode blocks
    """
    message = """
====================================================
        PRODUCTION SHIFT REPORT
        Plant: Chicago Assembly - Line 4
        Shift: Day Shift (06:00 - 14:00)
====================================================

SHIFT PERFORMANCE SUMMARY

  Overall Efficiency:  [=========>          ]  89.4%
  Quality Rate:        [==========>         ]  97.2%
  Availability:        [========>           ]  91.8%
  OEE Score:           [========>           ]  79.7%

PRODUCTION METRICS

  Units Produced:     2,847 / 3,200 target (88.9%)
  Defects Found:           79 units (2.8%)
  Rework Items:            23 units
  Scrap:                   12 units

DOWNTIME BREAKDOWN

  Changeover:         42 min
  Mechanical:         18 min
  Quality Hold:       27 min
  Material Wait:      15 min
  ------------------------
  Total Downtime:    102 min (21.3%)

TOP PRODUCED ITEMS

   1. Widget-A (WGT-001)     1,247 units
   2. Gadget-B (GDG-002)       892 units
   3. Component-C (CMP-003)    456 units
   4. Assembly-D (ASM-004)     252 units

ACHIEVEMENTS

   New Record: Fastest changeover time
   Zero Safety Incidents (Day 47)
   Quality above target for 12th day

SHIFT SUPERVISOR NOTES
----------------------
Good shift overall. Minor delay on Line 4-B due to
pneumatic actuator replacement. Team adapted well
and recovered 15 minutes of the lost time.

Recommend preventive maintenance on Station 7
conveyor belt - showing early wear signs.

Great teamwork today! - Mike Chen (Shift Lead)

====================================================
Report generated: 2026-01-30 14:05:00 CST
Next shift: Swing (14:00 - 22:00)
====================================================
"""

    payload = {
        "message": message,
        "category": "Production Report",
        "retention": 60,  # Keep for 60 days
        "contextId": 20260130,  # Date as context
        "subContextId": 1,  # Shift number
        "distribution": get_distribution(),
        "parameters": [
            # Shift Info
            {"name": "Plant Code", "value": "CHI-ASSY-04", "dataType": "STRING"},
            {"name": "Shift Date", "value": "2026-01-30", "dataType": "DATE"},
            {"name": "Shift Start", "value": "2026-01-30T06:00:00Z", "dataType": "DATETIME"},
            {"name": "Shift End", "value": "2026-01-30T14:00:00Z", "dataType": "DATETIME"},
            {"name": "Shift Number", "value": "1", "dataType": "INTEGER"},

            # Production Metrics
            {"name": "Units Produced", "value": "2847", "dataType": "INTEGER"},
            {"name": "Target Units", "value": "3200", "dataType": "INTEGER"},
            {"name": "Production %", "value": "88.97", "dataType": "DECIMAL"},
            {"name": "Defects", "value": "79", "dataType": "INTEGER"},
            {"name": "Defect Rate %", "value": "2.77", "dataType": "DECIMAL"},
            {"name": "Rework Units", "value": "23", "dataType": "INTEGER"},
            {"name": "Scrap Units", "value": "12", "dataType": "INTEGER"},

            # OEE Metrics
            {"name": "Availability %", "value": "91.8", "dataType": "DECIMAL"},
            {"name": "Performance %", "value": "89.4", "dataType": "DECIMAL"},
            {"name": "Quality %", "value": "97.2", "dataType": "DECIMAL"},
            {"name": "OEE Score %", "value": "79.7", "dataType": "DECIMAL"},

            # Downtime
            {"name": "Total Downtime (min)", "value": "102", "dataType": "INTEGER"},
            {"name": "Changeover (min)", "value": "42", "dataType": "INTEGER"},
            {"name": "Mechanical (min)", "value": "18", "dataType": "INTEGER"},
            {"name": "Quality Hold (min)", "value": "27", "dataType": "INTEGER"},
            {"name": "Material Wait (min)", "value": "15", "dataType": "INTEGER"},

            # Safety & Quality
            {"name": "Safety Incidents", "value": "0", "dataType": "INTEGER"},
            {"name": "Days Without Incident", "value": "47", "dataType": "INTEGER"},
            {"name": "Quality Above Target", "value": "true", "dataType": "BOOLEAN"},
            {"name": "Record Set", "value": "true", "dataType": "BOOLEAN"},

            # Personnel
            {"name": "Shift Supervisor", "value": "Mike Chen", "dataType": "STRING"},
            {"name": "Operators On Shift", "value": "24", "dataType": "INTEGER"},
            {"name": "Maintenance Calls", "value": "3", "dataType": "INTEGER"}
        ]
    }

    return send_request(NOTIFICATION_URL, payload, "NOTIFICATION (Production Report)")


def send_quality_task():
    """
    TASK: Quality Control Hold Decision

    Demonstrates:
    - customActions with 4 buttons
    - HIGH priority with dueDate
    - translations (multi-language: ES, DE, FR)
      - translations format: {locale: {message, category, parameterLabels, viewLabels}}
      - parameterLabels keys must match parameter names
      - viewLabels keys must match view names
    - views (data passed to view)
      - views format: {name, label, properties: [{name, value}]}
    - Rich technical formatting with ASCII art
    - All parameter dataTypes (STRING, INTEGER, DECIMAL, BOOLEAN, DATE, DATETIME)
    """
    message = """
====================================================
      QUALITY CONTROL HOLD - DECISION REQUIRED
====================================================

A production lot has been placed on QUALITY HOLD
pending your disposition decision.

LOT INFORMATION
---------------
  Lot Number:      LOT-2026-003847
  Product:         Industrial Bearing Assembly
  Part Number:     BRG-7890-HD
  Quantity:        500 units
  Production Date: 2026-01-29
  Line/Cell:       Assembly Cell 7

DEFECT DETAILS
--------------
  Issue Type:      Dimensional Variance
  Spec Parameter:  Inner Diameter
  Specification:   25.00mm +/- 0.02mm
  Measured Value:  25.04mm (+0.04mm out of spec)

  Measurement Equipment: CMM-003 (Cal Due: 2026-03-15)
  Inspector:             Jennifer Walsh (QC-204)
  Detection Point:       Final Inspection

SAMPLE ANALYSIS
---------------
  Sample Size:    50 units (10% of lot)
  Defective:      23 units (46% fail rate)
  Pattern:        Random distribution across lot

ROOT CAUSE ANALYSIS (Preliminary)
---------------------------------
  Suspected Cause:   Tool wear on Station 3 lathe
  Tool Change:       Due at 2,500 units - currently at 2,847
  Last Calibration:  2026-01-15 (within spec)

FINANCIAL IMPACT
----------------
  Lot Value:         $47,500.00
  Rework Cost (est): $8,200.00
  Scrap Cost (est):  $47,500.00
  Customer Impact:   ACME Corp - Order #ORD-789456
  Ship Date Risk:    2026-02-03 (HIGH)

DISPOSITION OPTIONS
-------------------
  [RELEASE]      - Release as-is with deviation
  [REWORK]       - Send to rework (100% reinspection)
  [SCRAP]        - Scrap entire lot
  [INVESTIGATE]  - Hold for further investigation

====================================================
Quality Hold Workflow: QH-2026-00892
Escalation: Level 2 - Quality Manager
Due: 2026-01-30 17:00 CST
====================================================
"""

    payload = {
        "message": message,
        "category": "Quality Control",
        "priority": "HIGH",
        "dueDate": "2026-01-30T23:00:00Z",
        "contextId": 2026003847,  # Lot number
        "subContextId": 892,  # QC hold number
        "distribution": get_distribution(),
        "parameters": [
            # Decision parameter (REQUIRED for customActions)
            {"name": "dispositionDecision", "value": "", "dataType": "STRING"},

            # Lot Information
            {"name": "Lot Number", "value": "LOT-2026-003847", "dataType": "STRING"},
            {"name": "Part Number", "value": "BRG-7890-HD", "dataType": "STRING"},
            {"name": "Product Name", "value": "Industrial Bearing Assembly", "dataType": "STRING"},
            {"name": "Quantity", "value": "500", "dataType": "INTEGER"},
            {"name": "Production Date", "value": "2026-01-29", "dataType": "DATE"},
            {"name": "Production Line", "value": "Assembly Cell 7", "dataType": "STRING"},

            # Defect Details
            {"name": "Defect Type", "value": "Dimensional Variance", "dataType": "STRING"},
            {"name": "Specification Min", "value": "24.98", "dataType": "DECIMAL"},
            {"name": "Specification Max", "value": "25.02", "dataType": "DECIMAL"},
            {"name": "Measured Value", "value": "25.04", "dataType": "DECIMAL"},
            {"name": "Variance", "value": "0.04", "dataType": "DECIMAL"},
            {"name": "Out of Spec", "value": "true", "dataType": "BOOLEAN"},

            # Sample Analysis
            {"name": "Sample Size", "value": "50", "dataType": "INTEGER"},
            {"name": "Defective Count", "value": "23", "dataType": "INTEGER"},
            {"name": "Fail Rate %", "value": "46.0", "dataType": "DECIMAL"},

            # Equipment
            {"name": "Measurement Equipment", "value": "CMM-003", "dataType": "STRING"},
            {"name": "Calibration Due", "value": "2026-03-15", "dataType": "DATE"},
            {"name": "Equipment In Spec", "value": "true", "dataType": "BOOLEAN"},
            {"name": "Inspector ID", "value": "QC-204", "dataType": "STRING"},
            {"name": "Inspector Name", "value": "Jennifer Walsh", "dataType": "STRING"},

            # Root Cause
            {"name": "Suspected Cause", "value": "Tool wear on Station 3 lathe", "dataType": "STRING"},
            {"name": "Tool Life Limit", "value": "2500", "dataType": "INTEGER"},
            {"name": "Current Tool Count", "value": "2847", "dataType": "INTEGER"},
            {"name": "Tool Overdue", "value": "true", "dataType": "BOOLEAN"},

            # Financial
            {"name": "Lot Value", "value": "47500.00", "dataType": "DECIMAL"},
            {"name": "Rework Cost Est", "value": "8200.00", "dataType": "DECIMAL"},
            {"name": "Scrap Cost Est", "value": "47500.00", "dataType": "DECIMAL"},
            {"name": "Currency", "value": "USD", "dataType": "STRING"},

            # Customer Impact
            {"name": "Customer Name", "value": "ACME Corporation", "dataType": "STRING"},
            {"name": "Customer Order", "value": "ORD-789456", "dataType": "STRING"},
            {"name": "Ship Date", "value": "2026-02-03", "dataType": "DATE"},
            {"name": "Ship Date At Risk", "value": "true", "dataType": "BOOLEAN"},

            # Workflow
            {"name": "QC Hold Number", "value": "QH-2026-00892", "dataType": "STRING"},
            {"name": "Escalation Level", "value": "2", "dataType": "INTEGER"},
            {"name": "Hold Created", "value": "2026-01-30T08:15:00Z", "dataType": "DATETIME"}
        ],
        "customActions": {
            "parameterName": "dispositionDecision",
            "buttons": [
                {"label": "Release", "value": "RELEASE"},
                {"label": "Rework", "value": "REWORK"},
                {"label": "Scrap", "value": "SCRAP"},
                {"label": "Investigate", "value": "INVESTIGATE"}
            ]
        },
        "translations": {
            "es-ES": {
                "message": "CONTROL DE CALIDAD - Se requiere decision de disposicion para el lote LOT-2026-003847",
                "category": "Control de Calidad",
                "parameterLabels": {
                    "Lot Number": "Numero de Lote",
                    "Part Number": "Numero de Pieza",
                    "Quantity": "Cantidad",
                    "Defect Type": "Tipo de Defecto"
                },
                "viewLabels": {
                    "lot_details": "Ver Detalles del Lote",
                    "customer_order": "Ver Pedido del Cliente"
                }
            },
            "de-DE": {
                "message": "QUALITAETSKONTROLLE - Verfuegungsentscheidung fuer Los LOT-2026-003847 erforderlich",
                "category": "Qualitaetskontrolle",
                "parameterLabels": {
                    "Lot Number": "Losnummer",
                    "Part Number": "Teilenummer",
                    "Quantity": "Menge",
                    "Defect Type": "Fehlerart"
                },
                "viewLabels": {
                    "lot_details": "Losdetails anzeigen",
                    "customer_order": "Kundenauftrag anzeigen"
                }
            },
            "fr-FR": {
                "message": "CONTROLE QUALITE - Decision de disposition requise pour le lot LOT-2026-003847",
                "category": "Controle Qualite",
                "parameterLabels": {
                    "Lot Number": "Numero de Lot",
                    "Part Number": "Numero de Piece",
                    "Quantity": "Quantite",
                    "Defect Type": "Type de Defaut"
                },
                "viewLabels": {
                    "lot_details": "Voir Details du Lot",
                    "customer_order": "Voir Commande Client"
                }
            }
        },
        "views": [
            {
                "name": "lot_details",
                "label": "View Lot Details",
                "properties": [
                    {"name": "lotNumber", "value": "LOT-2026-003847"},
                    {"name": "partNumber", "value": "BRG-7890-HD"}
                ]
            },
            {
                "name": "customer_order",
                "label": "View Customer Order",
                "properties": [
                    {"name": "orderNumber", "value": "ORD-789456"},
                    {"name": "customerName", "value": "ACME Corporation"}
                ]
            }
        ]
    }

    return send_request(TASK_URL, payload, "TASK (Quality Control Hold)")


def main():
    parser = argparse.ArgumentParser(description='Send creative Pulse examples')
    parser.add_argument('--alert', action='store_true', help='Send only the Security Alert')
    parser.add_argument('--notification', action='store_true', help='Send only the Production Notification')
    parser.add_argument('--task', action='store_true', help='Send only the Quality Task')
    args = parser.parse_args()

    # If no specific type requested, send all
    send_all = not (args.alert or args.notification or args.task)

    print("\n" + "="*70)
    print("ION Pulse API - Creative Examples")
    print("Showcasing: Deep trees, rich formatting, translations, drillbacks")
    print("="*70)

    results = {}

    if send_all or args.alert:
        results['alert'] = send_security_alert()

    if send_all or args.notification:
        results['notification'] = send_production_notification()

    if send_all or args.task:
        results['task'] = send_quality_task()

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    for item_type, result in results.items():
        if result:
            print(f"  {item_type.upper()}: ID {result.get('id')}")
        else:
            print(f"  {item_type.upper()}: FAILED")
    print("="*70)
    print("\nCheck your Infor OS Pulse inbox for the messages!")
    print("\nHighlights to verify:")
    print("  - ALERT: Deep tree hierarchy (4 levels), all dataTypes")
    print("  - NOTIFICATION: 30 parameters, retention=60 days, ASCII tables")
    print("  - TASK: 4 action buttons, translations (ES/DE/FR), drillback views")


if __name__ == "__main__":
    main()
