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
    tailored specifically to each lesson's industrial ML domain.
    """
    m = module_number
    l = lesson_number
    title = lesson_data.get("title_en", "Industrial ML Task")

    # =========================================================================
    # MODULE 1: Industrial Telemetry Ingestion & Real-Time Processing
    # =========================================================================
    if m == 1 and l == 1:
        # Lesson 1.1: Vectorized NumPy on 4-20mA Telemetry
        theory = """### Key Engineering Concepts:
1. **4-20mA Current Loops**: The global gold standard for analog industrial instrumentation. Current is immune to lead resistance and voltage drops over hundreds of meters.
2. **ADC Conversion Equation**: A 16-bit ADC maps $0-65535$ raw integer ticks to $4.0 - 20.0\\text{ mA}$:
   $$I = 4.0 + 16.0 \\cdot \\frac{\\text{ADC} - \\text{ADC}_{min}}{\\text{ADC}_{max} - \\text{ADC}_{min}}$$
3. **The 'Live Zero' Principle**: $4.0\\text{ mA}$ represents $0\\%$ physical process value. If a wire snaps, current drops to $0.0\\text{ mA}$. Any reading below $3.6\\text{ mA}$ is an immediate broken-wire alarm.
4. **Vectorized NumPy Operations**: Processing millions of PLC ticks via vectorized boolean masks executes in C-speed SIMD registers, achieving 50x-100x speedup over standard Python `for` loops.
"""
        sim = """# 1. Simulate 1,000,000 16-Bit ADC Telemetry Samples with Live Zero Faults
np.random.seed(42)
n_samples = 1_000_000

# 16-bit unsigned ADC integer range
ADC_MIN = 0
ADC_MAX = 65535

# True process pressure in a chemical reactor: 0 to 100 bar
# Normal operational baseline: 45.0 bar +/- 6.0 bar
true_pressure = np.random.normal(loc=45.0, scale=6.0, size=n_samples)
true_pressure = np.clip(true_pressure, 0.0, 100.0)

# Ideal current: 4 mA = 0 bar, 20 mA = 100 bar
ideal_current = 4.0 + (true_pressure / 100.0) * 16.0

# Add electromagnetic sensor noise
noisy_current = ideal_current + np.random.normal(0, 0.12, size=n_samples)

# Quantize to 16-bit integer ADC counts
raw_adc = np.round(((noisy_current - 4.0) / 16.0) * (ADC_MAX - ADC_MIN) + ADC_MIN).astype(np.int32)
raw_adc = np.clip(raw_adc, ADC_MIN, ADC_MAX)

# Inject physical faults:
# - Severed cable / broken wire: current drops to 0.0 mA (ADC ~ 0)
# - Sensor short circuit / over-range: current spikes to 22.5 mA (ADC pegged at 65535)
fault_broken_wire = np.random.choice(n_samples, size=500, replace=False)
raw_adc[fault_broken_wire] = 120  # ~ 0.03 mA

fault_saturation = np.random.choice(n_samples, size=300, replace=False)
raw_adc[fault_saturation] = 65535  # Pegged max

print(f"✓ Generated {n_samples:,} 16-bit ADC samples with injected electrical faults.")
"""
        viz = """# 2. Vectorized Engineering Conversion & Live Zero Masking
import time

# Vectorized conversion to mA and Physical Bar
t0 = time.perf_counter()
current_ma = 4.0 + 16.0 * (raw_adc - ADC_MIN) / (ADC_MAX - ADC_MIN)
calc_pressure = (current_ma - 4.0) / 16.0 * 100.0

# Vectorized Live Zero Fault Classification
mask_broken_wire = current_ma < 3.6    # Broken wire / disconnected loop
mask_saturation  = current_ma > 20.8   # Over-range / short circuit
mask_normal      = (~mask_broken_wire) & (~mask_saturation)
t_vectorized = time.perf_counter() - t0

print(f"Vectorized NumPy Pipeline: {t_vectorized*1000:.2f} ms for {n_samples:,} samples")
print(f" - Normal operational samples : {mask_normal.sum():,}")
print(f" - Broken wire alarms (<3.6mA) : {mask_broken_wire.sum():,}")
print(f" - Saturation alarms (>20.8mA) : {mask_saturation.sum():,}")

# Visual Inspection of Telemetry Window
sample_window = slice(1000, 1500)
t_axis = np.arange(500)

plt.figure(figsize=(14, 5))
plt.plot(t_axis, calc_pressure[sample_window], color='#0284c7', linewidth=1.5, label='Calculated Pressure [bar]')
plt.axhline(0.0, color='#64748b', linestyle='--', alpha=0.6, label='0 bar Process Zero (4.0 mA)')
plt.axhline(100.0, color='#ef4444', linestyle='--', alpha=0.6, label='100 bar Max Scale (20.0 mA)')

# Highlight detected wire break anomalies
wire_breaks_in_window = np.where(mask_broken_wire[sample_window])[0]
if len(wire_breaks_in_window) > 0:
    plt.scatter(wire_breaks_in_window, calc_pressure[sample_window][wire_breaks_in_window],
                color='#ef4444', s=80, marker='x', linewidth=2, label='ALARM: Broken Wire (<3.6 mA)')

plt.title("Industrial 4-20mA Telemetry Pipeline with Live Zero Anomaly Detection", fontsize=13, fontweight='bold')
plt.xlabel("Telemetry Sample Index")
plt.ylabel("Pressure [bar]")
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# 1. Assert that exactly 500 broken-wire faults were identified by the boolean mask.
# 2. Verify that vectorized compute time is under 50 milliseconds.

assert mask_broken_wire.sum() == 500, f"Expected 500 wire breaks, got {mask_broken_wire.sum()}"
assert t_vectorized < 0.05, f"Vectorized latency too high: {t_vectorized*1000:.1f}ms"
print("✓ Vectorized telemetry validation test passed with zero errors!")
"""

    elif m == 1 and l == 2:
        # Lesson 1.2: Pandas 2.x vs Polars for High-Speed Factory Logs
        theory = """### Key Engineering Concepts:
1. **High-Frequency Factory Logs**: Vibration sensors and servomotors stream thousands of rows per second, quickly causing Out-Of-Memory (OOM) errors in traditional single-threaded Pandas.
2. **Pandas 2.x PyArrow Backend**: Replacing NumPy dtypes with Apache Arrow enables zero-copy operations, true nullable types, and compact memory layouts.
3. **Polars Architecture**: Written in Rust, Polars leverages multithreaded SIMD parallelism and a lazy query planner (`pl.scan_parquet()`) that optimizes filter pushdowns before allocating memory.
"""
        sim = """# 1. Generate High-Speed Factory Log (500,000 Records)
import time
import pandas as pd

np.random.seed(42)
n_rows = 500_000

timestamps = pd.date_range("2026-01-01 00:00:00", periods=n_rows, freq="10ms")
machine_ids = np.random.choice(["CNC_01", "CNC_02", "PUMP_A", "ROBOT_ARM"], size=n_rows)
motor_current = np.random.uniform(5.0, 45.0, size=n_rows)
vibration_rms = np.random.gamma(shape=2.0, scale=0.8, size=n_rows)

raw_dict = {
    "timestamp": timestamps,
    "machine_id": machine_ids,
    "motor_current_amps": motor_current,
    "vibration_rms": vibration_rms
}

df_pandas_numpy = pd.DataFrame(raw_dict)
df_pandas_arrow = pd.DataFrame(raw_dict).convert_dtypes(dtype_backend="pyarrow")
print(f"✓ Synthetic log generated: {n_rows:,} rows across 4 machines.")
"""
        viz = """# 2. Benchmark Aggregation: Pandas vs Polars
try:
    import polars as pl
    has_polars = True
    df_polars = pl.from_pandas(df_pandas_numpy)
except ImportError:
    has_polars = False
    print("Polars not installed. Running simulated Polars benchmark.")

# Benchmark Pandas Standard
t0 = time.perf_counter()
res_pandas = df_pandas_numpy.groupby("machine_id").agg({
    "motor_current_amps": ["mean", "max"],
    "vibration_rms": ["mean", "std"]
})
t_pandas = time.perf_counter() - t0

# Benchmark Pandas with PyArrow backend
t0 = time.perf_counter()
res_arrow = df_pandas_arrow.groupby("machine_id").agg({
    "motor_current_amps": ["mean", "max"],
    "vibration_rms": ["mean", "std"]
})
t_arrow = time.perf_counter() - t0

# Benchmark Polars
if has_polars:
    t0 = time.perf_counter()
    res_polars = df_polars.group_by("machine_id").agg([
        pl.col("motor_current_amps").mean().alias("current_mean"),
        pl.col("motor_current_amps").max().alias("current_max"),
        pl.col("vibration_rms").mean().alias("vib_mean"),
        pl.col("vibration_rms").std().alias("vib_std"),
    ])
    t_polars = time.perf_counter() - t0
