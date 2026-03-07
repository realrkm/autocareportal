"""
FILE: ServerModule1.py  (Server Module)
─────────────────────────────────────────────────────────────
In Anvil:
  1. Click "+" next to Server Modules in the left sidebar
  2. Name it "ServerModule1" (or any name you like)
  3. Paste this entire file into it

DATABASE TABLES REQUIRED  (App Tables → add these):
  ┌─────────────┬──────────────────────────────────────────────────────────────┐
  │ Table Name  │ Columns                                                      │
  ├─────────────┼──────────────────────────────────────────────────────────────┤
  │ jobs        │ job_ref(text), customer(link→customers), vehicle(link→        │
  │             │ vehicles), advisor(text), bay(text), checkin_date(date),      │
  │             │ checkin_time(text), mileage_in(number), fuel_level(text),     │
  │             │ exterior_condition(text), warning_lights(text),               │
  │             │ customer_complaint(text), service_type(text),                 │
  │             │ current_step(number), status(text)                            │
  ├─────────────┼──────────────────────────────────────────────────────────────┤
  │ customers   │ name(text), phone(text), email(text)                          │
  ├─────────────┼──────────────────────────────────────────────────────────────┤
  │ vehicles    │ plate(text), model(text)                                      │
  ├─────────────┼──────────────────────────────────────────────────────────────┤
  │ quotations  │ job(link→jobs), quote_ref(text), status(text), currency(text),│
  │             │ subtotal(number), discount(number), discount_label(text),     │
  │             │ tax(number), tax_label(text), grand_total(number),            │
  │             │ est_duration(text), approval_status(text)                     │
  ├─────────────┼──────────────────────────────────────────────────────────────┤
  │ quote_items │ quotation(link→quotations), description(text), item_type(text)│
  │             │ qty(text), unit_price(number), total(number)                  │
  ├─────────────┼──────────────────────────────────────────────────────────────┤
  │ service_log │ job(link→jobs), technician(text), start_date(text),           │
  │             │ est_completion(text), progress_pct(number), status(text)      │
  ├─────────────┼──────────────────────────────────────────────────────────────┤
  │ timeline    │ service(link→service_log), time_label(text), title(text),     │
  │             │ description(text), status(text), sort_order(number)           │
  ├─────────────┼──────────────────────────────────────────────────────────────┤
  │ tech_notes  │ service(link→service_log), note_text(text), color(text)       │
  ├─────────────┼──────────────────────────────────────────────────────────────┤
  │ invoices    │ job(link→jobs), invoice_ref(text), invoice_date(text),        │
  │             │ due_date(text), status(text), currency(text), subtotal(number)│
  │             │ discount(number), discount_label(text), tax(number),          │
  │             │ tax_label(text), total_due(number), biller_name(text),        │
  │             │ biller_pin(text), biller_address(text), biller_phone(text)    │
  ├─────────────┼──────────────────────────────────────────────────────────────┤
  │ invoice_    │ invoice(link→invoices), description(text), qty(text),         │
  │ items       │ unit_price(number), total(number)                             │
  ├─────────────┼──────────────────────────────────────────────────────────────┤
  │ payments    │ job(link→jobs), currency(text), balance(number),              │
  │             │ deposit_paid(number), status(text)                            │
  ├─────────────┼──────────────────────────────────────────────────────────────┤
  │ payment_    │ payment(link→payments), date(text), method(text),             │
  │ history     │ reference(text), amount(number), status(text)                 │
  └─────────────┴──────────────────────────────────────────────────────────────┘
─────────────────────────────────────────────────────────────
"""

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


# ════════════════════════════════════════════════════════════
#  MAIN PORTAL DATA FUNCTION
# ════════════════════════════════════════════════════════════

