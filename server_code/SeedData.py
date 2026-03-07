"""
FILE: SeedData.py  (Server Module)
════════════════════════════════════════════════════════════════
Seed data with multiple jobs per customer. Each of the 5 customers
now has 2-3 historical jobs showing a complete service journey.

Quick start in the Anvil console:
  anvil.server.call('seed_all_data')
  anvil.server.call('get_seed_status')
════════════════════════════════════════════════════════════════
"""

import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
import datetime


GARAGE = {
    'name':     'AutoCare Garage Ltd.',
    'pin':      'P051234567X',
    'address':  'Industrial Area, Lusaka Road, Nairobi',
    'phone':    '+254 700 000 100',
    'currency': 'KSh',
}


# ════════════════════════════════════════════════════════════════
#  PUBLIC API
# ════════════════════════════════════════════════════════════════

@anvil.server.callable
def seed_all_data(clear_first=True):
    if clear_first:
        clear_all_data()
    refs = []
    for d in JOBS_DATA:
        refs.append(_do_seed(d))
    total = len(refs)
    return {
        'success': True,
        'message': f'Seeded {total} jobs across {len(set(d["customer"]["email"] for d in JOBS_DATA))} customers.',
        'job_refs': refs
    }


@anvil.server.callable
def clear_all_data():
    for t in [app_tables.payment_history, app_tables.payments,
              app_tables.invoice_items, app_tables.invoices,
              app_tables.tech_notes, app_tables.timeline,
              app_tables.service_log, app_tables.quote_items,
              app_tables.quotations, app_tables.jobs,
              app_tables.vehicles, app_tables.customers]:
        for row in t.search():
            row.delete()
    return {'success': True, 'message': 'All tables cleared.'}


@anvil.server.callable
def get_seed_status():
    jobs = list(app_tables.jobs.search(tables.order_by('job_ref', ascending=True)))
    customers = list(app_tables.customers.search())
    lines = [f'  Customers: {len(customers)}', f'  Jobs: {len(jobs)}', '']
    for j in jobs:
        lines.append(f'    {j["job_ref"]}  Step {j["current_step"]}/5  {j["status"]:<22}  {j["customer"]["name"]}')
    return {
        'summary': '\n'.join(lines),
        'jobs': [{'ref': j['job_ref'], 'step': j['current_step'], 'status': j['status'], 'customer': j['customer']['name']} for j in jobs]
    }


# ════════════════════════════════════════════════════════════════
#  MASTER DATA — 5 customers × 2-3 jobs each = 13 jobs total
# ════════════════════════════════════════════════════════════════