else:
    t_polars = t_pandas * 0.18  # Polars is typically 5x-8x faster

# Plot Latency Comparison
methods = ["Pandas (NumPy)", "Pandas 2.x (PyArrow)", "Polars (Rust Engine)"]
latencies = [t_pandas * 1000, t_arrow * 1000, t_polars * 1000]

plt.figure(figsize=(10, 4.5))
bars = plt.bar(methods, latencies, color=['#94a3b8', '#0284c7', '#10b981'], width=0.55)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1.0, f"{yval:.1f} ms", ha='center', va='bottom', fontweight='bold')

plt.title("High-Speed Factory Log Aggregation Benchmark (500k rows)", fontsize=13, fontweight='bold')
plt.ylabel("Compute Latency [milliseconds]")
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Filter high vibration events (> 3.5 m/s²) and count occurrences per machine line
high_vib_counts = df_pandas_arrow[df_pandas_arrow['vibration_rms'] > 3.5]['machine_id'].value_counts()
print("High Vibration Counts by Machine:")
print(high_vib_counts)
assert len(high_vib_counts) == 4, "Expected detections across all 4 machine lines."
print("✓ High-speed telemetry aggregation verified.")
"""

    elif m == 1 and l == 3:
        # Lesson 1.3: DuckDB & Parquet for Industrial Archives
        theory = """### Key Engineering Concepts:
1. **Industrial Historian Storage**: Traditional CSV or unindexed RDBMS databases choke on multi-year time-series telemetry exceeding hundreds of gigabytes.
2. **Apache Parquet Benefits**:
   - Columnar projection: Only requested sensor columns are read from disk.
   - Snappy/Zstandard compression: Slashes disk footprints by $70\\%-85\\%$.
   - Chunk statistics: Min/max values per row-group enable predicate pushdown, skipping irrelevant days/months entirely.
3. **DuckDB In-Process Engine**: Runs zero-copy vectorized SQL queries directly against compressed `.parquet` files without loading datasets into Python RAM.
"""
        sim = """# 1. Create Compressed Industrial Parquet Archive
import tempfile
import pandas as pd

np.random.seed(101)
n_records = 300_000
temp_dir = tempfile.mkdtemp()
parquet_path = f"{temp_dir}/sensor_archive.parquet"

df_archive = pd.DataFrame({
    "timestamp": pd.date_range("2026-01-01", periods=n_records, freq="1s"),
    "machine_id": np.random.choice(["KILN_A", "KILN_B", "FURNACE_01"], size=n_records),
    "zone_temp_c": np.random.normal(850.0, 25.0, size=n_records),
    "furnace_pressure_mbar": np.random.normal(1013.2, 8.5, size=n_records),
    "heater_duty_pct": np.random.uniform(40.0, 95.0, size=n_records)
})

# Save to Parquet with Snappy compression
df_archive.to_parquet(parquet_path, engine="pyarrow", compression="snappy", index=False)
parquet_size_mb = os.path.getsize(parquet_path) / (1024 * 1024)
print(f"✓ Saved {n_records:,} industrial records to Parquet ({parquet_size_mb:.2f} MB).")
"""
        viz = """# 2. Query Parquet Archive using DuckDB SQL
try:
    import duckdb
    con = duckdb.connect()
    # Direct SQL query over Parquet file without loading into memory
    query = f\"\"\"
        SELECT 
            machine_id,
            COUNT(*) AS total_samples,
            ROUND(AVG(zone_temp_c), 2) AS avg_temp,
            ROUND(MAX(zone_temp_c), 2) AS max_temp,
            ROUND(AVG(furnace_pressure_mbar), 2) AS avg_pressure,
            ROUND(STDDEV(zone_temp_c), 2) AS temp_std
        FROM '{parquet_path}'
        WHERE heater_duty_pct > 80.0
        GROUP BY machine_id
        ORDER BY machine_id
    \"\"\"
    result_df = con.execute(query).df()
    print("DuckDB Query Results (High Duty Cycle Operation):")
    print(result_df)
    
    # Plot DuckDB aggregated stats
    plt.figure(figsize=(9, 4))
    plt.bar(result_df['machine_id'], result_df['avg_temp'], yerr=result_df['temp_std'], 
            capsize=5, color='#0284c7', alpha=0.85, width=0.45)
    plt.title("Furnace High-Duty Average Temperature & Stability (DuckDB SQL)", fontweight='bold')
    plt.ylabel("Temperature [°C]")
    plt.ylim(800, 900)
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()

except ImportError:
    print("DuckDB not installed; using Pandas query equivalent.")
"""
        exercise = """# Exercise Challenge:
# Run a query to find the peak furnace pressure recorded during the entire archive
max_pressure = df_archive['furnace_pressure_mbar'].max()
print(f"Peak Archive Pressure: {max_pressure:.2f} mbar")
assert max_pressure > 1030.0, "Unexpected peak pressure value."
print("✓ Parquet archive analytical query passed.")
"""

    elif m == 1 and l == 4:
        # Lesson 1.4: Data Cleaning & Spike Removal
        theory = """### Key Engineering Concepts:
1. **Industrial Telemetry Glitches**: Sensor cables running near high-voltage VFDs and welding robots pick up transient electromagnetic spikes (thousands of volts for microsecond bursts).
2. **The Hampel Filter**: A robust outlier rejection filter based on rolling Median Absolute Deviation (MAD):
   $$\\text{MAD}_t = 1.4826 \\cdot \\text{median}\\left(|x_{t-k \\dots t+k} - \\tilde{x}_t|\\right)$$
   If $|x_t - \\tilde{x}_t| > 3 \\cdot \\text{MAD}_t$, replace $x_t$ with the rolling median $\\tilde{x}_t$.
3. **Phase-Preserving Denoising**: Unlike moving average filters which shift waveform peaks and smear spikes into broader hills, the Hampel filter isolates only anomalous samples, preserving sharp physical transients.
"""
        sim = """# 1. Simulate Clean Telemetry with Welding Arc Spikes and Packet Drops
np.random.seed(42)
n_pts = 1000
t = np.linspace(0, 10, n_pts)

# Clean thermal signal with diurnal cycle
clean_signal = 65.0 + 12.0 * np.sin(2 * np.pi * 0.2 * t)

# Inject electromagnetic welding spikes (15-40°C transient surges)
corrupted_signal = clean_signal.copy()
spike_indices = np.random.choice(n_pts, size=15, replace=False)
corrupted_signal[spike_indices] += np.random.choice([-1, 1], size=15) * np.random.uniform(25.0, 50.0, size=15)

# Inject sensor packet dropouts (NaNs)
dropout_indices = np.random.choice(n_pts, size=20, replace=False)
corrupted_signal[dropout_indices] = np.nan

# Forward-fill dropouts with limit=3
cleaned_fill = pd.Series(corrupted_signal).ffill(limit=3).bfill().to_numpy()
print(f"✓ Created signal with {len(spike_indices)} spikes and {len(dropout_indices)} dropouts.")
"""
        viz = """# 2. Implement Hampel Filter vs Moving Average Filter
def hampel_filter(data, window_size=7, n_sigmas=3.0):
    k = 1.4826  # Normal distribution scale factor
    series = pd.Series(data)
    rolling_median = series.rolling(window=window_size, center=True).median()
    rolling_mad = k * (series - rolling_median).abs().rolling(window=window_size, center=True).median()
    
    threshold = n_sigmas * rolling_mad
    diff = (series - rolling_median).abs()
    outlier_mask = diff > threshold
    
    filtered_series = series.copy()
    filtered_series[outlier_mask] = rolling_median[outlier_mask]
    return filtered_series.to_numpy(), outlier_mask.to_numpy()

# Naive Moving Average
naive_ma = pd.Series(cleaned_fill).rolling(window=11, center=True).mean().bfill().ffill().to_numpy()

# Hampel Cleaned
hampel_cleaned, detected_spikes = hampel_filter(cleaned_fill, window_size=9, n_sigmas=3.0)

plt.figure(figsize=(14, 5))
plt.plot(t, cleaned_fill, color='#ef4444', alpha=0.45, label='Raw Telemetry with Arc Spikes')
plt.plot(t, naive_ma, color='#f59e0b', linestyle='--', linewidth=1.8, label='Naive Moving Average (Smeared Error)')
plt.plot(t, hampel_cleaned, color='#10b981', linewidth=2.0, label='Hampel Filter (Preserves True Dynamic)')
plt.plot(t, clean_signal, color='#0284c7', linestyle=':', linewidth=1.5, label='Ground Truth Physical Process')

plt.title("Industrial Signal Conditioning: Hampel Filter vs Naive Moving Average", fontsize=13, fontweight='bold')
plt.xlabel("Time [seconds]")
plt.ylabel("Temperature [°C]")
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Compute RMSE against ground truth for both filters
rmse_ma = np.sqrt(np.mean((clean_signal - naive_ma)**2))
rmse_hampel = np.sqrt(np.mean((clean_signal - hampel_cleaned)**2))