@anvil.server.callable
def get_portal_data(job_ref=None):
    """
    Returns the complete data dictionary for the client portal.
    If job_ref is None, returns the active job for the logged-in user.
    """

    # ── Get the job row
    if job_ref:
        job = app_tables.jobs.get(job_ref=job_ref)
    else:
        user = anvil.users.get_user()
        if not user:
            raise Exception("Not logged in and no job_ref provided.")
        # Get the most recent active job for this user's email
        jobs = app_tables.jobs.search(
            tables.order_by("checkin_date", ascending=False)
        )
        job = next((j for j in jobs if j['customer']['email'] == user['email']), None)

    if not job:
        raise Exception(f"No job found for ref: {job_ref}")

    customer = job['customer']
    vehicle = job['vehicle']

    # ── Get related records
    quotation = app_tables.quotations.get(job=job)
    service = app_tables.service_log.get(job=job)
    invoice = app_tables.invoices.get(job=job)
    payment = app_tables.payments.get(job=job)

    # ── Build and return the full data dict
    return {
        'current_step': job['current_step'] or 1,

        # ── CHECK-IN
        'checkin': {
            'job_ref':             job['job_ref'],
            'customer_name':       customer['name'],
            'customer_phone':      customer['phone'],
            'customer_email':      customer['email'],
            'vehicle_plate':       vehicle['plate'],
            'vehicle_model':       vehicle['model'],
            'checkin_date':        str(job['checkin_date']),
            'checkin_time':        job['checkin_time'] or '—',
            'advisor':             job['advisor'] or '—',
            'bay':                 job['bay'] or '—',
            'mileage':             f"{job['mileage_in']:,} km" if job['mileage_in'] else '—',
            'fuel_level':          job['fuel_level'] or '—',
            'exterior_condition':  job['exterior_condition'] or 'Not noted',
            'warning_lights':      job['warning_lights'] or 'None',
            'customer_complaint':  job['customer_complaint'] or 'No complaint recorded.',
            'service_type':        job['service_type'] or 'General Service',
        },

        # ── QUOTATION
        'quotation': _build_quotation(quotation) if quotation else _empty_quotation(),

        # ── SERVICE
        'service': _build_service(service) if service else _empty_service(),

        # ── INVOICE
        'invoice': _build_invoice(invoice) if invoice else _empty_invoice(),

        # ── PAYMENT
        'payment': _build_payment(payment) if payment else _empty_payment(),
    }


# ════════════════════════════════════════════════════════════
#  BUILDER HELPERS
# ════════════════════════════════════════════════════════════

def _build_quotation(qt):
    items = app_tables.quote_items.search(quotation=qt)
    status_map = {
        'Approved':        ('✓ Customer Approved', 'badge-orange'),
        'Pending':         ('⏳ Awaiting Approval', 'badge-blue'),
        'Rejected':        ('✗ Rejected',           'badge-red'),
    }
    label, badge_cls = status_map.get(qt['status'], (qt['status'], 'badge-blue'))
    return {
        'quote_ref':        qt['quote_ref'],
        'status':           label,
        'status_badge_class': badge_cls,
        'currency':         qt['currency'] or 'KSh',
        'subtotal':         qt['subtotal'] or 0,
        'discount':         qt['discount'] or 0,
        'discount_label':   qt['discount_label'] or 'Discount',
        'tax':              qt['tax'] or 0,
        'tax_label':        qt['tax_label'] or 'VAT',
        'grand_total':      qt['grand_total'] or 0,
        'est_duration':     qt['est_duration'] or '—',
        'approval_status':  qt['approval_status'] or '—',
        'items': [{
            'description': i['description'],
            'type':        i['item_type'],
            'qty':         i['qty'],
            'unit_price':  i['unit_price'] or 0,
            'total':       i['total'] or 0,
        } for i in items],
    }


def _build_service(sv):
    timeline_rows = app_tables.timeline.search(
        tables.order_by('sort_order', ascending=True), service=sv
    )
    notes_rows = app_tables.tech_notes.search(service=sv)
    status_map = {
        'In Progress': ('⚡ In Progress', 'badge-accent'),
        'Completed':   ('✓ Completed',   'badge-green'),
        'On Hold':     ('⏸ On Hold',     'badge-orange'),
    }
    label, badge_cls = status_map.get(sv['status'], (sv['status'], 'badge-blue'))
    return {
        'technician':         sv['technician'] or '—',
        'start_date':         sv['start_date'] or '—',
        'est_completion':     sv['est_completion'] or '—',
        'progress_pct':       sv['progress_pct'] or 0,
        'status_label':       label,
        'status_badge_class': badge_cls,
        'timeline': [{
            'time_label':  t['time_label'],
            'title':       t['title'],
            'description': t['description'],
            'status':      t['status'],  # 'done' | 'active' | 'pending'
        } for t in timeline_rows],
        'notes': [{
            'text':  n['note_text'],
            'color': n['color'] or 'blue',
        } for n in notes_rows],
    }