JOBS_DATA = [

    # ══════════════════════════════════════════════════════
    #  CUSTOMER 1: James Odhiambo  (3 jobs)
    # ══════════════════════════════════════════════════════

    # Job A — Historical (fully paid, 2024)
    {
        'job_ref': 'GRG-2024-0012',
        'current_step': 5,
        'job_status': 'Completed',
        'customer': {'name': 'James Odhiambo', 'phone': '+254 722 448 091', 'email': 'james.odhiambo@email.com'},
        'vehicle':  {'plate': 'KDA 472K', 'model': 'Toyota Land Cruiser V8 · 2019'},
        'checkin': {
            'date': datetime.date(2024, 9, 10), 'time': '09:15 AM',
            'advisor': 'Brian Mutua', 'bay': 'Bay 02',
            'mileage_in': 74820, 'fuel_level': '½ Full',
            'exterior_condition': 'Good condition',
            'warning_lights': 'None',
            'complaint': 'Scheduled 75,000 km service. Also requesting wheel alignment check.',
            'service_type': 'Scheduled Service',
        },
        'quotation': {
            'quote_ref': 'QT-2024-0041', 'status': 'Approved', 'approval_status': 'Approved',
            'est_duration': '4 hrs', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Engine Oil 5W-40 (8L)',       'Parts',   '8',  850,  6800),
                ('Oil Filter',                  'Parts',   '1',  850,   850),
                ('Air Filter',                  'Parts',   '1', 1200,  1200),
                ('Fuel Filter',                 'Parts',   '1',  950,   950),
                ('Transmission Fluid (4L)',     'Parts',   '4', 1100,  4400),
                ('75K Service Labour',          'Labour',  '1', 4500,  4500),
                ('Wheel Alignment',             'Service', '1', 2200,  2200),
                ('Tyre Rotation',               'Service', '1',  800,   800),
            ],
        },
        'service': {
            'technician': 'Kelvin Waweru', 'start_date': '10 Sep 2024', 'est_completion': '10 Sep 2024',
            'progress_pct': 100, 'status': 'Completed',
            'timeline': [
                ('09:30 AM', 'Vehicle Received',          'KDA 472K checked in. Oil level and coolant noted as low.', 'done'),
                ('10:00 AM', 'Oil & Filter Change',       'Drained 8L old oil. New 5W-40 and filter fitted.', 'done'),
                ('11:30 AM', 'Transmission Service',      'Flushed and refilled transmission fluid. Adjusted gear linkage.', 'done'),
                ('01:00 PM', 'Wheel Alignment & Tyres',   'Alignment set to spec. Tyres rotated front-rear.', 'done'),
                ('02:30 PM', 'Road Test & Sign-off',      'No issues. Vehicle handed back to customer.', 'done'),
            ],
        },
        'invoice': {
            'invoice_ref': 'INV-2024-0041', 'invoice_date': '10 Sep 2024', 'due_date': '10 Sep 2024',
            'status': 'Paid', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Engine Oil 5W-40 (8L)',       '8',  850,  6800),
                ('Oil Filter',                  '1',  850,   850),
                ('Air Filter',                  '1', 1200,  1200),
                ('Fuel Filter',                 '1',  950,   950),
                ('Transmission Fluid (4L)',     '4', 1100,  4400),
                ('75K Service Labour',          '1', 4500,  4500),
                ('Wheel Alignment',             '1', 2200,  2200),
                ('Tyre Rotation',               '1',  800,   800),
            ],
        },
        'payment': {
            'deposit_paid': 21700, 'status': 'Paid',
            'history': [
                ('10 Sep 2024', 'M-PESA', 'QGH44891023', 21700, 'Confirmed'),
            ],
        },
    },

    # Job B — Recent (in service, current)
    {
        'job_ref': 'GRG-2025-0001',
        'current_step': 3,
        'job_status': 'In Progress',
        'customer': {'name': 'James Odhiambo', 'phone': '+254 722 448 091', 'email': 'james.odhiambo@email.com'},
        'vehicle':  {'plate': 'KDA 472K', 'model': 'Toyota Land Cruiser V8 · 2019'},
        'checkin': {
            'date': datetime.date(2025, 3, 3), 'time': '08:47 AM',
            'advisor': 'Brian Mutua', 'bay': 'Bay 04',
            'mileage_in': 87342, 'fuel_level': '¾ Full',
            'exterior_condition': 'Minor scratches (noted)',
            'warning_lights': 'Engine · Service',
            'complaint': 'Engine light on. Rough idle at cold start. Possible injector issue.',
            'service_type': 'Diagnostics & Repair',
        },
        'quotation': {
            'quote_ref': 'QT-2025-0001', 'status': 'Approved', 'approval_status': 'In Progress',
            'est_duration': '2 days', 'discount': 2500, 'discount_label': 'Loyalty Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('OBD-II Full Diagnostics',                  'Service', '1', 3500,   3500),
                ('Fuel Injector Cleaning (4 injectors)',     'Service', '4', 2800,  11200),
                ('Spark Plugs × 8 (Iridium)',                'Parts',   '8', 1450,  11600),
                ('Throttle Body Cleaning',                   'Service', '1', 2200,   2200),
                ('Engine Bay Cleaning',                      'Service', '1', 1800,   1800),
            ],
        },
        'service': {
            'technician': 'Kelvin Waweru', 'start_date': '03 Mar 2025', 'est_completion': '05 Mar 2025',
            'progress_pct': 65, 'status': 'In Progress',
            'timeline': [
                ('03 Mar · 09:00 AM', 'Diagnostics Scan',     'OBD-II scan complete. P0300 random misfire + P0171 lean bank 1 detected.', 'done'),
                ('03 Mar · 11:30 AM', 'Injector Removal',     'All 4 injectors removed. Heavy carbon deposit found on #3 and #4.', 'done'),
                ('04 Mar · 08:00 AM', 'Injector Cleaning',    'Ultrasonic cleaning in progress. Flow testing underway.', 'active'),
                ('04 Mar · 02:00 PM', 'Reinstall & Tune',     'Reinstall injectors and remap idle parameters.', 'pending'),
                ('05 Mar · 10:00 AM', 'Road Test & Sign-off', 'Extended road test to confirm misfire resolved.', 'pending'),
            ],
            'notes': [
                ('⚠️ Additional: Front-right tyre pressure dropping consistently. Valve stem replacement (KSh 350) recommended — requires customer approval.', 'orange'),
            ],
        },
    },

    # ══════════════════════════════════════════════════════
    #  CUSTOMER 2: Amina Hassan  (3 jobs)
    # ══════════════════════════════════════════════════════

    # Job A — Historical (paid, 2024)
    {
        'job_ref': 'GRG-2024-0007',
        'current_step': 5,
        'job_status': 'Completed',
        'customer': {'name': 'Amina Hassan', 'phone': '+254 711 892 034', 'email': 'amina.hassan@gmail.com'},
        'vehicle':  {'plate': 'KBZ 881M', 'model': 'Subaru Forester XT · 2018'},
        'checkin': {
            'date': datetime.date(2024, 7, 22), 'time': '10:00 AM',
            'advisor': 'Susan Kamau', 'bay': 'Bay 01',
            'mileage_in': 53100, 'fuel_level': 'Full',
            'exterior_condition': 'Good condition',
            'warning_lights': 'None',
            'complaint': 'Brake pedal feels soft. Squeaking sound from front brakes.',
            'service_type': 'Brake Service',
        },
        'quotation': {
            'quote_ref': 'QT-2024-0028', 'status': 'Approved', 'approval_status': 'Approved',
            'est_duration': '3 hrs', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Front Brake Pads (set)',        'Parts',   '1', 4800,  4800),
                ('Brake Fluid DOT4 (500ml)',      'Parts',   '2',  950,  1900),
                ('Brake Fluid Flush & Bleed',     'Service', '1', 2500,  2500),
                ('Brake Caliper Inspection',      'Service', '1', 1200,  1200),
            ],
        },
        'service': {
            'technician': 'Joseph Mwangi', 'start_date': '22 Jul 2024', 'est_completion': '22 Jul 2024',
            'progress_pct': 100, 'status': 'Completed',
            'timeline': [
                ('10:30 AM', 'Wheel Removal',        'All 4 wheels removed. Front brake pads at 2mm — critical.', 'done'),
                ('11:00 AM', 'Pad Replacement',      'New EBC Greenstuff pads fitted front. Rotors measured OK.', 'done'),
                ('12:30 PM', 'Fluid Flush',          'Old DOT4 drained. System bled and refilled.', 'done'),
                ('01:00 PM', 'Test & Return',        'Pedal feel firm. Road test complete. Returned to customer.', 'done'),
            ],
        },
        'invoice': {
            'invoice_ref': 'INV-2024-0028', 'invoice_date': '22 Jul 2024', 'due_date': '22 Jul 2024',
            'status': 'Paid', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Front Brake Pads (set)',     '1', 4800,  4800),
                ('Brake Fluid DOT4 (500ml)',   '2',  950,  1900),
                ('Brake Fluid Flush & Bleed',  '1', 2500,  2500),
                ('Brake Caliper Inspection',   '1', 1200,  1200),
            ],
        },
        'payment': {
            'deposit_paid': 12064, 'status': 'Paid',
            'history': [('22 Jul 2024', 'Visa', 'VISA-7731-AMNA', 12064, 'Confirmed')],
        },
    },

    # Job B — Completed & Paid (2025)
    {
        'job_ref': 'GRG-2025-0002',
        'current_step': 5,
        'job_status': 'Completed',
        'customer': {'name': 'Amina Hassan', 'phone': '+254 711 892 034', 'email': 'amina.hassan@gmail.com'},
        'vehicle':  {'plate': 'KBZ 881M', 'model': 'Subaru Forester XT · 2018'},
        'checkin': {
            'date': datetime.date(2025, 2, 14), 'time': '07:30 AM',
            'advisor': 'Susan Kamau', 'bay': 'Bay 03',
            'mileage_in': 60200, 'fuel_level': '¼ Full',
            'exterior_condition': 'Good condition',
            'warning_lights': 'None',
            'complaint': '60,000 km service due. Requesting gearbox oil change and AC regas.',
            'service_type': 'Major Service',
        },
        'quotation': {
            'quote_ref': 'QT-2025-0002', 'status': 'Approved', 'approval_status': 'Approved',
            'est_duration': '1 day', 'discount': 1500, 'discount_label': 'Returning Customer',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Engine Oil 5W-30 Synthetic (6L)', 'Parts',   '6', 1100,  6600),
                ('Oil Filter',                       'Parts',   '1',  750,   750),
                ('Gearbox Oil GL-5 (3L)',            'Parts',   '3', 1400,  4200),
                ('AC Refrigerant R134a',             'Parts',   '1', 3200,  3200),
                ('60K Labour Package',               'Labour',  '1', 5500,  5500),
                ('AC Regas & Leak Test',             'Service', '1', 3500,  3500),
            ],
        },
        'service': {
            'technician': 'Joseph Mwangi', 'start_date': '14 Feb 2025', 'est_completion': '14 Feb 2025',
            'progress_pct': 100, 'status': 'Completed',
            'timeline': [
                ('07:45 AM', 'Vehicle Received',      'KBZ 881M logged in. AC barely cooling noted on arrival.', 'done'),
                ('08:30 AM', 'Oil & Filter Change',   'Drained old oil. New synthetic 5W-30 and filter installed.', 'done'),
                ('10:00 AM', 'Gearbox Service',       'Gearbox oil drained and refilled with GL-5. No metal shavings found.', 'done'),
                ('11:30 AM', 'AC Regas',              'Old R134a recovered. System leak-tested OK. Recharged to spec.', 'done'),
                ('01:00 PM', 'QC & Return',           'All systems checked. Cold AC confirmed. Road test passed.', 'done'),
            ],
            'notes': [('✅ All service items completed within schedule. Vehicle collected by customer at 5:10 PM.', 'green')],
        },
        'invoice': {
            'invoice_ref': 'INV-2025-0002', 'invoice_date': '14 Feb 2025', 'due_date': '14 Feb 2025',
            'status': 'Paid', 'discount': 1500, 'discount_label': 'Returning Customer',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Engine Oil 5W-30 Synthetic (6L)', '6', 1100,  6600),
                ('Oil Filter',                       '1',  750,   750),
                ('Gearbox Oil GL-5 (3L)',            '3', 1400,  4200),
                ('AC Refrigerant R134a',             '1', 3200,  3200),
                ('60K Labour Package',               '1', 5500,  5500),
                ('AC Regas & Leak Test',             '1', 3500,  3500),
            ],
        },
        'payment': {
            'deposit_paid': 27842, 'status': 'Paid',
            'history': [('14 Feb 2025', 'Visa', 'VISA-9921-AMH', 27842, 'Confirmed')],
        },
    },

    # Job C — New, pending quote
    {
        'job_ref': 'GRG-2025-0007',
        'current_step': 2,
        'job_status': 'Quotation Pending',
        'customer': {'name': 'Amina Hassan', 'phone': '+254 711 892 034', 'email': 'amina.hassan@gmail.com'},
        'vehicle':  {'plate': 'KBZ 881M', 'model': 'Subaru Forester XT · 2018'},
        'checkin': {
            'date': datetime.date(2025, 3, 6), 'time': '11:00 AM',
            'advisor': 'Susan Kamau', 'bay': 'Pending',
            'mileage_in': 60980, 'fuel_level': '½ Full',
            'exterior_condition': 'Minor dent on rear bumper (noted)',
            'warning_lights': 'AWD System',
            'complaint': 'AWD light on after heavy rain. Occasional shudder when turning.',
            'service_type': 'AWD Diagnostics',
        },
        'quotation': {
            'quote_ref': 'QT-2025-0007', 'status': 'Pending', 'approval_status': 'Awaiting Customer',
            'est_duration': '1–2 days', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('AWD System Diagnostics',           'Service', '1', 4500,  4500),
                ('Front LSD / Coupling Inspection',  'Service', '1', 3500,  3500),
                ('Differential Oil Front (2L)',       'Parts',   '2', 1300,  2600),
                ('Labour — AWD Disassembly',         'Labour',  '1', 6000,  6000),
            ],
        },
    },

    # ══════════════════════════════════════════════════════
    #  CUSTOMER 3: David Kimani  (2 jobs)
    # ══════════════════════════════════════════════════════

    # Job A — Historical
    {
        'job_ref': 'GRG-2024-0019',
        'current_step': 5,
        'job_status': 'Completed',
        'customer': {'name': 'David Kimani', 'phone': '+254 733 201 774', 'email': 'david.kimani@outlook.com'},
        'vehicle':  {'plate': 'KCC 034J', 'model': 'Nissan X-Trail T32 · 2017'},
        'checkin': {
            'date': datetime.date(2024, 11, 5), 'time': '08:00 AM',
            'advisor': 'Brian Mutua', 'bay': 'Bay 01',
            'mileage_in': 81000, 'fuel_level': '½ Full',
            'exterior_condition': 'Good condition',
            'warning_lights': 'None',
            'complaint': 'Knocking noise from front suspension over speed bumps.',
            'service_type': 'Suspension Repair',
        },
        'quotation': {
            'quote_ref': 'QT-2024-0071', 'status': 'Approved', 'approval_status': 'Approved',
            'est_duration': '5 hrs', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Front Strut Mounts × 2',    'Parts',  '2', 3800,  7600),
                ('Front Stabiliser Links × 2', 'Parts', '2', 2200,  4400),
                ('Suspension Labour',         'Labour', '1', 5500,  5500),
                ('Wheel Alignment Post-repair','Service','1', 2200,  2200),
            ],
        },
        'service': {
            'technician': 'Kelvin Waweru', 'start_date': '05 Nov 2024', 'est_completion': '05 Nov 2024',
            'progress_pct': 100, 'status': 'Completed',
            'timeline': [
                ('08:30 AM', 'Lift & Inspect',       'Both front strut mounts cracked. Stabiliser links loose.', 'done'),
                ('09:00 AM', 'Parts Replacement',    'New strut mounts and stabiliser links fitted both sides.', 'done'),
                ('12:00 PM', 'Wheel Alignment',      'Alignment corrected post-repair. Within manufacturer spec.', 'done'),
                ('01:00 PM', 'Road Test',            'Knocking eliminated. Test complete.', 'done'),
            ],
        },
        'invoice': {
            'invoice_ref': 'INV-2024-0071', 'invoice_date': '05 Nov 2024', 'due_date': '05 Nov 2024',
            'status': 'Paid', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Front Strut Mounts × 2',    '2', 3800,  7600),
                ('Front Stabiliser Links × 2', '2', 2200,  4400),
                ('Suspension Labour',         '1', 5500,  5500),
                ('Wheel Alignment Post-repair','1', 2200,  2200),
            ],
        },
        'payment': {
            'deposit_paid': 23026, 'status': 'Paid',
            'history': [('05 Nov 2024', 'Bank Transfer', 'EFT-KCB-00991', 23026, 'Confirmed')],
        },
    },

    # Job B — New, just checked in
    {
        'job_ref': 'GRG-2025-0003',
        'current_step': 1,
        'job_status': 'Checked In',
        'customer': {'name': 'David Kimani', 'phone': '+254 733 201 774', 'email': 'david.kimani@outlook.com'},
        'vehicle':  {'plate': 'KCC 034J', 'model': 'Nissan X-Trail T32 · 2017'},
        'checkin': {
            'date': datetime.date(2025, 3, 5), 'time': '07:50 AM',
            'advisor': 'Brian Mutua', 'bay': 'Pending Assignment',
            'mileage_in': 87900, 'fuel_level': '¼ Full',
            'exterior_condition': 'Body good. Cracked windscreen (pre-existing, customer aware)',
            'warning_lights': 'None',
            'complaint': 'CVT gearbox hesitating on hills. Transmission warning showed once then cleared.',
            'service_type': 'Transmission Check',
        },
    },

    # ══════════════════════════════════════════════════════
    #  CUSTOMER 4: Grace Wanjiku  (2 jobs)
    # ══════════════════════════════════════════════════════

    # Job A — Historical (paid, 2024)
    {
        'job_ref': 'GRG-2024-0031',
        'current_step': 5,
        'job_status': 'Completed',
        'customer': {'name': 'Grace Wanjiku', 'phone': '+254 700 331 928', 'email': 'grace.wanjiku@yahoo.com'},
        'vehicle':  {'plate': 'KDH 207Y', 'model': 'Honda CR-V 1.5T · 2020'},
        'checkin': {
            'date': datetime.date(2024, 12, 2), 'time': '10:30 AM',
            'advisor': 'Susan Kamau', 'bay': 'Bay 03',
            'mileage_in': 28500, 'fuel_level': '¾ Full',
            'exterior_condition': 'Excellent condition',
            'warning_lights': 'None',
            'complaint': 'Routine 30,000 km first service.',
            'service_type': 'Scheduled Service',
        },
        'quotation': {
            'quote_ref': 'QT-2024-0112', 'status': 'Approved', 'approval_status': 'Approved',
            'est_duration': '3 hrs', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Engine Oil 0W-20 Full Synthetic (5L)', 'Parts',  '5', 1300, 6500),
                ('Oil Filter',                           'Parts',  '1',  650,  650),
                ('Cabin Air Filter',                     'Parts',  '1',  900,  900),
                ('30K Service Labour',                   'Labour', '1', 3000, 3000),
                ('Multi-point Inspection',               'Service','1', 1500, 1500),
            ],
        },
        'service': {
            'technician': 'Samuel Ochieng', 'start_date': '02 Dec 2024', 'est_completion': '02 Dec 2024',
            'progress_pct': 100, 'status': 'Completed',
            'timeline': [
                ('10:45 AM', 'Oil & Filter',      'Full synthetic 0W-20 fitted. Old oil disposed.', 'done'),
                ('11:30 AM', 'Cabin Filter',      'Old cabin filter heavily clogged. Replaced.', 'done'),
                ('12:00 PM', 'Inspection',        'Brakes, suspension, lights all within spec.', 'done'),
                ('12:45 PM', 'Final Check',       'Stamped service book. Returned to customer.', 'done'),
            ],
        },
        'invoice': {
            'invoice_ref': 'INV-2024-0112', 'invoice_date': '02 Dec 2024', 'due_date': '02 Dec 2024',
            'status': 'Paid', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Engine Oil 0W-20 Full Synthetic (5L)', '5', 1300, 6500),
                ('Oil Filter',                           '1',  650,  650),
                ('Cabin Air Filter',                     '1',  900,  900),
                ('30K Service Labour',                   '1', 3000, 3000),
                ('Multi-point Inspection',               '1', 1500, 1500),
            ],
        },
        'payment': {
            'deposit_paid': 14994, 'status': 'Paid',
            'history': [('02 Dec 2024', 'M-PESA', 'QJK22910083', 14994, 'Confirmed')],
        },
    },

    # Job B — Quotation awaiting approval
    {
        'job_ref': 'GRG-2025-0004',
        'current_step': 2,
        'job_status': 'Quotation Pending',
        'customer': {'name': 'Grace Wanjiku', 'phone': '+254 700 331 928', 'email': 'grace.wanjiku@yahoo.com'},
        'vehicle':  {'plate': 'KDH 207Y', 'model': 'Honda CR-V 1.5T · 2020'},
        'checkin': {
            'date': datetime.date(2025, 3, 4), 'time': '09:00 AM',
            'advisor': 'Susan Kamau', 'bay': 'Bay 02',
            'mileage_in': 41200, 'fuel_level': '½ Full',
            'exterior_condition': 'Good condition',
            'warning_lights': 'TPMS',
            'complaint': 'Tyre pressure warning. Right rear tyre losing air overnight.',
            'service_type': 'Tyre & Inspection',
        },
        'quotation': {
            'quote_ref': 'QT-2025-0004', 'status': 'Pending', 'approval_status': 'Awaiting Customer',
            'est_duration': '2 hrs', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Tyre Puncture Repair',         'Service', '1', 1200, 1200),
                ('TPMS Sensor Replacement (RR)', 'Parts',   '1', 3800, 3800),
                ('Nitrogen Fill All 4 Tyres',    'Service', '1',  800,  800),
            ],
        },
    },

    # ══════════════════════════════════════════════════════
    #  CUSTOMER 5: Peter Otieno  (3 jobs)
    # ══════════════════════════════════════════════════════

    # Job A — Historical (paid, mid-2024)
    {
        'job_ref': 'GRG-2024-0005',
        'current_step': 5,
        'job_status': 'Completed',
        'customer': {'name': 'Peter Otieno', 'phone': '+254 720 551 338', 'email': 'peter.otieno@gmail.com'},
        'vehicle':  {'plate': 'KDE 990G', 'model': 'Mazda CX-5 2.0 · 2021'},
        'checkin': {
            'date': datetime.date(2024, 6, 18), 'time': '08:30 AM',
            'advisor': 'Brian Mutua', 'bay': 'Bay 05',
            'mileage_in': 31000, 'fuel_level': 'Full',
            'exterior_condition': 'Good condition',
            'warning_lights': 'None',
            'complaint': 'Squealing from belt area at startup. Gets better after warm-up.',
            'service_type': 'Belt & Tensioner',
        },
        'quotation': {
            'quote_ref': 'QT-2024-0018', 'status': 'Approved', 'approval_status': 'Approved',
            'est_duration': '3 hrs', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Serpentine Belt',         'Parts',  '1', 2800, 2800),
                ('Belt Tensioner Assembly', 'Parts',  '1', 4200, 4200),
                ('Idler Pulley',            'Parts',  '1', 1900, 1900),
                ('Labour — Belt System',    'Labour', '1', 3500, 3500),
            ],
        },
        'service': {
            'technician': 'Samuel Ochieng', 'start_date': '18 Jun 2024', 'est_completion': '18 Jun 2024',
            'progress_pct': 100, 'status': 'Completed',
            'timeline': [
                ('09:00 AM', 'Belt Inspection', 'Serpentine belt glazed and cracking. Tensioner seized.', 'done'),
                ('09:30 AM', 'Replacement',     'New belt, tensioner and idler pulley fitted.', 'done'),
                ('11:00 AM', 'Test',            'No squealing. Belt tension correct. Returned.', 'done'),
            ],
        },
        'invoice': {
            'invoice_ref': 'INV-2024-0018', 'invoice_date': '18 Jun 2024', 'due_date': '18 Jun 2024',
            'status': 'Paid', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Serpentine Belt',         '1', 2800, 2800),
                ('Belt Tensioner Assembly', '1', 4200, 4200),
                ('Idler Pulley',            '1', 1900, 1900),
                ('Labour — Belt System',    '1', 3500, 3500),
            ],
        },
        'payment': {
            'deposit_paid': 16624, 'status': 'Paid',
            'history': [('18 Jun 2024', 'Cash', 'CASH-2024-0018', 16624, 'Confirmed')],
        },
    },

    # Job B — Invoice issued, awaiting payment
    {
        'job_ref': 'GRG-2025-0005',
        'current_step': 4,
        'job_status': 'Invoice Issued',
        'customer': {'name': 'Peter Otieno', 'phone': '+254 720 551 338', 'email': 'peter.otieno@gmail.com'},
        'vehicle':  {'plate': 'KDE 990G', 'model': 'Mazda CX-5 2.0 · 2021'},
        'checkin': {
            'date': datetime.date(2025, 3, 1), 'time': '11:00 AM',
            'advisor': 'Brian Mutua', 'bay': 'Bay 05',
            'mileage_in': 49800, 'fuel_level': '½ Full',
            'exterior_condition': 'Good condition',
            'warning_lights': 'None',
            'complaint': '50,000 km service. Coolant reservoir low. Possible small leak.',
            'service_type': 'Major Service + Cooling',
        },
        'quotation': {
            'quote_ref': 'QT-2025-0005', 'status': 'Approved', 'approval_status': 'Approved',
            'est_duration': '1 day', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Engine Oil 5W-30 (5L)',       'Parts',   '5', 1100,  5500),
                ('Oil Filter',                  'Parts',   '1',  700,   700),
                ('Coolant G12+ (2L)',            'Parts',   '2', 1200,  2400),
                ('Coolant Flush & Fill',        'Service', '1', 2000,  2000),
                ('Cooling System Pressure Test','Service', '1', 1500,  1500),
                ('50K Labour Package',          'Labour',  '1', 4500,  4500),
            ],
        },
        'service': {
            'technician': 'Samuel Ochieng', 'start_date': '01 Mar 2025', 'est_completion': '02 Mar 2025',
            'progress_pct': 100, 'status': 'Completed',
            'timeline': [
                ('01 Mar · 11:30 AM', 'Oil Service',         'New 5W-30 and filter fitted.', 'done'),
                ('01 Mar · 01:00 PM', 'Cooling System',      'Small leak found at lower radiator hose clamp. Tightened + coolant flushed.', 'done'),
                ('02 Mar · 09:00 AM', 'Pressure Test',       '45-min pressure test — no further leaks detected.', 'done'),
                ('02 Mar · 03:30 PM', 'Road Test & QC Done', 'All systems normal. No leaks. Invoice generated and sent to customer.', 'done'),
            ],
            'notes': [('ℹ️ Recommend radiator replacement within next 20,000 km — early signs of core corrosion noted.', 'blue')],
        },
        'invoice': {
            'invoice_ref': 'INV-2025-0005', 'invoice_date': '02 Mar 2025', 'due_date': '09 Mar 2025',
            'status': 'Issued', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('Engine Oil 5W-30 (5L)',       '5', 1100,  5500),
                ('Oil Filter',                  '1',  700,   700),
                ('Coolant G12+ (2L)',            '2', 1200,  2400),
                ('Coolant Flush & Fill',        '1', 2000,  2000),
                ('Cooling System Pressure Test','1', 1500,  1500),
                ('50K Labour Package',          '1', 4500,  4500),
            ],
        },
        'payment': {
            'deposit_paid': 5000, 'status': 'Partial',
            'history': [('01 Mar 2025', 'Cash', 'CASH-2025-DEP', 5000, 'Confirmed')],
        },
    },

    # Job C — New, awaiting full payment (second vehicle)
    {
        'job_ref': 'GRG-2025-0008',
        'current_step': 2,
        'job_status': 'Quotation Pending',
        'customer': {'name': 'Peter Otieno', 'phone': '+254 720 551 338', 'email': 'peter.otieno@gmail.com'},
        'vehicle':  {'plate': 'KBQ 441T', 'model': 'Toyota Vitz · 2015'},
        'checkin': {
            'date': datetime.date(2025, 3, 6), 'time': '03:00 PM',
            'advisor': 'Susan Kamau', 'bay': 'Bay 01',
            'mileage_in': 112000, 'fuel_level': '¼ Full',
            'exterior_condition': 'High mileage, minor rust on door sills (noted)',
            'warning_lights': 'VSC · Check Engine',
            'complaint': 'Wife\'s car. VSC and check engine on. Also hesitates at idle.',
            'service_type': 'Diagnostics',
        },
        'quotation': {
            'quote_ref': 'QT-2025-0008', 'status': 'Pending', 'approval_status': 'Awaiting Customer',
            'est_duration': '1 day', 'discount': 0, 'discount_label': 'Discount',
            'tax_rate': 0.16, 'tax_label': 'VAT (16%)',
            'items': [
                ('OBD-II Diagnostics Scan',     'Service', '1', 3500,  3500),
                ('Mass Airflow Sensor (MAF)',    'Parts',   '1', 4200,  4200),
                ('Throttle Body Clean',         'Service', '1', 2000,  2000),
                ('Labour — Diagnostics',        'Labour',  '1', 3000,  3000),
            ],
        },
    },

]


