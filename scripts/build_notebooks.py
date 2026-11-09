#!/usr/bin/env python3
"""
scripts/build_notebooks.py
Industrial Machine Learning & Predictive Maintenance Course

Compiles structured lesson definitions into valid, production-ready Jupyter Notebooks (.ipynb)
using Python's nbformat (v4) library.
"""

import os
import json
import re
from pathlib import Path
import nbformat as nbf

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = PROJECT_ROOT / "src" / "data" / "lessons"
SYLLABUS_FILE = PROJECT_ROOT / "src" / "data" / "syllabus.json"
OUTPUT_DIR = PROJECT_ROOT / "public" / "notebooks"
CONFIG_FILE = PROJECT_ROOT / "src" / "config.js"

def load_github_config():
    """Reads githubUser and githubRepo from src/config.js"""
    user = "max480425"
    repo = "industrial-ml-course"
    branch = "main"
    if CONFIG_FILE.exists():
        content = CONFIG_FILE.read_text(encoding="utf-8")
        m_user = re.search(r"githubUser:\s*['\"]([^'\"]+)['\"]", content)
        m_repo = re.search(r"githubRepo:\s*['\"]([^'\"]+)['\"]", content)
        m_branch = re.search(r"githubBranch:\s*['\"]([^'\"]+)['\"]", content)
        if m_user: user = m_user.group(1)
        if m_repo: repo = m_repo.group(1)
        if m_branch: branch = m_branch.group(1)
    return user, repo, branch

