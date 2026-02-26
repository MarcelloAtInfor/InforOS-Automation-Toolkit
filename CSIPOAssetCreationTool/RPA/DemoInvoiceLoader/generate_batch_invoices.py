"""
Generate 10 test PDF invoices for DemoInvoiceLoader RPA workflow testing.
Each invoice has different vendor, PO number, and line items.
"""

from fpdf import FPDF
from datetime import datetime, timedelta
import os
import random

class InvoicePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 10, 'PURCHASE ORDER', align='C', ln=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


# Vendor data pool
VENDORS = [
    {
        'name': 'Precision Tools & Equipment Inc.',
        'address': '2750 Technology Drive, Austin, TX 78745',
        'phone': '(512) 555-8834',
        'email': 'orders@precisiontools.com'
    },
    {
        'name': 'Global Parts Distribution LLC',
        'address': '500 Commerce Way, Detroit, MI 48201',
        'phone': '(313) 555-2200',
        'email': 'sales@globalparts.com'
    },
    {
        'name': 'Acme Supply Company',
        'address': '123 Industrial Blvd, Cleveland, OH 44114',
        'phone': '(216) 555-7700',
        'email': 'orders@acmesupply.com'
    },
    {
        'name': 'Northern Steel & Metal Works',
        'address': '8800 Foundry Road, Pittsburgh, PA 15201',
        'phone': '(412) 555-3300',
        'email': 'procurement@northernsteel.com'
    },
    {
        'name': 'Pacific Industrial Supply',
        'address': '1200 Harbor Drive, Long Beach, CA 90802',
        'phone': '(562) 555-9900',
        'email': 'orders@pacificindustrial.com'
    },
    {
        'name': 'Midwest Machine Components',
        'address': '3400 Manufacturing Lane, Milwaukee, WI 53202',
        'phone': '(414) 555-4455',
        'email': 'sales@midwestmachine.com'
    },
    {
        'name': 'Atlantic Hardware Distributors',
        'address': '750 Warehouse Row, Newark, NJ 07102',
        'phone': '(973) 555-6677',
        'email': 'orders@atlantichardware.com'
    },
    {
        'name': 'Southern Manufacturing Supplies',
        'address': '2100 Industrial Park Blvd, Atlanta, GA 30301',
        'phone': '(404) 555-1122',
        'email': 'procurement@southernmfg.com'
    },
    {
        'name': 'Rocky Mountain Tool Co.',
        'address': '4500 Mountain View Dr, Denver, CO 80202',
        'phone': '(303) 555-8899',
        'email': 'sales@rockymountaintool.com'
    },
    {
        'name': 'Great Lakes Fasteners Inc.',
        'address': '900 Lakeshore Industrial, Chicago, IL 60601',
        'phone': '(312) 555-5544',
        'email': 'orders@greatlakesfasteners.com'
    }
]

# Line items pool
LINE_ITEMS_POOL = [
    ('DRILL-CARB-10', 'Carbide Drill Bit 10mm Coated', 'EA'),
    ('MILL-END-4FL', 'End Mill 4-Flute HSS 12mm', 'EA'),
    ('INSERT-CNMG', 'Carbide Insert CNMG 120408', 'EA'),
    ('TOOL-HOLD-BT40', 'Tool Holder BT40 ER32 Collet', 'EA'),
    ('COOL-SYNTH-5G', 'Synthetic Cutting Fluid 5 Gallon', 'EA'),
    ('BOLT-HEX-M10', 'Hex Bolt M10x50 Grade 8.8', 'EA'),
    ('NUT-HEX-M10', 'Hex Nut M10 Grade 8', 'EA'),
    ('WASHER-FLAT-M10', 'Flat Washer M10 Zinc Plated', 'EA'),
    ('BEARING-6205', 'Ball Bearing 6205-2RS Sealed', 'EA'),
    ('SEAL-OIL-35X50', 'Oil Seal 35x50x10 NBR', 'EA'),
    ('VALVE-BALL-1IN', 'Ball Valve 1 Inch Brass', 'EA'),
    ('PIPE-SCH40-2IN', 'Steel Pipe SCH40 2 Inch x 10ft', 'EA'),
    ('FITTING-ELBOW-2', 'Pipe Elbow 90deg 2 Inch', 'EA'),
    ('MOTOR-AC-5HP', 'AC Motor 5HP 1800RPM 3-Phase', 'EA'),
    ('BELT-V-B68', 'V-Belt B68 Industrial Grade', 'EA'),
    ('CHAIN-ROLL-60', 'Roller Chain #60 10ft Length', 'EA'),
    ('SPROCKET-60-20', 'Sprocket #60 Chain 20 Teeth', 'EA'),
    ('GEAR-SPUR-M2', 'Spur Gear Module 2 40 Teeth', 'EA'),
    ('SHAFT-STEEL-1', 'Steel Shaft 1 Inch Dia x 24in', 'EA'),
    ('KEY-WOOD-1/4', 'Woodruff Key 1/4 x 1 Inch', 'EA'),
    ('LUBR-GREASE-14', 'Lithium Grease 14oz Cartridge', 'EA'),
    ('FILTER-HYD-10M', 'Hydraulic Filter 10 Micron', 'EA'),
    ('HOSE-HYD-1/2', 'Hydraulic Hose 1/2in x 6ft', 'EA'),
    ('COUPL-FLEX-1', 'Flexible Coupling 1in Bore', 'EA'),
    ('MOUNT-VIBR-M8', 'Vibration Mount M8 Thread', 'EA'),
]