def _build_invoice(inv):
    items = app_tables.invoice_items.search(invoice=inv)
    status_map = {
        'Pending Payment': ('⏳ Pending Payment', 'badge-orange'),
        'Paid':            ('✓ Paid',             'badge-green'),
        'Overdue':         ('⚠ Overdue',          'badge-red'),
    }
    label, badge_cls = status_map.get(inv['status'], (inv['status'], 'badge-blue'))
    return {
        'invoice_ref':        inv['invoice_ref'],
        'invoice_date':       inv['invoice_date'] or '—',
        'due_date':           inv['due_date'] or '—',
        'billed_to':          inv['job']['customer']['name'],
        'status_label':       label,
        'status_badge_class': badge_cls,
        'currency':           inv['currency'] or 'KSh',
        'subtotal':           inv['subtotal'] or 0,
        'discount':           inv['discount'] or 0,
        'discount_label':     inv['discount_label'] or 'Discount',
        'tax':                inv['tax'] or 0,
        'tax_label':          inv['tax_label'] or 'VAT',
        'total_due':          inv['total_due'] or 0,
        'biller_name':        inv['biller_name'] or '—',
        'biller_pin':         inv['biller_pin'] or '—',
        'biller_address':     inv['biller_address'] or '—',
        'biller_phone':       inv['biller_phone'] or '—',
        'items': [{
            'description': i['description'],
            'qty':         i['qty'],
            'unit_price':  i['unit_price'] or 0,
            'total':       i['total'] or 0,
        } for i in items],
    }


def _build_payment(pay):
    history_rows = app_tables.payment_history.search(
        tables.order_by('date', ascending=False), payment=pay
    )
    status_map = {
        'Unpaid':          ('Unpaid',     'badge-red'),
        'Partial':         ('Partial',    'badge-orange'),
        'Paid':            ('✓ Paid',     'badge-green'),
    }
    label, badge_cls = status_map.get(pay['status'], (pay['status'], 'badge-blue'))
    return {
        'currency':           pay['currency'] or 'KSh',
        'balance':            pay['balance'] or 0,
        'deposit_paid':       pay['deposit_paid'] or 0,
        'status_label':       label,
        'status_badge_class': badge_cls,
        'methods': [
            {
                'name':         'M-PESA',
                'icon':         '📱',
                'description':  'Paybill · Instant',
                'instructions': '📱 <strong>M-PESA Paybill:</strong> Business No. <strong style="color:var(--accent)">400200</strong> — Account No. <strong style="color:var(--accent)">' + (pay['job']['job_ref']) + '</strong>',
            },
            {
                'name':         'Bank Transfer',
                'icon':         '🏦',
                'description':  'KCB · 1–2 days',
                'instructions': '🏦 <strong>Bank:</strong> KCB Bank · A/C: <strong style="color:var(--accent)">1234567890</strong> · Branch: Industrial Area',
            },
            {
                'name':         'Visa / Mastercard',
                'icon':         '💳',
                'description':  'Card payment · Instant',
                'instructions': None,  # handled via redirect_url in initiate_payment
            },
            {
                'name':         'Cash',
                'icon':         '🤝',
                'description':  'At the garage counter',
                'instructions': '🤝 <strong>Cash:</strong> Please visit our reception. Open Mon–Sat 7:30 AM – 6:00 PM.',
            },
        ],
        'history': [{
            'date':      h['date'],
            'method':    h['method'],
            'reference': h['reference'],
            'amount':    h['amount'] or 0,
            'status':    h['status'],
        } for h in history_rows],
    }


# ════════════════════════════════════════════════════════════
#  EMPTY / PLACEHOLDER STATES  (if records don't exist yet)
# ════════════════════════════════════════════════════════════

def _empty_quotation():
    return {'quote_ref': '—', 'status': 'Not yet generated', 'status_badge_class': 'badge-blue',
            'currency': 'KSh', 'subtotal': 0, 'discount': 0, 'discount_label': 'Discount',
            'tax': 0, 'tax_label': 'VAT', 'grand_total': 0, 'est_duration': '—',
            'approval_status': '—', 'items': []}

def _empty_service():
    return {'technician': '—', 'start_date': '—', 'est_completion': '—', 'progress_pct': 0,
            'status_label': 'Not Started', 'status_badge_class': 'badge-blue',
            'timeline': [], 'notes': []}