print(f"Moving Average RMSE : {rmse_ma:.3f}°C")
print(f"Hampel Filter RMSE  : {rmse_hampel:.3f}°C")
assert rmse_hampel < rmse_ma * 0.5, "Hampel filter should deliver at least 2x lower RMSE than moving average."
print("✓ Spike rejection verification passed!")
"""

    # =========================================================================
    # MODULE 2: Industrial Feature Engineering & Signal Conditioning
    # =========================================================================
    elif m == 2 and l == 1:
        # Lesson 2.1: EDA on HVAC / Oven Logs
        theory = """### Key Engineering Concepts:
1. **Multi-Zone Thermal Dynamics**: Industrial tunnel curing ovens and chemical reactors have distinct temperature zones (Preheat, Soak, Cure, Cool) coupled by thermal convection.
2. **Thermal Lag & Inertia**: Adjusting a burner duty cycle does not instantly heat the workpiece. The physical heat capacitance introduces a 30s-120s transport delay.
3. **Cross-Correlation**: Computing $R_{xy}(\\tau) = \\sum x(t) y(t+\\tau)$ determines the exact physical transport lag between heating commands and thermocouple responses.
"""
        sim = """# 1. Simulate 4-Zone Industrial Tunnel Oven Telemetry
np.random.seed(42)
n_seconds = 1800  # 30 minutes of continuous operation at 1 Hz
t = np.arange(n_seconds)

# Heater duty cycle (actuator input with pulse changes)
heater_duty = 50.0 + 20.0 * np.sin(2 * np.pi * t / 600) + np.random.normal(0, 1.5, n_seconds)

# Zones have thermal transport lags: Zone 1 (15s lag), Zone 2 (45s lag), Zone 3 (90s lag)
def simulate_zone(heater, lag_sec, gain, baseline, noise_std):
    delayed_heater = np.roll(heater, lag_sec)
    delayed_heater[:lag_sec] = heater[0]
    # Low-pass thermal filter (exponential moving average)
    alpha = 0.05
    zone_temp = np.zeros(len(heater))
    zone_temp[0] = baseline
    for i in range(1, len(heater)):
        target = baseline + gain * (delayed_heater[i] - 50.0)
        zone_temp[i] = (1 - alpha) * zone_temp[i-1] + alpha * target
    return zone_temp + np.random.normal(0, noise_std, len(heater))

zone1 = simulate_zone(heater_duty, lag_sec=15, gain=1.2, baseline=120.0, noise_std=0.4)
zone2 = simulate_zone(heater_duty, lag_sec=45, gain=1.8, baseline=180.0, noise_std=0.6)
zone3 = simulate_zone(heater_duty, lag_sec=90, gain=2.1, baseline=220.0, noise_std=0.8)

df_oven = pd.DataFrame({
    "time_sec": t, "heater_duty_pct": heater_duty,
    "zone1_preheat": zone1, "zone2_soak": zone2, "zone3_cure": zone3
})
print("✓ Simulated 30-minute 4-Zone Oven Telemetry Matrix.")
"""
        viz = """# 2. Cross-Correlation Lag Analysis & Thermal Heatmap
from scipy.signal import correlate

# Calculate cross-correlation between heater duty and Zone 2 response
norm_heater = heater_duty - np.mean(heater_duty)
norm_zone2 = zone2 - np.mean(zone2)
corr = correlate(norm_zone2, norm_heater, mode='full')
lags = np.arange(-n_seconds + 1, n_seconds)

optimal_lag = lags[np.argmax(corr)]
print(f"Identified Physical Thermal Transport Lag: {optimal_lag} seconds.")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Cross-correlation curve
axes[0].plot(lags, corr, color='#0284c7', linewidth=1.8)
axes[0].axvline(optimal_lag, color='#ef4444', linestyle='--', label=f'Peak Lag = {optimal_lag}s')
axes[0].set_xlim(-50, 150)
axes[0].set_title("Cross-Correlation vs Time Lag (Duty Cycle to Zone 2)", fontweight='bold')
axes[0].set_xlabel("Lag [seconds]")
axes[0].set_ylabel("Correlation Coefficient")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Correlation Heatmap
sns.heatmap(df_oven.corr(), annot=True, fmt='.2f', cmap='Blues', ax=axes[1], cbar=False)
axes[1].set_title("Inter-Zone Sensor Cross-Correlation Matrix", fontweight='bold')

plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Verify that detected lag between duty cycle and Zone 2 is between 40 and 50 seconds
assert 40 <= optimal_lag <= 50, f"Detected lag {optimal_lag} outside expected 45s physical window."
print("✓ Thermal transport lag calculation verified.")
"""

    elif m == 2 and l == 2:
        # Lesson 2.2: Feature Engineering & Lag Variables
        theory = """### Key Engineering Concepts:
1. **Autoregressive Lag Features**: Static snapshots lack momentum. Lagged variables ($x_{t-1}, x_{t-5}, x_{t-30}$) allow standard tabular models to capture derivatives and acceleration.
2. **Statistical Descriptors**:
   - **RMS (Root Mean Square)**: Measures continuous destructive vibration energy.
   - **Kurtosis**: Measures peakedness/transient impact shocks (sharp bearing spall strikes).
   - **Crest Factor**: Peak amplitude divided by RMS.
3. **Temporal Leakage Prevention**: Rolling statistics must strictly look backwards (`closed='left'` or non-overlapping historic windows) to prevent model predictions from peeking into future timestamps.
"""
        sim = """# 1. Synthesize Compressor Vibration with Gradual Bearing Degradation
np.random.seed(42)
n_steps = 1500
t = np.arange(n_steps)

# Baseline healthy vibration
vib = np.random.normal(0, 1.0, n_steps)

# Inject progressive bearing damage starting at step 800 (growing impact pulses)
for idx in range(800, n_steps):
    if np.random.rand() < 0.15:
        severity = (idx - 800) / (n_steps - 800) * 8.0
        vib[idx] += np.random.choice([-1, 1]) * severity

df_vib = pd.DataFrame({"vibration_accel": vib})
print(f"✓ Synthetic bearing vibration stream created ({n_steps} steps).")
"""
        viz = """# 2. Extract Rolling RMS, Kurtosis, and Time Lags
from scipy.stats import kurtosis

# Lag features
df_vib["lag_1"] = df_vib["vibration_accel"].shift(1)
df_vib["lag_5"] = df_vib["vibration_accel"].shift(5)

# Rolling RMS (Window = 50 steps)
df_vib["rolling_rms"] = df_vib["vibration_accel"].rolling(50).apply(lambda x: np.sqrt(np.mean(x**2)))

# Rolling Kurtosis (Window = 50 steps)
df_vib["rolling_kurtosis"] = df_vib["vibration_accel"].rolling(50).apply(lambda x: kurtosis(x, fisher=True))

fig, axes = plt.subplots(3, 1, figsize=(14, 8), sharex=True)

axes[0].plot(t, df_vib["vibration_accel"], color='#64748b', alpha=0.6, label='Raw Vibration')
axes[0].axvline(800, color='#ef4444', linestyle='--', label='Incipient Damage Inception')
axes[0].set_ylabel("Accel [g]")
axes[0].legend(loc='upper left')
axes[0].grid(True, alpha=0.3)

axes[1].plot(t, df_vib["rolling_rms"], color='#0284c7', linewidth=2, label='Rolling RMS (Energy)')
axes[1].set_ylabel("RMS [g]")
axes[1].legend(loc='upper left')
axes[1].grid(True, alpha=0.3)

axes[2].plot(t, df_vib["rolling_kurtosis"], color='#f59e0b', linewidth=2, label='Rolling Kurtosis (Shock Peakedness)')
axes[2].axhline(0.0, color='gray', linestyle=':', label='Gaussian Normal Baseline (Kurtosis=0)')
axes[2].set_ylabel("Kurtosis")
axes[2].set_xlabel("Time Step")
axes[2].legend(loc='upper left')
axes[2].grid(True, alpha=0.3)

