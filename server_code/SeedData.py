import anvil.users
"""
FILE: SeedData.py  (Server Module)
═══════════════════════════════════════════════════════════════════
PURPOSE
  Standalone server module that clears and repopulates all 12 app
  tables with realistic dummy data covering every stage of the
  garage workflow.

HOW TO USE
  Option A — Anvil Console (quickest):
      anvil.server.call('seed_all_data')

  Option B — from any client form:
      result = anvil.server.call('seed_all_data')
      anvil.alert(result['message'])

  Option C — clear only, no re-seed:
      anvil.server.call('clear_all_data')

  Option D — seed a single specific job:
      anvil.server.call('seed_job', job_index=2)   # 0-based, 0–4

JOBS INCLUDED (5 total, one per workflow stage)
  #1  GRG-2025-0001  James Odhiambo      → Stage 3: In Service   (65% done)
  #2  GRG-2025-0002  Amina Hassan         → Stage 5: Paid         (complete)
  #3  GRG-2025-0003  David Kimani         → Stage 1: Just Checked In
  #4  GRG-2025-0004  Grace Wanjiku        → Stage 2: Quotation Pending Approval
  #5  GRG-2025-0005  Peter Otieno         → Stage 4: Invoice / Awaiting Payment

TABLES SEEDED
  customers · vehicles · jobs · quotations · quote_items
  service_log · timeline · tech_notes · invoices · invoice_items
  payments · payment_history
═══════════════════════════════════════════════════════════════════
"""

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime
import random
import string


# ════════════════════════════════════════════════════════════════
#  UTILITY HELPERS
# ════════════════════════════════════════════════════════════════

def _rand_ref(prefix, length=6):
    """Generate a random alphanumeric reference suffix."""
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def _clear_table(tbl):
    """Delete every row in a table safely."""
    for row in tbl.search():
        row.delete()


# ════════════════════════════════════════════════════════════════
#  PUBLIC: CLEAR ALL DATA
# ════════════════════════════════════════════════════════════════

@anvil.server.callable
def clear_all_data():
    """
    Deletes every row from all 12 garage tables.
    Safe to call before re-seeding or during development.
    """
    # Delete child tables first (foreign keys point upward)
    _clear_table(app_tables.payment_history)
    _clear_table(app_tables.payments)
    _clear_table(app_tables.invoice_items)
    _clear_table(app_tables.invoices)
    _clear_table(app_tables.tech_notes)
    _clear_table(app_tables.timeline)
    _clear_table(app_tables.service_log)
    _clear_table(app_tables.quote_items)
    _clear_table(app_tables.quotations)
    _clear_table(app_tables.jobs)
    _clear_table(app_tables.vehicles)
    _clear_table(app_tables.customers)
    return {'success': True, 'message': 'All tables cleared.'}


# ════════════════════════════════════════════════════════════════
#  PUBLIC: SEED ALL DATA
# ════════════════════════════════════════════════════════════════

@anvil.server.callable
def seed_all_data(clear_first=True):
    """
    Populates all tables with 5 realistic dummy garage jobs.

    Parameters
    ----------
    clear_first : bool
        If True (default), clears all tables before seeding.
        Set to False to append without clearing.

    Returns
    -------
    dict  { 'success': bool, 'message': str, 'job_refs': list }
    """
    if clear_first:
        clear_all_data()

    created_refs = []
    for i in range(5):
        ref = _seed_single_job(i)
        created_refs.append(ref)

    return {
        'success': True,
        'message': f'Successfully seeded {len(created_refs)} jobs: {", ".join(created_refs)}',
        'job_refs': created_refs
    }


# ════════════════════════════════════════════════════════════════
#  PUBLIC: SEED A SINGLE JOB BY INDEX
# ════════════════════════════════════════════════════════════════

@anvil.server.callable
def seed_job(job_index=0):
    """
    Seeds a single job by index (0–4) without clearing other data.
    Useful for testing one specific workflow stage.
    """
    if job_index < 0 or job_index > 4:
        raise ValueError("job_index must be 0–4")
    ref = _seed_single_job(job_index)
    return {'success': True, 'message': f'Seeded job: {ref}', 'job_ref': ref}