def get_module_specific_code(module_number, lesson_number, lesson_data):
    """
    Returns (theory_md, simulation_code, visualization_code, exercise_code)
    tailored to the lesson's industrial ML domain.
    """
    m = module_number
    l = lesson_number
    title = lesson_data.get("title_en", "Industrial ML Task")

    if m == 1:
        # Module 1: Signals, Filtering, Noise
        theory = f"""### Key Engineering Concepts:
1. **Sampling Frequency & Nyquist Criterion**: $F_s \\ge 2 \\cdot F_{{max}}$ is required to avoid frequency aliasing.
2. **Noise Sources**: High-voltage VFD drives and welding arcs induce electromagnetic high-frequency noise into sensor wiring.
3. **Phase Delay vs Smoothing**: Larger filter windows eliminate noise but introduce group delay, slowing safety shutdown reactions.
"""
        sim = """# 1. Simulate High-Speed Factory Telemetry (Vibration & Spikes)
np.random.seed(42)
sampling_rate = 1000  # Hz
duration = 2.0        # seconds
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Fundamental mechanical rotation (30 Hz ~ 1800 RPM) + 90 Hz harmonic
clean_signal = 2.5 * np.sin(2 * np.pi * 30 * t) + 1.2 * np.sin(2 * np.pi * 90 * t)

# Add electromagnetic sensor noise
noise = 0.8 * np.random.randn(len(t))

# Inject intermittent electrical arc spikes
spikes = np.zeros_like(t)
spike_indices = np.random.choice(len(t), size=8, replace=False)
spikes[spike_indices] = np.random.choice([-1, 1], size=8) * 6.5

raw_telemetry = clean_signal + noise + spikes
print(f"✓ Generated {len(raw_telemetry)} telemetry samples across {duration}s at {sampling_rate} Hz.")
"""
        viz = """# 2. Digital Filtering & Waveform Inspection
# Apply Moving Average filter
window_size = 15
kernel = np.ones(window_size) / window_size
smoothed_ma = np.convolve(raw_telemetry, kernel, mode='same')

# Apply 4th-order Butterworth Low-Pass Filter
nyquist = 0.5 * sampling_rate
cutoff = 45.0  # Hz
b, a = signal.butter(4, cutoff / nyquist, btype='low')
smoothed_butter = signal.filtfilt(b, a, raw_telemetry)

plt.figure(figsize=(14, 5))
plt.plot(t[:300], raw_telemetry[:300], color='#ef4444', alpha=0.5, label='Raw Telemetry with Noise & Spikes')
plt.plot(t[:300], smoothed_ma[:300], color='#f59e0b', linewidth=1.8, label=f'Moving Average (N={window_size})')
plt.plot(t[:300], smoothed_butter[:300], color='#10b981', linewidth=2.2, label='Zero-Phase Butterworth (Cutoff 45Hz)')
plt.title(f"Telemetry Signal Conditioning Pipeline - {title}", fontsize=13, fontweight='bold')
plt.xlabel("Time [seconds]")
plt.ylabel("Sensor Amplitude [V / m/s²]")
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# 1. Calculate the Root Mean Square (RMS) error between clean_signal and smoothed_butter.
# 2. Experiment with cutoff = 25 Hz vs 60 Hz and observe the signal attenuation.

rms_error = np.sqrt(np.mean((clean_signal - smoothed_butter)**2))
print(f"Filter Reconstruction RMS Error: {rms_error:.4f}")
assert rms_error < 1.5, "Reconstruction error is too high! Tune the filter parameters."
print("✓ Exercise verification passed.")
"""

    elif m == 2:
        # Module 2: Feature Engineering & Robust Scaling
        theory = """### Key Engineering Concepts:
1. **Statistical Descriptors**: RMS (destructive energy), Kurtosis (peakedness/impact shocks), and Skewness indicate machine degradation.
2. **StandardScaler Breakdown**: Single extreme spikes (e.g. 5,000A startup surge) artificially inflate variance, crushing normal operational readings into a near-zero range.
3. **RobustScaler**: Uses median and IQR ($Q_3 - Q_1$), providing immunity to severe outliers.
"""
        sim = """# 1. Simulate Industrial Motor Current with Outliers
np.random.seed(101)
n_samples = 500

# Normal steady-state operation: Mean = 24.5 A, Std = 2.8 A
normal_current = np.random.normal(loc=24.5, scale=2.8, size=n_samples)

# Contaminate with severe startup surge outliers (300A - 800A)
outlier_indices = np.random.choice(n_samples, size=15, replace=False)
telemetry = normal_current.copy()
telemetry[outlier_indices] = np.random.uniform(250.0, 750.0, size=len(outlier_indices))

df_telemetry = pd.DataFrame({'motor_current_amps': telemetry})
print(df_telemetry.describe().round(2))
"""
        viz = """# 2. Compare StandardScaler vs RobustScaler
std_scaler = StandardScaler()
robust_scaler = RobustScaler()

df_telemetry['standard_scaled'] = std_scaler.fit_transform(df_telemetry[['motor_current_amps']])
df_telemetry['robust_scaled'] = robust_scaler.fit_transform(df_telemetry[['motor_current_amps']])

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Normal range distribution comparison (excluding extreme outliers for zoom)
normal_mask = ~df_telemetry.index.isin(outlier_indices)

axes[0].hist(df_telemetry.loc[normal_mask, 'standard_scaled'], bins=25, color='#f59e0b', alpha=0.8, edgecolor='black')
axes[0].set_title("StandardScaler on Normal Data (Crushed Resolution)", fontweight='bold')
axes[0].set_xlabel("Scaled Value (Z-Score)")

axes[1].hist(df_telemetry.loc[normal_mask, 'robust_scaled'], bins=25, color='#10b981', alpha=0.8, edgecolor='black')
axes[1].set_title("RobustScaler on Normal Data (Preserved Variance)", fontweight='bold')
axes[1].set_xlabel("Scaled Value (IQR Units)")

plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Compute the Interquartile Range (IQR) for motor_current_amps and count Tukey outliers
q1 = df_telemetry['motor_current_amps'].quantile(0.25)
q3 = df_telemetry['motor_current_amps'].quantile(0.75)
iqr = q3 - q1
outlier_mask = (df_telemetry['motor_current_amps'] < q1 - 1.5 * iqr) | (df_telemetry['motor_current_amps'] > q3 + 1.5 * iqr)
print(f"Identified {outlier_mask.sum()} outliers using Tukey IQR rule (Expected ~15).")
assert outlier_mask.sum() >= 15, "Outlier detection failed to identify injected spikes."
print("✓ Outlier filtering exercise verified.")
"""

    elif m == 3:
        # Module 3: Cost-Sensitive Classification
        theory = """### Key Engineering Concepts:
1. **Asymmetric Business Penalties**: Cost(False Negative) = $10,000 (catastrophic engine breakdown), Cost(False Positive) = $50 (30-second manual check).
2. **Extreme Class Imbalance**: Flawless parts represent 99% of line output; high accuracy is trivial and misleading.
3. **Threshold Economics**: The optimal threshold minimizes expected monetary loss, not classification error count.
"""
        sim = """# 1. Simulate Plant Defect Probabilities & Financial Matrix
np.random.seed(42)
n_parts = 2000
defect_ratio = 0.03  # 3% defective parts

y_true = (np.random.rand(n_parts) < defect_ratio).astype(int)

# Simulated model predicted probabilities
# Defective parts have higher scores on average, but with overlap
pred_probs = np.zeros(n_parts)
pred_probs[y_true == 0] = np.random.beta(a=1.5, b=8.0, size=(y_true == 0).sum())
pred_probs[y_true == 1] = np.random.beta(a=6.0, b=2.0, size=(y_true == 1).sum())

print(f"Generated {n_parts} parts: {(y_true == 1).sum()} defective, {(y_true == 0).sum()} healthy.")
"""
        viz = """# 2. Sweep Thresholds and Compute Real Dollar Losses
thresholds = np.linspace(0.01, 0.95, 100)
cost_fn = 10000.0  # $10,000 per missed defect
cost_fp = 50.0     # $50 per false alarm

total_costs = []
recalls = []

for t in thresholds:
    y_pred = (pred_probs >= t).astype(int)
    fn = ((y_true == 1) & (y_pred == 0)).sum()
    fp = ((y_true == 0) & (y_pred == 1)).sum()
    tp = ((y_true == 1) & (y_pred == 1)).sum()
    
    cost = fn * cost_fn + fp * cost_fp
    total_costs.append(cost)
    recalls.append(tp / ((y_true == 1).sum() or 1))

best_idx = np.argmin(total_costs)
optimal_t = thresholds[best_idx]
min_cost = total_costs[best_idx]
naive_cost = total_costs[np.argmin(np.abs(thresholds - 0.50))]

plt.figure(figsize=(10, 5))
plt.plot(thresholds, total_costs, color='#ef4444', linewidth=2.5, label='Total Expected Financial Loss ($)')
plt.axvline(optimal_t, color='#10b981', linestyle='--', label=f'Cost-Optimal Threshold = {optimal_t:.2f} (Loss: ${min_cost:,.0f})')
plt.axvline(0.50, color='#64748b', linestyle=':', label=f'Academic 0.50 Default (Loss: ${naive_cost:,.0f})')
plt.title("Financial Loss vs Classification Decision Threshold", fontsize=13, fontweight='bold')
plt.xlabel("Decision Threshold (tau)")
plt.ylabel("Total Loss [USD]")
plt.legend()
plt.grid(True, alpha=0.4)
plt.show()
print(f"Optimal Threshold saves ${naive_cost - min_cost:,.0f} compared to the default 0.50 threshold!")
"""
        exercise = """# Exercise Challenge:
# Calculate Recall and Precision at the optimal threshold
y_opt = (pred_probs >= optimal_t).astype(int)
tp_opt = ((y_true == 1) & (y_opt == 1)).sum()
fp_opt = ((y_true == 0) & (y_opt == 1)).sum()
fn_opt = ((y_true == 1) & (y_opt == 0)).sum()

recall_opt = tp_opt / (tp_opt + fn_opt)
precision_opt = tp_opt / (tp_opt + fp_opt)
print(f"Optimal Operating Point -> Recall: {recall_opt*100:.1f}%, Precision: {precision_opt*100:.1f}%")
assert recall_opt >= 0.90, "Recall must be at least 90% to prevent expensive machine breakdowns!"
print("✓ Cost optimization exercise passed.")
"""

    elif m == 4:
        # Module 4: Clustering & Unsupervised Anomaly Detection
        theory = """### Key Engineering Concepts:
1. **Operational Regimes**: Multi-mode CNC machining (Standby, Roughing, High-Speed Finishing) exhibit distinct physical baselines.
2. **K-Means Centroids**: Act as golden reference signatures for healthy machine cycles.
3. **DBSCAN & Isolation Forests**: Detect zero-shot anomalies without requiring historical breakdown labels.
"""
        sim = """# 1. Simulate CNC Spindle Operational Regimes (RPM vs Motor Current)
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

np.random.seed(42)
# Regime 1: Idle (RPM: ~300, Current: ~6A)
c1 = np.random.multivariate_normal([300, 6], [[400, 5], [5, 0.8]], size=150)
# Regime 2: Normal Milling (RPM: ~2800, Current: ~32A)
c2 = np.random.multivariate_normal([2800, 32], [[2500, 20], [20, 4.0]], size=200)
# Regime 3: Heavy Roughing (RPM: ~2200, Current: ~65A)
c3 = np.random.multivariate_normal([2200, 65], [[2000, 30], [30, 8.0]], size=120)

# Unmodeled Breakdown Anomalies (e.g. tool seizure or mechanical bind)
anomalies = np.array([
    [1200, 58], [1500, 72], [3200, 80], [400, 35], [2600, 12]
])

X = np.vstack([c1, c2, c3, anomalies])
print(f"Total operational points: {len(X)}")
"""
        viz = """# 2. Fit K-Means Regimes and Isolation Forest Anomaly Detection
kmeans = KMeans(n_clusters=3, random_state=42).fit(X)
iso_forest = IsolationForest(contamination=0.03, random_state=42).fit(X)
anomaly_pred = iso_forest.predict(X)  # -1 represents anomaly

plt.figure(figsize=(11, 6))
# Plot normal clusters
plt.scatter(X[anomaly_pred == 1, 0], X[anomaly_pred == 1, 1], c=kmeans.labels_[anomaly_pred == 1], cmap='viridis', alpha=0.7, edgecolors='none', label='Healthy Regimes')
# Plot flagged anomalies
plt.scatter(X[anomaly_pred == -1, 0], X[anomaly_pred == -1, 1], color='#ef4444', s=120, edgecolors='black', linewidth=1.5, marker='o', label='Isolated Machine Anomalies')
# Plot cluster centroids
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=200, linewidth=2, label='Regime Centroids')

plt.title("Unsupervised Machine Regime Discovery & Anomaly Envelopes", fontsize=13, fontweight='bold')
plt.xlabel("Spindle Speed [RPM]")
plt.ylabel("Motor Current [Amps]")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
"""
        exercise = """# Exercise Challenge:
# Verify that the known synthetic anomalies were successfully flagged by Isolation Forest
flagged_count = (anomaly_pred == -1).sum()
print(f"Flagged Anomalies: {flagged_count} (Expected 5 to 15)")
assert flagged_count >= 5, "Anomaly detector failed to isolate unmodeled states!"
print("✓ Unsupervised clustering exercise passed.")
"""

    elif m == 5:
        # Module 5: Frequency Domain & Vibration FFT
        theory = """### Key Engineering Concepts:
1. **Time Domain vs Frequency Spectrum**: Microscopic bearing damage is hidden in time signals but exhibits distinct spectral peaks.
2. **Spectral Leakage & Hanning Windowing**: Non-periodic signal truncation causes energy smear; windowing restores frequency resolution.
3. **Characteristic Defect Frequencies**: Outer race defect (BPFO) peaks at $f_{{BPFO}} = \\frac{{N_{{balls}}}}{{2}} \\cdot f_{{shaft}} \\cdot \\left(1 - \\frac{{d}}{{D}}\\cos\\alpha\\right)$.
"""
        sim = """# 1. Synthesize Accelerometer Vibration Signal with Bearing Outer Race Defect
np.random.seed(42)
Fs = 2000.0  # Sampling frequency: 2000 Hz
T = 1.0 / Fs
N = 2048
time = np.linspace(0.0, N*T, N, endpoint=False)

# Motor speed: 1800 RPM -> 30 Hz shaft rotational frequency
f_shaft = 30.0
# Bearing outer race defect frequency (BPFO) ~ 3.58 * f_shaft
f_bpfo = 3.58 * f_shaft  # 107.4 Hz

# Synthetic vibration = 1X unbalance + 2X misalignment + BPFO impacts + noise
sig_1x = 1.8 * np.sin(2.0 * np.pi * f_shaft * time)
sig_2x = 0.6 * np.sin(2.0 * np.pi * (2 * f_shaft) * time)
sig_bpfo = 1.4 * np.sin(2.0 * np.pi * f_bpfo * time)
noise = 0.5 * np.random.randn(N)

vibration_accel = sig_1x + sig_2x + sig_bpfo + noise
print(f"Vibration signal generated: {N} samples over {N*T:.2f} seconds.")
"""
        viz = """# 2. Compute FFT Spectrum with Hanning Window
# Apply Hanning window to eliminate boundary leakage
window = np.hanning(N)
windowed_sig = vibration_accel * window

# Compute discrete Fourier Transform
fft_vals = np.fft.rfft(windowed_sig)
fft_freqs = np.fft.rfftfreq(N, T)
fft_mag = (2.0 / N) * np.abs(fft_vals)

fig, axes = plt.subplots(2, 1, figsize=(14, 7), sharex=False)

# Time domain plot
axes[0].plot(time[:300], vibration_accel[:300], color='#0284c7', linewidth=1.2)
axes[0].set_title("Time Domain: Accelerometer Raw Vibration (Looks Like Random Noise)", fontweight='bold')
axes[0].set_xlabel("Time [s]")
axes[0].set_ylabel("Acceleration [m/s²]")
axes[0].grid(True, alpha=0.3)

# Frequency domain plot
axes[1].plot(fft_freqs, fft_mag, color='#10b981', linewidth=1.5, label='FFT Magnitude Spectrum')
axes[1].axvline(f_shaft, color='#f59e0b', linestyle='--', label=f'1X Shaft Speed ({f_shaft:.1f} Hz)')
axes[1].axvline(f_bpfo, color='#ef4444', linestyle='-', linewidth=2, label=f'BPFO Defect Peak ({f_bpfo:.1f} Hz)')
axes[1].set_xlim(0, 300)
axes[1].set_title("Frequency Domain (FFT): Bearing Fault Signature Exposed!", fontweight='bold')
axes[1].set_xlabel("Frequency [Hz]")
axes[1].set_ylabel("Amplitude Peak [m/s²]")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Locate the frequency with maximum magnitude between 90 Hz and 130 Hz (BPFO range)
bpfo_band = (fft_freqs >= 90) & (fft_freqs <= 130)
peak_freq = fft_freqs[bpfo_band][np.argmax(fft_mag[bpfo_band])]
print(f"Detected Bearing Defect Frequency Peak at: {peak_freq:.2f} Hz (Expected ~107.4 Hz)")
assert abs(peak_freq - f_bpfo) < 2.0, "FFT defect peak detection out of tolerance!"
print("✓ Vibration analysis exercise passed.")
"""

    elif m == 6:
        # Module 6: Edge Vision & Bounding Boxes
        theory = """### Key Engineering Concepts:
1. **Spatial Localization**: In automated quality inspection, defect coordinates $[x, y, w, h]$ direct spot-repair robotics.
2. **Intersection over Union (IoU)**: $\\text{IoU} = \\frac{\\text{Area of Overlap}}{\\text{Area of Union}}$.
3. **mAP@0.50 Threshold**: Standard industry metric requiring $\\text{IoU} \\ge 0.50$ for a prediction to count as a True Positive.
"""
        sim = """# 1. Bounding Box Math & Vectorized IoU Calculation
def compute_iou(box_a, box_b):
    \"\"\"
    Computes Intersection over Union (IoU) for two boxes in [x1, y1, x2, y2] format.
    \"\"\"
    x_left = max(box_a[0], box_b[0])
    y_top = max(box_a[1], box_b[1])
    x_right = min(box_a[2], box_b[2])
    y_bottom = min(box_a[3], box_b[3])
    
    inter_w = max(0.0, x_right - x_left)
    inter_h = max(0.0, y_bottom - y_top)
    inter_area = inter_w * inter_h
    
    area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
    union_area = area_a + area_b - inter_area
    
    return inter_area / union_area if union_area > 0 else 0.0

# Ground truth scratch defect on sheet metal: [x1, y1, x2, y2]
ground_truth = [100.0, 80.0, 260.0, 180.0]
# CNN predicted candidate bounding box
predicted = [115.0, 75.0, 275.0, 175.0]

iou = compute_iou(ground_truth, predicted)
print(f"Calculated IoU: {iou:.3f} ({(iou*100):.1f}%)")
"""
        viz = """# 2. Visualizing Bounding Box Inspection
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(8, 6))
# Simulate gray sheet metal background
metal = np.random.normal(0.4, 0.05, (300, 400))
ax.imshow(metal, cmap='gray', vmin=0, vmax=1)

# Draw ground truth rectangle (Green)
gt_rect = patches.Rectangle((ground_truth[0], ground_truth[1]),
                            ground_truth[2] - ground_truth[0],
                            ground_truth[3] - ground_truth[1],
                            linewidth=2.5, edgecolor='#10b981', facecolor='none', label='Ground Truth')
ax.add_patch(gt_rect)

# Draw CNN predicted rectangle (Amber)
pred_rect = patches.Rectangle((predicted[0], predicted[1]),
                              predicted[2] - predicted[0],
                              predicted[3] - predicted[1],
                              linewidth=2.5, edgecolor='#f59e0b', linestyle='--', facecolor='none', label=f'CNN Prediction (IoU={iou:.2f})')
ax.add_patch(pred_rect)

plt.title("Industrial Optical Inspection - Bounding Box IoU Evaluation", fontsize=13, fontweight='bold')
plt.legend(loc='lower right')
plt.xlim(0, 400)
plt.ylim(300, 0)
plt.show()
"""
        exercise = """# Exercise Challenge:
# Implement a function that verifies whether a prediction passes quality inspection (IoU >= 0.50)
def is_valid_detection(gt, pred, threshold=0.50):
    return compute_iou(gt, pred) >= threshold

passes_qc = is_valid_detection(ground_truth, predicted, threshold=0.50)
print(f"Inspection Result: {'PASS (True Positive)' if passes_qc else 'REJECT (Localization Miss)'}")
assert passes_qc, "Predicted bounding box failed IoU threshold!"
print("✓ Computer vision evaluation exercise passed.")
"""

    else:
        # Module 7: MLOps, Drift & Edge Optimization
        theory = """### Key Engineering Concepts:
1. **Data Drift vs Concept Drift**: Seasonal factory temperature increases shift sensor inputs P(X); tool wear alters physical failure relationships P(Y|X).
2. **Kolmogorov-Smirnov Testing**: Non-parametric two-sample test comparing cumulative distributions to flag calibration drift.
3. **Edge Optimization**: Converting models from FP32 to INT8 precision slashes inference latency by ~3.8x with < 0.5% accuracy drop.
"""
        sim = """# 1. Simulate Production Telemetry Shift & Kolmogorov-Smirnov Test
from scipy import stats

np.random.seed(42)
# Baseline golden calibration data (e.g. ambient 22°C baseline)
baseline_telemetry = np.random.normal(loc=50.0, scale=4.0, size=1000)

# Deployed live telemetry during July summer heatwave (shifted by +1.5 standard deviations)
production_telemetry = np.random.normal(loc=56.2, scale=4.3, size=1000)

# Run two-sample Kolmogorov-Smirnov hypothesis test
ks_stat, p_value = stats.ks_2samp(baseline_telemetry, production_telemetry)
print(f"KS Statistic: {ks_stat:.4f}, p-value: {p_value:.2e}")
"""
        viz = """# 2. Visualize Telemetry Drift Distribution Shift
plt.figure(figsize=(11, 5))
sns.kdeplot(baseline_telemetry, color='#0284c7', fill=True, alpha=0.3, label='Golden Baseline Reference', linewidth=2)
sns.kdeplot(production_telemetry, color='#ef4444', fill=True, alpha=0.3, label='Live Production Telemetry (Drifted)', linewidth=2)
plt.axvline(np.mean(baseline_telemetry), color='#0284c7', linestyle='--')
plt.axvline(np.mean(production_telemetry), color='#ef4444', linestyle='--')

plt.title(f"Production Telemetry Distribution Drift (KS p-value = {p_value:.2e})", fontsize=13, fontweight='bold')
plt.xlabel("Sensor Physical Parameter Value")
plt.ylabel("Probability Density")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
"""
        exercise = """# Exercise Challenge:
# Trigger automated MLOps retraining alarm if p-value < 0.01
is_drift_detected = p_value < 0.01
print(f"MLOps Monitor Status: {'[CRITICAL ALARM] Automated Retraining Triggered' if is_drift_detected else '[NORMAL] Model Calibrated'}")
assert is_drift_detected, "Drift detection failed to trigger on shifted telemetry!"
print("✓ MLOps monitoring exercise passed.")
"""

    return theory, sim, viz, exercise

