"""
Generate test PDF invoice for DemoInvoiceLoader RPA workflow.
Batch Invoice 07: Invoice with Logo Area Style - Pacific Bearing & Drive
"""

from fpdf import FPDF
from datetime import datetime
import os


class LogoAreaInvoicePDF(FPDF):
    def header(self):
        # Logo placeholder area with teal accent
        self.set_fill_color(0, 128, 128)
        self.rect(10, 10, 40, 20, 'F')
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(255, 255, 255)
        self.set_xy(12, 17)
        self.cell(36, 6, '[COMPANY LOGO]', align='C')

        # Title next to logo area
        self.set_xy(60, 10)
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(0, 128, 128)
        self.cell(0, 12, 'INVOICE', ln=True)

        # Teal accent line under header
        self.set_draw_color(0, 128, 128)
        self.set_line_width(2)
        self.line(10, 35, 200, 35)
        self.ln(25)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(0, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def generate_invoice(output_path):
    pdf = LogoAreaInvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Order metadata - letterhead style
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 128, 128)
    pdf.cell(40, 6, 'Order Date:')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(60, 6, datetime.now().strftime("%Y-%m-%d"))

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 128, 128)
    pdf.cell(50, 6, 'Purchase Order Number:')
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 6, 'PO-2026-1007', ln=True)
    pdf.ln(8)

    # Two-column layout for vendor and ship-to
    col_width = 95
    start_y = pdf.get_y()

    # Vendor column
    pdf.set_fill_color(240, 250, 250)
    pdf.set_draw_color(0, 128, 128)
    pdf.rect(10, start_y, col_width - 5, 40, 'DF')

    pdf.set_xy(15, start_y + 3)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 128, 128)
    pdf.cell(0, 6, 'VENDOR', ln=True)

    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, 'Vendor Name: Pacific Bearing & Drive Co.', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, 'Vendor Address: 3200 Harbor Boulevard,', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, '                Long Beach, CA 90802', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, 'Vendor Phone Number: (562) 555-4500', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, 'Vendor Email Address: orders@pacificbearing.com', ln=True)

    # Ship-to column
    pdf.rect(105, start_y, col_width - 5, 40, 'DF')

    pdf.set_xy(110, start_y + 3)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 128, 128)
    pdf.cell(0, 6, 'SHIP TO', ln=True)

    pdf.set_x(110)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, 'Infor Demo Company', ln=True)
    pdf.set_x(110)
    pdf.cell(0, 5, 'Power Transmission Dept.', ln=True)
    pdf.set_x(110)
    pdf.cell(0, 5, '1000 Factory Road', ln=True)
    pdf.set_x(110)
    pdf.cell(0, 5, 'Chicago, IL 60601', ln=True)

    pdf.set_y(start_y + 45)

    # Line Items Table Header - Teal theme
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(0, 128, 128)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(20, 8, 'Line Number', border=1, fill=True, align='C')
    pdf.cell(35, 8, 'Item Code', border=1, fill=True, align='C')
    pdf.cell(75, 8, 'Description', border=1, fill=True, align='C')
    pdf.cell(30, 8, 'Quantity Shipped', border=1, fill=True, align='C')
    pdf.cell(20, 8, 'UOM', border=1, fill=True, align='C')
    pdf.ln()

    # Line Items Data - Bearings/Power transmission
    line_items = [
        ('1', 'BRG-6205-2RS', 'Deep Groove Ball Bearing 6205-2RS', '24', 'EA'),
        ('2', 'BRG-TAPR-32008', 'Tapered Roller Bearing 32008X', '12', 'EA'),
        ('3', 'BELT-V-A68', 'V-Belt A68 Industrial Grade', '10', 'EA'),
        ('4', 'CHAIN-ROLL-60', 'Roller Chain #60 10ft Length', '5', 'EA'),
    ]

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(0, 128, 128)
    for i, item in enumerate(line_items):
        if i % 2 == 0:
            pdf.set_fill_color(245, 252, 252)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(20, 7, item[0], border=1, align='C', fill=True)
        pdf.cell(35, 7, item[1], border=1, align='C', fill=True)
        pdf.cell(75, 7, item[2], border=1, fill=True)
        pdf.cell(30, 7, item[3], border=1, align='C', fill=True)
        pdf.cell(20, 7, item[4], border=1, align='C', fill=True)
        pdf.ln()

    pdf.ln(12)

    # Terms section with teal accent
    pdf.set_draw_color(0, 128, 128)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 128, 128)
    pdf.cell(0, 6, 'Terms & Conditions', ln=True)

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, 'Payment Terms: Net 30  |  Shipping: UPS Ground  |  Expected Delivery: 2026-02-14', ln=True)

    pdf.ln(3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(12)

    # Notes
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, 'Please confirm receipt and expected ship date.', ln=True, align='C')
    pdf.cell(0, 6, 'Contact: purchasing@example.com', ln=True, align='C')

    # Save
    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path


if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "Invoice_PacificBearing_PO-2026-1007.pdf")
    generate_invoice(output_file)
    print(f"\nReady for RPA testing!")
