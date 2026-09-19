/**
 * Miniature Galaxy - Custom GLSL Shaders
 * Implements Keplerian orbits, spiral arm stretching, volumetric core pulse,
 * star diffraction spikes, chromatic dispersion, dual-zone color gradient,
 * burning edge interface, near-screen Brownian chaos, and supernova shockwaves.
 */

export const galaxyVertexShader = /* glsl */ `
  precision highp float;

  attribute float aOrbitRadius;
  attribute float aOrbitAngle;
  attribute float aOrbitSpeed;
  attribute float aArmOffset;
  attribute float aVerticalOffset;
  attribute float aParticleSize;
  attribute float aParticleType; // 0=Core, 1=Spiral Arm, 2=Ambient Dust, 3=Filament
  attribute float aColorSeed;

  uniform float uTime;
  uniform float uTimeScale;
  uniform float uExpansion;     // 0.0 to 1.5 (normal = 1.0)
  uniform float uCollapse;      // 0.0 to 1.0 (clenched fist = 1.0)
  uniform float uBreath;        // Periodic pulse
  uniform float uChaos;         // 0.0 to 1.0 (near-screen chaos)
  uniform float uSupernovaTime; // Time since explosion (-1.0 if inactive)
  uniform float uSupernovaIntensity;
  uniform float uPixelRatio;
  uniform float uBrightness;

  varying vec3 vColor;
  varying float vAlpha;
  varying float vParticleType;
  varying float vNormalizedRadius;
  varying float vSpeedRatio;
  varying float vSize;

  // Simple 3D pseudo-random & simplex noise
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

    // 1. Keplerian Orbit Dynamics: Inner fast, outer slow
    float t = uTime * uTimeScale;
    float currentAngle = aOrbitAngle + aOrbitSpeed * t;

    // 2. Breathing and Contraction/Expansion radius
    // When uCollapse -> 1.0: radius drops sharply towards 10%
    // When uExpansion -> 1.5: radius expands, spiral arms bloom
    float rScale = mix(1.0, 0.12, uCollapse) * mix(0.5, 1.45, uExpansion) * (1.0 + uBreath * 0.08);
    float r = (aOrbitRadius + aArmOffset) * rScale;

    // Logarithmic pitch adjustment
    float logWinding = log(max(aOrbitRadius, 0.2) + 1.0) * 0.35;
    float angle = currentAngle + logWinding;

    // Calculate planar position
    vec3 pos;
    pos.x = cos(angle) * r;
    pos.z = sin(angle) * r;

    // Vertical thickness with disk flaring: inner thin, outer flared
    float verticalFlare = (0.04 + aOrbitRadius * 0.035) * mix(1.0, 0.15, uCollapse);
    pos.y = aVerticalOffset * verticalFlare;

    // Ambient dust slow 3D undulation
    if (aParticleType > 1.5 && aParticleType < 2.5) {
      pos.x += sin(t * 0.4 + aOrbitAngle) * 0.4;
      pos.y += cos(t * 0.3 + aOrbitRadius) * 0.3;
      pos.z += sin(t * 0.35 + aArmOffset) * 0.4;
    }

    // 3. Fist Clench Micro-Tremble (When clutched tightly in fist)
    if (uCollapse > 0.1) {
      float trembleFreq = 42.0;
      float trembleAmp = 0.045 * uCollapse * (1.0 + sin(t * trembleFreq + aColorSeed * 10.0));
      pos += (vec3(hash(pos), hash(pos + 1.0), hash(pos + 2.0)) - 0.5) * trembleAmp;
    }

    // 4. Supernova Shockwave Interaction
    if (uSupernovaTime > 0.0 && uSupernovaTime < 4.0) {
      float waveSpeed = 16.0;
      float waveRadius = uSupernovaTime * waveSpeed;
      float particleDist = length(pos);
      float distDiff = abs(particleDist - waveRadius);
      float waveWidth = 2.2;

      // Impulsive push along radial vector
      if (distDiff < waveWidth * 2.5) {
        float impulse = exp(-pow(distDiff / waveWidth, 2.0)) * exp(-uSupernovaTime * 0.9) * uSupernovaIntensity;
        vec3 pushDir = normalize(pos + vec3(0.0001));
        // Push outward + upward turbulence
        pos += pushDir * impulse * 4.8;
        pos += curlNoise(pos * 0.8 + t * 4.0) * impulse * 2.2;
      }
    }

    // 5. Near-Screen Chaos: High-frequency Brownian noise storm
    if (uChaos > 0.001) {
      float noiseFreq = 1.2;
      vec3 chaosDisplacement = curlNoise(pos * noiseFreq + vec3(t * 3.5, t * 2.8, t * 3.1));
      float chaosBurst = uChaos * (3.5 + 2.0 * sin(t * 8.0 + aColorSeed * 6.28));
      pos += chaosDisplacement * chaosBurst;
    }

    // 6. Project to screen
    vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * mvPosition;

    // Distance attenuation & dynamic size
    float dist = -mvPosition.z;
    float sizeScale = mix(0.7, 1.5, uExpansion) * mix(1.0, 0.7, uCollapse);
    float pointSize = aParticleSize * sizeScale * (120.0 / max(dist, 0.5)) * uPixelRatio;

    // Filament stars elongated along motion
    if (aParticleType > 2.5) {
      pointSize *= 1.35;
    }

    gl_PointSize = clamp(pointSize, 1.2, 160.0);
    vSize = gl_PointSize;

    // Varyings passed to fragment shader
    vNormalizedRadius = clamp(aOrbitRadius / 14.0, 0.0, 1.0);
    vSpeedRatio = clamp(aOrbitSpeed / 1.5, 0.0, 1.0);

    // Dynamic Base Alpha
    // Individual star hue micro-variation
    vColor = vec3(
      fract(aColorSeed * 12.9898),
      fract(aColorSeed * 78.233),
      fract(aColorSeed * 45.164)
    );

    float baseAlpha = 0.85;
    if (aParticleType > 1.5 && aParticleType < 2.5) {
      // Ambient background stardust: dim and ethereal
      baseAlpha = 0.28;
    } else if (aParticleType < 0.5) {
      // Core: hyper-dense and radiant
      baseAlpha = 0.95;
    }
    vAlpha = baseAlpha;
  }
`;