def build_single_notebook(lesson_data, github_user, github_repo, github_branch):
    """Compiles a complete, valid nbformat v4 notebook for one lesson."""
    nb = nbf.v4.new_notebook()

    # Standard Jupyter Notebook metadata
    nb["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.12"
        },
        "colab": {
            "provenance": [],
            "toc_visible": True
        }
    }

    lesson_id = lesson_data.get("id", "1-1")
    mod_num = lesson_data.get("module_number", int(lesson_id.split("-")[0]))
    les_num = int(lesson_id.split("-")[1])
    title_en = lesson_data.get("title_en", "Industrial ML Lesson")
    title_pl = lesson_data.get("title_pl", "")
    summary_en = lesson_data.get("summary_en", "")
    summary_pl = lesson_data.get("summary_pl", "")
    notebook_file = lesson_data.get("colab_notebook", f"lesson_{lesson_id}.ipynb")
    est_min = lesson_data.get("estimated_minutes", 20)
    checklist = lesson_data.get("checklist", [])

    colab_badge_url = f"https://colab.research.google.com/github/{github_user}/{github_repo}/blob/{github_branch}/public/notebooks/{notebook_file}"

    # 1. Header Markdown Cell
    header_md = f"""# Module {mod_num}.{les_num}: {title_en}
### 🇵🇱 {title_pl}

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_badge_url})

**Industrial Machine Learning & Predictive Maintenance Interactive Laboratory**

> **Summary:** {summary_en}  
> 🇵🇱 **Streszczenie:** {summary_pl}

- **Estimated Time:** {est_min} minutes
- **Runtime:** Python 3.10+ (CPU or Free Tier T4 GPU)
- **Packages:** `numpy`, `scipy`, `scikit-learn`, `pandas`, `matplotlib`, `seaborn`
---
"""
    nb.cells.append(nbf.v4.new_markdown_cell(header_md))

    # 2. Setup Code Cell
    setup_code = """# Step 1: Install & Verify Python Scientific Environment
!pip install -q numpy scipy scikit-learn pandas matplotlib seaborn

import numpy as np
import pandas as pd
import scipy.signal as signal
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'monospace'
print("✓ Industrial ML environment loaded successfully.")
"""
    nb.cells.append(nbf.v4.new_code_cell(setup_code))

    # 3. Domain Theory Markdown & Simulation Code
    theory_md, sim_code, viz_code, exercise_code = get_module_specific_code(mod_num, les_num, lesson_data)
    nb.cells.append(nbf.v4.new_markdown_cell(theory_md))
    nb.cells.append(nbf.v4.new_code_cell(sim_code))
    nb.cells.append(nbf.v4.new_code_cell(viz_code))

    # 4. Checklist Markdown Cell
    checklist_md = "## 📋 Practical Hands-On Checklist\n\n"
    if checklist:
        for idx, task in enumerate(checklist, start=1):
            checklist_md += f"- [ ] **Task {idx}:** {task.get('textEn', task.get('text_en', ''))} *(🇵🇱 {task.get('textPl', task.get('text_pl', ''))})*\n"
    else:
        checklist_md += "- [ ] Complete interactive simulation and verify numerical assertions.\n"
    nb.cells.append(nbf.v4.new_markdown_cell(checklist_md))

    # 5. Interactive Exercise Cell
    nb.cells.append(nbf.v4.new_code_cell(exercise_code))

    return nb

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    github_user, github_repo, github_branch = load_github_config()
    print(f"Building notebooks for {github_user}/{github_repo} on branch {github_branch}...")

    # Load lessons from src/data/lessons/ or fallback to syllabus.json
    lesson_files = sorted(LESSONS_DIR.glob("*.json"))
    lessons = []

    if lesson_files:
        for lf in lesson_files:
            with open(lf, "r", encoding="utf-8") as f:
                lessons.append(json.load(f))
    elif SYLLABUS_FILE.exists():
        with open(SYLLABUS_FILE, "r", encoding="utf-8") as f:
            syllabus = json.load(f)
        for mod in syllabus:
            for les in mod["lessons"]:
                lessons.append(les)

    print(f"Found {len(lessons)} lessons to build.")
    built_count = 0

    for lesson in lessons:
        filename = lesson.get("colab_notebook") or lesson.get("notebook")
        if not filename:
            filename = f"lesson_{lesson.get('id', '1-1')}.ipynb"
        
        target_path = OUTPUT_DIR / filename
        nb = build_single_notebook(lesson, github_user, github_repo, github_branch)
        
        with open(target_path, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
        
        built_count += 1
        les_id = lesson.get("id", "1-1")
        les_num = les_id.split("-")[1] if "-" in les_id else "?"
        mod_num = lesson.get("module_number", les_id.split("-")[0])
        print(f"  [✓] {filename} (Module {mod_num}.{les_num})")

    print(f"\nSuccessfully compiled {built_count} valid .ipynb notebooks in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
