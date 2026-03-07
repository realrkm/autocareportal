"""
FILE: ClientPortalForm.py  (Client-side Form)
═══════════════════════════════════════════════════════════════════
SETUP — No HTMLPanel needed. Uses anvil.js to inject HTML directly.

In Anvil designer:
  1. Create a new Blank Form → name it "ClientPortalForm"
  2. Leave the canvas completely EMPTY (no components needed)
  3. Paste this code into the form's Code view
  4. Done — the portal renders itself into the page body via JS
═══════════════════════════════════════════════════════════════════
"""

from ._anvil_designer import ClientPortalFormTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.js
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..client_portal_html import PORTAL_HTML


class ClientPortalForm(ClientPortalFormTemplate):
    def __init__(self, job_ref=None, **properties):
        self.init_components(**properties)

        # ── Determine which job to load
        # get_url_hash() returns a plain string in Anvil (e.g. "GRG-2025-0001")
        # get_url_hash_dict() returns a dict (e.g. {"ref": "GRG-2025-0001"})
        url_hash = get_url_hash()
        url_ref = None
        if isinstance(url_hash, dict):
            url_ref = url_hash.get('ref')
        elif isinstance(url_hash, str) and url_hash:
            url_ref = url_hash  # treat the whole hash as the job ref

        self.job_ref = job_ref or url_ref or None

        # ── Inject the portal HTML into the page
        self._inject_portal()

        # ── Register the Python payment handler so JS can call it
        anvil.js.window['_anvilPayHandler'] = self._js_pay_handler

        # ── Load data from server and push into the portal
        self.load_portal_data()

    # ─────────────────────────────────────────────
    # INJECT HTML INTO THE DOM
    # ─────────────────────────────────────────────
    def _inject_portal(self):
        """
        Writes the portal HTML into a wrapper div appended to
        the Anvil app's content area. Also injects the CSS fonts
        and styles if not already present.
        """
        anvil.js.call_js('eval', f"""
          (function() {{
            // Remove any previous portal instance
            var old = document.getElementById('garage-portal-root');
            if (old) old.remove();

            // Create wrapper
            var wrapper = document.createElement('div');
            wrapper.id = 'garage-portal-root';
            wrapper.style.cssText = 'position:relative;z-index:1;';
            wrapper.innerHTML = {repr(PORTAL_HTML)};

            // Mount into Anvil's content area (works for all themes)
            var target =
              document.querySelector('.content') ||
              document.querySelector('.anvil-measure-this') ||
              document.body;
            target.appendChild(wrapper);

            // Patch window.anvil so JS inside the portal can call Python
            window._portalMounted = true;
          }})();
        """)

    # ─────────────────────────────────────────────
    # LOAD DATA → SERVER → PUSH TO JS
    # ─────────────────────────────────────────────
    def load_portal_data(self):
        try:
            data = anvil.server.call('get_portal_data', self.job_ref)
            # Convert to a JS-friendly object and call populatePortal()
            anvil.js.call_js('eval', f"""
              (function() {{
                var data = {self._to_json(data)};
                if (typeof populatePortal === 'function') {{
                  populatePortal(data);
                }} else {{
                  // populatePortal lives inside the injected HTML's <script>
                  // Find it on the window scope after injection
                  var scripts = document.getElementById('garage-portal-root')
                                        .querySelectorAll('script');
                  scripts.forEach(function(s) {{
                    var clone = document.createElement('script');
                    clone.textContent = s.textContent;
                    document.head.appendChild(clone);
                  }});
                  if (typeof populatePortal === 'function') populatePortal(data);
                }}
              }})();
            """)
        except Exception as e:
            alert(f"Could not load portal data: {e}")

    # ─────────────────────────────────────────────
    # JS → PYTHON BRIDGE  (payment button)
    # ─────────────────────────────────────────────
    def _js_pay_handler(self, payment_method):
        """
        Called from JavaScript via window._anvilPayHandler(method).
        Returns a result string back to JS.
        """
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

    # ─────────────────────────────────────────────
    # HELPER: safely serialise a Python dict to JSON
    # ─────────────────────────────────────────────
    @staticmethod
    def _to_json(obj):
        import json
        def _clean(o):
            if isinstance(o, dict):
                return {str(k): _clean(v) for k, v in o.items()}
            elif isinstance(o, (list, tuple)):
                return [_clean(i) for i in o]
            elif hasattr(o, 'isoformat'):   # date / datetime
                return o.isoformat()
            elif o is None or isinstance(o, (bool, int, float, str)):
                return o
            else:
                return str(o)
        return json.dumps(_clean(obj))