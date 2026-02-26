"""
Generate a fake PDF invoice for testing DemoInvoiceLoader RPA workflow.
Data structured for InvoiceAutomation_Agent_v2 extraction.
"""

from fpdf import FPDF
from datetime import datetime
import os

class InvoicePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 10, 'INVOICE', align='C', ln=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_invoice(output_path):
    pdf = InvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Invoice metadata
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, f'Invoice Date: {datetime.now().strftime("%B %d, %Y")}', ln=True)
    pdf.cell(0, 6, f'Invoice #: INV-2026-0042', ln=True)
    pdf.ln(10)

    # Vendor Information (FROM section)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'FROM (Vendor):', ln=True)
    pdf.set_font('Helvetica', '', 10)

    vendor_info = [
        'Acme Industrial Supply Co.',
        '1234 Commerce Boulevard',
        'Chicago, IL 60601',
        'Phone: (312) 555-7890',
        'Email: orders@acmeindustrial.com'
    ]
    for line in vendor_info:
        pdf.cell(0, 6, line, ln=True)

    pdf.ln(10)

    # Bill To section
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'BILL TO:', ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, 'Infor Demo Company', ln=True)
    pdf.cell(0, 6, '500 Technology Drive', ln=True)
    pdf.cell(0, 6, 'Alpharetta, GA 30009', ln=True)

    pdf.ln(10)

    # Purchase Order Information
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'PURCHASE ORDER DETAILS:', ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, 'PO Number: PO-0012345', ln=True)
    pdf.cell(0, 6, f'Order Date: {datetime.now().strftime("%Y%m%d")}', ln=True)
    pdf.cell(0, 6, 'Warehouse: MAIN', ln=True)
    pdf.cell(0, 6, 'Payment Terms: N30', ln=True)

    pdf.ln(10)

    # Line Items Table Header
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(15, 8, 'Line', border=1, fill=True, align='C')
    pdf.cell(30, 8, 'Item Code', border=1, fill=True, align='C')
    pdf.cell(70, 8, 'Description', border=1, fill=True, align='C')
    pdf.cell(25, 8, 'Qty', border=1, fill=True, align='C')
    pdf.cell(25, 8, 'UOM', border=1, fill=True, align='C')
    pdf.cell(25, 8, 'Unit Price', border=1, fill=True, align='C')
    pdf.ln()

    # Line Items Data
    line_items = [
        ('1', 'WIDGET-A1', 'Industrial Widget Assembly Type A', '100', 'EA', '$25.00'),
        ('2', 'BOLT-HEX-M8', 'Hex Bolt M8x25mm Stainless Steel', '500', 'EA', '$0.45'),
        ('3', 'GASKET-RND', 'Round Rubber Gasket 50mm OD', '250', 'EA', '$1.20'),
        ('4', 'BEARING-6205', 'Ball Bearing 6205-2RS Sealed', '24', 'EA', '$12.50'),
        ('5', 'LUBRICANT-5L', 'Machine Lubricant Grade 32 - 5L', '10', 'EA', '$45.00'),
    ]

    pdf.set_font('Helvetica', '', 9)
    for item in line_items:
        pdf.cell(15, 7, item[0], border=1, align='C')
        pdf.cell(30, 7, item[1], border=1, align='C')
        pdf.cell(70, 7, item[2], border=1)
        pdf.cell(25, 7, item[3], border=1, align='C')
        pdf.cell(25, 7, item[4], border=1, align='C')
        pdf.cell(25, 7, item[5], border=1, align='R')
        pdf.ln()

    pdf.ln(10)

    # Totals
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(140, 7, '', border=0)
    pdf.cell(25, 7, 'Subtotal:', border=0, align='R')
    pdf.cell(25, 7, '$3,475.00', border=0, align='R')
    pdf.ln()
    pdf.cell(140, 7, '', border=0)
    pdf.cell(25, 7, 'Tax (8%):', border=0, align='R')
    pdf.cell(25, 7, '$278.00', border=0, align='R')
    pdf.ln()
    pdf.cell(140, 7, '', border=0)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(25, 7, 'TOTAL:', border=0, align='R')
    pdf.cell(25, 7, '$3,753.00', border=0, align='R')

    pdf.ln(15)

    # Notes
    pdf.set_font('Helvetica', 'I', 9)
    pdf.cell(0, 6, 'Thank you for your business!', ln=True, align='C')

    # Save
    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")

if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\Invoices"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "TestInvoice_AcmeSupply.pdf")
    generate_invoice(output_file)
