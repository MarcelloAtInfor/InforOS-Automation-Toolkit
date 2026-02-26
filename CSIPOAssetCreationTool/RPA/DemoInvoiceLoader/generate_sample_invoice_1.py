"""
Generate a test PDF invoice with TWO-COLUMN LAYOUT.
Vendor info on left, order details on right, line items below.
"""

from fpdf import FPDF
from datetime import datetime
import os
import random

class TwoColumnInvoice(FPDF):
    def header(self):
        # Title bar
        self.set_fill_color(25, 60, 95)
        self.rect(0, 0, 210, 25, 'F')
        self.set_font('Helvetica', 'B', 24)
        self.set_text_color(255, 255, 255)
        self.set_y(8)
        self.cell(0, 10, 'SUPPLIER INVOICE', align='C')
        self.set_text_color(0, 0, 0)
        self.ln(25)

    def footer(self):
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Invoice generated on {datetime.now().strftime("%Y-%m-%d %H:%M")} | Page {self.page_no()}', align='C')

def generate_invoice(output_path):
    pdf = TwoColumnInvoice()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=25)

    # Two-column section
    left_x = 15
    right_x = 110
    start_y = 35

    # LEFT COLUMN - Vendor Information
    pdf.set_xy(left_x, start_y)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(85, 8, ' VENDOR INFORMATION', border=1, fill=True, ln=True)

    pdf.set_xy(left_x, pdf.get_y())
    pdf.set_font('Helvetica', '', 9)
    vendor_lines = [
        'Vendor Name: Summit Industrial Distributors',
        'Vendor Address: 5600 Enterprise Lane',
        '                   Portland, OR 97201',
        'Vendor Phone Number: (503) 555-4400',
        'Vendor Email Address: orders@summitind.com'
    ]
    for line in vendor_lines:
        pdf.cell(85, 6, line, border='LR', ln=True)
    pdf.cell(85, 2, '', border='LRB', ln=True)  # Bottom border

    # RIGHT COLUMN - Order Details
    pdf.set_xy(right_x, start_y)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(85, 8, ' ORDER DETAILS', border=1, fill=True, ln=True)

    pdf.set_xy(right_x, pdf.get_y())
    pdf.set_font('Helvetica', '', 9)
    order_lines = [
        f'Order Date: {datetime.now().strftime("%B %d, %Y")}',
        'Purchase Order Number: PO-2026-0601',
        'Invoice Number: INV-S-78452',
        'Ship Via: FedEx Ground',
        'Payment Terms: NET 45'
    ]
    for line in order_lines:
        pdf.set_x(right_x)
        pdf.cell(85, 6, line, border='LR', ln=True)
    pdf.set_x(right_x)
    pdf.cell(85, 2, '', border='LRB', ln=True)

    # Horizontal divider
    pdf.ln(10)
    current_y = pdf.get_y()
    pdf.set_draw_color(25, 60, 95)
    pdf.set_line_width(0.5)
    pdf.line(15, current_y, 195, current_y)
    pdf.ln(5)

    # Line Items Table
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(25, 60, 95)
    pdf.set_text_color(255, 255, 255)

    col_widths = [18, 32, 70, 30, 30]
    headers = ['Line Number', 'Item Code', 'Description', 'Quantity Shipped', 'UOM']

    for i, (w, h) in enumerate(zip(col_widths, headers)):
        pdf.cell(w, 9, h, border=1, fill=True, align='C')
    pdf.ln()
    pdf.set_text_color(0, 0, 0)

    # 3 line items
    line_items = [
        ('1', 'FLNG-SS-6IN', 'Stainless Steel Flange 6 Inch 150#', '12', 'EA'),
        ('2', 'PIPE-SCH40-4', 'Carbon Steel Pipe Schedule 40 4"x20ft', '8', 'EA'),
        ('3', 'ELBOW-90-SS', '90 Degree Elbow Stainless 4 Inch', '24', 'EA'),
    ]

    pdf.set_font('Helvetica', '', 9)
    for i, item in enumerate(line_items):
        if i % 2 == 0:
            pdf.set_fill_color(248, 248, 248)
        else:
            pdf.set_fill_color(255, 255, 255)

        pdf.cell(col_widths[0], 8, item[0], border=1, align='C', fill=True)
        pdf.cell(col_widths[1], 8, item[1], border=1, align='C', fill=True)
        pdf.cell(col_widths[2], 8, item[2], border=1, fill=True)
        pdf.cell(col_widths[3], 8, item[3], border=1, align='C', fill=True)
        pdf.cell(col_widths[4], 8, item[4], border=1, align='C', fill=True)
        pdf.ln()

    # Ship To Box (bottom right)
    pdf.ln(10)
    pdf.set_x(right_x)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(85, 7, ' SHIP TO:', border=1, fill=True, ln=True)
    pdf.set_x(right_x)
    pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(85, 5, 'Infor Demo Company\nWarehouse B - Receiving Dock\n2000 Industrial Way\nChicago, IL 60601', border=1)

    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path

if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "Sample_TwoColumn_SummitInd.pdf")
    generate_invoice(output_file)
