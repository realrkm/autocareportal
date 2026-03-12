"""
FILE: client_portal_html.py  (Client Module)
Three constants: PORTAL_CSS, PORTAL_BODY, PORTAL_JS
"""

# ---------------------------------------------------------------------------
# PORTAL_CSS
# Styles for the client portal. Injected into <head> via ClientPortalForm.py
# ---------------------------------------------------------------------------
PORTAL_CSS = """
:root {
  --bg: #0d0f14;
  --surface: #13161d;
  --surface-2: #1a1e28;
  --border: #252a38;
  --accent: #e8ff47;
  --accent-dim: rgba(232,255,71,0.12);
  --accent-glow: rgba(232,255,71,0.25);
  --text: #f0f2f8;
  --text-muted: #6b7394;
  --text-mid: #9da3bf;
  --green: #3dffa0;
  --green-dim: rgba(61,255,160,0.12);
  --orange: #ff8c42;
  --orange-dim: rgba(255,140,66,0.12);
  --blue: #4da8ff;
  --blue-dim: rgba(77,168,255,0.12);
  --red: #ff4d6d;
  --red-dim: rgba(255,77,109,0.12);
  --purple: #b87fff;
  --purple-dim: rgba(184,127,255,0.12);
  --radius: 16px;
  --radius-sm: 10px;
}
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
body, .portal-root {
  background: var(--bg);
  color: var(--text);
  font-family: 'PortalFont', sans-serif;
  font-size: 14px;
}
.portal-root {
  padding: 0;
  min-height: 100vh;
  position: relative;
}
.portal-root::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
  linear-gradient(rgba(232,255,71,0.03) 1px, transparent 1px),
  linear-gradient(90deg, rgba(232,255,71,0.03) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
  z-index: 0;
}
.portal-inner {
  position: relative;
  z-index: 1;
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px;
}
/* LOADING STATE */
.loading-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  gap: 16px;
  color: var(--text-muted);
  font-size: 14px;
}
.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {to {
    transform: rotate(360deg);
  }
}/* HERO */
.hero {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: end;
  gap: 24px;
  margin-bottom: 32px;
  animation: slideUp 0.4s ease both;
}
.hero-greeting {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 6px;
}
.hero-title {
  font-family: 'PortalFont', sans-serif;
  font-weight: 800;
  font-size: clamp(24px,4vw,38px);
  line-height: 1.1;
  letter-spacing: -1px;
}
.hero-title span {
  color: var(--accent);
}
.hero-sub {
  margin-top: 8px;
  color: var(--text-muted);
  font-size: 13px;
}
.vehicle-chip {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 20px;
  text-align: right;
  white-space: nowrap;
}
.vc-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-muted);
  margin-bottom: 3px;
}
.vc-plate {
  font-family: 'PortalFont', sans-serif;
  font-weight: 700;
  font-size: 20px;
  color: var(--accent);
  letter-spacing: 3px;
}
.vc-model {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}
/* PROGRESS TRACK */
.progress-track {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 28px;
  margin-bottom: 28px;
  overflow-x: auto;
  animation: slideUp 0.4s ease 0.1s both;
}
.track-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--text-muted);
  margin-bottom: 18px;
  font-weight: 500;
}
.steps {
  display: flex;
  align-items: center;
  min-width: 500px;
}
.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 7px;
  flex: 1;
  position: relative;
}
.step:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 17px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: var(--border);
  z-index: 0;
}
.step.done:not(:last-child)::after {
  background: var(--accent);
}
.step.active:not(:last-child)::after {
  background: linear-gradient(90deg, var(--accent), var(--border));
}
.step-dot {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  z-index: 1;
  position: relative;
  transition: all 0.3s;
}
.step.done .step-dot {
  background: var(--accent);
  border-color: var(--accent);
  color: #000;
  font-weight: 700;
}
.step.active .step-dot {
  background: var(--accent-dim);
  border-color: var(--accent);
  color: var(--accent);
  box-shadow: 0 0 0 4px var(--accent-glow);
}
.step-name {
  font-size: 10px;
  font-weight: 500;
  color: var(--text-muted);
  text-align: center;
}
.step.done .step-name, .step.active .step-name {
  color: var(--text);
}
/* TABS */
.tabs-wrap {
  display: flex;
  gap: 4px;
  margin-bottom: 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 5px;
  overflow-x: auto;
  animation: slideUp 0.4s ease 0.15s both;
}
.tab-btn {
  flex: 1;
  min-width: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 9px 14px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-family: 'PortalFont', sans-serif;
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.tab-btn:hover {
  color: var(--text);
  background: var(--surface-2);
}
.tab-btn.active {
  background: var(--accent);
  color: #000;
  font-weight: 600;
}
/* PANELS */
.panel {
  display: none;
  animation: fadeIn 0.3s ease;
}
.panel.active {
  display: block;
}

@keyframes fadeIn {from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes slideUp {from {
    opacity: 0;
    transform: translateY(18px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}/* CARD */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  margin-bottom: 18px;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 22px;
  border-bottom: 1px solid var(--border);
}
.card-title {
  font-family: 'PortalFont', sans-serif;
  font-weight: 700;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 9px;
}
.card-title-icon {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}
.card-body {
  padding: 22px;
}
/* DATA GRID */
.data-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}
.data-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: var(--text-muted);
  margin-bottom: 4px;
  font-weight: 500;
}
.data-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
}
.data-value.highlight {
  color: var(--accent);
  font-family: 'PortalFont', sans-serif;
  font-size: 16px;
  font-weight: 700;
}
/* TABLE */
.table-wrap {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
}
thead tr {
  background: var(--surface-2);
}
th {
  text-align: left;
  padding: 11px 14px;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: var(--text-muted);
  font-weight: 600;
  border-bottom: 1px solid var(--border);
}
td {
  padding: 13px 14px;
  border-bottom: 1px solid var(--border);
  color: var(--text);
  font-size: 13px;
}
tr:last-child td {
  border-bottom: none;
}
tr:hover td {
  background: rgba(255,255,255,0.015);
}
.td-mono {
  font-family: 'PortalFont', sans-serif;
  font-weight: 600;
  font-size: 12px;
}
.tr-right {
  text-align: right;
}
/* BADGE */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 9px;
  border-radius: 100px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.4px;
}
.badge-green {
  background: var(--green-dim);
  color: var(--green);
}
.badge-orange {
  background: var(--orange-dim);
  color: var(--orange);
}
.badge-blue {
  background: var(--blue-dim);
  color: var(--blue);
}
.badge-accent {
  background: var(--accent-dim);
  color: var(--accent);
}
.badge-red {
  background: var(--red-dim);
  color: var(--red);
}
.badge-purple {
  background: var(--purple-dim);
  color: var(--purple);
}
/* TOTALS */
.totals-section {
  margin-top: 14px;
  border-top: 1px solid var(--border);
  padding-top: 14px;
}
.total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 0;
  color: var(--text-mid);
  font-size: 13px;
}
.total-row.grand {
  margin-top: 10px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
  color: var(--text);
  font-family: 'PortalFont', sans-serif;
  font-weight: 700;
  font-size: 17px;
}
.total-row.grand .amount {
  color: var(--accent);
}
/* STATS */
.stat-row {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}
.stat-block {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 14px;
}
.stat-num {
  font-family: 'PortalFont', sans-serif;
  font-weight: 800;
  font-size: 20px;
  line-height: 1;
  margin-bottom: 4px;
}
.stat-lbl {
  font-size: 10px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
}
/* TIMELINE */
.timeline {
  padding-left: 4px;
}
.timeline-item {
  display: flex;
  gap: 14px;
  padding-bottom: 22px;
  position: relative;
}
.timeline-item:not(:last-child)::before {
  content: '';
  position: absolute;
  left: 15px;
  top: 32px;
  bottom: 0;
  width: 1px;
  background: var(--border);
}
.tl-dot {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  z-index: 1;
}
.tl-time {
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 2px;
}
.tl-title {
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 3px;
}
.tl-desc {
  font-size: 12px;
  color: var(--text-mid);
  line-height: 1.5;
}
/* TECH NOTE */
.tech-note {
  background: var(--surface-2);
  border-left: 3px solid var(--blue);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  padding: 12px 16px;
  font-size: 12px;
  color: var(--text-mid);
  line-height: 1.6;
}
/* PROGRESS BAR */
.prog-bar-bg {
  background: var(--surface-2);
  border-radius: 100px;
  height: 8px;
  overflow: hidden;
  margin-bottom: 22px;
}
.prog-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--green));
  border-radius: 100px;
  transition: width 1s ease;
}
/* DIVIDER LABEL */
.divider-label {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 20px 0 14px;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-muted);
  font-weight: 500;
}
.divider-label::before, .divider-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}
/* PAYMENT */
.payment-methods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
  margin-bottom: 20px;
}
.payment-method-card {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s;
}
.payment-method-card:hover {
  border-color: var(--accent);
  background: var(--accent-dim);
}
.payment-method-card.selected {
  border-color: var(--accent);
  background: var(--accent-dim);
  box-shadow: 0 0 0 1px var(--accent);
}
.pm-icon {
  width: 40px;
  height: 40px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  background: var(--surface);
  flex-shrink: 0;
}
.pm-name {
  font-weight: 600;
  font-size: 13px;
}
.pm-desc {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}
.pm-radio {
  margin-left: auto;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: transparent;
  transition: all 0.2s;
  flex-shrink: 0;
}
.payment-method-card.selected .pm-radio {
  border-color: var(--accent);
  background: var(--accent);
}
.balance-box {
  background: var(--surface-2);
  border-radius: var(--radius-sm);
  padding: 16px 20px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  border: 1px solid var(--border);
}
.bal-label {
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 3px;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.bal-amount {
  font-family: 'PortalFont', sans-serif;
  font-weight: 800;
  font-size: 26px;
  color: var(--accent);
}
.pay-btn {
  width: 100%;
  padding: 15px;
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
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.pay-btn:hover {
  background: #f5ff72;
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(232,255,71,0.3);
}
.pay-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}
/* ── PORTAL HEADER BAR ── */
.portal-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(13,15,20,0.9);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
}
.portal-header-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.ph-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'PortalFont', sans-serif;
  font-weight: 800;
  font-size: 16px;
  color: var(--text);
}
.ph-logo-mark {
  width: 30px;
  height: 30px;
  background: var(--accent);
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #000;
}
.ph-right {
  display: flex;
  align-items: center;
  gap: 14px;
}
.ph-user {
  display: flex;
  align-items: center;
  gap: 10px;
}
.ph-user-avatar {
  width: 32px;
  height: 32px;
  background: var(--accent);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'PortalFont', sans-serif;
  font-weight: 800;
  font-size: 14px;
  color: #000;
  flex-shrink: 0;
}
.ph-user-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  line-height: 1.2;
}
.ph-user-email {
  font-size: 11px;
  color: var(--text-muted);
}
.ph-sep {
  width: 1px;
  height: 24px;
  background: var(--border);
}
.ref-badge {
  font-family: 'PortalFont', sans-serif;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  background: var(--surface-2);
  border: 1px solid var(--border);
  padding: 5px 12px;
  border-radius: 100px;
  letter-spacing: 0.5px;
}
.status-live {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 500;
  color: var(--green);
}
.status-live::before {
  content: '';
  width: 6px;
  height: 6px;
  background: var(--green);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {0%,100% {
    box-shadow: 0 0 0 0 rgba(61,255,160,0.4);
  }
  50% {
    box-shadow: 0 0 0 5px rgba(61,255,160,0);
  }

}.logout-btn {
  padding: 7px 14px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 100px;
  color: var(--text-muted);
  font-family: 'PortalFont', sans-serif;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.logout-btn:hover {
  border-color: var(--red);
  color: var(--red);
  background: var(--red-dim);
}

@media(max-width:600px) {.ph-user-info, .ph-sep, .ref-badge, .status-live {
    display: none;
  }
  .portal-header-inner {
    padding: 0 16px;
  }

}::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 3px;
}

@media(max-width:600px) {.hero {
    grid-template-columns: 1fr;
  }
  .vehicle-chip {
    text-align: left;
  }
  .data-grid {
    grid-template-columns: 1fr 1fr;
  }

}/* ── JOB SWITCHER ── */
.job-switcher-wrap {
  position: relative;
}
.job-switcher-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px 6px 10px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 100px;
  color: var(--text);
  font-family: 'PortalFont', sans-serif;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.job-switcher-btn:hover {
  border-color: var(--accent);
}
.job-switcher-btn.open {
  border-color: var(--accent);
  background: var(--accent-dim);
}
.job-switcher-icon {
  font-size: 13px;
}
.job-switcher-caret {
  font-size: 9px;
  color: var(--text-muted);
  transition: transform 0.2s;
}
.job-switcher-btn.open .job-switcher-caret {
  transform: rotate(180deg);
}
.job-dropdown {
  display: none;
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 340px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  z-index: 9999;
  overflow: hidden;
  animation: dropIn 0.2s cubic-bezier(0.22,1,0.36,1);
}
.job-dropdown.open {
  display: block;
}

@keyframes dropIn {from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }

}.jd-header {
  padding: 14px 16px 10px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border);
}
.jd-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.15s;
  border-bottom: 1px solid var(--border);
  text-decoration: none;
}
.jd-item:last-child {
  border-bottom: none;
}
.jd-item:hover {
  background: var(--surface-2);
}
.jd-item.active {
  background: var(--accent-dim);
}
.jd-step-dot {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
}
.jd-info {
  flex: 1;
  min-width: 0;
}
.jd-ref {
  font-family: 'PortalFont', sans-serif;
  font-weight: 700;
  font-size: 12px;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 6px;
}
.jd-vehicle {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 1px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.jd-right {
  text-align: right;
  flex-shrink: 0;
}
.jd-date {
  font-size: 10px;
  color: var(--text-muted);
}
.jd-status {
  font-size: 10px;
  font-weight: 600;
  margin-top: 3px;
}
.jd-loading {
  padding: 20px;
  text-align: center;
  font-size: 12px;
  color: var(--text-muted);
}

@media(max-width:600px) {.ph-user-info, .ph-sep, .ref-badge, .status-live {
    display: none;
  }
  .portal-header-inner {
    padding: 0 10px;
  }
  .portal-inner {
    padding: 14px;
  }
  .hero {
    grid-template-columns: 1fr;
    gap: 12px;
    margin-bottom: 18px;
  }
  .hero-sub {
    font-size: 12px;
  }
  .vehicle-chip {
    text-align: left;
    padding: 12px 14px;
  }
  .data-grid {
    grid-template-columns: 1fr;
  }
  .card-header {
    padding: 12px 14px;
    gap: 8px;
    align-items: flex-start;
  }
  .card-body {
    padding: 14px;
  }
  .progress-track {
    padding: 14px 12px;
    margin-bottom: 16px;
  }
  .tabs-wrap {
    position: sticky;
    top: 66px;
    z-index: 90;
    background: rgba(13,15,20,0.95);
    backdrop-filter: blur(12px);
  }
  .payment-methods-grid {
    grid-template-columns: 1fr;
  }
  .job-dropdown {
    width: calc(100vw - 20px);
    right: -6px;
    max-height: 60vh;
    overflow-y: auto;
  }
  .ph-right {
    gap: 8px;
    max-width: 72vw;
    overflow-x: auto;
    padding-bottom: 2px;
    scrollbar-width: none;
  }
  .ph-right::-webkit-scrollbar {
    display: none;
  }
  .job-switcher-btn {
    padding: 7px 10px;
    font-size: 11px;
    max-width: 190px;
  }
  #job-switcher-label {
    max-width: 112px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: inline-block;
    vertical-align: bottom;
  }
  .logout-btn {
    padding: 7px 10px;
    font-size: 11px;
  }

}

@media(max-width:420px) {.ph-logo span {
    font-size: 13px;
  }
  .ph-logo-mark {
    width: 26px;
    height: 26px;
    font-size: 12px;
  }
  .hero-title {
    font-size: clamp(22px, 9vw, 30px);
  }
  .steps {
    min-width: 540px;
  }
  .tab-btn {
    min-width: 96px;
    padding: 8px 10px;
  }

}
"""