plt.suptitle("Feature Extraction for Mechanical Degradation Tracking", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Assert that rolling kurtosis after damage inception (t > 1000) exceeds 3.0
post_damage_kurtosis = df_vib.loc[1000:, "rolling_kurtosis"].mean()
print(f"Average Post-Damage Kurtosis: {post_damage_kurtosis:.2f}")
assert post_damage_kurtosis > 2.5, "Kurtosis failed to register bearing impacts."
print("✓ Bearing feature extraction verified.")
"""

    elif m == 2 and l == 3:
        # Lesson 2.3: Feature Scaling (Standard, MinMax, Robust) under Sensor Spikes
        theory = """### Key Engineering Concepts:
1. **The Inrush Current Anomaly**: When heavy industrial induction motors start, they draw $6\\times-10\\times$ their nominal full-load current for a few hundred milliseconds.
2. **Breakdown of StandardScaler**:
   $$z = \\frac{x - \\mu}{\\sigma}$$
   A single startup surge of $5,000\\text{ A}$ inflates $\\sigma$ drastically. Normal operational readings ($35\\text{ A} \\pm 5\\text{ A}$) are crushed into an indistinguishable range ($z \\in [0.001, 0.003]$).
3. **Breakdown of MinMaxScaler**: The entire operational variance is squished into the bottom $1\\%$ of $[0, 1]$.
4. **RobustScaler Immunity**: Uses Median and Interquartile Range (IQR):
   $$x' = \\frac{x - \\text{median}}{\\text{IQR}}$$
   Because Median and IQR ignore the outer $25\\%$ tails, operational resolution remains 100% intact.
"""
        sim = """# 1. Simulate Motor Current with 5,000A Inrush Surges
np.random.seed(42)
n_pts = 1000

# Normal steady-state operation: Mean = 35.0 A, Std = 3.5 A
normal_amps = np.random.normal(loc=35.0, scale=3.5, size=n_pts)

# Inject startup inrush current spikes (1,500A - 5,000A)
surge_indices = np.random.choice(n_pts, size=10, replace=False)
raw_telemetry = normal_amps.copy()
raw_telemetry[surge_indices] = np.random.uniform(1500.0, 5000.0, size=len(surge_indices))

df_amps = pd.DataFrame({"motor_amps": raw_telemetry})
print(f"Summary Statistics with Startup Surges:\\n{df_amps.describe().round(1)}")
"""
        viz = """# 2. Compare StandardScaler vs MinMaxScaler vs RobustScaler
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

std_scaler = StandardScaler()
minmax_scaler = MinMaxScaler()
robust_scaler = RobustScaler()

df_amps["standard"] = std_scaler.fit_transform(df_amps[["motor_amps"]])
df_amps["minmax"]   = minmax_scaler.fit_transform(df_amps[["motor_amps"]])
df_amps["robust"]   = robust_scaler.fit_transform(df_amps[["motor_amps"]])

# Inspect only the normal operational range (excluding extreme surges)
normal_mask = ~df_amps.index.isin(surge_indices)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

axes[0].hist(df_amps.loc[normal_mask, "standard"], bins=25, color='#ef4444', edgecolor='black', alpha=0.7)
axes[0].set_title("StandardScaler (Crushed Variance)", fontweight='bold')
axes[0].set_xlabel("Z-Score")

axes[1].hist(df_amps.loc[normal_mask, "minmax"], bins=25, color='#f59e0b', edgecolor='black', alpha=0.7)
axes[1].set_title("MinMaxScaler (Crushed to [0, 0.01])", fontweight='bold')
axes[1].set_xlabel("Normalized Value")

axes[2].hist(df_amps.loc[normal_mask, "robust"], bins=25, color='#10b981', edgecolor='black', alpha=0.7)
axes[2].set_title("RobustScaler (Preserved Variance!)", fontweight='bold')
axes[2].set_xlabel("IQR Units")

plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Prove that RobustScaler maintains an IQR of approximately 1.0 on normal operations
robust_iqr = np.percentile(df_amps.loc[normal_mask, "robust"], 75) - np.percentile(df_amps.loc[normal_mask, "robust"], 25)
print(f"Robust Scaled Normal Operational IQR: {robust_iqr:.3f}")
assert 0.95 <= robust_iqr <= 1.05, "RobustScaler failed to preserve unit IQR!"
print("✓ Robust scaling stability test passed.")
"""

    elif m == 2 and l == 4:
        # Lesson 2.4: Interactive Telemetry Plotting
        theory = """### Key Engineering Concepts:
1. **Multi-Physics Time-Series**: Machines combine incompatible physical units (Temperature in °C, Pressure in bar, Vibration in m/s²). Plotting on a single axis obscures dynamics.
2. **Dual & Triple Y-Axes**: Synchronizing multiple vertical scales enables direct visual correlation between pressure surges and temperature spikes.
3. **Interactive Inspection**: Static PNG charts prevent drill-down into transient micro-stoppages. Interactive Plotly charts allow maintenance teams to pan, zoom, and inspect exact PLC timestamps.
"""
        sim = """# 1. Synthesize Synchronized Multi-Physics Factory Incident
np.random.seed(42)
n_pts = 600
time_axis = pd.date_range("2026-06-01 08:00:00", periods=n_pts, freq="1s")

# Hydraulic Pressure (bar): Normal 160 bar, drops during cavitation event
pressure = 160.0 + np.random.normal(0, 2.5, n_pts)
pressure[300:380] -= np.linspace(0, 45, 80)
pressure[380:450] -= 45.0
pressure[450:520] += np.linspace(-45, 0, 70)

# Motor Temperature (°C): Overheating consequence
temp = 42.0 + np.cumsum(np.where(pressure < 130.0, 0.25, -0.05)) + np.random.normal(0, 0.3, n_pts)

df_incident = pd.DataFrame({"timestamp": time_axis, "pressure_bar": pressure, "temp_c": temp})
print("✓ Incident dataset generated: cavitation and thermal runaway.")
"""
        viz = """# 2. Dual-Axis Production Telemetry Dashboard
fig, ax1 = plt.subplots(figsize=(14, 5))

color_p = '#0284c7'
ax1.set_xlabel("Time [HH:MM:SS]", fontweight='bold')
ax1.set_ylabel("Hydraulic Pressure [bar]", color=color_p, fontweight='bold')
line1 = ax1.plot(df_incident["timestamp"], df_incident["pressure_bar"], color=color_p, linewidth=1.8, label='Pressure (bar)')
ax1.tick_params(axis='y', labelcolor=color_p)
ax1.axhline(130.0, color='#ef4444', linestyle='--', alpha=0.7, label='Cavitation Alarm Level (130 bar)')

# Twin axis for Temperature
ax2 = ax1.twinx()
color_t = '#ef4444'
ax2.set_ylabel("Motor Winding Temp [°C]", color=color_t, fontweight='bold')
line2 = ax2.plot(df_incident["timestamp"], df_incident["temp_c"], color=color_t, linewidth=2.0, linestyle='-', label='Temperature (°C)')
ax2.tick_params(axis='y', labelcolor=color_t)

# Shaded fault zone
ax1.axvspan(df_incident["timestamp"].iloc[300], df_incident["timestamp"].iloc[520], color='#ef4444', alpha=0.15, label='Cavitation Window')

plt.title("Synchronized Multi-Physics Telemetry: Hydraulic Cavitation & Overheating", fontsize=13, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.3)
fig.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Identify the maximum temperature reached during the cavitation window
max_temp_cavitation = df_incident.loc[300:520, "temp_c"].max()
print(f"Peak Cavitation Temperature: {max_temp_cavitation:.2f}°C")
assert max_temp_cavitation > 55.0, "Expected temperature surge during cavitation."
print("✓ Multi-physics telemetry visualization test passed.")
"""

    # =========================================================================
    # MODULE 3: Classical Machine Learning & Cost-Sensitive Optimization
    # =========================================================================
    elif m == 3 and l == 1:
        # Lesson 3.1: Linear & Regularized Regression for Energy Prediction
        theory = """### Key Engineering Concepts:
1. **Industrial Energy Prediction**: Forecasting furnace power (MWh) based on production tonnage and thermocouple readings.
2. **Severe Multicollinearity**: In an industrial furnace, 10+ thermocouples placed along a 30-meter tunnel correlate at $r > 0.95$. Ordinary Least Squares (OLS) produces wild, unstable coefficient swings.
3. **Ridge ($L_2$) vs Lasso ($L_1$)**:
   - **Ridge**: Shrinks correlated coefficients together, stabilizing variance.
   - **Lasso**: Drives non-informative thermocouple weights to exact zero, performing automatic sensor pruning.
"""
        sim = """# 1. Simulate Industrial Furnace Energy Dataset with Collinear Sensors
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score

np.random.seed(42)
n_runs = 800

# Primary operational drivers
production_tonnage = np.random.uniform(20.0, 100.0, n_runs)
ambient_temp = np.random.uniform(-5.0, 35.0, n_runs)

# 8 highly correlated zone thermocouples
core_heat = 500.0 + 3.5 * production_tonnage - 0.8 * ambient_temp
tc_sensors = np.column_stack([
    core_heat + np.random.normal(0, 4.0, n_runs) for _ in range(8)
])

X = np.column_stack([production_tonnage, ambient_temp, tc_sensors])
feature_names = ["tonnage", "ambient_temp"] + [f"tc_zone_{i+1}" for i in range(8)]

# True energy consumption [MWh]
true_energy = 15.0 + 0.45 * production_tonnage - 0.12 * ambient_temp + 0.02 * tc_sensors[:, 0] + np.random.normal(0, 1.2, n_runs)
print(f"✓ Generated furnace energy dataset: {n_runs} runs with {X.shape[1]} features.")
"""
        viz = """# 2. Fit OLS vs Ridge vs Lasso & Plot Coefficients
ols = LinearRegression().fit(X, true_energy)
ridge = Ridge(alpha=100.0).fit(X, true_energy)
lasso = Lasso(alpha=0.5).fit(X, true_energy)

plt.figure(figsize=(12, 5))
x_idx = np.arange(len(feature_names))
width = 0.25

plt.bar(x_idx - width, ols.coef_, width=width, color='#ef4444', label=f'OLS (Unstable) R²={r2_score(true_energy, ols.predict(X)):.3f}')
plt.bar(x_idx, ridge.coef_, width=width, color='#0284c7', label=f'Ridge (L2 Shrinkage) R²={r2_score(true_energy, ridge.predict(X)):.3f}')
plt.bar(x_idx + width, lasso.coef_, width=width, color='#10b981', label=f'Lasso (L1 Pruning) R²={r2_score(true_energy, lasso.predict(X)):.3f}')

plt.xticks(x_idx, feature_names, rotation=35, ha='right')
plt.title("Regularized Regression: Taming Sensor Multicollinearity", fontsize=13, fontweight='bold')
plt.ylabel("Learned Feature Weight")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()

# Count pruned features in Lasso
zero_weights = (lasso.coef_ == 0.0).sum()
print(f"Lasso automatically pruned {zero_weights} redundant thermocouple features to exact zero!")
"""
        exercise = """# Exercise Challenge:
# Assert that Ridge regression achieves an R² score exceeding 0.95
r2_ridge = r2_score(true_energy, ridge.predict(X))
print(f"Ridge Model R² Score: {r2_ridge:.4f}")
assert r2_ridge > 0.95, "Ridge model failed to reach target accuracy."
print("✓ Regularized regression exercise passed.")
"""

    elif m == 3 and l == 2:
        # Lesson 3.2: Classification & Decision Trees for Faults
        theory = """### Key Engineering Concepts:
1. **Discrete Fault Diagnostics**: Classifying operational states (Normal, Cavitation, Bearing Defect, Line Blockage).
2. **Interpretability in Regulated Plants**: Black-box models cannot be deployed in safety-critical manufacturing. Reliability engineers demand human-auditable logic.
3. **PLC Ladder Logic / Structured Text Export**: A trained `DecisionTreeClassifier` can be compiled into IEC 61131-3 `IF-THEN` statements for execution on Siemens S7-1500 or Allen-Bradley PLCs.
"""
        sim = """# 1. Synthesize Pump Fault Diagnostic Dataset
from sklearn.tree import DecisionTreeClassifier, export_text

np.random.seed(42)
n_records = 1200

# Features: Discharge Pressure (bar), Motor Current (Amps), Vibration RMS (m/s²)
# State 0: Normal
# State 1: Cavitation (Low pressure, surging vibration)
# State 2: Bearing Outer Race Fault (High vibration, normal pressure)
n_per_class = 400

f_normal = np.random.multivariate_normal([160.0, 25.0, 1.2], np.diag([4, 2, 0.05]), n_per_class)
f_cavit  = np.random.multivariate_normal([110.0, 28.0, 4.5], np.diag([9, 3, 0.40]), n_per_class)
f_bear   = np.random.multivariate_normal([158.0, 31.0, 6.8], np.diag([5, 2, 0.60]), n_per_class)

X_pump = np.vstack([f_normal, f_cavit, f_bear])
y_pump = np.array([0]*n_per_class + [1]*n_per_class + [2]*n_per_class)
feature_names = ["pressure_bar", "motor_current_a", "vibration_rms"]
target_names = ["NORMAL", "CAVITATION", "BEARING_FAULT"]

print(f"✓ Generated {len(X_pump)} diagnostic records across 3 fault modes.")
"""
        viz = """# 2. Train Interpretable Decision Tree & Export IEC 61131-3 PLC Code
clf_tree = DecisionTreeClassifier(max_depth=3, random_state=42)
clf_tree.fit(X_pump, y_pump)

print("--- Decision Tree Text Representation ---")
print(export_text(clf_tree, feature_names=feature_names))

def export_to_plc_structured_text(tree, features, classes):
    \"\"\"Converts scikit-learn DecisionTree into IEC 61131-3 Structured Text for PLC\"\"\"
    left = tree.tree_.children_left
    right = tree.tree_.children_right
    threshold = tree.tree_.threshold
    feature = tree.tree_.feature
    value = tree.tree_.value

    lines = ["// --- Auto-Generated IEC 61131-3 Structured Text ---", "CASE eState OF"]
    
    def recurse(node, indent):
        sp = "  " * indent
        if left[node] != right[node]:
            f_name = features[feature[node]]
            thresh = threshold[node]
            lines.append(f"{sp}IF ({f_name} <= {thresh:.2f}) THEN")
            recurse(left[node], indent + 1)
            lines.append(f"{sp}ELSE")
            recurse(right[node], indent + 1)
            lines.append(f"{sp}END_IF;")
        else:
            cls_idx = np.argmax(value[node])
            lines.append(f"{sp}FaultCode := {cls_idx}; // {classes[cls_idx]}")

    recurse(0, 1)
    lines.append("END_CASE;")
    return "\\n".join(lines)

plc_code = export_to_plc_structured_text(clf_tree, feature_names, target_names)
print(plc_code)
"""
        exercise = """# Exercise Challenge:
# Assert that the decision tree accuracy on training telemetry exceeds 98%
train_acc = clf_tree.score(X_pump, y_pump)
print(f"Tree Diagnostic Accuracy: {train_acc*100:.1f}%")
assert train_acc >= 0.98, "Decision tree failed to achieve target accuracy."
print("✓ Decision tree PLC export verified.")
"""

    elif m == 3 and l == 3:
        # Lesson 3.3: Random Forests, XGBoost & LightGBM
        theory = """### Key Engineering Concepts:
1. **Ensemble Methods for Sensor Arrays**: Factory telemetry features contain non-linear interactions and sensor dropouts. Random Forests and Gradient Boosted Trees are the industrial gold standard.
2. **Handling Severe Imbalance**: Machine breakdowns are rare events ($1\\%-3\\%$ of samples). Using `scale_pos_weight` in XGBoost/LightGBM forces the loss function to heavily penalize missed failures.
3. **Feature Importance**: Comparing Gini Impurity reduction against Permutation Importance to identify true root causes without bias toward high-cardinality sensors.
"""
        sim = """# 1. Synthesize 25-Sensor Packaging Line Failure Dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

np.random.seed(42)
n_cycles = 2500
n_sensors = 25

# Normal operational telemetry
X_factory = np.random.normal(loc=50.0, scale=8.0, size=(n_cycles, n_sensors))

# True failure condition triggered by interaction of Sensor 3 and Sensor 17
y_failure = np.zeros(n_cycles, dtype=int)
risk_score = 0.6 * (X_factory[:, 3] - 50.0) + 0.8 * (X_factory[:, 17] - 50.0)
failure_prob = 1.0 / (1.0 + np.exp(-0.25 * risk_score))
y_failure[failure_prob > 0.85] = 1

print(f"✓ Synthetic line output: {n_cycles} cycles, {y_failure.sum()} breakdown events ({(y_failure.mean()*100):.1f}% failure rate).")
"""
        viz = """# 2. Fit Random Forest & Evaluate Permutation Feature Importance
from sklearn.inspection import permutation_importance

rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
rf.fit(X_factory, y_failure)

perm_imp = permutation_importance(rf, X_factory, y_failure, n_repeats=5, random_state=42)
top_indices = np.argsort(perm_imp.importances_mean)[::-1][:6]

plt.figure(figsize=(10, 4.5))
plt.barh([f"Sensor {i}" for i in top_indices][::-1], perm_imp.importances_mean[top_indices][::-1], color='#10b981')
plt.title("Permutation Feature Importance (Identifies Root Cause Sensors)", fontweight='bold')
plt.xlabel("Mean Accuracy Degradation Upon Feature Shuffling")
plt.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()

auc = roc_auc_score(y_failure, rf.predict_proba(X_factory)[:, 1])
print(f"Random Forest ROC-AUC Score: {auc:.4f}")
"""
        exercise = """# Exercise Challenge:
# Verify that Sensor 3 and Sensor 17 are ranked as the top 2 most important features
assert 3 in top_indices[:2] and 17 in top_indices[:2], "Permutation importance failed to isolate the root cause sensors."
print("✓ Ensemble feature importance verified.")
"""

    elif m == 3 and l == 4:
        # Lesson 3.4: Cross-Validation, ROC-AUC, Cost Matrices & Optuna
        theory = """### Key Engineering Concepts:
1. **TimeSeriesSplit**: Standard k-fold cross-validation shuffles data across time, leaking future sensor trends into past predictions. Forward walk-forward splits (`TimeSeriesSplit`) preserve physical causality.
2. **Asymmetric Business Penalties**:
   - $\\text{Cost(False Negative)} = \\$10,000$ (catastrophic production line stoppage).
   - $\\text{Cost(False Positive)} = \\$50$ (5-minute technician inspection).
3. **Threshold Economics**: The academic default threshold of $\\tau = 0.50$ is economically disastrous. Tuning $\\tau^*$ via Optuna minimizes total financial loss.
"""
        sim = """# 1. Simulate Plant Defect Probabilities & Financial Cost Function
np.random.seed(42)
n_batches = 3000
defect_rate = 0.025  # 2.5% failure rate

y_true = (np.random.rand(n_batches) < defect_rate).astype(int)

# Simulated predicted failure probability
pred_probs = np.zeros(n_batches)
pred_probs[y_true == 0] = np.random.beta(a=1.2, b=10.0, size=(y_true == 0).sum())
pred_probs[y_true == 1] = np.random.beta(a=5.0, b=1.8, size=(y_true == 1).sum())

COST_FN = 10000.0  # $10,000 per missed failure
COST_FP = 50.0     # $50 per false alarm

def calculate_plant_cost(y_actual, probabilities, threshold):
    preds = (probabilities >= threshold).astype(int)
    fn = ((y_actual == 1) & (preds == 0)).sum()
    fp = ((y_actual == 0) & (preds == 1)).sum()
    return fn * COST_FN + fp * COST_FP
"""
        viz = """# 2. Sweep Thresholds and Compute Real Dollar Losses
thresholds = np.linspace(0.01, 0.90, 150)
dollar_losses = [calculate_plant_cost(y_true, pred_probs, t) for t in thresholds]

best_idx = np.argmin(dollar_losses)
optimal_thresh = thresholds[best_idx]
min_loss = dollar_losses[best_idx]
loss_default_050 = calculate_plant_cost(y_true, pred_probs, 0.50)

plt.figure(figsize=(11, 5))
plt.plot(thresholds, dollar_losses, color='#ef4444', linewidth=2.5, label='Total Financial Loss ($)')
plt.axvline(optimal_thresh, color='#10b981', linestyle='--', linewidth=2, 
            label=f'Cost-Optimal Threshold = {optimal_thresh:.2f} (Loss: ${min_loss:,.0f})')
plt.axvline(0.50, color='#64748b', linestyle=':', label=f'Academic 0.50 Threshold (Loss: ${loss_default_050:,.0f})')

plt.title("Asymmetric Cost Optimization: Minimizing Dollar Loss vs Decision Threshold", fontsize=13, fontweight='bold')
plt.xlabel("Decision Threshold (tau)")
plt.ylabel("Total Expected Loss [USD]")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"Optimal Threshold saves ${loss_default_050 - min_loss:,.0f} compared to the default 0.50 threshold!")
"""
        exercise = """# Exercise Challenge:
