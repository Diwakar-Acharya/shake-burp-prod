# Visual Design & React Bits Specification - Shake & Burp

This document serves as the official visual design, UX specification, and **React Bits MCP Server Integration Guide** for the **Shake & Burp** cold-redded luxury shaker bottle ecommerce platform.

---

## 1. Executive Design Vision

**Shake & Burp** delivers a stealth, cold, luxury aesthetic. Built for modern fitness enthusiasts and athletes, the design blends futuristic industrial styling with high-performance motion graphics.

### Design Archetype & Aesthetics
- **Aesthetic Tone:** Cold, Stealth, Refined, Minimalist, High-Contrast Crimson & Carbon.
- **Inspirations:** 
  - **Nothing & Apple:** Grid discipline, spatial typography, stark minimalist layouts.
  - **Razer & Tesla:** Performance tactical surfaces, matte dark carbon, glowing cold-red accents.
  - **Gymshark & Nike:** Athletic intensity, bold headlines, studio product showcases.
- **Strict Avoidance:** Cartoonish badges, generic card grids, excessive rainbow gradients, non-brand pastels.

---

## 2. Antigravity React Bits MCP Server Workflow

Antigravity uses the `react-bits` MCP server to discover, analyze, install, and generate code for React Bits background components and micro-animations.

### Available MCP Server Tools
- `search-react-bits-components`: Query available components by category or tag.
- `get-react-bits-component`: Inspect props, default configurations, and source code.
- `analyze-frontend-code`: Evaluate existing component performance and visual cohesion.
- `recommend-animations`: Get AI recommendations for optimal motion design per user persona.
- `generate-integration-code`: Generate ready-to-use React / Tailwind code wrappers.

### Integration Workflow
1. **Search & Inspect:** Query `react-bits` via MCP for targeted component schemas.
2. **Install Component:** Execute `npx shadcn@latest add @react-bits/<component-name>` to pull component code directly into `@/components/react-bits/`.
3. **Configure & Layer:** Position animation canvas as a fixed/absolute background (`z-0` or `z-[-1]`) behind glassmorphic container UI (`z-10`).
4. **Tune Parameters:** Match the cold crimson palette (`#ff0000`, `#a00000`, `#3d0000`, `#6a0000`, `#dd0000`).

---

## 3. Cold Red Color System

All color tokens are engineered around deep black matte surfaces, steel greys, and high-energy cold blood red accents.

| Token Name | Hex / CSS Value | Description & Purpose |
| :--- | :--- | :--- |
| **Primary Background** | `#070707` | Deepest matte black surface |
| **Secondary Background** | `#0F0F10` | Dark metallic carbon grey |
| **Surface Card** | `#151515` | Elevated tactical container |
| **Primary Crimson Accent** | `#FF0000` / `#D10000` | Cold, vibrant blood red for active CTAs & beams |
| **Deep Red Glow** | `#6A0000` | Shadow ambient glow & sub-button depth |
| **Dark Crimson Base** | `#3D0000` / `#4D0000` | Background fluid layer & ray falloffs |
| **Accent White** | `#F8F8F8` | Crisp non-glare off-white primary text |
| **Muted Steel** | `#B8B8B8` | Neutral secondary copy & metadata |
| **Glass Border Muted** | `rgba(255, 255, 255, 0.08)` | Ultra-thin structural borders |
| **Glass Border Red Hover** | `rgba(255, 0, 0, 0.35)` | Glowing red outlines on focus/hover |

---

## 4. React Bits Component Mapping & Page Specifications

React Bits components are integrated as interactive background layers behind foreground content.

```
+-------------------------------------------------------------+
|  Layer 3 (Foreground): Content, Headers, Buttons, Products   |
|  Layer 2 (Middle): Glassmorphic Card (blur-16px, bg-black/40)|
|  Layer 1 (Background): React Bits Canvas Animation           |
+-------------------------------------------------------------+
```

---

### A. Homepage (Hero Section)

**Component:** `@react-bits/Beams-JS-CSS`  
**Concept:** Moving luxury laser rays cutting through deep matte space.

#### CLI Installation
```bash
npx shadcn@latest add @react-bits/Beams-JS-CSS
```

#### JSX Implementation Snippet
```tsx
import Beams from "@/components/react-bits/Beams";

export default function HeroBackground() {
  return (
    <div style={{ width: '100%', height: '100vh', position: 'relative', overflow: 'hidden' }}>
      <Beams
        beamWidth={2}
        beamHeight={15}
        beamNumber={12}
        lightColor="#ff0000"
        speed={3.9}
        noiseIntensity={2}
        scale={0.25}
        rotation={-50}
      />
    </div>
  );
}
```

---

### B. Auth Pages (Login & Signup)

**Component:** `@react-bits/Dither-JS-CSS`  
**Concept:** High-tech retro-futuristic dithered crimson wave matrix.

#### CLI Installation
```bash
npx shadcn@latest add @react-bits/Dither-JS-CSS
```

