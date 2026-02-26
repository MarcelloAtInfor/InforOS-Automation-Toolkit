"""
Generate a test PDF invoice for DemoInvoiceLoader RPA workflow.
Version 4: Mountain Valley Industrial Supply vendor
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
    pdf.cell(0, 6, 'Purchase Order Number: PO-2026-0201', ln=True)
    pdf.ln(10)

    # Vendor Information (FROM section)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'VENDOR:', ln=True)
    pdf.set_font('Helvetica', '', 10)

    vendor_info = [
        'Vendor Name: Mountain Valley Industrial Supply',
        'Vendor Address: 4500 Commerce Park Drive, Denver, CO 80239',
        'Vendor Phone Number: (303) 555-4200',
        'Vendor Email Address: sales@mvindust.com'
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

    # Line Items Data - Industrial supplies
    line_items = [
        ('1', 'VALVE-BALL-2IN', 'Ball Valve 2 inch Brass NPT', '12', 'EA'),
        ('2', 'PIPE-GALV-2X10', 'Galvanized Pipe 2in x 10ft', '25', 'EA'),
        ('3', 'FITTING-ELB-90', 'Elbow Fitting 90deg 2 inch', '50', 'EA'),
        ('4', 'GASKET-FLANG-2', 'Flange Gasket 2 inch Rubber', '100', 'EA'),
        ('5', 'PUMP-CENT-5HP', 'Centrifugal Pump 5HP 230V', '2', 'EA'),
        ('6', 'SEAL-MECH-STD', 'Mechanical Seal Standard', '8', 'EA'),
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
    pdf.cell(0, 6, 'Shipping Method: Freight LTL', ln=True)
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

    output_file = os.path.join(output_dir, "TestInvoice_MountainValley.pdf")
    generate_invoice(output_file)
    print(f"\nReady for RPA testing!")
