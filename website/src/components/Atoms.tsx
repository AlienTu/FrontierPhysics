"use client";

import { useEffect, useRef } from "react";
import "./Atoms.css";

interface AtomsProps {
  direction?: "right" | "left" | "up" | "down" | "diagonal";
  speed?: number;
  /** Stroke colour of the orbits and the nucleus. */
  atomColor?: string;
  /** Spacing of the lattice the atoms sit on. */
  cellSize?: number;
  className?: string;
}

/*
 * Spacetime curvature under the cursor.
 *
 * The pointer acts as a mass sitting on the lattice: nearby atoms fall inward
 * toward it and shrink as they recede into the well, so the even spacing bunches
 * up near the centre and relaxes back to flat further out — the standard
 * rubber-sheet picture of a mass curving spacetime.
 *
 * The deformation is static rather than propagating. It tracks the pointer, and
 * eases in and out as the pointer enters and leaves, instead of radiating.
 */
const WELL_RADIUS = 200; // px — scale over which curvature falls off
const WELL_PULL = 28; // px — deepest inward displacement
const WELL_SHRINK = 0.24; // how much an atom shrinks at the bottom of the well
const FOLLOW_EASE = 0.16; // how quickly the well tracks the pointer
const STRENGTH_EASE = 0.08; // how quickly it eases in and out

/**
 * Renders one atom — a nucleus inside three orbital ellipses, the same glyph as
 * the FrontierPhysics mark — into an offscreen canvas. The animation loop blits
 * this sprite per cell instead of re-stroking three ellipses for every atom on
 * every frame, which keeps a dense full-screen field cheap.
 */
function createAtomSprite(
  color: string,
  cellSize: number,
  dpr: number,
): HTMLCanvasElement {
  const sprite = document.createElement("canvas");
  sprite.width = cellSize * dpr;
  sprite.height = cellSize * dpr;

  const ctx = sprite.getContext("2d");
  if (!ctx) return sprite;

  ctx.scale(dpr, dpr);
  ctx.translate(cellSize / 2, cellSize / 2);
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = 1;

  const rx = cellSize * 0.3;
  const ry = cellSize * 0.125;

  for (const rotation of [0, Math.PI / 3, (2 * Math.PI) / 3]) {
    ctx.beginPath();
    ctx.ellipse(0, 0, rx, ry, rotation, 0, Math.PI * 2);
    ctx.stroke();
  }

  ctx.beginPath();
  ctx.arc(0, 0, cellSize * 0.048, 0, Math.PI * 2);
  ctx.fill();

  return sprite;
}