export const galaxyFragmentShader = /* glsl */ `
  precision highp float;

  uniform float uTime;
  uniform float uExpansion;     // 0.0 to 1.5
  uniform float uCollapse;      // 0.0 to 1.0
  uniform float uBrightness;    // Master brightness
  uniform float uSupernovaTime;

  varying vec3 vColor;
  varying float vAlpha;
  varying float vParticleType;
  varying float vNormalizedRadius;
  varying float vSpeedRatio;
  varying float vSize;

  void main() {
    vec2 coord = gl_PointCoord - vec2(0.5);
    float dist = length(coord);

    if (dist > 0.5) {
      discard;
    }

    // 1. Core radial hot spot
    float coreGlow = exp(-dist * 14.0);
    float softGlow = exp(-dist * 4.5);

    // 2. Bright Star Spikes (十字星光衍射)
    // Prominent on bright/larger stars, subtle on smaller ones
    float spikeWeight = smoothstep(6.0, 36.0, vSize);
    float spikeX = exp(-abs(coord.x) * 50.0) * exp(-abs(coord.y) * 4.0);
    float spikeY = exp(-abs(coord.y) * 50.0) * exp(-abs(coord.x) * 4.0);
    float crossSpike = (spikeX + spikeY) * spikeWeight * 1.8;

    // Subtle 45-degree diagonal spikes
    float d1 = abs(coord.x + coord.y) * 0.7071;
    float d2 = abs(coord.x - coord.y) * 0.7071;
    float diagSpike = (exp(-d1 * 65.0) * exp(-d2 * 5.0) + exp(-d2 * 65.0) * exp(-d1 * 5.0)) * spikeWeight * 0.6;

    // 3. Prism Chromatic Dispersion (大粒子宝石般棱镜色散)
    // Red, Green, Blue channels sample at slightly different radii
    float dispersionShift = 0.045 * spikeWeight;
    float distR = length(coord * (1.0 - dispersionShift));
    float distG = length(coord);
    float distB = length(coord * (1.0 + dispersionShift));

    vec3 spectralIntensity = vec3(
      exp(-distR * 7.5),
      exp(-distG * 7.5),
      exp(-distB * 7.5)
    );

    // 4. Color Narrative (色彩叙事)
    // Contracted: Ice Blue (#88c0d0, #caf0f8) & Silver White (#e5e9f0)
    // Expanded: Molten Gold (#ffd166, #ffb703), Rose Gold (#ff70a6), Astral Violet (#7209b7)

    // Inner Core Colors
    vec3 colCoreCold = vec3(0.72, 0.90, 1.0);       // Ice diamond
    vec3 colCoreWarm = vec3(1.0, 0.94, 0.75);       // Scorching golden core
    vec3 colCore = mix(colCoreCold, colCoreWarm, clamp(uExpansion, 0.0, 1.0));

    // Mid Disk / Inner Arms
    vec3 colMidCold = vec3(0.35, 0.55, 0.85);        // Dawn ocean cobalt
    vec3 colMidWarm = vec3(1.0, 0.68, 0.35);        // Molten amber gold
    vec3 colMid = mix(colMidCold, colMidWarm, clamp(uExpansion, 0.0, 1.0));

    // Outer Spiral Arms
    vec3 colOuterCold = vec3(0.20, 0.30, 0.65);      // Deep silent indigo
    vec3 colOuterWarm = vec3(0.55, 0.15, 0.85);      // Astral nebular violet
    vec3 colOuter = mix(colOuterCold, colOuterWarm, clamp(uExpansion, 0.0, 1.0));

    // Rose gold accent for filament particles
    vec3 colRoseGold = vec3(1.0, 0.55, 0.72);

    // Base galactic color by normalized radius
    vec3 starColor;
    if (vNormalizedRadius < 0.22) {
      starColor = mix(colCore, colMid, vNormalizedRadius / 0.22);
    } else {
      float tOuter = (vNormalizedRadius - 0.22) / 0.78;
      starColor = mix(colMid, colOuter, tOuter);
    }

    if (vParticleType > 2.5) {
      // Filaments have rose gold / aurora silk tint
      starColor = mix(starColor, colRoseGold, 0.55);
    }

    // Subtle individual star hue temperature micro-variation
    starColor += (vColor - 0.5) * 0.09;

    // 5. Burning Edge Fault Line (燃烧的边缘 - 冷暖交界处的光晕断层)
    // Boundary at normalized radius ~ 0.26
    float edgeCenter = 0.26;
    float edgeWidth = 0.07;
    float burningEdge = exp(-pow((vNormalizedRadius - edgeCenter) / edgeWidth, 2.0));
    vec3 burningColor = vec3(1.0, 0.42, 0.18) * (1.0 + 0.35 * sin(uTime * 4.0 + vNormalizedRadius * 20.0));
    starColor += burningColor * burningEdge * 0.75 * mix(0.4, 1.2, uExpansion);

    // 6. Supernova Flash Tint
    if (uSupernovaTime > 0.0 && uSupernovaTime < 2.5) {
      float flash = exp(-uSupernovaTime * 2.2);
      starColor = mix(starColor, vec3(1.0, 0.98, 0.95), flash * 0.7);
    }

    // 7. Physical Scale-to-Luminosity Linkage (小=暗，大=亮)
    // Smooth physical transition from faint night-light to blazing stellar fire
    float scaleLuminance = mix(0.18, 2.2, pow(clamp(uExpansion, 0.0, 1.5), 1.25));
    scaleLuminance *= mix(1.0, 0.15, uCollapse);

    // Final Composite Luminance & Alpha
    float shape = coreGlow * 1.6 + softGlow * 0.65 + crossSpike + diagSpike;
    vec3 finalColor = starColor * spectralIntensity * shape * scaleLuminance * uBrightness;

    float alpha = clamp(shape * vAlpha, 0.0, 1.0);

    gl_FragColor = vec4(finalColor, alpha);
  }
`;

