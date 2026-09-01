/**
 * CYBERQUANT 2050 // MASTER APPLICATION CONTROLLER
 * 10/10 Interactive Background Warp, Liquid Cursor, 3D Tilt Kinetics,
 * Complete Project Dataset Repository (150 Assets, 69 CVEs, 6 Controls, 5 Threats,
 * 20 Department Aggregations & 10,000 Monte Carlo FAIR Iterations),
 * Live Multi-Filter Toolbar, Pagination & Instant JSON/CSV Exporters.
 */

import { apiClient } from './api.js';
import { soundFx } from './audio_fx.js';
import { CyberGlobe3D } from './three_scene.js';
import { chartEngine } from './charts.js';
import { CyberMatrixBackground } from './background_warp.js';

class CyberQuantApp {
  constructor() {
    this.globe = null;
    this.bgWarp = null;
    this.activeTab = 'tab-command';
    this.activeSubtab = 'assets';
    this.pagination = {
      page: 1,
      pageSize: 15,
      showAll: false
    };
    this.filters = {
      query: '',
      department: '',
      criticality: ''
    };
    this.cachedData = {
      assets: [],
      vulns: [],
      controls: [],
      threats: [],
      departments: [],
      monteCarlo: null
    };
    this.sandboxState = {
      actions: ['enable_mfa', 'enable_edr'],
      coverage: 100
    };
  }

  async init() {
    console.log("[CYBERQUANT 2050] Booting Cyber Warfare & Quantitative Capital Suite...");

    // 1. 10/10 Interactive Cyber Matrix Background Engine
    this.bgWarp = new CyberMatrixBackground('cyber-matrix-bg');

    // 2. Audio Setup
    this.setupAudioUI();

    // 3. Tab Navigation & Floating Dock
    this.setupTabsAndDock();

    // 4. Liquid Cursor Follower
    this.setupLiquidCursor();

    // 5. 3D Card Tilt Physics
    this.setup3DCardTilt();

    // 6. Initialize 3D Celestial Threat Globe
    this.globe = new CyberGlobe3D('three-canvas-container', (assetData) => {
      this.openAssetModal(assetData);
    });

    // 7. Load Complete Project Datasets (All 6 Data Dimensions)
    await this.loadAllDatasets();

    // 8. Render Telemetry & KPIs
    await this.refreshTelemetry();

    // 9. Setup Interactive Dataset Explorer
    this.setupDatasetExplorer();

    // 10. Setup Knapsack 0/1 Solver
    this.setupKnapsackControls();

    // 11. Setup What-If Remediation Sandbox
    this.setupSandboxControls();

    // 12. Setup GenAI CISO Terminal
    this.setupAIChat();

    // 13. Start HUD Clock
    this.startHUDClock();
  }

  setupAudioUI() {
    const btn = document.getElementById('audio-toggle-btn');
    if (btn) {
      btn.innerHTML = soundFx.enabled ? '🔊' : '🔇';
      btn.addEventListener('click', () => {
        const isEnabled = soundFx.toggle();
        btn.innerHTML = isEnabled ? '🔊' : '🔇';
      });
    }
  }

  setupTabsAndDock() {
    const switchTab = (targetId) => {
      if (!targetId || targetId === this.activeTab) return;
      soundFx.playTabSwitch();

      // Sync Header Tabs
      document.querySelectorAll('.hud-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === targetId);
      });

      // Sync Floating Dynamic Dock
      document.querySelectorAll('.dock-item-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === targetId);
      });

      // Switch View
      document.querySelectorAll('.tab-view').forEach(view => {
        view.classList.remove('active');
      });
      const targetView = document.getElementById(targetId);
      if (targetView) targetView.classList.add('active');

      this.activeTab = targetId;