# ════════════════════════════════════════════════════════════════
#  MASTER JOB DEFINITIONS
# ════════════════════════════════════════════════════════════════

# Shared garage info used across all invoices
GARAGE = {
    'name':    'AutoCare Garage Ltd.',
    'pin':     'P051234567X',
    'address': 'Industrial Area, Lusaka Road, Nairobi',
    'phone':   '+254 700 000 100',
    'currency': 'KSh',
}

JOBS_DATA = [

    # ──────────────────────────────────────────────────────────
    # JOB 0 ·  James Odhiambo  ·  Stage 3: IN SERVICE (65%)
    # ──────────────────────────────────────────────────────────
    {
        'job_ref': 'GRG-2025-0001',
        'current_step': 3,
        'job_status': 'In Progress',

        'customer': {
            'name':  'James Odhiambo',
            'phone': '+254 722 448 091',
            'email': 'james.odhiambo@email.com',
        },
        'vehicle': {
            'plate': 'KDA 472K',
            'model': 'Toyota Land Cruiser V8 · 2019',
        },
        'checkin': {
            'date':               datetime.date(2025, 3, 3),
            'time':               '08:47 AM',
            'advisor':            'Brian Mutua',
            'bay':                'Bay 04',
            'mileage_in':         87342,
            'fuel_level':         '¾ Full',
            'exterior_condition': 'Minor scratches (noted)',
            'warning_lights':     'Engine · Service',
            'complaint':          'Engine making a knocking sound at idle. AC not cooling. Hesitates when accelerating from a stop.',
            'service_type':       'Repair + Maintenance',
        },
        'quotation': {
            'quote_ref':       'QT-2025-0001',
            'status':          'Approved',
            'est_duration':    '3 days',
            'approval_status': 'Approved',
            'discount':        2140,
            'discount_label':  'Loyalty Discount (5%)',
            'tax_rate':        0.16,
            'tax_label':       'VAT (16%)',
            'items': [
                ('Engine Oil — Mobil 1 5W-30 (Full Synthetic)', 'Parts',   '6L',    800,   4800),
                ('Oil Filter Replacement',                       'Parts',   '1',     650,    650),
                ('AC Gas Recharge (R134a)',                      'Service', '1',    4500,   4500),
                ('AC Compressor Belt',                           'Parts',   '1',    3200,   3200),
                ('Injector Cleaning Service',                    'Service', '1',    7000,   7000),
                ('Spark Plugs — NGK Iridium (Set of 8)',         'Parts',   '8',    1200,   9600),
                ('Diagnostic Scan & Report',                     'Labour',  '1',    2500,   2500),
                ('Labour — Engine & AC',                         'Labour',  '1',   10550,  10550),
            ],
        },
        'service': {
            'technician':    'Moses Karanja',
            'start_date':    '03 Mar · 11:00 AM',
            'est_completion':'05 Mar · 5:00 PM',
            'progress_pct':  65,
            'status':        'In Progress',
            'timeline': [
                ('03 Mar · 11:00 AM', 'Diagnostic Scan Completed',     'Full OBD-II scan. Fault codes P0300 (random misfire) and P0715 found.', 'done'),
                ('03 Mar · 1:30 PM',  'Spark Plugs Replaced',          'All 8 NGK Iridium spark plugs replaced. Coils inspected — all within spec.', 'done'),
                ('04 Mar · 9:00 AM',  'Oil & Filter Change Completed', 'Old oil drained (dark, 11,000 km overdue). Mobil 1 5W-30 installed.', 'done'),
                ('04 Mar · 11:30 AM', 'Injector Cleaning Underway',    'Ultrasonic injector cleaning in progress. Flow rate testing ongoing.', 'active'),
                ('Scheduled — 05 Mar','AC Recharge & Belt Replacement','Compressor belt replacement then R134a recharge and pressure test.', 'pending'),
            ],
            'notes': [
                ('🔩 Injector #3 and #6 showing 18% flow variance — cleaning expected to resolve. Will retest before reinstalling.', 'blue'),
                ('⚠️ Additional finding: Front-right tyre pressure consistently dropping. Recommend valve stem replacement (KSh 350) — requires customer approval.', 'orange'),
            ],
        },
        'invoice': {
            'invoice_ref':  'INV-2025-0001',
            'invoice_date': '05 Mar 2025',
            'due_date':     '12 Mar 2025',
            'status':       'Pending Payment',
            'items': [
                ('Engine Oil — Mobil 1 5W-30 6L + Filter', '1 set', 5450, 5450),
                ('AC Gas Recharge + Compressor Belt',        '1',    7700, 7700),
                ('Injector Cleaning Service',                '1',    7000, 7000),
                ('Spark Plugs — NGK Iridium × 8',           '8',    1200, 9600),
                ('Diagnostic Scan & Report',                 '1',    2500, 2500),
                ('Labour — Engine, Injectors & AC',          '1',   10550,10550),
            ],
            'discount':       2140,
            'discount_label': 'Loyalty Discount (5%)',
            'tax_rate':       0.16,
            'tax_label':      'VAT (16%)',
        },
        'payment': {
            'status':       'Partial',
            'deposit_paid': 10000,
            'history': [
                ('03 Mar 2025', 'M-PESA', 'RGX9K2HH1', 10000, 'Confirmed'),
            ],
        },
    },

    # ──────────────────────────────────────────────────────────
    # JOB 1 ·  Amina Hassan  ·  Stage 5: FULLY PAID
    # ──────────────────────────────────────────────────────────
    {
        'job_ref': 'GRG-2025-0002',
        'current_step': 5,
        'job_status': 'Completed',

        'customer': {
            'name':  'Amina Hassan',
            'phone': '+254 733 912 004',
            'email': 'amina.hassan@gmail.com',
        },
        'vehicle': {
            'plate': 'KBZ 017T',
            'model': 'Nissan X-Trail · 2017',
        },
        'checkin': {
            'date':               datetime.date(2025, 2, 17),
            'time':               '09:15 AM',
            'advisor':            'Carol Njeri',
            'bay':                'Bay 02',
            'mileage_in':         61820,
            'fuel_level':         'Half',
            'exterior_condition': 'Good — no visible damage',
            'warning_lights':     'None',
            'complaint':          'Routine 60,000 km service. Brakes feel spongy. Wipers streaking.',
            'service_type':       'Scheduled Maintenance',
        },
        'quotation': {
            'quote_ref':       'QT-2025-0002',
            'status':          'Approved',
            'est_duration':    '1 day',
            'approval_status': 'Approved',
            'discount':        0,
            'discount_label':  '',
            'tax_rate':        0.16,
            'tax_label':       'VAT (16%)',
            'items': [
                ('60,000 km Full Service Package',     'Service', '1',   8500,   8500),
                ('Brake Fluid Flush',                   'Service', '1',   2200,   2200),
                ('Brake Pads — Front Set (OEM)',        'Parts',   '1',   5500,   5500),
                ('Wiper Blades — Pair',                 'Parts',   '1',    900,    900),
                ('Air Filter Replacement',              'Parts',   '1',   1200,   1200),
                ('Cabin Filter Replacement',            'Parts',   '1',    850,    850),
                ('Labour — Service & Brakes',           'Labour',  '1',   4500,   4500),
            ],
        },
        'service': {
            'technician':    'Alex Mwangi',
            'start_date':    '17 Feb · 9:30 AM',
            'est_completion':'17 Feb · 5:00 PM',
            'progress_pct':  100,
            'status':        'Completed',
            'timeline': [
                ('17 Feb · 9:30 AM',  'Vehicle Received & Inspected',  'Pre-service inspection completed. All noted items confirmed.', 'done'),
                ('17 Feb · 10:00 AM', '60,000 km Service Performed',   'Oil, filter, air filter, cabin filter all replaced per schedule.', 'done'),
                ('17 Feb · 12:30 PM', 'Brake System Serviced',         'Front brake pads replaced. Brake fluid flushed and topped up.', 'done'),
                ('17 Feb · 2:00 PM',  'Wipers & Final Checks Done',    'Wiper blades replaced. Road test performed — all systems normal.', 'done'),
                ('17 Feb · 4:30 PM',  'Vehicle Ready for Collection',  'Customer notified via SMS. Vehicle washed and waiting.', 'done'),
            ],
            'notes': [
                ('✅ All service items completed within schedule. Vehicle collected by customer at 5:10 PM on 17 Feb 2025.', 'green'),
            ],
        },
        'invoice': {
            'invoice_ref':  'INV-2025-0002',
            'invoice_date': '17 Feb 2025',
            'due_date':     '17 Feb 2025',
            'status':       'Paid',
            'items': [
                ('60,000 km Full Service Package',  '1',    8500, 8500),
                ('Brake Fluid Flush',                '1',    2200, 2200),
                ('Brake Pads — Front Set (OEM)',     '1',    5500, 5500),
                ('Wiper Blades — Pair',              '1',     900,  900),
                ('Air Filter + Cabin Filter',        '1',    2050, 2050),
                ('Labour — Service & Brakes',        '1',    4500, 4500),
            ],
            'discount':       0,
            'discount_label': '',
            'tax_rate':       0.16,
            'tax_label':      'VAT (16%)',
        },
        'payment': {
            'status':       'Paid',
            'deposit_paid': 0,
            'history': [
                ('17 Feb 2025', 'Visa Card', 'VSA7731KE92', 27081, 'Confirmed'),
            ],
        },
    },

    # ──────────────────────────────────────────────────────────
    # JOB 2 ·  David Kimani  ·  Stage 1: JUST CHECKED IN
    # ──────────────────────────────────────────────────────────
    {
        'job_ref': 'GRG-2025-0003',
        'current_step': 1,
        'job_status': 'Checked In',

        'customer': {
            'name':  'David Kimani',
            'phone': '+254 710 333 456',
            'email': 'david.kimani@outlook.com',
        },
        'vehicle': {
            'plate': 'KCJ 881B',
            'model': 'Subaru Forester XT · 2015',
        },
        'checkin': {
            'date':               datetime.date(2025, 3, 7),
            'time':               '07:55 AM',
            'advisor':            'Brian Mutua',
            'bay':                'Pending Assignment',
            'mileage_in':         134500,
            'fuel_level':         'Quarter',
            'exterior_condition': 'Dent on rear bumper (pre-existing, photographed)',
            'warning_lights':     'Check Engine · AWD',
            'complaint':          'Strong vibration above 80 km/h. Check engine light on for 2 weeks. Grinding noise when reversing.',
            'service_type':       'Diagnosis & Repair',
        },
        'quotation':  None,  # Not yet generated
        'service':    None,
        'invoice':    None,
        'payment':    None,
    },

    # ──────────────────────────────────────────────────────────
    # JOB 3 ·  Grace Wanjiku  ·  Stage 2: QUOTATION PENDING
    # ──────────────────────────────────────────────────────────
    {
        'job_ref': 'GRG-2025-0004',
        'current_step': 2,
        'job_status': 'Awaiting Approval',

        'customer': {
            'name':  'Grace Wanjiku',
            'phone': '+254 744 205 877',
            'email': 'grace.wanjiku@yahoo.com',
        },
        'vehicle': {
            'plate': 'KDD 553P',
            'model': 'Honda CR-V · 2020',
        },
        'checkin': {
            'date':               datetime.date(2025, 3, 5),
            'time':               '10:30 AM',
            'advisor':            'Carol Njeri',
            'bay':                'Bay 07',
            'mileage_in':         42100,
            'fuel_level':         'Full',
            'exterior_condition': 'Excellent — no damage',
            'warning_lights':     'TPMS',
            'complaint':          'Tyre pressure warning light on. Unusual noise from front suspension over bumps. Wants full inspection before long road trip.',
            'service_type':       'Inspection & Repair',
        },
        'quotation': {
            'quote_ref':       'QT-2025-0004',
            'status':          'Pending',
            'est_duration':    '2 days',
            'approval_status': 'Awaiting Customer',
            'discount':        0,
            'discount_label':  '',
            'tax_rate':        0.16,
            'tax_label':       'VAT (16%)',
            'items': [
                ('Full Pre-Trip Vehicle Inspection',     'Service', '1',   3500,   3500),
                ('TPMS Sensor Replacement (Front Left)', 'Parts',   '1',   4200,   4200),
                ('Front Shock Absorbers — Pair (OEM)',   'Parts',   '1',  18000,  18000),
                ('Wheel Alignment & Balancing',          'Service', '1',   2800,   2800),
                ('Tyre Rotation',                        'Service', '1',    800,    800),
                ('Labour — Suspension & Alignment',      'Labour',  '1',   6500,   6500),
            ],
        },
        'service':  None,
        'invoice':  None,
        'payment':  None,
    },

    # ──────────────────────────────────────────────────────────
    # JOB 4 ·  Peter Otieno  ·  Stage 4: INVOICE ISSUED
    # ──────────────────────────────────────────────────────────
    {
        'job_ref': 'GRG-2025-0005',
        'current_step': 4,
        'job_status': 'Awaiting Payment',

        'customer': {
            'name':  'Peter Otieno',
            'phone': '+254 725 661 990',
            'email': 'p.otieno@ke.business.com',
        },
        'vehicle': {
            'plate': 'KCU 114G',
            'model': 'Mitsubishi Outlander · 2018',
        },
        'checkin': {
            'date':               datetime.date(2025, 2, 28),
            'time':               '02:10 PM',
            'advisor':            'Brian Mutua',
            'bay':                'Bay 01',
            'mileage_in':         77900,
            'fuel_level':         'Half',
            'exterior_condition': 'Cracked windscreen (driver side — noted)',
            'warning_lights':     'Battery · Service',
            'complaint':          'Car not starting reliably. Battery warning light. Wants windscreen replaced if affordable.',
            'service_type':       'Electrical & Body Repair',
        },
        'quotation': {
            'quote_ref':       'QT-2025-0005',
            'status':          'Approved',
            'est_duration':    '2 days',
            'approval_status': 'Approved',
            'discount':        1500,
            'discount_label':  'Corporate Discount',
            'tax_rate':        0.16,
            'tax_label':       'VAT (16%)',
            'items': [
                ('Car Battery — Amaron 65Ah',          'Parts',   '1',   7500,   7500),
                ('Alternator Belt Replacement',         'Parts',   '1',   2200,   2200),
                ('Windscreen Replacement (OEM Grade)',  'Parts',   '1',  22000,  22000),
                ('Electrical System Diagnostic',        'Service', '1',   2500,   2500),
                ('Labour — Electrical & Windscreen',    'Labour',  '1',   5800,   5800),
            ],
        },
        'service': {
            'technician':    'Moses Karanja',
            'start_date':    '01 Mar · 8:00 AM',
            'est_completion':'02 Mar · 4:00 PM',
            'progress_pct':  100,
            'status':        'Completed',
            'timeline': [
                ('01 Mar · 8:00 AM',  'Electrical Diagnostic Run',      'Battery load test failed (35% capacity). Alternator belt cracked — confirmed cause.', 'done'),
                ('01 Mar · 10:30 AM', 'Battery & Belt Replaced',        'Amaron 65Ah fitted. Alternator belt replaced. Charging voltage confirmed at 14.2V.', 'done'),
                ('01 Mar · 2:00 PM',  'Windscreen Removal Started',     'Old windscreen removed. Frame cleaned and inspected — no rust damage.', 'done'),
                ('02 Mar · 9:00 AM',  'New Windscreen Fitted & Cured',  'OEM-grade windscreen bonded. 4-hour cure time observed before road test.', 'done'),
                ('02 Mar · 3:30 PM',  'Road Test & Quality Check Done', 'All systems normal. No leaks. Invoice generated and sent to customer.', 'done'),
            ],
            'notes': [
                ('✅ All work completed. Vehicle ready for collection pending payment.', 'green'),
            ],
        },
        'invoice': {
            'invoice_ref':  'INV-2025-0005',
            'invoice_date': '02 Mar 2025',
            'due_date':     '09 Mar 2025',
            'status':       'Pending Payment',
            'items': [
                ('Car Battery — Amaron 65Ah',        '1',  7500,  7500),
                ('Alternator Belt',                   '1',  2200,  2200),
                ('Windscreen Replacement (OEM Grade)','1', 22000, 22000),
                ('Electrical Diagnostic',             '1',  2500,  2500),
                ('Labour — Electrical & Windscreen',  '1',  5800,  5800),
            ],
            'discount':       1500,
            'discount_label': 'Corporate Discount',
            'tax_rate':       0.16,
            'tax_label':      'VAT (16%)',
        },
        'payment': {
            'status':       'Unpaid',
            'deposit_paid': 0,
            'history':      [],
        },
    },
]