/**
 * Volumetric Core Glow Shader
 * Renders the pulsating, living star-heart with multi-layered volume glow.
 */
export const coreGlowVertexShader = /* glsl */ `
  varying vec2 vUv;
  varying vec3 vNormal;

  void main() {
    vUv = uv;
    vNormal = normalize(normalMatrix * normal);
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

export const coreGlowFragmentShader = /* glsl */ `
  precision highp float;

  uniform float uTime;
  uniform float uBreath;
  uniform float uExpansion;
  uniform float uCollapse;
  uniform float uSupernovaTime;

  varying vec2 vUv;
  varying vec3 vNormal;

  void main() {
    vec2 p = vUv - vec2(0.5);
    float d = length(p) * 2.0;

    if (d > 1.0) {
      discard;
    }

    // Heartbeat pulsation
    float pulse = 1.0 + uBreath * 0.25 + 0.08 * sin(uTime * 6.0);

    // Multi-layered exponential falloff for volumetric depth
    float innerCore = exp(-d * 4.5 * pulse);
    float outerHalo = exp(-d * 1.8 * pulse);
    float rim = pow(1.0 - d, 2.5);

    // Color transition: Cold ice diamond -> Blazing gold & rose
    vec3 coldColor = vec3(0.55, 0.85, 1.0);
    vec3 warmColor = vec3(1.0, 0.82, 0.45);
    vec3 roseHalo = vec3(1.0, 0.35, 0.65);

    vec3 baseCol = mix(coldColor, warmColor, clamp(uExpansion, 0.0, 1.0));
    vec3 coreColor = mix(baseCol, roseHalo, outerHalo * 0.4);

    // Supernova burst
    if (uSupernovaTime > 0.0 && uSupernovaTime < 3.0) {
      float flash = exp(-uSupernovaTime * 2.5);
      coreColor = mix(coreColor, vec3(1.0, 0.98, 0.92), flash * 0.9);
    }

    float brightness = mix(0.2, 2.5, uExpansion) * mix(1.0, 0.25, uCollapse);
    float alpha = (innerCore * 0.9 + outerHalo * 0.45 + rim * 0.2) * brightness;

    gl_FragColor = vec4(coreColor * (innerCore * 2.2 + outerHalo), alpha);
  }