# ---------------------------------------------------------------------------
# PORTAL_BODY
# HTML markup for the portal overlay (header bar + all tab panels).
# No onclick attributes — all events are wired in PORTAL_JS via addEventListener.
# ---------------------------------------------------------------------------
PORTAL_BODY = """
<div class="portal-root">

  <!-- PORTAL HEADER BAR -->
  <div class="portal-header">
    <div class="portal-header-inner">
      <div class="ph-logo">
        <div class="ph-logo-mark">⚙</div>
        <span>AutoCare Portal</span>
      </div>
      <div class="ph-right">
        <div class="ph-user" id="ph-user">
          <div class="ph-user-avatar" id="ph-avatar">J</div>
          <div class="ph-user-info">
            <div class="ph-user-name" id="ph-user-name">—</div>
            <div class="ph-user-email" id="ph-user-email">—</div>
          </div>
        </div>
        <div class="ph-sep"></div>
        <div class="status-live">Active</div>
        <div class="job-switcher-wrap" id="job-switcher-wrap">
          <button class="job-switcher-btn" id="job-switcher-btn">
            <span class="job-switcher-icon">📋</span>
            <span id="job-switcher-label">REF# —</span>
            <span class="job-switcher-caret">▼</span>
          </button>
          <div class="job-dropdown" id="job-dropdown">
            <div class="jd-header">Your Service Jobs</div>
            <div id="jd-items"><div class="jd-loading">Loading jobs...</div></div>
          </div>
        </div>
        <button class="logout-btn" id="portal-logout-btn">⏻ Sign Out</button>
      </div>
    </div>
  </div>

<div class="portal-inner">

  <!-- Loading state -->
  <div id="loading" class="loading-overlay">
    <div class="spinner"></div>
    <span>Loading your service details...</span>
  </div>

  <!-- Main content (hidden until data arrives) -->
  <div id="portal-content" style="display:none">

    <!-- HERO -->
    <div class="hero">
      <div>
        <div class="hero-greeting">Welcome back</div>
        <div class="hero-title" id="hero-name">— —</div>
        <div class="hero-sub" id="hero-sub">Loading service information...</div>
      </div>
      <div class="vehicle-chip">
        <div class="vc-label">Vehicle</div>
        <div class="vc-plate" id="vehicle-plate">—</div>
        <div class="vc-model" id="vehicle-model">—</div>
      </div>
    </div>

    <!-- PROGRESS TRACK -->
    <div class="progress-track">
      <div class="track-label">Service Progress</div>
      <div class="steps" id="progress-steps">
        <!-- Populated by JS -->
      </div>
    </div>

    <!-- TABS -->
    <div class="tabs-wrap">
      <button class="tab-btn active" id="tab-btn-checkin" data-panel="checkin">📋 Check-In</button>
      <button class="tab-btn" id="tab-btn-quotation" data-panel="quotation">📄 Quotation</button>
      <button class="tab-btn" id="tab-btn-service" data-panel="service">🔧 Service</button>
      <button class="tab-btn" id="tab-btn-invoice" data-panel="invoice">🧾 Invoice</button>
      <button class="tab-btn" id="tab-btn-payment" data-panel="payment">💳 Payment</button>
    </div>

    <!-- ── CHECK-IN ── -->
    <div class="panel active" id="panel-checkin">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><div class="card-title-icon" style="background:var(--green-dim);color:var(--green)">📋</div>Check-In Details</div>
          <span class="badge badge-green">✓ Completed</span>
        </div>
        <div class="card-body">
          <div class="data-grid" id="checkin-grid"><!-- populated --></div>
          <div style="margin-top:18px" id="checkin-complaint-wrap">
            <div class="tech-note" id="checkin-complaint"></div>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="card-title"><div class="card-title-icon" style="background:var(--blue-dim);color:var(--blue)">👤</div>Customer Information</div>
        </div>
        <div class="card-body">
          <div class="data-grid" id="customer-grid"><!-- populated --></div>
        </div>
      </div>
    </div>

    <!-- ── QUOTATION ── -->
    <div class="panel" id="panel-quotation">
      <div class="stat-row" id="quote-stats"><!-- populated --></div>
      <div class="card">
        <div class="card-header">
          <div class="card-title"><div class="card-title-icon" style="background:var(--accent-dim);color:var(--accent)">📄</div><span id="quote-title">Quotation</span></div>
          <span class="badge" id="quote-status-badge">—</span>
        </div>
        <div class="card-body">
          <div class="table-wrap">
            <table>
              <thead><tr><th>#</th><th>Description</th><th>Type</th><th class="tr-right">Qty</th><th class="tr-right">Unit</th><th class="tr-right">Total</th></tr></thead>
              <tbody id="quote-items"><!-- populated --></tbody>
            </table>
          </div>
          <div class="totals-section" id="quote-totals"><!-- populated --></div>
        </div>
      </div>
    </div>

    <!-- ── SERVICE ── -->
    <div class="panel" id="panel-service">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><div class="card-title-icon" style="background:var(--orange-dim);color:var(--orange)">🔧</div>Service Status</div>
          <span class="badge badge-accent" id="service-status-badge">⚡ In Progress</span>
        </div>
        <div class="card-body">
          <div class="data-grid" id="service-grid"><!-- populated --></div>
          <div style="margin-top:18px">
            <div class="prog-bar-bg"><div class="prog-bar-fill" id="service-prog-bar" style="width:0%"></div></div>
          </div>
          <div class="divider-label">Service Timeline</div>
          <div class="timeline" id="service-timeline"><!-- populated --></div>
          <div id="service-notes-wrap" style="margin-top:8px"><!-- populated --></div>
        </div>
      </div>
    </div>

    <!-- ── INVOICE ── -->
    <div class="panel" id="panel-invoice">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><div class="card-title-icon" style="background:var(--accent-dim);color:var(--accent)">🧾</div><span id="invoice-title">Invoice</span></div>
          <span class="badge" id="invoice-status-badge">—</span>
        </div>
        <div class="card-body">
          <div class="data-grid" id="invoice-grid"><!-- populated --></div>
          <div style="margin-top:20px" class="table-wrap">
            <table>
              <thead><tr><th>Description</th><th class="tr-right">Qty</th><th class="tr-right">Unit</th><th class="tr-right">Total</th></tr></thead>
              <tbody id="invoice-items"><!-- populated --></tbody>
            </table>
          </div>
          <div class="totals-section" id="invoice-totals"><!-- populated --></div>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="card-title"><div class="card-title-icon" style="background:var(--green-dim);color:var(--green)">🏢</div>Billed By</div>
        </div>
        <div class="card-body">
          <div class="data-grid" id="biller-grid"><!-- populated --></div>
        </div>
      </div>
    </div>

    <!-- ── PAYMENT ── -->
    <div class="panel" id="panel-payment">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><div class="card-title-icon" style="background:var(--red-dim);color:var(--red)">💳</div>Payment</div>
          <span class="badge" id="payment-status-badge">—</span>
        </div>
        <div class="card-body">
          <div class="balance-box">
            <div>
              <div class="bal-label">Balance Remaining</div>
              <div class="bal-amount" id="balance-amount">—</div>
            </div>
            <div style="text-align:right">
              <div class="bal-label">Deposit Paid</div>
              <div style="font-weight:600;color:var(--green);font-size:15px" id="deposit-amount">—</div>
            </div>
          </div>
          <div class="divider-label">Choose Payment Method</div>
          <div class="payment-methods-grid" id="payment-methods"><!-- populated --></div>
          <div id="payment-method-info" style="margin-bottom:14px"></div>
          <button class="pay-btn" id="pay-btn">
            ⚡ Pay Now
          </button>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="card-title"><div class="card-title-icon" style="background:var(--green-dim);color:var(--green)">📊</div>Payment History</div>
        </div>
        <div class="card-body">
          <div class="table-wrap">
            <table>
              <thead><tr><th>Date</th><th>Method</th><th>Reference</th><th class="tr-right">Amount</th><th>Status</th></tr></thead>
              <tbody id="payment-history"><!-- populated --></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

  </div><!-- /portal-content -->
</div>
</div>
"""