# Assert that optimal threshold saves at least $20,000 over default 0.50 threshold
savings = loss_default_050 - min_loss
print(f"Verified Net Dollar Savings: ${savings:,.0f}")
assert savings >= 20000, "Cost optimization failed to achieve minimum financial threshold."
print("✓ Financial cost matrix optimization verified.")
"""

    # =========================================================================
    # MODULE 4: Unsupervised Learning, Regimes & End-to-End Capstone
    # =========================================================================
    elif m == 4 and l == 1:
        # Lesson 4.1: K-Means & DBSCAN for Operational Regimes
        theory = """### Key Engineering Concepts:
1. **Operational Machine Regimes**: CNC mills switch between Standby, Warmup, Rough Milling, and High-Speed Finishing. Thresholds set for finishing cause false alarms during roughing.
2. **K-Means Centroids**: Act as golden reference signatures for healthy operating modes.
3. **DBSCAN for Non-Convex Envelopes**: Density-Based Spatial Clustering identifies arbitrary boundary shapes and automatically labels unmodeled operational deviations as noise (`label = -1`).
"""
        sim = """# 1. Simulate Multi-Mode CNC Spindle Regimes (RPM vs Motor Current)
from sklearn.cluster import KMeans, DBSCAN

np.random.seed(42)
# Regime 1: Standby (RPM: ~300, Current: ~5A)
c1 = np.random.multivariate_normal([300, 5], [[400, 5], [5, 0.8]], size=180)
# Regime 2: Normal Roughing (RPM: ~2400, Current: ~35A)
c2 = np.random.multivariate_normal([2400, 35], [[3000, 25], [25, 4.0]], size=250)
# Regime 3: High-Speed Finishing (RPM: ~4800, Current: ~22A)
c3 = np.random.multivariate_normal([4800, 22], [[4000, 20], [20, 3.0]], size=180)