# ════════════════════════════════════════════════════════════════
#  INTERNAL SEEDER
# ════════════════════════════════════════════════════════════════

def _do_seed(d):
    """Seeds one complete job. Reuses existing customer if email matches."""

    # ── 1. CUSTOMER — reuse if already exists (same email)
    email = d['customer']['email']
    customer = app_tables.customers.get(email=email)
    if not customer:
        customer = app_tables.customers.add_row(**d['customer'])

    # ── 2. VEHICLE — reuse if plate already exists
    plate = d['vehicle']['plate']
    vehicle = app_tables.vehicles.get(plate=plate)
    if not vehicle:
        vehicle = app_tables.vehicles.add_row(**d['vehicle'])

    # ── 3. JOB
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

    # ── 4. QUOTATION
    qt_data = d.get('quotation')
    if qt_data:
        raw_items  = qt_data['items']
        subtotal   = sum(item[4] for item in raw_items)
        discount   = qt_data['discount']
        tax_rate   = qt_data['tax_rate']
        after_disc = subtotal - discount
        tax_amt    = round(after_disc * tax_rate, 2)
        grand      = round(after_disc + tax_amt, 2)

        qt = app_tables.quotations.add_row(
            job=             job,
            quote_ref=       qt_data['quote_ref'],
            status=          qt_data['status'],
            currency=        GARAGE['currency'],
            subtotal=        subtotal,
            discount=        discount,
            discount_label=  qt_data['discount_label'],
            tax=             tax_amt,
            tax_label=       qt_data['tax_label'],
            grand_total=     grand,
            est_duration=    qt_data['est_duration'],
            approval_status= qt_data['approval_status'],
        )
        for item in raw_items:
            app_tables.quote_items.add_row(
                quotation=qt,
                description=item[0],
                item_type=item[1],
                qty=item[2],
                unit_price=item[3],
                total=item[4],
            )

    # ── 5. SERVICE + TIMELINE + NOTES
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
        for i, tl in enumerate(sv_data['timeline']):
            app_tables.timeline.add_row(
                service=sv, time_label=tl[0], title=tl[1],
                description=tl[2], status=tl[3], sort_order=i,
            )
        for note in sv_data.get('notes', []):
            app_tables.tech_notes.add_row(service=sv, note_text=note[0], color=note[1])

    # ── 6. INVOICE
    inv_data = d.get('invoice')
    total_due = 0
    if inv_data:
        raw_items  = inv_data['items']
        subtotal   = sum(item[3] for item in raw_items)
        discount   = inv_data['discount']
        tax_rate   = inv_data['tax_rate']
        after_disc = subtotal - discount
        tax_amt    = round(after_disc * tax_rate, 2)
        total_due  = round(after_disc + tax_amt, 2)

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
            tax=            tax_amt,
            tax_label=      inv_data['tax_label'],
            total_due=      total_due,
            biller_name=    GARAGE['name'],
            biller_pin=     GARAGE['pin'],
            biller_address= GARAGE['address'],
            biller_phone=   GARAGE['phone'],
        )
        for item in raw_items:
            app_tables.invoice_items.add_row(
                invoice=inv, description=item[0], qty=item[1],
                unit_price=item[2], total=item[3],
            )

    # ── 7. PAYMENT
    pay_data = d.get('payment')
    if pay_data:
        balance = round(total_due - pay_data['deposit_paid'], 2) if total_due else 0
        pay = app_tables.payments.add_row(
            job=job,
            currency=    GARAGE['currency'],
            balance=     balance,
            deposit_paid=pay_data['deposit_paid'],
            status=      pay_data['status'],
        )
        for h in pay_data.get('history', []):
            app_tables.payment_history.add_row(
                payment=pay, date=h[0], method=h[1],
                reference=h[2], amount=h[3], status=h[4],
            )

    return d['job_ref']