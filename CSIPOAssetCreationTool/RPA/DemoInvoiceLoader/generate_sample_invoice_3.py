"""
Generate a test PDF invoice with COMPACT ACCOUNTING FORM style.
Minimalist tabular key-value layout, accounting-style.
"""

from fpdf import FPDF
from datetime import datetime
import os

class CompactInvoice(FPDF):
    def header(self):
        pass  # No fancy header

    def footer(self):
        self.set_y(-10)
        self.set_font('Courier', '', 7)
        self.cell(0, 5, f'Form PO-STD Rev 2026.1 | Page {self.page_no()}', align='C')

def generate_invoice(output_path):
    pdf = CompactInvoice()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Courier', '', 9)

    # Title line
    pdf.set_font('Courier', 'B', 12)
    pdf.cell(0, 8, '=' * 60, ln=True, align='C')
    pdf.cell(0, 8, 'PURCHASE ORDER / MATERIALS REQUEST', ln=True, align='C')
    pdf.cell(0, 8, '=' * 60, ln=True, align='C')
    pdf.ln(5)

    # Key-value pairs in tabular format
    pdf.set_font('Courier', '', 9)

    def add_field(label, value, width=90):
        pdf.set_font('Courier', 'B', 9)
        pdf.cell(width, 6, label, border=0)
        pdf.set_font('Courier', '', 9)
        pdf.cell(100, 6, value, border=0, ln=True)

    add_field('DOCUMENT DATE:', datetime.now().strftime('%Y-%m-%d'))
    add_field('DOCUMENT NUMBER:', 'PO-2026-0822')
    pdf.ln(3)

    pdf.cell(0, 6, '-' * 80, ln=True)
    pdf.set_font('Courier', 'B', 9)
    pdf.cell(0, 6, 'SUPPLIER INFORMATION', ln=True)
    pdf.cell(0, 6, '-' * 80, ln=True)
    pdf.set_font('Courier', '', 9)

    add_field('Vendor Name:', 'Midwest Fastener & Hardware Supply')
    add_field('Vendor Address:', '4400 Commerce Drive, Suite 100')
    add_field('              ', 'Indianapolis, IN 46201')
    add_field('Vendor Phone Number:', '(317) 555-6622')
    add_field('Vendor Email Address:', 'orders@midwestfastener.com')

    pdf.ln(3)
    pdf.cell(0, 6, '-' * 80, ln=True)
    pdf.set_font('Courier', 'B', 9)
    pdf.cell(0, 6, 'ORDER INFORMATION', ln=True)
    pdf.cell(0, 6, '-' * 80, ln=True)
    pdf.set_font('Courier', '', 9)

    add_field('Purchase Order Number:', 'PO-2026-0822')
    add_field('Order Date:', datetime.now().strftime('%Y-%m-%d'))
    add_field('Requested By:', 'J. Smith - Maintenance Dept')
    add_field('Ship To:', 'Infor Demo Company - Dock 3')
    add_field('Terms:', 'Net 30 Days')

    pdf.ln(5)
    pdf.cell(0, 6, '=' * 80, ln=True)
    pdf.set_font('Courier', 'B', 9)
    pdf.cell(0, 6, 'LINE ITEMS', ln=True)
    pdf.cell(0, 6, '=' * 80, ln=True)

    # Simple ASCII-style table header
    pdf.set_font('Courier', 'B', 8)
    header = f"{'Line Number':<12}{'Item Code':<16}{'Description':<40}{'Quantity Shipped':>10}  {'UOM':<5}"
    pdf.cell(0, 6, header, ln=True)
    pdf.cell(0, 4, '-' * 85, ln=True)

    # Only 2 line items (minimum)
    line_items = [
        ('1', 'BOLT-HX-M12X50', 'Hex Bolt M12x50 Grade 8.8 Zinc Plated', '200', 'EA'),
        ('2', 'NUT-HX-M12', 'Hex Nut M12 Grade 8 Zinc Plated', '200', 'EA'),
    ]

    pdf.set_font('Courier', '', 8)
    for item in line_items:
        row = f"{item[0]:<12}{item[1]:<16}{item[2]:<40}{item[3]:>10}  {item[4]:<5}"
        pdf.cell(0, 5, row, ln=True)

    pdf.ln(5)
    pdf.cell(0, 4, '-' * 85, ln=True)

    # Summary
    pdf.ln(5)
    pdf.set_font('Courier', '', 9)
    pdf.cell(0, 5, 'TOTAL LINE ITEMS: 2', ln=True)
    pdf.cell(0, 5, 'TOTAL QUANTITY:   400 EA', ln=True)

    pdf.ln(10)
    pdf.cell(0, 6, '=' * 80, ln=True)
    pdf.set_font('Courier', 'B', 9)
    pdf.cell(0, 6, 'AUTHORIZATION', ln=True)
    pdf.cell(0, 6, '=' * 80, ln=True)

    pdf.set_font('Courier', '', 9)
    pdf.ln(5)
    pdf.cell(60, 6, 'Requested By: ________________', ln=False)
    pdf.cell(60, 6, 'Approved By: ________________', ln=True)
    pdf.ln(5)
    pdf.cell(60, 6, 'Date: ________________', ln=False)
    pdf.cell(60, 6, 'Date: ________________', ln=True)

    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path

if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "Sample_Compact_MidwestFastener.pdf")
    generate_invoice(output_file)
