#!/usr/bin/env python3
"""Generate a 50-invoice V2 mass-test batch with expected-outcome manifest."""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from generate_test_invoice import draw_invoice


@dataclass
class InvoiceSpec:
    index: int
    filename: str
    scenario_group: str
    expected_status: str
    expected_vendor_number: str
    expected_behavior: str
    vendor_name: str
    vendor_address: str
    vendor_phone: str
    vendor_email: str
    po_number: str
    order_date: str
    sales_tax: str
    lines: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        default=r"C:\InforRPA\DemoInvoiceLoaderV2\MassTest\2026-03-08_Batch50",
        help="Root folder where Input and manifest files will be created.",
    )
    return parser.parse_args()


def invoice(
    index: int,
    scenario_group: str,
    expected_status: str,
    expected_vendor_number: str,
    expected_behavior: str,
    vendor_name: str,
    vendor_address: str,
    vendor_phone: str,
    vendor_email: str,
    po_number: str,
    order_date: str,
    sales_tax: str,
    lines: Iterable[str],
) -> InvoiceSpec:
    return InvoiceSpec(
        index=index,
        filename=f"Invoice_V2_Mass_{index:02d}.pdf",
        scenario_group=scenario_group,
        expected_status=expected_status,
        expected_vendor_number=expected_vendor_number,
        expected_behavior=expected_behavior,
        vendor_name=vendor_name,
        vendor_address=vendor_address,
        vendor_phone=vendor_phone,
        vendor_email=vendor_email,
        po_number=po_number,
        order_date=order_date,
        sales_tax=sales_tax,
        lines=list(lines),
    )


def line(line_no: int, item_code: str, description: str, qty: str, uom: str, unit_price: str) -> str:
    return f"{line_no}|{item_code}|{description}|{qty}|{uom}|{unit_price}"


