"""
FILE: auth_html.py  (Client Module)
Three constants: AUTH_CSS, AUTH_BODY, AUTH_JS — imported by AuthForm.py
"""

# ---------------------------------------------------------------------------
# AUTH_CSS
# Styles for the login / signup overlay. Injected into <head> via AuthForm.py
# ---------------------------------------------------------------------------
AUTH_CSS = """
:root {
  --bg:           #0d0f14;
  --surface:      #13161d;
  --surface-2:    #1a1e28;
  --border:       #252a38;
  --accent:       #e8ff47;
  --accent-dim:   rgba(232, 255, 71, 0.12);
  --accent-glow:  rgba(232, 255, 71, 0.3);
  --text:         #f0f2f8;
  --text-muted:   #6b7394;
  --text-mid:     #9da3bf;
  --green:        #3dffa0;
  --green-dim:    rgba(61, 255, 160, 0.1);
  --red:          #ff4d6d;
  --red-dim:      rgba(255, 77, 109, 0.12);
  --radius:       20px;
  --radius-sm:    12px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

/* ── ROOT ── */
.auth-root {
  min-height: 100vh;
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'PortalFont', sans-serif;
  position: relative;
  overflow: hidden;
}

/* Animated grid background */
.auth-root::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(232, 255, 71, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(232, 255, 71, 0.04) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
}

/* Glow blob */
.auth-root::after {
  content: '';
  position: fixed;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(232, 255, 71, 0.06) 0%, transparent 70%);
  top: -100px;
  left: -100px;
  pointer-events: none;
}

/* ── SPLIT LAYOUT ── */
.auth-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  width: 100%;
  max-width: 1000px;
  min-height: 580px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  position: relative;
  z-index: 1;
  box-shadow: 0 40px 80px rgba(0, 0, 0, 0.5);
  animation: authIn 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@keyframes authIn {
  from { opacity: 0; transform: translateY(30px) scale(0.97); }
  to   { opacity: 1; transform: translateY(0)    scale(1);    }
}

/* ── LEFT PANEL (branding) ── */
.auth-brand {
  background: linear-gradient(145deg, #111419 0%, #0d0f14 100%);
  padding: 48px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-right: 1px solid var(--border);
  position: relative;
  overflow: hidden;
}

.auth-brand::before {
  content: '⚙';
  position: absolute;
  font-size: 320px;
  line-height: 1;
  bottom: -60px;
  right: -60px;
  opacity: 0.03;
  pointer-events: none;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: 'PortalFont', sans-serif;
  font-weight: 800;
  font-size: 20px;
  color: var(--text);
}

.brand-logo-mark {
  width: 40px;
  height: 40px;
  background: var(--accent);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #000;
  flex-shrink: 0;
}

.brand-tagline {
  font-family: 'PortalFont', sans-serif;
  font-weight: 800;
  font-size: clamp(28px, 3vw, 38px);
  line-height: 1.15;
  letter-spacing: -1px;
  color: var(--text);
  margin-bottom: 16px;
}

.brand-tagline span { color: var(--accent); }

.brand-desc {
  font-size: 14px;
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 32px;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.brand-feature {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--text-mid);
}

.brand-feature-dot {
  width: 6px;
  height: 6px;
  background: var(--accent);
  border-radius: 50%;
  flex-shrink: 0;
}

/* ── RIGHT PANEL (form) ── */
.auth-form-panel {
  padding: 48px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: var(--surface);
}

.auth-tabs {
  display: flex;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 4px;
  margin-bottom: 32px;
}

.auth-tab {
  flex: 1;
  padding: 9px 16px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-family: 'PortalFont', sans-serif;
  font-size: 13px;
  font-weight: 500;
  border-radius: 100px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.auth-tab.active {
  background: var(--accent);
  color: #000;
  font-weight: 700;
}

.auth-form         { display: none; }
.auth-form.active  { display: block; animation: fadeSlide 0.25s ease; }

@keyframes fadeSlide {
  from { opacity: 0; transform: translateX(10px); }
  to   { opacity: 1; transform: translateX(0);    }
}

.form-title {
  font-family: 'PortalFont', sans-serif;
  font-weight: 700;
  font-size: 22px;
  color: var(--text);
  margin-bottom: 6px;
}

.form-subtitle {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 28px;
  line-height: 1.5;
}

/* ── FIELDS ── */
.field { margin-bottom: 16px; }

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.field-row .field { margin-bottom: 0; }

label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
  margin-bottom: 6px;
}

.input-wrap { position: relative; }

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 15px;
  pointer-events: none;
  opacity: 0.5;
}

input[type="text"],
input[type="email"],
input[type="password"],
input[type="tel"] {
  width: 100%;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text);
  font-family: 'PortalFont', sans-serif;
  font-size: 14px;
  padding: 12px 14px 12px 40px;
  outline: none;
  transition: all 0.2s;
  -webkit-appearance: none;
}

input:focus {
  border-color: var(--accent);
  background: var(--accent-dim);
  box-shadow: 0 0 0 3px var(--accent-glow);
}

input.error {
  border-color: var(--red);
  background: var(--red-dim);
}

input::placeholder { color: var(--text-muted); opacity: 0.6; }

.eye-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 15px;
  padding: 4px;
  line-height: 1;
}

/* ── MESSAGES ── */
.error-msg {
  display: none;
  background: var(--red-dim);
  border: 1px solid var(--red);
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  font-size: 13px;
  color: var(--red);
  margin-bottom: 16px;
  line-height: 1.5;
}

.error-msg.show { display: block; animation: shake 0.3s ease; }

@keyframes shake {
  0%, 100% { transform: translateX(0);  }
  25%       { transform: translateX(-6px); }
  75%       { transform: translateX(6px);  }
}

.success-msg {
  display: none;
  background: var(--green-dim);
  border: 1px solid var(--green);
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  font-size: 13px;
  color: var(--green);
  margin-bottom: 16px;
}

.success-msg.show { display: block; }

/* ── SUBMIT BUTTON ── */
.submit-btn {
  width: 100%;
  padding: 14px;
  background: var(--accent);
  color: #000;
  font-family: 'PortalFont', sans-serif;
  font-weight: 700;
  font-size: 14px;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  letter-spacing: 0.5px;
  transition: all 0.2s;
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  overflow: hidden;
}

.submit-btn:hover:not(:disabled) {
  background: #f5ff72;
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(232, 255, 71, 0.35);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-spinner {
  display: none;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0, 0, 0, 0.3);
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.submit-btn.loading .btn-text    { display: none; }
.submit-btn.loading .btn-spinner { display: block; }

/* ── DIVIDER ── */
.auth-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 20px 0;
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.auth-divider::before,
.auth-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

/* ── JOB REFERENCE LOOKUP ── */
.job-lookup-wrap {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 16px;
  margin-top: 12px;
  display: none;
}

.job-lookup-wrap.show { display: block; animation: fadeSlide 0.2s ease; }

.job-lookup-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.job-result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  margin-bottom: 6px;
  cursor: pointer;
  transition: all 0.15s;
  font-size: 13px;
}

.job-result-item:hover {
  border-color: var(--accent);
  background: var(--accent-dim);
}

.job-result-ref {
  font-family: 'PortalFont', sans-serif;
  font-weight: 700;
  font-size: 12px;
  color: var(--accent);
}

.job-result-vehicle { color: var(--text-muted); font-size: 12px; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar       { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── RESPONSIVE ── */
@media (max-width: 700px) {
  .auth-root        { padding: 12px; align-items: flex-start; }
  .auth-split       { grid-template-columns: 1fr; max-width: 100%; min-height: 0; margin-top: 56px; }
  .auth-brand       { display: none; }
  .auth-form-panel  { padding: 24px 16px; }
  .field-row        { grid-template-columns: 1fr; gap: 10px; }
  .auth-tab         { font-size: 12px; padding: 10px 8px; }
  .form-title       { font-size: 20px; }
  .submit-btn       { padding: 13px; }
}

@media (max-width: 420px) {
  .auth-form-panel  { padding: 20px 12px; }
  .auth-tabs        { margin-bottom: 22px; }
  .auth-divider     { margin: 16px 0; }
}
"""