def _empty_invoice():
    return {'invoice_ref': '—', 'invoice_date': '—', 'due_date': '—', 'billed_to': '—',
            'status_label': 'Not yet generated', 'status_badge_class': 'badge-blue',
            'currency': 'KSh', 'subtotal': 0, 'discount': 0, 'discount_label': 'Discount',
            'tax': 0, 'tax_label': 'VAT', 'total_due': 0,
            'biller_name': '—', 'biller_pin': '—', 'biller_address': '—', 'biller_phone': '—',
            'items': []}

def _empty_payment():
    return {'currency': 'KSh', 'balance': 0, 'deposit_paid': 0,
            'status_label': '—', 'status_badge_class': 'badge-blue',
            'methods': [], 'history': []}


# ════════════════════════════════════════════════════════════
#  PAYMENT INITIATION
# ════════════════════════════════════════════════════════════

@anvil.server.callable
def initiate_payment(job_ref, method):
    """
    Called when customer clicks 'Pay Now'.
    Integrate your actual payment gateway here.

    Should return:
      { 'success': True, 'message': '...', 'redirect_url': '...' }
    """
    job = app_tables.jobs.get(job_ref=job_ref)
    payment = app_tables.payments.get(job=job)

    if not job or not payment:
        raise Exception("Job or payment record not found.")

    amount = payment['balance']

    if method == 'M-PESA':
        # TODO: Integrate Daraja API (Safaricom M-PESA STK Push)
        # from .mpesa_integration import stk_push
        # result = stk_push(phone=job['customer']['phone'], amount=amount, ref=job_ref)
        return {
            'success': True,
            'message': 'M-PESA STK Push sent to your phone. Enter your PIN to complete.',
            'redirect_url': None,
        }

    elif method == 'Visa / Mastercard':
        # TODO: Integrate Stripe / Flutterwave / Pesapal
        # from .stripe_integration import create_checkout_session
        # session = create_checkout_session(amount=amount, ref=job_ref)
        return {
            'success': True,
            'message': 'Redirecting to card payment...',
            'redirect_url': 'https://checkout.stripe.com/YOUR_SESSION_ID',  # Replace with real URL
        }

    elif method == 'Bank Transfer':
        return {
            'success': True,
            'message': 'Bank details sent to your email. Payment confirmed within 1–2 days.',
            'redirect_url': None,
        }

    elif method == 'Cash':
        return {
            'success': True,
            'message': 'Please visit the garage reception to complete cash payment.',
            'redirect_url': None,
        }

    else:
        raise Exception(f"Unknown payment method: {method}")


# ════════════════════════════════════════════════════════════
#  OPTIONAL: SEED DEMO DATA  (run once for testing)
# ════════════════════════════════════════════════════════════