def build_specs() -> list[InvoiceSpec]:
    specs: list[InvoiceSpec] = []

    bicycle_name = "Bicycle Parts Company"
    bicycle_address = "7768 E Lincoln Way, Apple Creek, OH 44606"
    bicycle_email = "william.davis@inforbc.com"
    bicycle_phone = "330-684-2607"

    bicycle_variants = [
        (bicycle_name, bicycle_address, bicycle_phone, bicycle_email),
        (bicycle_name, bicycle_address, "3306842607", bicycle_email),
        (bicycle_name, bicycle_address, "(330) 684-2607", bicycle_email),
        (bicycle_name, bicycle_address, bicycle_phone, "WILLIAM.DAVIS@INFORBC.COM"),
        ("BICYCLE PARTS COMPANY", bicycle_address, bicycle_phone, bicycle_email),
        (bicycle_name, "7768 E LINCOLN WAY, APPLE CREEK, OH 44606", bicycle_phone, bicycle_email),
        (bicycle_name, "7768 E Lincoln Way , Apple Creek, OH 44606", bicycle_phone, bicycle_email),
        (bicycle_name, bicycle_address, "330 684 2607", bicycle_email),
        (bicycle_name, bicycle_address, bicycle_phone, "William.Davis@InforBC.com"),
        (bicycle_name, bicycle_address, bicycle_phone, bicycle_email),
        (bicycle_name, bicycle_address, bicycle_phone, bicycle_email),
        (bicycle_name, bicycle_address, bicycle_phone, bicycle_email),
    ]

    bicycle_lines = [
        [line(1, "BMX-CBL-2801", "Bicycle Shift Cable Kit", "8", "EA", "14.25"), line(2, "BMX-HDL-2802", "Drop Bar Handle Assembly", "4", "EA", "48.90"), line(3, "BMX-SPK-2803", "Stainless Spoke Pack", "12", "EA", "6.80")],
        [line(1, "BMX-BRG-2804", "Bottom Bracket Set", "5", "EA", "29.40"), line(2, "BMX-RTR-2805", "Disc Rotor 160mm", "6", "EA", "18.95"), line(3, "BMX-PDL-2806", "Pedal Bearing Kit", "10", "EA", "9.10")],
        [line(1, "BMX-FRK-2807", "Fork Crown Race", "7", "EA", "11.45"), line(2, "BMX-STM-2808", "Stem Clamp Alloy", "4", "EA", "37.80"), line(3, "BMX-TBB-2809", "Tubeless Tape Roll", "9", "EA", "7.25")],
        [line(1, "BMX-GRD-2810", "Chain Guard Plate", "3", "EA", "26.15"), line(2, "BMX-SDL-2811", "Saddle Rail Clamp", "5", "EA", "17.35"), line(3, "BMX-VAL-2812", "Valve Extender Pack", "11", "EA", "4.90")],
        [line(1, "BMX-HUB-2813", "Front Hub Locknut", "8", "EA", "8.40"), line(2, "BMX-AXL-2814", "Axle Spacer Kit", "6", "EA", "12.55"), line(3, "BMX-CLM-2815", "Seat Clamp 34.9", "5", "EA", "10.20")],
        [line(1, "BMX-ARM-2816", "Crank Fixing Bolt", "14", "EA", "3.95"), line(2, "BMX-LNK-2817", "Derailleur Link Plate", "7", "EA", "16.80"), line(3, "BMX-NPL-2818", "Nipple Washer Set", "20", "EA", "1.90")],
        [line(1, "BMX-RNG-2819", "Chain Ring Guard", "4", "EA", "31.25"), line(2, "BMX-SKT-2820", "Cassette Spacer Pack", "12", "EA", "5.75"), line(3, "BMX-BLT-2821", "Bottle Cage Bolt", "24", "EA", "0.95")],
        [line(1, "BMX-CLP-2822", "Cable End Clip", "30", "EA", "0.85"), line(2, "BMX-BSH-2823", "Pivot Bushing Set", "9", "EA", "7.60"), line(3, "BMX-RNG-2824", "Retaining Ring", "13", "EA", "2.40")],
        [line(1, "BMX-EXT-2825", "Stem Extension Collar", "5", "EA", "21.45"), line(2, "BMX-CAP-2826", "Headset Top Cap", "7", "EA", "6.70"), line(3, "BMX-INS-2827", "Tube Insert Sleeve", "10", "EA", "3.80")],
        [line(1, "BMX-LVR-2828", "Brake Lever Reach Screw", "16", "EA", "1.25"), line(2, "BMX-PAD-2829", "Disc Pad Spring", "12", "EA", "2.95"), line(3, "BMX-CLS-2830", "Quick Release Clamp", "6", "EA", "13.90")],
        [line(1, "CHAIN-RING-5T6K", "Anodized Chain Ring 52T", "4", "EA", "44.80"), line(2, "HUB-REAR-8L2P", "Rear Hub Cartridge Unit", "3", "EA", "63.50"), line(3, "SEAT-POST-V3N7", "Alloy Seat Post 31.6mm", "5", "EA", "32.10")],
        [line(1, "CRNK-ARMS-7Q1A", "Forged Crank Arm Assembly", "2", "EA", "86.40"), line(2, "PEDL-BODY-2M4C", "Composite Pedal Body Kit", "6", "EA", "22.85"), line(3, "RIM-ALUM-9Z8H", "Aluminum Wheel Rim 700C", "3", "EA", "58.95")],
    ]
    bicycle_taxes = ["21.36", "18.74", "16.22", "19.48", "17.02", "14.91", "20.55", "12.84", "15.63", "13.47", "24.18", "26.44"]

    for idx in range(12):
        name, address, phone, email = bicycle_variants[idx]
        specs.append(invoice(idx + 1, "reuse_base_threshold_bicycle", "SUCCESS", "1", "Existing vendor should reuse by name+address; phone/email formatting should not break selection.", name, address, phone, email, f"PO263850{idx + 1:02d}", f"2026-03-{9 + (idx % 5):02d}", bicycle_taxes[idx], bicycle_lines[idx]))

    pioneer_name = "Pioneer Fluid Works"
    pioneer_address = "6512 Delta Park Blvd, Dayton, OH 45414"
    pioneer_phone = "937-555-0199"
    pioneer_email = "ap@pioneerfluid.example"
    pioneer_variants = [
        (pioneer_name, pioneer_address, pioneer_phone, pioneer_email),
        (pioneer_name, pioneer_address, "9375550199", pioneer_email),
        (pioneer_name, pioneer_address, pioneer_phone, "AP@PIONEERFLUID.EXAMPLE"),
        (pioneer_name.upper(), pioneer_address, pioneer_phone, pioneer_email),
    ]
    pioneer_lines = [
        [line(1, "PFW-MAN-2801", "Fluid Manifold Block", "3", "EA", "118.40"), line(2, "PFW-ORG-2802", "O-Ring Gland Kit", "8", "EA", "12.90"), line(3, "PFW-FLT-2803", "Inline Filter Screen", "7", "EA", "17.75")],
        [line(1, "PFW-PRT-2804", "Pressure Tap Assembly", "6", "EA", "24.10"), line(2, "PFW-SFT-2805", "Pump Shaft Coupler", "4", "EA", "46.30"), line(3, "PFW-HSG-2806", "Reservoir Housing", "2", "EA", "133.80")],
        [line(1, "PFW-SLP-2807", "Slip Ring Adapter", "5", "EA", "29.95"), line(2, "PFW-CHK-2808", "Check Valve Insert", "10", "EA", "9.45"), line(3, "PFW-PNL-2809", "Control Panel Face", "3", "EA", "54.70")],
        [line(1, "PFW-GSK-2810", "Gasket Plate Set", "9", "EA", "7.85"), line(2, "PFW-SNS-2811", "Pressure Switch Block", "3", "EA", "68.25"), line(3, "PFW-ARM-2812", "Mounting Arm", "4", "EA", "31.40")],
    ]
    pioneer_taxes = ["23.91", "28.44", "19.87", "17.22"]
    for offset in range(4):
        name, address, phone, email = pioneer_variants[offset]
        specs.append(invoice(13 + offset, "reuse_exact_pioneer", "SUCCESS", "PIONE01", "Existing vendor should reuse; normalized phone/email/name casing should not change the match.", name, address, phone, email, f"PO263850{13 + offset:02d}", f"2026-03-{10 + offset:02d}", pioneer_taxes[offset], pioneer_lines[offset]))

    north_name = "North Ridge Controls"
    north_address = "9025 Innovation Way, Madison, WI 53718"
    north_phone = "608-555-0137"
    north_email = "billing@northridgecontrols.example"
    north_variants = [
        (north_name, north_address, north_phone, north_email),
        (north_name, north_address, "6085550137", north_email),
        (north_name, north_address, north_phone, "BILLING@NORTHRIDGECONTROLS.EXAMPLE"),
        (north_name.upper(), north_address, north_phone, north_email),
    ]
    north_lines = [
        [line(1, "NRC-SNS-19A", "North Ridge Sensor Array", "5", "PCS", "48.20"), line(2, "NRC-CBL-19B", "North Ridge Control Cable", "9", "PR", "6.55"), line(3, "V2OCRITEM1", "V2 OCR Sample Item 1", "4", "PCS", "22.10")],
        [line(1, "NRC-SNS-19A", "North Ridge Sensor Array", "6", "PCS", "48.20"), line(2, "NRC-CBL-19B", "North Ridge Control Cable", "10", "PR", "6.55"), line(3, "V2OCRITEM2", "V2 OCR Sample Item 2", "3", "PCS", "18.40")],
        [line(1, "NRC-SNS-19A", "North Ridge Sensor Array", "4", "PCS", "48.20"), line(2, "NRC-CBL-19B", "North Ridge Control Cable", "8", "PR", "6.55"), line(3, "V2OCRITEM1", "V2 OCR Sample Item 1", "5", "PCS", "22.10")],
        [line(1, "NRC-SNS-19A", "North Ridge Sensor Array", "7", "PCS", "48.20"), line(2, "NRC-CBL-19B", "North Ridge Control Cable", "11", "PR", "6.55"), line(3, "V2OCRITEM2", "V2 OCR Sample Item 2", "6", "PCS", "18.40")],
    ]
    north_taxes = ["20.16", "22.04", "19.52", "24.11"]
    for offset in range(4):
        name, address, phone, email = north_variants[offset]
        specs.append(invoice(17 + offset, "reuse_north_uom_fallback", "SUCCESS", "NORTH03", "Existing vendor should reuse and reused items should resolve to persisted UM=EA even when OCR sends PCS/PR.", name, address, phone, email, f"PO263850{17 + offset:02d}", f"2026-03-{11 + offset:02d}", north_taxes[offset], north_lines[offset]))

    atlas_name = "Atlas Conveyor Supply"
    atlas_address = "8801 Transit Park Drive, Columbus, OH 43085"
    atlas_phone = "614-555-0177"
    atlas_email = "ap@atlasconveyor.example"
    atlas_variants = [
        (atlas_name, atlas_address, atlas_phone, atlas_email),
        (atlas_name, atlas_address, "6145550177", atlas_email),
        (atlas_name, atlas_address, atlas_phone, "AP@ATLASCONVEYOR.EXAMPLE"),
        (atlas_name.upper(), atlas_address, atlas_phone, atlas_email),
    ]
    atlas_lines = [
        [line(1, "ATS-RLR-2801", "Conveyor Roller Set", "8", "EA", "27.60"), line(2, "ATS-MNT-2802", "Motor Mount Plate", "4", "EA", "73.90"), line(3, "ATS-BRG-2803", "Bearing Housing Block", "6", "EA", "32.15")],
        [line(1, "ATS-SFT-2804", "Drive Shaft Sleeve", "5", "EA", "41.25"), line(2, "ATS-GRD-2805", "Safety Guard Panel", "3", "EA", "88.40"), line(3, "ATS-TRK-2806", "Tracking Wheel Kit", "4", "EA", "59.80")],
        [line(1, "ATS-LNK-2807", "Chain Link Segment", "20", "EA", "3.85"), line(2, "ATS-BLT-2808", "Mount Bolt Assortment", "30", "EA", "1.15"), line(3, "ATS-PAD-2809", "Guide Pad Insert", "10", "EA", "6.40")],
        [line(1, "ATS-RLS-2810", "Return Roller Spacer", "9", "EA", "5.95"), line(2, "ATS-HNG-2811", "Hinge Support Bracket", "6", "EA", "24.70"), line(3, "ATS-DRV-2812", "Drive Coupling", "4", "EA", "66.30")],
    ]
    atlas_taxes = ["26.18", "31.07", "14.36", "19.82"]
    for offset in range(4):
        name, address, phone, email = atlas_variants[offset]
        specs.append(invoice(21 + offset, "reuse_exact_atlas", "SUCCESS", "ATLASC1", "Existing vendor should reuse using exact identity with normalized phone/email/name formatting.", name, address, phone, email, f"PO263850{21 + offset:02d}", f"2026-03-{12 + offset:02d}", atlas_taxes[offset], atlas_lines[offset]))

    specs.extend([
        invoice(25, "reuse_existing_granite", "SUCCESS", "GRANIT1", "Existing vendor should reuse using exact live identity.", "Granite Motion Supply", "1188 Foundry Avenue, Rockford, IL 61109", "(815) 555-2864", "orders@granitemotion.com", "PO26385025", "2026-03-15", "27.34", [line(1, "PUMP-HSG-3W5E", "Pump Housing Cast Body", "3", "EA", "214.60"), line(2, "VALV-CORE-6N2J", "Hydraulic Valve Core", "4", "EA", "38.70"), line(3, "SEAL-KIT-1R8D", "Pressure Seal Service Kit", "5", "EA", "29.15")]),
        invoice(26, "reuse_existing_granite", "SUCCESS", "GRANIT1", "Existing vendor should reuse even with compact phone formatting.", "Granite Motion Supply", "1188 Foundry Avenue, Rockford, IL 61109", "8155552864", "orders@granitemotion.com", "PO26385026", "2026-03-16", "19.66", [line(1, "PUMP-HSG-3W5E", "Pump Housing Cast Body", "2", "EA", "214.60"), line(2, "VALV-CORE-6N2J", "Hydraulic Valve Core", "5", "EA", "38.70"), line(3, "SEAL-KIT-1R8D", "Pressure Seal Service Kit", "6", "EA", "29.15")]),
        invoice(27, "reuse_existing_v2ocr", "SUCCESS", "V2OCR01", "Existing vendor should reuse using exact live identity.", "V2 OCR Sample Supply", "1248 Foundry Parkway, Toledo, OH 43604", "419-555-0144", "ap@v2ocrsample.example", "PO26385027", "2026-03-15", "18.55", [line(1, "V2OCRITEM1", "V2 OCR Sample Item 1", "4", "EA", "22.10"), line(2, "V2OCRITEM2", "V2 OCR Sample Item 2", "6", "EA", "18.40")]),
        invoice(28, "reuse_existing_v2ocr", "SUCCESS", "V2OCR01", "Existing vendor should reuse with normalized email casing.", "V2 OCR Sample Supply", "1248 Foundry Parkway, Toledo, OH 43604", "419-555-0144", "AP@V2OCRSAMPLE.EXAMPLE", "PO26385028", "2026-03-16", "16.42", [line(1, "V2OCRITEM1", "V2 OCR Sample Item 1", "5", "EA", "22.10"), line(2, "V2OCRITEM2", "V2 OCR Sample Item 2", "4", "EA", "18.40")]),
    ])

    new_vendor_pairs = [
        ("Lattice Flow Systems", "4108 Harbor Loop Drive, Erie, PA 16509", "814-555-0114", "ap@latticeflow.example", "LFS", 29),
        ("Copper Ridge Motion", "8721 Alloy Point Blvd, Akron, OH 44312", "330-555-0188", "payables@copperridge.example", "CRM", 31),
        ("Delta Shore Controls", "1916 Breakwater Avenue, Cleveland, OH 44114", "216-555-0121", "billing@deltashore.example", "DSC", 33),
        ("Meridian Harbor Drives", "6420 Jetty Park Road, Toledo, OH 43611", "419-555-0172", "ap@meridianharbor.example", "MHD", 35),
        ("Summit Trace Pneumatics", "2558 Summit Field Way, Canton, OH 44708", "330-555-0146", "invoices@summittrace.example", "STP", 37),
        ("Keystone Loop Sensors", "7445 Keystone Commerce Dr, Fort Wayne, IN 46808", "260-555-0159", "ap@keystoneloop.example", "KLS", 39),
    ]
    for vendor_name, address, phone, email, prefix, start_index in new_vendor_pairs:
        pair_lines = [
            [line(1, f"{prefix}-DRV-01A", f"{vendor_name} Drive Module", "4", "EA", "126.40"), line(2, f"{prefix}-SNS-01B", f"{vendor_name} Sensor Node", "6", "EA", "39.25"), line(3, f"{prefix}-MNT-01C", f"{vendor_name} Mounting Plate", "5", "EA", "18.60")],
            [line(1, f"{prefix}-DRV-01A", f"{vendor_name} Drive Module", "3", "EA", "126.40"), line(2, f"{prefix}-SNS-01B", f"{vendor_name} Sensor Node", "5", "EA", "39.25"), line(3, f"{prefix}-MNT-01C", f"{vendor_name} Mounting Plate", "4", "EA", "18.60")],
        ]
        pair_taxes = ["24.75", "19.35"]
        for offset in range(2):
            specs.append(invoice(start_index + offset, "create_then_reuse_standard", "SUCCESS", "", "First invoice should create vendor/items; second should reuse the same identity and items.", vendor_name, address, phone, email if offset == 0 else email.upper(), f"PO263850{start_index + offset:02d}", f"2026-03-{14 + ((start_index + offset) % 5):02d}", pair_taxes[offset], pair_lines[offset]))

    specs.extend([
        invoice(41, "duplicate_po_pair_a", "SUCCESS", "1", "First PO in duplicate pair should succeed.", bicycle_name, bicycle_address, bicycle_phone, bicycle_email, "PO26385041", "2026-03-18", "14.28", [line(1, "BMX-DUP-2841", "Duplicate PO Pair A Item 1", "4", "EA", "28.10"), line(2, "BMX-DUP-2842", "Duplicate PO Pair A Item 2", "6", "EA", "11.45")]),
        invoice(42, "duplicate_po_pair_a", "FAIL_DUPLICATE_PO", "1", "Second invoice uses the same PO and should fail on duplicate PO detection.", bicycle_name, bicycle_address, bicycle_phone, bicycle_email, "PO26385041", "2026-03-19", "12.97", [line(1, "BMX-DUP-2843", "Duplicate PO Pair A Item 3", "5", "EA", "19.80"), line(2, "BMX-DUP-2844", "Duplicate PO Pair A Item 4", "7", "EA", "9.90")]),
        invoice(43, "duplicate_po_pair_b", "SUCCESS", "", "First PO in duplicate pair should create a new vendor and PO successfully.", "Harbor North Drives", "5824 Pier Street, Lorain, OH 44052", "440-555-0148", "ap@harbornorth.example", "PO26385043", "2026-03-18", "22.63", [line(1, "HND-DRV-01A", "Harbor North Drive", "3", "EA", "144.20"), line(2, "HND-SFT-01B", "Harbor North Shaft", "4", "EA", "58.10"), line(3, "HND-MNT-01C", "Harbor North Mount", "5", "EA", "17.45")]),
        invoice(44, "duplicate_po_pair_b", "FAIL_DUPLICATE_PO", "", "Second invoice uses the same PO and should fail on duplicate PO detection after vendor reuse.", "Harbor North Drives", "5824 Pier Street, Lorain, OH 44052", "4405550148", "AP@HARBORNORTH.EXAMPLE", "PO26385043", "2026-03-19", "20.11", [line(1, "HND-DRV-01A", "Harbor North Drive", "2", "EA", "144.20"), line(2, "HND-SFT-01B", "Harbor North Shaft", "3", "EA", "58.10"), line(3, "HND-MNT-01C", "Harbor North Mount", "4", "EA", "17.45")]),
        invoice(45, "fail_closed_wrong_identity", "FAIL_VENDOR_IDENTITY_REVIEW", "1", "Existing-name vendor with wrong address should fail closed instead of silently reusing or creating a duplicate.", bicycle_name, "9911 West Ridge Road, Apple Creek, OH 44606", bicycle_phone, bicycle_email, "PO26385045", "2026-03-20", "11.84", [line(1, "FC-BIC-2845", "Fail Closed Bicycle Item", "3", "EA", "34.10"), line(2, "FC-BIC-2846", "Fail Closed Bicycle Item 2", "4", "EA", "22.95")]),
        invoice(46, "fail_closed_wrong_identity", "FAIL_VENDOR_IDENTITY_REVIEW", "PIONE01", "Existing-name vendor with wrong address should fail closed instead of silently reusing or creating a duplicate.", pioneer_name, "7450 Delta Park Blvd, Dayton, OH 45414", pioneer_phone, pioneer_email, "PO26385046", "2026-03-20", "12.46", [line(1, "FC-PFW-2847", "Fail Closed Pioneer Item", "2", "EA", "71.30"), line(2, "FC-PFW-2848", "Fail Closed Pioneer Item 2", "5", "EA", "16.20")]),
        invoice(47, "fail_closed_wrong_identity", "FAIL_VENDOR_IDENTITY_REVIEW", "NORTH03", "Existing-name vendor with wrong address should fail closed instead of silently reusing or creating a duplicate.", north_name, "9025 Innovation Lane, Madison, WI 53718", north_phone, north_email, "PO26385047", "2026-03-20", "13.18", [line(1, "FC-NRC-2849", "Fail Closed North Item", "3", "PCS", "42.80"), line(2, "FC-NRC-2850", "Fail Closed North Item 2", "6", "PR", "8.95")]),
        invoice(48, "fail_closed_wrong_identity", "FAIL_VENDOR_IDENTITY_REVIEW", "ATLASC1", "Existing-name vendor with wrong address should fail closed instead of silently reusing or creating a duplicate.", atlas_name, "8801 Transit Park Blvd, Columbus, OH 43085", atlas_phone, atlas_email, "PO26385048", "2026-03-20", "15.77", [line(1, "FC-ATL-2851", "Fail Closed Atlas Item", "4", "EA", "27.40"), line(2, "FC-ATL-2852", "Fail Closed Atlas Item 2", "5", "EA", "19.85")]),
        invoice(49, "create_reuse_uom_fallback", "SUCCESS", "", "New vendor/items should be created; unsupported OCR UOM values should fall back to persisted EA.", "Harbor Span Robotics", "3187 Bridgeport Drive, Sandusky, OH 44870", "419-555-0284", "ap@harborspan.example", "PO26385049", "2026-03-21", "24.68", [line(1, "HSR-ACT-28A", "Harbor Span Actuator", "4", "PCS", "118.20"), line(2, "HSR-SNS-28B", "Harbor Span Sensor", "7", "PR", "31.40"), line(3, "HSR-MNT-28C", "Harbor Span Mount", "5", "PCS", "16.85")]),
        invoice(50, "create_reuse_uom_fallback", "SUCCESS", "", "Second invoice should reuse the same vendor/items and still resolve PO-line UM to persisted EA.", "Harbor Span Robotics", "3187 Bridgeport Drive, Sandusky, OH 44870", "4195550284", "AP@HARBORSPAN.EXAMPLE", "PO26385050", "2026-03-22", "18.94", [line(1, "HSR-ACT-28A", "Harbor Span Actuator", "3", "PCS", "118.20"), line(2, "HSR-SNS-28B", "Harbor Span Sensor", "6", "PR", "31.40"), line(3, "HSR-MNT-28C", "Harbor Span Mount", "4", "PCS", "16.85")]),
    ])

    if len(specs) != 50:
        raise ValueError(f"Expected 50 invoices, built {len(specs)}")

    return specs


