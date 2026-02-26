"""
Generate test PDF invoice for DemoInvoiceLoader RPA workflow.
Batch Invoice 04: Split Panel Style - Great Lakes Chemical Corp
"""

from fpdf import FPDF
from datetime import datetime
import os


class SplitPanelInvoicePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(40, 80, 120)
        self.cell(0, 15, 'INVOICE', align='C', ln=True)
        self.set_draw_color(40, 80, 120)
        self.set_line_width(1)
        self.line(10, 20, 200, 20)
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def generate_invoice(output_path):
    pdf = SplitPanelInvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Split panel layout - Left: Vendor, Right: Order Details
    panel_y = pdf.get_y()

    # Left Panel - Vendor Info with background
    pdf.set_fill_color(235, 242, 250)
    pdf.rect(10, panel_y, 92, 50, 'F')

    pdf.set_xy(15, panel_y + 3)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(40, 80, 120)
    pdf.cell(82, 6, 'VENDOR', ln=True)

    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(82, 5, 'Vendor Name: Great Lakes Chemical Corp', ln=True)
    pdf.set_x(15)
    pdf.cell(82, 5, 'Vendor Address: 5500 Lakeshore Drive,', ln=True)
    pdf.set_x(15)
    pdf.cell(82, 5, '                Gary, IN 46402', ln=True)
    pdf.set_x(15)
    pdf.cell(82, 5, 'Vendor Phone Number: (219) 555-3300', ln=True)
    pdf.set_x(15)
    pdf.cell(82, 5, 'Vendor Email Address: sales@greatlakeschem.com', ln=True)

    # Right Panel - Order Details
    pdf.set_xy(108, panel_y + 3)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(40, 80, 120)
    pdf.cell(82, 6, 'ORDER DETAILS', ln=True)

    pdf.set_x(108)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(82, 5, f'Order Date: {datetime.now().strftime("%Y-%m-%d")}', ln=True)
    pdf.set_x(108)
    pdf.cell(82, 5, 'Purchase Order Number: PO-2026-1004', ln=True)
    pdf.set_x(108)
    pdf.cell(82, 5, 'Payment Terms: Net 30', ln=True)
    pdf.set_x(108)
    pdf.cell(82, 5, 'Shipping: Hazmat Carrier', ln=True)
    pdf.set_x(108)
    pdf.cell(82, 5, 'Expected: 2026-02-18', ln=True)

    pdf.set_y(panel_y + 55)

    # Ship To section - centered
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(10, pdf.get_y(), 190, 20, 'F')

    pdf.set_xy(15, pdf.get_y() + 2)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(40, 80, 120)
    pdf.cell(40, 6, 'SHIP TO:')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, 'Infor Demo Company - Chemical Storage, 1000 Factory Road, Chicago, IL 60601', ln=True)

    pdf.ln(15)

    # Line Items Table Header
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(40, 80, 120)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(20, 8, 'Line Number', border=1, fill=True, align='C')
    pdf.cell(35, 8, 'Item Code', border=1, fill=True, align='C')
    pdf.cell(75, 8, 'Description', border=1, fill=True, align='C')
    pdf.cell(30, 8, 'Quantity Shipped', border=1, fill=True, align='C')
    pdf.cell(20, 8, 'UOM', border=1, fill=True, align='C')
    pdf.ln()

    # Line Items Data - Chemicals/Lubricants
    line_items = [
        ('1', 'SOLV-ACET-5G', 'Acetone Industrial Grade 5 Gallon', '8', 'EA'),
        ('2', 'LUBR-HYD-55G', 'Hydraulic Oil ISO 46 55 Gallon', '2', 'DR'),
        ('3', 'CLEAN-DEGR-1G', 'Degreaser Concentrate 1 Gallon', '12', 'EA'),
    ]

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(40, 80, 120)
    for i, item in enumerate(line_items):
        if i % 2 == 0:
            pdf.set_fill_color(245, 248, 252)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(20, 7, item[0], border=1, align='C', fill=True)
        pdf.cell(35, 7, item[1], border=1, align='C', fill=True)
        pdf.cell(75, 7, item[2], border=1, fill=True)
        pdf.cell(30, 7, item[3], border=1, align='C', fill=True)
        pdf.cell(20, 7, item[4], border=1, align='C', fill=True)
        pdf.ln()

    pdf.ln(15)

    # Hazmat Notice - split panel style
    pdf.set_fill_color(255, 245, 230)
    pdf.set_draw_color(200, 150, 50)
    pdf.rect(10, pdf.get_y(), 190, 20, 'DF')

    pdf.set_xy(15, pdf.get_y() + 3)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(180, 120, 30)
    pdf.cell(0, 6, 'HAZMAT NOTICE', ln=True)

    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 80, 40)
    pdf.cell(0, 5, 'Materials require proper handling and storage. SDS sheets included with shipment.', ln=True)

    pdf.ln(15)

    # Notes
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, 'Please confirm receipt and expected ship date.', ln=True, align='C')

    # Save
    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path


if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "Invoice_GreatLakesChem_PO-2026-1004.pdf")
    generate_invoice(output_file)
    print(f"\nReady for RPA testing!")