@anvil.server.callable
def seed_demo_data():
    """
    Call this ONCE from the Anvil console to populate demo data:
      anvil.server.call('seed_demo_data')
    """
    # Create customer
    customer = app_tables.customers.add_row(
        name='James Odhiambo',
        phone='+254 722 448 091',
        email='james.o@email.com'
    )
    # Create vehicle
    vehicle = app_tables.vehicles.add_row(
        plate='KDA 472K',
        model='Toyota Land Cruiser V8 · 2019'
    )
    # Create job
    import datetime
    job = app_tables.jobs.add_row(
        job_ref='GRG-2024-4471',
        customer=customer,
        vehicle=vehicle,
        advisor='Brian Mutua',
        bay='Bay 04',
        checkin_date=datetime.date(2025, 3, 3),
        checkin_time='08:47 AM',
        mileage_in=87342,
        fuel_level='¾ Full',
        exterior_condition='Minor scratches (noted)',
        warning_lights='Engine · Service',
        customer_complaint='Engine making a knocking sound at idle, AC not cooling well, and the car hesitates when accelerating from a stop.',
        service_type='Repair + Maintenance',
        current_step=3,
        status='In Progress'
    )
    # Create quotation
    qt = app_tables.quotations.add_row(
        job=job,
        quote_ref='QT-2024-4471',
        status='Approved',
        currency='KSh',
        subtotal=42800,
        discount=2140,
        discount_label='Loyalty Discount (5%)',
        tax=6505.60,
        tax_label='VAT (16%)',
        grand_total=47165.60,
        est_duration='3 days',
        approval_status='Approved'
    )
    for item in [
        ('Engine Oil — Mobil 1 5W-30 (Full Synthetic)', 'Parts',   '6L',  800,   4800),
        ('Oil Filter Replacement',                       'Parts',   '1',   650,   650),
        ('AC Gas Recharge (R134a)',                      'Service', '1',   4500,  4500),
        ('AC Compressor Belt',                           'Parts',   '1',   3200,  3200),
        ('Injector Cleaning Service',                    'Service', '1',   7000,  7000),
        ('Spark Plugs — NGK Iridium (Set of 8)',         'Parts',   '8',   1200,  9600),
        ('Diagnostic Scan & Report',                     'Labour',  '1',   2500,  2500),
        ('Labour — Engine & AC',                         'Labour',  '1',   10550, 10550),
    ]:
        app_tables.quote_items.add_row(
            quotation=qt, description=item[0], item_type=item[1],
            qty=item[2], unit_price=item[3], total=item[4]
        )
    # Create service log
    sv = app_tables.service_log.add_row(
        job=job,
        technician='Moses Karanja',
        start_date='03 Mar · 11:00 AM',
        est_completion='05 Mar · 5:00 PM',
        progress_pct=65,
        status='In Progress'
    )
    for i, tl in enumerate([
        ('03 Mar · 11:00 AM', 'Diagnostic Scan Completed',     'Full OBD-II scan run. Found fault codes P0300 and P0715.', 'done'),
        ('03 Mar · 1:30 PM',  'Spark Plugs Replaced',          'All 8 NGK Iridium spark plugs replaced. Coils checked.', 'done'),
        ('04 Mar · 9:00 AM',  'Oil & Filter Change Done',      'Drained old oil. Replaced with Mobil 1 5W-30.',          'done'),
        ('04 Mar · 11:30 AM', 'Injector Cleaning Underway',    'Ultrasonic injector cleaning in progress.',              'active'),
        ('Scheduled — 05 Mar','AC Recharge & Belt Replacement','AC compressor belt replacement and R134a recharge.',     'pending'),
    ]):
        app_tables.timeline.add_row(service=sv, time_label=tl[0], title=tl[1], description=tl[2], status=tl[3], sort_order=i)
    app_tables.tech_notes.add_row(service=sv, note_text='🔩 Injector #3 and #6 showing 18% flow variance — cleaning expected to resolve.', color='blue')
    app_tables.tech_notes.add_row(service=sv, note_text='⚠️ Front-right tyre pressure dropping. Recommend valve stem replacement (KSh 350).', color='orange')
    # Create invoice
    inv = app_tables.invoices.add_row(
        job=job,
        invoice_ref='INV-2024-4471',
        invoice_date='05 Mar 2025',
        due_date='12 Mar 2025',
        status='Pending Payment',
        currency='KSh',
        subtotal=42800,
        discount=2140,
        discount_label='Loyalty Discount (5%)',
        tax=6505.60,
        tax_label='VAT (16%)',
        total_due=47165.60,
        biller_name='AutoCare Garage Ltd.',
        biller_pin='P051234567X',
        biller_address='Industrial Area, Nairobi',
        biller_phone='+254 700 000 100'
    )
    for item in [
        ('Engine Oil — Mobil 1 5W-30 6L + Filter', '1 set', 5450,  5450),
        ('AC Gas Recharge + Compressor Belt',        '1',     7700,  7700),
        ('Injector Cleaning Service',                '1',     7000,  7000),
        ('Spark Plugs — NGK Iridium × 8',           '8',     1200,  9600),
        ('Diagnostic Scan & Report',                 '1',     2500,  2500),
        ('Labour — Engine, Injectors & AC',          '1',     10550, 10550),
    ]:
        app_tables.invoice_items.add_row(
            invoice=inv, description=item[0], qty=item[1],
            unit_price=item[2], total=item[3]
        )
    # Create payment
    pay = app_tables.payments.add_row(
        job=job,
        currency='KSh',
        balance=37165.60,
        deposit_paid=10000,
        status='Partial'
    )
    app_tables.payment_history.add_row(
        payment=pay,
        date='03 Mar 2025',
        method='M-PESA',
        reference='RGX9K2HH1',
        amount=10000,
        status='Confirmed'
    )
    return "Demo data seeded successfully!"