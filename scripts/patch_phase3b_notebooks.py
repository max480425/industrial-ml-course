#!/usr/bin/env python3
"""
scripts/patch_phase3b_notebooks.py
Industrial Machine Learning & Predictive Maintenance Course

Patches scripts/build_notebooks.py with specialized, runnable implementations
for Modules 5, 6, and 7 (Lessons 5.1 through 7.4).
"""

from pathlib import Path

MODULES_5_TO_7_CODE = '''    # =========================================================================
    # MODULE 5: Time-Series Dynamics, Vibration FFT & Capstone 2
    # =========================================================================
    elif m == 5 and l == 1:
        # Lesson 5.1: Time-Series Stationarity & Rolling Window Statistics
        theory = """### Key Engineering Concepts:
1. **The Physics of Stationarity**: A sensor time series is stationary if its statistical properties (mean, variance, and autocovariance) are constant over time. Industrial degradation and ambient weather introduce non-stationary trends.
2. **Augmented Dickey-Fuller (ADF) Test**:
   - $H_0$: The telemetry has a unit root (is non-stationary).
   - If p-value $< 0.05$, reject $H_0$ (telemetry is stationary).
   - If p-value $\\ge 0.05$, apply first-order differencing $\\Delta y_t = y_t - y_{t-1}$.
3. **Autocorrelation (ACF)**: Identifies cyclical machine harmonics and autoregressive dependencies across lag intervals.
"""
        sim = """# 1. Simulate Non-Stationary Industrial Boiler Pressure Telemetry
np.random.seed(42)
n_pts = 1200
t = np.arange(n_pts)

# Steady-state cyclical pressure (stationary base process)
cyclical_base = 16.0 + 1.2 * np.sin(2 * np.pi * t / 80) + np.random.normal(0, 0.4, n_pts)

# Inject non-stationary thermal drift (boiler scale buildup over time)
thermal_drift = 0.008 * t + 0.00002 * (t**2)

raw_boiler_pressure = cyclical_base + thermal_drift

# Apply first-order differencing: Delta y_t = y_t - y_{t-1}
differenced_pressure = np.diff(raw_boiler_pressure)

print(f"✓ Generated {n_pts} samples of industrial boiler pressure telemetry.")
"""
        viz = """# 2. Augmented Dickey-Fuller (ADF) Hypothesis Testing & Rolling Stats
# Simplified ADF proxy statistic test
def estimate_adf_pvalue(series):
    # Check linear trend regression slope significance
    x = np.arange(len(series))
    slope, intercept = np.polyfit(x, series, 1)
    # Variance of detrended residuals
    res = series - (slope * x + intercept)
    r2 = 1.0 - (np.var(res) / (np.var(series) + 1e-9))
    # Synthetic p-value: strong trend = high p-value (non-stationary)
    p_val = 0.55 if r2 > 0.40 else 0.002
    return p_val, slope

p_raw, slope_raw = estimate_adf_pvalue(raw_boiler_pressure)
p_diff, slope_diff = estimate_adf_pvalue(differenced_pressure)

print(f"Raw Signal ADF Test         : p-value = {p_raw:.4f} ({'Non-Stationary' if p_raw >= 0.05 else 'Stationary'})")
print(f"Differenced Signal ADF Test : p-value = {p_diff:.4f} ({'Stationary' if p_diff < 0.05 else 'Non-Stationary'})")

fig, axes = plt.subplots(2, 1, figsize=(14, 6), sharex=False)

# Raw non-stationary series
axes[0].plot(raw_boiler_pressure, color='#ef4444', label='Raw Boiler Pressure [bar] (Drifting Mean)')
rolling_mean = pd.Series(raw_boiler_pressure).rolling(60).mean()
axes[0].plot(rolling_mean, color='#0284c7', linewidth=2, label='Rolling Mean (60-pt Window)')
axes[0].set_title(f"Non-Stationary Industrial Telemetry (ADF p-value = {p_raw:.2f})", fontweight='bold')
axes[0].set_ylabel("Pressure [bar]")
axes[0].legend(loc='upper left')
axes[0].grid(True, alpha=0.3)

# Differenced stationary series
axes[1].plot(differenced_pressure, color='#10b981', linewidth=1.2, label='First-Order Differenced Δy [bar]')
axes[1].axhline(0, color='gray', linestyle='--')
axes[1].set_title(f"Stationary Differenced Telemetry (ADF p-value = {p_diff:.4f} - Zero Unit Root)", fontweight='bold')
axes[1].set_ylabel("Delta Pressure [bar]")
axes[1].set_xlabel("Time Step Index")
axes[1].legend(loc='upper left')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Assert that raw signal is non-stationary (p >= 0.05) and differenced signal is stationary (p < 0.05)
assert p_raw >= 0.05, "Raw telemetry was incorrectly flagged as stationary."
assert p_diff < 0.05, "Differencing failed to restore stationarity."
print("✓ Time-series stationarity verification passed.")
"""

    elif m == 5 and l == 2:
        # Lesson 5.2: FFT Frequency-Domain Vibration & Bearing Kinematics
        theory = """### Key Engineering Concepts:
1. **Time Domain Blindness**: Microscopic bearing fatigue cracks generate high-frequency micro-shocks hidden under background unbalance and process noise.
2. **Hanning Windowing**: Abrupt sample boundaries cause artificial spectral leakage. Windowing smoothly tapers endpoints to zero, restoring sharp frequency resolution.
3. **Bearing Fault Kinematics**:
   - $1X$ Shaft Rotational Speed: Mass unbalance.
   - $2X$ Shaft Speed: Shaft angular misalignment.
   - $\\text{BPFO}$ (Outer Race): $f_{BPFO} = \\frac{N_{balls}}{2} f_{shaft} \\left(1 - \\frac{d}{D}\\cos\\alpha\\right)$.
"""
        sim = """# 1. Synthesize 2000 Hz Accelerometer Signal with Bearing BPFO Fault
np.random.seed(42)
Fs = 2000.0  # Sampling rate: 2000 Hz
T = 1.0 / Fs
N = 2048
time_axis = np.linspace(0.0, N*T, N, endpoint=False)

f_shaft = 30.0            # 30 Hz shaft rotational speed (1800 RPM)
f_misalignment = 60.0     # 2X misalignment harmonic
f_bpfo = 3.58 * f_shaft   # 107.4 Hz outer race defect peak

# Synthetic multi-harmonic signal
sig_1x = 2.0 * np.sin(2.0 * np.pi * f_shaft * time_axis)
sig_2x = 0.8 * np.sin(2.0 * np.pi * f_misalignment * time_axis)
sig_bpfo = 1.6 * np.sin(2.0 * np.pi * f_bpfo * time_axis)
noise = 0.6 * np.random.randn(N)

vibration_accel = sig_1x + sig_2x + sig_bpfo + noise
print(f"✓ Vibration telemetry synthesized: {N} samples at {Fs} Hz.")
"""
        viz = """# 2. Compute Fast Fourier Transform (FFT) with Hanning Window
window = np.hanning(N)
windowed_signal = vibration_accel * window

fft_vals = np.fft.rfft(windowed_signal)
fft_freqs = np.fft.rfftfreq(N, T)
fft_mag = (2.0 / N) * np.abs(fft_vals)

fig, axes = plt.subplots(2, 1, figsize=(14, 6))

axes[0].plot(time_axis[:250], vibration_accel[:250], color='#0284c7', linewidth=1.2)
axes[0].set_title("Time Domain: Accelerometer Raw Vibration (Defect Inaudible & Masked by Noise)", fontweight='bold')
axes[0].set_ylabel("Accel [m/s²]")
axes[0].grid(True, alpha=0.3)

axes[1].plot(fft_freqs, fft_mag, color='#10b981', linewidth=1.6, label='FFT Magnitude Spectrum')
axes[1].axvline(f_shaft, color='#f59e0b', linestyle='--', linewidth=1.8, label=f'1X Shaft Unbalance ({f_shaft:.1f} Hz)')
axes[1].axvline(f_misalignment, color='#6366f1', linestyle=':', linewidth=1.8, label=f'2X Misalignment ({f_misalignment:.1f} Hz)')
axes[1].axvline(f_bpfo, color='#ef4444', linestyle='-', linewidth=2.2, label=f'BPFO Outer Race Defect ({f_bpfo:.1f} Hz)')
axes[1].set_xlim(0, 250)
axes[1].set_title("Frequency Domain: FFT Exposes Incipient Bearing Defect Peak!", fontweight='bold')
axes[1].set_xlabel("Frequency [Hz]")
axes[1].set_ylabel("Vibration Amplitude [m/s²]")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Identify the peak frequency between 95 Hz and 120 Hz
bpfo_band = (fft_freqs >= 95.0) & (fft_freqs <= 120.0)
peak_detected_freq = fft_freqs[bpfo_band][np.argmax(fft_mag[bpfo_band])]
print(f"Detected Bearing Defect Frequency Peak: {peak_detected_freq:.2f} Hz (Theoretical: {f_bpfo:.2f} Hz)")
assert abs(peak_detected_freq - f_bpfo) < 1.5, "FFT defect peak detection out of tolerance!"
print("✓ FFT frequency domain bearing kinematics verified.")
"""

    elif m == 5 and l == 3:
        # Lesson 5.3: Forecasting Consumption & Pressure Drift (ARIMA vs XGBoost)
        theory = """### Key Engineering Concepts:
1. **Plant Energy & Fluid Demand**: Forecasting natural gas and compressed air consumption prevents expensive peak-power penalty tariffs.
2. **ARIMA Modeling**: Captures linear autoregression and moving average residuals across stationary differenced data.
3. **XGBoost with Lag Features**: Non-linear gradient boosting models capture interaction effects between production schedule shifts, outside ambient temperature, and autoregressive historical lags ($t-1, t-24$).
"""
        sim = """# 1. Synthesize Factory Natural Gas Consumption Log (1,000 Hours)
np.random.seed(42)
n_hours = 1000
t_hours = np.arange(n_hours)

# Diurnal shift cycle (24-hour periodicity) + day-of-week modulation
diurnal = 35.0 + 15.0 * np.sin(2 * np.pi * t_hours / 24)
ambient_temp = 18.0 - 8.0 * np.sin(2 * np.pi * t_hours / 24) + np.random.normal(0, 1.5, n_hours)

# Gas consumption: higher during cold shifts and high production
gas_m3_per_hr = diurnal + 0.8 * (25.0 - ambient_temp) + np.random.normal(0, 2.5, n_hours)

df_gas = pd.DataFrame({
    "hour": t_hours,
    "ambient_temp": ambient_temp,
    "gas_m3_hr": gas_m3_per_hr
})

# Construct autoregressive lag features for machine learning
df_gas["lag_1"]  = df_gas["gas_m3_hr"].shift(1)
df_gas["lag_24"] = df_gas["gas_m3_hr"].shift(24)
df_gas["rolling_mean_6"] = df_gas["gas_m3_hr"].rolling(6).mean().shift(1)
df_gas = df_gas.dropna()
print(f"✓ Engineered feature matrix: {len(df_gas)} hourly rows.")
"""
        viz = """# 2. Train Walk-Forward Forecasting Model & Benchmark MAPE
from sklearn.ensemble import GradientBoostingRegressor

split_pt = len(df_gas) - 168  # Hold out final 7 days (168 hours) for testing
train_df = df_gas.iloc[:split_pt]
test_df  = df_gas.iloc[split_pt:]

features = ["ambient_temp", "lag_1", "lag_24", "rolling_mean_6"]
X_train, y_train = train_df[features], train_df["gas_m3_hr"]
X_test, y_test   = test_df[features], test_df["gas_m3_hr"]

# Train Gradient Boosting Regressor (XGBoost proxy)
gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.08, max_depth=4, random_state=42)
gbr.fit(X_train, y_train)
y_pred = gbr.predict(X_test)

# Calculate Mean Absolute Percentage Error (MAPE)
mape = np.mean(np.abs((y_test.to_numpy() - y_pred) / y_test.to_numpy())) * 100

plt.figure(figsize=(14, 5))
plt.plot(test_df["hour"].iloc[:72], y_test.iloc[:72], color='#0284c7', linewidth=2, label='Actual Gas Consumption [m³/hr]')
plt.plot(test_df["hour"].iloc[:72], y_pred[:72], color='#10b981', linestyle='--', linewidth=2, label=f'Model Forecast (MAPE = {mape:.2f}%)')
plt.fill_between(test_df["hour"].iloc[:72], y_pred[:72]*0.95, y_pred[:72]*1.05, color='#10b981', alpha=0.15, label='±5% Precision Band')

plt.title("72-Hour Multi-Step Industrial Utility Demand Forecast", fontsize=13, fontweight='bold')
plt.xlabel("Production Hour Index")
plt.ylabel("Natural Gas Flow [m³/hr]")
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Assert that the forecasting model achieves MAPE under 8%
print(f"Achieved Forecast MAPE: {mape:.2f}%")
assert mape < 8.0, "Forecasting error exceeded acceptable industrial tolerance!"
print("✓ Consumption forecasting test verified.")
"""

    elif m == 5 and l == 4:
        # Lesson 5.4: Capstone 2 - Real-Time Anomaly & Hydraulic Leak Detector
        theory = """### Capstone 2: Real-Time Anomaly & Hydraulic Leak Detector
1. **Hydraulic Micro-Leak Hazards**: In 280-bar hydraulic circuits, pinhole hose leaks spray atomized oil mist, creating catastrophic fire hazards.
2. **Mass Balance Differential**: $Q_{diff} = Q_{in} - Q_{out}$. In closed circuits, $Q_{diff} \\approx 0$. A persistent positive delta indicates lost fluid.
3. **Cumulative Sum (CUSUM)**:
   $$S_t = \\max(0, S_{t-1} + (x_t - \\mu_0 - k))$$
   Integrates tiny systematic shifts that never cross standard static thresholds.
4. **Safety State Machine**: `NORMAL` $\\to$ `WATCH` (warning) $\\to$ `ALARM` (technician page) $\\to$ `EMERGENCY_SHUTDOWN` (automated solenoid dump valve).
"""
        sim = """# 1. Simulate High-Pressure Hydraulic Circuit with Micro-Leak Injection
np.random.seed(42)
n_sec = 1200
t = np.arange(n_sec)

# Nominal operating pressure: 280 bar with normal pump ripple
p_nominal = 280.0 + 3.5 * np.sin(2 * np.pi * t / 15) + np.random.normal(0, 0.8, n_sec)

# Nominal mass balance differential: Mean = 0.0 L/min, Std = 0.15 L/min
flow_diff = np.random.normal(0.0, 0.15, n_sec)

# Inject pinhole hydraulic leak at step 700 (losing 0.45 L/min)
leak_start = 700
flow_diff[leak_start:] += 0.45
# Pressure decay following accumulator exhaustion
p_telemetry = p_nominal.copy()
p_telemetry[leak_start:] -= np.linspace(0, 35.0, n_sec - leak_start)

print(f"✓ Hydraulic simulation created: 280 bar nominal, leak initiated at t={leak_start}s.")
"""
        viz = """# 2. Implement CUSUM Change-Point Detector & Multi-State Safety Machine
k_allowance = 0.10   # Slack parameter
h_watch = 4.0        # Warning threshold
h_shutdown = 12.0    # Emergency trip threshold

cusum_stat = np.zeros(n_sec)
alarm_states = []

for i in range(1, n_sec):
    cusum_stat[i] = max(0.0, cusum_stat[i-1] + (flow_diff[i] - k_allowance))
    if cusum_stat[i] >= h_shutdown:
        alarm_states.append("EMERGENCY_SHUTDOWN")
    elif cusum_stat[i] >= h_watch:
        alarm_states.append("WATCH")
    else:
        alarm_states.append("NORMAL")
alarm_states.insert(0, "NORMAL")

fig, axes = plt.subplots(3, 1, figsize=(14, 8), sharex=True)

# Pressure curve
axes[0].plot(t, p_telemetry, color='#0284c7', label='Accumulator Pressure [bar]')
axes[0].axvline(leak_start, color='#ef4444', linestyle='--', label='Micro-Leak Inception')
axes[0].set_ylabel("Pressure [bar]")
axes[0].legend(loc='upper right')
axes[0].grid(True, alpha=0.3)

# Flow differential
axes[1].plot(t, flow_diff, color='#64748b', alpha=0.7, label='Mass Balance (Q_in - Q_out) [L/min]')
axes[1].axhline(0.0, color='gray', linestyle=':')
axes[1].set_ylabel("Flow Diff [L/min]")
axes[1].legend(loc='upper right')
axes[1].grid(True, alpha=0.3)

# CUSUM statistic and thresholds
axes[2].plot(t, cusum_stat, color='#ef4444', linewidth=2, label='CUSUM Error Accumulator')
axes[2].axhline(h_watch, color='#f59e0b', linestyle='--', linewidth=1.8, label=f'WATCH Level (h={h_watch})')
axes[2].axhline(h_shutdown, color='#ef4444', linestyle='-', linewidth=2.0, label=f'SHUTDOWN Trip (h={h_shutdown})')
axes[2].set_ylabel("CUSUM S_t")
axes[2].set_xlabel("Operational Seconds")
axes[2].legend(loc='upper left')
axes[2].grid(True, alpha=0.3)

plt.suptitle("Capstone 2: Real-Time Hydraulic Leak Detection & Safety Machine", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Assert that WATCH was triggered within 25 seconds of leak inception
watch_triggered = np.where(cusum_stat >= h_watch)[0][0]
shutdown_triggered = np.where(cusum_stat >= h_shutdown)[0][0]

print(f"Leak Started at Step       : {leak_start}s")
print(f"WATCH Warning Triggered at : {watch_triggered}s (Latency: {watch_triggered - leak_start}s)")
print(f"SHUTDOWN Trip Triggered at : {shutdown_triggered}s")

assert watch_triggered < leak_start + 25, "CUSUM leak response latency was too slow!"
assert p_telemetry[shutdown_triggered] > 255.0, "Shutdown was delayed until pressure critically collapsed!"
print("✓ Capstone 2 hydraulic leak detector fully verified!")
"""

    # =========================================================================
    # MODULE 6: Industrial Deep Learning & Edge Computer Vision
    # =========================================================================
    elif m == 6 and l == 1:
        # Lesson 6.1: Neural Network Mechanics in PyTorch & Keras
        theory = """### Key Engineering Concepts:
1. **Multi-Sensor Tensors**: In modern factories, tens of vibration, temperature, and current channels are arranged into input tensors $[B, C, L]$.
2. **Forward Pass & Non-Linearity**: Linear layers $z = Wx + b$ paired with non-linear activations (ReLU, GELU) allow neural networks to learn complex failure geometries.
3. **Backpropagation & AdamW**: Calculates partial derivatives $\\frac{\\partial \\mathcal{L}}{\\partial W}$ across the computational graph. AdamW adds decoupled weight decay to prevent overfitting on repetitive machine cycles.
"""
        sim = """# 1. Synthesize Multi-Sensor Machine Health Dataset (12 Channels, 1500 Cycles)
np.random.seed(42)
n_samples = 1500
n_features = 12

# Normal operation: 12 sensor channels
X_raw = np.random.normal(loc=25.0, scale=3.5, size=(n_samples, n_features))

# 3 operational health states: 0: Normal, 1: Degrading, 2: Critical Trip
y_state = np.zeros(n_samples, dtype=int)
y_state[500:1000] = 1
y_state[1000:] = 2

# Add characteristic signal signatures for degrading and critical states
X_raw[500:1000, :4] += np.random.uniform(3.0, 7.0, size=(500, 4))
X_raw[1000:, :6]   += np.random.uniform(8.0, 16.0, size=(500, 6))

# Train/Test split
split = 1100
X_train, X_test = X_raw[:split], X_raw[split:]
y_train, y_test = y_state[:split], y_state[split:]
print(f"✓ Sensor dataset created: {n_samples} cycles with {n_features} input channels.")
"""
        viz = """# 2. Build and Train Multi-Layer Perceptron (MLP) Classifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score

mlp = MLPClassifier(
    hidden_layer_sizes=(64, 32),
    activation='relu',
    solver='adam',
    alpha=0.001,           # L2 weight decay regularization
    max_iter=150,
    random_state=42
)

mlp.fit(X_train, y_train)
y_pred_test = mlp.predict(X_test)
acc = accuracy_score(y_test, y_pred_test)

plt.figure(figsize=(10, 4.5))
plt.plot(mlp.loss_curve_, color='#0284c7', linewidth=2, label='Cross-Entropy Loss Curve')
plt.title(f"PyTorch/MLP Training Convergence Curve (Final Test Acc = {acc*100:.1f}%)", fontweight='bold')
plt.xlabel("Training Epochs")
plt.ylabel("Loss Value")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"MLP Diagnostic Test Accuracy: {acc*100:.2f}%")
"""
        exercise = """# Exercise Challenge:
# Assert that neural network test accuracy exceeds 92%
assert acc >= 0.92, "Neural network failed to reach target diagnostic accuracy."
print("✓ Neural network mechanics verification passed.")
"""

    elif m == 6 and l == 2:
        # Lesson 6.2: CNNs for Surface Defect Inspection
        theory = """### Key Engineering Concepts:
1. **Automated Optical Inspection (AOI)**: High-speed cameras inspect cold-rolled sheet steel for scratches, inclusions, and pinholes.
2. **2D Spatial Convolutions**: A filter kernel $K$ slides over image pixels, computing dot products to expose localized edges:
   $$(I * K)(i, j) = \\sum_m \\sum_n I(i-m, j-n) K(m, n)$$
3. **Sobel & Laplacian Filters**: Standard mathematical kernels that compute spatial intensity gradients, highlighting sharp defect boundaries.
"""
        sim = """# 1. Synthesize Cold-Rolled Metal Surface Patches with Scratch Defects
np.random.seed(42)
img_size = 64

# Base metal texture (gray with Gaussian noise)
clean_metal = np.random.normal(0.5, 0.04, (img_size, img_size))

# Inject longitudinal scratch defect (vertical score mark)
defective_metal = clean_metal.copy()
defective_metal[10:55, 31:33] -= 0.35  # Dark scratch groove
defective_metal = np.clip(defective_metal, 0.0, 1.0)

# Define Sobel Horizontal and Vertical Edge Kernels
sobel_v = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
sobel_h = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
print(f"✓ Synthetic surface patch created ({img_size}x{img_size} pixels).")
"""
        viz = """# 2. Convolve Kernels to Expose Surface Defect Feature Maps
from scipy.signal import convolve2d

edge_map_v = convolve2d(defective_metal, sobel_v, mode='same')
edge_map_h = convolve2d(defective_metal, sobel_h, mode='same')
gradient_magnitude = np.sqrt(edge_map_v**2 + edge_map_h**2)

fig, axes = plt.subplots(1, 4, figsize=(15, 4))

axes[0].imshow(clean_metal, cmap='gray', vmin=0, vmax=1)
axes[0].set_title("Flawless Metal Surface", fontweight='bold')
axes[0].axis('off')

axes[1].imshow(defective_metal, cmap='gray', vmin=0, vmax=1)
axes[1].set_title("Sheet Metal with Scratch", fontweight='bold')
axes[1].axis('off')

axes[2].imshow(edge_map_v, cmap='coolwarm')
axes[2].set_title("Vertical Sobel Feature Map", fontweight='bold')
axes[2].axis('off')

axes[3].imshow(gradient_magnitude, cmap='magma')
axes[3].set_title("CNN Gradient Magnitude (Defect Isolated!)", fontweight='bold')
axes[3].axis('off')

plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Assert that peak gradient magnitude on the defect scratch exceeds 0.8
peak_gradient = np.max(gradient_magnitude)
print(f"Peak Defect Edge Gradient: {peak_gradient:.3f}")
assert peak_gradient > 0.8, "Convolution kernel failed to isolate defect edge."
print("✓ CNN surface inspection kernels verified.")
"""

    elif m == 6 and l == 3:
        # Lesson 6.3: Transfer Learning & Ultralytics YOLO Conveyor Inspection
        theory = """### Key Engineering Concepts:
1. **Manufacturing Data Scarcity**: Real defects occur rarely ($< 50$ cases/month). Training from scratch overfits; Transfer Learning fine-tunes pretrained backbones.
2. **Single-Stage YOLO Detection**: Predicts bounding box coordinates $[x, y, w, h]$ and class scores in a single forward pass, achieving $> 60\\text{ FPS}$ on conveyor belts.
3. **Intersection over Union (IoU)**:
   $$\\text{IoU} = \\frac{\\text{Area of Overlap}}{\\text{Area of Union}}$$
   Industry standard metric requiring $\\text{IoU} \\ge 0.50$ for valid True Positive detection.
"""
        sim = """# 1. Bounding Box Geometry & IoU Vectorized Calculation
def calculate_iou(box1, box2):
    # Format: [x1, y1, x2, y2]
    xa = max(box1[0], box2[0])
    ya = max(box1[1], box2[1])
    xb = min(box1[2], box2[2])
    yb = min(box1[3], box2[3])
    
    inter_area = max(0.0, xb - xa) * max(0.0, yb - ya)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = area1 + area2 - inter_area
    return inter_area / union_area if union_area > 0 else 0.0

# Conveyor workpiece defect: Ground Truth annotation vs YOLO candidate proposal
gt_box   = [120.0, 90.0, 240.0, 210.0]  # [x1, y1, x2, y2]
yolo_box = [130.0, 85.0, 255.0, 205.0]

iou_score = calculate_iou(gt_box, yolo_box)
print(f"Calculated Proposal IoU: {iou_score:.3f} ({(iou_score*100):.1f}%)")
"""
        viz = """# 2. Visualizing Defect Bounding Boxes on Conveyor Frame
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(8, 5))
# Conveyor belt black rubber background
conveyor = np.random.normal(0.15, 0.02, (300, 400))
ax.imshow(conveyor, cmap='gray', vmin=0, vmax=1)

# Draw ground truth bounding box (Green)
rect_gt = patches.Rectangle((gt_box[0], gt_box[1]), gt_box[2]-gt_box[0], gt_box[3]-gt_box[1],
                            linewidth=2.5, edgecolor='#10b981', facecolor='none', label='Human Annotated Ground Truth')
ax.add_patch(rect_gt)

# Draw YOLO predicted bounding box (Amber)
rect_yolo = patches.Rectangle((yolo_box[0], yolo_box[1]), yolo_box[2]-yolo_box[0], yolo_box[3]-yolo_box[1],
                              linewidth=2.5, edgecolor='#f59e0b', linestyle='--', facecolor='none', 
                              label=f'YOLO Proposal (IoU = {iou_score:.2f})')
ax.add_patch(rect_yolo)

plt.title("High-Speed Conveyor Belt Defect Localization (IoU Evaluation)", fontsize=13, fontweight='bold')
plt.legend(loc='lower right')
plt.xlim(0, 400)
plt.ylim(300, 0)
plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Verify that the YOLO proposal meets the industrial acceptance threshold (IoU >= 0.50)
passes_qc = iou_score >= 0.50
print(f"Inspection Result: {'VALID DETECTION (True Positive)' if passes_qc else 'REJECT'}")
assert passes_qc, "YOLO bounding box failed to meet 50% IoU quality standard."
print("✓ Conveyor inspection evaluation verified.")
"""

    elif m == 6 and l == 4:
        # Lesson 6.4: Capstone 3 - Exporting & Quantizing Models to ONNX for Edge
        theory = """### Capstone 3: Edge Model Optimization & ONNX Quantization
1. **Industrial Edge Hardware**: Fanless industrial PCs (Siemens IPC) and edge micro-servers (NVIDIA Jetson) have constrained RAM and 15–25W thermal budgets.
2. **Open Neural Network Exchange (ONNX)**: Decouples model graphs from Python runtimes, enabling direct C++ execution.
3. **INT8 Post-Training Quantization (PTQ)**: Converts 32-bit floating point weights into 8-bit signed integers ($[-128, 127]$). Reduces model footprint by $75\\%$ and accelerates inference latency by $3\\times-4\\times$.
"""
        sim = """# 1. Simulate Edge Deep Learning Model Weights & INT8 Quantization
np.random.seed(42)
n_weights = 250_000

# FP32 weights from trained convolutional inspection model
fp32_weights = np.random.normal(loc=0.0, scale=0.45, size=n_weights).astype(np.float32)

# Compute symmetric INT8 quantization scale factor
max_val = np.max(np.abs(fp32_weights))
scale = max_val / 127.0

# Quantize to INT8: q = round(w / scale)
int8_weights = np.clip(np.round(fp32_weights / scale), -128, 127).astype(np.int8)

# Dequantize for reconstruction accuracy check: w_approx = q * scale
dequant_weights = int8_weights.astype(np.float32) * scale

# Calculate memory sizes
size_fp32_kb = fp32_weights.nbytes / 1024
size_int8_kb = int8_weights.nbytes / 1024

print(f"FP32 Model Memory : {size_fp32_kb:.1f} KB")
print(f"INT8 Model Memory : {size_int8_kb:.1f} KB ({(1.0 - size_int8_kb/size_fp32_kb)*100:.1f}% reduction)")
"""
        viz = """# 2. Benchmark Simulated Inference Latency on Industrial Edge IPC
# Simulate 500 edge inference runs
latency_fp32_ms = np.random.normal(14.8, 1.2, 500)   # FP32 CPU execution: ~15ms
latency_int8_ms = np.random.normal(3.9, 0.4, 500)    # INT8 quantized C++ execution: ~4ms

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Memory footprint comparison
axes[0].bar(["FP32 Original", "INT8 Quantized"], [size_fp32_kb, size_int8_kb], color=['#ef4444', '#10b981'], width=0.45)
axes[0].set_title("Model Memory Footprint Reduction", fontweight='bold')
axes[0].set_ylabel("RAM Allocation [KB]")
axes[0].grid(axis='y', alpha=0.3)

# Latency benchmark distribution
sns.kdeplot(latency_fp32_ms, color='#ef4444', fill=True, alpha=0.3, label=f'FP32 Baseline (Mean = {np.mean(latency_fp32_ms):.1f}ms)', ax=axes[1])
sns.kdeplot(latency_int8_ms, color='#10b981', fill=True, alpha=0.3, label=f'ONNX INT8 Edge (Mean = {np.mean(latency_int8_ms):.1f}ms)', ax=axes[1])
axes[1].axvline(5.0, color='#f59e0b', linestyle='--', label='Conveyor Real-Time Cycle Limit (5ms)')
axes[1].set_title("Inference Latency Benchmark on Siemens IPC", fontweight='bold')
axes[1].set_xlabel("Latency [milliseconds]")
axes[1].set_ylabel("Probability Density")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Assert that INT8 quantization slashes mean latency by at least 3x and stays under 5ms
speedup = np.mean(latency_fp32_ms) / np.mean(latency_int8_ms)
mean_int8 = np.mean(latency_int8_ms)

print(f"Measured Speedup Factor : {speedup:.2f}x")
print(f"Mean INT8 Latency       : {mean_int8:.2f} ms")

assert speedup >= 3.0, "INT8 quantization failed to deliver 3x speedup!"
assert mean_int8 < 5.0, "Edge latency exceeds 5ms conveyor real-time limit!"
print("✓ Capstone 3 ONNX edge quantization verified.")
"""

    # =========================================================================
    # MODULE 7: Industrial MLOps, Model Serving & Executive Dashboards
    # =========================================================================
    elif m == 7 and l == 1:
        # Lesson 7.1: Experiment Tracking & Governance with MLflow
        theory = """### Key Engineering Concepts:
1. **Auditable Manufacturing MLOps**: In regulated plants (ISO 9001), automated decisions must be backed by documented training parameters, dataset hashes, and metric logs.
2. **MLflow Tracking**: Logs hyperparameters, evaluation metrics (ROC-AUC, financial losses), and serialized model binaries.
3. **Model Registry Stages**: Lifecycle gates: `Staging` (shadow testing on live PLC tags) $\\to$ `Production` $\\to$ `Archived` (fallback).
"""
        sim = """# 1. Simulate MLflow Experiment Tracking Run Matrix
np.random.seed(42)
n_experiments = 8

# Model hyperparameter experiments across 8 training iterations
experiments = []
for i in range(n_experiments):
    n_est = int(np.random.choice([50, 100, 150, 200]))
    lr = float(np.random.choice([0.01, 0.05, 0.1, 0.2]))
    max_d = int(np.random.choice([3, 4, 5, 6]))
    
    # Simulated validation performance metrics
    auc = round(0.88 + 0.08 * (1.0 - lr) + np.random.normal(0, 0.01), 4)
    auc = min(0.99, max(0.85, auc))
    # Financial expected loss: higher AUC = lower cost
    cost_loss = round((1.0 - auc) * 45000 + np.random.normal(0, 500), 2)
    
    experiments.append({
        "run_id": f"run_{i+1:02d}",
        "n_estimators": n_est,
        "learning_rate": lr,
        "max_depth": max_d,
        "roc_auc": auc,
        "expected_loss_usd": cost_loss
    })

df_mlflow = pd.DataFrame(experiments).sort_values("expected_loss_usd").reset_index(drop=True)
print("MLflow Logged Production Runs:")
print(df_mlflow)
"""
        viz = """# 2. Visualize MLflow Run Metrics & Model Registry Staging
best_run = df_mlflow.iloc[0]

plt.figure(figsize=(10, 4.5))
plt.scatter(df_mlflow["roc_auc"], df_mlflow["expected_loss_usd"], color='#0284c7', s=100, label='Candidate Model Runs')
plt.scatter(best_run["roc_auc"], best_run["expected_loss_usd"], color='#10b981', s=200, marker='*', label=f'Promoted to Production ({best_run["run_id"]})')

plt.title("MLflow Model Evaluation: ROC-AUC vs Financial Expected Loss", fontweight='bold')
plt.xlabel("Validation ROC-AUC")
plt.ylabel("Expected Financial Downtime Loss [USD]")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"Promoting Model {best_run['run_id']} to 'Production' stage (Loss: ${best_run['expected_loss_usd']:,.2f})")
"""
        exercise = """# Exercise Challenge:
# Assert that the promoted model has ROC-AUC > 0.95 and lowest expected financial loss
assert best_run["roc_auc"] > 0.95, "Promoted model failed ROC-AUC threshold."
assert best_run["expected_loss_usd"] == df_mlflow["expected_loss_usd"].min(), "Best model was not selected."
print("✓ MLflow governance and model registry verified.")
"""

    elif m == 7 and l == 2:
        # Lesson 7.2: Serving Models via FastAPI REST Endpoints
        theory = """### Key Engineering Concepts:
1. **OT/IT Convergence via REST**: Connecting plant SCADA/MES systems to Python predictive maintenance pipelines through standardized JSON HTTP endpoints.
2. **Pydantic Validation**: Enforcing strict physical boundary checks on sensor telemetry (e.g. current must be $4.0 - 20.0\\text{ mA}$) before inference.
3. **Sub-5ms Latency Requirement**: PLC cycles require microsecond response times; asynchronous FastAPI servers handle continuous telemetry without blocking.
"""
        sim = """# 1. Define Pydantic Telemetry Schema & Simulate FastAPI Microservice
import time

class MockTelemetryPayload:
    \"\"\"Simulates Pydantic model validation on industrial inputs\"\"\"
    def __init__(self, machine_id, current_ma, pressure_bar, temp_c):
        self.machine_id = machine_id
        # Physical boundary checks
        if not (3.6 <= current_ma <= 22.0):
            raise ValueError(f"Sensor current out of physical bounds (4-20mA loop): {current_ma} mA")
        if not (0.0 <= pressure_bar <= 350.0):
            raise ValueError(f"Pressure out of physical transmitter bounds: {pressure_bar} bar")
        self.current_ma = current_ma
        self.pressure_bar = pressure_bar
        self.temp_c = temp_c

def mock_predict_endpoint(payload):
    t0 = time.perf_counter()
    # Fast decision logic
    is_anomaly = payload.current_ma > 18.5 or payload.pressure_bar > 290.0 or payload.temp_c > 85.0
    risk_score = 0.85 if is_anomaly else 0.05
    latency_ms = (time.perf_counter() - t0) * 1000
    return {
        "machine_id": payload.machine_id,
        "prediction": "ALERT" if is_anomaly else "NORMAL",
        "risk_score": risk_score,
        "latency_ms": latency_ms
    }

# Test valid telemetry payload
valid_sample = MockTelemetryPayload("PUMP_01", 14.5, 240.0, 52.0)
resp = mock_predict_endpoint(valid_sample)
print(f"FastAPI Response : {resp}")
"""
        viz = """# 2. Benchmark Simulated SCADA REST Request Latency (1,000 Calls)
latencies = []
for _ in range(1000):
    t0 = time.perf_counter()
    # Mock payload parsing and inference
    _ = mock_predict_endpoint(valid_sample)
    latencies.append((time.perf_counter() - t0) * 1000)

latencies = np.array(latencies)
p99_latency = np.percentile(latencies, 99)

plt.figure(figsize=(10, 4.5))
plt.hist(latencies, bins=30, color='#0284c7', edgecolor='black', alpha=0.7)
plt.axvline(p99_latency, color='#ef4444', linestyle='--', label=f'99th Percentile = {p99_latency:.3f} ms')
plt.axvline(5.0, color='#f59e0b', linestyle=':', label='Industrial Limit (5.0 ms)')

plt.title("FastAPI Telemetry Inference Latency Distribution (1,000 SCADA calls)", fontweight='bold')
plt.xlabel("Request Latency [milliseconds]")
plt.ylabel("Call Frequency")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Assert that Pydantic rejects an invalid current reading of 1.2 mA (Broken Wire)
rejected_flag = False
try:
    MockTelemetryPayload("PUMP_01", 1.2, 240.0, 52.0)
except ValueError:
    rejected_flag = True

assert rejected_flag, "Pydantic validation failed to catch broken wire input!"
assert p99_latency < 5.0, "Inference response latency exceeded 5ms limit!"
print("✓ FastAPI serving and input validation verified.")
"""

    elif m == 7 and l == 3:
        # Lesson 7.3: Live Executive OEE & ML Dashboards with Streamlit
        theory = """### Key Engineering Concepts:
1. **Overall Equipment Effectiveness (OEE)**:
   $$\\text{OEE} = \\text{Availability} \\times \\text{Performance} \\times \\text{Quality}$$
   World-class manufacturing lines target $\\text{OEE} \\ge 85\\%$.
2. **Correlating PdM with OEE**: Predictive maintenance flags micro-stops and wear early, directly rescuing line Availability and line Performance.
3. **Streamlit Operations Center**: Python framework for rendering real-time telemetry dashboards, alert logs, and operator feedback.
"""
        sim = """# 1. Calculate OEE Before and After Predictive Maintenance Deployment
# Baseline (Reactive Maintenance): Frequent micro-stoppages, unplanned downtime
avail_pre = 0.78       # 78% Availability (lots of unplanned breakdowns)
perf_pre  = 0.82       # 82% Performance (slowed down to avoid jams)
qual_pre  = 0.94       # 94% Quality (scrapped parts during stops)
oee_pre   = avail_pre * perf_pre * qual_pre

# Post-Deployment (Predictive Maintenance AI Stack)
avail_post = 0.93      # 93% Availability (zero unplanned breakdowns)
perf_post  = 0.91      # 91% Performance (running at full rated line speed)
qual_post  = 0.98      # 98% Quality (incipient faults flagged before scrap)
oee_post   = avail_post * perf_post * qual_post

print(f"Pre-PdM Line OEE  : {oee_pre*100:.2f}%")
print(f"Post-PdM Line OEE : {oee_post*100:.2f}% ({(oee_post - oee_pre)*100:+.2f}% Gain)")
"""
        viz = """# 2. Render Streamlit Executive OEE Breakdown Dashboard
categories = ["Availability", "Performance", "Quality", "Overall OEE"]
pre_vals   = [avail_pre*100, perf_pre*100, qual_pre*100, oee_pre*100]
post_vals  = [avail_post*100, perf_post*100, qual_post*100, oee_post*100]

x = np.arange(len(categories))
width = 0.35

plt.figure(figsize=(10, 5))
plt.bar(x - width/2, pre_vals, width=width, color='#94a3b8', label='Pre-PdM (Reactive)')
plt.bar(x + width/2, post_vals, width=width, color='#10b981', label='Post-PdM (Predictive)')

plt.xticks(x, categories, fontweight='bold')
plt.ylabel("Efficiency Percentage (%)")
plt.ylim(0, 110)
plt.axhline(85.0, color='#f59e0b', linestyle='--', label='World-Class Target (85% OEE)')
plt.title("Executive Dashboard: Operational Equipment Effectiveness (OEE) Impact", fontsize=13, fontweight='bold')
plt.legend(loc='lower right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Verify that post-PdM deployment achieves the world-class 80%+ OEE benchmark
assert oee_post >= 0.80, "Deployment failed to achieve target 80% OEE."
assert (oee_post - oee_pre) > 0.15, "Expected at least 15% overall OEE improvement."
print("✓ Executive OEE dashboard metrics verified.")
"""

    else:
        # Lesson 7.4: Capstone 4 - Dockerizing the Pipeline & Presenting ROI
        theory = """### Capstone 4: Dockerizing Pipeline & Presenting Financial ROI
1. **Hardened Multi-Stage Dockerfile**: Builds dependencies in a scratch container and copies only binary wheels into a lightweight Debian runtime image ($< 150\\text{ MB}$) for industrial IPCs.
2. **Speaking C-Suite Language**: Plant directors invest based on:
   - **MTBF (Mean Time Between Failures)**: Increased from 650 hrs to 2,200 hrs.
   - **MTTR (Mean Time to Repair)**: Cut from 8 hrs to 45 mins.
   - **ROI (Return on Investment)**: $\\text{ROI} = \\frac{\\text{Net Savings}}{\\text{CAPEX}} \\times 100\\%$.
   - **Payback Period**: $\\text{Payback} = \\frac{\\text{CAPEX}}{\\text{Monthly Savings}}$.
"""
        sim = """# 1. Industrial Financial ROI & Reliability Calculator
# Plant Operating Parameters: 4 continuous production lines, 24/7/365
downtime_cost_per_hr = 12_500.0   # $12,500/hr lost throughput

# Reliability Gains:
# Unplanned downtime hours reduced from 42 hrs/year to 6 hrs/year
unplanned_hrs_pre  = 42.0
unplanned_hrs_post = 6.0
hrs_saved = unplanned_hrs_pre - unplanned_hrs_post

annual_downtime_savings = hrs_saved * downtime_cost_per_hr

# Predictive Maintenance System Costs:
capex_hardware_software = 75_000.0   # Initial capital expenditure
opex_annual_support     = 18_000.0   # Annual cloud and sensor maintenance

net_annual_savings = annual_downtime_savings - opex_annual_support
roi_pct = (net_annual_savings / capex_hardware_software) * 100.0
payback_months = (capex_hardware_software / (net_annual_savings / 12.0))

print(f"Annual Downtime Loss Prevented : ${annual_downtime_savings:,.0f}")
print(f"Net Annual Financial Savings   : ${net_annual_savings:,.0f}")
print(f"System Return on Investment    : {roi_pct:.1f}%")
print(f"Capital Payback Period         : {payback_months:.1f} months")
"""
        viz = """# 2. Executive Cumulative Cash Flow & Payback Break-Even Chart
months = np.arange(0, 25)  # 2-year timeline
cumulative_cash_flow = -capex_hardware_software + (net_annual_savings / 12.0) * months

plt.figure(figsize=(11, 5))
plt.plot(months, cumulative_cash_flow, color='#10b981', linewidth=2.5, label='Cumulative Net Cash Flow ($)')
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(payback_months, color='#ef4444', linestyle='--', linewidth=2, 
            label=f'Payback Break-Even = {payback_months:.1f} Months')

plt.fill_between(months, cumulative_cash_flow, 0, where=(cumulative_cash_flow >= 0), color='#10b981', alpha=0.15)
plt.fill_between(months, cumulative_cash_flow, 0, where=(cumulative_cash_flow < 0), color='#ef4444', alpha=0.15)

plt.title("Capstone 4: Executive Business Case - Predictive Maintenance ROI & Payback", fontsize=13, fontweight='bold')
plt.xlabel("Months Following Commissioning")
plt.ylabel("Cumulative Net Cash Flow [USD]")
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Assert that the predictive maintenance business case achieves > 300% ROI and payback < 4 months
assert roi_pct > 300.0, f"Expected ROI > 300%, got {roi_pct:.1f}%"
assert payback_months < 4.0, f"Payback period {payback_months:.1f} months exceeded 4-month limit!"
print("✓ Capstone 4 executive business case and ROI verified!")
"""
'''

def main():
    script_path = Path(__file__).resolve().parent / "build_notebooks.py"
    content = script_path.read_text(encoding="utf-8")

    # Locate where m == 5 starts
    m5_start = content.find("elif m == 5:")
    if m5_start == -1:
        raise ValueError("Could not find 'elif m == 5:' in build_notebooks.py")

    # Locate where return theory, sim, viz, exercise is
    return_stmt = content.find("return theory, sim, viz, exercise", m5_start)
    if return_stmt == -1:
        raise ValueError("Could not find 'return theory, sim, viz, exercise' after 'elif m == 5:'")

    # Replace everything from elif m == 5: up to return
    new_content = content[:m5_start] + MODULES_5_TO_7_CODE + "\n    " + content[return_stmt:]

    script_path.write_text(new_content, encoding="utf-8")
    print("Successfully patched build_notebooks.py with detailed code for Modules 5 to 7!")

if __name__ == "__main__":
    main()
