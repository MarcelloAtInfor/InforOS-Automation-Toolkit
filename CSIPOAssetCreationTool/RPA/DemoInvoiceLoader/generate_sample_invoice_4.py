"""
Generate a test PDF invoice with MANIFEST/PACKING LIST style.
Detailed narrative format with inline item descriptions, like a shipping manifest.
"""

from fpdf import FPDF
from datetime import datetime
import os

class ManifestInvoice(FPDF):
    def header(self):
        # Top banner
        self.set_fill_color(50, 50, 50)
        self.rect(0, 0, 210, 12, 'F')
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(255, 255, 255)
        self.set_y(3)
        self.cell(0, 6, 'SHIPPING MANIFEST & INVOICE', align='C')
        self.set_text_color(0, 0, 0)
        self.ln(15)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', '', 7)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, f'Document ID: MAN-{datetime.now().strftime("%Y%m%d")}-001 | Generated {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Page {self.page_no()}', align='C')

def generate_invoice(output_path):
    pdf = ManifestInvoice()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=18)

    # Document reference section
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(95, 7, 'DOCUMENT REFERENCE', border='B', ln=False)
    pdf.cell(95, 7, 'SHIPMENT DETAILS', border='B', ln=True)

    pdf.set_font('Helvetica', '', 9)
    pdf.cell(95, 5, f'Date Issued: {datetime.now().strftime("%A, %B %d, %Y")}', ln=False)
    pdf.cell(95, 5, 'Carrier: ABC Freight Services', ln=True)
    pdf.cell(95, 5, 'Purchase Order Number: PO-2026-0999', ln=False)
    pdf.cell(95, 5, 'Tracking #: 1Z999AA10123456784', ln=True)
    pdf.cell(95, 5, 'Invoice Reference: INV-EC-88742', ln=False)
    pdf.cell(95, 5, 'Weight: 485 lbs | 12 Packages', ln=True)

    pdf.ln(5)

    # Vendor block - narrative style
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 7, ' ORIGIN / VENDOR', border=1, fill=True, ln=True)

    pdf.set_font('Helvetica', '', 9)
    narrative = (
        "Vendor Name: Eastern Components & Electronics Ltd.\n"
        "Vendor Address: 12000 Technology Park Circle, Building 7, Raleigh, NC 27606\n"
        "Vendor Phone Number: (919) 555-3300\n"
        "Vendor Email Address: shipping@easterncomponents.com\n"
        "Contact: Sarah Williams, Shipping Coordinator"
    )
    pdf.multi_cell(0, 5, narrative, border='LRB')

    pdf.ln(3)

    # Destination block
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 7, ' DESTINATION / SHIP TO', border=1, fill=True, ln=True)

    pdf.set_font('Helvetica', '', 9)
    dest = (
        "Infor Demo Company - Electronics Assembly Division\n"
        "Building 12, Receiving Bay C\n"
        "1500 Manufacturing Parkway, Chicago, IL 60601\n"
        "Attention: Receiving Department | Ref: PO-2026-0999"
    )
    pdf.multi_cell(0, 5, dest, border='LRB')

    pdf.ln(5)

    # Items manifest
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(50, 50, 50)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 7, ' ITEMIZED MANIFEST (10 ITEMS)', border=1, fill=True, ln=True)
    pdf.set_text_color(0, 0, 0)

    # Table header
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_fill_color(220, 220, 220)
    cols = [12, 25, 95, 25, 15, 18]
    headers = ['Line Number', 'Item Code', 'Description', 'Quantity Shipped', 'UOM', 'Box #']
    for w, h in zip(cols, headers):
        pdf.cell(w, 6, h, border=1, fill=True, align='C')
    pdf.ln()

    # 10 line items (maximum requested)
    line_items = [
        ('1', 'CAP-ELEC-100UF', 'Electrolytic Capacitor 100uF 50V 105C', '500', 'EA', '1'),
        ('2', 'CAP-CER-0.1UF', 'Ceramic Capacitor 0.1uF 50V X7R', '1000', 'EA', '1'),
        ('3', 'RES-SMD-10K', 'SMD Resistor 10K Ohm 0805 1%', '2000', 'EA', '2'),
        ('4', 'RES-SMD-4.7K', 'SMD Resistor 4.7K Ohm 0805 1%', '2000', 'EA', '2'),
        ('5', 'LED-RED-5MM', 'LED Red 5mm Diffused 2V 20mA', '250', 'EA', '3'),
        ('6', 'LED-GRN-5MM', 'LED Green 5mm Diffused 2.2V 20mA', '250', 'EA', '3'),
        ('7', 'IC-ATMEGA328', 'Microcontroller ATmega328P-PU DIP28', '50', 'EA', '4'),
        ('8', 'IC-LM7805', 'Voltage Regulator LM7805 TO-220', '100', 'EA', '5'),
        ('9', 'CONN-HDR-40P', 'Pin Header 40-Pin Male 2.54mm', '75', 'EA', '6'),
        ('10', 'PCB-PROTO-L', 'Prototype PCB Double-Sided 10x15cm', '25', 'EA', '6'),
    ]

    pdf.set_font('Helvetica', '', 8)
    for i, item in enumerate(line_items):
        if i % 2 == 0:
            pdf.set_fill_color(255, 255, 255)
        else:
            pdf.set_fill_color(248, 248, 248)

        pdf.cell(cols[0], 5, item[0], border=1, align='C', fill=True)
        pdf.cell(cols[1], 5, item[1], border=1, align='C', fill=True)
        pdf.cell(cols[2], 5, item[2], border=1, fill=True)
        pdf.cell(cols[3], 5, item[3], border=1, align='C', fill=True)
        pdf.cell(cols[4], 5, item[4], border=1, align='C', fill=True)
        pdf.cell(cols[5], 5, item[5], border=1, align='C', fill=True)
        pdf.ln()

    # Summary section
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(0, 6, 'SHIPMENT SUMMARY', border='B', ln=True)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(60, 5, 'Total Line Items: 10', ln=False)
    pdf.cell(60, 5, 'Total Packages: 6 boxes', ln=False)
    pdf.cell(60, 5, 'Order Date: ' + datetime.now().strftime('%Y-%m-%d'), ln=True)
    pdf.cell(60, 5, 'Payment Terms: NET 30', ln=False)
    pdf.cell(60, 5, 'Ship Method: Ground Freight', ln=True)

    # Signature area
    pdf.ln(10)
    pdf.set_draw_color(150, 150, 150)
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(90, 5, 'Shipped By: ____________________________', ln=False)
    pdf.cell(90, 5, 'Received By: ____________________________', ln=True)
    pdf.cell(90, 5, 'Date/Time: ____________________________', ln=False)
    pdf.cell(90, 5, 'Date/Time: ____________________________', ln=True)

    pdf.output(output_path)
    print(f"Invoice generated: {output_path}")
    return output_path

if __name__ == "__main__":
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "Sample_Manifest_EasternComponents.pdf")
    generate_invoice(output_file)
