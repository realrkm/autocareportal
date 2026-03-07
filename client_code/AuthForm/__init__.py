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

        # 3. Now run the JS (bridges already on window, addEventListener safe)
        self._inject_js()

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