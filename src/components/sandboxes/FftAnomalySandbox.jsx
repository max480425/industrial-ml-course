import React, { useState, useMemo, useRef, useEffect } from 'react';
import { Sliders, RefreshCw, Radio, AlertTriangle, ShieldCheck } from 'lucide-react';

export const FftAnomalySandbox = () => {
  const [rpm, setRpm] = useState(1800); // 30 Hz shaft rotation
  const [defectSeverity, setDefectSeverity] = useState(45); // 0% to 100%
  const [noiseLevel, setNoiseLevel] = useState(25); // %
  const [useHanning, setUseHanning] = useState(true);
  const canvasRef = useRef(null);

  // Derived kinematics
  const fShaft = rpm / 60; // 1X rotational frequency (e.g. 30 Hz)
  const fHarmonic = fShaft * 2; // 2X harmonic (e.g. 60 Hz)
  // Characteristic BPFO (Ball Pass Frequency Outer race) for typical 6205 bearing = 3.58 * fShaft
  const fBPFO = fShaft * 3.58; // e.g. 107.4 Hz

  // Compute Time Domain and simulated discrete FFT spectrum
  const { timeSignal, spectrum, alarmTriggered } = useMemo(() => {
    const nSamples = 256;
    const samplingRate = 800; // Hz
    const dt = 1 / samplingRate;
    const time = [];
    const timeSignal = [];

    for (let i = 0; i < nSamples; i++) {
      const t = i * dt;
      time.push(t);

      // Shaft unbalance 1X
      const s1 = Math.sin(2 * Math.PI * fShaft * t) * 1.8;
      // 2X harmonic
      const s2 = Math.sin(2 * Math.PI * fHarmonic * t) * 0.7;
      // Bearing BPFO sharp impact pulses
      const bpfoAmp = (defectSeverity / 100) * 3.8;
      const sBPFO = Math.sin(2 * Math.PI * fBPFO * t) * bpfoAmp;
      // Random noise
      const noise = (Math.random() - 0.5) * (noiseLevel / 100) * 4.0;

      timeSignal.push(s1 + s2 + sBPFO + noise);
    }

    // Discrete FFT magnitude calculation
    const spectrum = [];
    const maxFreq = 400; // Hz
    const freqStep = 2; // Hz

    for (let f = 0; f <= maxFreq; f += freqStep) {
      let real = 0;
      let imag = 0;

      for (let i = 0; i < nSamples; i++) {
        // Windowing weight
        let w = 1.0;
        if (useHanning) {
          w = 0.5 * (1 - Math.cos((2 * Math.PI * i) / (nSamples - 1)));
        }
        const val = timeSignal[i] * w;
        const angle = (2 * Math.PI * f * i) / samplingRate;
        real += val * Math.cos(angle);
        imag -= val * Math.sin(angle);
      }

      // Magnitude
      let mag = Math.sqrt(real * real + imag * imag) / (nSamples / 2);
      // Rectangular window spectral leakage smear
      if (!useHanning) {
        mag += 0.15;
      }
      spectrum.push({ f, mag });
    }

    const alarmTriggered = defectSeverity >= 35;
    return { timeSignal, spectrum, alarmTriggered };
  }, [fShaft, fHarmonic, fBPFO, defectSeverity, noiseLevel, useHanning]);

  // Draw Dual Display Canvas: Top = Time Domain, Bottom = Frequency Domain
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const halfH = height / 2;

    ctx.clearRect(0, 0, width, height);

    // Dark grid lines
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

    // Divider line between Time and Frequency panes
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(0, halfH);
    ctx.lineTo(width, halfH);
    ctx.stroke();

    // 1. TOP PANE: Time Domain Waveform
    const timeCenterY = halfH / 2;
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    const tStep = width / (timeSignal.length - 1);
    timeSignal.forEach((val, i) => {
      const x = i * tStep;
      const y = timeCenterY - val * 12;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // 2. BOTTOM PANE: Frequency Spectrum (FFT)
    const baseFreqY = height - 15;
    const maxSpecH = halfH - 35;
    const fStep = width / (spectrum.length - 1);

    // Alarm Threshold line
    const alarmY = baseFreqY - maxSpecH * 0.45;
    ctx.strokeStyle = '#ef444480';
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(0, alarmY);
    ctx.lineTo(width, alarmY);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw spectrum fill and line
    ctx.strokeStyle = alarmTriggered ? '#f59e0b' : '#10b981';
    ctx.fillStyle = alarmTriggered ? '#f59e0b15' : '#10b98115';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, baseFreqY);

    spectrum.forEach((pt, i) => {
      const x = i * fStep;
      const h = Math.min(maxSpecH, pt.mag * 32);
      const y = baseFreqY - h;
      ctx.lineTo(x, y);
    });
    ctx.lineTo(width, baseFreqY);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    spectrum.forEach((pt, i) => {
      const x = i * fStep;
      const h = Math.min(maxSpecH, pt.mag * 32);
      const y = baseFreqY - h;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Mark BPFO peak position with arrow
    const bpfoX = (fBPFO / 400) * width;
    if (defectSeverity > 10) {
      ctx.fillStyle = '#ef4444';
      ctx.beginPath();
      ctx.arc(bpfoX, baseFreqY - 50, 4, 0, 2 * Math.PI);
      ctx.fill();

      ctx.fillStyle = '#f87171';
      ctx.font = '10px monospace';
      ctx.fillText(`BPFO (${fBPFO.toFixed(1)}Hz)`, bpfoX - 25, baseFreqY - 58);
    }
  }, [timeSignal, spectrum, alarmTriggered, defectSeverity, fBPFO]);

  return (
    <div className="bg-industrial-900 border border-industrial-800 rounded-xl p-5 text-industrial-100 shadow-xl font-sans">
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-industrial-800">
        <div>
          <span className="text-[10px] font-mono uppercase tracking-wider text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
            MOD-05 VISUAL LAB
          </span>
          <h3 className="text-base font-bold text-white mt-1 flex items-center gap-2">
            <Radio className="text-amber-500" size={18} />
            <span>FFT Vibration Analysis & Characteristic Bearing Defect</span>
          </h3>
          <p className="text-xs text-industrial-400">
            Top: Time-domain vibration (m/s²). Bottom: Frequency spectrum (0 - 400 Hz) highlighting outer race fault peak (BPFO).
          </p>
        </div>

        {/* Alarm Banner */}
        <div className={`px-3 py-1.5 rounded-lg border font-mono text-xs flex items-center gap-2 ${
          alarmTriggered
            ? 'bg-rose-500/15 border-rose-500/50 text-rose-300'
            : 'bg-emerald-500/15 border-emerald-500/50 text-emerald-300'
        }`}>
          {alarmTriggered ? <AlertTriangle size={15} /> : <ShieldCheck size={15} />}
          <span className="font-bold">
            {alarmTriggered ? 'BEARING FAULT ALARM (BPFO SPIKE)' : 'HEALTHY VIBRATION SPECTRUM'}
          </span>
        </div>
      </div>

      {/* Main Dual-Screen Display */}
      <div className="relative mt-4 bg-industrial-950 rounded-lg border border-industrial-800 overflow-hidden shadow-inner">
        <canvas
          ref={canvasRef}
          width={680}
          height={320}
          className="w-full h-72 block"
        />

        {/* Labels overlay */}
        <div className="absolute top-2 left-3 text-[10px] font-mono text-cyan-400 bg-industrial-900/80 px-2 py-0.5 rounded border border-industrial-700">
          TIME DOMAIN: Accelerometer Waveform (Raw Vibration)
        </div>
        <div className="absolute top-[52%] left-3 text-[10px] font-mono text-amber-400 bg-industrial-900/80 px-2 py-0.5 rounded border border-industrial-700">
          FREQUENCY DOMAIN (FFT): Spectral Peaks (1X: {fShaft.toFixed(1)}Hz | BPFO: {fBPFO.toFixed(1)}Hz)
        </div>
        <div className="absolute bottom-2 right-3 text-[10px] font-mono text-industrial-400">
          Frequency: 0 Hz → 400 Hz
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Motor Speed</div>
          <div className="text-base font-bold font-mono text-white">{rpm} RPM</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Shaft 1X Speed</div>
          <div className="text-base font-bold font-mono text-cyan-400">{fShaft.toFixed(1)} Hz</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Outer Race BPFO</div>
          <div className="text-base font-bold font-mono text-rose-400">{fBPFO.toFixed(1)} Hz</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Windowing</div>
          <div className="text-base font-bold font-mono text-emerald-400">
            {useHanning ? 'Hanning (Clean)' : 'Rectangular (Leakage)'}
          </div>
        </div>
      </div>

      {/* Sliders */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-5 p-4 bg-industrial-850/60 rounded-lg border border-industrial-800/80">
        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Motor Rotational Speed (RPM):</span>
            <span className="text-cyan-400 font-bold">{rpm} RPM ({fShaft.toFixed(0)} Hz)</span>
          </div>
          <input
            type="range"
            min="600"
            max="3000"
            step="60"
            value={rpm}
            onChange={(e) => setRpm(parseInt(e.target.value, 10))}
            className="w-full accent-cyan-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Bearing Defect Severity (BPFO Peak):</span>
            <span className="text-rose-400 font-bold">{defectSeverity}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            step="5"
            value={defectSeverity}
            onChange={(e) => setDefectSeverity(parseInt(e.target.value, 10))}
            className="w-full accent-rose-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Background Noise Level:</span>
            <span className="text-industrial-400 font-bold">{noiseLevel}%</span>
          </div>
          <input
            type="range"
            min="5"
            max="70"
            step="5"
            value={noiseLevel}
            onChange={(e) => setNoiseLevel(parseInt(e.target.value, 10))}
            className="w-full accent-industrial-400 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="text-xs font-mono mb-1.5 text-industrial-300">Window Function:</div>
          <div className="flex gap-2">
            <button
              onClick={() => setUseHanning(true)}
              className={`flex-1 py-1.5 px-3 rounded text-xs font-mono transition border ${
                useHanning
                  ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500 font-bold'
                  : 'bg-industrial-800 text-industrial-400 border-industrial-700 hover:text-white'
              }`}
            >
              Hanning Window
            </button>
            <button
              onClick={() => setUseHanning(false)}
              className={`flex-1 py-1.5 px-3 rounded text-xs font-mono transition border ${
                !useHanning
                  ? 'bg-amber-500/20 text-amber-300 border-amber-500 font-bold'
                  : 'bg-industrial-800 text-industrial-400 border-industrial-700 hover:text-white'
              }`}
            >
              Rectangular (Leakage)
            </button>
          </div>
        </div>
      </div>

      {/* Industrial Engineering Insight */}
      <div className="mt-4 p-3 bg-industrial-950/80 border-l-2 border-amber-500 rounded text-xs text-industrial-300 leading-relaxed">
        <span className="font-mono font-bold text-amber-400 uppercase">🏭 Inżynierski Wniosek: </span>
        Zauważ: w dziedzinie czasu (wykres górny) drgania wyglądają na chaotyczny szum. Dopiero transformata FFT (wykres dolny) dekomponuje sygnał i wyraźnie ukazuje pik <span className="font-mono text-rose-400 font-bold">BPFO ({fBPFO.toFixed(1)} Hz)</span>. Wyłączenie okna Hanninga powoduje rozmycie energii na sąsiednie prążki (spectral leakage).
      </div>
    </div>
  );
};

export default FftAnomalySandbox;