#### JSX Implementation Snippet
```tsx
import Dither from "@/components/react-bits/Dither";

export default function AuthBackground() {
  return (
    <div style={{ width: '100%', height: '100vh', position: 'relative' }}>
      <Dither
        waveColor={[0.5137254901960784, 0, 0]}
        disableAnimation={false}
        enableMouseInteraction
        mouseRadius={0.8}
        colorNum={6}
        pixelSize={1}
        waveAmplitude={0.4}
        waveFrequency={3}
        waveSpeed={0.02}
      />
    </div>
  );
}
```

---

### C. Shaker Product Catalog & Customizer Buying Section

**Component:** `@react-bits/Ferrofluid-JS-CSS`  
**Concept:** Reactive magnetic crimson fluid simulating liquid inside high-performance shaker bottles.

#### CLI Installation
```bash
npx shadcn@latest add @react-bits/Ferrofluid-JS-CSS
```

#### JSX Implementation Snippet
```tsx
import Ferrofluid from "@/components/react-bits/Ferrofluid";

export default function ProductBuyingBackground() {
  return (
    <div style={{ width: '100%', height: '100%', minHeight: '800px', position: 'relative' }}>
      <Ferrofluid
        colors={["#a00000", "#ff0000", "#3d0000"]}
        speed={0.5}
        scale={1.2}
        turbulence={1.5}
        fluidity={0.1}
        rimWidth={0.23}
        sharpness={1.6}
        shimmer={1.15}
        glow={1.3}
        flowDirection="up"
        opacity={1}
        mouseInteraction
        mouseStrength={1.2}
        mouseRadius={0.35}
      />
    </div>
  );
}
```

---

### D. Static & Legal Pages (Error, Privacy, Terms)

**Component:** `@react-bits/SideRays-JS-CSS`  
**Concept:** Tactical corner side rays providing subtle ambient illumination.

#### CLI Installation
```bash
npx shadcn@latest add @react-bits/SideRays-JS-CSS
```

#### JSX Implementation Snippet
```tsx
import SideRays from "@/components/react-bits/SideRays";

export default function LegalPagesBackground() {
  return (
    <div style={{ width: '100%', height: '100vh', position: 'relative' }}>
      <SideRays
        rayColor1="#ff0404"
        rayColor2="#4d0000"
        origin="top-right"
        speed={1.8}
        intensity={3}
        spread={1.9}
        tilt={4}
        saturation={2}
        blend={0.73}
        falloff={1.6}
        opacity={1}
      />
    </div>
  );
}
```

---

### E. FAQs, Contact & Secondary Content Pages

**Component:** `@react-bits/LightRays-JS-CSS`  
**Concept:** Top-centered pulsating light rays generating depth across body text.

#### CLI Installation
```bash
npx shadcn@latest add @react-bits/LightRays-JS-CSS
```

#### JSX Implementation Snippet
```tsx
import LightRays from "@/components/react-bits/LightRays";

export default function InfoPageBackground() {
  return (
    <div style={{ width: '100%', height: '100vh', position: 'relative' }}>
      <LightRays
        raysOrigin="top-center"
        raysColor="#dd0000"
        raysSpeed={2.4}
        lightSpread={2.1}
        rayLength={3.3}
        pulsating={false}
        fadeDistance={0.9}
        saturation={1.5}
        followMouse
        mouseInfluence={0.25}
        noiseAmount={0}
        distortion={0}
      />
    </div>
  );
}
```

---

## 5. Typography System

- **Headings (Display):** `Space Grotesk` (Geometric, futuristic, wide posture)
- **Body Text:** `Inter` (Neutral, ultra-legible, crisp line rendering)
- **Monospace Elements (Pricing & Specs):** `JetBrains Mono` (Technical precision)

### Scale Reference
- **Hero Title:** `Space Grotesk`, `700 (Bold)`, `clamp(3.5rem, 9vw, 7rem)`, tracking `-0.05em`, leading `0.95`.
- **H1 Section Title:** `Space Grotesk`, `700 (Bold)`, `clamp(2.25rem, 5vw, 3.75rem)`, tracking `-0.03em`.
- **Body Regular:** `Inter`, `400 (Regular)`, `15px`, color `#B8B8B8`.
- **Price Badges:** `JetBrains Mono`, `600 (SemiBold)`, `20px`, color `#FF0000`.

---

## 6. Glassmorphism & UI Component Styling

### Tailwind Utility Classes
```css
/* Glass Card Container */
.glass-panel {
  background: rgba(15, 15, 15, 0.45);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

/* Glass Interactive Button */
.glass-btn {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.glass-btn:hover {
  background: rgba(255, 0, 0, 0.15);
  border-color: rgba(255, 0, 0, 0.4);
  box-shadow: inset 0 0 0 1px rgba(255, 0, 0, 0.2), 0 0 30px rgba(255, 0, 0, 0.25);
  transform: translateY(-2px);
}
```

---

## 7. Performance & Optimization Guidelines

1. **Lazy Loading & Viewport Observer:** React Bits WebGL/Canvas components (`Ferrofluid`, `Beams`) automatically suspend rendering (`cancelAnimationFrame`) when out of viewport.
2. **Reduced Motion Compliance:** When `@media (prefers-reduced-motion: reduce)` is true, canvas animations are safely disabled and replaced with solid matte gradient overlays.
3. **Layer Isolation:** Background canvas containers use CSS `will-change: transform` and `pointer-events: none` to guarantee 60fps scrolling and uninhibited clicks on foreground elements.