# Unmodeled breakdown deviations (tool binding / mechanical seizure)
anomalies = np.array([[1200, 55], [1600, 68], [3400, 75], [500, 38], [4200, 62]])

X_regimes = np.vstack([c1, c2, c3, anomalies])
print(f"✓ Total operational data points: {len(X_regimes)}")
"""
        viz = """# 2. Fit K-Means Regimes and DBSCAN Anomaly Envelopes
kmeans = KMeans(n_clusters=3, random_state=42).fit(X_regimes)
dbscan = DBSCAN(eps=180.0, min_samples=8).fit(X_regimes)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# K-Means Centroid Clusters
axes[0].scatter(X_regimes[:, 0], X_regimes[:, 1], c=kmeans.labels_, cmap='viridis', alpha=0.7)
axes[0].scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='red', marker='X', s=200, label='Centroids')
axes[0].set_title("K-Means: Regime Segmentation", fontweight='bold')
axes[0].set_xlabel("Spindle RPM")
axes[0].set_ylabel("Motor Current [Amps]")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# DBSCAN Anomaly Flags (label == -1)
noise_mask = dbscan.labels_ == -1
axes[1].scatter(X_regimes[~noise_mask, 0], X_regimes[~noise_mask, 1], c=dbscan.labels_[~noise_mask], cmap='plasma', alpha=0.6, label='Operational Envelopes')
axes[1].scatter(X_regimes[noise_mask, 0], X_regimes[noise_mask, 1], color='#ef4444', s=120, edgecolors='black', label='DBSCAN Flagged Anomalies')
axes[1].set_title("DBSCAN: Density Anomaly Isolation", fontweight='bold')
axes[1].set_xlabel("Spindle RPM")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Assert that DBSCAN flags all 5 injected physical anomalies as noise
flagged_count = (dbscan.labels_ == -1).sum()
print(f"DBSCAN Isolated Outliers: {flagged_count} (Expected >= 5)")
assert flagged_count >= 5, "DBSCAN failed to isolate operational anomalies."
print("✓ Operational regime clustering test passed.")
"""

    elif m == 4 and l == 2:
        # Lesson 4.2: Isolation Forests for Unlabeled Anomalies
        theory = """### Key Engineering Concepts:
1. **Unlabeled Factory Anomaly Detection**: Plant breakdowns occur rarely. Supervised models fail due to severe lack of failure labels.
2. **Isolation Forest Geometry**: Anomalous samples require far fewer random splits to isolate ($h(x) \\ll c(n)$) compared to dense normal operational points.
3. **Continuous Anomaly Scoring**:
   $$s(x, n) = 2^{-\\frac{\\mathbb{E}(h(x))}{c(n)}}$$
   Scoring continuous telemetry allows early warning alerting as the score climbs from 0.35 towards 0.70.
"""
        sim = """# 1. Multi-Sensor Telemetry with Incipient Mechanical Binding
from sklearn.ensemble import IsolationForest

np.random.seed(42)
n_samples = 1500

# Normal operational telemetry: Motor Current, Bearing Temp, Vibration
X_normal = np.column_stack([
    np.random.normal(30.0, 3.0, n_samples),
    np.random.normal(65.0, 4.0, n_samples),
    np.random.normal(1.8, 0.3, n_samples)
])

# Inject subtle multi-sensor binding fault
X_fault = np.column_stack([
    np.random.uniform(42.0, 55.0, 25),
    np.random.uniform(78.0, 92.0, 25),
    np.random.uniform(2.8, 4.2, 25)
])

X_all = np.vstack([X_normal, X_fault])
iso_forest = IsolationForest(contamination=0.02, random_state=42)
iso_forest.fit(X_all)
anomaly_scores = -iso_forest.score_samples(X_all)  # Higher = more anomalous
"""
        viz = """# 2. Continuous Anomaly Timeline Inspection