# ════════════════════════════════════════════════════════════════
#  INTERNAL: SEED A SINGLE JOB
# ════════════════════════════════════════════════════════════════

def _seed_single_job(index):
    """Seeds one complete job record by index. Returns the job_ref."""
    d = JOBS_DATA[index]

    # ── 1. CUSTOMER
    customer = app_tables.customers.add_row(**d['customer'])

    # ── 2. VEHICLE
    vehicle = app_tables.vehicles.add_row(**d['vehicle'])

    # ── 3. JOB (check-in)
    ci = d['checkin']
    job = app_tables.jobs.add_row(
        job_ref=           d['job_ref'],
        customer=          customer,
        vehicle=           vehicle,
        advisor=           ci['advisor'],
        bay=               ci['bay'],
        checkin_date=      ci['date'],
        checkin_time=      ci['time'],
        mileage_in=        ci['mileage_in'],
        fuel_level=        ci['fuel_level'],
        exterior_condition=ci['exterior_condition'],
        warning_lights=    ci['warning_lights'],
        customer_complaint=ci['complaint'],
        service_type=      ci['service_type'],
        current_step=      d['current_step'],
        status=            d['job_status'],
    )

    # ── 4. QUOTATION (optional)
    qt_data = d.get('quotation')
    if qt_data:
        raw_items   = qt_data['items']
        subtotal    = sum(item[4] for item in raw_items)
        discount    = qt_data['discount']
        tax_rate    = qt_data['tax_rate']
        after_disc  = subtotal - discount
        tax_amount  = round(after_disc * tax_rate, 2)
        grand_total = round(after_disc + tax_amount, 2)

        qt = app_tables.quotations.add_row(
            job=             job,
            quote_ref=       qt_data['quote_ref'],
            status=          qt_data['status'],
            currency=        GARAGE['currency'],
            subtotal=        subtotal,
            discount=        discount,
            discount_label=  qt_data['discount_label'],
            tax=             tax_amount,
            tax_label=       qt_data['tax_label'],
            grand_total=     grand_total,
            est_duration=    qt_data['est_duration'],
            approval_status= qt_data['approval_status'],
        )
        for item in raw_items:
            app_tables.quote_items.add_row(
                quotation=  qt,
                description=item[0],
                item_type=  item[1],
                qty=        item[2],
                unit_price= item[3],
                total=      item[4],
            )

    # ── 5. SERVICE LOG + TIMELINE + NOTES (optional)
    sv_data = d.get('service')
    if sv_data:
        sv = app_tables.service_log.add_row(
            job=            job,
            technician=     sv_data['technician'],
            start_date=     sv_data['start_date'],
            est_completion= sv_data['est_completion'],
            progress_pct=   sv_data['progress_pct'],
            status=         sv_data['status'],
        )
        for sort_order, tl in enumerate(sv_data['timeline']):
            app_tables.timeline.add_row(
                service=    sv,
                time_label= tl[0],
                title=      tl[1],
                description=tl[2],
                status=     tl[3],
                sort_order= sort_order,
            )
        for note in sv_data.get('notes', []):
            app_tables.tech_notes.add_row(
                service=   sv,
                note_text= note[0],
                color=     note[1],
            )

    # ── 6. INVOICE + INVOICE ITEMS (optional)
    inv_data = d.get('invoice')
    if inv_data:
        raw_items   = inv_data['items']
        subtotal    = sum(item[3] for item in raw_items)
        discount    = inv_data['discount']
        tax_rate    = inv_data['tax_rate']
        after_disc  = subtotal - discount
        tax_amount  = round(after_disc * tax_rate, 2)
        total_due   = round(after_disc + tax_amount, 2)

        inv = app_tables.invoices.add_row(
            job=            job,
            invoice_ref=    inv_data['invoice_ref'],
            invoice_date=   inv_data['invoice_date'],
            due_date=       inv_data['due_date'],
            status=         inv_data['status'],
            currency=       GARAGE['currency'],
            subtotal=       subtotal,
            discount=       discount,
            discount_label= inv_data['discount_label'],
            tax=            tax_amount,
            tax_label=      inv_data['tax_label'],
            total_due=      total_due,
            biller_name=    GARAGE['name'],
            biller_pin=     GARAGE['pin'],
            biller_address= GARAGE['address'],
            biller_phone=   GARAGE['phone'],
        )
        for item in raw_items:
            app_tables.invoice_items.add_row(
                invoice=    inv,
                description=item[0],
                qty=        item[1],
                unit_price= item[2],
                total=      item[3],
            )

    # ── 7. PAYMENT + PAYMENT HISTORY (optional)
    pay_data = d.get('payment')
    if pay_data:
        # Calculate balance from invoice if available
        if inv_data:
            balance = round(total_due - pay_data['deposit_paid'], 2)
        else:
            balance = 0

        pay = app_tables.payments.add_row(
            job=          job,
            currency=     GARAGE['currency'],
            balance=      balance,
            deposit_paid= pay_data['deposit_paid'],
            status=       pay_data['status'],
        )
        for h in pay_data.get('history', []):
            app_tables.payment_history.add_row(
                payment=   pay,
                date=      h[0],
                method=    h[1],
                reference= h[2],
                amount=    h[3],
                status=    h[4],
            )

    return d['job_ref']