def generate_invoice(output_path, vendor, po_number, order_date, line_items):
    pdf = InvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Invoice metadata
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, f'Order Date: {order_date.strftime("%Y-%m-%d")}', ln=True)
    pdf.cell(0, 6, f'Purchase Order Number: {po_number}', ln=True)
    pdf.ln(10)

    # Vendor Information
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'VENDOR:', ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, f"Vendor Name: {vendor['name']}", ln=True)
    pdf.cell(0, 6, f"Vendor Address: {vendor['address']}", ln=True)
    pdf.cell(0, 6, f"Vendor Phone Number: {vendor['phone']}", ln=True)
    pdf.cell(0, 6, f"Vendor Email Address: {vendor['email']}", ln=True)
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

    # Line Items Data
    pdf.set_font('Helvetica', '', 9)
    for i, item in enumerate(line_items):
        if i % 2 == 0:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(20, 7, str(item[0]), border=1, align='C', fill=True)
        pdf.cell(35, 7, item[1], border=1, align='C', fill=True)
        pdf.cell(75, 7, item[2], border=1, fill=True)
        pdf.cell(30, 7, str(item[3]), border=1, align='C', fill=True)
        pdf.cell(20, 7, item[4], border=1, align='C', fill=True)
        pdf.ln()

    pdf.ln(15)

    # Terms
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'Terms & Conditions:', ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, 'Payment Terms: Net 30', ln=True)
    pdf.cell(0, 6, 'Shipping Method: UPS Ground', ln=True)
    delivery_date = order_date + timedelta(days=14)
    pdf.cell(0, 6, f'Expected Delivery: {delivery_date.strftime("%Y-%m-%d")}', ln=True)

    pdf.ln(15)

    # Notes
    pdf.set_font('Helvetica', 'I', 9)
    pdf.cell(0, 6, 'Please confirm receipt and expected ship date.', ln=True, align='C')
    pdf.cell(0, 6, 'Questions? Contact purchasing@example.com', ln=True, align='C')

    # Save
    pdf.output(output_path)
    return output_path


def generate_random_line_items(num_items):
    """Generate random line items for an invoice."""
    selected = random.sample(LINE_ITEMS_POOL, min(num_items, len(LINE_ITEMS_POOL)))
    items = []
    for i, (code, desc, uom) in enumerate(selected, 1):
        qty = random.choice([5, 10, 15, 20, 25, 50, 100])
        items.append((i, code, desc, qty, uom))
    return items


def main():
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)

    base_date = datetime.now()
    generated_files = []

    print("Generating 10 test invoices...")
    print("-" * 50)

    for i in range(10):
        # Select vendor (cycle through all 10)
        vendor = VENDORS[i]

        # Generate PO number
        po_number = f"PO-2026-{1001 + i:04d}"

        # Vary the order date slightly
        order_date = base_date - timedelta(days=random.randint(0, 7))

        # Generate 3-6 random line items
        num_items = random.randint(3, 6)
        line_items = generate_random_line_items(num_items)

        # Create filename
        vendor_short = vendor['name'].split()[0]
        filename = f"Invoice_{i+1:02d}_{vendor_short}_{po_number}.pdf"
        output_path = os.path.join(output_dir, filename)

        # Generate the invoice
        generate_invoice(output_path, vendor, po_number, order_date, line_items)
        generated_files.append(filename)

        print(f"  [{i+1:2d}/10] {filename}")
        print(f"         Vendor: {vendor['name']}")
        print(f"         PO: {po_number}, Items: {num_items}")

    print("-" * 50)
    print(f"\nGenerated {len(generated_files)} invoices in: {output_dir}")
    print("\nReady for RPA testing!")


if __name__ == "__main__":
    main()
