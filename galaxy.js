/**
 * Miniature Galaxy - Main Simulation & Interaction Engine
 * Three.js 3D Particle Universe with Keplerian Dynamics, Volumetric Core,
 * Binary Star Dance, Wishing Star Easter Egg, MediaPipe Hand Tracking,
 * and Near-Screen Brownian Chaos.
 */

import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

import {
  galaxyVertexShader,
  galaxyFragmentShader,
  coreGlowVertexShader,
  coreGlowFragmentShader,
  bokehVertexShader,
  bokehFragmentShader
} from './shaders.js';

import { cosmicAudio } from './audio.js';

class MiniatureGalaxyApp {
  constructor() {
    this.canvas = document.getElementById('webgl-canvas');
    this.width = window.innerWidth;
    this.height = window.innerHeight;

    // Simulation parameters
    this.params = {
      particleCount: 110000,
      timeScale: 1.0,
      expansion: 1.0,
      collapse: 0.0,
      brightness: 1.25,
      chaos: 0.0,
      cameraDistance: 16.0,
      targetCameraDistance: 16.0,
      isHoldingFist: false,
      isWebcamActive: false,
      wishingStarCountdown: 90.0, // 90 seconds easter egg
    };

    // Interaction state
    this.targetRotation = { x: 0.55, y: 0.0 };
    this.currentRotation = { x: 0.55, y: 0.0 };
    this.mouse = { x: 0, y: 0, isDown: false, lastDownTime: 0 };
    this.supernovaState = {
      time: -1.0,
      intensity: 0.0
    };

    // Clock
    this.clock = new THREE.Clock();

    this.initThree();
    this.createVolumetricCore();
    this.createGalaxyParticles();
    this.createBokehDust();
    this.createBinaryStars();
    this.createWishingStar();
    this.createComet();
    this.setupPostProcessing();
    this.setupEventListeners();
    this.setupUI();

    // Start render loop
    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
  }