# ---------------------------------------------------------------------------
# PORTAL_JS
# All portal interactivity: job switcher, tab switching, payment method
# selection, pay button handler, and the main populatePortal() function
# called from Python after data is loaded.
# ---------------------------------------------------------------------------
PORTAL_JS = """
// ── JOB SWITCHER ──────────────────────────────────────────────
var _jobSwitcherLoaded = false;
var _currentJobRef = null;
var _jobSwitcherWired = false;

function initJobSwitcher(jobRef) {
  _currentJobRef = jobRef;
  var btn       = document.getElementById('job-switcher-btn');
  var dropdown  = document.getElementById('job-dropdown');
  var label     = document.getElementById('job-switcher-label');

  if (label) label.textContent = 'REF# ' + jobRef;

  if (!btn || !dropdown) return;
  if (_jobSwitcherWired) return;

  _jobSwitcherWired = true;

  // Toggle open/close
  btn.addEventListener('click', function(e) {
    e.stopPropagation();
    var isOpen = dropdown.classList.contains('open');
    if (!isOpen) {
      dropdown.classList.add('open');
      btn.classList.add('open');
      if (!_jobSwitcherLoaded) loadJobList();
    } else {
      closeJobSwitcher();
    }
  });

  // Close on outside click
  document.addEventListener('click', function(e) {
    var wrap = document.getElementById('job-switcher-wrap');
    if (wrap && !wrap.contains(e.target)) closeJobSwitcher();
  });
}

function closeJobSwitcher() {
  var btn      = document.getElementById('job-switcher-btn');
  var dropdown = document.getElementById('job-dropdown');
  if (btn)      btn.classList.remove('open');
  if (dropdown) dropdown.classList.remove('open');
}

function loadJobList() {
  if (typeof window._anvilGetCustomerJobs !== 'function') return;
  Promise.resolve(window._anvilGetCustomerJobs(_currentJobRef))
    .then(function(jobs) {
      _jobSwitcherLoaded = true;
      renderJobList(jobs);
    })
    .catch(function() {
      var el = document.getElementById('jd-items');
      if (el) el.innerHTML = '<div class="jd-loading" style="color:var(--red)">Could not load jobs.</div>';
    });
}

function renderJobList(jobs) {
  var el = document.getElementById('jd-items');
  if (!el) return;
  if (!jobs || jobs.length === 0) {
    el.innerHTML = '<div class="jd-loading">No other jobs found.</div>';
    return;
  }

  var colorMap = {
    green:  {bg: 'var(--green-dim)',  color: 'var(--green)'},
    accent: {bg: 'var(--accent-dim)', color: 'var(--accent)'},
    orange: {bg: 'var(--orange-dim)', color: 'var(--orange)'},
    blue:   {bg: 'var(--blue-dim)',   color: 'var(--blue)'},
    red:    {bg: 'var(--red-dim)',     color: 'var(--red)'},
  };

  el.innerHTML = jobs.map(function(j) {
    var c = colorMap[j.badge_color] || colorMap.blue;
    var isCurrent = j.job_ref === _currentJobRef;
    return '<div class="jd-item' + (isCurrent ? ' active' : '') + '" ' +
           'id="jd-' + j.job_ref + '" ' +
           'data-ref="' + j.job_ref + '">' +
      '<div class="jd-step-dot" style="background:' + c.bg + ';color:' + c.color + '">' +
        j.step +
      '</div>' +
      '<div class="jd-info">' +
        '<div class="jd-ref">' +
          j.job_ref +
          (isCurrent ? ' <span style="font-size:9px;background:var(--accent);color:#000;padding:1px 6px;border-radius:100px">current</span>' : '') +
        '</div>' +
        '<div class="jd-vehicle">' + j.vehicle_plate + ' · ' + j.vehicle_model + '</div>' +
      '</div>' +
      '<div class="jd-right">' +
        '<div class="jd-date">' + j.date + '</div>' +
        '<div class="jd-status" style="color:' + c.color + '">' + j.status + '</div>' +
      '</div>' +
    '</div>';
  }).join('');

  // Wire click events
  jobs.forEach(function(j) {
    var item = document.getElementById('jd-' + j.job_ref);
    if (item) {
      item.addEventListener('click', function() {
        if (j.job_ref === _currentJobRef) { closeJobSwitcher(); return; }
        switchToJob(j.job_ref);
      });
    }
  });
}

function switchToJob(jobRef) {
  closeJobSwitcher();
  // Show loading overlay
  var content = document.getElementById('portal-content');
  var loading = document.getElementById('loading');
  if (content) content.style.display = 'none';
  if (loading) loading.style.display = 'flex';

  if (typeof window._anvilSwitchJob === 'function') {
    window._anvilSwitchJob(jobRef);
  }
}


// ── WIRE ALL INTERACTIVE ELEMENTS ─────────────────────
(function wirePortal() {
  // Logout
  var logoutBtn = document.getElementById('portal-logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function() {
      if (typeof window._anvilLogout === 'function') window._anvilLogout();
    });
  }

  // Tabs
  var tabBtns = document.querySelectorAll('.tab-btn[data-panel]');
  tabBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var panel = btn.getAttribute('data-panel');
      document.querySelectorAll('.panel').forEach(function(p)    { p.classList.remove('active'); });
      document.querySelectorAll('.tab-btn').forEach(function(b)  { b.classList.remove('active'); });
      var panelEl = document.getElementById('panel-' + panel);
      if (panelEl) panelEl.classList.add('active');
      btn.classList.add('active');
    });
  });

  // Pay button
  var payBtn = document.getElementById('pay-btn');
  if (payBtn) {
    payBtn.addEventListener('click', handlePay);
  }
})();

// ─────────────────────────────────────────────
// TAB SWITCHING
// ─────────────────────────────────────────────
// ── LOGOUT
function doLogout() {
  if (typeof window._anvilLogout === 'function') {
    window._anvilLogout();
  }
}

function showTab(name, btn) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('panel-' + name).classList.add('active');
  btn.classList.add('active');
}

// ─────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────
function dataItem(label, value, highlight) {
  return `<div class="data-item">
    <div class="data-label">${label}</div>
    <div class="data-value${highlight ? ' highlight' : ''}">${value}</div>
  </div>`;
}

function statBlock(num, lbl, color) {
  return `<div class="stat-block"><div class="stat-num" style="color:${color}">${num}</div><div class="stat-lbl">${lbl}</div></div>`;
}

function totalRow(label, value, colorStyle, isGrand) {
  return `<div class="total-row${isGrand ? ' grand' : ''}" ${colorStyle ? `style="${colorStyle}"` : ''}>
    <span>${label}</span><span class="${isGrand ? 'amount' : ''}">${value}</span>
  </div>`;
}

function badgeHtml(text, cls) {
  return `<span class="badge badge-${cls}">${text}</span>`;
}

// ─────────────────────────────────────────────
// PAYMENT METHOD SELECTION
// ─────────────────────────────────────────────
var selectedPaymentMethod = null;
var paymentMethodsData = [];

function selectPM(index) {
  selectedPaymentMethod = paymentMethodsData[index];
  document.querySelectorAll('.payment-method-card').forEach((c,i) => {
    c.classList.toggle('selected', i === index);
  });
  var infoDiv = document.getElementById('payment-method-info');
  if (selectedPaymentMethod.instructions) {
    infoDiv.innerHTML = `<div class="tech-note" style="border-color:var(--green)">${selectedPaymentMethod.instructions}</div>`;
  } else {
    infoDiv.innerHTML = '';
  }
  var payBtn = document.getElementById('pay-btn');
  var bal = document.getElementById('balance-amount').textContent;
  payBtn.innerHTML = `⚡ Pay ${bal} via ${selectedPaymentMethod.name}`;
}

// ─────────────────────────────────────────────
// PAY BUTTON
// ─────────────────────────────────────────────
function handlePay() {
  if (!selectedPaymentMethod) {
    alert('Please select a payment method first.');
    return;
  }
  var btn = document.getElementById('pay-btn');
  btn.disabled = true;
  btn.textContent = '⏳ Processing...';
  // Call back to Anvil Python via handler registered in ClientPortalForm
  try {
    if (typeof window._anvilPayHandler === 'function') {
      var result = window._anvilPayHandler(selectedPaymentMethod.name);
      Promise.resolve(result).then(function(msg) {
        btn.textContent = '✓ ' + (msg || 'Payment initiated!');
        btn.style.background = 'var(--green)';
      }).catch(function(err) {
        btn.disabled = false;
        btn.textContent = '⚡ Pay Now';
        alert('Payment failed: ' + err);
      });
    } else {
      btn.textContent = '✓ Request sent — check your phone / email.';
      btn.style.background = 'var(--green)';
    }
  } catch(err) {
    btn.disabled = false;
    btn.textContent = '⚡ Pay Now';
    alert('Payment error: ' + err);
  }
}

// ─────────────────────────────────────────────
// MAIN POPULATE FUNCTION — called from Python
// ─────────────────────────────────────────────
function populatePortal(data) {
  document.getElementById('loading').style.display = 'none';
  document.getElementById('portal-content').style.display = 'block';

  var ci = data.checkin;
  var qt = data.quotation;
  var sv = data.service;
  var inv = data.invoice;
  var pay = data.payment;

  // ── HERO
  var nameParts = ci.customer_name.split(' ');
  var firstName = nameParts[0];
  var lastName = nameParts.slice(1).join(' ');
  document.getElementById('hero-name').innerHTML = `${firstName} <span>${lastName}</span>`;
  document.getElementById('hero-sub').textContent = 'Ref: ' + ci.job_ref + ' · Track your vehicle service in real-time.';
  document.getElementById('vehicle-plate').textContent = ci.vehicle_plate;
  document.getElementById('vehicle-model').textContent = ci.vehicle_model;

  // ── Populate portal header bar
  document.getElementById('ph-user-name').textContent = ci.customer_name;
  document.getElementById('ph-user-email').textContent = ci.customer_email;
  document.getElementById('ph-avatar').textContent = ci.customer_name.charAt(0).toUpperCase();

  // ── Init job switcher (lazy loads the job list on first open)
  _jobSwitcherLoaded = false;
  initJobSwitcher(ci.job_ref);

  // ── PROGRESS STEPS
  var stepDefs = ['Check-In','Quotation','In Service','Invoice','Payment'];
  var currentStep = data.current_step || 3; // 1-based
  var stepsHtml = stepDefs.map(function(name, i) {
    var stepNum = i + 1;
    var cls = stepNum < currentStep ? 'done' : stepNum === currentStep ? 'active' : '';
    var dot = stepNum < currentStep ? '✓' : stepNum === currentStep ? '▶' : stepNum;
    return `<div class="step ${cls}">
      <div class="step-dot">${dot}</div>
      <div class="step-name">${name}</div>
    </div>`;
  }).join('');
  document.getElementById('progress-steps').innerHTML = stepsHtml;

  // ── CHECK-IN GRID
  document.getElementById('checkin-grid').innerHTML = [
    dataItem('Check-In Date', ci.checkin_date),
    dataItem('Check-In Time', ci.checkin_time),
    dataItem('Service Advisor', ci.advisor),
    dataItem('Bay Assigned', ci.bay, true),
    dataItem('Mileage In', ci.mileage),
    dataItem('Fuel Level', ci.fuel_level),
    dataItem('Exterior', ci.exterior_condition),
    dataItem('Warning Lights', `<span style="color:var(--orange)">${ci.warning_lights || 'None'}</span>`)
  ].join('');

  document.getElementById('checkin-complaint').innerHTML =
    '🔍 <strong>Customer Complaint:</strong> "' + ci.customer_complaint + '"';

  document.getElementById('customer-grid').innerHTML = [
    dataItem('Full Name', ci.customer_name),
    dataItem('Phone', ci.customer_phone),
    dataItem('Email', ci.customer_email),
    dataItem('Service Type', badgeHtml(ci.service_type, 'orange'))
  ].join('');

  // ── QUOTATION
  document.getElementById('quote-title').textContent = 'Quotation ' + qt.quote_ref;
  var qBadge = document.getElementById('quote-status-badge');
  qBadge.textContent = qt.status;
  qBadge.className = 'badge ' + (qt.status_badge_class || 'badge-orange');

  document.getElementById('quote-stats').innerHTML = [
    statBlock(qt.currency + ' ' + qt.grand_total.toLocaleString(), 'Quoted Total', 'var(--accent)'),
    statBlock(qt.items.length, 'Line Items', 'var(--green)'),
    statBlock(qt.est_duration, 'Est. Duration', 'var(--blue)'),
    statBlock(qt.approval_status, 'Status', 'var(--orange)')
  ].join('');

  var typeColors = {Parts:'blue', Service:'purple', Labour:'orange'};
  document.getElementById('quote-items').innerHTML = qt.items.map(function(item, i) {
    var tc = typeColors[item.type] || 'blue';
    return `<tr>
      <td class="td-mono">${String(i+1).padStart(2,'0')}</td>
      <td>${item.description}</td>
      <td>${badgeHtml(item.type, tc)}</td>
      <td class="tr-right">${item.qty}</td>
      <td class="tr-right">${qt.currency} ${item.unit_price.toLocaleString()}</td>
      <td class="tr-right">${qt.currency} ${item.total.toLocaleString()}</td>
    </tr>`;
  }).join('');

  document.getElementById('quote-totals').innerHTML =
    totalRow('Subtotal', qt.currency + ' ' + qt.subtotal.toLocaleString()) +
    (qt.discount > 0 ? totalRow(qt.discount_label || 'Discount', '− ' + qt.currency + ' ' + qt.discount.toLocaleString(), 'color:var(--green)') : '') +
    (qt.tax > 0 ? totalRow(qt.tax_label || 'Tax', qt.currency + ' ' + qt.tax.toLocaleString()) : '') +
    totalRow('Grand Total', qt.currency + ' ' + qt.grand_total.toLocaleString(), '', true);

  // ── SERVICE
  var svcBadge = document.getElementById('service-status-badge');
  svcBadge.textContent = sv.status_label;
  svcBadge.className = 'badge ' + (sv.status_badge_class || 'badge-accent');

  document.getElementById('service-grid').innerHTML = [
    dataItem('Technician', sv.technician),
    dataItem('Started', sv.start_date),
    dataItem('Est. Completion', sv.est_completion, true),
    dataItem('Progress', `<span style="color:var(--accent)">${sv.progress_pct}%</span>`)
  ].join('');

  setTimeout(function() {
    document.getElementById('service-prog-bar').style.width = sv.progress_pct + '%';
  }, 300);

  var tlDotStyles = {done:'background:var(--green-dim);color:var(--green)', active:'background:var(--accent-dim);color:var(--accent)', pending:'background:var(--surface-2);color:var(--text-muted)'};
  var tlDotSymbols = {done:'✓', active:'▶', pending:'○'};
  document.getElementById('service-timeline').innerHTML = sv.timeline.map(function(item) {
    var style = tlDotStyles[item.status] || tlDotStyles.pending;
    var sym = tlDotSymbols[item.status] || '○';
    return `<div class="timeline-item">
      <div class="tl-dot" style="${style}">${sym}</div>
      <div class="tl-content">
        <div class="tl-time">${item.time_label}</div>
        <div class="tl-title">${item.title}</div>
        <div class="tl-desc">${item.description}</div>
      </div>
    </div>`;
  }).join('');

  if (sv.notes && sv.notes.length) {
    document.getElementById('service-notes-wrap').innerHTML =
      sv.notes.map(function(n) {
        return `<div class="tech-note" style="border-color:var(--${n.color || 'blue'});margin-bottom:10px">${n.text}</div>`;
      }).join('');
  }

  // ── INVOICE
  document.getElementById('invoice-title').textContent = 'Invoice ' + inv.invoice_ref;
  var invBadge = document.getElementById('invoice-status-badge');
  invBadge.textContent = inv.status_label;
  invBadge.className = 'badge ' + (inv.status_badge_class || 'badge-orange');

  document.getElementById('invoice-grid').innerHTML = [
    dataItem('Invoice Date', inv.invoice_date),
    dataItem('Due Date', `<span style="color:var(--red)">${inv.due_date}</span>`),
    dataItem('Invoice Ref', `<span class="td-mono">${inv.invoice_ref}</span>`),
    dataItem('Billed To', inv.billed_to)
  ].join('');

  document.getElementById('invoice-items').innerHTML = inv.items.map(function(item) {
    return `<tr>
      <td>${item.description}</td>
      <td class="tr-right">${item.qty}</td>
      <td class="tr-right">${inv.currency} ${item.unit_price.toLocaleString()}</td>
      <td class="tr-right">${inv.currency} ${item.total.toLocaleString()}</td>
    </tr>`;
  }).join('');

  document.getElementById('invoice-totals').innerHTML =
    totalRow('Subtotal', inv.currency + ' ' + inv.subtotal.toLocaleString()) +
    (inv.discount > 0 ? totalRow(inv.discount_label || 'Discount', '− ' + inv.currency + ' ' + inv.discount.toLocaleString(), 'color:var(--green)') : '') +
    (inv.tax > 0 ? totalRow(inv.tax_label || 'Tax', inv.currency + ' ' + inv.tax.toLocaleString()) : '') +
    totalRow('Amount Due', inv.currency + ' ' + inv.total_due.toLocaleString(), '', true);

  document.getElementById('biller-grid').innerHTML = [
    dataItem('Garage Name', inv.biller_name),
    dataItem('PIN / VAT No.', `<span class="td-mono">${inv.biller_pin}</span>`),
    dataItem('Address', inv.biller_address),
    dataItem('Phone', inv.biller_phone)
  ].join('');

  // ── PAYMENT
  var payBadge = document.getElementById('payment-status-badge');
  payBadge.textContent = pay.status_label;
  payBadge.className = 'badge ' + (pay.status_badge_class || 'badge-red');

  document.getElementById('balance-amount').textContent = pay.currency + ' ' + pay.balance.toLocaleString();
  document.getElementById('deposit-amount').textContent = pay.currency + ' ' + pay.deposit_paid.toLocaleString() + ' ✓';

  paymentMethodsData = pay.methods;
  document.getElementById('payment-methods').innerHTML = pay.methods.map(function(m, i) {
    return `<div class="payment-method-card${i===0?' selected':''}" onclick="selectPM(${i})">
      <div class="pm-icon">${m.icon}</div>
      <div class="pm-info">
        <div class="pm-name">${m.name}</div>
        <div class="pm-desc">${m.description}</div>
      </div>
      <div class="pm-radio"></div>
    </div>`;
  }).join('');

  if (pay.methods[0]) {
    selectedPaymentMethod = pay.methods[0];
    if (pay.methods[0].instructions) {
      document.getElementById('payment-method-info').innerHTML =
        `<div class="tech-note" style="border-color:var(--green)">${pay.methods[0].instructions}</div>`;
    }
    document.getElementById('pay-btn').innerHTML = `⚡ Pay ${pay.currency} ${pay.balance.toLocaleString()} via ${pay.methods[0].name}`;
  }

  document.getElementById('payment-history').innerHTML = pay.history.length
    ? pay.history.map(function(h) {
        var sc = h.status === 'Confirmed' ? 'badge-green' : 'badge-orange';
        return `<tr>
          <td>${h.date}</td>
          <td>${h.method}</td>
          <td class="td-mono">${h.reference}</td>
          <td class="tr-right">${pay.currency} ${h.amount.toLocaleString()}</td>
          <td>${badgeHtml(h.status, sc.replace('badge-',''))}</td>
        </tr>`;
      }).join('')
    : `<tr><td colspan="5" style="color:var(--text-muted);text-align:center;padding:20px">No payments recorded yet.</td></tr>`;
}
"""