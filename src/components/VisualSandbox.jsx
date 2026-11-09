import React, { useState } from 'react';
import SignalFilterSandbox from './sandboxes/SignalFilterSandbox';
import ScalingOutlierSandbox from './sandboxes/ScalingOutlierSandbox';
import CostMatrixSandbox from './sandboxes/CostMatrixSandbox';
import ClusteringSandbox from './sandboxes/ClusteringSandbox';
import FftAnomalySandbox from './sandboxes/FftAnomalySandbox';
import CnnIouSandbox from './sandboxes/CnnIouSandbox';
import DriftLatencySandbox from './sandboxes/DriftLatencySandbox';
import { Layers, ChevronRight } from 'lucide-react';

const SANDBOX_LIST = [
  { id: 'signal_filter_sandbox', modNum: 1, label: 'Mod 1: Signal & Noise Filter' },
  { id: 'scaling_outlier_sandbox', modNum: 2, label: 'Mod 2: Robust vs Standard Scaling' },
  { id: 'cost_matrix_sandbox', modNum: 3, label: 'Mod 3: Asymmetric Cost Matrix' },
  { id: 'clustering_sandbox', modNum: 4, label: 'Mod 4: Regime Clustering & DBSCAN' },
  { id: 'fft_anomaly_sandbox', modNum: 5, label: 'Mod 5: FFT & Bearing BPFO' },
  { id: 'cnn_iou_sandbox', modNum: 6, label: 'Mod 6: Defect IoU Bounding Box' },
  { id: 'drift_latency_sandbox', modNum: 7, label: 'Mod 7: MLOps Drift & INT8 Edge' },
];

export const VisualSandbox = ({ type = 'signal_filter_sandbox', allowSwitch = true }) => {
  const [activeType, setActiveType] = useState(type);

  // Sync if prop changes
  React.useEffect(() => {
    setActiveType(type);
  }, [type]);

  const renderSandbox = () => {
    switch (activeType) {
      case 'signal_filter_sandbox':
        return <SignalFilterSandbox />;
      case 'scaling_outlier_sandbox':
        return <ScalingOutlierSandbox />;
      case 'cost_matrix_sandbox':
        return <CostMatrixSandbox />;
      case 'clustering_sandbox':
        return <ClusteringSandbox />;
      case 'fft_anomaly_sandbox':
        return <FftAnomalySandbox />;
      case 'cnn_iou_sandbox':
        return <CnnIouSandbox />;
      case 'drift_latency_sandbox':
        return <DriftLatencySandbox />;
      default:
        return <SignalFilterSandbox />;
    }
  };

  return (
    <div className="my-6">
      {allowSwitch && (
        <div className="mb-3 flex items-center justify-between flex-wrap gap-2">
          <div className="flex items-center gap-2 text-xs font-mono text-industrial-500 dark:text-industrial-400">
            <Layers size={14} className="text-amber-500" />
            <span className="uppercase tracking-wider font-semibold">Interactive Sandbox Lab</span>
          </div>

          <div className="flex items-center gap-1.5 overflow-x-auto max-w-full pb-1">
            {SANDBOX_LIST.map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveType(item.id)}
                className={`px-2 py-1 text-[11px] font-mono rounded transition shrink-0 ${
                  activeType === item.id
                    ? 'bg-amber-500 text-industrial-950 font-bold shadow-sm'
                    : 'bg-industrial-200/80 dark:bg-industrial-800 text-industrial-700 dark:text-industrial-300 hover:bg-industrial-300 dark:hover:bg-industrial-700'
                }`}
              >
                M{item.modNum}
              </button>
            ))}
          </div>
        </div>
      )}

      {renderSandbox()}
    </div>
  );
};

export default VisualSandbox;