# ---------------------------------------------------------------------------
# AUTH_BODY
# HTML markup for the auth overlay. No onclick attributes — all events are
# wired in AUTH_JS via addEventListener.
# ---------------------------------------------------------------------------
AUTH_BODY = """
<div class="auth-root">
  <div class="auth-split">

    <!-- ── LEFT: BRANDING ── -->
    <div class="auth-brand">
      <div class="brand-logo">
        <div class="brand-logo-mark">&#9881;</div>
        AutoCare Portal
      </div>

      <div>
        <div class="brand-tagline">
          Your garage,<br><span>always in sync.</span>
        </div>
        <div class="brand-desc">
          Track your vehicle's service journey from check-in to
          payment &mdash; all in one place.
        </div>
        <div class="brand-features">
          <div class="brand-feature">
            <div class="brand-feature-dot"></div>Real-time service updates
          </div>
          <div class="brand-feature">
            <div class="brand-feature-dot"></div>View &amp; approve quotations
          </div>
          <div class="brand-feature">
            <div class="brand-feature-dot"></div>Download invoices instantly
          </div>
          <div class="brand-feature">
            <div class="brand-feature-dot"></div>Pay via M-PESA, card or cash
          </div>
          <div class="brand-feature">
            <div class="brand-feature-dot"></div>Full service history
          </div>
        </div>
      </div>

      <div style="font-size:11px;color:var(--text-muted)">
        &#169; 2025 AutoCare Garage Ltd. &middot; Nairobi
      </div>
    </div>

    <!-- ── RIGHT: FORM ── -->
    <div class="auth-form-panel">

      <!-- Tab switcher -->
      <div class="auth-tabs">
        <button class="auth-tab active" id="tab-login">Sign In</button>
        <button class="auth-tab"        id="tab-signup">Create Account</button>
      </div>

      <!-- ── LOGIN FORM ── -->
      <div class="auth-form active" id="form-login">
        <div class="form-title">Welcome back</div>
        <div class="form-subtitle">Sign in to track your vehicle service.</div>

        <div class="error-msg"   id="login-error"></div>
        <div class="success-msg" id="login-success"></div>

        <div class="field">
          <label for="login-email">Email address</label>
          <div class="input-wrap">
            <span class="input-icon">&#9993;</span>
            <input type="email" id="login-email"
                   placeholder="you@example.com" autocomplete="off">
          </div>
        </div>

        <div class="field">
          <label for="login-password">Password</label>
          <div class="input-wrap">
            <span class="input-icon">&#128274;</span>
            <input type="password" id="login-password"
                   placeholder="Your password" autocomplete="new-password">
            <button class="eye-btn" id="toggle-login-pwd" tabindex="-1">
              &#128065;
            </button>
          </div>
        </div>

        <button class="submit-btn" id="login-btn">
          <span class="btn-text">Sign In &#8594;</span>
          <div class="btn-spinner"></div>
        </button>

        <div class="auth-divider">or</div>
        <div style="text-align:center;font-size:13px;color:var(--text-muted)">
          Don't have an account?
          <span id="link-to-signup"
                style="color:var(--accent);cursor:pointer;font-weight:600">
            Create one &#8594;
          </span>
        </div>
      </div>

      <!-- ── SIGNUP FORM ── -->
      <div class="auth-form" id="form-signup">
        <div class="form-title">Create account</div>
        <div class="form-subtitle">Join as an existing or new customer.</div>

        <div class="error-msg"   id="signup-error"></div>
        <div class="success-msg" id="signup-success"></div>

        <div class="field-row">
          <div class="field">
            <label for="signup-firstname">First Name</label>
            <div class="input-wrap">
              <span class="input-icon">&#128100;</span>
              <input type="text" id="signup-firstname" placeholder="James">
            </div>
          </div>
          <div class="field">
            <label for="signup-lastname">Last Name</label>
            <div class="input-wrap">
              <span class="input-icon">&#128100;</span>
              <input type="text" id="signup-lastname" placeholder="Odhiambo">
            </div>
          </div>
        </div>

        <div class="field">
          <label for="signup-email">Email address</label>
          <div class="input-wrap">
            <span class="input-icon">&#9993;</span>
            <input type="email" id="signup-email"
                   placeholder="you@example.com" autocomplete="email">
          </div>
        </div>

        <div class="field">
          <label for="signup-phone">Phone number</label>
          <div class="input-wrap">
            <span class="input-icon">&#128241;</span>
            <input type="tel" id="signup-phone" placeholder="+254 7XX XXX XXX">
          </div>
        </div>

        <div class="field">
          <label for="signup-password">Password</label>
          <div class="input-wrap">
            <span class="input-icon">&#128274;</span>
            <input type="password" id="signup-password"
                   placeholder="Min. 8 characters" autocomplete="new-password">
            <button class="eye-btn" id="toggle-signup-pwd" tabindex="-1">
              &#128065;
            </button>
          </div>
        </div>

        <div class="field">
          <label for="signup-password2">Confirm password</label>
          <div class="input-wrap">
            <span class="input-icon">&#128274;</span>
            <input type="password" id="signup-password2"
                   placeholder="Repeat password" autocomplete="new-password">
          </div>
        </div>

        <!-- Existing-customer job lookup -->
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
          <input type="checkbox" id="existing-customer-chk"
                 style="width:16px;height:16px;accent-color:var(--accent);cursor:pointer">
          <label for="existing-customer-chk"
                 style="font-size:13px;text-transform:none;letter-spacing:0;
                        color:var(--text-mid);cursor:pointer;margin:0">
            I'm an existing customer &mdash; link my records
          </label>
        </div>

        <div class="job-lookup-wrap" id="job-lookup-wrap">
          <div class="job-lookup-label">Enter your Job Reference</div>
          <div class="input-wrap" style="margin-bottom:10px">
            <span class="input-icon">&#128269;</span>
            <input type="text" id="job-ref-input"
                   placeholder="e.g. GRG-2025-0001">
          </div>
          <div id="job-lookup-results"></div>
        </div>

        <button class="submit-btn" id="signup-btn" style="margin-top:16px">
          <span class="btn-text">Create Account &#8594;</span>
          <div class="btn-spinner"></div>
        </button>

        <div class="auth-divider">or</div>
        <div style="text-align:center;font-size:13px;color:var(--text-muted)">
          Already have an account?
          <span id="link-to-login"
                style="color:var(--accent);cursor:pointer;font-weight:600">
            Sign in &#8594;
          </span>
        </div>
      </div>

    </div><!-- /auth-form-panel -->
  </div><!-- /auth-split -->
</div><!-- /auth-root -->
"""


