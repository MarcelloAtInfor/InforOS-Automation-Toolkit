"""
Generate 25 unique PDF invoices for DemoInvoiceLoader RPA workflow testing.

Uses cryptographic randomness and programmatic generation to ensure uniqueness:
- PO Numbers: Timestamp + random hex (billions of combinations)
- Vendor Names: Prefix + Suffix + Entity type combinations
- Item Codes: Category + Subcategory + random alphanumeric
- Order Dates: Random within last 30 days
- Line Items: Random count (2-7) with randomized quantities

Output: C:\RPAFiles\OCR_TEST\Samples\
"""

import secrets
import random
import string
import os
from fpdf import FPDF
from datetime import datetime, timedelta


class InvoicePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 10, 'INVOICE', align='C', ln=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


# ============================================================================
# DATA POOLS FOR RANDOMIZATION
# ============================================================================

# Vendor name components
VENDOR_PREFIXES = [
    'Apex', 'Quantum', 'Stellar', 'Vanguard', 'Cascade', 'Meridian', 'Pinnacle',
    'Summit', 'Atlas', 'Horizon', 'Nexus', 'Velocity', 'Precision', 'Global',
    'Premier', 'Dynamic', 'Integrated', 'Advanced', 'Elite', 'Strategic',
    'Unified', 'Continental', 'Pacific', 'Atlantic', 'Northern', 'Southern',
    'Central', 'Metro', 'National', 'Allied'
]

VENDOR_SUFFIXES = [
    'Manufacturing', 'Industrial', 'Fabrication', 'Components', 'Solutions',
    'Technologies', 'Systems', 'Products', 'Supplies', 'Parts', 'Equipment',
    'Tools', 'Materials', 'Resources', 'Engineering', 'Automation', 'Dynamics',
    'Metalworks', 'Machining', 'Precision'
]

ENTITY_TYPES = ['Inc.', 'LLC', 'Corp.', 'Co.', 'Ltd.', 'Group']

# Address components
STREET_NAMES = [
    'Industrial', 'Commerce', 'Enterprise', 'Technology', 'Business', 'Corporate',
    'Factory', 'Manufacturing', 'Innovation', 'Progress', 'Prosperity', 'Market',
    'Trade', 'Distribution', 'Warehouse', 'Logistics', 'Supply', 'Production'
]

STREET_TYPES = ['Drive', 'Boulevard', 'Avenue', 'Way', 'Parkway', 'Road', 'Lane', 'Street']

CITIES_STATES_ZIPS = [
    ('Houston', 'TX', '77001'), ('Dallas', 'TX', '75201'), ('Austin', 'TX', '78701'),
    ('Phoenix', 'AZ', '85001'), ('Denver', 'CO', '80201'), ('Seattle', 'WA', '98101'),
    ('Portland', 'OR', '97201'), ('Atlanta', 'GA', '30301'), ('Miami', 'FL', '33101'),
    ('Tampa', 'FL', '33601'), ('Charlotte', 'NC', '28201'), ('Nashville', 'TN', '37201'),
    ('Detroit', 'MI', '48201'), ('Cleveland', 'OH', '44101'), ('Columbus', 'OH', '43201'),
    ('Indianapolis', 'IN', '46201'), ('Milwaukee', 'WI', '53201'), ('Minneapolis', 'MN', '55401'),
    ('Kansas City', 'MO', '64101'), ('St. Louis', 'MO', '63101'), ('Memphis', 'TN', '38101'),
    ('Louisville', 'KY', '40201'), ('Birmingham', 'AL', '35201'), ('New Orleans', 'LA', '70112'),
    ('Salt Lake City', 'UT', '84101'), ('Albuquerque', 'NM', '87101'), ('Tucson', 'AZ', '85701'),
    ('Sacramento', 'CA', '95814'), ('San Diego', 'CA', '92101'), ('Oakland', 'CA', '94601')
]

# Item code components
ITEM_CATEGORIES = [
    ('MECH', 'Mechanical'), ('ELEC', 'Electrical'), ('HYDR', 'Hydraulic'),
    ('PNEU', 'Pneumatic'), ('FAST', 'Fastener'), ('TOOL', 'Tooling'),
    ('SEAL', 'Sealing'), ('BEAR', 'Bearing'), ('VALV', 'Valve'),
    ('PUMP', 'Pump'), ('MOTR', 'Motor'), ('GEAR', 'Gearing'),
    ('FILT', 'Filter'), ('SENS', 'Sensor'), ('CTRL', 'Control')
]

ITEM_SUBCATEGORIES = [
    'PLT', 'ROD', 'BRK', 'ASM', 'KIT', 'MOD', 'CPL', 'FTG',
    'HSG', 'SFT', 'BLK', 'CAP', 'RNG', 'SPR', 'PIN', 'BLT'
]

# Item description components
ITEM_ADJECTIVES = [
    'Heavy-Duty', 'Industrial', 'Precision', 'High-Performance', 'Standard',
    'Premium', 'Commercial', 'Professional', 'Reinforced', 'Stainless',
    'Hardened', 'Coated', 'Galvanized', 'Anodized', 'Chrome'
]

