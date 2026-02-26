"""
Generate test PDF invoice for DemoInvoiceLoader RPA workflow.
Batch Invoice 08: Color Accent Lines Style - Riverside Steel & Metal
"""

from fpdf import FPDF
from datetime import datetime
import os


class AccentLinesInvoicePDF(FPDF):
    def header(self):
        # Purple/burgundy accent lines
        self.set_draw_color(128, 0, 64)
        self.set_line_width(3)
        self.line(10, 8, 200, 8)
        self.set_line_width(1)
        self.line(10, 13, 200, 13)

        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(128, 0, 64)
        self.set_y(18)
        self.cell(0, 10, 'INVOICE', align='C', ln=True)

        self.set_line_width(1)
        self.line(10, 32, 200, 32)
        self.set_line_width(3)
        self.line(10, 37, 200, 37)

        self.ln(18)

    def footer(self):
        self.set_draw_color(128, 0, 64)
        self.set_line_width(1)
        self.line(10, 282, 200, 282)
        self.set_y(-12)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(128, 0, 64)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def generate_invoice(output_path):
    pdf = AccentLinesInvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Order metadata with accent color
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(128, 0, 64)
    pdf.cell(50, 6, 'Order Date:', align='R')
    pdf.set_text_color(60, 60, 60)
    pdf.cell(50, 6, f' {datetime.now().strftime("%Y-%m-%d")}')
    pdf.set_text_color(128, 0, 64)
    pdf.cell(50, 6, 'Purchase Order Number:', align='R')
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 6, ' PO-2026-1008', ln=True)
    pdf.ln(5)

    # Accent line separator
    pdf.set_draw_color(128, 0, 64)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Vendor Section
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(128, 0, 64)
    pdf.cell(0, 7, 'VENDOR', ln=True)

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    vendor_info = [
        'Vendor Name: Riverside Steel & Metal Inc.',
        'Vendor Address: 6700 River Industrial Parkway, St. Louis, MO 63118',
        'Vendor Phone Number: (314) 555-8800',
        'Vendor Email Address: sales@riversidesteel.com'
    ]
    for line in vendor_info:
        pdf.cell(0, 5, line, ln=True)

    pdf.ln(3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Ship To Section
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(128, 0, 64)
    pdf.cell(0, 7, 'SHIP TO', ln=True)

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, 'Infor Demo Company - Fabrication Shop', ln=True)
    pdf.cell(0, 5, '1000 Factory Road, Chicago, IL 60601', ln=True)

    pdf.ln(3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    # Line Items Table Header - Accent colored
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(128, 0, 64)
    pdf.cell(20, 8, 'Line Number', border='B', align='C')
    pdf.cell(35, 8, 'Item Code', border='B', align='C')
    pdf.cell(75, 8, 'Description', border='B', align='C')
    pdf.cell(30, 8, 'Quantity Shipped', border='B', align='C')
    pdf.cell(20, 8, 'UOM', border='B', align='C')
    pdf.ln()

    # Line Items Data - Steel/Metal stock
    line_items = [
        ('1', 'STEEL-FLAT-1X4', 'Flat Bar Steel 1" x 4" x 20ft', '10', 'EA'),
        ('2', 'STEEL-ANGLE-2X2', 'Angle Iron 2" x 2" x 20ft', '15', 'EA'),
        ('3', 'STEEL-TUBE-SQ-2', 'Square Tube 2" x 2" x 20ft', '8', 'EA'),
        ('4', 'ALUM-SHEET-4X8', 'Aluminum Sheet 4ft x 8ft 0.125"', '6', 'EA'),
        ('5', 'STEEL-PLATE-12', 'Steel Plate 12" x 24" x 0.5"', '4', 'EA'),
        ('6', 'STEEL-ROUND-2IN', 'Round Bar Steel 2" Diameter x 6ft', '12', 'EA'),
    ]

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.set_draw_color(200, 180, 190)
    for item in line_items:
        pdf.cell(20, 7, item[0], border='B', align='C')
        pdf.cell(35, 7, item[1], border='B', align='C')
        pdf.cell(75, 7, item[2], border='B')
        pdf.cell(30, 7, item[3], border='B', align='C')
        pdf.cell(20, 7, item[4], border='B', align='C')
        pdf.ln()

    pdf.ln(10)

    # Accent line
    pdf.set_draw_color(128, 0, 64)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Terms Section
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(128, 0, 64)
    pdf.cell(0, 6, 'TERMS & CONDITIONS', ln=True)

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, 'Payment Terms: Net 30', ln=True)
    pdf.cell(0, 5, 'Shipping Method: Flatbed Truck', ln=True)
    pdf.cell(0, 5, 'Expected Delivery: 2026-02-22', ln=True)

    pdf.ln(3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(10)

    # Notes
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(128, 0, 64)
    pdf.cell(0, 6, 'Please confirm receipt and expected ship date.', ln=True, align='C')

    # Save
    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path


if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "Invoice_RiversideSteel_PO-2026-1008.pdf")
    generate_invoice(output_file)
    print(f"\nReady for RPA testing!")
