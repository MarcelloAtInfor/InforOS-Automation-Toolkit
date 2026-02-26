"""
Generate test PDF invoice for DemoInvoiceLoader RPA workflow.
Batch Invoice 01: Minimal Clean Style - Delta Automation Systems
"""

from fpdf import FPDF
from datetime import datetime
import os


class MinimalInvoicePDF(FPDF):
    def header(self):
        # Minimal clean header with thin line
        self.set_font('Helvetica', '', 24)
        self.set_text_color(80, 80, 80)
        self.cell(0, 12, 'INVOICE', align='C', ln=True)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.3)
        self.line(20, 22, 190, 22)
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def generate_invoice(output_path):
    pdf = MinimalInvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Order metadata - minimal styling
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f'Order Date: {datetime.now().strftime("%Y-%m-%d")}', ln=True)
    pdf.cell(0, 6, 'Purchase Order Number: PO-2026-1001', ln=True)
    pdf.ln(12)

    # Vendor Information
    pdf.set_text_color(60, 60, 60)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 7, 'VENDOR', ln=True)
    pdf.set_draw_color(220, 220, 220)
    pdf.line(10, pdf.get_y(), 60, pdf.get_y())
    pdf.ln(3)

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    vendor_info = [
        'Vendor Name: Delta Automation Systems LLC',
        'Vendor Address: 4500 Industrial Parkway, Detroit, MI 48201',
        'Vendor Phone Number: (313) 555-2100',
        'Vendor Email Address: sales@deltaautomation.com'
    ]
    for line in vendor_info:
        pdf.cell(0, 6, line, ln=True)

    pdf.ln(12)

    # Ship To section
    pdf.set_text_color(60, 60, 60)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 7, 'SHIP TO', ln=True)
    pdf.line(10, pdf.get_y(), 60, pdf.get_y())
    pdf.ln(3)

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, 'Infor Demo Company', ln=True)
    pdf.cell(0, 6, 'Assembly Plant - East Wing', ln=True)
    pdf.cell(0, 6, '1000 Factory Road, Chicago, IL 60601', ln=True)

    pdf.ln(12)

    # Line Items Table Header - minimal with thin borders
    pdf.set_font('Helvetica', '', 9)
    pdf.set_fill_color(250, 250, 250)
    pdf.set_text_color(80, 80, 80)
    pdf.set_draw_color(200, 200, 200)
    pdf.cell(20, 7, 'Line Number', border='B', fill=True, align='C')
    pdf.cell(35, 7, 'Item Code', border='B', fill=True, align='C')
    pdf.cell(75, 7, 'Description', border='B', fill=True, align='C')
    pdf.cell(30, 7, 'Quantity Shipped', border='B', fill=True, align='C')
    pdf.cell(20, 7, 'UOM', border='B', fill=True, align='C')
    pdf.ln()

    # Line Items Data - PLCs/Sensors
    line_items = [
        ('1', 'PLC-MICRO-800', 'Micro800 PLC Controller Unit', '5', 'EA'),
        ('2', 'SENS-PROX-18MM', 'Proximity Sensor 18mm Inductive', '20', 'EA'),
        ('3', 'SENS-PHOTO-LR', 'Photoelectric Sensor Long Range', '12', 'EA'),
        ('4', 'HMI-TOUCH-7IN', '7-inch Touchscreen HMI Panel', '3', 'EA'),
    ]

    pdf.set_font('Helvetica', '', 9)
    for item in line_items:
        pdf.set_text_color(60, 60, 60)
        pdf.cell(20, 7, item[0], border='B', align='C')
        pdf.cell(35, 7, item[1], border='B', align='C')
        pdf.cell(75, 7, item[2], border='B')
        pdf.cell(30, 7, item[3], border='B', align='C')
        pdf.cell(20, 7, item[4], border='B', align='C')
        pdf.ln()

    pdf.ln(15)

    # Terms - minimal
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 5, 'Payment Terms: Net 30  |  Shipping: FedEx Ground  |  Expected: 2026-02-15', ln=True, align='C')

    pdf.ln(10)

    # Notes
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, 'Please confirm receipt and expected ship date.', ln=True, align='C')

    # Save
    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path


if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "Invoice_DeltaAutomation_PO-2026-1001.pdf")
    generate_invoice(output_file)
    print(f"\nReady for RPA testing!")
