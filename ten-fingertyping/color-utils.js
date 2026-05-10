// utils/color.js

export function hexToRgb(hex) {
  hex = hex.replace("#", "");

  return {
    r: parseInt(hex.substring(0, 2), 16),
    g: parseInt(hex.substring(2, 4), 16),
    b: parseInt(hex.substring(4, 6), 16),
  };
}

export function colorizeWhiteImage(hex) {
  const { r, g, b } = hexToRgb(hex);

  const rNorm = r / 255;
  const gNorm = g / 255;
  const bNorm = b / 255;

  const max = Math.max(rNorm, gNorm, bNorm);
  const min = Math.min(rNorm, gNorm, bNorm);

  let h, s, l = (max + min) / 2;

  if (max === min) {
    h = s = 0;
  } else {
    const d = max - min;

    s = l > 0.5
      ? d / (2 - max - min)
      : d / (max + min);

    switch (max) {
      case rNorm:
        h = (gNorm - bNorm) / d + (gNorm < bNorm ? 6 : 0);
        break;

      case gNorm:
        h = (bNorm - rNorm) / d + 2;
        break;

      case bNorm:
        h = (rNorm - gNorm) / d + 4;
        break;
    }

    h *= 60;
  }

  return `
    brightness(0)
    saturate(100%)
    invert(100%)
    sepia(100%)
    saturate(5000%)
    hue-rotate(${h}deg)
    brightness(${l * 2})
  `;
}

window.colorUtils = {
  hexToRgb,
  colorizeWhiteImage
};