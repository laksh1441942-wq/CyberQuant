/**
 * CYBERQUANT 2050 // 10/10 INTERACTIVE CYBER MATRIX BACKGROUND ENGINE
 * High-performance HTML5 Canvas: Gravitational Warp, Constellation Mesh,
 * Perspective Cyber Horizon Waves, and Reactive Click Shockwaves.
 */

export class CyberMatrixBackground {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    this.particles = [];
    this.particleCount = 85;
    this.connectionDistance = 140;
    
    this.mouse = { x: -1000, y: -1000, radius: 180 };
    this.shockwaves = [];
    this.gridTime = 0;

    this.init();
  }

  init() {
    this.resize();
    window.addEventListener('resize', () => this.resize());

    // Generate Constellation Particles
    for (let i = 0; i < this.particleCount; i++) {
      this.particles.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        vx: (Math.random() - 0.5) * 0.75,
        vy: (Math.random() - 0.5) * 0.75,
        baseSize: Math.random() * 2.2 + 1.2,
        size: Math.random() * 2.2 + 1.2,
        color: Math.random() > 0.3 ? '#00F2FE' : '#9D4EDD',
        alpha: Math.random() * 0.6 + 0.3,
        pulseSpeed: Math.random() * 0.03 + 0.01,
        pulsePhase: Math.random() * Math.PI * 2
      });
    }

    // Mouse Interaction
    window.addEventListener('mousemove', (e) => {
      this.mouse.x = e.clientX;
      this.mouse.y = e.clientY;
    });

    window.addEventListener('mouseleave', () => {
      this.mouse.x = -1000;
      this.mouse.y = -1000;
    });

    window.addEventListener('click', (e) => {
      this.addShockwave(e.clientX, e.clientY);
    });

    this.animate();
  }

  resize() {
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    this.canvas.width = this.width;
    this.canvas.height = this.height;
  }

  addShockwave(x, y) {
    this.shockwaves.push({
      x,
      y,
      radius: 5,
      maxRadius: 280,
      opacity: 0.8,
      speed: 7.5
    });
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    this.ctx.clearRect(0, 0, this.width, this.height);
    this.gridTime += 0.012;

    // 1. Draw Perspective Cyber Grid Horizon (Bottom Area)
    this.drawPerspectiveGrid();

    // 2. Update & Draw Shockwaves
    this.drawShockwaves();

    // 3. Update & Draw Constellation Mesh
    this.drawConstellation();
  }

  drawPerspectiveGrid() {
    const horizonY = this.height * 0.72;
    const ctx = this.ctx;

    ctx.save();
    ctx.strokeStyle = 'rgba(0, 242, 254, 0.05)';
    ctx.lineWidth = 1;

    // Vertical Vanishing Lines
    const centerX = this.width / 2;
    const numLines = 32;
    for (let i = -numLines; i <= numLines; i++) {
      const xBottom = centerX + (i * this.width) / 16;
      ctx.beginPath();
      ctx.moveTo(centerX, horizonY);
      ctx.lineTo(xBottom, this.height);
      ctx.stroke();
    }

    // Horizontal Moving Perspective Lines
    const step = 20;
    const offset = (this.gridTime * 25) % step;
    for (let y = 0; y < this.height - horizonY; y += step) {
      const actualY = horizonY + y + offset;
      if (actualY <= this.height) {
        const factor = (actualY - horizonY) / (this.height - horizonY);
        ctx.strokeStyle = `rgba(0, 242, 254, ${factor * 0.08})`;
        ctx.beginPath();
        ctx.moveTo(0, actualY);
        ctx.lineTo(this.width, actualY);
        ctx.stroke();
      }
    }
    ctx.restore();
  }

  drawShockwaves() {
    const ctx = this.ctx;
    for (let i = this.shockwaves.length - 1; i >= 0; i--) {
      const sw = this.shockwaves[i];
      sw.radius += sw.speed;
      sw.opacity *= 0.94;

      if (sw.opacity < 0.01 || sw.radius >= sw.maxRadius) {
        this.shockwaves.splice(i, 1);
        continue;
      }

      ctx.save();
      ctx.beginPath();
      ctx.arc(sw.x, sw.y, sw.radius, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(0, 242, 254, ${sw.opacity})`;
      ctx.lineWidth = 2.5;
      ctx.shadowColor = '#00F2FE';
      ctx.shadowBlur = 15;
      ctx.stroke();
      ctx.restore();
    }
  }

  drawConstellation() {
    const ctx = this.ctx;

    // Update Particles
    for (let i = 0; i < this.particles.length; i++) {
      const p = this.particles[i];

      p.x += p.vx;
      p.y += p.vy;

      // Bounce at boundaries
      if (p.x < 0) { p.x = 0; p.vx *= -1; }
      if (p.x > this.width) { p.x = this.width; p.vx *= -1; }
      if (p.y < 0) { p.y = 0; p.vy *= -1; }
      if (p.y > this.height) { p.y = this.height; p.vy *= -1; }

      // Mouse Gravitational Warp
      const dx = this.mouse.x - p.x;
      const dy = this.mouse.y - p.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (dist < this.mouse.radius) {
        const force = (1 - dist / this.mouse.radius) * 3.5;
        const angle = Math.atan2(dy, dx);
        p.x -= Math.cos(angle) * force;
        p.y -= Math.sin(angle) * force;
      }

      // Sine Pulse
      p.pulsePhase += p.pulseSpeed;
      p.size = p.baseSize + Math.sin(p.pulsePhase) * 0.8;

      // Draw Particle
      ctx.save();
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.shadowColor = p.color;
      ctx.shadowBlur = 10;
      ctx.globalAlpha = p.alpha;
      ctx.fill();
      ctx.restore();

      // Connect to other nearby particles
      for (let j = i + 1; j < this.particles.length; j++) {
        const p2 = this.particles[j];
        const pDist = Math.hypot(p.x - p2.x, p.y - p2.y);

        if (pDist < this.connectionDistance) {
          const lineAlpha = (1 - pDist / this.connectionDistance) * 0.28;
          ctx.save();
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = p.color === p2.color ? p.color : '#00F2FE';
          ctx.globalAlpha = lineAlpha;
          ctx.lineWidth = 0.85;
          ctx.stroke();
          ctx.restore();
        }
      }
    }
  }
}