      // On-demand rendering
      if (targetId === 'tab-knapsack') {
        chartEngine.renderRosiCurve('rosi-curve-canvas', 10000000);
      } else if (targetId === 'tab-compliance') {
        chartEngine.renderComplianceRadar('compliance-radar-canvas');
      } else if (targetId === 'tab-dataset') {
        this.renderDatasetView();
      } else if (targetId === 'tab-command' && this.globe) {
        this.globe.onResize();
      }
    };

    document.querySelectorAll('.hud-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    document.querySelectorAll('.dock-item-btn').forEach(btn => {
      btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });
  }

  setupLiquidCursor() {
    const blob = document.getElementById('cursor-glow-blob');
    if (!blob) return;

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let currentX = mouseX;
    let currentY = mouseY;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    const animateCursor = () => {
      currentX += (mouseX - currentX) * 0.12;
      currentY += (mouseY - currentY) * 0.12;
      blob.style.transform = `translate3d(${currentX - 225}px, ${currentY - 225}px, 0)`;
      requestAnimationFrame(animateCursor);
    };
    animateCursor();
  }

  setup3DCardTilt() {
    const cards = document.querySelectorAll('.kpi-card, .viewport-card, .intel-panel, .control-simulator-card, .sandbox-card, .dataset-explorer-card, .meta-pill');
    cards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = `perspective(1000px) rotateX(${y * -7}deg) rotateY(${x * 7}deg) scale3d(1.015, 1.015, 1.015)`;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      });
    });
  }

  async loadAllDatasets() {
    this.cachedData.assets = await apiClient.getAssets(150);
    this.cachedData.vulns = await apiClient.getVulnerabilities(69);
    this.cachedData.controls = apiClient.getControls();
    this.cachedData.threats = apiClient.getThreats();
    this.cachedData.departments = await apiClient.getDepartmentAnalytics();
    this.cachedData.monteCarlo = await apiClient.getMonteCarloData();

    // Populate Department Filter Select
    const deptSelect = document.getElementById('dataset-dept-filter');
    if (deptSelect) {
      const depts = Array.from(new Set(this.cachedData.assets.map(a => a.department))).sort();
      deptSelect.innerHTML = '<option value="">All Departments (' + depts.length + ')</option>';
      depts.forEach(d => {
        const opt = document.createElement('option');
        opt.value = d;
        opt.innerText = d;
        deptSelect.appendChild(opt);
      });
    }
  }

  async refreshTelemetry() {
    const dash = await apiClient.getDashboard();
    this.animateNumber('kpi-eal', dash.expected_annual_loss_inr / 10000000, '₹', ' Cr', 2);
    this.animateNumber('kpi-avoided', 6.91, '₹', ' Cr', 2);
    this.animateNumber('kpi-rosi', 3359, '', '%', 0);
    this.animateNumber('kpi-compliance', dash.compliance_score_pct, '', '%', 1);

    // Render Priority Financial Risks List
    const topRisks = await apiClient.getTopRisks(6);
    const riskContainer = document.getElementById('risk-mini-list');
    if (riskContainer) {
      riskContainer.innerHTML = '';
      topRisks.forEach(r => {
        const lossCr = (r.expected_loss_inr / 10000000).toFixed(2);
        const card = document.createElement('div');
        card.className = 'risk-card-mini';
        card.innerHTML = `
          <div class="risk-top-meta">
            <span class="risk-asset-name">${r.asset_name}</span>
            <span class="risk-eal-badge">₹${lossCr} Cr EAL</span>
          </div>
          <div class="risk-cve-list">🚨 ${r.cve_count || 3} CVE Flaws | ${r.department}</div>
          <div class="risk-impact-breakdown">
            <span>Breach Prob: <strong style="color:var(--neon-crimson)">${r.breach_likelihood_pct}%</strong></span>
            <span>Criticality: <strong style="color:#FFFFFF">${r.criticality || 'Critical'}</strong></span>
          </div>
        `;
        card.addEventListener('click', () => {
          soundFx.playClick();
          this.openAssetModal(r);
        });
        riskContainer.appendChild(card);
      });
    }
  }

  setupDatasetExplorer() {
    // 1. Subtab Switching
    const subtabs = document.querySelectorAll('.subtab-btn');
    subtabs.forEach(btn => {
      btn.addEventListener('click', () => {
        soundFx.playClick();
        subtabs.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.activeSubtab = btn.dataset.subtab;
        this.pagination.page = 1;
        this.renderDatasetView();
      });
    });

    // 2. Search Input
    const searchInput = document.getElementById('dataset-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        this.filters.query = searchInput.value.trim().toLowerCase();
        this.pagination.page = 1;
        this.renderDatasetView();
      });
    }

    // 3. Department Dropdown Filter
    const deptSelect = document.getElementById('dataset-dept-filter');
    if (deptSelect) {
      deptSelect.addEventListener('change', () => {
        soundFx.playClick();
        this.filters.department = deptSelect.value;
        this.pagination.page = 1;
        this.renderDatasetView();
      });
    }

    // 4. Criticality Dropdown Filter
    const critSelect = document.getElementById('dataset-crit-filter');
    if (critSelect) {
      critSelect.addEventListener('change', () => {
        soundFx.playClick();
        this.filters.criticality = critSelect.value;
        this.pagination.page = 1;
        this.renderDatasetView();
      });
    }

    // 5. Pagination Buttons
    const prevBtn = document.getElementById('btn-page-prev');
    const nextBtn = document.getElementById('btn-page-next');
    const showAllBtn = document.getElementById('btn-show-all');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (this.pagination.page > 1) {
          soundFx.playClick();
          this.pagination.page--;
          this.renderDatasetView();
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        soundFx.playClick();
        this.pagination.page++;
        this.renderDatasetView();
      });
    }

    if (showAllBtn) {
      showAllBtn.addEventListener('click', () => {
        soundFx.playClick();
        this.pagination.showAll = !this.pagination.showAll;
        showAllBtn.innerText = this.pagination.showAll ? 'PAGE VIEW' : 'SHOW ALL';
        this.renderDatasetView();
      });
    }

    // 6. Export Handlers
    const exportJsonBtn = document.getElementById('btn-export-json');
    const exportCsvBtn = document.getElementById('btn-export-csv');

    if (exportJsonBtn) {
      exportJsonBtn.addEventListener('click', () => this.exportCurrentData('json'));
    }
    if (exportCsvBtn) {
      exportCsvBtn.addEventListener('click', () => this.exportCurrentData('csv'));
    }
  }

  renderDatasetView() {
    const tableContainer = document.getElementById('dataset-table-container');
    const analyticsContainer = document.getElementById('dataset-analytics-container');
    const paginationBar = document.getElementById('dataset-pagination');

    if (!tableContainer || !analyticsContainer) return;

    if (this.activeSubtab === 'monte_carlo') {
      tableContainer.style.display = 'none';
      if (paginationBar) paginationBar.style.display = 'none';
      analyticsContainer.style.display = 'block';
      this.renderMonteCarloView(analyticsContainer);
      return;
    }

    tableContainer.style.display = 'block';
    analyticsContainer.style.display = 'none';
    if (paginationBar) paginationBar.style.display = 'flex';

    this.renderDatasetTable();
  }

  renderDatasetTable() {
    const thead = document.getElementById('dataset-table-head');
    const tbody = document.getElementById('dataset-table-body');
    const pageNumEl = document.getElementById('page-current-num');
    const pageInfoEl = document.getElementById('pagination-info');
    const prevBtn = document.getElementById('btn-page-prev');
    const nextBtn = document.getElementById('btn-page-next');

    if (!thead || !tbody) return;

    thead.innerHTML = '';
    tbody.innerHTML = '';

    const q = this.filters.query;
    const dFilter = this.filters.department;
    const cFilter = this.filters.criticality;

    let items = [];

    // A. ASSETS SUBTAB (150 Items)
    if (this.activeSubtab === 'assets') {
      thead.innerHTML = `
        <tr>
          <th>Asset ID</th>
          <th>Asset Name</th>
          <th>Type</th>
          <th>Department</th>
          <th>Criticality</th>
          <th>Valuation</th>
          <th>Downtime/Hr</th>
          <th>Exposed</th>
          <th>MFA</th>
          <th>EDR</th>
          <th>Annual Loss (EAL)</th>
        </tr>
      `;

      items = this.cachedData.assets.filter(a => {
        const matchesQuery = !q || a.asset_id.toLowerCase().includes(q) ||
                                  a.asset_name.toLowerCase().includes(q) ||
                                  a.department.toLowerCase().includes(q) ||
                                  a.asset_type.toLowerCase().includes(q);
        const matchesDept = !dFilter || a.department === dFilter;
        const matchesCrit = !cFilter || a.criticality.toLowerCase() === cFilter.toLowerCase();
        return matchesQuery && matchesDept && matchesCrit;
      });

      const paginated = this.paginateItems(items);

      paginated.forEach(a => {
        const tr = document.createElement('tr');
        const valCr = (a.asset_value_inr / 10000000).toFixed(2);
        const lossLakh = ((a.expected_loss_inr || a.expected_annual_loss_inr || 1500000) / 100000).toFixed(1);
        const isCrit = a.criticality.toLowerCase() === 'critical';

        tr.innerHTML = `
          <td><strong>${a.asset_id}</strong></td>
          <td style="font-family:var(--font-hud); font-weight:700; color:#FFFFFF;">${a.asset_name}</td>
          <td>${a.asset_type}</td>
          <td>${a.department}</td>
          <td><span class="${isCrit ? 'badge-crit' : 'badge-high'}">${a.criticality}</span></td>
          <td>₹${valCr} Cr</td>
          <td>₹${(a.downtime_cost_per_hour_inr || 20000).toLocaleString('en-IN')}/hr</td>
          <td>${a.is_internet_exposed ? '<span class="badge-crit">YES</span>' : '<span class="badge-ok">NO</span>'}</td>
          <td>${a.mfa_enabled ? '✓ Enforced' : '✗ Disabled'}</td>
          <td>${a.edr_installed ? '✓ Active' : '✗ None'}</td>
          <td style="color:var(--neon-crimson); font-weight:800;">₹${lossLakh} L</td>
        `;

        tr.addEventListener('click', () => {
          soundFx.playClick();
          this.openAssetModal(a);
        });
        tbody.appendChild(tr);
      });

    // B. VULNERABILITIES SUBTAB (69 Items)
    } else if (this.activeSubtab === 'vulns') {
      thead.innerHTML = `
        <tr>
          <th>Vuln ID</th>
          <th>Asset ID</th>
          <th>CVE ID</th>
          <th>Vulnerability Name</th>
          <th>Severity</th>
          <th>CVSS 3.1</th>
          <th>Public Exploit</th>
          <th>Patch Cost</th>
        </tr>
      `;

      items = this.cachedData.vulns.filter(v => {
        const matchesQuery = !q || v.cve_id.toLowerCase().includes(q) ||
                                  v.asset_id.toLowerCase().includes(q) ||
                                  (v.title && v.title.toLowerCase().includes(q));
        const matchesCrit = !cFilter || v.severity.toLowerCase() === cFilter.toLowerCase();
        return matchesQuery && matchesCrit;
      });

      const paginated = this.paginateItems(items);

      paginated.forEach(v => {
        const tr = document.createElement('tr');
        const isCrit = v.severity.toLowerCase() === 'critical';
        tr.innerHTML = `
          <td>${v.vuln_id}</td>
          <td><strong>${v.asset_id}</strong></td>
          <td style="color:var(--neon-crimson); font-weight:800;">${v.cve_id}</td>
          <td style="font-family:var(--font-hud); font-weight:700; color:#FFFFFF;">${v.title}</td>
          <td><span class="${isCrit ? 'badge-crit' : 'badge-high'}">${v.severity}</span></td>
          <td style="font-weight:800; color:${v.cvss_score >= 9.0 ? 'var(--neon-crimson)' : 'var(--neon-cyan)'};">${v.cvss_score}</td>
          <td>${v.exploit_available ? '<span class="badge-crit">EXPLOIT READY</span>' : 'None'}</td>
          <td>₹${(v.patch_cost_inr || 50000).toLocaleString('en-IN')}</td>
        `;
        tbody.appendChild(tr);
      });

    // C. CONTROLS SUBTAB (6 Controls)
    } else if (this.activeSubtab === 'controls') {
      thead.innerHTML = `
        <tr>
          <th>Control ID</th>
          <th>Security Control Name</th>
          <th>Category</th>
          <th>Cost (₹)</th>
          <th>Risk Reduction (₹)</th>
          <th>Annual Maintenance</th>
          <th>Implementation</th>
          <th>Framework Mappings</th>
        </tr>
      `;

      items = this.cachedData.controls;
      items.forEach(c => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${c.control_id}</strong></td>
          <td style="font-family:var(--font-hud); font-weight:700; color:#FFFFFF;">${c.name}</td>
          <td>${c.category}</td>
          <td style="color:var(--neon-cyan); font-weight:700;">₹${(c.cost_inr / 100000).toFixed(1)} Lakhs</td>
          <td style="color:var(--neon-emerald); font-weight:800;">₹${(c.risk_reduction_inr / 100000).toFixed(1)} Lakhs</td>
          <td>₹${(c.annual_maintenance_inr / 100000).toFixed(1)} L/yr</td>
          <td>${c.implementation_days} Days</td>
          <td style="font-size:0.78rem; color:var(--text-muted);">${c.framework_mapping}</td>
        `;
        tbody.appendChild(tr);
      });

    // D. THREATS SUBTAB (5 Threat Vectors)
    } else if (this.activeSubtab === 'threats') {
      thead.innerHTML = `
        <tr>
          <th>Threat ID</th>
          <th>Threat Vector Name</th>
          <th>Target Asset Type</th>
          <th>Annual Base Likelihood</th>
          <th>Typical Impact</th>
        </tr>
      `;

      items = this.cachedData.threats;
      items.forEach(t => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${t.threat_id}</strong></td>
          <td style="font-family:var(--font-hud); font-weight:700; color:#FFFFFF;">${t.name}</td>
          <td>${t.target}</td>
          <td style="color:var(--neon-crimson); font-weight:800;">${(t.annual_base_likelihood * 100).toFixed(0)}%</td>
          <td><span class="badge-crit">${t.typical_impact}</span></td>
        `;
        tbody.appendChild(tr);
      });

    // E. DEPARTMENTS SUBTAB (20 Aggregations)
    } else if (this.activeSubtab === 'departments') {
      thead.innerHTML = `
        <tr>
          <th>Department Unit</th>
          <th>Asset Count</th>
          <th>Total Valuation (₹)</th>
          <th>Total Exposure (₹)</th>
          <th>Expected Annual Loss (EAL)</th>
          <th>Active CVEs</th>
          <th>Critical Nodes</th>
        </tr>
      `;

      items = this.cachedData.departments;
      items.forEach(d => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td style="font-family:var(--font-hud); font-weight:800; color:#FFFFFF;">${d.department}</td>
          <td><strong>${d.asset_count}</strong></td>
          <td>₹${(d.total_valuation_inr / 10000000).toFixed(2)} Cr</td>
          <td>₹${(d.total_exposure_inr / 10000000).toFixed(2)} Cr</td>
          <td style="color:var(--neon-crimson); font-weight:900;">₹${(d.total_eal_inr / 10000000).toFixed(2)} Cr</td>
          <td>🚨 ${d.vulnerability_count} Flaws</td>
          <td><span class="${d.critical_assets > 0 ? 'badge-crit' : 'badge-ok'}">${d.critical_assets} Nodes</span></td>
        `;
        tbody.appendChild(tr);
      });
    }

    // Update Pagination UI
    const totalItems = items.length;
    const totalPages = Math.ceil(totalItems / this.pagination.pageSize) || 1;

    if (this.pagination.showAll) {
      if (pageNumEl) pageNumEl.innerText = `All (${totalItems})`;
      if (pageInfoEl) pageInfoEl.innerText = `Showing all ${totalItems} records`;
      if (prevBtn) prevBtn.disabled = true;
      if (nextBtn) nextBtn.disabled = true;
    } else {
      const startIdx = (this.pagination.page - 1) * this.pagination.pageSize + 1;
      const endIdx = Math.min(this.pagination.page * this.pagination.pageSize, totalItems);

      if (pageNumEl) pageNumEl.innerText = `${this.pagination.page} / ${totalPages}`;
      if (pageInfoEl) pageInfoEl.innerText = totalItems > 0 ? `Showing ${startIdx} to ${endIdx} of ${totalItems} records` : 'No records found';
      if (prevBtn) prevBtn.disabled = this.pagination.page <= 1;
      if (nextBtn) nextBtn.disabled = this.pagination.page >= totalPages;
    }
  }

  paginateItems(items) {
    if (this.pagination.showAll) return items;
    const start = (this.pagination.page - 1) * this.pagination.pageSize;
    return items.slice(start, start + this.pagination.pageSize);
  }

  renderMonteCarloView(container) {
    const mc = this.cachedData.monteCarlo;
    if (!mc) return;

    container.innerHTML = `
      <div style="margin-bottom:1.5rem;">
        <h3 style="font-family:var(--font-cyber); font-size:1.15rem; color:#FFFFFF; margin-bottom:4px;">
          🎲 10,000 ITERATION MONTE CARLO FAIR SIMULATION
        </h3>
        <p style="font-size:0.85rem; color:var(--text-secondary);">
          Probabilistic loss frequency & loss magnitude distribution modeling 95% Value-at-Risk (VaR) and Tail Risk (CVaR).
        </p>
      </div>

      <div class="analytics-grid" style="margin-bottom:2rem;">
        <div class="analytics-card" style="border-left:5px solid var(--neon-cyan)">
          <div style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono); font-weight:700">VALUE AT RISK (VaR 95%)</div>
          <div style="font-family:var(--font-cyber); font-size:1.8rem; font-weight:900; color:var(--neon-cyan); margin:6px 0;">₹${(mc.var_95_inr / 10000000).toFixed(2)} Cr</div>
          <div style="font-size:0.78rem; color:var(--text-secondary)">Maximum loss expected in 95% of annual scenarios</div>
        </div>

        <div class="analytics-card" style="border-left:5px solid var(--neon-crimson)">
          <div style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono); font-weight:700">CONDITIONAL VaR (CVaR 95%)</div>
          <div style="font-family:var(--font-cyber); font-size:1.8rem; font-weight:900; color:var(--neon-crimson); margin:6px 0;">₹${(mc.cvar_95_inr / 10000000).toFixed(2)} Cr</div>
          <div style="font-size:0.78rem; color:var(--text-secondary)">Expected shortfall in worst 5% tail breach events</div>
        </div>

        <div class="analytics-card" style="border-left:5px solid var(--neon-emerald)">
          <div style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono); font-weight:700">SIMULATED ITERATIONS</div>
          <div style="font-family:var(--font-cyber); font-size:1.8rem; font-weight:900; color:var(--neon-emerald); margin:6px 0;">10,000 RUNS</div>
          <div style="font-size:0.78rem; color:var(--text-secondary)">OpenFAIR calibrated Poisson & LogNormal distributions</div>
        </div>
      </div>

      <div class="table-responsive-container">
        <table class="genz-table">
          <thead>
            <tr>
              <th>Percentile Metric</th>
              <th>Simulated Annualized Loss (₹)</th>
              <th>Executive Probability Interpretation</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>5th Percentile (P5 - Best Case)</strong></td>
              <td style="color:var(--neon-emerald); font-weight:800;">₹${(mc.percentiles.p5 / 10000000).toFixed(2)} Cr</td>
              <td>Optimistic baseline with strong proactive detection</td>
            </tr>
            <tr>
              <td><strong>50th Percentile (P50 - Median)</strong></td>
              <td style="color:var(--neon-cyan); font-weight:800;">₹${(mc.percentiles.p50_median / 10000000).toFixed(2)} Cr</td>
              <td>Most probable expected annual breach loss exposure</td>
            </tr>
            <tr>
              <td><strong>75th Percentile (P75)</strong></td>
              <td style="color:var(--text-main); font-weight:800;">₹${(mc.percentiles.p75 / 10000000).toFixed(2)} Cr</td>
              <td>Elevated breach scenario with multiple CVE chain exploits</td>
            </tr>
            <tr>
              <td><strong>90th Percentile (P90)</strong></td>
              <td style="color:var(--neon-gold); font-weight:800;">₹${(mc.percentiles.p90 / 10000000).toFixed(2)} Cr</td>
              <td>Severe systemic campaign targeting Core Banking & KYC data</td>
            </tr>
            <tr>
              <td><strong>95th Percentile (P95 - Value-at-Risk)</strong></td>
              <td style="color:var(--neon-crimson); font-weight:900;">₹${(mc.percentiles.p95 / 10000000).toFixed(2)} Cr</td>
              <td>Board-level solvency & regulatory capital reserve threshold</td>
            </tr>
            <tr>
              <td><strong>99th Percentile (P99 - Black Swan)</strong></td>
              <td style="color:var(--neon-crimson); font-weight:900; background:rgba(255,42,85,0.1)">₹${(mc.percentiles.p99_black_swan / 10000000).toFixed(2)} Cr</td>
              <td>Catastrophic multi-site ransomware extortion outage</td>
            </tr>
          </tbody>
        </table>
      </div>
    `;
  }

  exportCurrentData(format = 'json') {
    soundFx.playClick();
    let dataToExport = [];
    let filename = `cyberquant_${this.activeSubtab}`;

    if (this.activeSubtab === 'assets') dataToExport = this.cachedData.assets;
    else if (this.activeSubtab === 'vulns') dataToExport = this.cachedData.vulns;
    else if (this.activeSubtab === 'controls') dataToExport = this.cachedData.controls;
    else if (this.activeSubtab === 'threats') dataToExport = this.cachedData.threats;
    else if (this.activeSubtab === 'departments') dataToExport = this.cachedData.departments;
    else if (this.activeSubtab === 'monte_carlo') dataToExport = this.cachedData.monteCarlo;

    if (format === 'json') {
      const blob = new Blob([JSON.stringify(dataToExport, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${filename}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } else if (format === 'csv') {
      if (!Array.isArray(dataToExport) || dataToExport.length === 0) return;
      const keys = Object.keys(dataToExport[0]);
      const csvRows = [keys.join(',')];
      dataToExport.forEach(row => {
        const values = keys.map(k => {
          const val = row[k];
          return typeof val === 'string' ? `"${val.replace(/"/g, '""')}"` : val;
        });
        csvRows.push(values.join(','));
      });
      const blob = new Blob([csvRows.join('\n')], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${filename}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    }
  }

  setupKnapsackControls() {
    const slider = document.getElementById('budget-slider');
    const display = document.getElementById('budget-val-display');
    if (!slider) return;

    slider.addEventListener('input', async (e) => {
      const budgetLakhs = parseInt(e.target.value, 10);
      const budgetInr = budgetLakhs * 100000;
      if (display) {
        display.innerText = `₹${budgetLakhs} Lakhs (₹${(budgetLakhs / 100).toFixed(1)} Cr)`;
      }

      soundFx.playClick();
      const result = await apiClient.optimizeBudget(budgetInr);
      this.updateKnapsackUI(result);
      chartEngine.renderRosiCurve('rosi-curve-canvas', budgetInr);
    });

    apiClient.optimizeBudget(10000000).then(res => this.updateKnapsackUI(res));
  }

  updateKnapsackUI(result) {
    const spendEl = document.getElementById('knapsack-spend');
    const savedEl = document.getElementById('knapsack-saved');
    const rosiEl = document.getElementById('knapsack-rosi');
    const listEl = document.getElementById('knapsack-controls-list');

    if (spendEl) spendEl.innerText = `₹${(result.total_spend_inr / 100000).toFixed(1)}L`;
    if (savedEl) savedEl.innerText = `₹${(result.total_risk_reduced_inr / 10000000).toFixed(2)} Cr`;
    if (rosiEl) rosiEl.innerText = `${result.net_rosi_pct}%`;

    if (listEl) {
      listEl.innerHTML = '';
      result.selected_controls.forEach(c => {
        const card = document.createElement('div');
        card.className = 'alloc-card active-selected';
        card.innerHTML = `
          <div class="alloc-name">✓ [${c.id}] ${c.name}</div>
          <div class="alloc-cost">Capital Cost: ₹${(c.cost_inr / 100000).toFixed(1)} Lakhs</div>
          <div class="alloc-rosi">Avoided Loss: ₹${(c.risk_reduction_inr / 10000000).toFixed(2)} Cr (${c.rosi_pct}% ROSI)</div>
        `;
        listEl.appendChild(card);
      });
    }
  }

  setupSandboxControls() {
    const toggleBlocks = document.querySelectorAll('.toggle-block');
    const mfaSlider = document.getElementById('mfa-coverage-slider');
    const mfaVal = document.getElementById('mfa-coverage-val');

    toggleBlocks.forEach(block => {
      block.addEventListener('click', async () => {
        soundFx.playClick();
        block.classList.toggle('active');
        const action = block.dataset.action;

        if (block.classList.contains('active')) {
          if (!this.sandboxState.actions.includes(action)) {
            this.sandboxState.actions.push(action);
          }
        } else {
          this.sandboxState.actions = this.sandboxState.actions.filter(a => a !== action);
        }

        await this.runSimulation();
      });
    });

    if (mfaSlider) {
      mfaSlider.addEventListener('input', async (e) => {
        const cov = parseInt(e.target.value, 10);
        this.sandboxState.coverage = cov;
        if (mfaVal) mfaVal.innerText = `${cov}%`;
        await this.runSimulation();
      });
    }

    this.runSimulation();
  }

  async runSimulation() {
    const res = await apiClient.simulateScenario(this.sandboxState.actions, this.sandboxState.coverage);
    const postLossEl = document.getElementById('sandbox-post-loss');
    const deltaEl = document.getElementById('sandbox-delta');
    const pctEl = document.getElementById('sandbox-pct');

    const postCr = (res.simulated_eal_inr / 10000000).toFixed(2);
    const deltaCr = (res.net_delta_inr / 10000000).toFixed(2);

    if (postLossEl) postLossEl.innerText = `₹${postCr} Cr`;
    if (deltaEl) deltaEl.innerText = `-₹${deltaCr} Cr`;
    if (pctEl) pctEl.innerText = `${res.percentage_reduction}% Risk Avoidance`;
  }

  setupAIChat() {
    const input = document.getElementById('ai-chat-input');
    const sendBtn = document.getElementById('ai-chat-send');
    const chips = document.querySelectorAll('.chip-btn');

    const handleSend = async (text) => {
      const prompt = text || (input ? input.value.trim() : '');
      if (!prompt) return;

      if (input) input.value = '';
      soundFx.playClick();

      this.appendChatMessage(prompt, 'msg-user');
      const tempAiMsg = this.appendChatMessage('CALCULATING QUANTITATIVE FINANCIAL IMPACT...', 'msg-ai');

      const aiResponse = await apiClient.queryAI(prompt);
      this.streamTypewriter(tempAiMsg, aiResponse.response, aiResponse.intent);
    };

    if (sendBtn) sendBtn.addEventListener('click', () => handleSend());
    if (input) {
      input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
      });
    }

    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        handleSend(chip.innerText);
      });
    });
  }

  streamTypewriter(container, fullText, intent) {
    container.innerHTML = `
      <div style="font-family:var(--font-cyber); font-size:0.75rem; color:var(--neon-cyan); margin-bottom:5px; font-weight:800; text-shadow:0 0 8px var(--neon-cyan-glow)">
        🤖 CYBERQUANT AI [${intent || 'EXECUTIVE_ANALYSIS'}]
      </div>
      <div class="stream-body" style="line-height:1.6"></div>
    `;

    const bodyEl = container.querySelector('.stream-body');
    let idx = 0;
    const speed = 12;

    const tick = () => {
      if (idx < fullText.length) {
        bodyEl.textContent += fullText.charAt(idx);
        idx++;
        setTimeout(tick, speed);
      } else {
        soundFx.playNodeScan();
      }
    };
    tick();
  }

  appendChatMessage(text, className) {
    const msgArea = document.getElementById('ai-messages-area');
    if (!msgArea) return null;
    const msg = document.createElement('div');
    msg.className = `chat-msg ${className}`;
    msg.innerText = text;
    msgArea.appendChild(msg);
    msgArea.scrollTop = msgArea.scrollHeight;
    return msg;
  }

  openAssetModal(asset) {
    const modal = document.getElementById('asset-modal');
    if (!modal) return;

    document.getElementById('modal-asset-title').innerText = asset.name || asset.asset_name || "Enterprise Node";
    document.getElementById('modal-asset-dept').innerText = asset.department || "Core Banking";
    document.getElementById('modal-asset-loss').innerText = asset.loss || `₹${((asset.expected_loss_inr || asset.expected_annual_loss_inr || 15000000) / 10000000).toFixed(2)} Cr`;
    document.getElementById('modal-asset-crit').innerText = asset.criticality || "CRITICAL";

    modal.classList.add('open');

    const closeBtn = document.getElementById('modal-close-btn');
    if (closeBtn) {
      closeBtn.onclick = () => modal.classList.remove('open');
    }
  }

  animateNumber(elId, targetVal, prefix = '', suffix = '', decimals = 0) {
    const el = document.getElementById(elId);
    if (!el) return;

    let start = 0;
    const duration = 1200;
    const startTime = performance.now();

    const update = (now) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      const current = start + (targetVal - start) * ease;
      el.innerText = `${prefix}${current.toFixed(decimals)}${suffix}`;

      if (progress < 1) {
        requestAnimationFrame(update);
      }
    };
    requestAnimationFrame(update);
  }

  startHUDClock() {
    const clockEl = document.getElementById('hud-live-clock');
    if (!clockEl) return;
    const updateTime = () => {
      const now = new Date();
      clockEl.innerText = now.toUTCString().replace("GMT", "UTC");
    };
    setInterval(updateTime, 1000);
    updateTime();
  }
}

window.addEventListener('DOMContentLoaded', () => {
  const app = new CyberQuantApp();
  app.init();
});
