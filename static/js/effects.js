/**
 * Terminal Visual Effects
 * Matrix rain, plasma, fire, and other retro effects
 */

// ============================================
// Matrix Rain Effect
// ============================================
class MatrixRain {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.columns = [];
    this.fontSize = 14;
    this.chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()_+-=[]{}|;:,.<>?~`';
    this.running = false;
    this.resize();
    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    const columnCount = Math.floor(this.canvas.width / this.fontSize);
    this.columns = Array(columnCount).fill(0).map(() => ({
      y: Math.random() * -100,
      speed: 0.5 + Math.random() * 1.5,
      chars: this.generateChars()
    }));
  }

  generateChars() {
    const length = 10 + Math.floor(Math.random() * 20);
    return Array(length).fill(0).map(() =>
      this.chars[Math.floor(Math.random() * this.chars.length)]
    );
  }

  draw() {
    // Fade effect
    this.ctx.fillStyle = 'rgba(10, 14, 20, 0.05)';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    this.ctx.font = `${this.fontSize}px "IBM Plex Mono", monospace`;

    this.columns.forEach((col, i) => {
      const x = i * this.fontSize;

      col.chars.forEach((char, j) => {
        const y = (col.y - j) * this.fontSize;
        if (y < 0 || y > this.canvas.height) return;

        // Head character is bright
        if (j === 0) {
          this.ctx.fillStyle = 'rgba(180, 255, 180, 1)';
          this.ctx.shadowColor = '#6effc8';
          this.ctx.shadowBlur = 10;
        } else {
          // Fade based on position in trail
          const alpha = 1 - (j / col.chars.length);
          const green = Math.floor(180 * alpha);
          this.ctx.fillStyle = `rgb(0, ${green}, ${Math.floor(green/4)})`;
          this.ctx.shadowBlur = 0;
        }

        this.ctx.fillText(char, x, y);
      });

      // Move column down
      col.y += col.speed;

      // Randomly change characters
      if (Math.random() < 0.02) {
        const idx = Math.floor(Math.random() * col.chars.length);
        col.chars[idx] = this.chars[Math.floor(Math.random() * this.chars.length)];
      }

      // Reset when off screen
      if ((col.y - col.chars.length) * this.fontSize > this.canvas.height) {
        col.y = Math.random() * -20;
        col.speed = 0.5 + Math.random() * 1.5;
        col.chars = this.generateChars();
      }
    });
  }

  start() {
    this.running = true;
    const animate = () => {
      if (!this.running) return;
      this.draw();
      requestAnimationFrame(animate);
    };
    animate();
  }

  stop() {
    this.running = false;
  }
}

// ============================================
// Plasma Effect
// ============================================
class PlasmaEffect {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.time = 0;
    this.running = false;
    this.imageData = null;
    this.resize();
    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    // Use lower resolution for performance
    this.width = Math.floor(window.innerWidth / 4);
    this.height = Math.floor(window.innerHeight / 4);
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.ctx.imageSmoothingEnabled = false;
    this.imageData = this.ctx.createImageData(this.width, this.height);
  }

  draw() {
    const data = this.imageData.data;
    const t = this.time;

    for (let y = 0; y < this.height; y++) {
      for (let x = 0; x < this.width; x++) {
        const i = (y * this.width + x) * 4;

        // Plasma formula
        const v1 = Math.sin(x * 0.05 + t);
        const v2 = Math.sin((y * 0.05 + t) * 0.5);
        const v3 = Math.sin((x * 0.05 + y * 0.05 + t) * 0.5);
        const v4 = Math.sin(Math.sqrt((x - this.width/2) ** 2 + (y - this.height/2) ** 2) * 0.05 + t);

        const v = (v1 + v2 + v3 + v4) / 4;

        // Cyberpunk colors
        const r = Math.floor((Math.sin(v * Math.PI + t) + 1) * 60);
        const g = Math.floor((Math.sin(v * Math.PI + t * 1.5) + 1) * 80 + 50);
        const b = Math.floor((Math.sin(v * Math.PI + t * 0.5) + 1) * 127);

        data[i] = r;
        data[i + 1] = g;
        data[i + 2] = b;
        data[i + 3] = 255;
      }
    }

    // Draw at low res then scale up
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = this.width;
    tempCanvas.height = this.height;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.putImageData(this.imageData, 0, 0);

    this.ctx.drawImage(tempCanvas, 0, 0, this.canvas.width, this.canvas.height);

    this.time += 0.02;
  }

  start() {
    this.running = true;
    const animate = () => {
      if (!this.running) return;
      this.draw();
      requestAnimationFrame(animate);
    };
    animate();
  }

  stop() {
    this.running = false;
  }
}

// ============================================
// Doom Fire Effect
// ============================================
class DoomFire {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.firePixels = [];
    this.palette = this.createPalette();
    this.running = false;
    this.resize();
    window.addEventListener('resize', () => this.resize());
  }

  createPalette() {
    // Classic Doom fire palette
    const colors = [
      [0, 0, 0], [31, 7, 7], [47, 15, 7], [71, 15, 7], [87, 23, 7],
      [103, 31, 7], [119, 31, 7], [143, 39, 7], [159, 47, 7], [175, 63, 7],
      [191, 71, 7], [199, 71, 7], [223, 79, 7], [223, 87, 7], [223, 87, 7],
      [215, 95, 7], [215, 95, 7], [215, 103, 15], [207, 111, 15], [207, 119, 15],
      [207, 127, 15], [207, 135, 23], [199, 135, 23], [199, 143, 23], [199, 151, 31],
      [191, 159, 31], [191, 159, 31], [191, 167, 39], [191, 167, 39], [191, 175, 47],
      [183, 175, 47], [183, 183, 47], [183, 183, 55], [207, 207, 111], [223, 223, 159],
      [239, 239, 199], [255, 255, 255]
    ];
    return colors;
  }

  resize() {
    this.width = Math.floor(window.innerWidth / 6);
    this.height = Math.floor(window.innerHeight / 6);
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.ctx.imageSmoothingEnabled = false;

    // Initialize fire pixels
    this.firePixels = new Array(this.width * this.height).fill(0);
    // Set bottom row to max (white hot)
    for (let x = 0; x < this.width; x++) {
      this.firePixels[(this.height - 1) * this.width + x] = this.palette.length - 1;
    }
  }

  spreadFire(src) {
    const pixel = this.firePixels[src];
    if (pixel === 0) {
      this.firePixels[src - this.width] = 0;
    } else {
      const rand = Math.floor(Math.random() * 3);
      const dst = src - rand + 1;
      this.firePixels[dst - this.width] = pixel - (rand & 1);
    }
  }

  draw() {
    // Spread fire upward
    for (let x = 0; x < this.width; x++) {
      for (let y = 1; y < this.height; y++) {
        this.spreadFire(y * this.width + x);
      }
    }

    // Render
    const imageData = this.ctx.createImageData(this.width, this.height);
    for (let i = 0; i < this.firePixels.length; i++) {
      const color = this.palette[this.firePixels[i]] || [0, 0, 0];
      const idx = i * 4;
      imageData.data[idx] = color[0];
      imageData.data[idx + 1] = color[1];
      imageData.data[idx + 2] = color[2];
      imageData.data[idx + 3] = 255;
    }

    // Scale up
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = this.width;
    tempCanvas.height = this.height;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.putImageData(imageData, 0, 0);

    this.ctx.drawImage(tempCanvas, 0, 0, this.canvas.width, this.canvas.height);
  }

  start() {
    this.running = true;
    const animate = () => {
      if (!this.running) return;
      this.draw();
      requestAnimationFrame(animate);
    };
    animate();
  }

  stop() {
    this.running = false;
  }
}

// ============================================
// Starfield Effect
// ============================================
class Starfield {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.stars = [];
    this.starCount = 200;
    this.running = false;
    this.resize();
    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.centerX = this.canvas.width / 2;
    this.centerY = this.canvas.height / 2;

    // Initialize stars
    this.stars = Array(this.starCount).fill(0).map(() => ({
      x: Math.random() * this.canvas.width - this.centerX,
      y: Math.random() * this.canvas.height - this.centerY,
      z: Math.random() * this.canvas.width,
      pz: 0
    }));
  }

  draw() {
    this.ctx.fillStyle = 'rgba(10, 14, 20, 0.2)';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    this.stars.forEach(star => {
      star.pz = star.z;
      star.z -= 8;

      if (star.z < 1) {
        star.x = Math.random() * this.canvas.width - this.centerX;
        star.y = Math.random() * this.canvas.height - this.centerY;
        star.z = this.canvas.width;
        star.pz = star.z;
      }

      const sx = (star.x / star.z) * 200 + this.centerX;
      const sy = (star.y / star.z) * 200 + this.centerY;
      const px = (star.x / star.pz) * 200 + this.centerX;
      const py = (star.y / star.pz) * 200 + this.centerY;

      const size = (1 - star.z / this.canvas.width) * 3;
      const alpha = 1 - star.z / this.canvas.width;

      this.ctx.beginPath();
      this.ctx.moveTo(px, py);
      this.ctx.lineTo(sx, sy);
      this.ctx.strokeStyle = `rgba(180, 220, 255, ${alpha})`;
      this.ctx.lineWidth = size;
      this.ctx.stroke();
    });
  }

  start() {
    this.running = true;
    const animate = () => {
      if (!this.running) return;
      this.draw();
      requestAnimationFrame(animate);
    };
    animate();
  }

  stop() {
    this.running = false;
  }
}

// ============================================
// Effect Manager
// ============================================
class EffectManager {
  constructor() {
    this.effects = {
      matrix: MatrixRain,
      plasma: PlasmaEffect,
      fire: DoomFire,
      starfield: Starfield
    };
    this.currentEffect = null;
    this.currentName = null;
  }

  init(canvasId, effectName = 'matrix') {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    this.stop();

    const EffectClass = this.effects[effectName];
    if (EffectClass) {
      this.currentEffect = new EffectClass(canvas);
      this.currentName = effectName;
      this.currentEffect.start();
    }
  }

  stop() {
    if (this.currentEffect) {
      this.currentEffect.stop();
      this.currentEffect = null;
    }
  }

  cycle() {
    const names = Object.keys(this.effects);
    const currentIndex = names.indexOf(this.currentName);
    const nextIndex = (currentIndex + 1) % names.length;
    const canvas = this.currentEffect?.canvas;
    if (canvas) {
      this.init(canvas.id, names[nextIndex]);
    }
    return names[nextIndex];
  }
}

// Global instance
window.effectManager = new EffectManager();