  initThree() {
    // 1. Scene
    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(0x020208, 0.012);

    // 2. Camera
    this.camera = new THREE.PerspectiveCamera(55, this.width / this.height, 0.1, 1000);
    this.camera.position.set(0, 8.5, this.params.cameraDistance);
    this.camera.lookAt(0, 0, 0);

    // 3. Renderer
    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: true,
      alpha: false,
      powerPreference: 'high-performance'
    });
    this.renderer.setSize(this.width, this.height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.35;

    // Galactic Container for gentle rotation and camera tilt
    this.galaxyGroup = new THREE.Group();
    this.scene.add(this.galaxyGroup);
  }

  setupPostProcessing() {
    this.composer = new EffectComposer(this.renderer);
    const renderPass = new RenderPass(this.scene, this.camera);
    this.composer.addPass(renderPass);

    // Cinema-grade Bloom Pass for dazzling star spikes and glowing filaments
    const bloomPass = new UnrealBloomPass(
      new THREE.Vector2(this.width, this.height),
      1.35, // strength
      0.55, // radius
      0.72  // threshold
    );
    this.composer.addPass(bloomPass);
    this.bloomPass = bloomPass;
  }

  /**
   * Layer 1: Volumetric Core Glow
   * Heart of the galaxy pulsating with living density
   */
  createVolumetricCore() {
    const coreGeo = new THREE.PlaneGeometry(6.5, 6.5);
    this.coreMaterial = new THREE.ShaderMaterial({
      vertexShader: coreGlowVertexShader,
      fragmentShader: coreGlowFragmentShader,
      uniforms: {
        uTime: { value: 0 },
        uBreath: { value: 0 },
        uExpansion: { value: 1.0 },
        uCollapse: { value: 0.0 },
        uSupernovaTime: { value: -1.0 }
      },
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      side: THREE.DoubleSide
    });

    // 4 Intersecting volumetric billboard core layers for full 3D depth
    this.coreMesh1 = new THREE.Mesh(coreGeo, this.coreMaterial);
    this.coreMesh2 = new THREE.Mesh(coreGeo, this.coreMaterial);
    this.coreMesh2.rotation.y = Math.PI * 0.5;

    this.coreMesh3 = new THREE.Mesh(coreGeo, this.coreMaterial);
    this.coreMesh3.rotation.x = Math.PI * 0.5;

    this.coreMesh4 = new THREE.Mesh(coreGeo, this.coreMaterial);
    this.coreMesh4.rotation.y = Math.PI * 0.25;
    this.coreMesh4.rotation.x = Math.PI * 0.25;

    this.galaxyGroup.add(this.coreMesh1);
    this.galaxyGroup.add(this.coreMesh2);
    this.galaxyGroup.add(this.coreMesh3);
    this.galaxyGroup.add(this.coreMesh4);
  }

  /**
   * Layer 2 & 3: Main Galaxy Particles (Core + 4 Spiral Arms + Ambient Dust + Filaments)
   */
  createGalaxyParticles() {
    const count = this.params.particleCount;
    const geometry = new THREE.BufferGeometry();

    const positions = new Float32Array(count * 3);
    const aOrbitRadius = new Float32Array(count);
    const aOrbitAngle = new Float32Array(count);
    const aOrbitSpeed = new Float32Array(count);
    const aArmOffset = new Float32Array(count);
    const aVerticalOffset = new Float32Array(count);
    const aParticleSize = new Float32Array(count);
    const aParticleType = new Float32Array(count);
    const aColorSeed = new Float32Array(count);

    // Distribution partitioning:
    // Core: 20%, Spiral arms: 50%, Filaments: 10%, Ambient deep dust: 20%
    const coreCount = Math.floor(count * 0.20);
    const armCount = Math.floor(count * 0.50);
    const filamentCount = Math.floor(count * 0.10);
    const ambientCount = count - coreCount - armCount - filamentCount;

    let idx = 0;

    // Helper: Box-Muller Gaussian random
    const randGaussian = (mean = 0, stdev = 1) => {
      let u = 1 - Math.random();
      let v = Math.random();
      let z = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
      return z * stdev + mean;
    };

    // 1. Core Cluster Particles (Intensely dense, high-frequency orbit)
    for (let i = 0; i < coreCount; i++, idx++) {
      const r = Math.pow(Math.random(), 2.2) * 2.2 + 0.08;
      const angle = Math.random() * Math.PI * 2;
      // Keplerian speed: inner speeds are fast
      const speed = (1.55 / Math.sqrt(r + 0.15)) * (0.9 + Math.random() * 0.25);

      aOrbitRadius[idx] = r;
      aOrbitAngle[idx] = angle;
      aOrbitSpeed[idx] = speed;
      aArmOffset[idx] = randGaussian(0, 0.08);
      aVerticalOffset[idx] = randGaussian(0, 0.35) * (1.0 - r / 2.5);
      // Particle size distribution: few bright gems, many delicate points
      aParticleSize[idx] = Math.pow(Math.random(), 3.5) * 8.0 + 1.6;
      aParticleType[idx] = 0.0; // Core
      aColorSeed[idx] = Math.random();
    }

    // 2. Spiral Arms (4 Logarithmic Arms: 2 major, 2 minor)
    const numArms = 4;
    for (let i = 0; i < armCount; i++, idx++) {
      const armIndex = i % numArms;
      const isMajorArm = armIndex < 2;
      const armBaseAngle = (armIndex * (Math.PI * 2 / numArms));

      // Radius distribution along the disk
      const r = 1.4 + Math.pow(Math.random(), 1.15) * 11.5;

      // Logarithmic spiral angle: theta = armAngle + b * ln(r/r0)
      const windingConstant = 2.4;
      const spiralTheta = armBaseAngle + windingConstant * Math.log(r / 1.4 + 1.0);

      // Arm width dispersion (flares outward)
      const dispersionWidth = (0.15 + r * 0.065) * (isMajorArm ? 1.0 : 1.4);
      const angleJitter = randGaussian(0, dispersionWidth / r);

      const speed = (1.4 / Math.sqrt(r + 0.2)) * (0.85 + Math.random() * 0.3);

      aOrbitRadius[idx] = r;
      aOrbitAngle[idx] = spiralTheta + angleJitter;
      aOrbitSpeed[idx] = speed;
      aArmOffset[idx] = randGaussian(0, 0.12);
      aVerticalOffset[idx] = randGaussian(0, 0.5) * (0.1 + r * 0.06);
      aParticleSize[idx] = Math.pow(Math.random(), 4.0) * 10.0 + 1.4;
      aParticleType[idx] = 1.0; // Spiral Arm
      aColorSeed[idx] = Math.random();
    }

    // 3. Trailing Filament Tracers (High-speed ribbon stars with long tail feel)
    for (let i = 0; i < filamentCount; i++, idx++) {
      const armIndex = i % 2;
      const armBaseAngle = armIndex * Math.PI;
      const r = 2.0 + Math.random() * 9.5;
      const spiralTheta = armBaseAngle + 2.5 * Math.log(r / 1.5 + 1.0);

      const speed = (1.6 / Math.sqrt(r + 0.1)) * 1.1; // Slightly faster for shear

      aOrbitRadius[idx] = r;
      aOrbitAngle[idx] = spiralTheta + randGaussian(0, 0.04);
      aOrbitSpeed[idx] = speed;
      aArmOffset[idx] = randGaussian(0, 0.05);
      aVerticalOffset[idx] = randGaussian(0, 0.2) * 0.08;
      aParticleSize[idx] = Math.pow(Math.random(), 3.0) * 6.5 + 2.2;
      aParticleType[idx] = 3.0; // Filament
      aColorSeed[idx] = Math.random();
    }

    // 4. Ambient Deep Space Dust (Ethereal vast cloud)
    for (let i = 0; i < ambientCount; i++, idx++) {
      const r = 1.5 + Math.pow(Math.random(), 0.9) * 22.0;
      const angle = Math.random() * Math.PI * 2;
      const speed = (0.7 / Math.sqrt(r + 0.5)) * (0.6 + Math.random() * 0.8);

      aOrbitRadius[idx] = r;
      aOrbitAngle[idx] = angle;
      aOrbitSpeed[idx] = speed;
      aArmOffset[idx] = (Math.random() - 0.5) * 4.0;
      aVerticalOffset[idx] = randGaussian(0, 2.5);
      aParticleSize[idx] = Math.random() * 2.5 + 0.8;
      aParticleType[idx] = 2.0; // Ambient Dust
      aColorSeed[idx] = Math.random();
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('aOrbitRadius', new THREE.BufferAttribute(aOrbitRadius, 1));
    geometry.setAttribute('aOrbitAngle', new THREE.BufferAttribute(aOrbitAngle, 1));
    geometry.setAttribute('aOrbitSpeed', new THREE.BufferAttribute(aOrbitSpeed, 1));
    geometry.setAttribute('aArmOffset', new THREE.BufferAttribute(aArmOffset, 1));
    geometry.setAttribute('aVerticalOffset', new THREE.BufferAttribute(aVerticalOffset, 1));
    geometry.setAttribute('aParticleSize', new THREE.BufferAttribute(aParticleSize, 1));
    geometry.setAttribute('aParticleType', new THREE.BufferAttribute(aParticleType, 1));
    geometry.setAttribute('aColorSeed', new THREE.BufferAttribute(aColorSeed, 1));

    this.galaxyUniforms = {
      uTime: { value: 0 },
      uTimeScale: { value: 1.0 },
      uExpansion: { value: 1.0 },
      uCollapse: { value: 0.0 },
      uBreath: { value: 0 },
      uChaos: { value: 0.0 },
      uSupernovaTime: { value: -1.0 },
      uSupernovaIntensity: { value: 0.0 },
      uPixelRatio: { value: Math.min(window.devicePixelRatio, 2) },
      uBrightness: { value: 1.25 }
    };

    this.galaxyMaterial = new THREE.ShaderMaterial({
      vertexShader: galaxyVertexShader,
      fragmentShader: galaxyFragmentShader,
      uniforms: this.galaxyUniforms,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    this.galaxyPoints = new THREE.Points(geometry, this.galaxyMaterial);
    this.galaxyGroup.add(this.galaxyPoints);
  }

  /**
   * Layer 4: Foreground Shallow DOF Bokeh Dust
   * Close floating dust motes drifting across the camera lens
   */
  createBokehDust() {
    const bokehCount = 650;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(bokehCount * 3);
    const aSize = new Float32Array(bokehCount);
    const aColor = new Float32Array(bokehCount * 3);

    const palette = [
      new THREE.Color('#ffd166'),
      new THREE.Color('#70d6ff'),
      new THREE.Color('#ff70a6'),
      new THREE.Color('#e0fbfc')
    ];

    for (let i = 0; i < bokehCount; i++) {
      positions[i * 3 + 0] = (Math.random() - 0.5) * 24.0;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 16.0;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 20.0 + 4.0;

      aSize[i] = Math.pow(Math.random(), 2.0) * 26.0 + 8.0;

      const col = palette[Math.floor(Math.random() * palette.length)];
      aColor[i * 3 + 0] = col.r;
      aColor[i * 3 + 1] = col.g;
      aColor[i * 3 + 2] = col.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('aSize', new THREE.BufferAttribute(aSize, 1));
    geometry.setAttribute('aColor', new THREE.BufferAttribute(aColor, 3));

    this.bokehUniforms = {
      uTime: { value: 0 },
      uPixelRatio: { value: Math.min(window.devicePixelRatio, 2) }
    };

    this.bokehMaterial = new THREE.ShaderMaterial({
      vertexShader: bokehVertexShader,
      fragmentShader: bokehFragmentShader,
      uniforms: this.bokehUniforms,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    this.bokehPoints = new THREE.Points(geometry, this.bokehMaterial);
    this.scene.add(this.bokehPoints);
  }

  /**
   * Layer 5: Binary Stars (双子星互绕环舞)
   * Two radiant twin stars dancing around their common barycenter near the galactic nucleus
   */
  createBinaryStars() {
    this.binaryGroup = new THREE.Group();

    // Twin star spheres
    const starGeo = new THREE.SphereGeometry(0.14, 16, 16);
    const mat1 = new THREE.MeshBasicMaterial({ color: 0xffe066 });
    const mat2 = new THREE.MeshBasicMaterial({ color: 0x70d6ff });

    this.twinStar1 = new THREE.Mesh(starGeo, mat1);
    this.twinStar2 = new THREE.Mesh(starGeo, mat2);

    this.binaryGroup.add(this.twinStar1);
    this.binaryGroup.add(this.twinStar2);

    // Glowing intertwined trails for both twin stars
    this.trailLength = 80;
    this.trailPositions1 = new Float32Array(this.trailLength * 3);
    this.trailPositions2 = new Float32Array(this.trailLength * 3);

    const trailGeo1 = new THREE.BufferGeometry();
    trailGeo1.setAttribute('position', new THREE.BufferAttribute(this.trailPositions1, 3));
    const trailMat1 = new THREE.LineBasicMaterial({
      color: 0xffe066,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending
    });
    this.binaryTrail1 = new THREE.Line(trailGeo1, trailMat1);

    const trailGeo2 = new THREE.BufferGeometry();
    trailGeo2.setAttribute('position', new THREE.BufferAttribute(this.trailPositions2, 3));
    const trailMat2 = new THREE.LineBasicMaterial({
      color: 0x70d6ff,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending
    });
    this.binaryTrail2 = new THREE.Line(trailGeo2, trailMat2);

    this.binaryGroup.add(this.binaryTrail1);
    this.binaryGroup.add(this.binaryTrail2);

    this.galaxyGroup.add(this.binaryGroup);
  }

  /**
   * Layer 6: Comet & 90s Wishing Star Easter Egg (星愿彩蛋)
   */
  createWishingStar() {
    this.wishingStarActive = false;
    this.wishingStarProgress = 0;
    this.wishingStarTrailLength = 60;

    const trailGeo = new THREE.BufferGeometry();
    this.wishingStarPoints = new Float32Array(this.wishingStarTrailLength * 3);
    trailGeo.setAttribute('position', new THREE.BufferAttribute(this.wishingStarPoints, 3));

    this.wishingStarMaterial = new THREE.LineBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.95,
      blending: THREE.AdditiveBlending
    });

    this.wishingStarMesh = new THREE.Line(trailGeo, this.wishingStarMaterial);
    this.wishingStarMesh.visible = false;
    this.scene.add(this.wishingStarMesh);

    // Blazing head for shooting star
    const headGeo = new THREE.SphereGeometry(0.28, 16, 16);
    const headMat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      blending: THREE.AdditiveBlending
    });
    this.wishingStarHead = new THREE.Mesh(headGeo, headMat);
    this.wishingStarHead.visible = false;
    this.scene.add(this.wishingStarHead);
  }

  triggerWishingStar() {
    if (this.wishingStarActive) return;

    this.wishingStarActive = true;
    this.wishingStarProgress = 0;
    this.wishingStarMesh.visible = true;

    // Trajectory: arc across upper field of view
    this.starStart = new THREE.Vector3(-25, 12, (Math.random() - 0.5) * 8 - 4);
    this.starEnd = new THREE.Vector3(25, -6, (Math.random() - 0.5) * 8 + 6);

    // Reset trail buffer
    for (let i = 0; i < this.wishingStarTrailLength * 3; i += 3) {
      this.wishingStarPoints[i] = this.starStart.x;
      this.wishingStarPoints[i + 1] = this.starStart.y;
      this.wishingStarPoints[i + 2] = this.starStart.z;
    }

    cosmicAudio.playWishingStar();

    // Show banner
    const banner = document.getElementById('wishing-star-banner');
    if (banner) {
      banner.classList.add('show');
      setTimeout(() => banner.classList.remove('show'), 4000);
    }
  }

  /**
   * Layer 7: Deep Space Sporadic Comet (偶尔一颗彗星拖长尾划破星域)
   */
  createComet() {
    this.cometActive = false;
    this.cometProgress = 0;
    this.cometCooldown = 22.0;
    this.cometTrailLength = 55;

    const trailGeo = new THREE.BufferGeometry();
    this.cometPoints = new Float32Array(this.cometTrailLength * 3);
    trailGeo.setAttribute('position', new THREE.BufferAttribute(this.cometPoints, 3));

    this.cometMaterial = new THREE.LineBasicMaterial({
      color: 0x5af5cf,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending
    });

    this.cometMesh = new THREE.Line(trailGeo, this.cometMaterial);
    this.cometMesh.visible = false;
    this.scene.add(this.cometMesh);

    const headGeo = new THREE.SphereGeometry(0.22, 16, 16);
    const headMat = new THREE.MeshBasicMaterial({
      color: 0xc8fff4,
      blending: THREE.AdditiveBlending
    });
    this.cometHead = new THREE.Mesh(headGeo, headMat);
    this.cometHead.visible = false;
    this.scene.add(this.cometHead);
  }

  triggerComet() {
    if (this.cometActive) return;

    this.cometActive = true;
    this.cometProgress = 0;
    this.cometMesh.visible = true;
    this.cometHead.visible = true;

    // Random oblique traversal through deep space
    const yStart = (Math.random() - 0.5) * 16.0 + 8.0;
    const yEnd = -yStart + (Math.random() - 0.5) * 6.0;
    this.cometStart = new THREE.Vector3(-28.0, yStart, (Math.random() - 0.5) * 14.0);
    this.cometEnd = new THREE.Vector3(28.0, yEnd, (Math.random() - 0.5) * 14.0);

    for (let i = 0; i < this.cometTrailLength * 3; i += 3) {
      this.cometPoints[i] = this.cometStart.x;
      this.cometPoints[i + 1] = this.cometStart.y;
      this.cometPoints[i + 2] = this.cometStart.z;
    }
  }

  /**
   * Supernova detonation event
   */
  triggerSupernova() {
    this.supernovaState.time = 0.0;
    this.supernovaState.intensity = 1.0;

    // Screen flash
    const overlay = document.getElementById('supernova-overlay');
    if (overlay) {
      overlay.className = 'supernova-overlay flash';
      setTimeout(() => {
        overlay.className = 'supernova-overlay decay';
      }, 70);
    }

    cosmicAudio.playSupernova();

    // Poetic message toast
    this.showPoeticToast('超新星爆发', '光之涟漪荡开，宇宙在心跳中重归秩序');
  }

  showPoeticToast(title, subtitle) {
    const toast = document.getElementById('poetic-toast');
    const toastTitle = document.getElementById('toast-title');
    const toastSub = document.getElementById('toast-sub');
    if (toast && toastTitle && toastSub) {
      toastTitle.textContent = title;
      toastSub.textContent = subtitle;
      toast.classList.add('visible');
      clearTimeout(this.toastTimer);
      this.toastTimer = setTimeout(() => {
        toast.classList.remove('visible');
      }, 3600);
    }
  }

  setupEventListeners() {
    // Resize
    window.addEventListener('resize', () => {
      this.width = window.innerWidth;
      this.height = window.innerHeight;
      this.camera.aspect = this.width / this.height;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(this.width, this.height);
      this.composer.setSize(this.width, this.height);
      const pr = Math.min(window.devicePixelRatio, 2);
      this.galaxyUniforms.uPixelRatio.value = pr;
      this.bokehUniforms.uPixelRatio.value = pr;
    });

    // Mouse Controls
    window.addEventListener('mousedown', (e) => {
      // Ignore click on UI
      if (e.target.closest('.control-dock') || e.target.closest('.webcam-panel') || e.target.closest('.app-header')) {
        return;
      }
      this.mouse.isDown = true;
      this.mouse.x = e.clientX;
      this.mouse.y = e.clientY;

      // Double-click check for Supernova
      const now = performance.now();
      if (now - this.mouse.lastDownTime < 320) {
        this.triggerSupernova();
      }
      this.mouse.lastDownTime = now;
    });

    window.addEventListener('mouseup', () => {
      this.mouse.isDown = false;
      this.params.isHoldingFist = false;
    });

    window.addEventListener('mousemove', (e) => {
      // Gentle camera parallax / holding the galaxy in hand
      const normX = (e.clientX / this.width - 0.5) * 2;
      const normY = (e.clientY / this.height - 0.5) * 2;

      this.targetRotation.y = normX * 0.75;
      this.targetRotation.x = 0.55 + normY * 0.45;

      if (this.mouse.isDown) {
        // Holding down mouse simulates clutching the galaxy into a fist
        this.params.isHoldingFist = true;
      }
    });

    // Zoom / Near-Screen Chaos Wheel
    window.addEventListener('wheel', (e) => {
      this.params.targetCameraDistance += e.deltaY * 0.015;
      this.params.targetCameraDistance = THREE.MathUtils.clamp(this.params.targetCameraDistance, 2.5, 32.0);
    }, { passive: true });

    // Touch events for mobile/tablet
    let touchStartDist = 0;
    window.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        this.mouse.isDown = true;
        this.params.isHoldingFist = true;
        const now = performance.now();
        if (now - this.mouse.lastDownTime < 320) {
          this.triggerSupernova();
        }
        this.mouse.lastDownTime = now;
      } else if (e.touches.length === 2) {
        touchStartDist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
      }
    });

    window.addEventListener('touchend', () => {
      this.mouse.isDown = false;
      this.params.isHoldingFist = false;
    });

    window.addEventListener('touchmove', (e) => {
      if (e.touches.length === 1) {
        const normX = (e.touches[0].clientX / this.width - 0.5) * 2;
        const normY = (e.touches[0].clientY / this.height - 0.5) * 2;
        this.targetRotation.y = normX * 0.75;
        this.targetRotation.x = 0.55 + normY * 0.45;
      } else if (e.touches.length === 2) {
        const dist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
        const delta = (touchStartDist - dist) * 0.05;
        this.params.targetCameraDistance += delta;
        this.params.targetCameraDistance = THREE.MathUtils.clamp(this.params.targetCameraDistance, 2.5, 32.0);
        touchStartDist = dist;
      }
    });

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
      switch (e.key.toLowerCase()) {
        case 'h': // Hide/Show UI
          document.body.classList.toggle('ui-hidden');
          break;
        case 'f': // Fullscreen
          this.toggleFullscreen();
          break;
        case ' ': // Space: Supernova
          e.preventDefault();
          this.triggerSupernova();
          break;
        case 'w': // Wishing Star
          this.triggerWishingStar();
          break;
        case 'm': // Audio Toggle
          this.toggleSoundUI();
          break;
      }
    });
  }

  toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  }

  toggleSoundUI() {
    const isPlaying = cosmicAudio.toggleSound();
    const btn = document.getElementById('btn-sound');
    if (btn) {
      btn.innerHTML = isPlaying ? '<span>🔊</span> 声音' : '<span>🔇</span> 静音';
      btn.classList.toggle('active', isPlaying);
    }
    if (isPlaying) {
      this.showPoeticToast('天籁苏醒', '432Hz 谐波微风与星核心跳共振');
    }
  }

  setupUI() {
    // Time speed slider
    const slider = document.getElementById('speed-slider');
    if (slider) {
      slider.addEventListener('input', (e) => {
        this.params.timeScale = parseFloat(e.target.value);
        this.galaxyUniforms.uTimeScale.value = this.params.timeScale;
      });
    }

    // Fullscreen button
    const fsBtn = document.getElementById('btn-fullscreen');
    if (fsBtn) {
      fsBtn.addEventListener('click', () => this.toggleFullscreen());
    }

    // Supernova button
    const snBtn = document.getElementById('btn-supernova');
    if (snBtn) {
      snBtn.addEventListener('click', () => this.triggerSupernova());
    }

    // Wishing star button
    const wsBtn = document.getElementById('btn-wish');
    if (wsBtn) {
      wsBtn.addEventListener('click', () => this.triggerWishingStar());
    }

    // Sound button
    const soundBtn = document.getElementById('btn-sound');
    if (soundBtn) {
      soundBtn.addEventListener('click', () => this.toggleSoundUI());
    }

    // Hand State Button (Toggles Fist / Open Palm manually)
    const handBtn = document.getElementById('btn-hand');
    if (handBtn) {
      handBtn.addEventListener('click', () => {
        this.params.isHoldingFist = !this.params.isHoldingFist;
        handBtn.classList.toggle('active', this.params.isHoldingFist);
        handBtn.innerHTML = this.params.isHoldingFist ? '<span>✊</span> 握拳坍缩' : '<span>🖐️</span> 张手绽放';
        this.showPoeticToast(
          this.params.isHoldingFist ? '握拳 · 宇宙坍缩' : '张手 · 银河绽放',
          this.params.isHoldingFist ? '万星向星核坠落，光芒收敛入微' : '旋臂舒展、星辉苏醒，银河为你点燃'
        );
      });
    }

    // Webcam AI Hand Tracking Toggle
    const camBtn = document.getElementById('btn-webcam');
    if (camBtn) {
      camBtn.addEventListener('click', () => {
        this.toggleWebcamTracking();
      });
    }
  }

  /**
   * MediaPipe Hands Integration for Live AI Hand Tracking
   */
  async toggleWebcamTracking() {
    const panel = document.getElementById('webcam-panel');
    const btn = document.getElementById('btn-webcam');

    if (this.params.isWebcamActive) {
      // Stop tracking
      this.params.isWebcamActive = false;
      if (this.cameraStream) {
        this.cameraStream.getTracks().forEach(track => track.stop());
      }
      if (panel) panel.classList.add('hidden');
      if (btn) btn.classList.remove('active');
      return;
    }

    try {
      if (btn) btn.textContent = '⌛ 加载AI模型...';
      const video = document.getElementById('webcam-video');

      // Request camera
      this.cameraStream = await navigator.mediaDevices.getUserMedia({
        video: { width: 320, height: 240, facingMode: 'user' }
      });
      video.srcObject = this.cameraStream;
      await video.play();

      // Check MediaPipe availability
      if (!window.Hands) {
        await this.loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js');
        await this.loadScript('https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js');
      }

      const hands = new window.Hands({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
      });

      hands.setOptions({
        maxNumHands: 1,
        modelComplexity: 1,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
      });

      hands.onResults((results) => {
        this.onHandResults(results);
      });

      // Frame processor
      const processVideo = async () => {
        if (!this.params.isWebcamActive) return;
        await hands.send({ image: video });
        requestAnimationFrame(processVideo);
      };

      this.params.isWebcamActive = true;
      if (panel) panel.classList.remove('hidden');
      if (btn) {
        btn.classList.add('active');
        btn.innerHTML = '<span>🖐️</span> AI手势已开启';
      }
      this.showPoeticToast('手势连接成功', '张开手掌舒展银河，合拢拳头坍缩深空');
      processVideo();
    } catch (err) {
      console.warn('Webcam/MediaPipe initialization failed:', err);
      alert('摄像头手势启动失败（可能无摄像头权限或离线）。您可直接使用鼠标按住/拖动/滚轮享受完整手势交互！');
      if (btn) {
        btn.classList.remove('active');
        btn.innerHTML = '<span>🖐️</span> 开启手势';
      }
    }
  }

  loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  /**
   * Process landmarks from MediaPipe Hands
   */
  onHandResults(results) {
    if (!results.multiHandLandmarks || results.multiHandLandmarks.length === 0) {
      return;
    }

    const landmarks = results.multiHandLandmarks[0];
    const wrist = landmarks[0];
    const fingerTips = [landmarks[4], landmarks[8], landmarks[12], landmarks[16], landmarks[20]];

    // Compute average distance between fingertips and wrist
    let totalDist = 0;
    for (const tip of fingerTips) {
      const dx = tip.x - wrist.x;
      const dy = tip.y - wrist.y;
      totalDist += Math.sqrt(dx * dx + dy * dy);
    }
    const avgDist = totalDist / fingerTips.length;

    // Hand Openness (0.15 = tight fist, 0.45+ = wide open palm)
    const openness = THREE.MathUtils.clamp((avgDist - 0.20) / 0.28, 0.0, 1.0);

    if (openness < 0.3) {
      // Clenched fist -> Universe collapses
      this.params.isHoldingFist = true;
    } else {
      // Open hand -> Universe expands
      this.params.isHoldingFist = false;
    }

    // Camera tilt follows palm position (Mirror x)
    const palmX = 1.0 - wrist.x;
    const palmY = wrist.y;
    this.targetRotation.y = (palmX - 0.5) * 1.5;
    this.targetRotation.x = 0.55 + (palmY - 0.5) * 0.9;

    // Draw hand skeleton on mini canvas
    const canvas = document.getElementById('webcam-canvas');
    if (canvas) {
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = this.params.isHoldingFist ? '#70d6ff' : '#ffd166';
      for (const pt of landmarks) {
        ctx.beginPath();
        ctx.arc(pt.x * canvas.width, pt.y * canvas.height, 2.5, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }

  /**
   * Main Render Loop
   */
  animate() {
    requestAnimationFrame(this.animate);

    const delta = this.clock.getDelta();
    const elapsedTime = this.clock.getElapsedTime();

    // 1. Smooth Camera Orbit & Parallax
    this.currentRotation.x += (this.targetRotation.x - this.currentRotation.x) * 0.05;
    this.currentRotation.y += (this.targetRotation.y - this.currentRotation.y) * 0.05;

    this.params.cameraDistance += (this.params.targetCameraDistance - this.params.cameraDistance) * 0.08;

    // Grand macro-scale slow rotation (斗转星移)
    const macroRotation = elapsedTime * 0.02 * this.params.timeScale;
    this.galaxyGroup.rotation.y = macroRotation + this.currentRotation.y;
    this.galaxyGroup.rotation.x = this.currentRotation.x;

    this.camera.position.z = this.params.cameraDistance;

    // 2. Expansion / Collapse State Lerp
    const targetCollapse = this.params.isHoldingFist ? 1.0 : 0.0;
    const targetExpansion = this.params.isHoldingFist ? 0.15 : 1.15;

    this.params.collapse += (targetCollapse - this.params.collapse) * 0.065;
    this.params.expansion += (targetExpansion - this.params.expansion) * 0.065;

    // Breathing pulse (心跳与呼吸感)
    const breath = Math.sin(elapsedTime * 1.8) * 0.1;

    // 3. Near-Screen Chaos Calculation (近屏混沌 / 浪漫的失控)
    // When camera is very close or zoom is deep, chaos ramps up
    const nearScreenThreshold = 6.8;
    let targetChaos = 0.0;
    if (this.params.cameraDistance < nearScreenThreshold) {
      targetChaos = (nearScreenThreshold - this.params.cameraDistance) / 4.0;
      targetChaos = THREE.MathUtils.clamp(targetChaos, 0.0, 1.0);
    }
    this.params.chaos += (targetChaos - this.params.chaos) * 0.1;

    // 4. Update Uniforms
    this.galaxyUniforms.uTime.value = elapsedTime;
    this.galaxyUniforms.uExpansion.value = this.params.expansion;
    this.galaxyUniforms.uCollapse.value = this.params.collapse;
    this.galaxyUniforms.uBreath.value = breath;
    this.galaxyUniforms.uChaos.value = this.params.chaos;
    this.galaxyUniforms.uBrightness.value = this.params.brightness;

    // Core Glow
    this.coreMaterial.uniforms.uTime.value = elapsedTime;
    this.coreMaterial.uniforms.uBreath.value = breath;
    this.coreMaterial.uniforms.uExpansion.value = this.params.expansion;
    this.coreMaterial.uniforms.uCollapse.value = this.params.collapse;

    // Bokeh Dust
    this.bokehUniforms.uTime.value = elapsedTime;

    // 5. Supernova Propagation
    if (this.supernovaState.time >= 0.0) {
      this.supernovaState.time += delta;
      this.galaxyUniforms.uSupernovaTime.value = this.supernovaState.time;
      this.galaxyUniforms.uSupernovaIntensity.value = this.supernovaState.intensity;
      this.coreMaterial.uniforms.uSupernovaTime.value = this.supernovaState.time;

      if (this.supernovaState.time > 4.5) {
        this.supernovaState.time = -1.0;
        this.galaxyUniforms.uSupernovaTime.value = -1.0;
        this.coreMaterial.uniforms.uSupernovaTime.value = -1.0;
      }
    }

    // 6. Binary Stars Dynamics (双子星互绕舞蹈)
    const binarySpeed = elapsedTime * 2.2 * this.params.timeScale;
    const binaryR = 0.75 * (1.0 - this.params.collapse * 0.65);
    const star1X = Math.cos(binarySpeed) * binaryR;
    const star1Z = Math.sin(binarySpeed) * binaryR;
    const star2X = -star1X;
    const star2Z = -star1Z;
    const starY = Math.sin(binarySpeed * 1.5) * 0.12;

    this.twinStar1.position.set(star1X, starY, star1Z);
    this.twinStar2.position.set(star2X, -starY, star2Z);

    // Update intertwined trails for both stars
    for (let i = this.trailLength - 1; i > 0; i--) {
      this.trailPositions1[i * 3 + 0] = this.trailPositions1[(i - 1) * 3 + 0];
      this.trailPositions1[i * 3 + 1] = this.trailPositions1[(i - 1) * 3 + 1];
      this.trailPositions1[i * 3 + 2] = this.trailPositions1[(i - 1) * 3 + 2];

      this.trailPositions2[i * 3 + 0] = this.trailPositions2[(i - 1) * 3 + 0];
      this.trailPositions2[i * 3 + 1] = this.trailPositions2[(i - 1) * 3 + 1];
      this.trailPositions2[i * 3 + 2] = this.trailPositions2[(i - 1) * 3 + 2];
    }
    this.trailPositions1[0] = star1X;
    this.trailPositions1[1] = starY;
    this.trailPositions1[2] = star1Z;

    this.trailPositions2[0] = star2X;
    this.trailPositions2[1] = -starY;
    this.trailPositions2[2] = star2Z;

    this.binaryTrail1.geometry.attributes.position.needsUpdate = true;
    this.binaryTrail2.geometry.attributes.position.needsUpdate = true;

    // 7. Wishing Star Update (星愿彩蛋)
    this.params.wishingStarCountdown -= delta;
    if (this.params.wishingStarCountdown <= 0) {
      this.triggerWishingStar();
      this.params.wishingStarCountdown = 90.0 + Math.random() * 20.0;
    }

    if (this.wishingStarActive) {
      this.wishingStarProgress += delta * 0.35; // ~3 seconds duration
      if (this.wishingStarProgress >= 1.0) {
        this.wishingStarActive = false;
        this.wishingStarMesh.visible = false;
        if (this.wishingStarHead) this.wishingStarHead.visible = false;
      } else {
        const currentPos = new THREE.Vector3().lerpVectors(
          this.starStart,
          this.starEnd,
          this.wishingStarProgress
        );
        if (this.wishingStarHead) {
          this.wishingStarHead.visible = true;
          this.wishingStarHead.position.copy(currentPos);
        }
        // Shift trail points
        for (let i = this.wishingStarTrailLength - 1; i > 0; i--) {
          this.wishingStarPoints[i * 3 + 0] = this.wishingStarPoints[(i - 1) * 3 + 0];
          this.wishingStarPoints[i * 3 + 1] = this.wishingStarPoints[(i - 1) * 3 + 1];
          this.wishingStarPoints[i * 3 + 2] = this.wishingStarPoints[(i - 1) * 3 + 2];
        }
        this.wishingStarPoints[0] = currentPos.x;
        this.wishingStarPoints[1] = currentPos.y;
        this.wishingStarPoints[2] = currentPos.z;
        this.wishingStarMesh.geometry.attributes.position.needsUpdate = true;
      }
    }

    // 7.5 Deep Space Sporadic Comet Update (偶发的彗星拖长尾)
    this.cometCooldown -= delta;
    if (this.cometCooldown <= 0) {
      this.triggerComet();
      this.cometCooldown = 25.0 + Math.random() * 20.0;
    }

    if (this.cometActive) {
      this.cometProgress += delta * 0.22; // ~4.5 seconds duration
      if (this.cometProgress >= 1.0) {
        this.cometActive = false;
        this.cometMesh.visible = false;
        if (this.cometHead) this.cometHead.visible = false;
      } else {
        const cPos = new THREE.Vector3().lerpVectors(
          this.cometStart,
          this.cometEnd,
          this.cometProgress
        );
        // Add subtle gravitational curve towards galactic center
        const toCenter = new THREE.Vector3(0, 0, 0).sub(cPos);
        const gravPull = Math.sin(this.cometProgress * Math.PI) * 2.8;
        cPos.addScaledVector(toCenter.normalize(), gravPull);

        if (this.cometHead) {
          this.cometHead.visible = true;
          this.cometHead.position.copy(cPos);
        }
        for (let i = this.cometTrailLength - 1; i > 0; i--) {
          this.cometPoints[i * 3 + 0] = this.cometPoints[(i - 1) * 3 + 0];
          this.cometPoints[i * 3 + 1] = this.cometPoints[(i - 1) * 3 + 1];
          this.cometPoints[i * 3 + 2] = this.cometPoints[(i - 1) * 3 + 2];
        }
        this.cometPoints[0] = cPos.x;
        this.cometPoints[1] = cPos.y;
        this.cometPoints[2] = cPos.z;
        this.cometMesh.geometry.attributes.position.needsUpdate = true;
      }
    }

    // 8. Update Audio engine
    cosmicAudio.update(this.params.expansion, this.params.collapse, breath);

    // 9. Update UI Status Dot
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    if (statusDot && statusText) {
      if (this.params.isHoldingFist) {
        statusDot.className = 'status-dot collapsed';
        statusText.textContent = '宇宙坍缩 (Fist)';
      } else if (this.params.chaos > 0.3) {
        statusDot.className = 'status-dot pulse';
        statusText.textContent = '近屏混沌 (Chaos)';
      } else {
        statusDot.className = 'status-dot warm';
        statusText.textContent = '星河绽放 (Bloom)';
      }
    }

    // 10. Post-processing render
    this.composer.render();
  }
}

// Instantiate application on DOM load
window.addEventListener('DOMContentLoaded', () => {
  new MiniatureGalaxyApp();
});