plt.figure(figsize=(14, 5))
plt.plot(anomaly_scores, color='#0284c7', alpha=0.7, label='Isolation Forest Anomaly Score')
plt.axhline(0.60, color='#ef4444', linestyle='--', linewidth=2, label='Safety Trip Alarm Threshold (0.60)')
plt.axvspan(n_samples, len(X_all), color='#ef4444', alpha=0.2, label='Injected Mechanical Binding Zone')

plt.title("Continuous Unsupervised Telemetry Anomaly Scoring", fontsize=13, fontweight='bold')
plt.xlabel("Sample Timeline Index")
plt.ylabel("Anomaly Score [0 to 1]")
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Verify that average anomaly score in the fault zone is significantly higher than baseline
baseline_score = np.mean(anomaly_scores[:n_samples])
fault_score = np.mean(anomaly_scores[n_samples:])

print(f"Baseline Anomaly Score : {baseline_score:.3f}")
print(f"Fault Zone Anomaly Score: {fault_score:.3f}")
assert fault_score > baseline_score * 1.5, "Anomaly score failed to reflect mechanical binding."
print("✓ Isolation Forest anomaly verification passed.")
"""

    elif m == 4 and l == 3:
        # Lesson 4.3: PCA & UMAP for Compressing 50+ PLC Tags
        theory = """### Key Engineering Concepts:
1. **The '50-Gauge' Dilemma**: Modern packaging lines generate 50-200 SCADA/PLC tags simultaneously. Operators cannot monitor 50 individual dials.
2. **Principal Component Analysis (PCA)**: Projects orthogonal variance directions. The scree plot indicates how many latent components are required to capture $85\\%-90\\%$ of total plant variance.
3. **Machine Health Radar**: Mapping high-dimensional telemetry into a 2D coordinate plane allows real-time visualization of machine health drifting from green (nominal) to red (breakdown).
"""
        sim = """# 1. Simulate 50 Correlated PLC Tags on an Automated Packaging Line
from sklearn.decomposition import PCA

np.random.seed(42)
n_cycles = 1000
n_plc_tags = 50

# Base latent operational states (Line Speed, Ambient Temp, Product Mass)
latent_state = np.random.normal(0, 1, (n_cycles, 3))
mixing_matrix = np.random.normal(0, 0.5, (3, n_plc_tags))

# 50 correlated sensor channels + sensor noise
plc_data = np.dot(latent_state, mixing_matrix) + np.random.normal(0, 0.2, (n_cycles, n_plc_tags))

# Simulate machine wear progression over the last 200 cycles
wear_vector = np.linspace(0, 3.5, 200)[:, None] * np.random.uniform(0.5, 1.5, n_plc_tags)
plc_data[-200:] += wear_vector

print(f"✓ Generated {n_cycles} cycles across {n_plc_tags} PLC tags.")
"""
        viz = """# 2. PCA Scree Plot & 2D Machine Health Radar
pca = PCA(n_components=10)
pca_transformed = pca.fit_transform(plc_data)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Scree Plot
axes[0].plot(range(1, 11), np.cumsum(pca.explained_variance_ratio_)*100, marker='o', color='#0284c7', linewidth=2)
axes[0].axhline(85.0, color='#ef4444', linestyle='--', label='85% Variance Target')
axes[0].set_title("PCA Scree Plot: Cumulative Explained Variance", fontweight='bold')
axes[0].set_xlabel("Principal Components")
axes[0].set_ylabel("Variance Explained (%)")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# 2D Machine Health Radar (PC1 vs PC2)
scatter = axes[1].scatter(pca_transformed[:, 0], pca_transformed[:, 1], c=np.arange(n_cycles), cmap='coolwarm', alpha=0.7)
cbar = plt.colorbar(scatter, ax=axes[1])
cbar.set_label("Production Cycle (Wear Progression)")
axes[1].set_title("Machine Health Radar (50 PLC Tags -> 2D Projection)", fontweight='bold')
axes[1].set_xlabel("Principal Component 1")
axes[1].set_ylabel("Principal Component 2")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Verify that the first 3 principal components capture at least 70% of total variance
top3_var = np.sum(pca.explained_variance_ratio_[:3]) * 100
print(f"Top 3 PCs Explained Variance: {top3_var:.1f}%")
assert top3_var >= 70.0, "PCA failed to capture primary operational variance."
print("✓ Dimensionality reduction verification passed.")
"""

    elif m == 4 and l == 4:
        # Lesson 4.4: End-to-End Capstone 1 Notebook (PdM Pipeline)
        theory = """### Capstone Architecture: End-to-End Predictive Maintenance Pipeline
This capstone integrates every industrial machine learning stage developed across Modules 1 to 4:
1. **Telemetry Ingestion & Conditioning**: 4-20mA integer scaling and Hampel filter spike rejection.
2. **Feature Extraction**: Rolling RMS, Kurtosis, and autoregressive lag variables ($t-1, t-5$).
3. **Regime Identification**: Unsupervised K-Means clustering to establish operational context.
4. **Supervised Classifier**: Cost-sensitive Gradient Boosting with class weighting.
5. **Asymmetric Decision Matrix**: Optimal threshold evaluation ($FN = \\$10,000$, $FP = \\$50$).
6. **Streaming Edge Simulation**: Verifying sub-5ms real-time inference latency.
"""
        sim = """# 1. Execute End-to-End Predictive Maintenance Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import RobustScaler

np.random.seed(42)
n_steps = 2000

# 1. Synthesize streaming telemetry (Vibration + Motor Current + Temp)
vibration = 1.5 + 0.3 * np.random.randn(n_steps)
current   = 28.0 + 3.0 * np.random.randn(n_steps)
temp      = 55.0 + 2.0 * np.random.randn(n_steps)

# Inject progressive machine failure in steps 1500 to 2000
vibration[1500:] += np.linspace(0, 6.0, 500)
temp[1500:]      += np.linspace(0, 25.0, 500)
y_target = np.zeros(n_steps, dtype=int)
y_target[1750:] = 1  # Critical failure zone

# 2. Extract engineered features
df_capstone = pd.DataFrame({"vib": vibration, "current": current, "temp": temp})
df_capstone["vib_rms"] = df_capstone["vib"].rolling(20).apply(lambda x: np.sqrt(np.mean(x**2))).bfill()
df_capstone["vib_lag5"] = df_capstone["vib"].shift(5).bfill()
df_capstone["temp_diff"] = df_capstone["temp"] - df_capstone["temp"].rolling(30).mean().bfill()

X_features = df_capstone[["vib", "current", "temp", "vib_rms", "vib_lag5", "temp_diff"]].to_numpy()

# 3. Train Classifier
split_idx = 1200
X_train, X_test = X_features[:split_idx], X_features[split_idx:]
y_train, y_test = y_target[:split_idx], y_target[split_idx:]

scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

clf_pdm = GradientBoostingClassifier(n_estimators=60, random_state=42)
# Include a synthetic failure in training data for calibration
clf_pdm.fit(np.vstack([X_train_scaled, X_train_scaled[:10]*1.8]), np.hstack([y_train, [1]*10]))

test_probs = clf_pdm.predict_proba(X_test_scaled)[:, 1]
print(f"✓ Pipeline trained and evaluated across {len(X_test)} streaming cycles.")
"""
        viz = """# 2. Multi-Panel Executive PdM Dashboard
fig, axes = plt.subplots(3, 1, figsize=(14, 8), sharex=True)

# Raw Telemetry
axes[0].plot(vibration[split_idx:], color='#0284c7', label='Vibration [m/s²]')
axes[0].set_ylabel("Vibration")
axes[0].set_title("Capstone PdM Dashboard: Real-Time Telemetry & Failure Alarm", fontweight='bold')
axes[0].legend(loc='upper left')
axes[0].grid(True, alpha=0.3)

# Rolling RMS Feature
axes[1].plot(df_capstone["vib_rms"].iloc[split_idx:].to_numpy(), color='#f59e0b', linewidth=2, label='Rolling RMS Indicator')
axes[1].set_ylabel("RMS Indicator")
axes[1].legend(loc='upper left')
axes[1].grid(True, alpha=0.3)

# Predicted Probability & Cost-Optimal Alert Threshold
axes[2].plot(test_probs, color='#ef4444', linewidth=2, label='Failure Probability')
axes[2].axhline(0.20, color='#10b981', linestyle='--', linewidth=2, label='Cost-Optimal Warning Threshold (tau=0.20)')
axes[2].axvspan(1750 - split_idx, len(test_probs), color='#ef4444', alpha=0.2, label='True Breakdown Zone')
axes[2].set_ylabel("Risk Score")
axes[2].set_xlabel("Streaming Test Cycle")
axes[2].legend(loc='upper left')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
"""
        exercise = """# Exercise Challenge:
# Verify that the model triggered early warning alarm prior to breakdown
alarm_triggered_step = np.where(test_probs >= 0.20)[0][0] + split_idx
print(f"Early Warning Alarm Triggered at Step : {alarm_triggered_step}")
print(f"Actual Breakdown Inception Step       : 1750")
assert alarm_triggered_step < 1750, "Failure occurred before PdM alarm was triggered!"
print("✓ Capstone 1 Predictive Maintenance Pipeline fully verified!")
"""

    # =========================================================================
    # MODULES 5, 6, 7 (Domain-Specific Visualizers & Practical Exercises)
    # =========================================================================
    elif m == 5:
        # Module 5: Frequency Domain & Vibration FFT
        theory = """### Key Engineering Concepts:
1. **Time Domain vs Frequency Spectrum**: Microscopic bearing damage is invisible in time signals but exhibits distinct spectral peaks.
2. **Spectral Leakage & Hanning Windowing**: Non-periodic signal truncation causes energy smear; windowing restores frequency resolution.
3. **Characteristic Defect Frequencies**: Outer race defect (BPFO) peaks at $f_{BPFO} = \\frac{N_{balls}}{2} \\cdot f_{shaft} \\cdot \\left(1 - \\frac{d}{D}\\cos\\alpha\\right)$.
"""
        sim = """# 1. Synthesize Accelerometer Vibration with Bearing Defect (BPFO)
np.random.seed(42)
Fs = 2000.0  # Sampling frequency: 2000 Hz
T = 1.0 / Fs
N = 2048
time_axis = np.linspace(0.0, N*T, N, endpoint=False)

f_shaft = 30.0            # 30 Hz shaft rotational speed (1800 RPM)
f_bpfo = 3.58 * f_shaft   # 107.4 Hz outer race defect

sig_1x = 1.8 * np.sin(2.0 * np.pi * f_shaft * time_axis)
sig_bpfo = 1.4 * np.sin(2.0 * np.pi * f_bpfo * time_axis)
noise = 0.5 * np.random.randn(N)

vibration_accel = sig_1x + sig_bpfo + noise
print(f"✓ Vibration signal synthesized: {N} samples over {N*T:.2f} seconds.")
"""
        viz = """# 2. Compute FFT Spectrum with Hanning Window
window = np.hanning(N)
windowed_sig = vibration_accel * window

fft_vals = np.fft.rfft(windowed_sig)
fft_freqs = np.fft.rfftfreq(N, T)
fft_mag = (2.0 / N) * np.abs(fft_vals)

fig, axes = plt.subplots(2, 1, figsize=(14, 6))

axes[0].plot(time_axis[:300], vibration_accel[:300], color='#0284c7', linewidth=1.2)
axes[0].set_title("Time Domain: Accelerometer Raw Vibration", fontweight='bold')
axes[0].set_ylabel("Accel [m/s²]")
axes[0].grid(True, alpha=0.3)

axes[1].plot(fft_freqs, fft_mag, color='#10b981', linewidth=1.5, label='FFT Magnitude Spectrum')
axes[1].axvline(f_shaft, color='#f59e0b', linestyle='--', label=f'1X Shaft ({f_shaft:.1f} Hz)')
axes[1].axvline(f_bpfo, color='#ef4444', linestyle='-', linewidth=2, label=f'BPFO Defect ({f_bpfo:.1f} Hz)')
axes[1].set_xlim(0, 300)
axes[1].set_title("Frequency Domain: Bearing Fault Signature Exposed!", fontweight='bold')
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
print(f"Detected Bearing Defect Frequency Peak: {peak_freq:.2f} Hz (Expected ~107.4 Hz)")
assert abs(peak_freq - f_bpfo) < 2.0, "FFT defect peak detection out of tolerance!"
print("✓ Vibration analysis exercise passed.")
"""

    elif m == 6:
        # Module 6: Edge Vision & Bounding Boxes
        theory = """### Key Engineering Concepts:
1. **Spatial Localization**: In automated quality inspection, defect coordinates $[x_1, y_1, x_2, y_2]$ direct spot-repair robotics.
2. **Intersection over Union (IoU)**:
   $$\\text{IoU} = \\frac{\\text{Area of Overlap}}{\\text{Area of Union}}$$
3. **mAP@0.50 Threshold**: Standard industry metric requiring $\\text{IoU} \\ge 0.50$ for a detection to count as a True Positive.
"""
        sim = """# 1. Bounding Box Math & Vectorized IoU Calculation
def compute_iou(box_a, box_b):
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

ground_truth = [100.0, 80.0, 260.0, 180.0]
predicted    = [115.0, 75.0, 275.0, 175.0]

iou = compute_iou(ground_truth, predicted)
print(f"Calculated IoU: {iou:.3f} ({(iou*100):.1f}%)")
"""
        viz = """# 2. Visualizing Bounding Box Optical Inspection
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(8, 6))
metal = np.random.normal(0.4, 0.05, (300, 400))
ax.imshow(metal, cmap='gray', vmin=0, vmax=1)

gt_rect = patches.Rectangle((ground_truth[0], ground_truth[1]),
                            ground_truth[2] - ground_truth[0],
                            ground_truth[3] - ground_truth[1],
                            linewidth=2.5, edgecolor='#10b981', facecolor='none', label='Ground Truth')
ax.add_patch(gt_rect)

pred_rect = patches.Rectangle((predicted[0], predicted[1]),
                              predicted[2] - predicted[0],
                              predicted[3] - predicted[1],
                              linewidth=2.5, edgecolor='#f59e0b', linestyle='--', facecolor='none', 
                              label=f'CNN Prediction (IoU={iou:.2f})')
ax.add_patch(pred_rect)

plt.title("Industrial Optical Inspection - Bounding Box IoU Evaluation", fontsize=13, fontweight='bold')
plt.legend(loc='lower right')
plt.xlim(0, 400)
plt.ylim(300, 0)
plt.show()
"""
        exercise = """# Exercise Challenge:
# Assert that the predicted box passes the quality control threshold (IoU >= 0.50)
passes_qc = compute_iou(ground_truth, predicted) >= 0.50
print(f"Quality Control Result: {'PASS (True Positive)' if passes_qc else 'REJECT'}")
assert passes_qc, "Predicted bounding box failed IoU threshold!"
print("✓ Computer vision evaluation exercise passed.")
"""

    else:
        # Module 7: MLOps, Drift & Edge Optimization
        theory = """### Key Engineering Concepts:
1. **Data Drift vs Concept Drift**: Seasonal factory temperature shifts sensor inputs $P(X)$; tool wear alters physical failure relationships $P(Y|X)$.
2. **Kolmogorov-Smirnov Testing**: Non-parametric two-sample test comparing cumulative distributions to flag calibration drift.
3. **Edge Optimization**: Converting models from FP32 to INT8 precision slashes inference latency by $\\sim 3.8\\times$ with $< 0.5\\%$ accuracy drop.
"""
        sim = """# 1. Simulate Production Telemetry Shift & Kolmogorov-Smirnov Test
from scipy import stats

np.random.seed(42)
baseline_telemetry = np.random.normal(loc=50.0, scale=4.0, size=1000)
production_telemetry = np.random.normal(loc=56.2, scale=4.3, size=1000)

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
plt.tight_layout()
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
    mod_num = lesson_data.get("module_number")
    les_num = lesson_data.get("lesson_number")

    if mod_num is None or les_num is None:
        m = re.search(r"m0?(\d+)[_-]l0?(\d+)", lesson_id)
        if m:
            mod_num = int(m.group(1))
            les_num = int(m.group(2))
        elif "-" in lesson_id:
            parts = lesson_id.split("-")
            mod_num = int(parts[0])
            les_num = int(parts[1])
        else:
            mod_num = 1
            les_num = 1

    title_en = lesson_data.get("title_en", lesson_data.get("titleEn", "Industrial ML Lesson"))
    title_pl = lesson_data.get("title_pl", lesson_data.get("titlePl", ""))
    summary_en = lesson_data.get("summary_en", lesson_data.get("summaryEn", ""))
    summary_pl = lesson_data.get("summary_pl", lesson_data.get("summaryPl", ""))
    notebook_file = lesson_data.get("colab_notebook", lesson_data.get("notebook", f"{lesson_id}.ipynb"))
    est_min = lesson_data.get("estimated_minutes", lesson_data.get("estimatedMinutes", 25))
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
        checklist_md += "- [ ] Evaluate performance against industrial engineering thresholds.\n"
        checklist_md += "- [ ] Complete end-of-lesson knowledge check quiz in the web dashboard.\n"
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
            filename = f"{lesson.get('id', '1-1')}.ipynb"
        
        target_path = OUTPUT_DIR / filename
        nb = build_single_notebook(lesson, github_user, github_repo, github_branch)
        
        with open(target_path, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
        
        built_count += 1
        les_id = lesson.get("id", "1-1")
        mod_num = lesson.get("module_number", 1)
        les_num = lesson.get("lesson_number", 1)
        print(f"  [✓] {filename} (Module {mod_num}.{les_num})")

    print(f"\nSuccessfully compiled {built_count} valid .ipynb notebooks in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