const Atoms = ({
  direction = "diagonal",
  speed = 0.15,
  atomColor = "#999",
  cellSize = 56,
  className = "",
}: AtomsProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const requestRef = useRef<number | null>(null);
  const gridOffset = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const pointerRef = useRef<{ x: number; y: number; inside: boolean }>({
    x: 0,
    y: 0,
    inside: false,
  });
  const wellRef = useRef<{ x: number; y: number; strength: number }>({
    x: 0,
    y: 0,
    strength: 0,
  });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Cap the ratio at 2 — beyond that the extra pixels cost more than the
    // sharpness is worth for a background this faint.
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const sprite = createAtomSprite(atomColor, cellSize, dpr);
    const reduceMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;

    let width = 0;
    let height = 0;

    const resizeCanvas = () => {
      width = canvas.offsetWidth;
      height = canvas.offsetHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      // Draw in CSS pixels; the transform handles the device ratio.
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    const drawField = () => {
      ctx.clearRect(0, 0, width, height);

      const startX = Math.floor(gridOffset.current.x / cellSize) * cellSize;
      const startY = Math.floor(gridOffset.current.y / cellSize) * cellSize;
      const well = wellRef.current;
      const curved = well.strength > 0.001;

      for (let x = startX; x < width + cellSize; x += cellSize) {
        for (let y = startY; y < height + cellSize; y += cellSize) {
          const cellX = x - (gridOffset.current.x % cellSize);
          const cellY = y - (gridOffset.current.y % cellSize);

          if (!curved) {
            ctx.drawImage(sprite, cellX, cellY, cellSize, cellSize);
            continue;
          }

          const centreX = cellX + cellSize / 2;
          const centreY = cellY + cellSize / 2;
          const dx = centreX - well.x;
          const dy = centreY - well.y;
          const distance = Math.hypot(dx, dy);

          // 1 at the centre of the well, decaying smoothly to 0 far away.
          const depth =
            (WELL_RADIUS * WELL_RADIUS) /
            (distance * distance + WELL_RADIUS * WELL_RADIUS);
          const falling = depth * well.strength;

          // Clamped so an atom is never dragged past the centre and inverted.
          const pull = Math.min(WELL_PULL * falling, distance * 0.8);
          const unitX = distance > 0 ? dx / distance : 0;
          const unitY = distance > 0 ? dy / distance : 0;

          const scale = 1 - WELL_SHRINK * falling;
          const size = cellSize * scale;
          const inset = (cellSize - size) / 2;

          ctx.drawImage(
            sprite,
            cellX - unitX * pull + inset,
            cellY - unitY * pull + inset,
            size,
            size,
          );
        }
      }
    };

    const advanceDrift = () => {
      const effectiveSpeed = Math.max(speed, 0.1);
      switch (direction) {
        case "right":
          gridOffset.current.x =
            (gridOffset.current.x - effectiveSpeed + cellSize) % cellSize;
          break;
        case "left":
          gridOffset.current.x =
            (gridOffset.current.x + effectiveSpeed + cellSize) % cellSize;
          break;
        case "up":
          gridOffset.current.y =
            (gridOffset.current.y + effectiveSpeed + cellSize) % cellSize;
          break;
        case "down":
          gridOffset.current.y =
            (gridOffset.current.y - effectiveSpeed + cellSize) % cellSize;
          break;
        case "diagonal":
          gridOffset.current.x =
            (gridOffset.current.x - effectiveSpeed + cellSize) % cellSize;
          gridOffset.current.y =
            (gridOffset.current.y - effectiveSpeed + cellSize) % cellSize;
          break;
        default:
          break;
      }
    };

    const advanceWell = () => {
      const pointer = pointerRef.current;
      const well = wellRef.current;

      if (pointer.inside && well.strength < 0.001) {
        // Materialise where the pointer already is rather than sliding in from
        // wherever it was last seen.
        well.x = pointer.x;
        well.y = pointer.y;
      } else {
        well.x += (pointer.x - well.x) * FOLLOW_EASE;
        well.y += (pointer.y - well.y) * FOLLOW_EASE;
      }

      const target = pointer.inside ? 1 : 0;
      well.strength += (target - well.strength) * STRENGTH_EASE;
      if (!pointer.inside && well.strength < 0.001) well.strength = 0;
    };

    const updateAnimation = () => {
      advanceDrift();
      advanceWell();
      drawField();
      requestRef.current = requestAnimationFrame(updateAnimation);
    };

    // Tracked on window, not the canvas: the hero's text and buttons sit above
    // the canvas and would otherwise swallow the pointer as it crosses them.
    const handleMouseMove = (event: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      pointerRef.current = {
        x,
        y,
        inside: x >= 0 && x <= rect.width && y >= 0 && y <= rect.height,
      };
    };

    const handleMouseLeave = () => {
      pointerRef.current.inside = false;
    };

    if (reduceMotion) {
      // A single flat frame: no drift, no curvature.
      drawField();
    } else {
      window.addEventListener("mousemove", handleMouseMove, { passive: true });
      document.addEventListener("mouseleave", handleMouseLeave);
      requestRef.current = requestAnimationFrame(updateAnimation);
    }

    return () => {
      window.removeEventListener("resize", resizeCanvas);
      window.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseleave", handleMouseLeave);
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
    };
  }, [direction, speed, atomColor, cellSize]);

  return (
    <canvas ref={canvasRef} className={`atoms-canvas ${className}`}></canvas>
  );
};

export default Atoms;
