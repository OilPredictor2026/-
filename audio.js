/**
 * Miniature Galaxy - Procedural Cosmic Soundscape
 * Zero-dependency Web Audio API synthesizer for breathing ambient drone,
 * supernova detonation rumble, and wishing star crystal chimes.
 */

class CosmicSoundEngine {
  constructor() {
    this.ctx = null;
    this.isMuted = true;
    this.masterGain = null;
    this.droneFilter = null;
    this.oscillators = [];
    this.shimmerNodes = [];
    this.isInitialized = false;
  }

  init() {
    if (this.isInitialized) return;

    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioContext();

      // Master output gain
      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.setValueAtTime(0, this.ctx.currentTime);
      this.masterGain.connect(this.ctx.destination);

      // Celestial ambient drone low-pass filter
      this.droneFilter = this.ctx.createBiquadFilter();
      this.droneFilter.type = 'lowpass';
      this.droneFilter.frequency.setValueAtTime(450, this.ctx.currentTime);
      this.droneFilter.Q.setValueAtTime(3.0, this.ctx.currentTime);
      this.droneFilter.connect(this.masterGain);

      // Deep space chords (432Hz harmonic proportions)
      const baseFreqs = [54.0, 81.0, 108.0, 162.0, 216.0];
      baseFreqs.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        osc.type = idx === 0 ? 'sine' : 'triangle';
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

        const oscGain = this.ctx.createGain();
        oscGain.gain.setValueAtTime(0.12 / (idx + 1), this.ctx.currentTime);

        // Subtle slow LFO detuning
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
      console.warn('Web Audio initialization error:', err);
    }
  }

  toggleSound() {
    if (!this.isInitialized) {
      this.init();
    }
    if (!this.ctx) return false;

    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }

    this.isMuted = !this.isMuted;
    const targetGain = this.isMuted ? 0 : 0.45;
    this.masterGain.gain.setTargetAtTime(targetGain, this.ctx.currentTime, 0.2);
    return !this.isMuted;
  }

  /**
   * Update audio parameters based on galaxy physics state
   * @param {number} expansion 0.0 to 1.5
   * @param {number} collapse 0.0 to 1.0
   * @param {number} breath -0.1 to 0.1
   */
  update(expansion, collapse, breath) {
    if (!this.isInitialized || this.isMuted) return;

    const now = this.ctx.currentTime;
    // Modulate filter frequency: expansion brings highs, collapse cuts down to sub-bass
    const cutoff = (300 + expansion * 600) * (1.0 - collapse * 0.7) + breath * 150;
    this.droneFilter.frequency.setTargetAtTime(Math.max(60, cutoff), now, 0.1);
  }

  /**
   * Trigger Supernova shockwave sound: deep sub-rumble + resonant shimmer
   */
  playSupernova() {
    if (!this.isInitialized || this.isMuted) return;

    const now = this.ctx.currentTime;

    // 1. Sub rumble oscillator
    const subOsc = this.ctx.createOscillator();
    subOsc.type = 'sine';
    subOsc.frequency.setValueAtTime(120, now);
    subOsc.frequency.exponentialRampToValueAtTime(32, now + 1.8);

    const subGain = this.ctx.createGain();
    subGain.gain.setValueAtTime(0.7, now);
    subGain.gain.exponentialRampToValueAtTime(0.001, now + 2.5);

    subOsc.connect(subGain);
    subGain.connect(this.masterGain);
    subOsc.start(now);
    subOsc.stop(now + 2.6);

    // 2. High crystalline shockwave sparkle
    for (let i = 0; i < 4; i++) {
      const chime = this.ctx.createOscillator();
      chime.type = 'sine';
      chime.frequency.setValueAtTime(864 * (i + 1) * 0.75, now);
      chime.frequency.exponentialRampToValueAtTime(432 * (i + 1), now + 3.0);

      const chimeGain = this.ctx.createGain();
      chimeGain.gain.setValueAtTime(0.08 / (i + 1), now);
      chimeGain.gain.exponentialRampToValueAtTime(0.0001, now + 3.2);

      chime.connect(chimeGain);
      chimeGain.connect(this.masterGain);
      chime.start(now + i * 0.05);
      chime.stop(now + 3.3);
    }
  }

  /**
   * Trigger Wishing Star pass: ethereal stereo bell sweep
   */
  playWishingStar() {
    if (!this.isInitialized || this.isMuted) return;

    const now = this.ctx.currentTime;
    const panner = this.ctx.createStereoPanner ? this.ctx.createStereoPanner() : null;

    if (panner) {
      panner.pan.setValueAtTime(-0.8, now);
      panner.pan.linearRampToValueAtTime(0.8, now + 3.5);
      panner.connect(this.masterGain);
    }

    const bell = this.ctx.createOscillator();
    bell.type = 'triangle';
    bell.frequency.setValueAtTime(1296, now);
    bell.frequency.exponentialRampToValueAtTime(1728, now + 1.5);
    bell.frequency.exponentialRampToValueAtTime(864, now + 3.5);

    const bellGain = this.ctx.createGain();
    bellGain.gain.setValueAtTime(0.001, now);
    bellGain.gain.linearRampToValueAtTime(0.18, now + 0.8);
    bellGain.gain.exponentialRampToValueAtTime(0.0001, now + 3.8);

    bell.connect(bellGain);
    if (panner) {
      bellGain.connect(panner);
    } else {
      bellGain.connect(this.masterGain);
    }

    bell.start(now);
    bell.stop(now + 4.0);
  }
}

export const cosmicAudio = new CosmicSoundEngine();
