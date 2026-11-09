import React, { useState, useMemo, useRef, useEffect } from 'react';
import { Eye, ShieldCheck, AlertTriangle, Scan, Check } from 'lucide-react';

export const CnnIouSandbox = () => {
  const [offsetX, setOffsetX] = useState(12); // px
  const [offsetY, setOffsetY] = useState(-8); // px
  const [scaleW, setScaleW] = useState(1.1); // width factor
  const [scaleH, setScaleH] = useState(0.95); // height factor
  const [iouThreshold, setIouThreshold] = useState(0.50);
  const [confidence, setConfidence] = useState(0.88);
  const [defectType, setDefectType] = useState('scratch'); // 'scratch', 'void', 'pore'
  const canvasRef = useRef(null);

  // Ground Truth box dimensions (centered on workpiece)
  const gtBox = {
    x: 220,
    y: 110,
    w: 160,
    h: 90,
  };

  // Predicted box from CNN
  const predBox = useMemo(() => {
    const w = Math.round(gtBox.w * scaleW);
    const h = Math.round(gtBox.h * scaleH);
    const x = Math.round(gtBox.x + offsetX - (w - gtBox.w) / 2);
    const y = Math.round(gtBox.y + offsetY - (h - gtBox.h) / 2);
    return { x, y, w, h };
  }, [gtBox, offsetX, offsetY, scaleW, scaleH]);

  // Compute exact IoU
  const metrics = useMemo(() => {
    // Coordinates of intersection rectangle
    const xLeft = Math.max(gtBox.x, predBox.x);
    const yTop = Math.max(gtBox.y, predBox.y);
    const xRight = Math.min(gtBox.x + gtBox.w, predBox.x + predBox.w);
    const yBottom = Math.min(gtBox.y + gtBox.h, predBox.y + predBox.h);

    const interW = Math.max(0, xRight - xLeft);
    const interH = Math.max(0, yBottom - yTop);
    const interArea = interW * interH;

    const gtArea = gtBox.w * gtBox.h;
    const predArea = predBox.w * predBox.h;
    const unionArea = gtArea + predArea - interArea;

    const iou = unionArea > 0 ? interArea / unionArea : 0;
    const isPass = iou >= iouThreshold && confidence >= 0.70;

    return {
      interArea,
      unionArea,
      gtArea,
      predArea,
      iou: Math.min(1.0, Math.max(0.0, iou)),
      isPass,
    };
  }, [gtBox, predBox, iouThreshold, confidence]);

  // Render on Canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    // 1. Draw Simulated Brushed Sheet Metal Texture
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1;
    for (let y = 0; y < height; y += 4) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // 2. Draw Realistic Surface Scratch Defect
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(gtBox.x + 20, gtBox.y + 25);
    ctx.quadraticCurveTo(gtBox.x + 80, gtBox.y + 60, gtBox.x + 140, gtBox.y + 55);
    ctx.stroke();

    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(gtBox.x + 22, gtBox.y + 26);
    ctx.quadraticCurveTo(gtBox.x + 82, gtBox.y + 61, gtBox.x + 138, gtBox.y + 56);
    ctx.stroke();

    // 3. Highlight Intersection Area (Cross-Hatch Pattern)
    const xLeft = Math.max(gtBox.x, predBox.x);
    const yTop = Math.max(gtBox.y, predBox.y);
    const xRight = Math.min(gtBox.x + gtBox.w, predBox.x + predBox.w);
    const yBottom = Math.min(gtBox.y + gtBox.h, predBox.y + predBox.h);
    const interW = Math.max(0, xRight - xLeft);
    const interH = Math.max(0, yBottom - yTop);

    if (interW > 0 && interH > 0) {
      ctx.fillStyle = 'rgba(245, 158, 11, 0.25)';
      ctx.fillRect(xLeft, yTop, interW, interH);

      ctx.strokeStyle = 'rgba(245, 158, 11, 0.5)';
      ctx.lineWidth = 1;
      for (let x = xLeft - interH; x < xRight; x += 8) {
        ctx.beginPath();
        ctx.moveTo(Math.max(xLeft, x), yTop);
        ctx.lineTo(Math.min(xRight, x + interH), yBottom);
        ctx.stroke();
      }
    }

    // 4. Draw Ground Truth Box (Green)
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 2.5;
    ctx.strokeRect(gtBox.x, gtBox.y, gtBox.w, gtBox.h);

    ctx.fillStyle = '#10b981';
    ctx.fillRect(gtBox.x, gtBox.y - 18, 120, 18);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 10px monospace';
    ctx.fillText('GROUND TRUTH', gtBox.x + 6, gtBox.y - 5);

    // 5. Draw Predicted Box (Amber / Cyan)
    const predColor = metrics.isPass ? '#f59e0b' : '#f43f5e';
    ctx.strokeStyle = predColor;
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 3]);
    ctx.strokeRect(predBox.x, predBox.y, predBox.w, predBox.h);
    ctx.setLineDash([]);

    ctx.fillStyle = predColor;
    ctx.fillRect(predBox.x, predBox.y + predBox.h, 160, 18);
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 10px monospace';
    ctx.fillText(`CNN PRED (${(confidence * 100).toFixed(0)}%)`, predBox.x + 6, predBox.y + predBox.h + 13);
  }, [gtBox, predBox, metrics, confidence]);

  return (
    <div className="bg-industrial-900 border border-industrial-800 rounded-xl p-5 text-industrial-100 shadow-xl font-sans">
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-industrial-800">
        <div>
          <span className="text-[10px] font-mono uppercase tracking-wider text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">
            MOD-06 VISUAL LAB
          </span>
          <h3 className="text-base font-bold text-white mt-1 flex items-center gap-2">
            <Scan className="text-rose-500" size={18} />
            <span>Industrial Optical Inspection & IoU Bounding Box Tuning</span>
          </h3>
          <p className="text-xs text-industrial-400">
            Green: Ground Truth (Inspector annotation). Amber/Red: CNN prediction. Intersection over Union (IoU) measures spatial accuracy.
          </p>
        </div>

        {/* Status Badge */}
        <div className={`px-3 py-1.5 rounded-lg border font-mono text-xs flex items-center gap-2 ${
          metrics.isPass
            ? 'bg-emerald-500/15 border-emerald-500/50 text-emerald-300'
            : 'bg-rose-500/15 border-rose-500/50 text-rose-300'
        }`}>
          {metrics.isPass ? <ShieldCheck size={16} /> : <AlertTriangle size={16} />}
          <span className="font-bold">
            {metrics.isPass ? 'ACCEPT: TRUE POSITIVE (IoU ≥ Threshold)' : 'REJECT: POOR LOCALIZATION'}
          </span>
        </div>
      </div>

      {/* Main Camera Canvas */}
      <div className="relative mt-4 bg-industrial-950 rounded-lg border border-industrial-800 overflow-hidden shadow-inner">
        <canvas
          ref={canvasRef}
          width={640}
          height={300}
          className="w-full h-72 block"
        />

        {/* Camera HUD Overlays */}
        <div className="absolute top-2 left-3 flex items-center gap-2 text-[10px] font-mono text-industrial-400 bg-industrial-900/80 px-2.5 py-1 rounded border border-industrial-800">
          <Eye size={13} className="text-emerald-400" />
          <span>CAM-04 LINEAR INSPECTOR [2048x1080 @ 60FPS]</span>
        </div>

        <div className="absolute bottom-2 right-3 bg-industrial-900/90 backdrop-blur p-2.5 rounded border border-industrial-800 text-xs font-mono">
          <div className="text-industrial-400 mb-1">Intersection over Union:</div>
          <div className="text-xl font-bold font-mono text-white flex items-center gap-2">
            <span>IoU = {(metrics.iou * 100).toFixed(1)}%</span>
            <span className={`text-[11px] px-1.5 py-0.5 rounded ${
              metrics.iou >= iouThreshold ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
            }`}>
              {metrics.iou >= iouThreshold ? 'PASS' : 'FAIL'}
            </span>
          </div>
        </div>
      </div>

      {/* Numerical Metrics Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Intersection Area</div>
          <div className="text-base font-bold font-mono text-amber-400">{metrics.interArea.toLocaleString()} px²</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Union Area</div>
          <div className="text-base font-bold font-mono text-cyan-400">{metrics.unionArea.toLocaleString()} px²</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Pass Threshold</div>
          <div className="text-base font-bold font-mono text-white">{(iouThreshold * 100).toFixed(0)}%</div>
        </div>
        <div className="bg-industrial-850 p-2.5 rounded border border-industrial-800 text-center">
          <div className="text-[10px] font-mono uppercase text-industrial-400">Model Confidence</div>
          <div className="text-base font-bold font-mono text-emerald-400">{(confidence * 100).toFixed(0)}%</div>
        </div>
      </div>

      {/* Sliders for Bounding Box Manipulation */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-5 p-4 bg-industrial-850/60 rounded-lg border border-industrial-800/80">
        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Predicted Box X Offset:</span>
            <span className="text-amber-400 font-bold">{offsetX} px</span>
          </div>
          <input
            type="range"
            min="-50"
            max="50"
            step="1"
            value={offsetX}
            onChange={(e) => setOffsetX(parseInt(e.target.value, 10))}
            className="w-full accent-amber-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Predicted Box Y Offset:</span>
            <span className="text-amber-400 font-bold">{offsetY} px</span>
          </div>
          <input
            type="range"
            min="-40"
            max="40"
            step="1"
            value={offsetY}
            onChange={(e) => setOffsetY(parseInt(e.target.value, 10))}
            className="w-full accent-amber-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Box Scale Factor:</span>
            <span className="text-cyan-400 font-bold">{scaleW.toFixed(2)}x</span>
          </div>
          <input
            type="range"
            min="0.6"
            max="1.5"
            step="0.05"
            value={scaleW}
            onChange={(e) => {
              setScaleW(parseFloat(e.target.value));
              setScaleH(parseFloat(e.target.value));
            }}
            className="w-full accent-cyan-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">IoU Certification Threshold:</span>
            <span className="text-emerald-400 font-bold">{iouThreshold.toFixed(2)}</span>
          </div>
          <input
            type="range"
            min="0.30"
            max="0.85"
            step="0.05"
            value={iouThreshold}
            onChange={(e) => setIouThreshold(parseFloat(e.target.value))}
            className="w-full accent-emerald-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>
      </div>

      {/* Industrial Engineering Insight */}
      <div className="mt-4 p-3 bg-industrial-950/80 border-l-2 border-rose-500 rounded text-xs text-industrial-300 leading-relaxed">
        <span className="font-mono font-bold text-rose-400 uppercase">🏭 Inżynierski Wniosek: </span>
        Przesuń suwaki pozycji X/Y: nawet przy prawidłowym wykryciu wady (wysoki Confidence), niedokładna ramka (IoU &lt; {iouThreshold}) spowoduje, że robot szlifierski uderzy kilka milimetrów obok rysy, uszkadzając zdrowy detal. W branży motoryzacyjnej standardem akceptacji wdrożenia jest <span className="font-mono text-white font-bold">mAP@0.50</span> lub wyższy.
      </div>
    </div>
  );
};

export default CnnIouSandbox;
