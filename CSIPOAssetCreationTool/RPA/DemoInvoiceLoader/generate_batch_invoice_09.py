"""
Generate test PDF invoice for DemoInvoiceLoader RPA workflow.
Batch Invoice 09: Statement Style - Allied Packaging Solutions
"""

from fpdf import FPDF
from datetime import datetime
import os


class StatementStyleInvoicePDF(FPDF):
    def header(self):
        # Statement/Account style header
        self.set_fill_color(60, 60, 60)
        self.rect(0, 0, 70, 297, 'F')  # Left sidebar

        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(255, 255, 255)
        self.set_xy(5, 15)
        self.cell(60, 10, 'INVOICE', align='C', ln=True)

        self.set_font('Helvetica', '', 9)
        self.set_xy(5, 45)
        self.cell(60, 6, 'Statement Document', align='C', ln=True)

        # Main content area header
        self.set_text_color(60, 60, 60)
        self.set_font('Helvetica', 'B', 14)
        self.set_xy(80, 15)
        self.cell(0, 10, 'Allied Packaging Solutions', ln=True)

        self.ln(25)

    def footer(self):
        self.set_y(-20)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(255, 255, 255)
        self.set_x(5)
        self.cell(60, 5, f'Page {self.page_no()}', align='C')

        self.set_text_color(100, 100, 100)
        self.set_x(80)
        self.cell(0, 5, 'Thank you for your business', align='C')


def generate_invoice(output_path):
    pdf = StatementStyleInvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.set_left_margin(75)

    # Order Information Block
    pdf.set_xy(80, 50)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(50, 6, 'Order Date:')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, datetime.now().strftime("%Y-%m-%d"), ln=True)

    pdf.set_x(80)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(50, 6, 'Purchase Order Number:')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, 'PO-2026-1009', ln=True)

    pdf.ln(8)

    # Vendor Information
    pdf.set_x(80)
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(80, pdf.get_y(), 120, 30, 'F')

    pdf.set_xy(85, pdf.get_y() + 3)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, 'VENDOR DETAILS', ln=True)

    pdf.set_x(85)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 5, 'Vendor Name: Allied Packaging Solutions LLC', ln=True)
    pdf.set_x(85)
    pdf.cell(0, 5, 'Vendor Address: 2100 Warehouse Way, Memphis, TN 38118', ln=True)
    pdf.set_x(85)
    pdf.cell(0, 5, 'Vendor Phone Number: (901) 555-6600', ln=True)
    pdf.set_x(85)
    pdf.cell(0, 5, 'Vendor Email Address: orders@alliedpackaging.com', ln=True)

    pdf.ln(10)

    # Ship To
    pdf.set_x(80)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(30, 6, 'SHIP TO:')
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 6, 'Infor Demo Company - Shipping Dept., 1000 Factory Road, Chicago, IL 60601', ln=True)

    pdf.ln(10)

    # Line Items - Statement style
    pdf.set_x(80)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(60, 60, 60)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(15, 7, 'Line Number', fill=True, align='C')
    pdf.cell(25, 7, 'Item Code', fill=True, align='C')
    pdf.cell(55, 7, 'Description', fill=True, align='C')
    pdf.cell(15, 7, 'Quantity Shipped', fill=True, align='C')
    pdf.cell(10, 7, 'UOM', fill=True, align='C')
    pdf.ln()

    # Line Items Data - Packaging materials (fewer items)
    line_items = [
        ('1', 'BOX-CORR-18X12', 'Corrugated Box 18x12x10 (Bundle 25)', '20', 'BDL'),
        ('2', 'TAPE-PACK-2IN', 'Packing Tape 2" x 110yd Clear', '48', 'RL'),
    ]

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    for i, item in enumerate(line_items):
        pdf.set_x(80)
        if i % 2 == 0:
            pdf.set_fill_color(250, 250, 250)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(15, 7, item[0], border='B', align='C', fill=True)
        pdf.cell(25, 7, item[1], border='B', align='C', fill=True)
        pdf.cell(55, 7, item[2], border='B', fill=True)
        pdf.cell(15, 7, item[3], border='B', align='C', fill=True)
        pdf.cell(10, 7, item[4], border='B', align='C', fill=True)
        pdf.ln()

    pdf.ln(15)

    # Summary Section - Statement style
    pdf.set_x(80)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 7, 'ORDER SUMMARY', ln=True)

    pdf.set_draw_color(200, 200, 200)
    pdf.set_x(80)
    pdf.line(80, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font('Helvetica', '', 9)
    pdf.set_x(80)
    pdf.cell(70, 6, 'Total Line Items:')
    pdf.cell(0, 6, '2', ln=True)
    pdf.set_x(80)
    pdf.cell(70, 6, 'Total Quantity:')
    pdf.cell(0, 6, '68 units', ln=True)
    pdf.set_x(80)
    pdf.cell(70, 6, 'Payment Terms:')
    pdf.cell(0, 6, 'Net 30', ln=True)
    pdf.set_x(80)
    pdf.cell(70, 6, 'Shipping Method:')
    pdf.cell(0, 6, 'LTL Freight', ln=True)
    pdf.set_x(80)
    pdf.cell(70, 6, 'Expected Delivery:')
    pdf.cell(0, 6, '2026-02-10', ln=True)

    pdf.set_x(80)
    pdf.line(80, pdf.get_y() + 3, 200, pdf.get_y() + 3)

    pdf.ln(15)

    # Notes
    pdf.set_x(80)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, 'Please confirm receipt and expected ship date.', ln=True)

    # Save
    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path


if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "Invoice_AlliedPackaging_PO-2026-1009.pdf")
    generate_invoice(output_file)
    print(f"\nReady for RPA testing!")
