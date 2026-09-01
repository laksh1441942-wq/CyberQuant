/**
 * CYBERQUANT 2077 // ONIKS_ASTARIT CYBERPUNK UI 01 3D ENGINE (Three.js)
 * Cyber Yellow (#FFE600) Wireframes, Volumetric Tactical Pillars,
 * Dual-Speed Cyan/Yellow Laser Comets, Concentric Angular Gimbals.
 */

import { soundFx } from './audio_fx.js';

export class CyberGlobe3D {
  constructor(containerId, onNodeClick) {
    this.container = document.getElementById(containerId);
    this.onNodeClick = onNodeClick;
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    
    this.globeGroup = new THREE.Group();
    this.gimbalRing1 = null;
    this.gimbalRing2 = null;
    this.arcsGroup = new THREE.Group();
    this.nodes = [];
    this.pillars = [];
    this.satellites = [];
    this.laserPulses = [];
    
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();
    this.targetRotation = { x: 0.2, y: 0 };
    this.currentRotation = { x: 0.2, y: 0 };
    this.isDragging = false;
    this.prevMousePos = { x: 0, y: 0 };
    this.autoRotate = true;
    this.clock = new THREE.Clock();

    if (this.container) {
      this.init();
    }
  }

  init() {
    const width = this.container.clientWidth || 800;
    const height = this.container.clientHeight || 550;

    // 1. Scene & Camera
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 1200);
    this.camera.position.set(0, 20, 245);

    // 2. High-Performance WebGL Renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.container.appendChild(this.renderer.domElement);

