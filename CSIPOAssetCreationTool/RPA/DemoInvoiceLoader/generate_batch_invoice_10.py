"""
Generate test PDF invoice for DemoInvoiceLoader RPA workflow.
Batch Invoice 10: Warehouse Receipt Style - Central Distribution Co.
"""

from fpdf import FPDF
from datetime import datetime
import os


class WarehouseReceiptInvoicePDF(FPDF):
    def header(self):
        # Warehouse receipt style header
        self.set_fill_color(70, 90, 70)
        self.rect(0, 0, 210, 28, 'F')

        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(255, 255, 255)
        self.set_y(5)
        self.cell(0, 10, 'INVOICE', align='C', ln=True)

        self.set_font('Helvetica', '', 10)
        self.cell(0, 6, 'Purchase Order / Delivery Receipt', align='C', ln=True)

        self.ln(12)

    def footer(self):
        self.set_y(-20)
        self.set_draw_color(70, 90, 70)
        self.set_line_width(0.5)
        self.line(10, 278, 200, 278)

        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(70, 90, 70)
        self.cell(0, 5, f'Page {self.page_no()} | Retain for receiving records', align='C')


def generate_invoice(output_path):
    pdf = WarehouseReceiptInvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=25)

    # Reference Information Row
    pdf.set_fill_color(240, 245, 240)
    pdf.set_draw_color(70, 90, 70)
    pdf.rect(10, pdf.get_y(), 190, 18, 'DF')

    ref_y = pdf.get_y() + 2
    pdf.set_xy(15, ref_y)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(70, 90, 70)
    pdf.cell(35, 5, 'ORDER DATE:')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(40, 5, datetime.now().strftime("%Y-%m-%d"))

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(70, 90, 70)
    pdf.cell(55, 5, 'PURCHASE ORDER NUMBER:')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 5, 'PO-2026-1010', ln=True)

    pdf.set_xy(15, ref_y + 7)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(70, 90, 70)
    pdf.cell(35, 5, 'DOCK/LOCATION:')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(40, 5, 'Dock 4 - Bay B')

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(70, 90, 70)
    pdf.cell(55, 5, 'RECEIVER:')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 5, '________________', ln=True)

    pdf.set_y(pdf.get_y() + 8)

    # Vendor and Ship-To side by side
    col_y = pdf.get_y()

    # Vendor Box
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(70, 90, 70)
    pdf.rect(10, col_y, 95, 35, 'D')

    pdf.set_xy(15, col_y + 3)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(70, 90, 70)
    pdf.cell(0, 6, 'VENDOR (FROM)', ln=True)

    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 5, 'Vendor Name: Central Distribution Co.', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, 'Vendor Address: 4400 Logistics Center Drive,', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, '                Indianapolis, IN 46241', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, 'Vendor Phone Number: (317) 555-2200', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, 'Vendor Email Address: orders@centraldist.com', ln=True)

    # Ship-To Box
    pdf.rect(105, col_y, 95, 35, 'D')

    pdf.set_xy(110, col_y + 3)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(70, 90, 70)
    pdf.cell(0, 6, 'DELIVER TO', ln=True)

    pdf.set_x(110)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 5, 'Infor Demo Company', ln=True)
    pdf.set_x(110)
    pdf.cell(0, 5, 'Main Warehouse - Receiving', ln=True)
    pdf.set_x(110)
    pdf.cell(0, 5, '1000 Factory Road', ln=True)
    pdf.set_x(110)
    pdf.cell(0, 5, 'Chicago, IL 60601', ln=True)

    pdf.set_y(col_y + 40)

    # Line Items Table Header - Warehouse style
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(70, 90, 70)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(18, 8, 'Line Number', border=1, fill=True, align='C')
    pdf.cell(30, 8, 'Item Code', border=1, fill=True, align='C')
    pdf.cell(72, 8, 'Description', border=1, fill=True, align='C')
    pdf.cell(25, 8, 'Quantity Shipped', border=1, fill=True, align='C')
    pdf.cell(18, 8, 'UOM', border=1, fill=True, align='C')
    pdf.cell(17, 8, 'Received', border=1, fill=True, align='C')
    pdf.ln()

    # Line Items Data - Mixed MRO supplies
    line_items = [
        ('1', 'LAMP-FLUOR-T8', 'Fluorescent Lamp T8 4ft (Case 30)', '4', 'CS'),
        ('2', 'FILTER-AIR-20X25', 'Air Filter 20x25x1 MERV 8 (Case 12)', '6', 'CS'),
        ('3', 'TRASH-LINER-55', 'Trash Liner 55 Gallon Heavy Duty', '10', 'RL'),
        ('4', 'CLEANER-FLOOR-5G', 'Floor Cleaner Concentrate 5 Gal', '4', 'EA'),
        ('5', 'TOWEL-PAPER-CS', 'Paper Towels Multi-Fold Case', '12', 'CS'),
    ]

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(70, 90, 70)
    for i, item in enumerate(line_items):
        if i % 2 == 0:
            pdf.set_fill_color(248, 252, 248)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(18, 7, item[0], border=1, align='C', fill=True)
        pdf.cell(30, 7, item[1], border=1, align='C', fill=True)
        pdf.cell(72, 7, item[2], border=1, fill=True)
        pdf.cell(25, 7, item[3], border=1, align='C', fill=True)
        pdf.cell(18, 7, item[4], border=1, align='C', fill=True)
        pdf.cell(17, 7, '______', border=1, align='C', fill=True)  # Received checkbox
        pdf.ln()

    pdf.ln(10)

    # Handling Notes Section
    pdf.set_fill_color(255, 250, 240)
    pdf.set_draw_color(180, 140, 80)
    pdf.rect(10, pdf.get_y(), 190, 22, 'DF')

    pdf.set_xy(15, pdf.get_y() + 3)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(140, 100, 40)
    pdf.cell(0, 5, 'HANDLING NOTES', ln=True)

    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(80, 60, 30)
    pdf.cell(0, 5, 'Store in dry location. Check for damage before signing. Report discrepancies within 24 hours.', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, 'Fragile items - handle with care.', ln=True)

    pdf.ln(8)

    # Signature/Terms Section
    pdf.set_draw_color(70, 90, 70)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(60, 6, 'Payment Terms: Net 30')
    pdf.cell(60, 6, 'Shipping: LTL Carrier')
    pdf.cell(0, 6, 'Expected: 2026-02-08', ln=True)

    pdf.ln(5)

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(70, 90, 70)
    pdf.cell(50, 6, 'Received By:')
    pdf.cell(70, 6, '_________________________')
    pdf.cell(25, 6, 'Date:')
    pdf.cell(0, 6, '___________', ln=True)

    # Save
    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path


if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "Invoice_CentralDistribution_PO-2026-1010.pdf")
    generate_invoice(output_file)
    print(f"\nReady for RPA testing!")
