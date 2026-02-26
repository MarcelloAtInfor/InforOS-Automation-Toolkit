"""
Generate test PDF invoice for DemoInvoiceLoader RPA workflow.
Batch Invoice 06: Modern Grid Style - TechFlow Automation Inc.
"""

from fpdf import FPDF
from datetime import datetime
import os


class ModernGridInvoicePDF(FPDF):
    def header(self):
        # Modern blue header
        self.set_fill_color(25, 118, 210)
        self.rect(0, 0, 210, 22, 'F')
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(255, 255, 255)
        self.set_y(5)
        self.cell(0, 12, 'INVOICE', align='C', ln=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(25, 118, 210)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def generate_invoice(output_path):
    pdf = ModernGridInvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Grid Layout - 2x2 for metadata
    grid_y = pdf.get_y()
    cell_width = 95
    cell_height = 25

    # Grid cell 1: Order Date
    pdf.set_fill_color(245, 248, 255)
    pdf.set_draw_color(25, 118, 210)
    pdf.rect(10, grid_y, cell_width, cell_height, 'DF')
    pdf.set_xy(15, grid_y + 3)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'ORDER DATE', ln=True)
    pdf.set_x(15)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(25, 118, 210)
    pdf.cell(0, 8, datetime.now().strftime("%Y-%m-%d"), ln=True)

    # Grid cell 2: PO Number
    pdf.set_fill_color(245, 248, 255)
    pdf.rect(105, grid_y, cell_width, cell_height, 'DF')
    pdf.set_xy(110, grid_y + 3)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, 'PURCHASE ORDER NUMBER', ln=True)
    pdf.set_x(110)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(25, 118, 210)
    pdf.cell(0, 8, 'PO-2026-1006', ln=True)

    pdf.set_y(grid_y + cell_height + 5)

    # Vendor Section - Grid style
    pdf.set_fill_color(25, 118, 210)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(95, 7, '  VENDOR', fill=True)
    pdf.cell(95, 7, '  SHIP TO', fill=True, ln=True)

    pdf.set_fill_color(250, 252, 255)
    pdf.set_draw_color(25, 118, 210)

    # Vendor info cell
    vendor_y = pdf.get_y()
    pdf.rect(10, vendor_y, 95, 35, 'DF')
    pdf.set_xy(15, vendor_y + 3)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 5, 'Vendor Name: TechFlow Automation Inc.', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, 'Vendor Address: 8800 Innovation Way,', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, '                San Jose, CA 95134', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, 'Vendor Phone Number: (408) 555-7700', ln=True)
    pdf.set_x(15)
    pdf.cell(0, 5, 'Vendor Email Address: orders@techflow.com', ln=True)

    # Ship to cell
    pdf.rect(105, vendor_y, 95, 35, 'DF')
    pdf.set_xy(110, vendor_y + 3)
    pdf.cell(0, 5, 'Infor Demo Company', ln=True)
    pdf.set_x(110)
    pdf.cell(0, 5, 'Robotics Lab - Building R', ln=True)
    pdf.set_x(110)
    pdf.cell(0, 5, '1000 Factory Road', ln=True)
    pdf.set_x(110)
    pdf.cell(0, 5, 'Chicago, IL 60601', ln=True)

    pdf.set_y(vendor_y + 40)

    # Line Items Table Header - Modern blue
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(25, 118, 210)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(18, 8, 'Line Number', border=0, fill=True, align='C')
    pdf.cell(32, 8, 'Item Code', border=0, fill=True, align='C')
    pdf.cell(80, 8, 'Description', border=0, fill=True, align='C')
    pdf.cell(28, 8, 'Quantity Shipped', border=0, fill=True, align='C')
    pdf.cell(22, 8, 'UOM', border=0, fill=True, align='C')
    pdf.ln()

    # Line Items Data - Robotics/Automation (8 items max)
    line_items = [
        ('1', 'SERVO-400W', 'AC Servo Motor 400W with Encoder', '4', 'EA'),
        ('2', 'DRIVE-SERVO', 'Servo Drive Controller Unit', '4', 'EA'),
        ('3', 'ARM-ROBOT-6AX', '6-Axis Robot Arm Assembly', '1', 'EA'),
        ('4', 'GRIP-PNEUM-2J', '2-Jaw Pneumatic Gripper', '2', 'EA'),
        ('5', 'CABLE-SERVO-5M', 'Servo Motor Cable 5 Meter', '8', 'EA'),
        ('6', 'SENS-VISION-HD', 'HD Vision Sensor Camera', '2', 'EA'),
        ('7', 'PLC-MOTION', 'Motion Control PLC Module', '1', 'EA'),
        ('8', 'POWER-24V-20A', '24V DC Power Supply 20A', '3', 'EA'),
    ]

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    for i, item in enumerate(line_items):
        if i % 2 == 0:
            pdf.set_fill_color(250, 252, 255)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(18, 7, item[0], border='B', align='C', fill=True)
        pdf.cell(32, 7, item[1], border='B', align='C', fill=True)
        pdf.cell(80, 7, item[2], border='B', fill=True)
        pdf.cell(28, 7, item[3], border='B', align='C', fill=True)
        pdf.cell(22, 7, item[4], border='B', align='C', fill=True)
        pdf.ln()

    pdf.ln(10)

    # Terms - Grid style footer
    pdf.set_fill_color(245, 248, 255)
    pdf.set_draw_color(25, 118, 210)
    pdf.rect(10, pdf.get_y(), 190, 18, 'DF')

    pdf.set_xy(15, pdf.get_y() + 3)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(25, 118, 210)
    pdf.cell(40, 5, 'Payment Terms:')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(50, 5, 'Net 60')
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(25, 118, 210)
    pdf.cell(25, 5, 'Shipping:')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 5, 'Air Freight', ln=True)

    pdf.set_x(15)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(25, 118, 210)
    pdf.cell(40, 5, 'Expected Delivery:')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 5, '2026-02-28', ln=True)

    pdf.ln(12)

    # Notes
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, 'Please confirm receipt and expected ship date.', ln=True, align='C')

    # Save
    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path


if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "Invoice_TechFlowAutomation_PO-2026-1006.pdf")
    generate_invoice(output_file)
    print(f"\nReady for RPA testing!")
