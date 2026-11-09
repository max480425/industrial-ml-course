import React, { useState, useMemo } from 'react';
import { DollarSign, AlertTriangle, ShieldCheck, ArrowRight, TrendingDown } from 'lucide-react';

export const CostMatrixSandbox = () => {
  const [threshold, setThreshold] = useState(0.18);
  const [costFN, setCostFN] = useState(10000); // $10k breakdown
  const [costFP, setCostFP] = useState(50); // $50 manual check
  const [defectRate, setDefectRate] = useState(2.0); // 2% defects

  const totalParts = 10000;
  const numDefects = Math.round((totalParts * defectRate) / 100);
  const numHealthy = totalParts - numDefects;

  // Model probability distribution simulation
  // Healthy parts follow Beta(2, 8) skewed near 0
  // Defective parts follow Beta(8, 2) skewed near 1
  const calculateOutcomes = (t) => {
    // Cumulative distribution approximations
    // Sensitivity / Recall at threshold t:
    // P(score > t | Defective) ~ (1 - t^2)^0.8
    const recall = Math.max(0, Math.min(1, Math.pow(1 - Math.pow(t, 2.5), 0.6)));
    const tp = Math.round(numDefects * recall);
    const fn = numDefects - tp;

    // False Positive Rate:
    // P(score > t | Healthy) ~ (1 - t)^3.5
    const fpr = Math.max(0, Math.min(1, Math.pow(1 - t, 3.8)));
    const fp = Math.round(numHealthy * fpr);
    const tn = numHealthy - fp;

    const totalCost = fn * costFN + fp * costFP;
    const precision = tp / ((tp + fp) || 1);

    return { tp, fn, fp, tn, recall, precision, totalCost };
  };

  const current = useMemo(() => calculateOutcomes(threshold), [threshold, costFN, costFP, defectRate]);
  const naive = useMemo(() => calculateOutcomes(0.50), [costFN, costFP, defectRate]);

  // Sweep threshold to find optimal operating point
  const { optimalThreshold, minCost, costCurve } = useMemo(() => {
    let bestT = 0.5;
    let lowestCost = Infinity;
    const curve = [];

    for (let t = 0.02; t <= 0.98; t += 0.02) {
      const res = calculateOutcomes(t);
      curve.push({ t, cost: res.totalCost });
      if (res.totalCost < lowestCost) {
        lowestCost = res.totalCost;
        bestT = t;
      }
    }
    return { optimalThreshold: bestT, minCost: lowestCost, costCurve: curve };
  }, [costFN, costFP, defectRate]);

  const savings = Math.max(0, naive.totalCost - current.totalCost);

  return (
    <div className="bg-industrial-900 border border-industrial-800 rounded-xl p-5 text-industrial-100 shadow-xl font-sans">
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-industrial-800">
        <div>
          <span className="text-[10px] font-mono uppercase tracking-wider text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
            MOD-03 VISUAL LAB
          </span>
          <h3 className="text-base font-bold text-white mt-1 flex items-center gap-2">
            <DollarSign className="text-amber-500" size={18} />
            <span>Asymmetric Cost Matrix & Threshold Economics</span>
          </h3>
          <p className="text-xs text-industrial-400">
            Simulate 10,000 manufactured parts. Align the decision threshold to minimize real factory losses.
          </p>
        </div>

        <div className="text-right">
          <div className="text-[10px] font-mono text-industrial-400 uppercase">Monthly Savings vs 0.50 Default</div>
          <div className="text-base font-bold font-mono text-emerald-400">
            +${savings.toLocaleString()} USD
          </div>
        </div>
      </div>

      {/* Financial Matrix Summary & Loss Card */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mt-4">
        {/* Confusion Matrix Display */}
        <div className="lg:col-span-2 bg-industrial-950 p-4 rounded-lg border border-industrial-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono font-bold text-industrial-300">
              INDUSTRIAL CONFUSION MATRIX ({totalParts.toLocaleString()} PARTS)
            </span>
            <span className="text-xs font-mono text-amber-400">
              Threshold: <span className="font-bold">{threshold.toFixed(2)}</span>
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3 text-center text-xs font-mono mt-3">
            {/* TP */}
            <div className="bg-emerald-950/30 border border-emerald-500/40 p-3 rounded-lg">
              <div className="text-emerald-400 text-[11px] font-semibold flex items-center justify-center gap-1">
                <ShieldCheck size={14} />
                <span>True Positive (Caught Defect)</span>
              </div>
              <div className="text-2xl font-bold text-white mt-1">{current.tp}</div>
              <div className="text-[10px] text-industrial-400 mt-0.5">Scrapped correctly</div>
            </div>

            {/* FP */}
            <div className="bg-amber-950/30 border border-amber-500/40 p-3 rounded-lg">
              <div className="text-amber-400 text-[11px] font-semibold flex items-center justify-center gap-1">
                <AlertTriangle size={14} />
                <span>False Positive (False Alarm)</span>
              </div>
              <div className="text-2xl font-bold text-white mt-1">{current.fp}</div>
              <div className="text-[10px] text-industrial-400 mt-0.5">
                Cost: ${(current.fp * costFP).toLocaleString()} (${costFP}/scan)
              </div>
            </div>

            {/* FN */}
            <div className="bg-rose-950/40 border-2 border-rose-500/70 p-3 rounded-lg shadow-md shadow-rose-900/20">
              <div className="text-rose-400 text-[11px] font-bold flex items-center justify-center gap-1">
                <AlertTriangle size={14} />
                <span>False Negative (MISSED CATASTROPHE)</span>
              </div>
              <div className="text-2xl font-bold text-rose-300 mt-1">{current.fn}</div>
              <div className="text-[10px] text-rose-400 font-bold mt-0.5">
                Loss: ${(current.fn * costFN).toLocaleString()} (${costFN}/failure)
              </div>
            </div>

            {/* TN */}
            <div className="bg-industrial-900 border border-industrial-800 p-3 rounded-lg">
              <div className="text-industrial-300 text-[11px] font-semibold flex items-center justify-center gap-1">
                <ShieldCheck size={14} />
                <span>True Negative (Clean Parts)</span>
              </div>
              <div className="text-2xl font-bold text-industrial-200 mt-1">{current.tn}</div>
              <div className="text-[10px] text-industrial-400 mt-0.5">Passed down line</div>
            </div>
          </div>
        </div>

        {/* Cost & Metrics Summary */}
        <div className="bg-industrial-850 p-4 rounded-lg border border-industrial-800 flex flex-col justify-between">
          <div>
            <div className="text-[10px] font-mono uppercase text-industrial-400">Total Financial Loss</div>
            <div className="text-2xl font-bold font-mono text-rose-400 mt-1">
              ${current.totalCost.toLocaleString()}
            </div>
            <div className="text-[11px] text-industrial-400 mt-1">
              At default 0.50 threshold: <span className="line-through text-industrial-500">${naive.totalCost.toLocaleString()}</span>
            </div>
          </div>

          <div className="space-y-2 mt-4 pt-4 border-t border-industrial-700/60 font-mono text-xs">
            <div className="flex justify-between">
              <span className="text-industrial-400">Defect Recall (Safety):</span>
              <span className="text-emerald-400 font-bold">{(current.recall * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-industrial-400">Precision:</span>
              <span className="text-cyan-400 font-bold">{(current.precision * 100).toFixed(1)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-industrial-400">Cost-Optimal Threshold:</span>
              <span className="text-amber-400 font-bold">{optimalThreshold.toFixed(2)}</span>
            </div>
          </div>

          <button
            onClick={() => setThreshold(optimalThreshold)}
            className="w-full mt-4 py-2 px-3 text-xs font-mono font-bold bg-amber-500 hover:bg-amber-400 text-industrial-950 rounded transition flex items-center justify-center gap-1.5"
          >
            <TrendingDown size={14} />
            <span>Apply Optimal Threshold ({optimalThreshold.toFixed(2)})</span>
          </button>
        </div>
      </div>

      {/* Interactive Sliders */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-5 p-4 bg-industrial-850/60 rounded-lg border border-industrial-800/80">
        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Decision Threshold:</span>
            <span className="text-amber-400 font-bold">{threshold.toFixed(2)}</span>
          </div>
          <input
            type="range"
            min="0.02"
            max="0.80"
            step="0.01"
            value={threshold}
            onChange={(e) => setThreshold(parseFloat(e.target.value))}
            className="w-full accent-amber-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
          <div className="flex justify-between text-[10px] font-mono text-industrial-500 mt-1">
            <span>0.02 (Aggressive inspection)</span>
            <span>0.50 (Academic default)</span>
            <span>0.80 (Permissive)</span>
          </div>
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Cost of Missed Defect (FN):</span>
            <span className="text-rose-400 font-bold">${costFN.toLocaleString()}</span>
          </div>
          <input
            type="range"
            min="1000"
            max="25000"
            step="1000"
            value={costFN}
            onChange={(e) => setCostFN(parseInt(e.target.value, 10))}
            className="w-full accent-rose-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Cost of False Alarm (FP):</span>
            <span className="text-amber-300 font-bold">${costFP}</span>
          </div>
          <input
            type="range"
            min="10"
            max="300"
            step="10"
            value={costFP}
            onChange={(e) => setCostFP(parseInt(e.target.value, 10))}
            className="w-full accent-amber-400 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-industrial-300">Defect Base Rate:</span>
            <span className="text-cyan-400 font-bold">{defectRate.toFixed(1)}%</span>
          </div>
          <input
            type="range"
            min="0.5"
            max="10.0"
            step="0.5"
            value={defectRate}
            onChange={(e) => setDefectRate(parseFloat(e.target.value))}
            className="w-full accent-cyan-500 h-1.5 bg-industrial-700 rounded-lg cursor-pointer"
          />
        </div>
      </div>

      {/* Industrial Engineering Insight */}
      <div className="mt-4 p-3 bg-industrial-950/80 border-l-2 border-amber-500 rounded text-xs text-industrial-300 leading-relaxed">
        <span className="font-mono font-bold text-amber-400 uppercase">🏭 Inżynierski Wniosek: </span>
        Trzymanie akademickiego progu <span className="font-mono text-white">0.50</span> przy asymetrycznych kosztach awarii kosztuje fabrykę setki tysięcy dolarów. Obniżenie progu do <span className="font-mono text-emerald-400">{optimalThreshold.toFixed(2)}</span> łapie niemal 100% wad (wysoki recall), a drobny wzrost tanich inspekcji ręcznych (${costFP}) drastycznie minimalizuje całkowity bilans strat.
      </div>
    </div>
  );
};

export default CostMatrixSandbox;