# ---------------------------------------------------------------------------
# AUTH_JS
# All interactivity wired with addEventListener — no inline onclick handlers.
# Injected via document.createElement('script') AFTER Python bridges are set.
# ---------------------------------------------------------------------------
AUTH_JS = """
(function () {
  'use strict';

  // ── UTILITIES ────────────────────────────────────────────────────────────

  function $(id) { return document.getElementById(id); }

  function showMsg(id, msg) {
    var el = $(id);
    if (!el) return;
    el.textContent = msg;
    el.classList.add('show');
  }

  function clearMessages() {
    ['login-error', 'login-success', 'signup-error', 'signup-success']
      .forEach(function (id) {
        var el = $(id);
        if (!el) return;
        el.classList.remove('show');
        el.textContent = '';
      });
  }

  function setLoading(btnId, on) {
    var btn = $(btnId);
    if (!btn) return;
    btn.disabled = on;
    btn.classList.toggle('loading', on);
  }

  // ── TAB SWITCHING ────────────────────────────────────────────────────────

  function switchTab(tab) {
    ['login', 'signup'].forEach(function (t) {
      var tabEl  = $('tab-'  + t);
      var formEl = $('form-' + t);
      if (tabEl)  tabEl.classList.toggle('active',  t === tab);
      if (formEl) formEl.classList.toggle('active', t === tab);
    });
    clearMessages();
  }

  var tabLogin  = $('tab-login');
  var tabSignup = $('tab-signup');
  if (tabLogin)  tabLogin.addEventListener('click',  function () { switchTab('login');  });
  if (tabSignup) tabSignup.addEventListener('click', function () { switchTab('signup'); });

  // "Create one" / "Sign in" inline links
  var linkToSignup = $('link-to-signup');
  var linkToLogin  = $('link-to-login');
  if (linkToSignup) linkToSignup.addEventListener('click', function () { switchTab('signup'); });
  if (linkToLogin)  linkToLogin.addEventListener('click',  function () { switchTab('login');  });

  // ── PASSWORD VISIBILITY TOGGLE ───────────────────────────────────────────

  function makeEyeToggle(btnId, inputId) {
    var btn = $(btnId);
    var inp = $(inputId);
    if (!btn || !inp) return;
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      if (inp.type === 'password') {
        inp.type = 'text';
        btn.innerHTML = '&#128584;';
      } else {
        inp.type = 'password';
        btn.innerHTML = '&#128065;';
      }
    });
  }

  makeEyeToggle('toggle-login-pwd',  'login-password');
  makeEyeToggle('toggle-signup-pwd', 'signup-password');

  // ── EXISTING CUSTOMER TOGGLE ─────────────────────────────────────────────

  var existingChk   = $('existing-customer-chk');
  var jobLookupWrap = $('job-lookup-wrap');
  var jobRefInput   = $('job-ref-input');
  var jobResults    = $('job-lookup-results');
  var selectedJobRef = null;

  if (existingChk) {
    existingChk.addEventListener('change', function () {
      if (jobLookupWrap) {
        jobLookupWrap.classList.toggle('show', existingChk.checked);
      }
      if (!existingChk.checked) {
        if (jobRefInput) jobRefInput.value = '';
        if (jobResults)  jobResults.innerHTML = '';
        selectedJobRef = null;
      }
    });
  }

  // ── JOB REFERENCE LOOKUP (debounced) ────────────────────────────────────

  var lookupTimer = null;

  function renderJobResults(jobs) {
    if (!jobResults) return;
    if (!jobs || jobs.length === 0) {
      jobResults.innerHTML =
        '<div style="font-size:12px;color:var(--text-muted);padding:6px 0">' +
        'No jobs found for that reference.</div>';
      return;
    }
    jobResults.innerHTML = '';
    jobs.forEach(function (j) {
      var item = document.createElement('div');
      item.className = 'job-result-item';
      item.innerHTML =
        '<div>' +
          '<div class="job-result-ref">'     + j.job_ref + '</div>' +
          '<div class="job-result-vehicle">' + j.vehicle + '</div>' +
        '</div>' +
        '<div style="font-size:11px;color:var(--text-muted)">' + j.date + '</div>';
      item.addEventListener('click', function () {
        selectedJobRef = j.job_ref;
        if (jobRefInput) jobRefInput.value = j.job_ref;
        jobResults.innerHTML =
          '<div style="font-size:12px;color:var(--green);padding:6px 0">' +
          '&#10003; Job ' + j.job_ref + ' selected &mdash; ' + j.vehicle + '</div>';
      });
      jobResults.appendChild(item);
    });
  }

  if (jobRefInput) {
    jobRefInput.addEventListener('input', function () {
      clearTimeout(lookupTimer);
      selectedJobRef = null;
      if (jobResults) jobResults.innerHTML = '';
      var val = jobRefInput.value.trim();
      if (val.length < 3) return;
      if (jobResults) {
        jobResults.innerHTML =
          '<div style="font-size:12px;color:var(--text-muted);padding:6px 0">Searching...</div>';
      }
      lookupTimer = setTimeout(function () {
        if (typeof window._anvilJobLookup !== 'function') return;
        Promise.resolve(window._anvilJobLookup(val))
          .then(renderJobResults)
          .catch(function () {
            if (jobResults) {
              jobResults.innerHTML =
                '<div style="font-size:12px;color:var(--red)">Lookup failed.</div>';
            }
          });
      }, 400);
    });
  }

  // ── LOGIN ────────────────────────────────────────────────────────────────

  function doLogin() {
    clearMessages();
    var email    = $('login-email')    ? $('login-email').value.trim() : '';
    var password = $('login-password') ? $('login-password').value      : '';

    if (!email || !password) {
      showMsg('login-error', 'Please enter your email and password.');
      return;
    }

    setLoading('login-btn', true);

    if (typeof window._anvilLogin !== 'function') {
      showMsg('login-error', 'Auth service not ready. Please wait a moment and try again.');
      setLoading('login-btn', false);
      return;
    }

    Promise.resolve(window._anvilLogin(email, password))
      .then(function (result) {
        setLoading('login-btn', false);
        if (result && result.success) {
          showMsg('login-success', '&#10003; Signed in! Loading your portal...');
          setTimeout(function () {
            if (typeof window._anvilLoginSuccess === 'function') {
              window._anvilLoginSuccess(result);
            }
          }, 800);
        } else {
          showMsg('login-error', (result && result.error) || 'Invalid email or password.');
        }
      })
      .catch(function (err) {
        setLoading('login-btn', false);
        showMsg('login-error', String(err) || 'Login failed. Please try again.');
      });
  }

  var loginBtn = $('login-btn');
  if (loginBtn) loginBtn.addEventListener('click', doLogin);

  // ── SIGNUP ───────────────────────────────────────────────────────────────

  function doSignup() {
    clearMessages();

    var first    = $('signup-firstname') ? $('signup-firstname').value.trim() : '';
    var last     = $('signup-lastname')  ? $('signup-lastname').value.trim()  : '';
    var email    = $('signup-email')     ? $('signup-email').value.trim()     : '';
    var phone    = $('signup-phone')     ? $('signup-phone').value.trim()     : '';
    var pwd      = $('signup-password')  ? $('signup-password').value         : '';
    var pwd2     = $('signup-password2') ? $('signup-password2').value        : '';
    var existing = existingChk ? existingChk.checked : false;

    if (!first || !last) {
      showMsg('signup-error', 'Please enter your full name.');
      return;
    }
    if (!email) {
      showMsg('signup-error', 'Please enter your email address.');
      return;
    }
    if (!phone) {
      showMsg('signup-error', 'Please enter your phone number.');
      return;
    }
    if (pwd.length < 8) {
      showMsg('signup-error', 'Password must be at least 8 characters.');
      return;
    }
    if (pwd !== pwd2) {
      showMsg('signup-error', 'Passwords do not match.');
      return;
    }
    if (existing && !selectedJobRef) {
      showMsg('signup-error',
        'Please select a job from the lookup to link your existing records.');
      return;
    }

    setLoading('signup-btn', true);

    if (typeof window._anvilSignup !== 'function') {
      showMsg('signup-error', 'Auth service not ready. Please wait a moment and try again.');
      setLoading('signup-btn', false);
      return;
    }

    var payload = {
      first_name: first,
      last_name:  last,
      email:      email,
      phone:      phone,
      password:   pwd,
      job_ref:    selectedJobRef || null,
    };

    Promise.resolve(window._anvilSignup(payload))
      .then(function (result) {
        setLoading('signup-btn', false);
        if (result && result.success) {
          showMsg('signup-success', '&#10003; Account created! Signing you in...');
          setTimeout(function () {
            if (typeof window._anvilLoginSuccess === 'function') {
              window._anvilLoginSuccess(result);
            }
          }, 1000);
        } else {
          showMsg('signup-error', (result && result.error) || 'Signup failed. Please try again.');
        }
      })
      .catch(function (err) {
        setLoading('signup-btn', false);
        showMsg('signup-error', String(err) || 'Signup failed.');
      });
  }

  var signupBtn = $('signup-btn');
  if (signupBtn) signupBtn.addEventListener('click', doSignup);

  // ── ENTER KEY SUPPORT ────────────────────────────────────────────────────

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter') return;
    var loginActive = $('form-login') && $('form-login').classList.contains('active');
    if (loginActive) doLogin();
    else doSignup();
  });

  // ── CLEAR CACHED INPUTS (post-logout / browser autofill guard) ───────────

  function clearAuthInputs() {
    var ids = [
      'login-email', 'login-password',
      'signup-firstname', 'signup-lastname',
      'signup-email', 'signup-phone',
      'signup-password', 'signup-password2',
      'job-ref-input',
    ];
    ids.forEach(function (id) {
      var el = $(id);
      if (!el) return;
      el.value = '';
      el.setAttribute('autocomplete', 'off');
    });
  }

  clearAuthInputs();
  setTimeout(clearAuthInputs,  60);
  setTimeout(clearAuthInputs, 300);

  console.log('[AutoCare] Auth JS wired up successfully.');
})();
"""
