"""
Generate a test PDF invoice with LETTERHEAD STYLE.
Modern clean design with boxed sections and company branding area.
"""

from fpdf import FPDF
from datetime import datetime
import os

class LetterheadInvoice(FPDF):
    def header(self):
        # Simulated letterhead area (would have logo)
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(0, 100, 80)
        self.set_line_width(1)
        self.rect(15, 10, 180, 30, 'D')

        # Company name simulation
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 100, 80)
        self.set_xy(20, 15)
        self.cell(100, 10, 'PACIFIC RIM MATERIALS CO.')

        # Contact info in header
        self.set_font('Helvetica', '', 8)
        self.set_text_color(80, 80, 80)
        self.set_xy(20, 26)
        self.cell(100, 5, '9100 Harbor Boulevard, Suite 400')
        self.set_xy(20, 31)
        self.cell(100, 5, 'San Francisco, CA 94102')

        # Invoice label on right
        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(0, 100, 80)
        self.set_xy(140, 18)
        self.cell(50, 15, 'INVOICE', align='R')

        self.set_text_color(0, 0, 0)
        self.ln(40)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(0, 100, 80)
        self.set_line_width(0.5)
        self.line(15, self.get_y(), 195, self.get_y())
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(100, 100, 100)
        self.ln(2)
        self.cell(0, 5, 'Thank you for your business! Questions? billing@pacificrim-materials.com | (415) 555-8800', align='C')

def generate_invoice(output_path):
    pdf = LetterheadInvoice()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Invoice details box (top right style)
    pdf.set_xy(120, 50)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(0, 100, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(75, 7, 'INVOICE DETAILS', border=1, fill=True, align='C', ln=True)

    pdf.set_x(120)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(245, 250, 248)
    details = [
        f'Date: {datetime.now().strftime("%m/%d/%Y")}',
        'Invoice #: PRM-2026-1157',
        'Purchase Order Number: PO-2026-0755',
        'Due Date: NET 30'
    ]
    for d in details:
        pdf.set_x(120)
        pdf.cell(75, 6, d, border='LR', fill=True, ln=True)
    pdf.set_x(120)
    pdf.cell(75, 1, '', border='LRB', fill=True, ln=True)

    # Vendor Information box (left side)
    pdf.set_xy(15, 50)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(0, 100, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(95, 7, 'VENDOR INFORMATION', border=1, fill=True, align='C', ln=True)

    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(245, 250, 248)
    vendor_lines = [
        'Vendor Name: Pacific Rim Materials Co.',
        'Vendor Address: 9100 Harbor Blvd Suite 400',
        '                   San Francisco, CA 94102',
        'Vendor Phone Number: (415) 555-8800',
        'Vendor Email Address: sales@pacificrim-materials.com'
    ]
    for line in vendor_lines:
        pdf.set_x(15)
        pdf.cell(95, 6, line, border='LR', fill=True, ln=True)
    pdf.set_x(15)
    pdf.cell(95, 1, '', border='LRB', fill=True, ln=True)

    # Bill To section
    pdf.ln(5)
    pdf.set_x(15)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(95, 6, 'BILL TO:', border=1, fill=True, ln=True)
    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(95, 5, 'Infor Demo Company\nAccounts Payable\n500 Technology Drive\nAlpharetta, GA 30009', border=1)

    # Items section
    pdf.ln(8)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 100, 80)
    pdf.cell(0, 8, 'ORDER ITEMS', ln=True)

    # Table header
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_fill_color(0, 100, 80)
    pdf.set_text_color(255, 255, 255)

    col_w = [15, 28, 77, 25, 15, 20]
    headers = ['Line Number', 'Item Code', 'Description', 'Quantity Shipped', 'UOM', 'Price']
    for w, h in zip(col_w, headers):
        pdf.cell(w, 7, h, border=1, fill=True, align='C')
    pdf.ln()
    pdf.set_text_color(0, 0, 0)

    # 7 line items
    line_items = [
        ('1', 'ALU-6061-T6', 'Aluminum Sheet 6061-T6 4x8ft 0.125"', '20', 'SH', '$145.00'),
        ('2', 'ALU-5052-H32', 'Aluminum Sheet 5052-H32 4x8ft 0.090"', '15', 'SH', '$98.50'),
        ('3', 'SS-304-2B', 'Stainless Steel 304 2B Finish 4x8ft', '10', 'SH', '$275.00'),
        ('4', 'BRASS-260', 'Brass Sheet 260 Half Hard 2x4ft 0.032"', '8', 'SH', '$89.00'),
        ('5', 'COPPER-110', 'Copper Sheet 110 Soft 2x4ft 0.064"', '6', 'SH', '$125.00'),
        ('6', 'GAL-G90', 'Galvanized Steel G90 4x8ft 20ga', '25', 'SH', '$62.00'),
        ('7', 'PERF-SS-1/4', 'Perforated SS 304 1/4" Holes 3x8ft', '4', 'SH', '$310.00'),
    ]

    pdf.set_font('Helvetica', '', 8)
    for i, item in enumerate(line_items):
        if i % 2 == 0:
            pdf.set_fill_color(255, 255, 255)
        else:
            pdf.set_fill_color(245, 250, 248)

        pdf.cell(col_w[0], 6, item[0], border=1, align='C', fill=True)
        pdf.cell(col_w[1], 6, item[1], border=1, align='C', fill=True)
        pdf.cell(col_w[2], 6, item[2], border=1, fill=True)
        pdf.cell(col_w[3], 6, item[3], border=1, align='C', fill=True)
        pdf.cell(col_w[4], 6, item[4], border=1, align='C', fill=True)
        pdf.cell(col_w[5], 6, item[5], border=1, align='R', fill=True)
        pdf.ln()

    # Notes
    pdf.ln(10)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, 'All metal sheets certified mill test reports available upon request.', ln=True)

    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path

if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "Sample_Letterhead_PacificRim.pdf")
    generate_invoice(output_file)
