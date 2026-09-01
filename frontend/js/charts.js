/**
 * CYBERQUANT 2077 // ONIKS_ASTARIT CYBERPUNK UI 01 CHART SUITE
 * Cyber Yellow (#FFE600), Electric Cyan (#00F0FF), Cyber Crimson (#FF003C).
 */

let rosiChartInstance = null;
let radarChartInstance = null;
let distributionChartInstance = null;

export const chartEngine = {
  // 1. 0/1 Knapsack Diminishing Returns & ROSI Curve
  renderRosiCurve(canvasId, activeBudgetInr = 10000000) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const budgets = [10, 20, 40, 60, 80, 100, 120, 150, 200]; // Lakhs
    const riskReduced = [28, 48, 58, 65, 69.1, 71, 72.2, 73.0, 73.5]; // Crores
    const rosiPct = [1400, 2400, 1450, 1083, 3359, 710, 601, 486, 367];

    const activeBudgetLakhs = Math.round(activeBudgetInr / 100000);

    if (rosiChartInstance) {
      rosiChartInstance.destroy();
    }

    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 320);
    gradient.addColorStop(0, 'rgba(255, 230, 0, 0.35)');
    gradient.addColorStop(1, 'rgba(255, 230, 0, 0.0)');

    rosiChartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: budgets.map(b => `₹${b}L`),
        datasets: [
          {
            label: 'Risk Loss Avoided (₹ Cr)',
            data: riskReduced,
            borderColor: '#FFE600',
            backgroundColor: gradient,
            borderWidth: 3,
            tension: 0.3,
            fill: true,
            pointBackgroundColor: budgets.map(b => Math.abs(b - activeBudgetLakhs) < 15 ? '#FF003C' : '#FFE600'),
            pointBorderColor: '#FFFFFF',
            pointBorderWidth: 2,
            pointRadius: budgets.map(b => Math.abs(b - activeBudgetLakhs) < 15 ? 8 : 4),
            yAxisID: 'y'
          },
          {
            label: 'ROSI (%)',
            data: rosiPct,
            borderColor: '#00F0FF',
            borderWidth: 2.2,
            borderDash: [4, 4],
            tension: 0.3,
            fill: false,
            pointBackgroundColor: '#00F0FF',
            pointRadius: 3,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: {
            labels: {
              color: '#FFFFFF',
              font: { family: 'Rajdhani', size: 13, weight: 700 }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(10, 12, 18, 0.95)',
            titleColor: '#FFE600',
            bodyColor: '#FFFFFF',
            borderColor: '#FFE600',
            borderWidth: 1.5,
            titleFont: { family: 'Orbitron', size: 12, weight: 800 },
            bodyFont: { family: 'Share Tech Mono', size: 13 }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 230, 0, 0.08)' },
            ticks: { color: '#94A3B8', font: { family: 'Share Tech Mono', size: 11, weight: 600 } }
          },
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            grid: { color: 'rgba(255, 230, 0, 0.08)' },
            ticks: {
              color: '#FFE600',
              font: { family: 'Share Tech Mono', size: 11, weight: 700 },
              callback: val => `₹${val} Cr`
            }
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            grid: { drawOnChartArea: false },
            ticks: {
              color: '#00F0FF',
              font: { family: 'Share Tech Mono', size: 11, weight: 700 },
              callback: val => `${val}%`
            }
          }
        }
      }
    });
  },

  // 2. Regulatory Compliance Radar
  renderComplianceRadar(canvasId, frameworks = null) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (radarChartInstance) {
      radarChartInstance.destroy();
    }

    const defaultFw = [
      { name: "RBI Cyber Framework", score: 82.5 },
      { name: "SEBI CSCRF 2.0", score: 75.0 },
      { name: "NIST CSF 2.0", score: 78.0 },
      { name: "ISO/IEC 27001", score: 72.0 },
      { name: "DPDPA 2023", score: 75.0 },
      { name: "CERT-In Cyber", score: 80.0 }
    ];

    const data = frameworks || defaultFw;

    radarChartInstance = new Chart(ctx, {
      type: 'radar',
      data: {
        labels: data.map(d => d.name),
        datasets: [
          {
            label: 'Current Audit Posture (%)',
            data: data.map(d => d.score),
            borderColor: '#FFE600',
            backgroundColor: 'rgba(255, 230, 0, 0.25)',
            borderWidth: 2.5,
            pointBackgroundColor: '#FFE600',
            pointBorderColor: '#FFFFFF',
            pointRadius: 5
          },
          {
            label: 'Post-Remediation Target',
            data: [95, 92, 94, 90, 92, 95],
            borderColor: '#00F0FF',
            backgroundColor: 'rgba(0, 240, 255, 0.12)',
            borderWidth: 1.5,
            borderDash: [4, 4],
            pointRadius: 3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: '#FFFFFF', font: { family: 'Rajdhani', size: 13, weight: 700 } }
          }
        },
        scales: {
          r: {
            min: 40,
            max: 100,
            grid: { color: 'rgba(255, 230, 0, 0.15)' },
            angleLines: { color: 'rgba(255, 230, 0, 0.15)' },
            pointLabels: {
              color: '#FFFFFF',
              font: { family: 'Rajdhani', size: 12, weight: 700 }
            },
            ticks: {
              color: '#94A3B8',
              backdropColor: 'transparent',
              font: { family: 'Share Tech Mono', size: 10 }
            }
          }
        }
      }
    });
  }
};
