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
        anvil.js.window['_anvilPayHandler']       = self._js_pay_handler
        anvil.js.window['_anvilLogout']           = self._handle_logout
        anvil.js.window['_anvilGetCustomerJobs']  = self._get_customer_jobs
        anvil.js.window['_anvilSwitchJob']        = self._switch_job

        # 3. Inject JS (event listeners run immediately, bridges already on window)
        self._inject_js()
        self._inject_theme_layer()

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

    def _inject_theme_layer(self):
        anvil.js.call_js('eval', """
          (function() {
            var root = document.querySelector('#garage-portal-root .portal-root');
            if (!root) return;

            var cssId = 'garage-portal-theme-css';
            var style = document.getElementById(cssId);
            if (!style) {
              style = document.createElement('style');
              style.id = cssId;
              style.textContent = [
                '@font-face{font-family:\"PortalFont\";src:url(\"/_/theme/assets/fonts/MozillaHeadline.ttf\") format(\"truetype\");font-display:swap;}',
                '.portal-root,.portal-root *{font-family:\"PortalFont\",sans-serif!important;}',
                '.portal-root{font-size:16px!important;}',
                '.portal-root .data-value{font-size:16px!important;}',
                '.portal-root .portal-header{position:fixed!important;top:0;left:0;right:0;z-index:10001;}',
                '.portal-root .portal-inner{padding-top:84px!important;}',
                '.portal-root.theme-light .portal-header{background:rgba(245,247,251,0.95)!important;border-bottom:1px solid var(--border)!important;}',
                '.portal-root.theme-light .status-live{color:var(--green)!important;}',
                '.portal-root.theme-light{',
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
                '  --green-dim:rgba(14,159,110,0.14);',
                '  --orange:#d97706;',
                '  --orange-dim:rgba(217,119,6,0.14);',
                '  --blue:#2563eb;',
                '  --blue-dim:rgba(37,99,235,0.12);',
                '  --red:#dc2626;',
                '  --red-dim:rgba(220,38,38,0.12);',
                '  --purple:#7c3aed;',
                '  --purple-dim:rgba(124,58,237,0.12);',
                '}',
                '.portal-theme-toggle{',
                '  display:inline-flex;',
                '  align-items:center;',
                '  gap:8px;',
                '  padding:5px 10px;',
                '  border:1px solid var(--border);',
                '  border-radius:100px;',
                '  background:var(--surface-2);',
                '  color:var(--text-muted);',
                '  font-family:\\'PortalFont\\',sans-serif;',
                '  font-size:11px;',
                '  font-weight:600;',
                '}',
                '.portal-theme-toggle .lbl{opacity:.75;transition:opacity .2s,color .2s;}',
                '.portal-theme-toggle[data-theme=\"dark\"] .lbl-dark, .portal-theme-toggle[data-theme=\"light\"] .lbl-light{opacity:1;color:var(--text);}',
                '.portal-theme-switch{position:relative;display:inline-block;width:44px;height:24px;}',
                '.portal-theme-switch input{opacity:0;width:0;height:0;position:absolute;}',
                '.portal-theme-slider{position:absolute;inset:0;border-radius:100px;background:var(--border);cursor:pointer;transition:all .2s;}',
                '.portal-theme-slider::before{content:\"\";position:absolute;width:18px;height:18px;left:3px;top:3px;border-radius:50%;background:#fff;transition:transform .2s;}',
                '.portal-theme-switch input:checked + .portal-theme-slider{background:var(--accent);}',
                '.portal-theme-switch input:checked + .portal-theme-slider::before{transform:translateX(20px);}',
                '@media(max-width:700px){.portal-theme-toggle{padding:4px 7px;gap:6px;}.portal-theme-toggle .lbl{display:none;}.portal-theme-switch{width:38px;height:20px;}.portal-theme-slider::before{width:14px;height:14px;top:3px;left:3px;}.portal-theme-switch input:checked + .portal-theme-slider::before{transform:translateX(18px);}}'
              ].join('');
              document.head.appendChild(style);
            }

            var key = 'autocare-theme';
            var toggleWrap = document.getElementById('portal-theme-toggle-btn');
            if (!toggleWrap) {
              var right = document.querySelector('#garage-portal-root .ph-right');
              if (right) {
                toggleWrap = document.createElement('div');
                toggleWrap.id = 'portal-theme-toggle-btn';
                toggleWrap.className = 'portal-theme-toggle';
                toggleWrap.innerHTML =
                  '<span class=\"lbl lbl-dark\">Dark</span>' +
                  '<label class=\"portal-theme-switch\">' +
                    '<input id=\"portal-theme-toggle-input\" type=\"checkbox\" aria-label=\"Toggle light mode\">' +
                    '<span class=\"portal-theme-slider\"></span>' +
                  '</label>' +
                  '<span class=\"lbl lbl-light\">Light</span>';
                var logoutBtn = document.getElementById('portal-logout-btn');
                if (logoutBtn) right.insertBefore(toggleWrap, logoutBtn);
                else right.appendChild(toggleWrap);
              }
            }
            var toggleInput = document.getElementById('portal-theme-toggle-input');

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
          })();
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
            err = str(e)
            if 'No job found' in err:
                self._show_loading_message(
                    "No Service Job Yet",
                    "Your account was created successfully. Service details will appear here once your job is added in the back office."
                )
                return

            self._show_loading_message(
                "Could Not Load Service Data",
                "Please try again in a moment. If the issue continues, contact support."
            )
            alert(f"Could not load portal data: {e}")

    def _show_loading_message(self, title, message):
        import json
        title_json = json.dumps(str(title))
        message_json = json.dumps(str(message))
        anvil.js.call_js('eval', f"""
          (function() {{
            var loading = document.getElementById('loading');
            var content = document.getElementById('portal-content');
            if (content) content.style.display = 'none';
            if (!loading) return;

            loading.style.display = 'flex';
            loading.innerHTML =
              '<div style="max-width:560px;text-align:center;line-height:1.55">' +
                '<div style="font-family:\\'PortalFont\\',sans-serif;font-size:22px;color:var(--text);margin-bottom:10px">' + {title_json} + '</div>' +
                '<div style="font-size:14px;color:var(--text-muted)">' + {message_json} + '</div>' +
              '</div>';
          }})();
        """)

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

    # ── BRIDGE: get all jobs for this customer ───────────
    def _get_customer_jobs(self, job_ref):
        try:
            jobs = anvil.server.call('get_customer_jobs', str(job_ref))
            return jobs
        except Exception:
            return []

    # ── BRIDGE: switch to a different job ─────────────────
    def _switch_job(self, job_ref):
        self.job_ref = str(job_ref)
        import json
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
            err = str(e)
            if 'No job found' in err:
                self._show_loading_message(
                    "No Service Job Yet",
                    "Your account was created successfully. Service details will appear here once your job is added in the back office."
                )
                return

            anvil.js.call_js('eval', """
              var loading = document.getElementById('loading');
              var content = document.getElementById('portal-content');
              if (loading) loading.style.display = 'none';
              if (content) content.style.display = 'block';
            """)
            alert(f"Could not load job: {e}")

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
