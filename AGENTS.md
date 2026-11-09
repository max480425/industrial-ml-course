# Industrial Machine Learning & Predictive Maintenance Course
## Agent Execution Guidelines & Architecture Specification

Welcome to the **Industrial Machine Learning & Predictive Maintenance Interactive Course** repository.
This document defines the technical architecture, development standards, and multi-phase roadmap for AI agents and human contributors.

---

### Project Overview
A specialized interactive engineering platform bridging machine learning and manufacturing plant operations. The course combines:
1. **Interactive Web Application (Vite + React + Tailwind CSS)**:
   - Industrial dark/light theme with precision monospace telemetry styling.
   - 7 industrial modules, 28 comprehensive lessons.
   - 7 interactive HTML5 Canvas / SVG simulation sandboxes.
   - 3-mode global language switcher (`EN + [PL Toggle]`, `Side-by-Side EN/PL`, `PL Focus`).
   - Interactive `{{term:id}}` bilingual tooltip parser connected to an 90-term engineering glossary.
   - Interactive bilingual quiz engine with immediate feedback and lesson completion tracking.
2. **Interactive Jupyter Notebooks (Hosted on Google Colab & GitHub)**:
   - 1-click "Open in Google Colab" URL integration.
   - Direct `.ipynb` download links.
   - Hands-on practical task checklist with local progress persistence.

---

### Phase Roadmap

#### Phase 1: Core Foundation & Scaffold (CURRENT)
- [x] Vite + React 18 + Tailwind CSS application scaffolding.
- [x] Configurable GitHub repository configuration (`src/config.js`) for Colab URL generation.
- [x] Core layout & navigation:
  - `Layout.jsx`: 7-module collapsible sidebar, progress tracker, completion checkmarks.
  - Global language modes (`EN_TOGGLE`, `SIDE_BY_SIDE`, `PL_FOCUS`).
  - Dark/Light industrial theme.
- [x] Bilingual content components:
  - `BilingualBlock.jsx`: Accordion toggle, side-by-side mode, callouts.
  - `TermTooltip.jsx`: Interactive popup with English + Polish definitions and factory application context.
- [x] 7 Interactive visual sandboxes in `VisualSandbox.jsx`:
  1. `signal_filter_sandbox` (Mod 1): Live noisy telemetry, moving average vs EMA, cutoff, lag.
  2. `scaling_outlier_sandbox` (Mod 2): RobustScaler vs StandardScaler on extreme spikes.
  3. `cost_matrix_sandbox` (Mod 3): Asymmetric cost matrices ($10k failure vs $50 check) and threshold economics.
  4. `clustering_sandbox` (Mod 4): Operational regimes (Idle, Nominal, Overload) and DBSCAN anomaly envelopes.
  5. `fft_anomaly_sandbox` (Mod 5): FFT spectral decomposition, windowing, and bearing BPFO fault peaks.
  6. `cnn_iou_sandbox` (Mod 6): Surface defect inspection, bounding box offsets, and IoU metric calculation.
  7. `drift_latency_sandbox` (Mod 7): Kolmogorov-Smirnov distribution drift and INT8 edge latency benchmarks.
- [x] Practice & Quiz engine:
  - `ColabLauncher.jsx`: Colab 1-click button, `.ipynb` downloader, interactive task checklist.
  - `QuizEngine.jsx`: Instant feedback, score calculation, confetti on pass, lesson completion hooks.
- [x] Complete data stores:
  - `src/data/syllabus.json`: 7 modules, 28 lessons.
  - `src/data/glossary.json`: 90 bilingual ML and engineering terms.
- [x] 28 notebook templates in `public/notebooks/`.

#### Phase 2: Notebook Content Deep-Dive & Real Plant Datasets
- [ ] Implement fully runnable data pipelines in each of the 28 `.ipynb` notebooks.
- [ ] Integrate real open-source industrial datasets (NASA C-MAPSS turbofan, Case Western Reserve bearing vibration, NEU surface defect database, Tennessee Eastman process).
- [ ] Add ONNX and TensorRT edge deployment scripts.

#### Phase 3: Telemetry Stream Playground & Hardware Bridge
- [ ] Add simulated WebSocket MQTT / Modbus TCP streaming telemetry mock.
- [ ] Live edge simulator for Raspberry Pi / Jetson latency Profiler.

---

### Configuration Guide (`src/config.js`)
To customize the GitHub repository for Google Colab links:
```javascript
export const CONFIG = {
  githubUser: 'YOUR_GITHUB_USERNAME',
  githubRepo: 'YOUR_REPO_NAME',
  githubBranch: 'main',
  notebooksPath: 'public/notebooks',
  ...
};
```
Google Colab 1-click URLs are generated dynamically as:
`https://colab.research.google.com/github/{githubUser}/{githubRepo}/blob/{githubBranch}/{notebooksPath}/{notebookFileName}`

---

### Code Structure
```
├── public/
│   └── notebooks/                 # 28 downloadable Jupyter notebooks (.ipynb)
├── src/
│   ├── components/
│   │   ├── sandboxes/             # 7 interactive visualizers
│   │   │   ├── SignalFilterSandbox.jsx
│   │   │   ├── ScalingOutlierSandbox.jsx
│   │   │   ├── CostMatrixSandbox.jsx
│   │   │   ├── ClusteringSandbox.jsx
│   │   │   ├── FftAnomalySandbox.jsx
│   │   │   ├── CnnIouSandbox.jsx
│   │   │   └── DriftLatencySandbox.jsx
│   │   ├── BilingualBlock.jsx     # Accordion and side-by-side text parser
│   │   ├── ColabLauncher.jsx      # Colab card and practical task checklist
│   │   ├── GlossaryModal.jsx      # 90-term searchable glossary modal
│   │   ├── Layout.jsx             # 7-module sidebar & theme layout
│   │   ├── LessonView.jsx         # Full lesson presentation view
│   │   ├── QuizEngine.jsx         # Interactive knowledge check quiz
│   │   ├── TermTooltip.jsx        # Term hover/click popup
│   │   └── VisualSandbox.jsx      # Multi-sandbox router & container
│   ├── context/
│   │   ├── LanguageContext.jsx    # Language modes & dark/light theme
│   │   └── ProgressContext.jsx    # Completed lessons & task checkmarks
│   ├── data/
│   │   ├── glossary.json          # 90 bilingual terms
│   │   └── syllabus.json          # 7 modules, 28 lessons
│   ├── config.js                  # GitHub user/repo configuration
│   ├── App.jsx                    # Root application component
│   ├── main.jsx                   # Entry point
│   └── index.css                  # Industrial design tokens & Tailwind
├── index.html
├── package.json
├── tailwind.config.js
└── vite.config.js
```

---

### Verification Commands
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run production build
npm run build
```
Build output must compile with zero errors and zero warnings.
