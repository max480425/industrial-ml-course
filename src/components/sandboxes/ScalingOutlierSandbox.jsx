import React, { useState, useMemo } from 'react';
import { Sliders, RefreshCw, BarChart2, AlertOctagon } from 'lucide-react';

export const ScalingOutlierSandbox = () => {
  const [contamination, setContamination] = useState(10); // % outliers
  const [spikeMultiplier, setSpikeMultiplier] = useState(8); // x times normal
  const [scalerType, setScalerType] = useState('robust'); // 'robust', 'standard', 'minmax'
  const [seed, setSeed] = useState(42);

  // Generate synthetic baseline normal operations + outliers
  const rawData = useMemo(() => {
    const points = [];
    const count = 100;
    const outlierCount = Math.floor((count * contamination) / 100);

    // Normal machine currents (around 25A +/- 4A)
    for (let i = 0; i < count - outlierCount; i++) {
      const u1 = Math.random();
      const u2 = Math.random();
      const z0 = Math.sqrt(-2.0 * Math.log(u1 || 0.0001)) * Math.cos(2.0 * Math.PI * u2);
      const val = 25 + z0 * 3.5;
      points.push({ val: Math.max(12, val), isOutlier: false });
    }

    // Industrial electrical spikes (e.g. arc flash or startup transient: 100A - 250A)
    for (let i = 0; i < outlierCount; i++) {
      const val = 25 * spikeMultiplier + (Math.random() - 0.5) * 30;
      points.push({ val, isOutlier: true });
    }

    // Sort values for quartile analysis
    return points.sort((a, b) => a.val - b.val);
  }, [contamination, spikeMultiplier, seed]);

  // Compute statistics
  const stats = useMemo(() => {
    const vals = rawData.map(d => d.val);
    const n = vals.length;
    const mean = vals.reduce((a, b) => a + b, 0) / n;
    const variance = vals.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / n;
    const std = Math.sqrt(variance);

    const median = vals[Math.floor(n * 0.5)];
    const q1 = vals[Math.floor(n * 0.25)];
    const q3 = vals[Math.floor(n * 0.75)];
    const iqr = q3 - q1;
    const min = vals[0];
    const max = vals[n - 1];

    return { mean, std, median, q1, q3, iqr, min, max };
  }, [rawData]);

  // Apply chosen scaler
  const scaledData = useMemo(() => {
    return rawData.map(d => {
      let scaled = 0;
      if (scalerType === 'standard') {
        scaled = (d.val - stats.mean) / (stats.std || 1);
      } else if (scalerType === 'robust') {
        scaled = (d.val - stats.median) / (stats.iqr || 1);
      } else {
        // minmax
        scaled = (d.val - stats.min) / ((stats.max - stats.min) || 1);
      }
      return { ...d, scaled };
    });
  }, [rawData, scalerType, stats]);

  // Compute span of normal operating data in scaled space
  const normalScaledSpan = useMemo(() => {
    const normalScaled = scaledData.filter(d => !d.isOutlier).map(d => d.scaled);
    const min = Math.min(...normalScaled);
    const max = Math.max(...normalScaled);
    return Math.abs(max - min).toFixed(2);
  }, [scaledData]);

  return (
    <div className="bg-industrial-900 border border-industrial-800 rounded-xl p-5 text-industrial-100 shadow-xl font-sans">
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-industrial-800">
        <div>
          <span className="text-[10px] font-mono uppercase tracking-wider text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20">
            MOD-02 VISUAL LAB
          </span>
          <h3 className="text-base font-bold text-white mt-1 flex items-center gap-2">
            <BarChart2 className="text-cyan-500" size={18} />
            <span>RobustScaler vs StandardScaler under Extreme Spikes</span>
          </h3>
          <p className="text-xs text-industrial-400">
            Compare how extreme motor current spikes distort StandardScaler vs how RobustScaler preserves resolution.
          </p>
        </div>

        <button
          onClick={() => setSeed(s => s + 1)}
          className="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-mono bg-industrial-800 hover:bg-industrial-700 text-industrial-200 rounded border border-industrial-700 transition"
        >
          <RefreshCw size={13} />
          <span>Resample Data</span>
        </button>
      </div>

      {/* Distribution Visualizer Canvas/SVG */}
      <div className="mt-4 p-4 bg-industrial-950 rounded-lg border border-industrial-800">
        <div className="flex justify-between items-center text-xs font-mono mb-2">
          <span className="text-industrial-400">Scaled Value Distribution (100 Samples):</span>
          <span className="text-cyan-400 font-bold uppercase">
            Active: {scalerType.toUpperCase()} SCALER
          </span>
        </div>

        {/* Scatter 1D distribution */}
        <div className="relative h-20 w-full bg-industrial-900/80 rounded border border-industrial-800 overflow-hidden flex items-center px-4">
          {/* Center line */}
          <div className="absolute inset-x-0 h-0.5 bg-industrial-700"></div>

          {/* Points */}
          {scaledData.map((d, i) => {
            // Map scaled value to 0-100% horizontal position
            let pct = 50;
            if (scalerType === 'standard') {
              pct = 50 + (d.scaled / (spikeMultiplier + 1)) * 45;
            } else if (scalerType === 'robust') {
              pct = 40 + (d.scaled / (spikeMultiplier * 4)) * 55;
            } else {
              pct = d.scaled * 95 + 2.5;
            }
            pct = Math.max(2, Math.min(98, pct));

            return (
              <div
                key={i}
                style={{ left: `${pct}%` }}
                className={`absolute w-2 h-2 -ml-1 rounded-full transition-all duration-300 ${
                  d.isOutlier
                    ? 'bg-rose-500 shadow-md shadow-rose-500/50 ring-2 ring-rose-400/40 z-20'
                    : 'bg-emerald-400/80 hover:bg-emerald-300 z-10'
                }`}
                title={`${d.isOutlier ? 'OUTLIER SPIKE' : 'Normal Part'}: ${d.val.toFixed(1)}A (Scaled: ${d.scaled.toFixed(2)})`}
              />
            );
          })}
        </div>

        {/* Legend */}
        <div className="flex items-center justify-between text-[11px] font-mono mt-2 text-industrial-400">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1 text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block"></span> Normal Telemetry (25A)
            </span>
            <span className="flex items-center gap-1 text-rose-400">
              <span className="w-2 h-2 rounded-full bg-rose-500 inline-block"></span> Severe Outlier ({Math.round(25 * spikeMultiplier)}A)
            </span>
          </div>
          <div>
            Normal Data Spread: <span className="text-white font-bold">{normalScaledSpan}</span> units
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Mean vs Median</div>
          <div className="text-sm font-mono text-industrial-200 mt-1">
            <span className="text-amber-400 font-bold">{stats.mean.toFixed(1)}</span> / {stats.median.toFixed(1)}
          </div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">StdDev vs IQR</div>
          <div className="text-sm font-mono text-industrial-200 mt-1">
            <span className="text-amber-400 font-bold">{stats.std.toFixed(1)}</span> / {stats.iqr.toFixed(1)}
          </div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Outlier Ratio</div>
          <div className="text-sm font-mono text-rose-400 font-bold mt-1">{contamination}%</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Scaling Diagnosis</div>
          <div className="text-sm font-mono font-bold mt-1 text-emerald-400">
            {scalerType === 'robust' ? 'Robust (IQR immune)' : 'Vulnerable to Spikes'}
          </div>
        </div>
      </div>

      {/* Scaler Selection & Controls */}
      <div className="mt-5 p-4 bg-industrial-850/60 rounded-lg border border-industrial-800/80 space-y-4">
        <div>
          <div className="text-xs font-mono mb-2 text-industrial-300">Choose Scaler Algorithm:</div>
          <div className="grid grid-cols-3 gap-2">
            <button
              onClick={() => setScalerType('robust')}
              className={`py-2 px-2 rounded text-xs font-mono transition border text-center ${
                scalerType === 'robust'
                  ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500 font-bold'
                  : 'bg-industrial-800 text-industrial-400 border-industrial-700 hover:text-white'
              }`}
            >
              RobustScaler (Median/IQR)
            </button>
            <button
              onClick={() => setScalerType('standard')}
              className={`py-2 px-2 rounded text-xs font-mono transition border text-center ${
                scalerType === 'standard'
                  ? 'bg-amber-500/20 text-amber-300 border-amber-500 font-bold'
                  : 'bg-industrial-800 text-industrial-400 border-industrial-700 hover:text-white'
              }`}
            >
              StandardScaler (Z-Score)
            </button>
            <button
              onClick={() => setScalerType('minmax')}
              className={`py-2 px-2 rounded text-xs font-mono transition border text-center ${
                scalerType === 'minmax'
                  ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500 font-bold'
                  : 'bg-industrial-800 text-industrial-400 border-industrial-700 hover:text-white'
              }`}
            >
              MinMaxScaler [0, 1]
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <div className="flex justify-between text-xs font-mono mb-1.5">
              <span className="text-industrial-300">Outlier Contamination Rate:</span>
              <span className="text-rose-400 font-semibold">{contamination}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="25"
              step="1"
              value={contamination}
              onChange={(e) => setContamination(parseInt(e.target.value, 10))}
              className="w-full accent-rose-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs font-mono mb-1.5">
              <span className="text-industrial-300">Spike Magnitude:</span>
              <span className="text-amber-400 font-semibold">{spikeMultiplier}x normal</span>
            </div>
            <input
              type="range"
              min="2"
              max="15"
              step="1"
              value={spikeMultiplier}
              onChange={(e) => setSpikeMultiplier(parseInt(e.target.value, 10))}
              className="w-full accent-amber-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
            />
          </div>
        </div>
      </div>

      {/* Industrial Engineering Insight */}
      <div className="mt-4 p-3 bg-industrial-950/80 border-l-2 border-cyan-500 rounded text-xs text-industrial-300 leading-relaxed">
        <span className="font-mono font-bold text-cyan-400 uppercase">🏭 Inżynierski Wniosek: </span>
        Przełącz na <span className="font-mono text-amber-300">StandardScaler</span> i zobacz, jak pojedynczy pik rozruchowy silnika spłaszcza 90% normalnych pomiarów w wąską kreskę o szerokości zaledwie {scalerType === 'standard' ? normalScaledSpan : '0.1'}. <span className="font-mono text-emerald-300">RobustScaler</span> zachowuje pełną rozdzielczość sygnału roboczego.
      </div>
    </div>
  );
};

export default ScalingOutlierSandbox;