ITEM_NOUNS = [
    'Assembly', 'Component', 'Module', 'Unit', 'Bracket', 'Plate', 'Housing',
    'Fitting', 'Coupling', 'Shaft', 'Bearing', 'Seal', 'Gasket', 'Valve',
    'Spring', 'Bushing', 'Rod', 'Block', 'Cap', 'Ring', 'Pin', 'Bolt'
]

ITEM_MODIFIERS = [
    '10mm', '12mm', '15mm', '20mm', '25mm', '1/4"', '3/8"', '1/2"', '3/4"', '1"',
    'Type A', 'Type B', 'Type C', 'Series 100', 'Series 200', 'Series 300',
    'Grade 5', 'Grade 8', 'Class 1', 'Class 2', 'Mark II', 'Rev B'
]

UOMS = ['EA', 'PK', 'BX', 'CS', 'PR', 'SET', 'KT', 'RL']


# ============================================================================
# GENERATION FUNCTIONS
# ============================================================================

def generate_po_number():
    """Generate unique PO number using timestamp + random hex."""
    year = datetime.now().year
    timestamp_hex = secrets.token_hex(2).upper()  # 4 hex chars from timestamp
    random_hex = secrets.token_hex(2).upper()      # 4 hex chars random
    return f"PO-{year}-{timestamp_hex}{random_hex}"


def generate_vendor_name(used_names: set) -> str:
    """Generate unique vendor name from prefix + suffix + entity."""
    max_attempts = 100
    for _ in range(max_attempts):
        prefix = random.choice(VENDOR_PREFIXES)
        suffix = random.choice(VENDOR_SUFFIXES)
        entity = random.choice(ENTITY_TYPES)
        name = f"{prefix} {suffix} {entity}"
        if name not in used_names:
            used_names.add(name)
            return name
    # Fallback: add random number
    return f"{prefix} {suffix} {secrets.token_hex(2).upper()} {entity}"


def generate_vendor_address() -> tuple:
    """Generate vendor address, phone, and email."""
    street_num = random.randint(100, 9999)
    street_name = random.choice(STREET_NAMES)
    street_type = random.choice(STREET_TYPES)
    city, state, zip_code = random.choice(CITIES_STATES_ZIPS)

    # Add some randomness to zip code
    zip_suffix = str(random.randint(0, 99)).zfill(2)
    zip_code = zip_code[:3] + zip_suffix

    address = f"{street_num} {street_name} {street_type}, {city}, {state} {zip_code}"

    area_codes = ['214', '469', '512', '713', '281', '602', '303', '206', '404', '305']
    phone = f"({random.choice(area_codes)}) 555-{random.randint(1000, 9999)}"

    return address, phone


def generate_item_code(used_codes: set) -> str:
    """Generate unique item code: CATEGORY-SUBCATEGORY-RANDOM4."""
    max_attempts = 100
    for _ in range(max_attempts):
        category = random.choice(ITEM_CATEGORIES)[0]
        subcategory = random.choice(ITEM_SUBCATEGORIES)
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        code = f"{category}-{subcategory}-{random_suffix}"
        if code not in used_codes:
            used_codes.add(code)
            return code
    # Fallback
    return f"{category}-{subcategory}-{secrets.token_hex(2).upper()}"


def generate_item_description() -> str:
    """Generate item description from adjective + noun + modifier."""
    adj = random.choice(ITEM_ADJECTIVES)
    noun = random.choice(ITEM_NOUNS)
    mod = random.choice(ITEM_MODIFIERS)
    return f"{adj} {noun} {mod}"


def generate_order_date() -> str:
    """Generate random order date within last 30 days."""
    days_ago = random.randint(0, 30)
    date = datetime.now() - timedelta(days=days_ago)
    return date.strftime("%Y-%m-%d")


def generate_line_items(count: int, used_codes: set) -> list:
    """Generate specified number of unique line items."""
    items = []
    for i in range(1, count + 1):
        code = generate_item_code(used_codes)
        description = generate_item_description()
        quantity = random.choice([5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200, 250, 500])
        uom = random.choice(UOMS)
        unit_price = round(random.uniform(5.00, 500.00), 2)
        items.append((str(i), code, description, str(quantity), uom, f'${unit_price:.2f}'))
    return items


