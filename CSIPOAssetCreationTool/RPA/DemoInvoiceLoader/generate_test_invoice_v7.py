"""
Generate a test PDF invoice for DemoInvoiceLoader RPA workflow.
Version 7: Western Manufacturing Solutions - 5 line items
"""

from fpdf import FPDF
from datetime import datetime
import os

class InvoicePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 10, 'PURCHASE ORDER', align='C', ln=True)
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
    pdf.cell(0, 6, f'Order Date: {datetime.now().strftime("%Y-%m-%d")}', ln=True)
    pdf.cell(0, 6, 'Purchase Order Number: PO-2026-0520', ln=True)
    pdf.ln(10)

    # Vendor Information (FROM section)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'VENDOR:', ln=True)
    pdf.set_font('Helvetica', '', 10)

    vendor_info = [
        'Vendor Name: Western Manufacturing Solutions',
        'Vendor Address: 3800 Industrial Park Road, Phoenix, AZ 85034',
        'Vendor Phone Number: (602) 555-3200',
        'Vendor Email Address: orders@westernmfg.com'
    ]
    for line in vendor_info:
        pdf.cell(0, 6, line, ln=True)

    pdf.ln(10)

    # Ship To section
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'SHIP TO:', ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, 'Infor Demo Company', ln=True)
    pdf.cell(0, 6, 'Manufacturing Plant - Building A', ln=True)
    pdf.cell(0, 6, '1000 Factory Road, Chicago, IL 60601', ln=True)

    pdf.ln(10)

    # Line Items Table Header
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(44, 90, 160)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(20, 8, 'Line Number', border=1, fill=True, align='C')
    pdf.cell(35, 8, 'Item Code', border=1, fill=True, align='C')
    pdf.cell(75, 8, 'Description', border=1, fill=True, align='C')
    pdf.cell(30, 8, 'Quantity Shipped', border=1, fill=True, align='C')
    pdf.cell(20, 8, 'UOM', border=1, fill=True, align='C')
    pdf.ln()
    pdf.set_text_color(0, 0, 0)

    # Line Items Data - 5 items for simpler testing
    line_items = [
        ('1', 'BEAR-6205-2RS', 'Ball Bearing 6205-2RS Sealed', '50', 'EA'),
        ('2', 'SHAFT-STL-25', 'Steel Shaft 25mm x 500mm', '20', 'EA'),
        ('3', 'SPRKT-40B-18', 'Sprocket 40B 18-Tooth', '12', 'EA'),
        ('4', 'CHAIN-40-10FT', 'Roller Chain #40 10ft Length', '8', 'EA'),
        ('5', 'COUP-JAW-L100', 'Jaw Coupling L100 Complete', '6', 'EA'),
    ]

    pdf.set_font('Helvetica', '', 9)
    for i, item in enumerate(line_items):
        if i % 2 == 0:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(20, 7, item[0], border=1, align='C', fill=True)
        pdf.cell(35, 7, item[1], border=1, align='C', fill=True)
        pdf.cell(75, 7, item[2], border=1, fill=True)
        pdf.cell(30, 7, item[3], border=1, align='C', fill=True)
        pdf.cell(20, 7, item[4], border=1, align='C', fill=True)
        pdf.ln()

    pdf.ln(15)

    # Terms
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'Terms & Conditions:', ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, 'Payment Terms: Net 30', ln=True)
    pdf.cell(0, 6, 'Shipping Method: FedEx Ground', ln=True)
    pdf.cell(0, 6, 'Expected Delivery: 2026-02-15', ln=True)

    pdf.ln(15)

    # Notes
    pdf.set_font('Helvetica', 'I', 9)
    pdf.cell(0, 6, 'Please confirm receipt and expected ship date.', ln=True, align='C')
    pdf.cell(0, 6, 'Questions? Contact purchasing@example.com', ln=True, align='C')

    # Save
    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path

if __name__ == "__main__":
    # Output directly to the RPA Input folder
    output_dir = r"C:\RPAFiles\OCR_TEST\Input"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "TestInvoice_WesternMfg.pdf")
    generate_invoice(output_file)
    print(f"\nReady for RPA testing!")