    // 3. Cyberpunk Tactical Lighting
    const ambientLight = new THREE.AmbientLight(0xFFE600, 0.6);
    this.scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xFFE600, 2.4);
    keyLight.position.set(150, 180, 200);
    this.scene.add(keyLight);

    const cyanRim = new THREE.DirectionalLight(0x00F0FF, 1.8);
    cyanRim.position.set(-150, -120, 150);
    this.scene.add(cyanRim);

    // 4. Construct Cyberpunk UI 01 World
    this.buildCyberGlobe();
    this.buildLandmassPointCloud();
    this.buildGemstoneNodesAndPillars();
    this.buildTransactionArcs();
    this.buildOrbitingSatellites();
    this.buildStarfield();

    this.globeGroup.add(this.arcsGroup);
    this.scene.add(this.globeGroup);

    // 5. Interaction Setup
    this.setupEvents();

    // 6. Start Render Loop
    this.animate();
  }

  buildCyberGlobe() {
    const radius = 68;

    // A. Cyber Yellow Wireframe Sphere
    const sphereGeo = new THREE.SphereGeometry(radius, 36, 36);
    const wireMat = new THREE.MeshBasicMaterial({
      color: 0xFFE600,
      wireframe: true,
      transparent: true,
      opacity: 0.28
    });
    const wireSphere = new THREE.Mesh(sphereGeo, wireMat);
    this.globeGroup.add(wireSphere);

    // B. Dark Carbon Obsidian Core
    const coreGeo = new THREE.SphereGeometry(radius - 1.5, 32, 32);
    const coreMat = new THREE.MeshBasicMaterial({
      color: 0x090B10,
      transparent: true,
      opacity: 0.95
    });
    const coreSphere = new THREE.Mesh(coreGeo, coreMat);
    this.globeGroup.add(coreSphere);

    // C. Concentric Tactical Gimbals
    const ringGeo1 = new THREE.RingGeometry(radius + 7, radius + 9.5, 64);
    const ringMat1 = new THREE.MeshBasicMaterial({
      color: 0xFFE600,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.55
    });
    this.gimbalRing1 = new THREE.Mesh(ringGeo1, ringMat1);
    this.gimbalRing1.rotation.x = Math.PI / 2.1;
    this.globeGroup.add(this.gimbalRing1);

    const ringGeo2 = new THREE.RingGeometry(radius + 15, radius + 17, 64);
    const ringMat2 = new THREE.MeshBasicMaterial({
      color: 0x00F0FF,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.45
    });
    this.gimbalRing2 = new THREE.Mesh(ringGeo2, ringMat2);
    this.gimbalRing2.rotation.x = Math.PI / 1.7;
    this.gimbalRing2.rotation.y = Math.PI / 3.8;
    this.globeGroup.add(this.gimbalRing2);
  }

  buildLandmassPointCloud() {
    const radius = 68.2;
    const count = 1200;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      const phi = Math.acos(-1 + (2 * i) / count);
      const theta = Math.sqrt(count * Math.PI) * phi;

      positions[i * 3] = radius * Math.cos(theta) * Math.sin(phi);
      positions[i * 3 + 1] = radius * Math.sin(theta) * Math.sin(phi);
      positions[i * 3 + 2] = radius * Math.cos(phi);
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const material = new THREE.PointsMaterial({
      color: 0xFFE600,
      size: 1.4,
      transparent: true,
      opacity: 0.65
    });

    const points = new THREE.Points(geometry, material);
    this.globeGroup.add(points);
  }

  buildGemstoneNodesAndPillars() {
    const radius = 68;
    // Exact banking nodes from README Section 12 & assets.json
    this.assetList = [
      { id: "AST-101", name: "Core Banking Database", lat: 28.6, lon: 77.2, loss: "₹1.85 Cr", color: 0xFF003C, size: 4.2 },
      { id: "AST-102", name: "Customer KYC & PII Store", lat: 19.0, lon: 72.8, loss: "₹1.42 Cr", color: 0xFF003C, size: 3.8 },
      { id: "AST-103", name: "Payment Gateway API", lat: 12.9, lon: 77.5, loss: "₹1.18 Cr", color: 0xFF003C, size: 3.6 },
      { id: "AST-104", name: "Identity & IAM Controller", lat: 17.3, lon: 78.4, loss: "₹96.0 L", color: 0xFFE600, size: 3.2 },
      { id: "AST-105", name: "Treasury Risk Engine", lat: 13.0, lon: 80.2, loss: "₹84.0 L", color: 0xFFE600, size: 3.0 },
      { id: "AST-106", name: "Corporate Active Directory", lat: 22.5, lon: 88.3, loss: "₹71.0 L", color: 0xFFE600, size: 2.8 },
      { id: "AST-107", name: "Secured Perimeter Firewall", lat: 51.5, lon: -0.1, loss: "₹18.0 L", color: 0x00FF66, size: 2.6 },
      { id: "AST-108", name: "Card HSM Security Module", lat: 40.7, lon: -74.0, loss: "₹12.5 L", color: 0x00FF66, size: 2.6 },
      { id: "AST-109", name: "Foreign Exchange Switch", lat: 35.6, lon: 139.6, loss: "₹45.0 L", color: 0x00F0FF, size: 2.9 }
    ];

    this.assetList.forEach(asset => {
      const phi = (90 - asset.lat) * (Math.PI / 180);
      const theta = (asset.lon + 180) * (Math.PI / 180);

      const x = -(radius * Math.sin(phi) * Math.cos(theta));
      const z = radius * Math.sin(phi) * Math.sin(theta);
      const y = radius * Math.cos(phi);

      const pos = new THREE.Vector3(x, y, z);

      // 1. Glowing Node Sphere
      const geo = new THREE.SphereGeometry(asset.size, 16, 16);
      const mat = new THREE.MeshBasicMaterial({ color: asset.color });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.copy(pos);
      mesh.userData = asset;

      // 2. Tactical Halo Ring
      const haloGeo = new THREE.RingGeometry(asset.size * 1.3, asset.size * 2.5, 16);
      const haloMat = new THREE.MeshBasicMaterial({
        color: asset.color,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.7
      });
      const halo = new THREE.Mesh(haloGeo, haloMat);
      halo.lookAt(pos.clone().multiplyScalar(2));
      mesh.add(halo);

      // 3. Volumetric Cyber Light Pillar
      const pillarHeight = 16 + asset.size * 2;
      const pillarGeo = new THREE.CylinderGeometry(0.6, 1.4, pillarHeight, 8);
      const pillarMat = new THREE.MeshBasicMaterial({
        color: asset.color,
        transparent: true,
        opacity: 0.48
      });
      const pillar = new THREE.Mesh(pillarGeo, pillarMat);
      
      const normal = pos.clone().normalize();
      pillar.position.copy(pos.clone().add(normal.clone().multiplyScalar(pillarHeight / 2)));
      pillar.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), normal);

      this.pillars.push(pillar);
      this.globeGroup.add(pillar);

      this.nodes.push(mesh);
      this.globeGroup.add(mesh);
    });
  }

  buildTransactionArcs() {
    const connections = [
      [0, 1], // Core Banking <-> Customer KYC
      [1, 2], // Customer KYC <-> Payment Gateway
      [0, 2], // Core Banking <-> Payment Gateway
      [1, 6], // Customer KYC <-> London Perimeter
      [6, 7], // London <-> New York Card HSM
      [0, 8]  // Core Banking <-> Tokyo FX
    ];

    connections.forEach(([i, j]) => {
      const nodeA = this.nodes[i].position;
      const nodeB = this.nodes[j].position;

      const mid = new THREE.Vector3().addVectors(nodeA, nodeB).multiplyScalar(0.5);
      const dist = nodeA.distanceTo(nodeB);
      mid.setLength(68 + dist * 0.36);

      const curve = new THREE.QuadraticBezierCurve3(nodeA, mid, nodeB);
      const points = curve.getPoints(45);
      const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
      const lineMat = new THREE.LineBasicMaterial({
        color: 0xFFE600,
        transparent: true,
        opacity: 0.45
      });
      const line = new THREE.Line(lineGeo, lineMat);
      this.arcsGroup.add(line);

      // Traveling Laser Pulse Comet
      const pulseGeo = new THREE.SphereGeometry(1.8, 8, 8);
      const pulseMat = new THREE.MeshBasicMaterial({ color: 0xFFE600 });
      const pulseMesh = new THREE.Mesh(pulseGeo, pulseMat);
      this.arcsGroup.add(pulseMesh);

      this.laserPulses.push({
        mesh: pulseMesh,
        curve: curve,
        progress: Math.random(),
        speed: 0.006 + Math.random() * 0.006
      });
    });
  }

  buildOrbitingSatellites() {
    for (let i = 0; i < 5; i++) {
      const satGeo = new THREE.OctahedronGeometry(2.5, 0);
      const satMat = new THREE.MeshBasicMaterial({ color: 0xFFE600 });
      const sat = new THREE.Mesh(satGeo, satMat);

      const orbitRadius = 94 + i * 11;
      const speed = 0.35 + i * 0.12;
      const angleOffset = (i * Math.PI) / 2.5;

      this.satellites.push({ mesh: sat, radius: orbitRadius, speed, angleOffset });
      this.scene.add(sat);
    }
  }

  buildStarfield() {
    const count = 900;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(count * 3);

    for (let i = 0; i < count * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 700;
      positions[i + 1] = (Math.random() - 0.5) * 700;
      positions[i + 2] = (Math.random() - 0.5) * 700;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const material = new THREE.PointsMaterial({
      color: 0xFFE600,
      size: 1.6,
      transparent: true,
      opacity: 0.45
    });

    const starfield = new THREE.Points(geometry, material);
    this.scene.add(starfield);
  }

  setupEvents() {
    window.addEventListener('resize', () => this.onResize());

    const dom = this.renderer.domElement;

    dom.addEventListener('mousedown', (e) => {
      this.isDragging = true;
      this.prevMousePos = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('mouseup', () => {
      this.isDragging = false;
    });

    dom.addEventListener('mousemove', (e) => {
      const rect = dom.getBoundingClientRect();
      this.mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      this.mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      if (this.isDragging) {
        const deltaX = e.clientX - this.prevMousePos.x;
        const deltaY = e.clientY - this.prevMousePos.y;

        this.targetRotation.y += deltaX * 0.006;
        this.targetRotation.x += deltaY * 0.006;

        this.prevMousePos = { x: e.clientX, y: e.clientY };
      }
    });

    dom.addEventListener('click', () => {
      this.raycaster.setFromCamera(this.mouse, this.camera);
      const intersects = this.raycaster.intersectObjects(this.nodes);

      if (intersects.length > 0) {
        const hit = intersects[0].object;
        soundFx.playNodeScan();
        if (this.onNodeClick) {
          this.onNodeClick(hit.userData);
        }
      }
    });
  }

  onResize() {
    if (!this.container) return;
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    const elapsed = this.clock.getElapsedTime();

    if (!this.isDragging && this.autoRotate) {
      this.targetRotation.y += 0.003;
    }

    this.currentRotation.x += (this.targetRotation.x - this.currentRotation.x) * 0.08;
    this.currentRotation.y += (this.targetRotation.y - this.currentRotation.y) * 0.08;

    this.globeGroup.rotation.x = this.currentRotation.x;
    this.globeGroup.rotation.y = this.currentRotation.y;

    if (this.gimbalRing1) this.gimbalRing1.rotation.z += 0.005;
    if (this.gimbalRing2) this.gimbalRing2.rotation.z -= 0.003;

    this.nodes.forEach(node => {
      if (node.children[0]) {
        const scale = 1.0 + Math.sin(elapsed * 4 + node.position.x) * 0.25;
        node.children[0].scale.set(scale, scale, 1);
      }
    });

    this.laserPulses.forEach(pulse => {
      pulse.progress = (pulse.progress + pulse.speed) % 1.0;
      const pt = pulse.curve.getPointAt(pulse.progress);
      pulse.mesh.position.copy(pt);
    });

    this.satellites.forEach(sat => {
      const angle = elapsed * sat.speed + sat.angleOffset;
      sat.mesh.position.x = Math.cos(angle) * sat.radius;
      sat.mesh.position.z = Math.sin(angle) * sat.radius;
      sat.mesh.position.y = Math.sin(angle * 2) * 20;
      sat.mesh.rotation.x += 0.02;
      sat.mesh.rotation.y += 0.03;
    });

    this.renderer.render(this.scene, this.camera);
  }
}
