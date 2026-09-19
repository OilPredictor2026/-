import os

# Complete script to build the Epic Miniature Galaxy with 5 morphing scenes,
# relativistic jets, gravitational singularity, warp speed hyperdrive,
# cinematic auto-tour, 4K wallpaper export, and 5 cosmic color themes.

epic_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>微缩银河 · Miniature Galaxy · 终极全景粒子宇宙</title>
  <meta name="description" content="包含五大深空宏观天体场景、引力黑洞透镜、曲率跃迁、电影级巡航与手势控制的终极3D微缩宇宙。">
  <link rel="stylesheet" href="./styles.css">
  <script type="importmap">
  {
    "imports": {
      "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
    }
  }
  </script>
</head>
<body>
  <!-- Three.js Canvas -->
  <canvas id="webgl-canvas"></canvas>

  <!-- Cosmic Ambient Vignette -->
  <div class="cosmic-vignette"></div>

  <!-- Cinematic Letterbox Bars (During Tour) -->
  <div id="cinema-bar-top" class="cinema-bar top"></div>
  <div id="cinema-bar-bottom" class="cinema-bar bottom"></div>

  <!-- Supernova Flash Effect -->
  <div id="supernova-overlay" class="supernova-overlay"></div>

  <!-- Warp Speed Motion Blur Lines Overlay -->
  <div id="warp-overlay" class="warp-overlay"></div>

  <!-- Floating Brand Header -->
  <header class="app-header">
    <div class="brand-title">
      <span class="sparkle-icon">✦</span> 微缩银河
      <span class="scene-badge" id="current-scene-name">螺旋银河</span>
    </div>
    <div class="brand-subtitle">MINIATURE COSMOS · 5 EPIC SCENES & RELATIVISTIC JETS</div>
  </header>

  <!-- Top Floating Cosmic Scene Switcher -->
  <nav class="scene-dock" id="scene-dock">
    <button class="scene-btn active" data-scene="0" title="经典微缩四旋臂螺旋银河 (快捷键 1)">
      <span>🌌</span> 螺旋银河
    </button>
    <button class="scene-btn" data-scene="1" title="超大质量黑洞与相对论极向喷流 (快捷键 2)">
      <span>🕳️</span> 黑洞喷流
    </button>
    <button class="scene-btn" data-scene="2" title="创生之柱恒星苗圃与璀璨星云 (快捷键 3)">
      <span>🏛️</span> 创生之柱
    </button>
    <button class="scene-btn" data-scene="3" title="双星系引力潮汐碰撞交织 (快捷键 4)">
      <span>💫</span> 星系碰撞
    </button>
    <button class="scene-btn" data-scene="4" title="霍格环形天体与量子共振波 (快捷键 5)">
      <span>🪐</span> 环形共振
    </button>
  </nav>

  <!-- Poetic Central Toast -->
  <div id="poetic-toast" class="poetic-toast">
    <div id="toast-title" class="poetic-text-primary">银河苏醒</div>
    <div id="toast-sub" class="poetic-text-secondary">你张开的不只是手掌，是银河的开关</div>
  </div>

  <!-- Wishing Star Banner (Easter Egg) -->
  <div id="wishing-star-banner" class="wishing-star-banner">
    <span>✦</span> 90秒星愿降临 · 宇宙记得你凝视过它 <span>✦</span>
  </div>

  <!-- Gravity Well Singularity Crosshair -->
  <div id="gravity-cursor" class="gravity-cursor">
    <div class="grav-ring"></div>
    <div class="grav-core"></div>
  </div>

  <!-- Webcam Mini PIP Floating Box -->
  <div id="webcam-panel" class="webcam-panel hidden">
    <div class="webcam-video-container">
      <video id="webcam-video" autoplay playsinline muted></video>
      <canvas id="webcam-canvas" width="320" height="240"></canvas>
      <span class="webcam-label">AI 掌心感知中</span>
    </div>
  </div>

  <!-- Bottom Floating Frosted Glass Dock -->
  <div class="control-dock" id="control-dock">
    <!-- Status Indicator Pill -->
    <div class="status-pill" id="status-pill">
      <div class="status-dot warm" id="status-dot"></div>
      <span id="status-text">星河绽放 (Bloom)</span>
    </div>

    <div class="dock-divider"></div>

    <!-- Time Speed Slider -->
    <div class="slider-container">
      <label for="speed-slider">流速</label>
      <input type="range" id="speed-slider" class="slender-slider" min="-2.0" max="3.0" step="0.1" value="1.0" title="时间流速 (负值可时间倒流)">
    </div>

    <div class="dock-divider"></div>

    <div class="dock-group">
      <!-- Hand State Toggle (Fist / Palm) -->
      <button id="btn-hand" class="glass-btn" title="点击或按住鼠标模拟手掌收合">
        <span>🖐️</span> 张手绽放
      </button>

      <!-- Gravitational Singularity Toggle -->
      <button id="btn-gravity" class="glass-btn" title="在鼠标处制造引力奇点吸引万星 (快捷键 G)">
        <span>🕳️</span> 引力奇点
      </button>

      <!-- Warp Hyperdrive Button -->
      <button id="btn-warp" class="glass-btn" title="曲率引擎全开 · 时空跃迁 (快捷键 Shift)">
        <span>🚀</span> 曲率跃迁
      </button>

      <!-- Supernova Detonation Button -->
      <button id="btn-supernova" class="glass-btn" title="双击掌心或按空格引发超新星爆发 (快捷键 Space)">
        <span>💥</span> 超新星
      </button>

      <!-- Cinema Tour Button -->
      <button id="btn-tour" class="glass-btn" title="开启电影运镜巡航漫游 (快捷键 C)">
        <span>🎥</span> 巡航漫游
      </button>

      <!-- Palette Theme Button -->
      <button id="btn-theme" class="glass-btn" title="切换宇宙色彩调色板 (快捷键 T)">
        <span>🎨</span> 主题配色
      </button>

      <!-- 4K Wallpaper Capture Button -->
      <button id="btn-snap" class="glass-btn" title="无UI高清壁纸截屏下载 (快捷键 P)">
        <span>📷</span> 保存壁纸
      </button>

      <!-- Webcam Hand Tracking Toggle -->
      <button id="btn-webcam" class="glass-btn" title="开启摄像头进行隔空手势追踪">
        <span>🖐️</span> 开启手势
      </button>

      <!-- Wishing Star Trigger -->
      <button id="btn-wish" class="glass-btn" title="触发90秒彗星划空彩蛋 (快捷键 W)">
        <span>⭐</span> 许愿星
      </button>

      <!-- Ambient Sound Toggle -->
      <button id="btn-sound" class="glass-btn" title="开启432Hz程序化星空天籁 (快捷键 M)">
        <span>🔇</span> 静音
      </button>

      <!-- Fullscreen Button -->
      <button id="btn-fullscreen" class="glass-btn icon-only" title="全屏沉浸 (快捷键 F)">
        ⛶
      </button>
    </div>
  </div>

  <!-- Bottom Right Keyboard Shortcuts Hint -->
  <div class="hint-badge" id="hint-badge">
    <span class="key-tag">1-5</span> 切换场景 &nbsp;|&nbsp; 
    <span class="key-tag">H</span> 隐匿界面 &nbsp;|&nbsp; 
    <span class="key-tag">C</span> 电影巡航 &nbsp;|&nbsp; 
    <span class="key-tag">G</span> 引力黑洞 &nbsp;|&nbsp; 
    <span class="key-tag">Shift</span> 曲率跃迁 &nbsp;|&nbsp; 
    <span class="key-tag">Space</span> 超新星 &nbsp;|&nbsp; 
    <span class="key-tag">T</span> 配色 &nbsp;|&nbsp; 
    <span class="key-tag">P</span> 截图
  </div>

  <!-- Complete Inlined ES Module -->
  <script type="module">
    import * as THREE from 'three';
    import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
    import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
    import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

    // -------------------------------------------------------------
    // GLSL SHADERS (With 5-Scene Morphing & Gravitational Singularity)
    // -------------------------------------------------------------
    const galaxyVertexShader = /* glsl */ `
      precision highp float;

      attribute vec3 aStartPos;
      attribute vec3 aTargetPos;
      attribute float aOrbitRadius;
      attribute float aOrbitAngle;
      attribute float aOrbitSpeed;
      attribute float aArmOffset;
      attribute float aVerticalOffset;
      attribute float aParticleSize;
      attribute float aParticleType; // 0=Core, 1=Disk, 2=Dust, 3=Jet/Filament
      attribute float aColorSeed;

      uniform float uTime;
      uniform float uTimeScale;
      uniform float uExpansion;
      uniform float uCollapse;
      uniform float uBreath;
      uniform float uChaos;
      uniform float uSupernovaTime;
      uniform float uSupernovaIntensity;
      uniform float uWarpProgress;     // 0.0 to 1.0 (Relativistic warp stretch)
      uniform float uMorphProgress;    // 0.0 to 1.0 (Scene morphing)
      uniform vec3 uGravityWell;       // Singularity 3D position
      uniform float uGravityStrength;  // Singularity mass/pull
      uniform float uPixelRatio;

      varying vec3 vColor;
      varying float vAlpha;
      varying float vParticleType;
      varying float vNormalizedRadius;
      varying float vSize;
      varying vec3 vWorldPos;

      float hash(vec3 p) {
        p = fract(p * 0.3183099 + 0.1);
        p *= 17.0;
        return fract(p.x * p.y * p.z * (p.x + p.y + p.z));
      }

      vec3 curlNoise(vec3 p) {
        float e = 0.1;
        float n1 = hash(p + vec3(e, 0.0, 0.0)) - hash(p - vec3(e, 0.0, 0.0));
        float n2 = hash(p + vec3(0.0, e, 0.0)) - hash(p - vec3(0.0, e, 0.0));
        float n3 = hash(p + vec3(0.0, 0.0, e)) - hash(p - vec3(0.0, 0.0, e));
        return normalize(vec3(n2 - n3, n3 - n1, n1 - n2) + 0.001);
      }

      void main() {
        vParticleType = aParticleType;
        float t = uTime * uTimeScale;

        // 1. Dynamic Morph between Current and Target Coordinates
        float morphT = smoothstep(0.0, 1.0, uMorphProgress);
        // Swirling stardust transit during morphing
        vec3 morphSwirl = curlNoise(mix(aStartPos, aTargetPos, morphT) * 0.4 + t * 0.5) * sin(morphT * 3.14159) * 2.8;
        vec3 basePos = mix(aStartPos, aTargetPos, morphT) + morphSwirl;

        // 2. Keplerian Orbit / Local Dynamics
        float currentAngle = aOrbitAngle + aOrbitSpeed * t;
        float rScale = mix(1.0, 0.14, uCollapse) * mix(0.5, 1.45, uExpansion) * (1.0 + uBreath * 0.08);

        // Compute local planar position
        float r = length(basePos.xz) * rScale;
        float theta = atan(basePos.z, basePos.x) + aOrbitSpeed * t * 0.6;

        vec3 pos;
        pos.x = cos(theta) * r;
        pos.z = sin(theta) * r;
        pos.y = basePos.y * mix(1.0, 0.25, uCollapse);

        // Jets spiral upwards in Scene 1 (Black Hole)
        if (aParticleType > 2.5) {
          pos.x += sin(t * 4.0 + pos.y * 0.5) * 0.25;
          pos.z += cos(t * 4.0 + pos.y * 0.5) * 0.25;
        }

        // 3. Clenched Fist Quantum Jitter
        if (uCollapse > 0.08) {
          float trembleFreq = 38.0;
          float trembleAmp = 0.035 * uCollapse * (1.0 + sin(t * trembleFreq + aColorSeed * 10.0));
          pos += (vec3(hash(pos), hash(pos + 1.0), hash(pos + 2.0)) - 0.5) * trembleAmp;
        }

        // 4. Interactive Gravitational Singularity (Black Hole on Mouse/Key)
        if (uGravityStrength > 0.01) {
          vec3 toGrav = uGravityWell - pos;
          float gravDist = length(toGrav);
          if (gravDist > 0.1) {
            float pull = uGravityStrength / (gravDist * gravDist + 1.2);
            vec3 vortex = cross(normalize(toGrav), vec3(0.0, 1.0, 0.0));
            pos += normalize(toGrav) * min(pull * 4.5, 8.0);
            pos += vortex * min(pull * 3.2, 5.0);
          }
        }

        // 5. Supernova Shockwave
        if (uSupernovaTime > 0.0 && uSupernovaTime < 4.0) {
          float waveSpeed = 16.0;
          float waveRadius = uSupernovaTime * waveSpeed;
          float particleDist = length(pos);
          float distDiff = abs(particleDist - waveRadius);
          float waveWidth = 2.2;

          if (distDiff < waveWidth * 2.5) {
            float impulse = exp(-pow(distDiff / waveWidth, 2.0)) * exp(-uSupernovaTime * 0.9) * uSupernovaIntensity;
            vec3 pushDir = normalize(pos + vec3(0.0001));
            pos += pushDir * impulse * 4.2;
            pos += curlNoise(pos * 0.8 + t * 4.0) * impulse * 2.0;
          }
        }

        // 6. Near-Screen Brownian Chaos
        if (uChaos > 0.001) {
          vec3 chaosDisplacement = curlNoise(pos * 1.2 + vec3(t * 3.5, t * 2.8, t * 3.1));
          float chaosBurst = uChaos * (3.5 + 2.0 * sin(t * 8.0 + aColorSeed * 6.28));
          pos += chaosDisplacement * chaosBurst;
        }

        // 7. Warp Speed Relativistic Streamlining
        if (uWarpProgress > 0.01) {
          pos.z += uWarpProgress * 45.0 * fract(aColorSeed + t * 0.8);
          pos.x *= (1.0 - uWarpProgress * 0.35);
          pos.y *= (1.0 - uWarpProgress * 0.35);
        }

        vWorldPos = pos;

        vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
        gl_Position = projectionMatrix * mvPosition;

        float dist = -mvPosition.z;
        float sizeScale = mix(0.75, 1.4, uExpansion) * mix(1.0, 0.75, uCollapse);
        float pointSize = aParticleSize * sizeScale * (38.0 / max(dist, 0.5)) * uPixelRatio;

        if (aParticleType > 2.5) pointSize *= 1.35;
        if (uWarpProgress > 0.01) pointSize *= (1.0 + uWarpProgress * 2.0);

        gl_PointSize = clamp(pointSize, 1.2, 85.0);
        vSize = gl_PointSize;

        vNormalizedRadius = clamp(length(pos.xz) / 13.5, 0.0, 1.0);

        vColor = vec3(
          fract(aColorSeed * 12.9898),
          fract(aColorSeed * 78.233),
          fract(aColorSeed * 45.164)
        );

        float baseAlpha = 0.70;
        if (aParticleType > 1.5 && aParticleType < 2.5) baseAlpha = 0.20;
        else if (aParticleType < 0.5) baseAlpha = 0.45;
        vAlpha = baseAlpha;
      }
    `;

    const galaxyFragmentShader = /* glsl */ `
      precision highp float;

      uniform float uTime;
      uniform float uExpansion;
      uniform float uCollapse;
      uniform float uBrightness;
      uniform float uSupernovaTime;
      uniform int uTheme; // 0=Gold/Violet, 1=Ice/Cyan, 2=Emerald/Teal, 3=Solar/Amber, 4=Neon/Cyber

      varying vec3 vColor;
      varying float vAlpha;
      varying float vParticleType;
      varying float vNormalizedRadius;
      varying float vSize;
      varying vec3 vWorldPos;

      void main() {
        vec2 coord = gl_PointCoord - vec2(0.5);
        float dist = length(coord);

        if (dist > 0.5) discard;

        float coreGlow = exp(-dist * 18.0);
        float softGlow = exp(-dist * 5.2);

        // Star spikes with high dynamic contrast
        float spikeWeight = smoothstep(10.0, 36.0, vSize);
        float spikeX = exp(-abs(coord.x) * 65.0) * exp(-abs(coord.y) * 5.0);
        float spikeY = exp(-abs(coord.y) * 65.0) * exp(-abs(coord.x) * 5.0);
        float crossSpike = (spikeX + spikeY) * spikeWeight * 1.5;

        // Diagonal Spikes
        float d1 = abs(coord.x + coord.y) * 0.7071;
        float d2 = abs(coord.x - coord.y) * 0.7071;
        float diagSpike = (exp(-d1 * 80.0) * exp(-d2 * 8.0) + exp(-d2 * 80.0) * exp(-d1 * 8.0)) * spikeWeight * 0.5;

        // Prism Chromatic Dispersion
        float dispersionShift = 0.045 * spikeWeight;
        vec3 spectralIntensity = vec3(
          exp(-length(coord * (1.0 - dispersionShift)) * 8.5),
          exp(-length(coord) * 8.5),
          exp(-length(coord * (1.0 + dispersionShift)) * 8.5)
        );

        // 5 Cosmic Color Palettes
        vec3 colCore, colMid, colOuter, colAccent;

        if (uTheme == 1) {
          // Glacial Ice Blue & Diamond Silver
          colCore = vec3(0.85, 0.95, 1.0);
          colMid = vec3(0.40, 0.75, 0.95);
          colOuter = vec3(0.15, 0.35, 0.75);
          colAccent = vec3(0.70, 0.90, 1.0);
        } else if (uTheme == 2) {
          // Emerald Star Nursery & Pillars of Creation Teal
          colCore = vec3(0.92, 1.0, 0.85);
          colMid = vec3(0.25, 0.85, 0.65);
          colOuter = vec3(0.08, 0.45, 0.55);
          colAccent = vec3(0.95, 0.75, 0.35);
        } else if (uTheme == 3) {
          // Solar Corona & Black Hole Flaring Plasma
          colCore = vec3(1.0, 0.95, 0.75);
          colMid = vec3(1.0, 0.45, 0.15);
          colOuter = vec3(0.65, 0.10, 0.12);
          colAccent = vec3(1.0, 0.75, 0.25);
        } else if (uTheme == 4) {
          // Cyber Space Neon Violet & Electric Cyan
          colCore = vec3(0.75, 1.0, 1.0);
          colMid = vec3(0.95, 0.25, 0.85);
          colOuter = vec3(0.25, 0.05, 0.85);
          colAccent = vec3(0.20, 0.85, 1.0);
        } else {
          // Default: Celestial Gold & Rose Violet
          vec3 colCoreCold = vec3(0.68, 0.88, 1.0);
          vec3 colCoreWarm = vec3(1.0, 0.88, 0.55);
          colCore = mix(colCoreCold, colCoreWarm, clamp(uExpansion, 0.0, 1.0));

          vec3 colMidCold = vec3(0.30, 0.48, 0.82);
          vec3 colMidWarm = vec3(1.0, 0.58, 0.28);
          colMid = mix(colMidCold, colMidWarm, clamp(uExpansion, 0.0, 1.0));

          vec3 colOuterCold = vec3(0.18, 0.24, 0.62);
          vec3 colOuterWarm = vec3(0.58, 0.12, 0.88);
          colOuter = mix(colOuterCold, colOuterWarm, clamp(uExpansion, 0.0, 1.0));
          colAccent = vec3(1.0, 0.45, 0.68);
        }

        vec3 starColor;
        if (vNormalizedRadius < 0.20) {
          starColor = mix(colCore, colMid, vNormalizedRadius / 0.20);
        } else {
          float tOuter = (vNormalizedRadius - 0.20) / 0.80;
          starColor = mix(colMid, colOuter, tOuter);
        }

        if (vParticleType > 2.5) {
          // Relativistic Jet / Filaments have high-energy accent
          starColor = mix(starColor, colAccent, 0.65);
        }

        // Star hue micro-variation
        starColor += (vColor - 0.5) * 0.07;

        // Burning Edge interface
        float edgeCenter = 0.24;
        float edgeWidth = 0.06;
        float burningEdge = exp(-pow((vNormalizedRadius - edgeCenter) / edgeWidth, 2.0));
        vec3 burningColor = vec3(1.0, 0.38, 0.12) * (1.0 + 0.3 * sin(uTime * 3.5 + vNormalizedRadius * 20.0));
        starColor += burningColor * burningEdge * 0.70 * mix(0.3, 1.1, uExpansion);

        // Supernova flash
        if (uSupernovaTime > 0.0 && uSupernovaTime < 2.5) {
          float flash = exp(-uSupernovaTime * 2.2);
          starColor = mix(starColor, vec3(1.0, 0.98, 0.95), flash * 0.7);
        }

        // Physical luminosity scaling
        float scaleLuminance = mix(0.25, 1.45, pow(clamp(uExpansion, 0.0, 1.5), 1.2));
        scaleLuminance *= mix(1.0, 0.18, uCollapse);

        // Core density damping to avoid additive blowout at galactic nucleus
        float coreDensityDamp = mix(0.04, 0.45, smoothstep(0.01, 0.32, vNormalizedRadius));

        float shape = coreGlow * 0.75 + softGlow * 0.28 + crossSpike + diagSpike;
        vec3 finalColor = starColor * spectralIntensity * shape * scaleLuminance * uBrightness * coreDensityDamp;

        float alpha = clamp(shape * vAlpha, 0.0, 1.0);
        gl_FragColor = vec4(finalColor, alpha);
      }
    `;

    const coreGlowVertexShader = /* glsl */ `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

    const coreGlowFragmentShader = /* glsl */ `
      precision highp float;

      uniform float uTime;
      uniform float uBreath;
      uniform float uExpansion;
      uniform float uCollapse;
      uniform float uSupernovaTime;

      varying vec2 vUv;

      void main() {
        vec2 p = vUv - vec2(0.5);
        float d = length(p) * 2.0;
        if (d > 1.0) discard;

        float pulse = 1.0 + uBreath * 0.25 + 0.08 * sin(uTime * 6.0);
        float innerCore = exp(-d * 5.2 * pulse);
        float outerHalo = exp(-d * 2.4 * pulse);
        float rim = pow(1.0 - d, 2.5);

        vec3 coldColor = vec3(0.60, 0.85, 1.0);
        vec3 warmColor = vec3(1.0, 0.85, 0.50);
        vec3 roseHalo = vec3(1.0, 0.40, 0.65);

        vec3 baseCol = mix(coldColor, warmColor, clamp(uExpansion, 0.0, 1.0));
        vec3 coreColor = mix(baseCol, roseHalo, outerHalo * 0.35);

        if (uSupernovaTime > 0.0 && uSupernovaTime < 3.0) {
          float flash = exp(-uSupernovaTime * 2.5);
          coreColor = mix(coreColor, vec3(1.0, 0.98, 0.92), flash * 0.9);
        }

        float brightness = mix(0.18, 1.35, uExpansion) * mix(1.0, 0.25, uCollapse);
        float alpha = (innerCore * 0.35 + outerHalo * 0.12 + rim * 0.04) * brightness;

        gl_FragColor = vec4(coreColor * (innerCore * 0.65 + outerHalo * 0.25) * brightness, alpha);
      }
    `;

    const bokehVertexShader = /* glsl */ `
      precision highp float;
      attribute float aSize;
      attribute vec3 aColor;
      uniform float uTime;
      uniform float uPixelRatio;
      varying vec3 vColor;
      varying float vDist;

      void main() {
        vColor = aColor;
        vec3 pos = position;
        pos.x += sin(uTime * 0.15 + position.z) * 0.25;
        pos.y += cos(uTime * 0.18 + position.x) * 0.20;
        pos.z += sin(uTime * 0.12 + position.y) * 0.25;

        vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
        gl_Position = projectionMatrix * mvPosition;

        vDist = -mvPosition.z;
        float bokehSize = aSize * (100.0 / max(vDist, 0.2)) * uPixelRatio;
        gl_PointSize = clamp(bokehSize, 6.0, 75.0);
      }
    `;

    const bokehFragmentShader = /* glsl */ `
      precision highp float;
      varying vec3 vColor;
      varying float vDist;

      void main() {
        vec2 coord = gl_PointCoord - vec2(0.5);
        float r = length(coord);
        if (r > 0.5) discard;

        float ring = smoothstep(0.38, 0.48, r) * (1.0 - smoothstep(0.48, 0.5, r));
        float softFill = smoothstep(0.5, 0.0, r);
        float bokehDisc = softFill * 0.35 + ring * 0.65;

        float rR = length(coord * 0.96);
        float rG = length(coord);
        float rB = length(coord * 1.04);

        vec3 chromatic = vec3(
          smoothstep(0.5, 0.0, rR) * 0.8 + 0.2,
          smoothstep(0.5, 0.0, rG) * 0.7 + 0.3,
          smoothstep(0.5, 0.0, rB) * 0.9 + 0.1
        );

        gl_FragColor = vec4(vColor * chromatic * bokehDisc * 0.85, bokehDisc * 0.08);
      }
    `;

    // -------------------------------------------------------------
    // PROCEDURAL CELESTIAL SOUND ENGINE
    // -------------------------------------------------------------
    class CosmicSoundEngine {
      constructor() {
        this.ctx = null;
        this.isMuted = true;
        this.masterGain = null;
        this.droneFilter = null;
        this.oscillators = [];
        this.isInitialized = false;
      }

      init() {
        if (this.isInitialized) return;
        try {
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          this.ctx = new AudioContext();
          this.masterGain = this.ctx.createGain();
          this.masterGain.gain.setValueAtTime(0, this.ctx.currentTime);
          this.masterGain.connect(this.ctx.destination);

          this.droneFilter = this.ctx.createBiquadFilter();
          this.droneFilter.type = 'lowpass';
          this.droneFilter.frequency.setValueAtTime(450, this.ctx.currentTime);
          this.droneFilter.Q.setValueAtTime(3.0, this.ctx.currentTime);
          this.droneFilter.connect(this.masterGain);

          const baseFreqs = [54.0, 81.0, 108.0, 162.0, 216.0];
          baseFreqs.forEach((freq, idx) => {
            const osc = this.ctx.createOscillator();
            osc.type = idx === 0 ? 'sine' : 'triangle';
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

            const oscGain = this.ctx.createGain();
            oscGain.gain.setValueAtTime(0.10 / (idx + 1), this.ctx.currentTime);

            const lfo = this.ctx.createOscillator();
            lfo.frequency.setValueAtTime(0.08 + idx * 0.03, this.ctx.currentTime);
            const lfoGain = this.ctx.createGain();
            lfoGain.gain.setValueAtTime(1.5, this.ctx.currentTime);
            lfo.connect(lfoGain);
            lfoGain.connect(osc.frequency);
            lfo.start();

            osc.connect(oscGain);
            oscGain.connect(this.droneFilter);
            osc.start();
            this.oscillators.push(osc);
          });
          this.isInitialized = true;
        } catch (err) {
          console.warn('AudioContext error:', err);
        }
      }

      toggleSound() {
        if (!this.isInitialized) this.init();
        if (!this.ctx) return false;
        if (this.ctx.state === 'suspended') this.ctx.resume();
        this.isMuted = !this.isMuted;
        this.masterGain.gain.setTargetAtTime(this.isMuted ? 0 : 0.4, this.ctx.currentTime, 0.2);
        return !this.isMuted;
      }

      update(expansion, collapse, breath, warp) {
        if (!this.isInitialized || this.isMuted) return;
        const now = this.ctx.currentTime;
        const cutoff = (300 + expansion * 600) * (1.0 - collapse * 0.7) + breath * 150 + (warp || 0) * 1200;
        this.droneFilter.frequency.setTargetAtTime(Math.max(60, cutoff), now, 0.1);
      }

      playSupernova() {
        if (!this.isInitialized || this.isMuted) return;
        const now = this.ctx.currentTime;
        const subOsc = this.ctx.createOscillator();
        subOsc.type = 'sine';
        subOsc.frequency.setValueAtTime(120, now);
        subOsc.frequency.exponentialRampToValueAtTime(32, now + 1.8);
        const subGain = this.ctx.createGain();
        subGain.gain.setValueAtTime(0.6, now);
        subGain.gain.exponentialRampToValueAtTime(0.001, now + 2.5);
        subOsc.connect(subGain);
        subGain.connect(this.masterGain);
        subOsc.start(now);
        subOsc.stop(now + 2.6);

        for (let i = 0; i < 4; i++) {
          const chime = this.ctx.createOscillator();
          chime.type = 'sine';
          chime.frequency.setValueAtTime(864 * (i + 1) * 0.75, now);
          chime.frequency.exponentialRampToValueAtTime(432 * (i + 1), now + 3.0);
          const chimeGain = this.ctx.createGain();
          chimeGain.gain.setValueAtTime(0.07 / (i + 1), now);
          chimeGain.gain.exponentialRampToValueAtTime(0.0001, now + 3.2);
          chime.connect(chimeGain);
          chimeGain.connect(this.masterGain);
          chime.start(now + i * 0.05);
          chime.stop(now + 3.3);
        }
      }

      playWishingStar() {
        if (!this.isInitialized || this.isMuted) return;
        const now = this.ctx.currentTime;
        const bell = this.ctx.createOscillator();
        bell.type = 'triangle';
        bell.frequency.setValueAtTime(1296, now);
        bell.frequency.exponentialRampToValueAtTime(1728, now + 1.5);
        bell.frequency.exponentialRampToValueAtTime(864, now + 3.5);
        const bellGain = this.ctx.createGain();
        bellGain.gain.setValueAtTime(0.001, now);
        bellGain.gain.linearRampToValueAtTime(0.18, now + 0.8);
        bellGain.exponentialRampToValueAtTime(0.0001, now + 3.8);
        bell.connect(bellGain);
        bellGain.connect(this.masterGain);
        bell.start(now);
        bell.stop(now + 4.0);
      }

      playWarpSound() {
        if (!this.isInitialized || this.isMuted) return;
        const now = this.ctx.currentTime;
        const sweep = this.ctx.createOscillator();
        sweep.type = 'sawtooth';
        sweep.frequency.setValueAtTime(80, now);
        sweep.frequency.exponentialRampToValueAtTime(1200, now + 2.0);
        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0.01, now);
        gain.gain.linearRampToValueAtTime(0.22, now + 0.8);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 2.5);
        sweep.connect(gain);
        gain.connect(this.masterGain);
        sweep.start(now);
        sweep.stop(now + 2.6);
      }
    }

    const cosmicAudio = new CosmicSoundEngine();

    // -------------------------------------------------------------
    // MAIN MINIATURE GALAXY APPLICATION (EPIC VERSION)
    // -------------------------------------------------------------
    class MiniatureGalaxyApp {
      constructor() {
        this.canvas = document.getElementById('webgl-canvas');
        this.width = window.innerWidth;
        this.height = window.innerHeight;

        this.params = {
          particleCount: 100000,
          timeScale: 1.0,
          expansion: 1.0,
          collapse: 0.0,
          brightness: 1.15,
          chaos: 0.0,
          cameraDistance: 16.5,
          targetCameraDistance: 16.5,
          currentScene: 0,
          themeIndex: 0,
          isHoldingFist: false,
          isWebcamActive: false,
          isGravityActive: false,
          gravityStrength: 0.0,
          isWarping: false,
          warpProgress: 0.0,
          isCinematicTour: false,
          tourTime: 0.0,
          wishingStarCountdown: 90.0,
        };

        this.targetRotation = { x: 0.52, y: 0.0 };
        this.currentRotation = { x: 0.52, y: 0.0 };
        this.mouse = { x: 0, y: 0, isDown: false, lastDownTime: 0 };
        this.gravityWellPos = new THREE.Vector3(0, 0, 0);
        this.supernovaState = { time: -1.0, intensity: 0.0 };
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

        this.animate = this.animate.bind(this);
        requestAnimationFrame(this.animate);
      }

      initThree() {
        this.scene = new THREE.Scene();
        this.scene.fog = new THREE.FogExp2(0x020208, 0.012);

        this.camera = new THREE.PerspectiveCamera(55, this.width / this.height, 0.1, 1000);
        this.camera.position.set(0, 8.0, this.params.cameraDistance);
        this.camera.lookAt(0, 0, 0);

        this.renderer = new THREE.WebGLRenderer({
          canvas: this.canvas,
          antialias: true,
          alpha: false,
          powerPreference: 'high-performance',
          preserveDrawingBuffer: true // Required for 4K Wallpaper Capture
        });
        this.renderer.setSize(this.width, this.height);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 0.98;

        this.galaxyGroup = new THREE.Group();
        this.scene.add(this.galaxyGroup);
      }

      setupPostProcessing() {
        this.composer = new EffectComposer(this.renderer);
        const renderPass = new RenderPass(this.scene, this.camera);
        this.composer.addPass(renderPass);

        this.bloomPass = new UnrealBloomPass(
          new THREE.Vector2(this.width, this.height),
          0.32, // strength
          0.22, // radius
          0.85  // threshold
        );
        this.composer.addPass(this.bloomPass);
      }

      createVolumetricCore() {
        const coreGeo = new THREE.PlaneGeometry(2.0, 2.0);
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

        this.coreMesh1 = new THREE.Mesh(coreGeo, this.coreMaterial);
        this.coreMesh2 = new THREE.Mesh(coreGeo, this.coreMaterial);
        this.coreMesh2.rotation.y = Math.PI * 0.5;

        this.coreMesh3 = new THREE.Mesh(coreGeo, this.coreMaterial);
        this.coreMesh3.rotation.x = Math.PI * 0.5;

        this.galaxyGroup.add(this.coreMesh1);
        this.galaxyGroup.add(this.coreMesh2);
        this.galaxyGroup.add(this.coreMesh3);
      }

      /**
       * Generate 5 Unique Cosmic Coordinate Configurations:
       * 0: Classic Spiral Galaxy (4-arm logarithmic disk)
       * 1: Supermassive Black Hole & Dual Polar Jets
       * 2: Pillars of Creation (3 interstellar gas columns)
       * 3: Galactic Collision (2 colliding galaxies with tidal tails)
       * 4: Hoag's Ring Galaxy & Cosmic Cymatics
       */
      generateSceneCoordinates(sceneIndex) {
        const count = this.params.particleCount;
        const coords = new Float32Array(count * 3);
        const randGaussian = (mean = 0, stdev = 1) => {
          let u = 1 - Math.random();
          let v = Math.random();
          let z = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
          return z * stdev + mean;
        };

        if (sceneIndex === 0) {
          // Scene 0: Classic 4-Arm Spiral
          const numArms = 4;
          for (let i = 0; i < count; i++) {
            let x, y, z;
            if (i < count * 0.18) {
              const r = Math.pow(Math.random(), 2.0) * 1.9 + 0.08;
              const angle = Math.random() * Math.PI * 2;
              x = Math.cos(angle) * r;
              z = Math.sin(angle) * r;
              y = randGaussian(0, 0.3) * (1.0 - r / 2.2);
            } else if (i < count * 0.70) {
              const armIndex = i % numArms;
              const armBaseAngle = armIndex * (Math.PI * 2 / numArms);
              const r = 1.3 + Math.pow(Math.random(), 1.15) * 11.2;
              const theta = armBaseAngle + 2.4 * Math.log(r / 1.3 + 1.0) + randGaussian(0, 0.12);
              x = Math.cos(theta) * r;
              z = Math.sin(theta) * r;
              y = randGaussian(0, 0.45) * (0.1 + r * 0.055);
            } else if (i < count * 0.80) {
              const r = 1.8 + Math.random() * 9.5;
              const theta = (i % 2) * Math.PI + 2.5 * Math.log(r / 1.4 + 1.0);
              x = Math.cos(theta) * r;
              z = Math.sin(theta) * r;
              y = randGaussian(0, 0.18) * 0.08;
            } else {
              const r = 1.5 + Math.pow(Math.random(), 0.9) * 20.0;
              const angle = Math.random() * Math.PI * 2;
              x = Math.cos(angle) * r + randGaussian(0, 0.8);
              z = Math.sin(angle) * r + randGaussian(0, 0.8);
              y = randGaussian(0, 2.2);
            }
            coords[i * 3 + 0] = x;
            coords[i * 3 + 1] = y;
            coords[i * 3 + 2] = z;
          }
        } else if (sceneIndex === 1) {
          // Scene 1: Black Hole & Relativistic Polar Jets
          for (let i = 0; i < count; i++) {
            let x, y, z;
            if (i < count * 0.22) {
              // Dual relativistic jets along Y axis (+Y and -Y)
              const jetDir = (i % 2 === 0) ? 1.0 : -1.0;
              const height = 1.5 + Math.pow(Math.random(), 1.2) * 16.0;
              const funnelRadius = (0.2 + height * 0.08) * (0.8 + Math.random() * 0.4);
              const angle = height * 3.5 + Math.random() * 0.5;
              x = Math.cos(angle) * funnelRadius;
              z = Math.sin(angle) * funnelRadius;
              y = jetDir * height;
            } else if (i < count * 0.75) {
              // Rapid ultra-thin accretion disk
              const r = 1.6 + Math.pow(Math.random(), 1.5) * 8.5;
              const angle = Math.random() * Math.PI * 2;
              x = Math.cos(angle) * r;
              z = Math.sin(angle) * r;
              y = randGaussian(0, 0.08) * (0.1 + r * 0.04);
            } else {
              // Event horizon outer halo
              const r = 10.0 + Math.random() * 12.0;
              const angle = Math.random() * Math.PI * 2;
              x = Math.cos(angle) * r;
              z = Math.sin(angle) * r;
              y = randGaussian(0, 1.5);
            }
            coords[i * 3 + 0] = x;
            coords[i * 3 + 1] = y;
            coords[i * 3 + 2] = z;
          }
        } else if (sceneIndex === 2) {
          // Scene 2: Pillars of Creation (3 Tall Interstellar Gas Columns)
          const pillars = [
            { x: -3.0, z: 0.0, hMin: -6.0, hMax: 9.0, radius: 1.8 },
            { x: 0.5, z: 1.2, hMin: -5.0, hMax: 5.5, radius: 1.5 },
            { x: 3.5, z: -1.0, hMin: -4.0, hMax: 2.8, radius: 1.3 }
          ];
          for (let i = 0; i < count; i++) {
            let x, y, z;
            if (i < count * 0.75) {
              const p = pillars[i % 3];
              const hRatio = Math.random();
              y = p.hMin + (p.hMax - p.hMin) * hRatio;
              const r = p.radius * (1.0 - hRatio * 0.45) * Math.sqrt(Math.random());
              const angle = Math.random() * Math.PI * 2;
              // Finger-like protrusions
              const bump = Math.sin(y * 1.5) * 0.4;
              x = p.x + Math.cos(angle) * (r + bump);
              z = p.z + Math.sin(angle) * (r + bump);
            } else {
              // Surrounding starburst nursery
              x = randGaussian(0, 9.0);
              y = randGaussian(0, 7.0);
              z = randGaussian(0, 8.0);
            }
            coords[i * 3 + 0] = x;
            coords[i * 3 + 1] = y;
            coords[i * 3 + 2] = z;
          }
        } else if (sceneIndex === 3) {
          // Scene 3: Galactic Collision (2 Merging Galaxies with Tidal Tails)
          for (let i = 0; i < count; i++) {
            let x, y, z;
            const isGalaxyA = (i % 2 === 0);
            const center = isGalaxyA ? new THREE.Vector3(-4.5, 1.2, -1.5) : new THREE.Vector3(4.5, -1.2, 1.5);
            const rotAngle = isGalaxyA ? 0.65 : -0.75;

            const r = 0.5 + Math.pow(Math.random(), 1.2) * 7.5;
            const angle = Math.random() * Math.PI * 2 + (r * 0.8);
            let lx = Math.cos(angle) * r;
            let lz = Math.sin(angle) * r;
            let ly = randGaussian(0, 0.25);

            // Tidal stretching towards each other
            if (r > 3.0) {
              const stretch = (r - 3.0) * 0.45;
              if (isGalaxyA) { lx += stretch; ly -= stretch * 0.3; }
              else { lx -= stretch; ly += stretch * 0.3; }
            }

            // Tilt in 3D
            x = center.x + lx * Math.cos(rotAngle) - ly * Math.sin(rotAngle);
            y = center.y + lx * Math.sin(rotAngle) + ly * Math.cos(rotAngle);
            z = center.z + lz;

            coords[i * 3 + 0] = x;
            coords[i * 3 + 1] = y;
            coords[i * 3 + 2] = z;
          }
        } else if (sceneIndex === 4) {
          // Scene 4: Hoag's Ring Galaxy & Cosmic Cymatics
          for (let i = 0; i < count; i++) {
            let x, y, z;
            if (i < count * 0.20) {
              // Isolated bright spherical core
              const r = Math.pow(Math.random(), 1.5) * 1.5 + 0.05;
              const theta = Math.random() * Math.PI * 2;
              const phi = (Math.random() - 0.5) * Math.PI;
              x = r * Math.cos(phi) * Math.cos(theta);
              y = r * Math.sin(phi);
              z = r * Math.cos(phi) * Math.sin(theta);
            } else if (i < count * 0.85) {
              // Huge detached circular ring
              const r = 5.5 + Math.pow(Math.random(), 1.0) * 4.2;
              const angle = Math.random() * Math.PI * 2;
              x = Math.cos(angle) * r;
              z = Math.sin(angle) * r;
              // Vertical harmonic standing waves (Cymatics)
              y = Math.sin(angle * 6.0) * 0.65 + randGaussian(0, 0.18);
            } else {
              // Deep space ambient dust
              const r = 1.0 + Math.random() * 18.0;
              const angle = Math.random() * Math.PI * 2;
              x = Math.cos(angle) * r;
              z = Math.sin(angle) * r;
              y = randGaussian(0, 2.0);
            }
            coords[i * 3 + 0] = x;
            coords[i * 3 + 1] = y;
            coords[i * 3 + 2] = z;
          }
        }
        return coords;
      }

      createGalaxyParticles() {
        const count = this.params.particleCount;
        this.galaxyGeometry = new THREE.BufferGeometry();

        const initialCoords = this.generateSceneCoordinates(0);
        this.currentCoords = new Float32Array(initialCoords);

        const aOrbitRadius = new Float32Array(count);
        const aOrbitAngle = new Float32Array(count);
        const aOrbitSpeed = new Float32Array(count);
        const aArmOffset = new Float32Array(count);
        const aVerticalOffset = new Float32Array(count);
        const aParticleSize = new Float32Array(count);
        const aParticleType = new Float32Array(count);
        const aColorSeed = new Float32Array(count);

        for (let i = 0; i < count; i++) {
          const r = Math.sqrt(initialCoords[i * 3] ** 2 + initialCoords[i * 3 + 2] ** 2);
          aOrbitRadius[i] = r;
          aOrbitAngle[i] = Math.atan2(initialCoords[i * 3 + 2], initialCoords[i * 3]);
          aOrbitSpeed[i] = (1.45 / Math.sqrt(r + 0.25)) * (0.85 + Math.random() * 0.3);
          aArmOffset[i] = (Math.random() - 0.5) * 0.1;
          aVerticalOffset[i] = initialCoords[i * 3 + 1];
          aParticleSize[i] = Math.pow(Math.random(), 3.5) * 8.5 + 1.4;

          if (i < count * 0.18) aParticleType[i] = 0.0;
          else if (i < count * 0.70) aParticleType[i] = 1.0;
          else if (i < count * 0.80) aParticleType[i] = 3.0; // Jet / Filament
          else aParticleType[i] = 2.0;

          aColorSeed[i] = Math.random();
        }

        this.galaxyGeometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(initialCoords), 3));
        this.galaxyGeometry.setAttribute('aStartPos', new THREE.BufferAttribute(new Float32Array(initialCoords), 3));
        this.galaxyGeometry.setAttribute('aTargetPos', new THREE.BufferAttribute(new Float32Array(initialCoords), 3));

        this.galaxyGeometry.setAttribute('aOrbitRadius', new THREE.BufferAttribute(aOrbitRadius, 1));
        this.galaxyGeometry.setAttribute('aOrbitAngle', new THREE.BufferAttribute(aOrbitAngle, 1));
        this.galaxyGeometry.setAttribute('aOrbitSpeed', new THREE.BufferAttribute(aOrbitSpeed, 1));
        this.galaxyGeometry.setAttribute('aArmOffset', new THREE.BufferAttribute(aArmOffset, 1));
        this.galaxyGeometry.setAttribute('aVerticalOffset', new THREE.BufferAttribute(aVerticalOffset, 1));
        this.galaxyGeometry.setAttribute('aParticleSize', new THREE.BufferAttribute(aParticleSize, 1));
        this.galaxyGeometry.setAttribute('aParticleType', new THREE.BufferAttribute(aParticleType, 1));
        this.galaxyGeometry.setAttribute('aColorSeed', new THREE.BufferAttribute(aColorSeed, 1));

        this.galaxyUniforms = {
          uTime: { value: 0 },
          uTimeScale: { value: 1.0 },
          uExpansion: { value: 1.0 },
          uCollapse: { value: 0.0 },
          uBreath: { value: 0 },
          uChaos: { value: 0.0 },
          uSupernovaTime: { value: -1.0 },
          uSupernovaIntensity: { value: 0.0 },
          uWarpProgress: { value: 0.0 },
          uMorphProgress: { value: 1.0 },
          uGravityWell: { value: new THREE.Vector3(0, 0, 0) },
          uGravityStrength: { value: 0.0 },
          uTheme: { value: 0 },
          uPixelRatio: { value: Math.min(window.devicePixelRatio, 2) },
          uBrightness: { value: 1.15 }
        };

        this.galaxyMaterial = new THREE.ShaderMaterial({
          vertexShader: galaxyVertexShader,
          fragmentShader: galaxyFragmentShader,
          uniforms: this.galaxyUniforms,
          transparent: true,
          blending: THREE.AdditiveBlending,
          depthWrite: false
        });

        this.galaxyPoints = new THREE.Points(this.galaxyGeometry, this.galaxyMaterial);
        this.galaxyPoints.frustumCulled = false;
        this.galaxyGroup.add(this.galaxyPoints);
      }

      /**
       * Switch Cosmic Scene with smooth GPU Stardust Morphing
       */
      switchScene(sceneIndex) {
        if (sceneIndex === this.params.currentScene) return;

        const sceneNames = ['螺旋银河', '黑洞喷流', '创生之柱', '星系碰撞', '环形共振'];
        const sceneDescriptions = [
          '四重对数旋臂舒展，炽热黄金星核与玫瑰星紫流转',
          '超大质量黑洞视界吞噬光芒，极向相对论喷流直冲深空',
          '三座数光年高的星际气体之柱巍然耸立，恒星在星云深处诞生',
          '两座巨型星系相撞撕扯，引力潮汐长尾跨越亿万光年',
          '霍格天体式光环星系，量子驻波共振如宇宙金刚曼陀罗'
        ];

        this.params.currentScene = sceneIndex;

        // Update badge and title
        const badge = document.getElementById('current-scene-name');
        if (badge) badge.textContent = sceneNames[sceneIndex];

        // Update scene dock buttons
        document.querySelectorAll('.scene-btn').forEach((btn, idx) => {
          btn.classList.toggle('active', idx === sceneIndex);
        });

        // Compute destination coordinates
        const newCoords = this.generateSceneCoordinates(sceneIndex);

        // Update GPU Morph buffers
        const startAttr = this.galaxyGeometry.attributes.aStartPos;
        const targetAttr = this.galaxyGeometry.attributes.aTargetPos;

        // Copy current target to start, and newCoords to target
        startAttr.array.set(targetAttr.array);
        targetAttr.array.set(newCoords);

        startAttr.needsUpdate = true;
        targetAttr.needsUpdate = true;

        // Animate morph progress from 0.0 to 1.0
        this.morphStartTime = performance.now();
        this.isMorphing = true;

        // Adjust Volumetric Core visibility depending on scene
        if (sceneIndex === 1) {
          // Black Hole: Black sphere center + relativistic photon ring
          this.coreMaterial.uniforms.uExpansion.value = 0.2;
        } else if (sceneIndex === 2) {
          this.coreMaterial.uniforms.uExpansion.value = 0.5;
        } else {
          this.coreMaterial.uniforms.uExpansion.value = 1.0;
        }

        this.showPoeticToast(sceneNames[sceneIndex], sceneDescriptions[sceneIndex]);
      }

      cycleTheme() {
        const themeNames = ['鎏金紫罗兰', '极境冰蓝', '创生翡翠', '熔火日冕', '深空赛博'];
        this.params.themeIndex = (this.params.themeIndex + 1) % 5;
        this.galaxyUniforms.uTheme.value = this.params.themeIndex;
        this.showPoeticToast('色彩主题切换', themeNames[this.params.themeIndex]);
      }

      createBokehDust() {
        const bokehCount = 70;
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
          positions[i * 3 + 0] = (Math.random() - 0.5) * 22.0;
          positions[i * 3 + 1] = (Math.random() - 0.5) * 15.0;
          positions[i * 3 + 2] = (Math.random() - 0.5) * 18.0 + 4.0;
          aSize[i] = Math.pow(Math.random(), 2.0) * 22.0 + 8.0;

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
        this.bokehPoints.frustumCulled = false;
        this.scene.add(this.bokehPoints);
      }

      createBinaryStars() {
        this.binaryGroup = new THREE.Group();
        const starGeo = new THREE.SphereGeometry(0.12, 16, 16);
        const mat1 = new THREE.MeshBasicMaterial({ color: 0xffe066 });
        const mat2 = new THREE.MeshBasicMaterial({ color: 0x70d6ff });

        this.twinStar1 = new THREE.Mesh(starGeo, mat1);
        this.twinStar2 = new THREE.Mesh(starGeo, mat2);

        this.binaryGroup.add(this.twinStar1);
        this.binaryGroup.add(this.twinStar2);

        this.trailLength = 80;
        this.trailPositions1 = new Float32Array(this.trailLength * 3);
        this.trailPositions2 = new Float32Array(this.trailLength * 3);

        const trailGeo1 = new THREE.BufferGeometry();
        trailGeo1.setAttribute('position', new THREE.BufferAttribute(this.trailPositions1, 3));
        this.binaryTrail1 = new THREE.Line(trailGeo1, new THREE.LineBasicMaterial({
          color: 0xffe066,
          transparent: true,
          opacity: 0.75,
          blending: THREE.AdditiveBlending
        }));

        const trailGeo2 = new THREE.BufferGeometry();
        trailGeo2.setAttribute('position', new THREE.BufferAttribute(this.trailPositions2, 3));
        this.binaryTrail2 = new THREE.Line(trailGeo2, new THREE.LineBasicMaterial({
          color: 0x70d6ff,
          transparent: true,
          opacity: 0.75,
          blending: THREE.AdditiveBlending
        }));

        this.binaryGroup.add(this.binaryTrail1);
        this.binaryGroup.add(this.binaryTrail2);
        this.galaxyGroup.add(this.binaryGroup);
      }

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

        this.wishingStarHead = new THREE.Mesh(
          new THREE.SphereGeometry(0.24, 16, 16),
          new THREE.MeshBasicMaterial({ color: 0xffffff, blending: THREE.AdditiveBlending })
        );
        this.wishingStarHead.visible = false;
        this.scene.add(this.wishingStarHead);
      }

      triggerWishingStar() {
        if (this.wishingStarActive) return;
        this.wishingStarActive = true;
        this.wishingStarProgress = 0;
        this.wishingStarMesh.visible = true;

        this.starStart = new THREE.Vector3(-25, 12, (Math.random() - 0.5) * 8 - 4);
        this.starEnd = new THREE.Vector3(25, -6, (Math.random() - 0.5) * 8 + 6);

        for (let i = 0; i < this.wishingStarTrailLength * 3; i += 3) {
          this.wishingStarPoints[i] = this.starStart.x;
          this.wishingStarPoints[i + 1] = this.starStart.y;
          this.wishingStarPoints[i + 2] = this.starStart.z;
        }

        cosmicAudio.playWishingStar();

        const banner = document.getElementById('wishing-star-banner');
        if (banner) {
          banner.classList.add('show');
          setTimeout(() => banner.classList.remove('show'), 4000);
        }
      }

      createComet() {
        this.cometActive = false;
        this.cometProgress = 0;
        this.cometCooldown = 18.0;
        this.cometTrailLength = 50;

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

        this.cometHead = new THREE.Mesh(
          new THREE.SphereGeometry(0.20, 16, 16),
          new THREE.MeshBasicMaterial({ color: 0xc8fff4, blending: THREE.AdditiveBlending })
        );
        this.cometHead.visible = false;
        this.scene.add(this.cometHead);
      }

      triggerComet() {
        if (this.cometActive) return;
        this.cometActive = true;
        this.cometProgress = 0;
        this.cometMesh.visible = true;
        this.cometHead.visible = true;

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

      triggerSupernova() {
        this.supernovaState.time = 0.0;
        this.supernovaState.intensity = 1.0;

        const overlay = document.getElementById('supernova-overlay');
        if (overlay) {
          overlay.className = 'supernova-overlay flash';
          setTimeout(() => {
            overlay.className = 'supernova-overlay decay';
          }, 70);
        }

        cosmicAudio.playSupernova();
        this.showPoeticToast('超新星爆发', '光之涟漪荡开，宇宙在心跳中重归秩序');
      }

      toggleWarpDrive() {
        this.params.isWarping = !this.params.isWarping;
        const btn = document.getElementById('btn-warp');
        const overlay = document.getElementById('warp-overlay');
        if (btn) btn.classList.toggle('active', this.params.isWarping);
        if (overlay) overlay.classList.toggle('active', this.params.isWarping);

        if (this.params.isWarping) {
          cosmicAudio.playWarpSound();
          this.showPoeticToast('曲率引擎全开', '时空跃迁中 · 恒星化作光束飞掠');
        } else {
          this.showPoeticToast('退出跃迁', '重返静谧深空坐标');
        }
      }

      toggleCinematicTour() {
        this.params.isCinematicTour = !this.params.isCinematicTour;
        const btn = document.getElementById('btn-tour');
        const topBar = document.getElementById('cinema-bar-top');
        const botBar = document.getElementById('cinema-bar-bottom');

        if (btn) btn.classList.toggle('active', this.params.isCinematicTour);
        if (topBar && botBar) {
          topBar.classList.toggle('active', this.params.isCinematicTour);
          botBar.classList.toggle('active', this.params.isCinematicTour);
        }

        if (this.params.isCinematicTour) {
          this.params.tourTime = 0;
          this.showPoeticToast('电影巡航开启', '跟随星际轨道镜头，沉浸漫游微缩宇宙');
        } else {
          this.showPoeticToast('巡航结束', '交还掌心控制权');
        }
      }

      capture4KWallpaper() {
        // Hide UI for a clean frame
        const dock = document.getElementById('control-dock');
        const sceneDock = document.getElementById('scene-dock');
        const header = document.querySelector('.app-header');
        const hint = document.getElementById('hint-badge');

        const prevDisplay = [dock.style.display, sceneDock.style.display, header.style.display, hint.style.display];
        dock.style.display = 'none';
        sceneDock.style.display = 'none';
        header.style.display = 'none';
        hint.style.display = 'none';

        // Render clean frame
        this.composer.render();

        try {
          const dataUrl = this.renderer.domElement.toDataURL('image/png');
          const a = document.createElement('a');
          a.download = `Miniature_Galaxy_Wallpaper_${Date.now()}.png`;
          a.href = dataUrl;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          this.showPoeticToast('壁纸导出成功', '已保存超高清星空纯净壁纸');
        } catch (e) {
          console.warn('Screenshot export error:', e);
        }

        // Restore UI
        dock.style.display = prevDisplay[0];
        sceneDock.style.display = prevDisplay[1];
        header.style.display = prevDisplay[2];
        hint.style.display = prevDisplay[3];
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

        // Mouse Down / Double Click / Singularity Hold
        window.addEventListener('mousedown', (e) => {
          if (e.target.closest('.control-dock') || e.target.closest('.scene-dock') || e.target.closest('.webcam-panel') || e.target.closest('.app-header')) {
            return;
          }
          this.mouse.isDown = true;
          this.mouse.x = e.clientX;
          this.mouse.y = e.clientY;

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
          const normX = (e.clientX / this.width - 0.5) * 2;
          const normY = (e.clientY / this.height - 0.5) * 2;

          this.targetRotation.y = normX * 0.70;
          this.targetRotation.x = 0.52 + normY * 0.40;

          if (this.mouse.isDown && !this.params.isGravityActive) {
            this.params.isHoldingFist = true;
          }

          // Update Gravity cursor and 3D singularity coordinates
          const gravCursor = document.getElementById('gravity-cursor');
          if (this.params.isGravityActive && gravCursor) {
            gravCursor.style.left = `${e.clientX}px`;
            gravCursor.style.top = `${e.clientY}px`;

            // Unproject mouse into 3D world space
            const rayVec = new THREE.Vector3(normX, -normY, 0.5);
            rayVec.unproject(this.camera);
            const dir = rayVec.sub(this.camera.position).normalize();
            const dist = -this.camera.position.z / dir.z;
            this.gravityWellPos.copy(this.camera.position).add(dir.multiplyScalar(dist));
            this.galaxyUniforms.uGravityWell.value.copy(this.gravityWellPos);
          }
        });

        window.addEventListener('wheel', (e) => {
          this.params.targetCameraDistance += e.deltaY * 0.015;
          this.params.targetCameraDistance = THREE.MathUtils.clamp(this.params.targetCameraDistance, 2.5, 34.0);
        }, { passive: true });

        // Keyboard Shortcuts
        window.addEventListener('keydown', (e) => {
          if (e.key >= '1' && e.key <= '5') {
            this.switchScene(parseInt(e.key) - 1);
            return;
          }
          switch (e.key.toLowerCase()) {
            case 'h':
              document.body.classList.toggle('ui-hidden');
              break;
            case 'f':
              this.toggleFullscreen();
              break;
            case ' ':
              e.preventDefault();
              this.triggerSupernova();
              break;
            case 'w':
              this.triggerWishingStar();
              break;
            case 'm':
              this.toggleSoundUI();
              break;
            case 'c':
              this.toggleCinematicTour();
              break;
            case 'g':
              this.toggleGravityWell();
              break;
            case 'p':
              this.capture4KWallpaper();
              break;
            case 't':
              this.cycleTheme();
              break;
            case 'shift':
              this.toggleWarpDrive();
              break;
          }
        });
      }

      toggleGravityWell() {
        this.params.isGravityActive = !this.params.isGravityActive;
        const btn = document.getElementById('btn-gravity');
        const cursor = document.getElementById('gravity-cursor');
        if (btn) btn.classList.toggle('active', this.params.isGravityActive);
        if (cursor) cursor.classList.toggle('active', this.params.isGravityActive);
        if (this.params.isGravityActive) {
          this.showPoeticToast('引力奇点激活', '滑动鼠标将附近万千星辰吸入空间漩涡');
        } else {
          this.showPoeticToast('引力奇点湮灭', '星辰恢复原有宇宙轨迹');
        }
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
        // Scene Switcher Buttons
        document.querySelectorAll('.scene-btn').forEach(btn => {
          btn.addEventListener('click', (e) => {
            const idx = parseInt(btn.getAttribute('data-scene'));
            this.switchScene(idx);
          });
        });

        // Sliders
        const slider = document.getElementById('speed-slider');
        if (slider) {
          slider.addEventListener('input', (e) => {
            this.params.timeScale = parseFloat(e.target.value);
            this.galaxyUniforms.uTimeScale.value = this.params.timeScale;
          });
        }

        // Action Buttons
        const fsBtn = document.getElementById('btn-fullscreen');
        if (fsBtn) fsBtn.addEventListener('click', () => this.toggleFullscreen());

        const snBtn = document.getElementById('btn-supernova');
        if (snBtn) snBtn.addEventListener('click', () => this.triggerSupernova());

        const wsBtn = document.getElementById('btn-wish');
        if (wsBtn) wsBtn.addEventListener('click', () => this.triggerWishingStar());

        const soundBtn = document.getElementById('btn-sound');
        if (soundBtn) soundBtn.addEventListener('click', () => this.toggleSoundUI());

        const warpBtn = document.getElementById('btn-warp');
        if (warpBtn) warpBtn.addEventListener('click', () => this.toggleWarpDrive());

        const tourBtn = document.getElementById('btn-tour');
        if (tourBtn) tourBtn.addEventListener('click', () => this.toggleCinematicTour());

        const snapBtn = document.getElementById('btn-snap');
        if (snapBtn) snapBtn.addEventListener('click', () => this.capture4KWallpaper());

        const themeBtn = document.getElementById('btn-theme');
        if (themeBtn) themeBtn.addEventListener('click', () => this.cycleTheme());

        const gravBtn = document.getElementById('btn-gravity');
        if (gravBtn) gravBtn.addEventListener('click', () => this.toggleGravityWell());

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

        const camBtn = document.getElementById('btn-webcam');
        if (camBtn) camBtn.addEventListener('click', () => this.toggleWebcamTracking());
      }

      async toggleWebcamTracking() {
        const panel = document.getElementById('webcam-panel');
        const btn = document.getElementById('btn-webcam');

        if (this.params.isWebcamActive) {
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

          this.cameraStream = await navigator.mediaDevices.getUserMedia({
            video: { width: 320, height: 240, facingMode: 'user' }
          });
          video.srcObject = this.cameraStream;
          await video.play();

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

      onHandResults(results) {
        if (!results.multiHandLandmarks || results.multiHandLandmarks.length === 0) return;
        const landmarks = results.multiHandLandmarks[0];
        const wrist = landmarks[0];
        const fingerTips = [landmarks[4], landmarks[8], landmarks[12], landmarks[16], landmarks[20]];

        let totalDist = 0;
        for (const tip of fingerTips) {
          const dx = tip.x - wrist.x;
          const dy = tip.y - wrist.y;
          totalDist += Math.sqrt(dx * dx + dy * dy);
        }
        const avgDist = totalDist / fingerTips.length;
        const openness = THREE.MathUtils.clamp((avgDist - 0.20) / 0.28, 0.0, 1.0);

        if (openness < 0.3) {
          this.params.isHoldingFist = true;
        } else {
          this.params.isHoldingFist = false;
        }

        const palmX = 1.0 - wrist.x;
        const palmY = wrist.y;
        this.targetRotation.y = (palmX - 0.5) * 1.5;
        this.targetRotation.x = 0.52 + (palmY - 0.5) * 0.9;

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

      animate() {
        requestAnimationFrame(this.animate);

        const delta = this.clock.getDelta();
        const elapsedTime = this.clock.getElapsedTime();

        // 1. Cinematic Tour Camera Motion
        if (this.params.isCinematicTour) {
          this.params.tourTime += delta * 0.45;
          const t = this.params.tourTime;
          // Smooth 3D flight trajectory dipping into the galaxy disk
          this.camera.position.x = Math.sin(t * 0.8) * 11.0;
          this.camera.position.y = 2.5 + Math.cos(t * 0.6) * 4.5;
          this.camera.position.z = Math.cos(t * 0.8) * 13.0;
          this.camera.lookAt(Math.sin(t * 0.4) * 2.0, 0, Math.cos(t * 0.4) * 2.0);
        } else {
          this.currentRotation.x += (this.targetRotation.x - this.currentRotation.x) * 0.05;
          this.currentRotation.y += (this.targetRotation.y - this.currentRotation.y) * 0.05;
          this.params.cameraDistance += (this.params.targetCameraDistance - this.params.cameraDistance) * 0.08;

          const macroRotation = elapsedTime * 0.02 * this.params.timeScale;
          this.galaxyGroup.rotation.y = macroRotation + this.currentRotation.y;
          this.galaxyGroup.rotation.x = this.currentRotation.x;

          this.camera.position.set(0, 8.0, this.params.cameraDistance);
          this.camera.lookAt(0, 0, 0);
        }

        // 2. Warp Drive Hyperdrive Transition
        const targetWarp = this.params.isWarping ? 1.0 : 0.0;
        this.params.warpProgress += (targetWarp - this.params.warpProgress) * 0.08;
        this.galaxyUniforms.uWarpProgress.value = this.params.warpProgress;

        if (this.params.isWarping) {
          this.camera.fov = 55.0 + this.params.warpProgress * 35.0; // Warp speed FOV stretch
          this.camera.updateProjectionMatrix();
        } else if (this.camera.fov > 55.1) {
          this.camera.fov += (55.0 - this.camera.fov) * 0.1;
          this.camera.updateProjectionMatrix();
        }

        // 3. Gravitational Singularity
        const targetGrav = this.params.isGravityActive ? 1.0 : 0.0;
        this.params.gravityStrength += (targetGrav - this.params.gravityStrength) * 0.1;
        this.galaxyUniforms.uGravityStrength.value = this.params.gravityStrength;

        // 4. Scene Morphing Transition
        if (this.isMorphing) {
          const elapsedMorph = (performance.now() - this.morphStartTime) / 2400.0; // 2.4s transition
          if (elapsedMorph >= 1.0) {
            this.isMorphing = false;
            this.galaxyUniforms.uMorphProgress.value = 1.0;
          } else {
            this.galaxyUniforms.uMorphProgress.value = elapsedMorph;
          }
        }

        // 5. Expansion / Collapse Lerp
        const targetCollapse = this.params.isHoldingFist ? 1.0 : 0.0;
        const targetExpansion = this.params.isHoldingFist ? 0.15 : 1.15;
        this.params.collapse += (targetCollapse - this.params.collapse) * 0.065;
        this.params.expansion += (targetExpansion - this.params.expansion) * 0.065;

        const breath = Math.sin(elapsedTime * 1.8) * 0.1;

        // 6. Near-Screen Chaos
        const nearScreenThreshold = 6.8;
        let targetChaos = 0.0;
        if (this.params.cameraDistance < nearScreenThreshold) {
          targetChaos = (nearScreenThreshold - this.params.cameraDistance) / 4.0;
          targetChaos = THREE.MathUtils.clamp(targetChaos, 0.0, 1.0);
        }
        this.params.chaos += (targetChaos - this.params.chaos) * 0.1;

        this.galaxyUniforms.uTime.value = elapsedTime;
        this.galaxyUniforms.uExpansion.value = this.params.expansion;
        this.galaxyUniforms.uCollapse.value = this.params.collapse;
        this.galaxyUniforms.uBreath.value = breath;
        this.galaxyUniforms.uChaos.value = this.params.chaos;
        this.galaxyUniforms.uBrightness.value = this.params.brightness;

        this.coreMaterial.uniforms.uTime.value = elapsedTime;
        this.coreMaterial.uniforms.uBreath.value = breath;
        this.coreMaterial.uniforms.uCollapse.value = this.params.collapse;

        this.bokehUniforms.uTime.value = elapsedTime;

        // 7. Supernova Shockwave Propagation
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

        // 8. Binary Stars Dynamics (Active in Scene 0, 3, 4)
        const binarySpeed = elapsedTime * 2.2 * this.params.timeScale;
        const binaryR = 0.75 * (1.0 - this.params.collapse * 0.65);
        const star1X = Math.cos(binarySpeed) * binaryR;
        const star1Z = Math.sin(binarySpeed) * binaryR;
        const star2X = -star1X;
        const star2Z = -star1Z;
        const starY = Math.sin(binarySpeed * 1.5) * 0.12;

        this.twinStar1.position.set(star1X, starY, star1Z);
        this.twinStar2.position.set(star2X, -starY, star2Z);

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

        // 9. Wishing Star Update
        this.params.wishingStarCountdown -= delta;
        if (this.params.wishingStarCountdown <= 0) {
          this.triggerWishingStar();
          this.params.wishingStarCountdown = 90.0 + Math.random() * 20.0;
        }

        if (this.wishingStarActive) {
          this.wishingStarProgress += delta * 0.35;
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

        // 10. Deep Space Comet
        this.cometCooldown -= delta;
        if (this.cometCooldown <= 0) {
          this.triggerComet();
          this.cometCooldown = 20.0 + Math.random() * 16.0;
        }

        if (this.cometActive) {
          this.cometProgress += delta * 0.22;
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

        cosmicAudio.update(this.params.expansion, this.params.collapse, breath, this.params.warpProgress);

        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');
        if (statusDot && statusText) {
          if (this.params.isHoldingFist) {
            statusDot.className = 'status-dot collapsed';
            statusText.textContent = '宇宙坍缩 (Fist)';
          } else if (this.params.isWarping) {
            statusDot.className = 'status-dot pulse';
            statusText.textContent = '曲率跃迁 (Warp)';
          } else if (this.params.isGravityActive) {
            statusDot.className = 'status-dot pulse';
            statusText.textContent = '引力奇点 (Gravity)';
          } else if (this.params.chaos > 0.3) {
            statusDot.className = 'status-dot pulse';
            statusText.textContent = '近屏混沌 (Chaos)';
          } else {
            statusDot.className = 'status-dot warm';
            statusText.textContent = '星河绽放 (Bloom)';
          }
        }

        this.composer.render();
      }
    }

    window.addEventListener('DOMContentLoaded', () => {
      new MiniatureGalaxyApp();
    });
  </script>
</body>
</html>
'''

with open('e:\\\\AN1\\\\micro_galaxy\\\\index.html', 'w', encoding='utf-8') as f:
    f.write(epic_html)

print("Generated Epic index.html with 5 morphing scenes successfully!")
