"""
Generate test PDF invoice for DemoInvoiceLoader RPA workflow.
Batch Invoice 02: Bold Headers Style - Sterling Welding Supply
"""

from fpdf import FPDF
from datetime import datetime
import os


class BoldHeaderInvoicePDF(FPDF):
    def header(self):
        # Bold dark header band
        self.set_fill_color(30, 30, 30)
        self.rect(0, 0, 210, 25, 'F')
        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(255, 255, 255)
        self.set_y(7)
        self.cell(0, 10, 'INVOICE', align='C', ln=True)
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def generate_invoice(output_path):
    pdf = BoldHeaderInvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Order metadata
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(40, 6, 'Order Date:', align='R')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, f' {datetime.now().strftime("%Y-%m-%d")}', ln=True)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(40, 6, 'Purchase Order Number:', align='R')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, ' PO-2026-1002', ln=True)
    pdf.ln(8)

    # Vendor Section - Bold header bar
    pdf.set_fill_color(50, 50, 50)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, '  VENDOR INFORMATION', fill=True, ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 10)
    pdf.ln(2)
    vendor_info = [
        'Vendor Name: Sterling Welding Supply Inc.',
        'Vendor Address: 7820 Fabrication Lane, Pittsburgh, PA 15201',
        'Vendor Phone Number: (412) 555-9876',
        'Vendor Email Address: orders@sterlingwelding.com'
    ]
    for line in vendor_info:
        pdf.cell(0, 6, line, ln=True)

    pdf.ln(8)

    # Ship To Section - Bold header bar
    pdf.set_fill_color(50, 50, 50)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, '  SHIP TO', fill=True, ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 10)
    pdf.ln(2)
    pdf.cell(0, 6, 'Infor Demo Company', ln=True)
    pdf.cell(0, 6, 'Welding Shop - Building C', ln=True)
    pdf.cell(0, 6, '1000 Factory Road, Chicago, IL 60601', ln=True)

    pdf.ln(8)

    # Line Items Header - Bold header bar
    pdf.set_fill_color(50, 50, 50)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, '  ORDER ITEMS', fill=True, ln=True)
    pdf.ln(2)

    # Table Header
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(200, 200, 200)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(20, 7, 'Line Number', border=1, fill=True, align='C')
    pdf.cell(32, 7, 'Item Code', border=1, fill=True, align='C')
    pdf.cell(78, 7, 'Description', border=1, fill=True, align='C')
    pdf.cell(28, 7, 'Quantity Shipped', border=1, fill=True, align='C')
    pdf.cell(22, 7, 'UOM', border=1, fill=True, align='C')
    pdf.ln()

    # Line Items Data - Welding equipment
    line_items = [
        ('1', 'WELD-MIG-250', 'MIG Welder 250 Amp Industrial', '2', 'EA'),
        ('2', 'WIRE-ER70S-035', 'MIG Wire ER70S-6 .035" 44lb Spool', '10', 'EA'),
        ('3', 'GAS-C25-CYL', 'C25 Shielding Gas Cylinder 80CF', '4', 'EA'),
        ('4', 'HELM-AUTO-DRK', 'Auto-Darkening Welding Helmet', '6', 'EA'),
        ('5', 'GLOVE-WELD-LG', 'Welding Gloves Leather Large', '12', 'PR'),
        ('6', 'TIP-CONTACT-035', 'Contact Tips .035" (50pk)', '5', 'PK'),
    ]

    pdf.set_font('Helvetica', '', 9)
    for i, item in enumerate(line_items):
        if i % 2 == 0:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(20, 7, item[0], border=1, align='C', fill=True)
        pdf.cell(32, 7, item[1], border=1, align='C', fill=True)
        pdf.cell(78, 7, item[2], border=1, fill=True)
        pdf.cell(28, 7, item[3], border=1, align='C', fill=True)
        pdf.cell(22, 7, item[4], border=1, align='C', fill=True)
        pdf.ln()

    pdf.ln(12)

    # Terms Section - Bold header
    pdf.set_fill_color(50, 50, 50)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, '  TERMS & CONDITIONS', fill=True, ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 10)
    pdf.ln(2)
    pdf.cell(0, 6, 'Payment Terms: Net 45', ln=True)
    pdf.cell(0, 6, 'Shipping Method: Freight', ln=True)
    pdf.cell(0, 6, 'Expected Delivery: 2026-02-20', ln=True)

    pdf.ln(10)

    # Notes
    pdf.set_font('Helvetica', 'I', 9)
    pdf.cell(0, 6, 'Please confirm receipt and expected ship date.', ln=True, align='C')

    # Save
    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path


if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "Invoice_SterlingWelding_PO-2026-1002.pdf")
    generate_invoice(output_file)
    print(f"\nReady for RPA testing!")
