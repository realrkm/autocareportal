"""
FILE: AuthForm.py  (Client-side Form)
SETUP:
  1. Create a new Blank Form -> name it "AuthForm"
  2. Leave the canvas EMPTY (no components)
  3. Paste this entire file into the Code view
  4. Set AuthForm as the Startup Form in App Settings
"""

from ._anvil_designer import AuthFormTemplate
from anvil import *
import anvil.server
import anvil.js
import anvil.users

from ..auth_html import AUTH_CSS, AUTH_BODY, AUTH_JS


class AuthForm(AuthFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Already logged in? Go straight to portal
        try:
            user = anvil.users.get_user()
            if user:
                self._go_to_portal()
                return
        except Exception:
            pass

        # 1. Inject CSS + HTML into DOM
        self._inject_html()

        # 2. Register Python bridges on window BEFORE running the JS
        anvil.js.window['_anvilLogin']        = self._handle_login
        anvil.js.window['_anvilSignup']       = self._handle_signup
        anvil.js.window['_anvilJobLookup']    = self._handle_job_lookup
        anvil.js.window['_anvilLoginSuccess'] = self._on_login_success
        anvil.js.window['_anvilForgotPassword'] = self._handle_forgot_password

        # 3. Now run the JS (bridges already on window, addEventListener safe)
        self._inject_js()
        self._inject_theme_layer()

    # ─── STEP 1: inject CSS + HTML (no scripts) ───────────────────
    def _inject_html(self):
        import json
        css_json  = json.dumps(AUTH_CSS)
        body_json = json.dumps(AUTH_BODY)

        anvil.js.call_js('eval', f"""
          (function() {{
            // Clean up previous instances
            ['garage-auth-root','garage-auth-css','garage-auth-js'].forEach(function(id) {{
              var el = document.getElementById(id);
              if (el) el.remove();
            }});

            // Zero out Anvil chrome
            ['app-bar','nav-holder','left-nav','content','anvil-measure-this'].forEach(function(cls) {{
              document.querySelectorAll('.' + cls).forEach(function(el) {{
                el.style.setProperty('margin-top', '0', 'important');
                el.style.setProperty('padding-top', '0', 'important');
              }});
            }});

            // Inject CSS
            var style = document.createElement('style');
            style.id = 'garage-auth-css';
            style.textContent = {css_json};
            document.head.appendChild(style);

            // Inject HTML
            var wrapper = document.createElement('div');
            wrapper.id = 'garage-auth-root';
            wrapper.style.cssText = [
              'position:fixed','top:0','left:0',
              'width:100vw','height:100vh',
              'overflow-y:auto','overflow-x:hidden',
              'z-index:9999','background:#0d0f14'
            ].join(';');
            wrapper.innerHTML = {body_json};
            document.body.appendChild(wrapper);
          }})();
        """)

    # ─── STEP 3: inject JS *after* bridges are on window ──────────
    def _inject_js(self):
        import json
        js_json = json.dumps(AUTH_JS)

        anvil.js.call_js('eval', f"""
          (function() {{
            var script = document.createElement('script');
            script.id = 'garage-auth-js';
            script.textContent = {js_json};
            document.body.appendChild(script);
          }})();
        """)

    def _inject_theme_layer(self):
        anvil.js.call_js('eval', """
          (function() {
            var root = document.querySelector('#garage-auth-root .auth-root');
            if (!root) return;

            var cssId = 'garage-auth-theme-css';
            var style = document.getElementById(cssId);
            if (!style) {
              style = document.createElement('style');
              style.id = cssId;
              style.textContent = [
                '@font-face{font-family:\"PortalFont\";src:url(\"/_/theme/assets/fonts/MozillaHeadline.ttf\") format(\"truetype\");font-display:swap;}',
                '.auth-root,.auth-root *{font-family:\"PortalFont\",sans-serif!important;}',
                '.auth-root{font-size:16px!important;}',
                '.auth-root.theme-light{',
                '  --bg:#f5f7fb;',
                '  --surface:#ffffff;',
                '  --surface-2:#eef2f8;',
                '  --border:#d6dde8;',
                '  --accent:#5161ff;',
                '  --accent-dim:rgba(81,97,255,0.12);',
                '  --accent-glow:rgba(81,97,255,0.24);',
                '  --text:#121826;',
                '  --text-muted:#5f6c84;',
                '  --text-mid:#4a556d;',
                '  --green:#0e9f6e;',
                '  --green-dim:rgba(14,159,110,0.1);',
                '  --red:#dc2626;',
                '  --red-dim:rgba(220,38,38,0.12);',
                '}',
                '.auth-root.theme-light .auth-brand{',
                '  background:linear-gradient(145deg,#eef3ff 0%,#e7ecfb 100%);',
                '  border-right:1px solid var(--border);',
                '}',
                '.auth-root.theme-light .auth-brand::before{',
                '  opacity:0.06;',
                '  color:#5161ff;',
                '}',
                '.auth-root.theme-light .brand-logo,',
                '.auth-root.theme-light .brand-tagline{',
                '  color:#121826;',
                '}',
                '.auth-root.theme-light .brand-tagline span{',
                '  color:var(--accent);',
                '}',
                '.auth-root.theme-light .brand-desc,',
                '.auth-root.theme-light .brand-feature,',
                '.auth-root.theme-light .auth-brand div[style*=\"font-size:11px\"]{',
                '  color:#4a556d!important;',
                '}',
                '.auth-theme-toggle{',
                '  position:fixed;',
                '  top:18px;',
                '  right:18px;',
                '  z-index:10002;',
                '  display:inline-flex;',
                '  align-items:center;',
                '  gap:8px;',
                '  padding:5px 10px;',
                '  border-radius:100px;',
                '  border:1px solid var(--border);',
                '  background:var(--surface-2);',
                '  color:var(--text-muted);',
                '  font-family:\\'PortalFont\\',sans-serif;',
                '  font-size:11px;',
                '  font-weight:600;',
                '}',
                '.auth-theme-toggle .lbl{opacity:.75;transition:opacity .2s,color .2s;}',
                '.auth-theme-toggle[data-theme=\"dark\"] .lbl-dark, .auth-theme-toggle[data-theme=\"light\"] .lbl-light{opacity:1;color:var(--text);}',
                '.auth-theme-switch{position:relative;display:inline-block;width:44px;height:24px;}',
                '.auth-theme-switch input{opacity:0;width:0;height:0;position:absolute;}',
                '.auth-theme-slider{position:absolute;inset:0;border-radius:100px;background:var(--border);cursor:pointer;transition:all .2s;}',
                '.auth-theme-slider::before{content:\"\";position:absolute;width:18px;height:18px;left:3px;top:3px;border-radius:50%;background:#fff;transition:transform .2s;}',
                '.auth-theme-switch input:checked + .auth-theme-slider{background:var(--accent);}',
                '.auth-theme-switch input:checked + .auth-theme-slider::before{transform:translateX(20px);}',
                '@media(max-width:700px){.auth-theme-toggle{top:10px;right:10px;padding:4px 8px;gap:6px;}.auth-theme-toggle .lbl{display:none;}.auth-theme-switch{width:38px;height:20px;}.auth-theme-slider::before{width:14px;height:14px;top:3px;left:3px;}.auth-theme-switch input:checked + .auth-theme-slider::before{transform:translateX(18px);}}'
              ].join('');
              document.head.appendChild(style);
            }

            var key = 'autocare-theme';
            var toggleWrap = document.getElementById('auth-theme-toggle-btn');
            if (!toggleWrap) {
              toggleWrap = document.createElement('div');
              toggleWrap.id = 'auth-theme-toggle-btn';
              toggleWrap.className = 'auth-theme-toggle';
              toggleWrap.innerHTML =
                '<span class=\"lbl lbl-dark\">Dark</span>' +
                '<label class=\"auth-theme-switch\">' +
                  '<input id=\"auth-theme-toggle-input\" type=\"checkbox\" aria-label=\"Toggle light mode\">' +
                  '<span class=\"auth-theme-slider\"></span>' +
                '</label>' +
                '<span class=\"lbl lbl-light\">Light</span>';
              var host = document.getElementById('garage-auth-root');
              if (host) host.appendChild(toggleWrap);
            }
            var toggleInput = document.getElementById('auth-theme-toggle-input');

            function apply(theme) {
              var isLight = theme === 'light';
              root.classList.toggle('theme-light', isLight);
              if (toggleInput) toggleInput.checked = isLight;
              if (toggleWrap) toggleWrap.setAttribute('data-theme', isLight ? 'light' : 'dark');
            }

            var stored = null;
            try { stored = localStorage.getItem(key); } catch (e) {}
            apply(stored === 'light' ? 'light' : 'dark');

            if (toggleInput && !toggleInput.dataset.bound) {
              toggleInput.dataset.bound = '1';
              toggleInput.onchange = function() {
                var next = toggleInput.checked ? 'light' : 'dark';
                try { localStorage.setItem(key, next); } catch (e) {}
                apply(next);
              };
            }

            var forgot = document.getElementById('forgot-password-link');
            if (!forgot) {
              var loginForm = document.getElementById('form-login');
              var loginBtn = document.getElementById('login-btn');
              if (loginForm && loginBtn) {
                forgot = document.createElement('div');
                forgot.id = 'forgot-password-link';
                forgot.textContent = 'Forgot password?';
                forgot.style.cssText = 'margin-top:10px;text-align:right;font-size:12px;color:var(--accent);cursor:pointer;font-weight:600;';
                loginBtn.insertAdjacentElement('afterend', forgot);
              }
            }

            if (forgot) {
              forgot.onclick = function() {
                var emailEl = document.getElementById('login-email');
                var email = (emailEl && emailEl.value || '').trim();
                if (!email) {
                  email = window.prompt('Enter your account email to receive a reset link:') || '';
                  email = email.trim();
                }
                if (!email) return;
                if (typeof window._anvilForgotPassword !== 'function') {
                  window.alert('Password reset service is not ready. Please try again.');
                  return;
                }
                Promise.resolve(window._anvilForgotPassword(email))
                  .then(function(result) {
                    var msg = (result && result.message) || 'If the account exists, a reset link has been sent.';
                    window.alert(msg);
                  })
                  .catch(function(err) {
                    window.alert('Could not send reset link: ' + err);
                  });
              };
            }
          })();
        """)

    # ─── BRIDGES ──────────────────────────────────────────────────
    def _handle_login(self, email, password):
        try:
            return anvil.server.call('login_user', str(email), str(password))
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _handle_signup(self, payload):
        try:
            return anvil.server.call('register_user', dict(payload))
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _handle_job_lookup(self, query):
        try:
            return anvil.server.call('lookup_job_ref', str(query))
        except Exception:
            return []

    def _handle_forgot_password(self, email):
        try:
            return anvil.server.call('request_password_reset', str(email))
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def _on_login_success(self, result):
        # Remove all auth assets
        anvil.js.call_js('eval', """
          ['garage-auth-root','garage-auth-css','garage-auth-js'].forEach(function(id) {
            var el = document.getElementById(id);
            if (el) el.remove();
          });
        """)
        job_ref = result.get('job_ref') if isinstance(result, dict) else None
        self._go_to_portal(job_ref=job_ref)

    def _go_to_portal(self, job_ref=None):
        from ..ClientPortalForm import ClientPortalForm
        open_form(ClientPortalForm(job_ref=job_ref))
