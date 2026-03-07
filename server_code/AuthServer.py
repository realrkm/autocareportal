"""
FILE: AuthServer.py  (Server Module)
═══════════════════════════════════════════════════════════════════
SETUP:
  1. Click "+" next to Server Modules → name it "AuthServer"
  2. Paste this entire file into it

PREREQUISITES:
  • Enable Anvil's built-in Users service:
      App Settings → Services → click "+" → Add "Users"
  • This adds the 'users' table automatically with email + password_hash columns
  • In the Users service settings:
      - Enable "Allow visitors to sign up"
      - Enable "Remember login between sessions"
      - Set "User table" to "users"

HOW AUTH WORKS:
  Login  → anvil.users.login_with_email()  (Anvil built-in)
  Signup → anvil.users.signup_with_email() (Anvil built-in)
         → then creates/links a customers row
  Logout → anvil.users.logout()

ADDITIONAL TABLE COLUMN NEEDED:
  Add to the 'users' table (App Tables → users):
    - customer  (link → customers)   ← links auth user to customer record
═══════════════════════════════════════════════════════════════════
"""

import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


# ════════════════════════════════════════════════════════════════
#  LOGIN
# ════════════════════════════════════════════════════════════════

@anvil.server.callable
def login_user(email, password):
    """
    Authenticates a user with email + password.
    Returns { success, job_ref, error }
    """
    try:
        user = anvil.users.login_with_email(email, password)
        if not user:
            return {'success': False, 'error': 'Invalid email or password.'}

        # Find most recent job for this user
        job_ref = _get_latest_job_ref(user)
        return {'success': True, 'job_ref': job_ref}

    except anvil.users.AuthenticationFailed:
        return {'success': False, 'error': 'Invalid email or password.'}
    except anvil.users.TooManyLoginAttempts:
        return {'success': False, 'error': 'Too many failed attempts. Please wait a few minutes.'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ════════════════════════════════════════════════════════════════
#  SIGNUP / REGISTER
# ════════════════════════════════════════════════════════════════

@anvil.server.callable
def register_user(data):
    """
    Registers a new user account.

    data keys:
      first_name, last_name, email, phone, password
      job_ref (optional) — to link to existing customer record

    Returns { success, job_ref, error }
    """
    try:
        first_name = data.get('first_name', '').strip()
        last_name  = data.get('last_name', '').strip()
        email      = data.get('email', '').strip().lower()
        phone      = data.get('phone', '').strip()
        password   = data.get('password', '')
        job_ref    = data.get('job_ref')

        # ── Basic server-side validation
        if not first_name or not last_name:
            return {'success': False, 'error': 'Full name is required.'}
        if not email or '@' not in email:
            return {'success': False, 'error': 'A valid email address is required.'}
        if len(password) < 8:
            return {'success': False, 'error': 'Password must be at least 8 characters.'}

        # ── Check email not already registered
        existing_user = app_tables.users.get(email=email)
        if existing_user:
            return {'success': False, 'error': 'An account with this email already exists. Please sign in.'}

        full_name = f"{first_name} {last_name}"

        # ── If linking to existing job, verify job + customer match
        customer_row = None
        if job_ref:
            job = app_tables.jobs.get(job_ref=job_ref)
            if not job:
                return {'success': False, 'error': f'Job reference {job_ref} not found.'}
            customer_row = job['customer']
            # Optionally verify phone matches
            if customer_row['phone'] and phone:
                # Normalise and loosely compare
                def _norm(p):
                    return ''.join(c for c in p if c.isdigit())[-9:]
                if _norm(customer_row['phone']) != _norm(phone):
                    return {
                        'success': False,
                        'error': 'Phone number does not match our records for that job reference. '
                        'Please check your details or contact the garage.'
                    }
            # Update customer record with potentially new info
            customer_row.update(
                name=full_name,
                phone=phone or customer_row['phone'],
                email=email
            )
        else:
            # ── New customer — check if customer row exists with this email
            customer_row = app_tables.customers.get(email=email)
            if not customer_row:
                # Create a brand new customer record
                customer_row = app_tables.customers.add_row(
                    name=full_name,
                    phone=phone,
                    email=email
                )

        # ── Create the Anvil user account
        user = anvil.users.signup_with_email(email, password)

        # ── Link user to customer record
        user.update(customer=customer_row)

        # ── Auto-login after signup
        anvil.users.login_with_email(email, password)

        # ── Get latest job ref for this user
        latest_job_ref = _get_latest_job_ref(user) or job_ref

        return {'success': True, 'job_ref': latest_job_ref}

    except anvil.users.UserExists:
        return {'success': False, 'error': 'An account with this email already exists. Please sign in.'}
    except anvil.users.PasswordNotAcceptable:
        return {'success': False, 'error': 'Password is too weak. Please choose a stronger password.'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ════════════════════════════════════════════════════════════════
#  LOGOUT
# ════════════════════════════════════════════════════════════════

@anvil.server.callable
def logout_user():
    """Logs out the current user session."""
    try:
        anvil.users.logout()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ════════════════════════════════════════════════════════════════
#  JOB REFERENCE LOOKUP  (for signup existing-customer flow)
# ════════════════════════════════════════════════════════════════


@anvil.server.callable
def request_password_reset(email):
    """
    Sends a password reset email via Anvil Users service.
    Always returns a generic success-style message to avoid leaking account existence.
    """
    try:
        email = (email or '').strip().lower()
        if not email or '@' not in email:
            return {
                'success': False,
                'message': 'Please enter a valid email address.'
            }

        # Built-in Anvil Users password reset flow.
        anvil.users.send_password_reset_email(email)
        return {
            'success': True,
            'message': 'If an account exists for that email, a password reset link has been sent.'
        }
    except Exception:
        # Keep response generic for security and UX consistency.
        return {
            'success': True,
            'message': 'If an account exists for that email, a password reset link has been sent.'
        }

@anvil.server.callable
def lookup_job_ref(query):
    """
    Searches for jobs matching a partial job_ref string.
    Returns a list of dicts safe to send to the client.
    Only returns minimal info (ref, vehicle, date) — no sensitive data.
    """
    query = str(query).strip().upper()
    if len(query) < 3:
        return []

    try:
        # Search jobs where job_ref contains the query string
        all_jobs = app_tables.jobs.search(
            tables.order_by('checkin_date', ascending=False)
        )
        results = []
        for job in all_jobs:
            if query in job['job_ref'].upper():
                results.append({
                    'job_ref': job['job_ref'],
                    'vehicle': job['vehicle']['plate'] + ' · ' + job['vehicle']['model'],
                    'date':    str(job['checkin_date']),
                })
                if len(results) >= 5:  # cap at 5 results
                    break
        return results
    except Exception:
        return []


# ════════════════════════════════════════════════════════════════
#  HELPER: get latest job ref for a user
# ════════════════════════════════════════════════════════════════

def _get_latest_job_ref(user):
    """Returns the most recent job_ref for the given user, or None."""
    try:
        customer = user['customer']
        if not customer:
            return None
        jobs = list(app_tables.jobs.search(
            tables.order_by('checkin_date', ascending=False),
            customer=customer
        ))
        return jobs[0]['job_ref'] if jobs else None
    except Exception:
        return None


# ════════════════════════════════════════════════════════════════
#  SESSION CHECK  (called on portal load to verify auth)
# ════════════════════════════════════════════════════════════════

@anvil.server.callable
def get_current_user_info():
    """
    Returns basic info about the logged-in user.
    Called by the portal on load to verify the session is valid.
    """
    user = anvil.users.get_user()
    if not user:
        raise Exception('Not authenticated. Please log in.')
    customer = user['customer']
    job_ref = _get_latest_job_ref(user)
    return {
        'email':    user['email'],
        'name':     customer['name'] if customer else user['email'],
        'job_ref':  job_ref
    }
