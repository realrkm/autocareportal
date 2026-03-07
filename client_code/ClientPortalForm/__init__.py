"""
FILE: ClientPortalForm.py  (Client-side Form)
SETUP:
  1. Create a Blank Form -> name it "ClientPortalForm"
  2. Leave canvas EMPTY
  3. Paste this file into Code view
"""

from ._anvil_designer import ClientPortalFormTemplate
from anvil import *
import anvil.server
import anvil.js
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..client_portal_html import PORTAL_CSS, PORTAL_BODY, PORTAL_JS


class ClientPortalForm(ClientPortalFormTemplate):
    def __init__(self, job_ref=None, **properties):
        self.init_components(**properties)

        # Resolve job ref
        url_hash = get_url_hash()
        url_ref = None
        if isinstance(url_hash, dict):
            url_ref = url_hash.get('ref')
        elif isinstance(url_hash, str) and url_hash:
            url_ref = url_hash
        self.job_ref = job_ref or url_ref or None

        # 1. Inject CSS + HTML
        self._inject_html()

        # 2. Register Python bridges on window BEFORE JS runs
        anvil.js.window['_anvilPayHandler'] = self._js_pay_handler
        anvil.js.window['_anvilLogout']     = self._handle_logout

        # 3. Inject JS (event listeners run immediately, bridges already on window)
        self._inject_js()

        # 4. Load and push data
        self.load_portal_data()

    # ── STEP 1: CSS + HTML ────────────────────────────────
    def _inject_html(self):
        import json
        css_json  = json.dumps(PORTAL_CSS)
        body_json = json.dumps(PORTAL_BODY)

        anvil.js.call_js('eval', f"""
          (function() {{
            ['garage-portal-root','garage-portal-css','garage-portal-js'].forEach(function(id) {{
              var el = document.getElementById(id); if (el) el.remove();
            }});

            ['app-bar','nav-holder','left-nav','content','anvil-measure-this'].forEach(function(cls) {{
              document.querySelectorAll('.' + cls).forEach(function(el) {{
                el.style.setProperty('margin-top', '0', 'important');
                el.style.setProperty('padding-top', '0', 'important');
              }});
            }});

            var style = document.createElement('style');
            style.id = 'garage-portal-css';
            style.textContent = {css_json};
            document.head.appendChild(style);

            var wrapper = document.createElement('div');
            wrapper.id = 'garage-portal-root';
            wrapper.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;overflow-y:auto;overflow-x:hidden;z-index:9999;background:#0d0f14';
            wrapper.innerHTML = {body_json};
            document.body.appendChild(wrapper);
          }})();
        """)

    # ── STEP 3: JS (bridges already set) ─────────────────
    def _inject_js(self):
        import json
        js_json = json.dumps(PORTAL_JS)

        anvil.js.call_js('eval', f"""
          (function() {{
            var script = document.createElement('script');
            script.id = 'garage-portal-js';
            script.textContent = {js_json};
            document.body.appendChild(script);
          }})();
        """)

    # ── STEP 4: load data and push to JS ─────────────────
    def load_portal_data(self):
        try:
            data = anvil.server.call('get_portal_data', self.job_ref)
            data_json = self._to_json(data)
            anvil.js.call_js('eval', f"""
              (function() {{
                if (typeof populatePortal === 'function') {{
                  populatePortal({data_json});
                }}
              }})();
            """)
        except Exception as e:
            alert(f"Could not load portal data: {e}")

    # ── BRIDGE: logout ────────────────────────────────────
    def _handle_logout(self):
        try:
            anvil.server.call('logout_user')
        except Exception:
            pass
        anvil.js.call_js('eval', """
          ['garage-portal-root','garage-portal-css','garage-portal-js'].forEach(function(id) {
            var el = document.getElementById(id); if (el) el.remove();
          });
        """)
        from ..AuthForm import AuthForm
        open_form(AuthForm())

    # ── BRIDGE: payment ───────────────────────────────────
    def _js_pay_handler(self, payment_method):
        try:
            result = anvil.server.call(
                'initiate_payment',
                job_ref=self.job_ref,
                method=str(payment_method)
            )
            if result.get('redirect_url'):
                open_url(result['redirect_url'], new_tab=True)
            return result.get('message', 'Payment initiated successfully!')
        except Exception as e:
            raise Exception(str(e))

    # ── HELPER: safe JSON serialisation ──────────────────
    @staticmethod
    def _to_json(obj):
        import json
        def _clean(o):
            if isinstance(o, dict):
                return {str(k): _clean(v) for k, v in o.items()}
            elif isinstance(o, (list, tuple)):
                return [_clean(i) for i in o]
            elif hasattr(o, 'isoformat'):
                return o.isoformat()
            elif o is None or isinstance(o, (bool, int, float, str)):
                return o
            else:
                return str(o)
        return json.dumps(_clean(obj))