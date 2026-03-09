#!/usr/bin/env python3
"""Generate a clear OCR-friendly invoice PDF for DemoInvoiceLoaderV2 testing."""

from __future__ import annotations

import argparse
from decimal import Decimal
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def money(value: Decimal) -> str:
    return f"{value:.2f}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Output PDF path")
    parser.add_argument("--vendor-name", required=True)
    parser.add_argument("--vendor-address", required=True)
    parser.add_argument("--vendor-phone", required=True)
    parser.add_argument("--vendor-email", required=True)
    parser.add_argument("--po-number", required=True)
    parser.add_argument("--order-date", required=True)
    parser.add_argument("--sales-tax", required=True, help="Header tax amount")
    parser.add_argument(
        "--line",
        action="append",
        required=True,
        help="Line format: line_no|item_code|description|qty|uom|unit_price",
    )
    return parser.parse_args()


def parse_lines(raw_lines: list[str]) -> tuple[list[dict[str, str]], Decimal]:
    lines: list[dict[str, str]] = []
    subtotal = Decimal("0.00")

    for raw in raw_lines:
        parts = raw.split("|")
        if len(parts) != 6:
            raise ValueError(f"Invalid --line value: {raw}")

        line_no, item_code, description, qty, uom, unit_price = parts
        qty_decimal = Decimal(qty)
        unit_price_decimal = Decimal(unit_price)
        line_total = qty_decimal * unit_price_decimal
        subtotal += line_total

        lines.append(
            {
                "line_no": line_no,
                "item_code": item_code,
                "description": description,
                "qty": qty,
                "uom": uom,
                "unit_price": money(unit_price_decimal),
                "line_total": money(line_total),
            }
        )

    return lines, subtotal


def draw_invoice(args: argparse.Namespace) -> None:
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sales_tax = Decimal(args.sales_tax)
    lines, subtotal = parse_lines(args.line)
    total = subtotal + sales_tax

    pdf = canvas.Canvas(str(output_path), pagesize=letter)
    width, height = letter

    left = 0.7 * inch
    right = width - 0.7 * inch
    y = height - 0.75 * inch

    pdf.setTitle(f"Invoice {args.po_number}")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(left, y, "AP Invoice Test Document")
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(right, y + 2, "CSI OCR Validation")
    y -= 0.35 * inch

    pdf.setLineWidth(1)
    pdf.line(left, y, right, y)
    y -= 0.3 * inch

    fields = [
        ("Vendor Name", args.vendor_name),
        ("Vendor Address", args.vendor_address),
        ("Vendor Phone Number", args.vendor_phone),
        ("Vendor Email Address", args.vendor_email),
        ("Purchase Order Number", args.po_number),
        ("Order Date", args.order_date),
        ("VAT/Tax Amount", money(sales_tax)),
        ("Sub Total", money(subtotal)),
        ("Total Amount", money(total)),
    ]

    pdf.setFont("Helvetica", 11)
    for label, value in fields:
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(left, y, f"{label}:")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(left + 1.75 * inch, y, value)
        y -= 0.25 * inch

    y -= 0.15 * inch
    table_top = y
    pdf.setFont("Helvetica-Bold", 10)
    headers = [
        ("Line Number", left),
        ("Item Code", left + 0.8 * inch),
        ("Description", left + 2.2 * inch),
        ("Quantity Shipped", left + 4.55 * inch),
        ("UOM", left + 5.65 * inch),
        ("Unit Price", left + 6.25 * inch),
    ]
    for header, x in headers:
        pdf.drawString(x, y, header)

    y -= 0.12 * inch
    pdf.line(left, y, right, y)
    y -= 0.2 * inch

    pdf.setFont("Helvetica", 10)
    for line in lines:
        pdf.drawString(left, y, line["line_no"])
        pdf.drawString(left + 0.8 * inch, y, line["item_code"])
        pdf.drawString(left + 2.2 * inch, y, line["description"])
        pdf.drawString(left + 4.75 * inch, y, line["qty"])
        pdf.drawString(left + 5.7 * inch, y, line["uom"])
        pdf.drawRightString(right, y, line["unit_price"])
        y -= 0.22 * inch

    y -= 0.08 * inch
    pdf.line(left, y, right, y)
    y -= 0.3 * inch

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawRightString(right - 1.2 * inch, y, "Sub Total:")
    pdf.setFont("Helvetica", 11)
    pdf.drawRightString(right, y, money(subtotal))
    y -= 0.22 * inch

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawRightString(right - 1.2 * inch, y, "VAT/Tax Amount:")
    pdf.setFont("Helvetica", 11)
    pdf.drawRightString(right, y, money(sales_tax))
    y -= 0.22 * inch

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawRightString(right - 1.2 * inch, y, "Total Amount:")
    pdf.drawRightString(right, y, money(total))

    footer_y = table_top - 2.9 * inch
    if y < footer_y:
        y = footer_y

    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(left, 0.7 * inch, "Generated for live OCR validation in DemoInvoiceLoaderV2.")
    pdf.save()


def main() -> int:
    args = parse_args()
    draw_invoice(args)
    print(f"Generated invoice PDF: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