def build_metadata(specs: list[InvoiceSpec], input_dir: Path) -> dict:
    scenario_counts: dict[str, int] = {}
    for spec in specs:
        scenario_counts[spec.scenario_group] = scenario_counts.get(spec.scenario_group, 0) + 1

    return {
        "batch_name": "V2 Mass Test Batch 50",
        "generated_at": "2026-03-08",
        "input_folder": str(input_dir),
        "document_count": len(specs),
        "expected_success_count": sum(1 for spec in specs if spec.expected_status == "SUCCESS"),
        "expected_failure_count": sum(1 for spec in specs if spec.expected_status != "SUCCESS"),
        "scenario_counts": scenario_counts,
        "notes": [
            "Existing-vendor scenarios use live tenant identities validated on 2026-03-08.",
            "Six invoices are intentional policy-failure cases: duplicate PO or fail-closed vendor identity mismatch.",
            "North Ridge and Harbor Span scenarios exercise item UOM fallback and persisted UM reuse.",
        ],
        "documents": [asdict(spec) for spec in specs],
    }


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    input_dir = output_root / "Input"
    input_dir.mkdir(parents=True, exist_ok=True)

    specs = build_specs()
    for spec in specs:
        draw_invoice(
            Namespace(
                output=str(input_dir / spec.filename),
                vendor_name=spec.vendor_name,
                vendor_address=spec.vendor_address,
                vendor_phone=spec.vendor_phone,
                vendor_email=spec.vendor_email,
                po_number=spec.po_number,
                order_date=spec.order_date,
                sales_tax=spec.sales_tax,
                line=spec.lines,
            )
        )

    manifest = build_metadata(specs, input_dir)
    manifest_path = output_root / "mass_test_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    readme_path = output_root / "README.txt"
    readme_path.write_text(
        "\n".join(
            [
                "DemoInvoiceLoaderV2 Mass Test Batch",
                f"Input folder: {input_dir}",
                f"Manifest: {manifest_path}",
                f"Documents: {len(specs)}",
                f"Expected successes: {manifest['expected_success_count']}",
                f"Expected intentional failures: {manifest['expected_failure_count']}",
                "",
                "Primary focus areas:",
                "- Existing vendor reuse by name+address base threshold",
                "- Phone/email normalization as tie-break support",
                "- Fail-closed behavior for wrong-address same-name vendors",
                "- Duplicate PO detection",
                "- Item UOM fallback and persisted UM reuse",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Generated {len(specs)} invoices in: {input_dir}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