def generate_invoice(invoice_num: int, output_dir: str, used_vendors: set, used_po: set) -> dict:
    """Generate a single unique invoice PDF."""

    # Generate unique data
    po_number = generate_po_number()
    while po_number in used_po:
        po_number = generate_po_number()
    used_po.add(po_number)

    vendor_name = generate_vendor_name(used_vendors)
    vendor_address, vendor_phone = generate_vendor_address()

    # Create email from vendor name
    email_domain = vendor_name.split()[0].lower() + random.choice(['supply', 'parts', 'ind', 'mfg']) + '.com'
    vendor_email = f"orders@{email_domain}"

    order_date = generate_order_date()

    # Generate 2-7 line items
    line_count = random.randint(2, 7)
    used_item_codes = set()
    line_items = generate_line_items(line_count, used_item_codes)

    # Create PDF
    pdf = InvoicePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Invoice metadata
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, f'Order Date: {order_date}', ln=True)
    pdf.cell(0, 6, f'Purchase Order Number: {po_number}', ln=True)
    pdf.ln(10)

    # Vendor Information
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'VENDOR:', ln=True)
    pdf.set_font('Helvetica', '', 10)

    pdf.cell(0, 6, f'Vendor Name: {vendor_name}', ln=True)
    pdf.cell(0, 6, f'Vendor Address: {vendor_address}', ln=True)
    pdf.cell(0, 6, f'Vendor Phone Number: {vendor_phone}', ln=True)
    pdf.cell(0, 6, f'Vendor Email Address: {vendor_email}', ln=True)
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
    pdf.cell(28, 8, 'Line Number', border=1, fill=True, align='C')
    pdf.cell(35, 8, 'Item Code', border=1, fill=True, align='C')
    pdf.cell(55, 8, 'Description', border=1, fill=True, align='C')
    pdf.cell(32, 8, 'Quantity Shipped', border=1, fill=True, align='C')
    pdf.cell(15, 8, 'UOM', border=1, fill=True, align='C')
    pdf.cell(25, 8, 'Unit Price', border=1, fill=True, align='C')
    pdf.ln()
    pdf.set_text_color(0, 0, 0)

    # Line Items Data
    pdf.set_font('Helvetica', '', 9)
    for i, item in enumerate(line_items):
        if i % 2 == 0:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(28, 7, item[0], border=1, align='C', fill=True)
        pdf.cell(35, 7, item[1], border=1, align='C', fill=True)
        pdf.cell(55, 7, item[2], border=1, fill=True)
        pdf.cell(32, 7, item[3], border=1, align='C', fill=True)
        pdf.cell(15, 7, item[4], border=1, align='C', fill=True)
        pdf.cell(25, 7, item[5], border=1, align='R', fill=True)
        pdf.ln()

    pdf.ln(15)

    # Terms
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'Terms & Conditions:', ln=True)
    pdf.set_font('Helvetica', '', 10)
    payment_terms = random.choice(['Net 15', 'Net 30', 'Net 45', 'Net 60', '2/10 Net 30'])
    shipping_methods = ['UPS Ground', 'FedEx Ground', 'Freight', 'LTL Freight', 'Standard Delivery']
    pdf.cell(0, 6, f'Payment Terms: {payment_terms}', ln=True)
    pdf.cell(0, 6, f'Shipping Method: {random.choice(shipping_methods)}', ln=True)

    # Expected delivery 7-21 days from order date
    order_dt = datetime.strptime(order_date, "%Y-%m-%d")
    delivery_dt = order_dt + timedelta(days=random.randint(7, 21))
    pdf.cell(0, 6, f'Expected Delivery: {delivery_dt.strftime("%Y-%m-%d")}', ln=True)

    pdf.ln(15)

    # Notes
    pdf.set_font('Helvetica', 'I', 9)
    pdf.cell(0, 6, 'Please confirm receipt and expected ship date.', ln=True, align='C')
    pdf.cell(0, 6, 'Questions? Contact purchasing@example.com', ln=True, align='C')

    # Generate filename
    vendor_prefix = vendor_name.split()[0]
    po_short = po_number.replace('PO-', '').replace('-', '')
    filename = f"Invoice_{str(invoice_num).zfill(2)}_{vendor_prefix}_{po_short}.pdf"
    output_path = os.path.join(output_dir, filename)

    # Save
    pdf.output(output_path)

    return {
        'filename': filename,
        'po_number': po_number,
        'vendor_name': vendor_name,
        'line_count': line_count
    }


def main():
    """Generate 25 unique invoices."""
    output_dir = r"C:\RPAFiles\OCR_TEST\Samples"
    os.makedirs(output_dir, exist_ok=True)

    # Seed random with current time for additional entropy
    random.seed()

    # Track used values to prevent duplicates
    used_vendors = set()
    used_po = set()

    print("=" * 70)
    print("Generating 25 Unique Test Invoices")
    print("=" * 70)
    print(f"Output Directory: {output_dir}")
    print()

    invoices = []
    for i in range(1, 26):
        invoice = generate_invoice(i, output_dir, used_vendors, used_po)
        invoices.append(invoice)
        print(f"[{i:02d}] {invoice['filename']}")
        print(f"     PO: {invoice['po_number']} | Vendor: {invoice['vendor_name']} | Lines: {invoice['line_count']}")

    print()
    print("=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    print(f"Total invoices generated: {len(invoices)}")
    print(f"Unique PO numbers: {len(used_po)}")
    print(f"Unique vendor names: {len(used_vendors)}")

    # List all files
    files = os.listdir(output_dir)
    pdf_files = [f for f in files if f.endswith('.pdf')]
    print(f"PDF files in output directory: {len(pdf_files)}")
    print()
    print("Generation complete!")


if __name__ == "__main__":
    main()
