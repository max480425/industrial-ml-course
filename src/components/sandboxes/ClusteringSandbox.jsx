import React, { useState, useMemo, useRef, useEffect } from 'react';
import { Sliders, RefreshCw, Cpu, AlertCircle, Crosshair } from 'lucide-react';

export const ClusteringSandbox = () => {
  const [numClusters, setNumClusters] = useState(3);
  const [anomalyCount, setAnomalyCount] = useState(4);
  const [thresholdRadius, setThresholdRadius] = useState(55);
  const [dispersion, setDispersion] = useState(18);
  const [seed, setSeed] = useState(1);
  const canvasRef = useRef(null);

  // Predefined realistic machine operating modes:
  // Mode 1: Idle (RPM: 200, Current: 5A)
  // Mode 2: Tool Warmup (RPM: 1200, Current: 15A)
  // Mode 3: Nominal Milling (RPM: 2800, Current: 32A)
  // Mode 4: Heavy Roughing (RPM: 2200, Current: 58A)
  // Mode 5: High Speed Finishing (RPM: 4500, Current: 40A)
  const regimePrototypes = [
    { label: 'Idle Standby', x: 70, y: 50, color: '#38bdf8' },
    { label: 'Warmup Spindle', x: 190, y: 120, color: '#34d399' },
    { label: 'Nominal Milling', x: 380, y: 220, color: '#fbbf24' },
    { label: 'Heavy Roughing', x: 310, y: 340, color: '#a78bfa' },
    { label: 'High Speed Polish', x: 540, y: 270, color: '#f472b6' },
  ];

  const activePrototypes = regimePrototypes.slice(0, numClusters);

  // Generate synthetic points around active regime centers
  const points = useMemo(() => {
    const pts = [];
    const ptsPerCluster = 35;

    activePrototypes.forEach((proto, cIdx) => {
      for (let i = 0; i < ptsPerCluster; i++) {
        const angle = Math.random() * 2 * Math.PI;
        const dist = Math.sqrt(Math.random()) * dispersion;
        const x = proto.x + Math.cos(angle) * dist * 1.5;
        const y = proto.y + Math.sin(angle) * dist;
        pts.push({ x, y, cluster: cIdx, isAnomaly: false });
      }
    });

    // Inject unmodeled anomalies (e.g. tool chatter, bearing seizure: abnormal RPM/Current pairs)
    for (let i = 0; i < anomalyCount; i++) {
      const x = 100 + Math.random() * 450;
      const y = 80 + Math.random() * 280;
      pts.push({ x, y, cluster: -1, isAnomaly: true });
    }

    return pts;
  }, [numClusters, anomalyCount, dispersion, seed]);

  // Compute cluster centroids
  const centroids = useMemo(() => {
    const centers = [];
    for (let c = 0; c < numClusters; c++) {
      const cPts = points.filter(p => p.cluster === c);
      if (cPts.length > 0) {
        const avgX = cPts.reduce((a, b) => a + b.x, 0) / cPts.length;
        const avgY = cPts.reduce((a, b) => a + b.y, 0) / cPts.length;
        centers.push({ x: avgX, y: avgY, label: activePrototypes[c].label, color: activePrototypes[c].color });
      }
    }
    return centers;
  }, [points, numClusters]);

  // Classify points based on distance to nearest centroid
  const classifiedPoints = useMemo(() => {
    return points.map(p => {
      let minDist = Infinity;
      let nearestCluster = 0;

      centroids.forEach((c, idx) => {
        const d = Math.hypot(p.x - c.x, p.y - c.y);
        if (d < minDist) {
          minDist = d;
          nearestCluster = idx;
        }
      });

      const flaggedAsAnomaly = minDist > thresholdRadius;
      return { ...p, assignedCluster: nearestCluster, dist: minDist, flagged: flaggedAsAnomaly };
    });
  }, [points, centroids, thresholdRadius]);

  const flaggedAnomalies = classifiedPoints.filter(p => p.flagged).length;

  // Draw 2D Phase Diagram
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    // Industrial Dark Background Grid
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1;
    for (let x = 0; x < width; x += 50) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = 0; y < height; y += 40) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // Centroid Acceptance Radii
    centroids.forEach((c) => {
      ctx.strokeStyle = `${c.color}30`;
      ctx.fillStyle = `${c.color}08`;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(c.x, height - c.y, thresholdRadius, 0, 2 * Math.PI);
      ctx.fill();
      ctx.stroke();
    });

    // Draw Points
    classifiedPoints.forEach((p) => {
      const canvasY = height - p.y;
      if (p.flagged) {
        // Red glowing anomaly halo
        ctx.fillStyle = '#ef4444';
        ctx.strokeStyle = '#f87171';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(p.x, canvasY, 6, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();

        ctx.strokeStyle = '#ef444460';
        ctx.beginPath();
        ctx.arc(p.x, canvasY, 11, 0, 2 * Math.PI);
        ctx.stroke();
      } else {
        const clusterColor = activePrototypes[p.assignedCluster]?.color || '#94a3b8';
        ctx.fillStyle = clusterColor;
        ctx.beginPath();
        ctx.arc(p.x, canvasY, 4, 0, 2 * Math.PI);
        ctx.fill();
      }
    });

    // Draw Centroids with Crosshairs
    centroids.forEach((c) => {
      const cy = height - c.y;
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = c.color;
      ctx.lineWidth = 2.5;

      // Circle
      ctx.beginPath();
      ctx.arc(c.x, cy, 7, 0, 2 * Math.PI);
      ctx.fill();
      ctx.stroke();

      // Crosshairs
      ctx.beginPath();
      ctx.moveTo(c.x - 12, cy);
      ctx.lineTo(c.x + 12, cy);
      ctx.moveTo(c.x, cy - 12);
      ctx.lineTo(c.x, cy + 12);
      ctx.stroke();

      // Label
      ctx.fillStyle = '#cbd5e1';
      ctx.font = '10px monospace';
      ctx.fillText(c.label, c.x + 12, cy - 8);
    });
  }, [classifiedPoints, centroids, thresholdRadius, activePrototypes]);

  return (
    <div className="bg-industrial-900 border border-industrial-800 rounded-xl p-5 text-industrial-100 shadow-xl font-sans">
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-industrial-800">
        <div>
          <span className="text-[10px] font-mono uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
            MOD-04 VISUAL LAB
          </span>
          <h3 className="text-base font-bold text-white mt-1 flex items-center gap-2">
            <Cpu className="text-emerald-500" size={18} />
            <span>Operational Regime Clustering & Anomaly Envelope</span>
          </h3>
          <p className="text-xs text-industrial-400">
            X: Spindle Speed (RPM) vs Y: Motor Current (Amps). Points outside regime envelopes are isolated as zero-shot anomalies.
          </p>
        </div>

        <button
          onClick={() => setSeed(s => s + 1)}
          className="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-mono bg-industrial-800 hover:bg-industrial-700 text-industrial-200 rounded border border-industrial-700 transition"
        >
          <RefreshCw size={13} />
          <span>Resimulate Shifts</span>
        </button>
      </div>

      {/* Main Canvas Phase Plane */}
      <div className="relative mt-4 bg-industrial-950 rounded-lg border border-industrial-800 overflow-hidden shadow-inner">
        <canvas
          ref={canvasRef}
          width={640}
          height={380}
          className="w-full h-72 block"
        />

        {/* Axis Labels */}
        <div className="absolute bottom-2 left-4 text-[10px] font-mono text-industrial-400">
          X: Spindle Speed [RPM] →
        </div>
        <div className="absolute top-3 left-4 text-[10px] font-mono text-industrial-400">
          ↑ Y: Motor Current [Amps]
        </div>

        {/* Legend */}
        <div className="absolute top-2 right-2 bg-industrial-900/90 backdrop-blur p-2 rounded border border-industrial-800 text-[10px] font-mono space-y-1">
          <div className="text-industrial-400 font-bold uppercase mb-1">Operating Regimes (K={numClusters}):</div>
          {activePrototypes.map((proto, idx) => (
            <div key={idx} className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: proto.color }}></span>
              <span>{proto.label}</span>
            </div>
          ))}
          <div className="flex items-center gap-1.5 text-red-400 pt-1 border-t border-industrial-800">
            <span className="w-2.5 h-2.5 rounded-full bg-red-500"></span>
            <span>Flagged Anomaly ({flaggedAnomalies})</span>
          </div>
        </div>
      </div>

      {/* Live Metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Active Regimes (K)</div>
          <div className="text-lg font-bold font-mono text-emerald-400">{numClusters} clusters</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Enclosed Normal Points</div>
          <div className="text-lg font-bold font-mono text-cyan-400">{classifiedPoints.length - flaggedAnomalies}</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Isolated Anomalies</div>
          <div className="text-lg font-bold font-mono text-rose-400">{flaggedAnomalies} events</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Threshold Radius (R)</div>
          <div className="text-lg font-bold font-mono text-amber-400">{thresholdRadius} units</div>
        </div>
      </div>

      {/* Sliders */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-5 p-4 bg-industrial-850/60 rounded-lg border border-industrial-800/80">
        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Operational Clusters (K):</span>
            <span className="text-emerald-400 font-bold">{numClusters} regimes</span>
          </div>
          <input
            type="range"
            min="2"
            max="5"
            step="1"
            value={numClusters}
            onChange={(e) => setNumClusters(parseInt(e.target.value, 10))}
            className="w-full accent-emerald-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Anomaly Envelope Radius:</span>
            <span className="text-amber-400 font-bold">{thresholdRadius} px</span>
          </div>
          <input
            type="range"
            min="30"
            max="90"
            step="5"
            value={thresholdRadius}
            onChange={(e) => setThresholdRadius(parseInt(e.target.value, 10))}
            className="w-full accent-amber-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Inject Unmodeled Anomaly Outliers:</span>
            <span className="text-rose-400 font-bold">{anomalyCount}</span>
          </div>
          <input
            type="range"
            min="0"
            max="12"
            step="1"
            value={anomalyCount}
            onChange={(e) => setAnomalyCount(parseInt(e.target.value, 10))}
            className="w-full accent-rose-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Process Load Variance (Dispersion):</span>
            <span className="text-cyan-400 font-bold">{dispersion}</span>
          </div>
          <input
            type="range"
            min="8"
            max="35"
            step="2"
            value={dispersion}
            onChange={(e) => setDispersion(parseInt(e.target.value, 10))}
            className="w-full accent-cyan-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>
      </div>

      {/* Industrial Engineering Insight */}
      <div className="mt-4 p-3 bg-industrial-950/80 border-l-2 border-emerald-500 rounded text-xs text-industrial-300 leading-relaxed">
        <span className="font-mono font-bold text-emerald-400 uppercase">🏭 Inżynierski Wniosek: </span>
        Uczenie nienadzorowane dzieli pracę obrabiarki na stany operacyjne bez konieczności ręcznego etykietowania. Każdy punkt leżący poza okręgami tolerancji (czerwone punkty) to natychmiastowe ostrzeżenie: silnik pobiera nienaturalny prąd w stosunku do swoich obrotów (np. zatarty frez lub zakleszczona prowadnica).
      </div>
    </div>
  );
};

export default ClusteringSandbox;
