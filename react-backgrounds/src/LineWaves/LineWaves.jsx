import { useEffect, useRef } from 'react';
import './LineWaves.css';

const LineWaves = ({
  speed = 0.5,
  innerLineCount = 32,
  outerLineCount = 29,
  warpIntensity = 1,
  rotation = -51,
  edgeFadeWidth = 0.05,
  colorCycleSpeed = 2.2,
  brightness = 0.2,
  color1 = '#ff0000',
  color2 = '#8b0000',
  color3 = '#481919',
  enableMouseInteraction = false,
  mouseInfluence = 2,
}) => {
  const canvasRef = useRef(null);
  const stateRef = useRef({
    animId: null,
    time: 0,
    mouse: { x: 0.5, y: 0.5 },
  });

  // Parse a hex/rgb colour into [r,g,b] 0-1
  const parseColor = (col) => {
    const d = document.createElement('div');
    d.style.color = col;
    document.body.appendChild(d);
    const c = window.getComputedStyle(d).color;
    document.body.removeChild(d);
    const m = c.match(/[\d.]+/g);
    return m ? [+m[0] / 255, +m[1] / 255, +m[2] / 255] : [1, 0, 0];
  };

  const lerpColor = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const state = stateRef.current;

    const c1 = parseColor(color1);
    const c2 = parseColor(color2);
    const c3 = parseColor(color3);

    const resize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(canvas);

    const onMouseMove = (e) => {
      if (!enableMouseInteraction) return;
      const rect = canvas.getBoundingClientRect();
      state.mouse.x = (e.clientX - rect.left) / rect.width;
      state.mouse.y = (e.clientY - rect.top) / rect.height;
    };
    if (enableMouseInteraction) {
      canvas.addEventListener('mousemove', onMouseMove);
    }

    const rotRad = (rotation * Math.PI) / 180;
    const cosR = Math.cos(rotRad);
    const sinR = Math.sin(rotRad);

    const drawLines = (lines, isInner) => {
      const W = canvas.width;
      const H = canvas.height;

      lines.forEach((line, idx) => {
        // normalised t 0→1 across all lines
        const t = lines.length > 1 ? idx / (lines.length - 1) : 0.5;

        // colour cycle based on time + position
        const cycle = (state.time * colorCycleSpeed * 0.3 + t * 2) % 2;
        let col;
        if (cycle < 1) {
          col = lerpColor(c1, c2, cycle);
        } else {
          col = lerpColor(c2, c3, cycle - 1);
        }

        // edge fade
        const edgeFade = Math.min(t / edgeFadeWidth, 1, (1 - t) / edgeFadeWidth);
        const alpha = brightness * edgeFade * (isInner ? 0.85 : 0.55);

        ctx.beginPath();
        ctx.strokeStyle = `rgba(${Math.round(col[0] * 255)},${Math.round(col[1] * 255)},${Math.round(col[2] * 255)},${alpha})`;
        ctx.lineWidth = isInner ? 1.2 : 0.8;

        const steps = 120;
        for (let s = 0; s <= steps; s++) {
          const u = s / steps;

          // Base wave along rotated axis
          const px = u - 0.5;
          const wavey = Math.sin(u * Math.PI * 4 + state.time * speed * 2 + idx * 0.18) * 0.08 * warpIntensity;
          const wave2 = Math.sin(u * Math.PI * 2.5 - state.time * speed + idx * 0.3) * 0.04 * warpIntensity;
          const py = line.offset + wavey + wave2;

          // Mouse warping
          let mx = 0, my = 0;
          if (enableMouseInteraction) {
            const dx = u - state.mouse.x;
            const dy = py + 0.5 - state.mouse.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            const influence = Math.max(0, 1 - dist * 3) * mouseInfluence * 0.04;
            mx = -(state.mouse.x - 0.5) * influence;
            my = -(state.mouse.y - 0.5) * influence;
          }

          // Rotate
          const rx = (px + mx) * cosR - (py + my) * sinR;
          const ry = (px + mx) * sinR + (py + my) * cosR;

          const sx = (rx + 0.5) * W;
          const sy = (ry + 0.5) * H;

          if (s === 0) ctx.moveTo(sx, sy);
          else ctx.lineTo(sx, sy);
        }
        ctx.stroke();
      });
    };

    const buildLines = (count, spread) =>
      Array.from({ length: count }, (_, i) => ({
        offset: (i / (count - 1) - 0.5) * spread,
      }));

    const innerLines = buildLines(innerLineCount, 0.6);
    const outerLines = buildLines(outerLineCount, 1.1);

    const render = () => {
      state.time += 0.016;
      const W = canvas.width;
      const H = canvas.height;

      ctx.clearRect(0, 0, W, H);

      drawLines(outerLines, false);
      drawLines(innerLines, true);

      state.animId = requestAnimationFrame(render);
    };

    state.animId = requestAnimationFrame(render);

    return () => {
      cancelAnimationFrame(state.animId);
      ro.disconnect();
      if (enableMouseInteraction) canvas.removeEventListener('mousemove', onMouseMove);
    };
  }, [
    speed, innerLineCount, outerLineCount, warpIntensity, rotation,
    edgeFadeWidth, colorCycleSpeed, brightness, color1, color2, color3,
    enableMouseInteraction, mouseInfluence,
  ]);

  return <canvas ref={canvasRef} className="line-waves-canvas" />;
};

export default LineWaves;
