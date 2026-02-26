"""
Generate test PDF invoice for DemoInvoiceLoader RPA workflow.
Batch Invoice 03: Gradient Banner Style (simulated) - Apex Safety Equipment Co.
"""

from fpdf import FPDF
from datetime import datetime
import os


class GradientBannerInvoicePDF(FPDF):
    def header(self):
        # Simulated gradient banner with orange/red tones
        self.set_fill_color(220, 80, 40)
        self.rect(0, 0, 210, 30, 'F')
        self.set_fill_color(200, 60, 30)
        self.rect(0, 5, 210, 20, 'F')
        self.set_fill_color(180, 50, 25)
        self.rect(0, 10, 210, 15, 'F')

        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(255, 255, 255)
        self.set_y(8)
        self.cell(0, 12, 'INVOICE', align='C', ln=True)
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(180, 50, 25)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def generate_invoice(output_path):
    pdf = GradientBannerInvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Order metadata with accent color
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(180, 50, 25)
    pdf.cell(0, 6, f'Order Date: {datetime.now().strftime("%Y-%m-%d")}', ln=True)
    pdf.cell(0, 6, 'Purchase Order Number: PO-2026-1003', ln=True)
    pdf.ln(8)

    # Vendor Section - Rounded box simulation
    pdf.set_fill_color(255, 245, 240)
    pdf.set_draw_color(220, 80, 40)
    pdf.set_line_width(0.5)
    pdf.rect(10, pdf.get_y(), 190, 32, 'DF')

    pdf.set_x(15)
    pdf.set_y(pdf.get_y() + 3)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(180, 50, 25)
    pdf.cell(0, 6, 'VENDOR', ln=True)

    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    vendor_info = [
        'Vendor Name: Apex Safety Equipment Co.',
        'Vendor Address: 1200 Guardian Boulevard, Cleveland, OH 44114',
        'Vendor Phone Number: (216) 555-4400',
        'Vendor Email Address: orders@apexsafety.com'
    ]
    for line in vendor_info:
        pdf.set_x(15)
        pdf.cell(0, 5, line, ln=True)

    pdf.ln(10)

    # Ship To Section - Rounded box simulation
    pdf.set_fill_color(255, 245, 240)
    pdf.rect(10, pdf.get_y(), 190, 24, 'DF')

    pdf.set_x(15)
    pdf.set_y(pdf.get_y() + 3)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(180, 50, 25)
    pdf.cell(0, 6, 'SHIP TO', ln=True)

    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, 'Infor Demo Company - Safety Department', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, '1000 Factory Road, Chicago, IL 60601', ln=True)

    pdf.ln(10)

    # Line Items Table Header - Orange theme
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(220, 80, 40)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(20, 8, 'Line Number', border=1, fill=True, align='C')
    pdf.cell(35, 8, 'Item Code', border=1, fill=True, align='C')
    pdf.cell(75, 8, 'Description', border=1, fill=True, align='C')
    pdf.cell(30, 8, 'Quantity Shipped', border=1, fill=True, align='C')
    pdf.cell(20, 8, 'UOM', border=1, fill=True, align='C')
    pdf.ln()

    # Line Items Data - Safety/PPE
    line_items = [
        ('1', 'HELM-HARD-WHT', 'Hard Hat Type II White', '50', 'EA'),
        ('2', 'GLASS-SAFE-CLR', 'Safety Glasses Clear Anti-Fog', '100', 'EA'),
        ('3', 'VEST-HIVIS-XL', 'Hi-Vis Safety Vest Class 2 XL', '30', 'EA'),
        ('4', 'GLOVE-NITR-LG', 'Nitrile Work Gloves Large', '200', 'PR'),
        ('5', 'BOOT-STEEL-11', 'Steel Toe Boots Size 11', '15', 'PR'),
    ]

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(220, 80, 40)
    for i, item in enumerate(line_items):
        if i % 2 == 0:
            pdf.set_fill_color(255, 250, 248)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(20, 7, item[0], border=1, align='C', fill=True)
        pdf.cell(35, 7, item[1], border=1, align='C', fill=True)
        pdf.cell(75, 7, item[2], border=1, fill=True)
        pdf.cell(30, 7, item[3], border=1, align='C', fill=True)
        pdf.cell(20, 7, item[4], border=1, align='C', fill=True)
        pdf.ln()

    pdf.ln(12)

    # Terms - Accent colored box
    pdf.set_fill_color(255, 245, 240)
    pdf.set_draw_color(220, 80, 40)
    pdf.rect(10, pdf.get_y(), 190, 20, 'DF')

    pdf.set_x(15)
    pdf.set_y(pdf.get_y() + 3)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(180, 50, 25)
    pdf.cell(0, 6, 'Terms & Conditions', ln=True)

    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, 'Payment: Net 30  |  Shipping: UPS Ground  |  Expected Delivery: 2026-02-12', ln=True)

    pdf.ln(15)

    # Notes
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(180, 50, 25)
    pdf.cell(0, 6, 'Safety First! Contact purchasing@example.com with questions.', ln=True, align='C')

    # Save
    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path


if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "Invoice_ApexSafety_PO-2026-1003.pdf")
    generate_invoice(output_file)
    print(f"\nReady for RPA testing!")
