import React, { useState, useMemo, useRef, useEffect } from 'react';
import { Gauge, Cpu, AlertTriangle, ShieldCheck, Zap, RefreshCw } from 'lucide-react';

export const DriftLatencySandbox = () => {
  const [driftShift, setDriftShift] = useState(0.4); // Standard deviation shift
  const [precision, setPrecision] = useState('int8'); // 'fp32', 'fp16', 'int8'
  const [batchSize, setBatchSize] = useState(1);
  const [edgeDevice, setEdgeDevice] = useState('jetson'); // 'jetson', 'rpi5', 'siemens_ipc'
  const canvasRef = useRef(null);

  // Compute KS distance and drift metrics
  const driftMetrics = useMemo(() => {
    // Normal CDF difference approximation
    const dKS = Math.min(1.0, driftShift * 0.28);
    // p-value drops exponentially with drift distance
    const pValue = Math.max(0.0001, Math.exp(-Math.pow(driftShift, 2) * 2.5));
    const isDrifting = pValue < 0.01;

    return { dKS, pValue, isDrifting };
  }, [driftShift]);

  // Compute Edge Latency & Throughput based on precision and device
  const edgeMetrics = useMemo(() => {
    let baseLatencyMs = 28.0; // FP32 baseline on Jetson
    let baseMemoryMb = 340;

    if (edgeDevice === 'rpi5') {
      baseLatencyMs = 65.0;
      baseMemoryMb = 420;
    } else if (edgeDevice === 'siemens_ipc') {
      baseLatencyMs = 18.0;
      baseMemoryMb = 310;
    }

    // Precision multipliers
    let precMult = 1.0;
    let memMult = 1.0;
    if (precision === 'fp16') {
      precMult = 0.58;
      memMult = 0.52;
    } else if (precision === 'int8') {
      precMult = 0.26; // ~4x speedup with INT8 TensorRT
      memMult = 0.28; // ~75% memory drop
    }

    const latencyPerItem = (baseLatencyMs * precMult) / Math.pow(batchSize, 0.4);
    const latencyBatch = latencyPerItem * batchSize;
    const throughputFps = Math.round(1000 / (latencyPerItem || 1));
    const memoryMb = Math.round(baseMemoryMb * memMult + batchSize * 4);

    return {
      latencyMs: latencyPerItem.toFixed(1),
      latencyBatchMs: latencyBatch.toFixed(1),
      throughputFps,
      memoryMb,
    };
  }, [precision, edgeDevice, batchSize]);

  // Draw Bell Curves for Baseline vs Streaming Telemetry
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const baseY = height - 25;

    ctx.clearRect(0, 0, width, height);

    // Grid lines
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1;
    for (let x = 0; x < width; x += 40) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }

    const mean0 = width * 0.38;
    const mean1 = mean0 + driftShift * 45;
    const sigma = 38;

    // Normal probability density function
    const pdf = (x, m, s) => {
      const z = (x - m) / s;
      return (1 / (s * Math.sqrt(2 * Math.PI))) * Math.exp(-0.5 * z * z);
    };

    // 1. Draw Golden Reference Baseline (Blue Bell Curve)
    ctx.strokeStyle = '#38bdf8';
    ctx.fillStyle = 'rgba(56, 189, 248, 0.15)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, baseY);

    for (let x = 0; x <= width; x += 4) {
      const yVal = pdf(x, mean0, sigma) * 9500;
      ctx.lineTo(x, baseY - yVal);
    }
    ctx.lineTo(width, baseY);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    for (let x = 0; x <= width; x += 4) {
      const yVal = pdf(x, mean0, sigma) * 9500;
      if (x === 0) ctx.moveTo(x, baseY - yVal);
      else ctx.lineTo(x, baseY - yVal);
    }
    ctx.stroke();

    // 2. Draw Live Production Telemetry (Amber/Red Bell Curve)
    const driftColor = driftMetrics.isDrifting ? '#ef4444' : '#f59e0b';
    ctx.strokeStyle = driftColor;
    ctx.fillStyle = driftMetrics.isDrifting ? 'rgba(239, 68, 68, 0.2)' : 'rgba(245, 158, 11, 0.2)';
    ctx.lineWidth = 2.5;
    ctx.setLineDash([4, 2]);

    ctx.beginPath();
    ctx.moveTo(0, baseY);
    for (let x = 0; x <= width; x += 4) {
      const yVal = pdf(x, mean1, sigma * 1.1) * 9500;
      ctx.lineTo(x, baseY - yVal);
    }
    ctx.lineTo(width, baseY);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    for (let x = 0; x <= width; x += 4) {
      const yVal = pdf(x, mean1, sigma * 1.1) * 9500;
      if (x === 0) ctx.moveTo(x, baseY - yVal);
      else ctx.lineTo(x, baseY - yVal);
    }
    ctx.stroke();
    ctx.setLineDash([]);

    // 3. Draw Kolmogorov-Smirnov Distance indicator
    if (driftShift > 0.2) {
      const ksX = (mean0 + mean1) / 2;
      ctx.strokeStyle = '#f43f5e';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(mean0, baseY - 60);
      ctx.lineTo(mean1, baseY - 60);
      ctx.stroke();

      ctx.fillStyle = '#f43f5e';
      ctx.font = 'bold 10px monospace';
      ctx.fillText(`Δμ = +${driftShift.toFixed(1)}σ`, ksX - 20, baseY - 68);
    }
  }, [driftShift, driftMetrics]);

  return (
    <div className="bg-industrial-900 border border-industrial-800 rounded-xl p-5 text-industrial-100 shadow-xl font-sans">
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-industrial-800">
        <div>
          <span className="text-[10px] font-mono uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
            MOD-07 VISUAL LAB
          </span>
          <h3 className="text-base font-bold text-white mt-1 flex items-center gap-2">
            <Zap className="text-emerald-500" size={18} />
            <span>MLOps: Automated Drift Detection & INT8 Edge Optimization</span>
          </h3>
          <p className="text-xs text-industrial-400">
            Monitor streaming distribution shift (KS-Test) and benchmark edge inference latency under INT8 quantization.
          </p>
        </div>

        {/* Drift Status Banner */}
        <div className={`px-3 py-1.5 rounded-lg border font-mono text-xs flex items-center gap-2 ${
          driftMetrics.isDrifting
            ? 'bg-rose-500/20 border-rose-500/50 text-rose-300'
            : 'bg-emerald-500/20 border-emerald-500/50 text-emerald-300'
        }`}>
          {driftMetrics.isDrifting ? <AlertTriangle size={15} /> : <ShieldCheck size={15} />}
          <span className="font-bold">
            {driftMetrics.isDrifting ? 'DRIFT DETECTED: RETRAINING TRIGGERED' : 'TELEMETRY CALIBRATED (STABLE)'}
          </span>
        </div>
      </div>

      {/* Main Dual-Column Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-4">
        {/* Left: Distribution Drift Chart */}
        <div className="bg-industrial-950 p-3.5 rounded-lg border border-industrial-800">
          <div className="flex items-center justify-between text-xs font-mono mb-2">
            <span className="text-industrial-300">STREAMING DATA DRIFT (KS-TEST)</span>
            <span className="text-industrial-400 text-[11px]">
              p-value: <span className={driftMetrics.isDrifting ? 'text-rose-400 font-bold' : 'text-emerald-400 font-bold'}>{driftMetrics.pValue.toFixed(4)}</span>
            </span>
          </div>

          <canvas
            ref={canvasRef}
            width={480}
            height={180}
            className="w-full h-44 block"
          />

          <div className="flex items-center justify-between text-[11px] font-mono mt-2 text-industrial-400 pt-1 border-t border-industrial-800/80">
            <span className="flex items-center gap-1.5 text-cyan-400">
              <span className="w-2.5 h-0.5 bg-cyan-400 inline-block"></span> Baseline Reference
            </span>
            <span className="flex items-center gap-1.5 text-amber-400">
              <span className="w-2.5 h-0.5 bg-amber-400 border-dashed border-b inline-block"></span> Live Production
            </span>
            <span>K-S Stat: {driftMetrics.dKS.toFixed(2)}</span>
          </div>
        </div>

        {/* Right: Edge Hardware Benchmark HUD */}
        <div className="bg-industrial-850 p-4 rounded-lg border border-industrial-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono uppercase text-industrial-400 flex items-center gap-1.5">
                <Cpu size={14} className="text-emerald-400" />
                <span>Edge Hardware Telemetry</span>
              </span>
              <span className="text-xs font-mono font-bold text-white bg-industrial-800 px-2 py-0.5 rounded border border-industrial-700">
                {edgeDevice.toUpperCase()}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3 mt-3">
              <div className="bg-industrial-900 p-2.5 rounded border border-industrial-800">
                <div className="text-[10px] font-mono uppercase text-industrial-400">Inference Latency</div>
                <div className="text-xl font-bold font-mono text-emerald-400 mt-0.5">
                  {edgeMetrics.latencyMs} <span className="text-xs font-normal text-industrial-400">ms/sample</span>
                </div>
              </div>

              <div className="bg-industrial-900 p-2.5 rounded border border-industrial-800">
                <div className="text-[10px] font-mono uppercase text-industrial-400">Edge Throughput</div>
                <div className="text-xl font-bold font-mono text-cyan-400 mt-0.5">
                  {edgeMetrics.throughputFps} <span className="text-xs font-normal text-industrial-400">FPS</span>
                </div>
              </div>

              <div className="bg-industrial-900 p-2.5 rounded border border-industrial-800">
                <div className="text-[10px] font-mono uppercase text-industrial-400">RAM Memory Footprint</div>
                <div className="text-xl font-bold font-mono text-amber-400 mt-0.5">
                  {edgeMetrics.memoryMb} <span className="text-xs font-normal text-industrial-400">MB</span>
                </div>
              </div>

              <div className="bg-industrial-900 p-2.5 rounded border border-industrial-800">
                <div className="text-[10px] font-mono uppercase text-industrial-400">Quantization Speedup</div>
                <div className="text-xl font-bold font-mono text-white mt-0.5">
                  {precision === 'int8' ? '3.8x Speed' : precision === 'fp16' ? '1.7x Speed' : '1.0x Baseline'}
                </div>
              </div>
            </div>
          </div>

          {/* Precision Selector Pills */}
          <div className="mt-4 pt-3 border-t border-industrial-700/60">
            <div className="text-xs font-mono text-industrial-400 mb-2">Model Precision & Weight Format:</div>
            <div className="grid grid-cols-3 gap-2">
              <button
                onClick={() => setPrecision('fp32')}
                className={`py-1.5 rounded text-xs font-mono transition border text-center ${
                  precision === 'fp32'
                    ? 'bg-amber-500/20 text-amber-300 border-amber-500 font-bold'
                    : 'bg-industrial-800 text-industrial-400 border-industrial-700 hover:text-white'
                }`}
              >
                FP32 (Float)
              </button>
              <button
                onClick={() => setPrecision('fp16')}
                className={`py-1.5 rounded text-xs font-mono transition border text-center ${
                  precision === 'fp16'
                    ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500 font-bold'
                    : 'bg-industrial-800 text-industrial-400 border-industrial-700 hover:text-white'
                }`}
              >
                FP16 (Half)
              </button>
              <button
                onClick={() => setPrecision('int8')}
                className={`py-1.5 rounded text-xs font-mono transition border text-center ${
                  precision === 'int8'
                    ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500 font-bold'
                    : 'bg-industrial-800 text-industrial-400 border-industrial-700 hover:text-white'
                }`}
              >
                INT8 (Quantized)
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Sliders and Settings */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-5 p-4 bg-industrial-850/60 rounded-lg border border-industrial-800/80">
        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Environmental Sensor Drift (Δμ):</span>
            <span className={driftMetrics.isDrifting ? 'text-rose-400 font-bold' : 'text-emerald-400 font-bold'}>
              +{driftShift.toFixed(2)}σ
            </span>
          </div>
          <input
            type="range"
            min="0.0"
            max="3.0"
            step="0.1"
            value={driftShift}
            onChange={(e) => setDriftShift(parseFloat(e.target.value))}
            className="w-full accent-rose-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Edge Batch Size:</span>
            <span className="text-cyan-400 font-bold">{batchSize} samples</span>
          </div>
          <input
            type="range"
            min="1"
            max="32"
            step="1"
            value={batchSize}
            onChange={(e) => setBatchSize(parseInt(e.target.value, 10))}
            className="w-full accent-cyan-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="text-xs font-mono text-industrial-300 mb-1.5">Target Edge Device:</div>
          <select
            value={edgeDevice}
            onChange={(e) => setEdgeDevice(e.target.value)}
            className="w-full bg-industrial-800 border border-industrial-700 text-white rounded p-1.5 text-xs font-mono cursor-pointer"
          >
            <option value="jetson">NVIDIA Jetson Nano / Orin</option>
            <option value="siemens_ipc">Siemens Microbox Industrial PC</option>
            <option value="rpi5">Raspberry Pi 5 (ARM Cortex-A76)</option>
          </select>
        </div>
      </div>

      {/* Industrial Engineering Insight */}
      <div className="mt-4 p-3 bg-industrial-950/80 border-l-2 border-emerald-500 rounded text-xs text-industrial-300 leading-relaxed">
        <span className="font-mono font-bold text-emerald-400 uppercase">🏭 Inżynierski Wniosek: </span>
        Przesuń suwak dryfu powyżej <span className="font-mono text-white">1.2σ</span>: p-value testu Kołmogorowa-Smirnowa spada poniżej 0.01, automatycznie uruchamiając potok dotrenowania modelu w MLOps. Przełączenie na <span className="font-mono text-emerald-400">INT8</span> redukuje czas opóźnienia z {edgeMetrics.latencyMs} ms do ułamka, pozwalając na inspekcję wyrobów w pełnym biegu taśmociągu.
      </div>
    </div>
  );
};

export default DriftLatencySandbox;
