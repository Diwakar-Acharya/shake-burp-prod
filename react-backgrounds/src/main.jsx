import React from 'react';
import { createRoot } from 'react-dom/client';
import Beams from './Beams/Beams';
import Dither from './Dither/Dither';
import Ferrofluid from './Ferrofluid/Ferrofluid';
import SideRays from './SideRays/SideRays';
import LightRays from './LightRays/LightRays';
import BlurText from './BlurText/BlurText';
import FuzzyText from './FuzzyText/FuzzyText';
import GradualBlur from './GradualBlur/GradualBlur';
import CircularGallery from './CircularGallery/CircularGallery';
import LineWaves from './LineWaves/LineWaves';

window.ReactBackgrounds = {
  renderBeams(elId, props) {
    const el = document.getElementById(elId);
    if (el) {
      createRoot(el).render(<Beams {...props} />);
    }
  },
  renderDither(elId, props) {
    const el = document.getElementById(elId);
    if (el) {
      createRoot(el).render(<Dither {...props} />);
    }
  },
  renderFerrofluid(elId, props) {
    const el = document.getElementById(elId);
    if (el) {
      createRoot(el).render(<Ferrofluid {...props} />);
    }
  },
  renderSideRays(elId, props) {
    const el = document.getElementById(elId);
    if (el) {
      createRoot(el).render(<SideRays {...props} />);
    }
  },
  renderLightRays(elId, props) {
    const el = document.getElementById(elId);
    if (el) {
      createRoot(el).render(<LightRays {...props} />);
    }
  },
  renderBlurText(elId, props) {
    const el = document.getElementById(elId);
    if (el) {
      createRoot(el).render(<BlurText {...props} />);
    }
  },
  renderFuzzyText(elId, props) {
    const el = document.getElementById(elId);
    if (el) {
      createRoot(el).render(<FuzzyText {...props} />);
    }
  },
  renderGradualBlur(elId, props) {
    const el = document.getElementById(elId);
    if (el) {
      createRoot(el).render(<GradualBlur {...props} />);
    }
  },
  renderCircularGallery(elId, props) {
    const el = document.getElementById(elId);
    if (el) {
      createRoot(el).render(<CircularGallery {...props} />);
    }
  },
  renderLineWaves(elId, props) {
    const el = document.getElementById(elId);
    if (el) {
      createRoot(el).render(<LineWaves {...props} />);
    }
  }
};