# ════════════════════════════════════════════════════════════════
#  BONUS: QUICK STATUS REPORT
# ════════════════════════════════════════════════════════════════

@anvil.server.callable
def get_seed_status():
    """
    Returns a quick summary of what's currently in the database.
    Useful to verify seeding worked correctly.

    Usage:
        result = anvil.server.call('get_seed_status')
        print(result['summary'])
    """
    jobs = list(app_tables.jobs.search())
    summary_lines = [f"{'─'*50}", f"  DATABASE STATUS REPORT", f"{'─'*50}"]
    summary_lines.append(f"  Total jobs:           {len(jobs)}")
    summary_lines.append(f"  Total customers:      {len(list(app_tables.customers.search()))}")
    summary_lines.append(f"  Total vehicles:       {len(list(app_tables.vehicles.search()))}")
    summary_lines.append(f"  Total quote items:    {len(list(app_tables.quote_items.search()))}")
    summary_lines.append(f"  Total timeline rows:  {len(list(app_tables.timeline.search()))}")
    summary_lines.append(f"  Total invoice items:  {len(list(app_tables.invoice_items.search()))}")
    summary_lines.append(f"  Total payment rows:   {len(list(app_tables.payment_history.search()))}")
    summary_lines.append(f"{'─'*50}")
    summary_lines.append(f"  JOBS:")
    for job in jobs:
        summary_lines.append(
            f"    {job['job_ref']}  |  Step {job['current_step']}/5  "
            f"|  {job['status']:<22}  |  {job['customer']['name']}"
        )
    summary_lines.append(f"{'─'*50}")
    summary = '\n'.join(summary_lines)
    return {
        'summary': summary,
        'job_count': len(jobs),
        'jobs': [{'ref': j['job_ref'], 'step': j['current_step'], 'status': j['status']} for j in jobs]
    }