`;

/**
 * Foreground Shallow DOF Bokeh Dust Shader
 * Near-camera dust motes that blur into soft circular discs with chromatic aberration.
 */
export const bokehVertexShader = /* glsl */ `
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
    // Slow drifting near the lens
    pos.x += sin(uTime * 0.2 + position.z) * 0.3;
    pos.y += cos(uTime * 0.25 + position.x) * 0.25;
    pos.z += sin(uTime * 0.15 + position.y) * 0.3;

    vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * mvPosition;

    vDist = -mvPosition.z;
    // Larger when very close (defocused bokeh disk)
    float bokehSize = aSize * (160.0 / max(vDist, 0.2)) * uPixelRatio;
    gl_PointSize = clamp(bokehSize, 12.0, 140.0);
  }
`;

export const bokehFragmentShader = /* glsl */ `
  precision highp float;

  varying vec3 vColor;
  varying float vDist;

  void main() {
    vec2 coord = gl_PointCoord - vec2(0.5);
    float r = length(coord);

    if (r > 0.5) {
      discard;
    }

    // Soft out-of-focus bokeh disc with subtle bright ring (spherical aberration)
    float ring = smoothstep(0.38, 0.48, r) * (1.0 - smoothstep(0.48, 0.5, r));
    float softFill = smoothstep(0.5, 0.0, r);
    float bokehDisc = softFill * 0.45 + ring * 0.55;

    // Chromatic aberration at edge of bokeh
    float rR = length(coord * 0.95);
    float rB = length(coord * 1.05);
    vec3 chromatic = vec3(
      smoothstep(0.5, 0.0, rR),
      bokehDisc,
      smoothstep(0.5, 0.0, rB)
    );

    vec3 finalColor = vColor * chromatic * 1.2;
    float alpha = bokehDisc * 0.22;

    gl_FragColor = vec4(finalColor, alpha);
  }
`;
