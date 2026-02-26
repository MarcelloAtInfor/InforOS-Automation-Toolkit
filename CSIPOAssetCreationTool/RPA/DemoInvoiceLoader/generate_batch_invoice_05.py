"""
Generate test PDF invoice for DemoInvoiceLoader RPA workflow.
Batch Invoice 05: Classic Serif Style - Heritage Machine Works
"""

from fpdf import FPDF
from datetime import datetime
import os


class ClassicSerifInvoicePDF(FPDF):
    def header(self):
        # Classic formal header with Times font style
        self.set_font('Times', 'B', 24)
        self.set_text_color(0, 0, 0)
        self.cell(0, 12, 'INVOICE', align='C', ln=True)
        self.set_font('Times', 'I', 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, 6, 'Official Document', align='C', ln=True)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.5)
        self.line(30, 28, 180, 28)
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def generate_invoice(output_path):
    pdf = ClassicSerifInvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Order metadata - formal style
    pdf.set_font('Times', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(50, 6, 'Date of Order:', align='R')
    pdf.cell(0, 6, f'  {datetime.now().strftime("%B %d, %Y")}', ln=True)
    pdf.cell(50, 6, 'Purchase Order Number:', align='R')
    pdf.cell(0, 6, '  PO-2026-1005', ln=True)
    pdf.ln(8)

    # Vendor Section - Classic indented style
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 8, 'VENDOR:', ln=True)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 50, pdf.get_y())

    pdf.set_font('Times', '', 11)
    pdf.ln(2)
    vendor_info = [
        'Vendor Name: Heritage Machine Works Ltd.',
        'Vendor Address: 890 Industrial Heritage Lane, Cincinnati, OH 45202',
        'Vendor Phone Number: (513) 555-1890',
        'Vendor Email Address: sales@heritagemachine.com'
    ]
    for line in vendor_info:
        pdf.cell(10, 6, '', ln=False)  # Indent
        pdf.cell(0, 6, line, ln=True)

    pdf.ln(8)

    # Ship To Section
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 8, 'DELIVER TO:', ln=True)
    pdf.line(10, pdf.get_y(), 50, pdf.get_y())

    pdf.set_font('Times', '', 11)
    pdf.ln(2)
    pdf.cell(10, 6, '', ln=False)
    pdf.cell(0, 6, 'Infor Demo Company', ln=True)
    pdf.cell(10, 6, '', ln=False)
    pdf.cell(0, 6, 'Machine Shop - Precision Division', ln=True)
    pdf.cell(10, 6, '', ln=False)
    pdf.cell(0, 6, '1000 Factory Road, Chicago, IL 60601', ln=True)

    pdf.ln(10)

    # Line Items Table Header - Classic style
    pdf.set_font('Times', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(18, 8, 'Line Number', border=1, fill=True, align='C')
    pdf.cell(32, 8, 'Item Code', border=1, fill=True, align='C')
    pdf.cell(80, 8, 'Description', border=1, fill=True, align='C')
    pdf.cell(28, 8, 'Quantity Shipped', border=1, fill=True, align='C')
    pdf.cell(22, 8, 'UOM', border=1, fill=True, align='C')
    pdf.ln()

    # Line Items Data - Machine parts
    line_items = [
        ('1', 'SHAFT-PREC-25', 'Precision Ground Shaft 25mm x 500mm', '8', 'EA'),
        ('2', 'GEAR-SPUR-M2', 'Spur Gear Module 2 50 Teeth', '12', 'EA'),
        ('3', 'BUSHING-BRZ-32', 'Bronze Bushing 32mm ID', '20', 'EA'),
        ('4', 'COUPLING-FLX', 'Flexible Coupling 25mm Bore', '6', 'EA'),
        ('5', 'SPINDLE-HSS', 'High Speed Spindle Assembly', '2', 'EA'),
        ('6', 'KEY-WOOD-8X7', 'Woodruff Key 8x7mm', '50', 'EA'),
        ('7', 'SEAL-OIL-50X70', 'Oil Seal 50x70x10mm', '15', 'EA'),
    ]

    pdf.set_font('Times', '', 10)
    for item in line_items:
        pdf.cell(18, 7, item[0], border=1, align='C')
        pdf.cell(32, 7, item[1], border=1, align='C')
        pdf.cell(80, 7, item[2], border=1)
        pdf.cell(28, 7, item[3], border=1, align='C')
        pdf.cell(22, 7, item[4], border=1, align='C')
        pdf.ln()

    pdf.ln(12)

    # Terms Section - Formal style
    pdf.set_font('Times', 'B', 11)
    pdf.cell(0, 7, 'TERMS AND CONDITIONS:', ln=True)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 80, pdf.get_y())

    pdf.set_font('Times', '', 10)
    pdf.ln(2)
    pdf.cell(10, 6, '', ln=False)
    pdf.cell(0, 6, 'Payment Terms: Net 45 Days', ln=True)
    pdf.cell(10, 6, '', ln=False)
    pdf.cell(0, 6, 'Shipping Method: Common Carrier', ln=True)
    pdf.cell(10, 6, '', ln=False)
    pdf.cell(0, 6, 'Expected Delivery Date: February 25, 2026', ln=True)

    pdf.ln(15)

    # Formal closing
    pdf.set_font('Times', 'I', 10)
    pdf.cell(0, 6, 'This purchase order is subject to standard terms and conditions.', ln=True, align='C')
    pdf.cell(0, 6, 'Please acknowledge receipt within 48 hours.', ln=True, align='C')

    # Save
    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path


if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "Invoice_HeritageMachine_PO-2026-1005.pdf")
    generate_invoice(output_file)
    print(f"\nReady for RPA testing!")
