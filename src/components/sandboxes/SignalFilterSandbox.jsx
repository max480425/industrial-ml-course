import React, { useState, useEffect, useRef } from 'react';
import { Sliders, RefreshCw, Activity, ShieldAlert, CheckCircle2 } from 'lucide-react';

export const SignalFilterSandbox = () => {
  const [noiseLevel, setNoiseLevel] = useState(0.6);
  const [windowSize, setWindowSize] = useState(7);
  const [spikeFreq, setSpikeFreq] = useState(2);
  const [filterType, setFilterType] = useState('ma'); // 'ma' or 'ema'
  const canvasRef = useRef(null);

  // Generate synthetic signal with noise and spikes
  const pointsCount = 120;
  const generateData = () => {
    const raw = [];
    const baseFreq = 0.05;

    for (let i = 0; i < pointsCount; i++) {
      // Base machine vibration signal (sine wave)
      const base = Math.sin(i * baseFreq * 2 * Math.PI) * 40 + Math.sin(i * baseFreq * 6 * Math.PI) * 15;
      // High frequency electromagnetic noise
      const noise = (Math.random() - 0.5) * 80 * noiseLevel;
      // Impulsive spikes (e.g. electrical arc or loose wire)
      let spike = 0;
      if (spikeFreq > 0 && i % Math.floor(pointsCount / (spikeFreq + 1)) === 0 && i > 0) {
        spike = (Math.random() > 0.5 ? 1 : -1) * 65;
      }
      raw.push(base + noise + spike);
    }

    // Apply filter
    const filtered = [];
    if (filterType === 'ma') {
      const halfWin = Math.floor(windowSize / 2);
      for (let i = 0; i < pointsCount; i++) {
        let sum = 0;
        let count = 0;
        for (let j = -halfWin; j <= halfWin; j++) {
          const idx = i + j;
          if (idx >= 0 && idx < pointsCount) {
            sum += raw[idx];
            count++;
          }
        }
        filtered.push(sum / count);
      }
    } else {
      // EMA with alpha inversely proportional to windowSize
      const alpha = 2 / (windowSize + 1);
      let prev = raw[0];
      filtered.push(prev);
      for (let i = 1; i < pointsCount; i++) {
        const val = alpha * raw[i] + (1 - alpha) * prev;
        filtered.push(val);
        prev = val;
      }
    }

    return { raw, filtered };
  };

  const [data, setData] = useState(generateData);

  useEffect(() => {
    setData(generateData());
  }, [noiseLevel, windowSize, spikeFreq, filterType]);

  // Draw on Canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const centerY = height / 2;

    ctx.clearRect(0, 0, width, height);

    // Industrial Dark Grid
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1;
    for (let x = 0; x < width; x += 40) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = 0; y < height; y += 30) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // Zero-line
    ctx.strokeStyle = '#475569';
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(0, centerY);
    ctx.lineTo(width, centerY);
    ctx.stroke();
    ctx.setLineDash([]);

    const stepX = width / (pointsCount - 1);

    // 1. Draw Raw Noisy Signal (Amber/Red)
    ctx.strokeStyle = '#f87171';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    data.raw.forEach((val, i) => {
      const x = i * stepX;
      const y = centerY - val;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // 2. Draw Filtered Signal (Cyan/Green)
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = '#10b981';
    ctx.shadowBlur = 4;
    ctx.beginPath();
    data.filtered.forEach((val, i) => {
      const x = i * stepX;
      const y = centerY - val;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.shadowBlur = 0;
  }, [data]);

  // Compute live metrics
  const rawVar = data.raw.reduce((acc, v) => acc + Math.pow(v, 2), 0) / pointsCount;
  const filteredVar = data.filtered.reduce((acc, v) => acc + Math.pow(v, 2), 0) / pointsCount;
  const noiseReductionPct = Math.max(0, Math.min(95, Math.round((1 - filteredVar / (rawVar || 1)) * 100)));
  const estimatedLagMs = Math.round(((windowSize - 1) / 2) * 10);

  return (
    <div className="bg-industrial-900 border border-industrial-800 rounded-xl p-5 text-industrial-100 shadow-xl font-sans">
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-industrial-800">
        <div>
          <span className="text-[10px] font-mono uppercase tracking-wider text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
            MOD-01 VISUAL LAB
          </span>
          <h3 className="text-base font-bold text-white mt-1 flex items-center gap-2">
            <Activity className="text-amber-500" size={18} />
            <span>Real-Time Sensor Telemetry & Signal Conditioning</span>
          </h3>
          <p className="text-xs text-industrial-400">
            Raw factory signal (Red) vs Filtered signal (Green). Observe noise rejection vs phase delay.
          </p>
        </div>

        <button
          onClick={() => setData(generateData())}
          className="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-mono bg-industrial-800 hover:bg-industrial-700 text-industrial-200 rounded border border-industrial-700 transition"
        >
          <RefreshCw size={13} />
          <span>Regenerate Stream</span>
        </button>
      </div>

      {/* Main Canvas Screen */}
      <div className="relative mt-4 bg-industrial-950 rounded-lg border border-industrial-800 overflow-hidden shadow-inner">
        <canvas
          ref={canvasRef}
          width={700}
          height={240}
          className="w-full h-56 block"
        />

        {/* Legend Overlay */}
        <div className="absolute top-2.5 right-3 flex items-center gap-3 bg-industrial-900/80 backdrop-blur px-2.5 py-1 rounded border border-industrial-700 text-[11px] font-mono">
          <div className="flex items-center gap-1.5 text-red-400">
            <span className="w-2.5 h-0.5 bg-red-400 inline-block"></span>
            <span>Raw Sensor Signal</span>
          </div>
          <div className="flex items-center gap-1.5 text-emerald-400">
            <span className="w-2.5 h-0.5 bg-emerald-400 inline-block"></span>
            <span>Filtered ({filterType.toUpperCase()})</span>
          </div>
        </div>
      </div>

      {/* Real-time Telemetry Metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Noise Attenuation</div>
          <div className="text-lg font-bold font-mono text-emerald-400">{noiseReductionPct}%</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Phase Lag (Delay)</div>
          <div className="text-lg font-bold font-mono text-amber-400">~{estimatedLagMs} ms</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Filter Window</div>
          <div className="text-lg font-bold font-mono text-cyan-400">N = {windowSize}</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Spike Injections</div>
          <div className="text-lg font-bold font-mono text-rose-400">{spikeFreq} / cycle</div>
        </div>
      </div>

      {/* Interactive Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-5 p-4 bg-industrial-850/60 rounded-lg border border-industrial-800/80">
        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Sensor Noise Amplitude:</span>
            <span className="text-amber-400 font-semibold">{Math.round(noiseLevel * 100)}%</span>
          </div>
          <input
            type="range"
            min="0.0"
            max="1.5"
            step="0.05"
            value={noiseLevel}
            onChange={(e) => setNoiseLevel(parseFloat(e.target.value))}
            className="w-full accent-amber-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Filter Window Size (N):</span>
            <span className="text-emerald-400 font-semibold">{windowSize} samples</span>
          </div>
          <input
            type="range"
            min="3"
            max="25"
            step="2"
            value={windowSize}
            onChange={(e) => setWindowSize(parseInt(e.target.value, 10))}
            className="w-full accent-emerald-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Transient Electrical Spikes:</span>
            <span className="text-rose-400 font-semibold">{spikeFreq}</span>
          </div>
          <input
            type="range"
            min="0"
            max="6"
            step="1"
            value={spikeFreq}
            onChange={(e) => setSpikeFreq(parseInt(e.target.value, 10))}
            className="w-full accent-rose-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="text-xs font-mono mb-1.5 text-industrial-300">Filter Algorithm:</div>
          <div className="flex gap-2">
            <button
              onClick={() => setFilterType('ma')}
              className={`flex-1 py-1.5 px-3 rounded text-xs font-mono transition border ${
                filterType === 'ma'
                  ? 'bg-amber-500/20 text-amber-300 border-amber-500'
                  : 'bg-industrial-800 text-industrial-400 border-industrial-700 hover:text-white'
              }`}
            >
              Moving Average (MA)
            </button>
            <button
              onClick={() => setFilterType('ema')}
              className={`flex-1 py-1.5 px-3 rounded text-xs font-mono transition border ${
                filterType === 'ema'
                  ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500'
                  : 'bg-industrial-800 text-industrial-400 border-industrial-700 hover:text-white'
              }`}
            >
              Exponential (EMA)
            </button>
          </div>
        </div>
      </div>

      {/* Industrial Engineering Insight */}
      <div className="mt-4 p-3 bg-industrial-950/80 border-l-2 border-amber-500 rounded text-xs text-industrial-300 leading-relaxed">
        <span className="font-mono font-bold text-amber-400 uppercase">🏭 Inżynierski Wniosek: </span>
        Zwiększanie okna <span className="font-mono text-white">N</span> idealnie wygładza szum falowników, lecz wprowadza opóźnienie reakcji (phase lag). W szybkich procesach (pakowanie, tłoczenie) nadmierny lag uniemożliwia natychmiastowe zgaszenie zaworu awaryjnego.
      </div>
    </div>
  );
};

export default SignalFilterSandbox;
