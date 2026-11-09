#!/usr/bin/env python3
"""
scripts/patch_phase3b_lessons.py
Industrial Machine Learning & Predictive Maintenance Course

Updates scripts/generate_phase3_lessons.py with the complete Phase 3B lesson definitions
for Modules 5, 6, and 7 according to AGENTS.md.
"""

import json
import re
from pathlib import Path

MODULES_5_TO_7 = [
    # =========================================================================
    # MODULE 5: Time-Series Dynamics, Vibration FFT & Capstone 2
    # =========================================================================
    {
        "id": "m05_l01_time_series_stationarity_rolling_stats",
        "module_id": "mod-5",
        "module_number": 5,
        "lesson_number": 1,
        "title_en": "Time-Series Stationarity & Rolling Window Statistics",
        "title_pl": "Stacjonarność Szeregów Czasowych i Ruchome Statystyki Okienne",
        "summary_en": "Diagnose non-stationarity in factory telemetry using the Augmented Dickey-Fuller test, differencing, and rolling statistics.",
        "summary_pl": "Diagnozuj niestacjonarność w telemetrii fabrycznej za pomocą testu ADF, różnicowania i ruchomych statystyk okiennych.",
        "visual_widget": "fft_anomaly_sandbox",
        "colab_notebook": "m05_l01_time_series_stationarity_rolling_stats.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m5-1-1", "textEn": "Execute Augmented Dickey-Fuller (ADF) hypothesis test on raw boiler pressure telemetry", "textPl": "Wykonaj test hipotezy Dickeya-Fullera (ADF) na surowej telemetrii ciśnienia kotła"},
            {"id": "chk-m5-1-2", "textEn": "Apply first-order differencing to eliminate non-stationary drift", "textPl": "Zastosuj różnicowanie pierwszego rzędu, aby wyeliminować niestacjonarny dryf"},
            {"id": "chk-m5-1-3", "textEn": "Compute and plot Autocorrelation (ACF) and Partial Autocorrelation (PACF) lag plots", "textPl": "Oblicz i wykreśl autokorelację (ACF) oraz częściową autokorelację (PACF)"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "The Physics of Stationarity in Manufacturing",
                "titlePl": "Fizyka Stacjonarności w Środowisku Produkcyjnym",
                "en": "A time series exhibits {{term:stationarity}} when its mean, variance, and autocovariance remain constant across time. In industrial plant operations, raw sensor signals are almost universally non-stationary: ambient summer temperatures cause thermal baselines to drift upward, furnace refractory linings thin over months, and pneumatic regulators experience gradual mechanical pressure decay. Applying standard machine learning or regression algorithms to non-stationary data leads to spurious statistical correlations and rampant false alarms.",
                "pl": "Szereg czasowy wykazuje {{term:stationarity}}, gdy jego średnia, wariancja i autokowariancja pozostają niezmienne w czasie. W zakładach produkcyjnych surowe sygnały czujników są niemal zawsze niestacjonarne: letnie upały powodują dryf temperatur bazowych, wymurówka pieców ulega stopniowej degradacji, a reduktory ciśnienia wykazują powolne spadki. Stosowanie algorytmów uczenia maszynowego na niestacjonarnych danych prowadzi do fałszywych korelacji i licznych błędnych alarmów."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "Hypothesis Testing: Augmented Dickey-Fuller (ADF)",
                "titlePl": "Weryfikacja Hipotez: Rozszerzony Test Dickeya-Fullera (ADF)",
                "en": "Before fitting predictive models, reliability engineers perform the {{term:adf_test}}. The null hypothesis $H_0$ states that the telemetry has a unit root (is non-stationary). If the resulting p-value is strictly below $0.05$, we reject $H_0$ and conclude the signal is stationary. If $p \\ge 0.05$, we apply first-order differencing $\\Delta y_t = y_t - y_{t-1}$ to transform drifting trends into stationary delta increments.",
                "pl": "Przed trenowaniem modeli inżynierowie wykonują {{term:adf_test}}. Hipoteza zerowa $H_0$ zakłada, że sygnał posiada pierwiastek jednostkowy (jest niestacjonarny). Jeśli wartość p-value jest niższa niż $0.05$, odrzucamy $H_0$ i uznajemy szereg za stacjonarny. W przeciwnym razie stosujemy różnicowanie pierwszego rzędu $\\Delta y_t = y_t - y_{t-1}$, przekształcając dryfujący trend w stacjonarne przyrosty."
            }
        ],
        "quiz": [
            {
                "id": "q-m5-1-1",
                "questionEn": "An ADF test on furnace thermocouple telemetry yields a p-value of 0.38. What engineering action is required before forecasting?",
                "questionPl": "Test ADF na danych z termopary pieca dał wartość p-value równą 0.38. Jakie działanie inżynierskie jest wymagane przed modelowaniem?",
                "optionsEn": [
                    "Proceed immediately; 0.38 indicates perfect stationarity",
                    "Apply first-order differencing (Δy = y_t - y_{t-1}) to remove the non-stationary trend and re-test",
                    "Multiply readings by 100 to increase numerical precision",
                    "Replace the thermocouple with a higher-frequency sensor"
                ],
                "optionsPl": [
                    "Kontynuować bez zmian; 0.38 oznacza idealną stacjonarność",
                    "Zastosować różnicowanie pierwszego rzędu (Δy = y_t - y_{t-1}), aby usunąć niestacjonarny trend, a następnie powtórzyć test",
                    "Pomnożyć odczyty przez 100 w celu zwiększenia precyzji numerycznej",
                    "Wymienić termoparę na czujnik o wyższej częstotliwości próbkowania"
                ],
                "correctIndex": 1,
                "explanationEn": "A p-value of 0.38 fails to reject the unit-root null hypothesis (p >= 0.05). Differencing eliminates the non-stationary drift.",
                "explanationPl": "Wartość p-value = 0.38 nie pozwala odrzucić hipotezy zerowej o pierwiastku jednostkowym. Różnicowanie eliminuje dryfujący trend."
            }
        ]
    },
    {
        "id": "m05_l02_fft_frequency_domain_vibration",
        "module_id": "mod-5",
        "module_number": 5,
        "lesson_number": 2,
        "title_en": "FFT Frequency-Domain Vibration & Bearing Kinematics",
        "title_pl": "Analiza Drgań w Dziedzinie Częstotliwości (FFT) i Kinematyka Łożysk",
        "summary_en": "Decompose raw accelerometer signals with FFT, apply Hanning windowing to stop leakage, and isolate bearing outer race defect peaks.",
        "summary_pl": "Rozłóż sygnały z akcelerometru za pomocą FFT, zastosuj okno Hanninga i zidentyfikuj piki uszkodzenia bieżni łożyska.",
        "visual_widget": "fft_anomaly_sandbox",
        "colab_notebook": "m05_l02_fft_frequency_domain_vibration.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m5-2-1", "textEn": "Synthesize multi-harmonic vibration signal with bearing defect frequencies", "textPl": "Wygeneruj sygnał drgań z harmonicznymi i częstotliwością uszkodzenia łożyska"},
            {"id": "chk-m5-2-2", "textEn": "Apply Hanning window function to suppress spectral boundary leakage", "textPl": "Zastosuj funkcję okna Hanninga, aby stłumić przeciek widmowy na brzegach"},
            {"id": "chk-m5-2-3", "textEn": "Calculate Fast Fourier Transform (FFT) and detect Ball Pass Frequency Outer Race (BPFO) peak", "textPl": "Oblicz szybką transformatę Fouriera (FFT) i zlokalizuj pik częstotliwości BPFO"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Vibration Analysis & Spectral Decomposition",
                "titlePl": "Analiza Wibracji i Dekompozycja Widmowa",
                "en": "Looking at raw accelerometer readings in the time domain reveals nothing more than a noisy, chaotic oscillation. However, rotating machinery operates under strict geometric kinematics: motor shafts rotate at rotational frequency $f_{shaft}$, gear meshes mesh at $N_{teeth} \\cdot f_{shaft}$, and bearing balls impact defects at characteristic kinematic frequencies. Using the {{term:fft}}, we project the time signal into the frequency domain, where discrete mechanical components appear as sharp spectral peaks.",
                "pl": "Analiza sygnału z akcelerometru w dziedzinie czasu ukazuje jedynie chaotyczny, zaszumiony przebieg. Jednak maszyny wirnikowe podlegają ścisłym prawom kinematyki: wał obraca się z częstotliwością $f_{shaft}$, zęby przekładni stykają się z częstością $N_{teeth} \\cdot f_{shaft}$, a kulki łożysk uderzają w mikropęknięcia z charakterystyczną częstotliwością. Używając {{term:fft}}, rzutujemy sygnał w dziedzinę częstotliwości, gdzie każdy element tworzy wyraźny pik."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "Bearing Defect Kinematics: BPFO & BPFI",
                "titlePl": "Kinematyka Uszkodzeń Łożysk: BPFO i BPFI",
                "en": "When a microscopic fatigue spall forms on the stationary outer ring of a rolling element bearing, every passing ball produces an impact shock at the Ball Pass Frequency Outer Race ({{term:bpfo}}): $f_{BPFO} = \\frac{N_{balls}}{2} f_{shaft} \\left(1 - \\frac{d}{D}\\cos\\alpha\\right)$. A defect on the rotating inner ring generates the Ball Pass Frequency Inner Race ({{term:bpfi}}). Detecting these spectral peaks weeks before audible noise occurs is the hallmark of modern predictive maintenance.",
                "pl": "Gdy na nieruchomej bieżni zewnętrznej łożyska tocznego powstanie mikropęknięcie zmęczeniowe, każda tocząca się kulka generuje impuls uderzeniowy z częstotliwością {{term:bpfo}}: $f_{BPFO} = \\frac{N_{balls}}{2} f_{shaft} \\left(1 - \\frac{d}{D}\\cos\\alpha\\right)$. Uszkodzenie bieżni wewnętrznej generuje z kolei częstotliwość {{term:bpfi}}. Wykrycie tych pików na tygodnie przed pojawieniem się hałasu stanowi fundament nowoczesnego predykcyjnego utrzymania ruchu."
            }
        ],
        "quiz": [
            {
                "id": "q-m5-2-1",
                "questionEn": "Why is a Hanning or Hamming window applied to vibration telemetry before calculating the FFT?",
                "questionPl": "Dlaczego przed obliczeniem FFT na sygnał drgań nakłada się okno Hanninga lub Hamminga?",
                "optionsEn": [
                    "To amplify high-frequency electrical sensor noise",
                    "To prevent spectral leakage caused by non-periodic truncation at signal sample boundaries",
                    "To convert the signal from acceleration to velocity automatically",
                    "To downsample the signal from 10 kHz to 1 kHz"
                ],
                "optionsPl": [
                    "Aby wzmocnić zakłócenia elektromagnetyczne w wysokich częstotliwościach",
                    "Aby zapobiec przeciekowi widmowemu wywołanemu nieciągłością sygnału na brzegach okna czasowego",
                    "Aby automatycznie przekształcić przyspieszenie w prędkość drgań",
                    "Aby zredukować częstotliwość próbkowania z 10 kHz do 1 kHz"
                ],
                "correctIndex": 1,
                "explanationEn": "Window functions smoothly taper signal endpoints to zero, eliminating artificial boundary discontinuities that smear spectral energy.",
                "explanationPl": "Funkcje okna łagodnie wygaszają końce sygnału do zera, eliminując sztuczne nieciągłości powodujące rozmycie energii widma."
            }
        ]
    },
    {
        "id": "m05_l03_forecasting_consumption_pressure_drift",
        "module_id": "mod-5",
        "module_number": 5,
        "lesson_number": 3,
        "title_en": "Forecasting Consumption & Pressure Drift: ARIMA vs XGBoost",
        "title_pl": "Prognozowanie Zużycia i Dryfu Ciśnienia: ARIMA kontra XGBoost",
        "summary_en": "Forecast factory compressed air and natural gas demand using statistical ARIMA and machine learning XGBoost with temporal lag features.",
        "summary_pl": "Prognozuj zapotrzebowanie na sprężone powietrze i gaz przy użyciu statystycznego modelu ARIMA oraz algorytmu XGBoost z cechami opóźnionymi.",
        "visual_widget": "fft_anomaly_sandbox",
        "colab_notebook": "m05_l03_forecasting_consumption_pressure_drift.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m5-3-1", "textEn": "Fit statistical ARIMA model on hourly factory gas consumption logs", "textPl": "Dopasuj model statystyczny ARIMA do godzinowych logów zużycia gazu w fabryce"},
            {"id": "chk-m5-3-2", "textEn": "Construct autoregressive lag features and calendar encodings for XGBoost regression", "textPl": "Zbuduj cechy opóźnione autoregresyjnie i kodowanie kalendarzowe dla modelu XGBoost"},
            {"id": "chk-m5-3-3", "textEn": "Evaluate multi-step walk-forward forecast horizon using Mean Absolute Percentage Error (MAPE)", "textPl": "Oceń wielokrokowy horyzont prognozy za pomocą błędu MAPE w walidacji kroczącej"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Industrial Utility & Fluid Pressure Forecasting",
                "titlePl": "Prognozowanie Mediów Przemysłowych i Ciśnień Płynów",
                "en": "Industrial manufacturing plants consume massive quantities of natural gas, electric power, and compressed air. Accurately forecasting utility demand 8 to 24 hours in advance allows energy managers to avoid expensive peak-demand surcharges and optimize compressor staging. Classical time-series modeling relies on {{term:arima}} (AutoRegressive Integrated Moving Average), which models linear relationships between lagged values and moving average error residuals.",
                "pl": "Zakłady produkcyjne zużywają ogromne ilości gazu ziemnego, energii elektrycznej i sprężonego powietrza. Dokładne prognozowanie zapotrzebowania z 8-24 godzinnym wyprzedzeniem pozwala uniknąć kar za przekroczenie mocy zamówionej i zoptymalizować pracę sprężarek. Klasyczne podejście opiera się na modelu {{term:arima}}, który opisuje liniowe zależności między przeszłymi wartościami i resztami średniej ruchomej."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "ARIMA vs XGBoost with Lag Variables",
                "titlePl": "ARIMA kontra XGBoost z Zmiennymi Opóźnionymi",
                "en": "While ARIMA assumes linear Gaussian dynamics, non-linear machine learning models like {{term:xgboost}} excel when paired with engineered lag features ($t-1, t-24$), rolling standard deviations, and exogenous variables (ambient temperature, production tonnage). In practice, XGBoost typically achieves 15-25% lower MAPE on complex multi-shift factory consumption profiles.",
                "pl": "Podczas gdy ARIMA zakłada liniową dynamikę Gaussa, nieliniowe modele uczenia maszynowego, takie jak {{term:xgboost}}, doskonale sprawdzają się w połączeniu z cechami opóźnionymi ($t-1, t-24$), ruchomymi odchyleniami standardowymi i zmiennymi zewnętrznymi (temperatura otoczenia, tonaż produkcji). W praktyce XGBoost osiąga o 15-25% niższy błąd MAPE na złożonych profilach zmianowych."
            }
        ],
        "quiz": [
            {
                "id": "q-m5-3-1",
                "questionEn": "When formatting time-series data for XGBoost multi-step forecasting, why must lag features strictly reference historical timestamps?",
                "questionPl": "Dlaczego podczas przygotowywania cech dla XGBoost w prognozowaniu szeregów czasowych cechy opóźnione muszą odwoływać się wyłącznie do przeszłości?",
                "optionsEn": [
                    "To prevent future data leakage that would create unrealistically optimistic offline training scores",
                    "To comply with European electrical grid frequency regulations (50 Hz)",
                    "Because gradient boosting trees cannot accept floating-point numbers",
                    "To force all predictions to sum to zero"
                ],
                "optionsPl": [
                    "Aby zapobiec wyciekowi danych z przyszłości (data leakage), który prowadzi do nierealistycznie optymistycznych wyników treningowych",
                    "Aby spełnić wymogi regulacji częstotliwości europejskiej sieci energetycznej (50 Hz)",
                    "Ponieważ drzewa gradientowe nie potrafią przetwarzać liczb zmiennoprzecinkowych",
                    "Aby wymusić, by suma wszystkich predykcji wynosiła zero"
                ],
                "correctIndex": 0,
                "explanationEn": "Referencing future timestamps during feature engineering constitutes lookahead leakage, rendering the model useless in live streaming production.",
                "explanationPl": "Odwołanie do przyszłych próbek w procesie inżynierii cech stanowi wyciek danych (lookahead leakage), uniemożliwiający poprawne działanie modelu na produkcji."
            }
        ]
    },
    {
        "id": "m05_l04_realtime_anomaly_capstone2_leak_detector",
        "module_id": "mod-5",
        "module_number": 5,
        "lesson_number": 4,
        "title_en": "Capstone 2: Real-Time Anomaly & Hydraulic Leak Detector",
        "title_pl": "Projekt Zwieńczeniowy 2: Detektor Wycieków Oleju i Spadków Ciśnienia w Czasie Rzeczywistym",
        "summary_en": "Build an end-to-end hydraulic leak detector using CUSUM and EWMA to detect micro-fissures and trigger automated safety shutdown alarms.",
        "summary_pl": "Zbuduj kompletny detektor wycieków hydraulicznych wykorzystujący algorytmy CUSUM i EWMA do wykrywania mikropęknięć i wyzwalania alarmów.",
        "visual_widget": "fft_anomaly_sandbox",
        "colab_notebook": "m05_l04_realtime_anomaly_capstone2_leak_detector.ipynb",
        "estimated_minutes": 30,
        "checklist": [
            {"id": "chk-m5-4-1", "textEn": "Simulate high-pressure hydraulic loop telemetry (inlet/outlet flow and pressure)", "textPl": "Zasymuluj telemetrię układu hydraulicznego wysokiego ciśnienia (przepływ i ciśnienie)"},
            {"id": "chk-m5-4-2", "textEn": "Implement Cumulative Sum (CUSUM) change-point detector for micro-leak tracking", "textPl": "Zaimplementuj algorytm CUSUM do wykrywania mikroskopijnych wycieków magistrali"},
            {"id": "chk-m5-4-3", "textEn": "Deploy multi-state safety state machine (NORMAL, WATCH, ALARM, EMERGENCY_SHUTDOWN)", "textPl": "Wdróż wielostanowy automat bezpieczeństwa (NORMAL, WATCH, ALARM, EMERGENCY_SHUTDOWN)"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Hydraulic System Dynamics & Micro-Leak Hazards",
                "titlePl": "Dynamika Układów Hydraulicznych i Ryzyko Mikro-Wycieków",
                "en": "Industrial hydraulic power units (HPUs) operating at 200–350 bar drive metal presses, injection molders, and robotic arms. A ruptured hydraulic hose sprays flammable oil mist, presenting severe fire hazards and catastrophic environmental fines. Standard PLC low-pressure pressure switches only trigger after $30\\%$ pressure loss—far too late. By pairing mass balance differential telemetry ($Q_{in} - Q_{out}$) with statistical process control, we detect incipient micro-fissures leaking less than $50\\text{ ml/min}$.",
                "pl": "Przemysłowe agregaty hydrauliczne (HPU) pracujące pod ciśnieniem 200–350 bar napędzają prasy, wtryskarki i ramiona robotów. Pęknięcie węża rozpyla łatwopalną mgłę olejową, stwarzając ryzyko pożaru i ogromne kary środowiskowe. Standardowe presostaty PLC reagują dopiero przy spadku ciśnienia o $30\\%$—zdecydowanie za późno. Łącząc bilans masowy ($Q_{in} - Q_{out}$) ze statystyczną kontrolą procesu, wykrywamy mikropęknięcia o wycieku poniżej $50\\text{ ml/min}$."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "Sequential Analysis: CUSUM & EWMA",
                "titlePl": "Analiza Sekwencyjna: Algorytmy CUSUM i EWMA",
                "en": "The Cumulative Sum ({{term:cusum}}) algorithm accumulates sequential deviations from the reference mean: $S_t = \\max(0, S_{t-1} + (x_t - \\mu_0 - k))$. By filtering transient pressure pulsations with {{term:ewma}} and accumulating persistent flow discrepancies in CUSUM, the system triggers a WATCH warning within 10 seconds of leak initiation and an automated EMERGENCY_SHUTDOWN command before oil pools on the factory floor.",
                "pl": "Algorytm {{term:cusum}} (Sum Skumulowanych) akumuluje sekwencyjne odchylenia od średniej referencyjnej: $S_t = \\max(0, S_{t-1} + (x_t - \\mu_0 - k))$. Filtrując chwilowe pulsacje ciśnienia za pomocą {{term:ewma}} i akumulując trwałe różnice przepływu w CUSUM, system wyzwala ostrzeżenie WATCH w ciągu 10 sekund od pojawienia się nieszczelności i wysyła sygnał EMERGENCY_SHUTDOWN przed rozlaniem oleju."
            }
        ],
        "quiz": [
            {
                "id": "q-m5-4-1",
                "questionEn": "Why is CUSUM superior to standard static threshold alarms for hydraulic leak detection?",
                "questionPl": "Dlaczego algorytm CUSUM jest lepszy od statycznych progów alarmowych w detekcji wycieków hydraulicznych?",
                "optionsEn": [
                    "CUSUM accumulates small, persistent systematic shifts over time that remain below static alarm limits",
                    "CUSUM eliminates the need for physical pressure sensors entirely",
                    "CUSUM only works when the factory is completely shut down on weekends",
                    "CUSUM automatically repairs severed hydraulic hoses using software commands"
                ],
                "optionsPl": [
                    "CUSUM akumuluje niewielkie, lecz trwałe przesunięcia średniej, które nigdy nie przekroczyłyby statycznego progu",
                    "CUSUM całkowicie eliminuje potrzebę stosowania fizycznych czujników ciśnienia",
                    "CUSUM działa wyłącznie podczas weekendowych przestojów fabryki",
                    "CUSUM automatycznie naprawia pęknięte węże hydrauliczne za pomocą oprogramowania"
                ],
                "correctIndex": 0,
                "explanationEn": "Static thresholds must be set wide to avoid false alarms from normal pump ripple; CUSUM detects subtle persistent shifts by integrating cumulative error.",
                "explanationPl": "Statyczne progi muszą być szerokie z uwagi na pulsacje pompy; CUSUM całkuje drobne, systematyczne odchylenia, wykrywając wyciek natychmiast."
            }
        ]
    },

    # =========================================================================
    # MODULE 6: Industrial Deep Learning & Edge Computer Vision
    # =========================================================================
    {
        "id": "m06_l01_neural_network_mechanics_pytorch_keras",
        "module_id": "mod-6",
        "module_number": 6,
        "lesson_number": 1,
        "title_en": "Neural Network Mechanics in PyTorch 2.x & Keras 3",
        "title_pl": "Mechanika Sieci Neuronowych w PyTorch 2.x i Keras 3",
        "summary_en": "Master deep neural network mechanics: tensors, backpropagation, AdamW optimization, and training MLPs on multi-channel sensor arrays.",
        "summary_pl": "Opanuj mechanikę sieci głębokich: tensory, propagację wsteczną, optymalizator AdamW i trenowanie sieci MLP na danych z czujników.",
        "visual_widget": "cnn_iou_sandbox",
        "colab_notebook": "m06_l01_neural_network_mechanics_pytorch_keras.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m6-1-1", "textEn": "Construct multi-layer perceptron (MLP) architecture using PyTorch 2.x nn.Module", "textPl": "Zbuduj architekturę perceptronu wielowarstwowego (MLP) w PyTorch 2.x nn.Module"},
            {"id": "chk-m6-1-2", "textEn": "Implement forward pass with ReLU and GELU activation functions", "textPl": "Zaimplementuj przejście w przód (forward pass) z funkcjami aktywacji ReLU i GELU"},
            {"id": "chk-m6-1-3", "textEn": "Train model with AdamW optimizer and plot cross-entropy loss convergence curve", "textPl": "Wytrenuj model optymalizatorem AdamW i wykreśl krzywą zbieżności funkcji straty"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Neural Network Architecture for Industrial Sensor Fusion",
                "titlePl": "Architektura Sieci Neuronowych w Fuzji Danych z Czujników",
                "en": "When industrial systems stream dozens of heterogeneous sensors simultaneously (accelerometers, thermocouples, acoustic emissions, servo motor torques), linear models and manual feature engineering hit scaling limits. Deep neural networks learn complex, non-linear representations directly from raw multi-channel tensors. In modern industrial stacks, {{term:pytorch}} and {{term:keras}} provide the standard foundation for defining computation graphs, automated differentiation (Autograd), and GPU-accelerated training.",
                "pl": "Gdy systemy przemysłowe transmitują dziesiątki zróżnicowanych czujników jednocześnie (akcelerometry, termopary, emisję akustyczną, momenty serwomotorów), modele liniowe i ręczna inżynieria cech napotykają ograniczenia. Głębokie sieci neuronowe uczą się złożonych, nieliniowych reprezentacji bezpośrednio z wielokanałowych tensorów. W nowoczesnych wdrożeniach {{term:pytorch}} i {{term:keras}} stanowią standard budowy grafów obliczeniowych i akcelerowanego treningu."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "Backpropagation & Preventing Factory Overfitting",
                "titlePl": "Propagacja Wsteczna i Zapobieganie Przeuczeniu Modeli",
                "en": "Backpropagation calculates the gradient of the loss function with respect to every model weight using the mathematical chain rule: $\\frac{\\partial \\mathcal{L}}{\\partial W} = \\frac{\\partial \\mathcal{L}}{\\partial \\hat{y}} \\frac{\\partial \\hat{y}}{\\partial W}$. Because factory datasets frequently contain repetitive operational states, deep networks can easily memorize steady-state cycles rather than physical degradation dynamics. Reliability engineers enforce Dropout ($p=0.2$), Weight Decay ($L_2$ regularization in AdamW), and Early Stopping based on validation loss.",
                "pl": "Propagacja wsteczna (backpropagation) oblicza gradient funkcji straty względem każdej wagi w sieci przy użyciu reguły łańcuchowej: $\\frac{\\partial \\mathcal{L}}{\\partial W} = \\frac{\\partial \\mathcal{L}}{\\partial \\hat{y}} \\frac{\\partial \\hat{y}}{\\partial W}$. Ponieważ dane fabryczne cechują się powtarzalnością, sieci mogą łatwo nauczyć się stanów ustalonych na pamięć. Aby temu zapobiec, stosuje się warstwy Dropout ($p=0.2$), regularyzację wag w optymalizatorze AdamW oraz Early Stopping."
            }
        ],
        "quiz": [
            {
                "id": "q-m6-1-1",
                "questionEn": "What occurs if an industrial neural network is trained without validation early stopping or weight decay?",
                "questionPl": "Co się stanie, jeśli przemysłowa sieć neuronowa zostanie wytrenowana bez techniki wczesnego zatrzymania (early stopping) lub regularyzacji wag?",
                "optionsEn": [
                    "The model overfits the training data, memorizing normal baseline noise while failing to generalize to real machine breakdowns",
                    "The physical PLC hardware burns out due to excessive GPU calculations",
                    "The model automatically converts itself into ladder logic",
                    "Training speeds up by 100x with zero accuracy loss"
                ],
                "optionsPl": [
                    "Model ulega przeuczeniu (overfitting), zapamiętując szum treningowy i tracąc zdolność wykrywania rzeczywistych awarii",
                    "Sterownik PLC ulega fizycznemu spaleniu z powodu przeciążenia obliczeniami GPU",
                    "Model automatycznie konwertuje się do języka drabinkowego PLC",
                    "Trening przyspiesza 100-krotnie bez jakiejkolwiek utraty dokładności"
                ],
                "correctIndex": 0,
                "explanationEn": "Overfitting causes the model to memorize the training set perfectly while failing completely on unseen production anomalies.",
                "explanationPl": "Przeuczenie powoduje, że model idealnie odwzorowuje zbiór treningowy, lecz traci zdolność generalizacji na nowe, unseen anomalie."
            }
        ]
    },
    {
        "id": "m06_l02_cnns_surface_defect_inspection",
        "module_id": "mod-6",
        "module_number": 6,
        "lesson_number": 2,
        "title_en": "Convolutional Neural Networks (CNNs) for Surface Defect Inspection",
        "title_pl": "Konwolucyjne Sieci Neuronowe (CNN) w Inspekcji Wad Powierzchniowych",
        "summary_en": "Build 2D convolutional neural networks with Sobel edge filters and pooling layers to automatically detect surface defects on manufactured parts.",
        "summary_pl": "Buduj konwolucyjne sieci neuronowe z filtrami Sobela i warstwami poolingu, aby automatycznie wykrywać wady powierzchniowe wyrobów.",
        "visual_widget": "cnn_iou_sandbox",
        "colab_notebook": "m06_l02_cnns_surface_defect_inspection.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m6-2-1", "textEn": "Synthesize synthetic surface defect images (scratches, pits, oil inclusions)", "textPl": "Wygeneruj syntetyczne obrazy wad powierzchniowych (rysy, wżery, plamy olejowe)"},
            {"id": "chk-m6-2-2", "textEn": "Apply 2D spatial convolution kernels (Sobel and Laplacian edge detectors)", "textPl": "Zastosuj dwuwymiarowe jądra splotu (filtry krawędziowe Sobela i Laplace'a)"},
            {"id": "chk-m6-2-3", "textEn": "Train a multi-class CNN surface inspection classifier and evaluate confusion matrix", "textPl": "Wytrenuj wieloklasowy klasyfikator CNN inspekcji jakości i oceń macierz pomyłek"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Automated Optical Inspection (AOI) on the Factory Floor",
                "titlePl": "Automatyczna Inspekcja Optyczna (AOI) na Linii Produkcyjnej",
                "en": "Manual visual inspection by human operators is slow, subjective, and prone to severe fatigue errors after long factory shifts. In high-speed manufacturing (cold-rolled steel coils, automotive stamping, semiconductor wafers), automated optical inspection stations capture high-resolution camera frames under strobe lighting. {{term:cnn}} (Convolutional Neural Networks) process these images using localized 2D filter kernels that slide across the image tensor, detecting microscopic scratches, dents, and voids regardless of their spatial location.",
                "pl": "Ręczna kontrola wizualna prowadzona przez operatorów jest powolna, subiektywna i podatna na błędy wynikające ze zmęczenia. W produkcji wielkoseryjnej (walcowanie blach, tłoczenie karoserii, płytki krzemowe) stacje automatycznej inspekcji optycznej rejestrują kadry w oświetleniu stroboskopowym. Sieci {{term:cnn}} przetwarzają te obrazy za pomocą lokalnych filtrów splotowych, wykrywając mikrorysy, wżery i pory niezależnie od ich położenia w kadrze."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "Convolution Mechanics: Kernels, Stride & Pooling",
                "titlePl": "Mechanika Konwolucji: Jądra Splotu, Krok i Warstwy Poolingu",
                "en": "A 2D convolution computes the element-wise dot product between an $n \\times n$ kernel matrix and local image patches: $S(i, j) = (I * K)(i, j) = \\sum_m \\sum_n I(i-m, j-n) K(m, n)$. Shallow layers learn low-level primitives like edges and texture gradients; deeper layers combine these into semantic defect signatures (e.g. longitudinal cracks vs circular blowholes). Max pooling layers reduce spatial dimensions, conferring translation invariance so a scratch is recognized anywhere in the camera field of view.",
                "pl": "Konwolucja 2D oblicza iloczyn skalarny jądra $n \\times n$ z wycinkiem obrazu: $S(i, j) = (I * K)(i, j) = \\sum_m \\sum_n I(i-m, j-n) K(m, n)$. Płytkie warstwy wykrywają krawędzie i gradienty jasności; głębsze łączą je w cechy semantyczne (np. pęknięcia wzdłużne vs pęcherze gazowe). Warstwy Max Pooling redukują wymiary przestrzenne, zapewniając niezmienniczość translacyjną."
            }
        ],
        "quiz": [
            {
                "id": "q-m6-2-1",
                "questionEn": "What is the primary benefit of Max Pooling layers in an industrial surface inspection CNN?",
                "questionPl": "Jaka jest główna korzyść ze stosowania warstw Max Pooling w przemysłowej sieci CNN do inspekcji powierzchni?",
                "optionsEn": [
                    "They reduce spatial dimensionality and provide translation invariance so defects are recognized regardless of slight conveyor belt shifts",
                    "They convert RGB color images into 1-bit monochrome binary arrays",
                    "They eliminate the need to collect training images from the production line",
                    "They increase image resolution by 4x using generative interpolation"
                ],
                "optionsPl": [
                    "Redukują wymiarowość przestrzenną i zapewniają niezmienniczość względem przesunięć wyrobu na taśmie przenośnika",
                    "Konwertują kolorowe obrazy RGB na 1-bitowe tablice monochromatyczne",
                    "Eliminują konieczność zbierania zdjęć treningowych z linii produkcyjnej",
                    "Zwiększają rozdzielczość obrazu 4-krotnie za pomocą interpolacji generatywnej"
                ],
                "correctIndex": 0,
                "explanationEn": "Max pooling downsamples feature maps, preserving the strongest activations while creating robustness against minor spatial vibrations.",
                "explanationPl": "Max pooling redukuje wymiarowość map cech, zachowując najsilniejsze aktywacje i uodparniając model na drgania taśmy transportowej."
            }
        ]
    },
    {
        "id": "m06_l03_transfer_learning_yolo_conveyor_inspection",
        "module_id": "mod-6",
        "module_number": 6,
        "lesson_number": 3,
        "title_en": "Transfer Learning & Ultralytics YOLO on Conveyor Inspection",
        "title_pl": "Transfer Learning i Ultralytics YOLO w Inspekcji Linii Przenośnikowej",
        "summary_en": "Leverage transfer learning and single-stage YOLO object detection to locate and classify packaging and machining defects on moving conveyor lines.",
        "summary_pl": "Wykorzystaj transfer learning i detekcję obiektów YOLO do lokalizowania i klasyfikacji wad wyrobów na ruchomych liniach przenośnikowych.",
        "visual_widget": "cnn_iou_sandbox",
        "colab_notebook": "m06_l03_transfer_learning_yolo_conveyor_inspection.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m6-3-1", "textEn": "Configure pretrained vision backbone weights using transfer learning", "textPl": "Skonfiguruj wagi wytrenowanego modelu wizyjnego za pomocą uczenia transferowego"},
            {"id": "chk-m6-3-2", "textEn": "Format defect bounding boxes in normalized coordinates [x_center, y_center, w, h]", "textPl": "Sformatuj ramki ograniczające defektów w znormalizowanych współrzędnych [x, y, w, h]"},
            {"id": "chk-m6-3-3", "textEn": "Calculate Intersection over Union (IoU) and evaluate mAP@0.50 detection metrics", "textPl": "Oblicz metrykę Intersection over Union (IoU) i oceń jakość detekcji mAP@0.50"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "The Data Scarcity Dilemma in Quality Assurance",
                "titlePl": "Dylemat Małej Liczby Danych w Zapewnieniu Jakości",
                "en": "In mature production lines, manufacturing defects occur rarely (often fewer than 50 examples per month across thousands of produced units). Training deep neural networks from scratch on 50 images yields severe overfitting. Using {{term:transfer_learning}}, we take a neural network pretrained on millions of diverse images and fine-tune only its final classification and regression heads on our small factory defect dataset, cutting training time from days to minutes while drastically improving accuracy.",
                "pl": "Na dojrzałych liniach produkcyjnych wady występują rzadko (często poniżej 50 przypadków miesięcznie na tysiące sztuk). Trening głębokich sieci od zera na 50 zdjęciach kończy się natychmiastowym przeuczeniem. Stosując {{term:transfer_learning}}, wykorzystujemy sieć wytrenowaną na milionach zróżnicowanych obrazów i dotrenowujemy jedynie warstwy końcowe na naszych danych fabrycznych, skracając czas treningu z dni do minut."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "Real-Time Detection with Ultralytics YOLO & IoU",
                "titlePl": "Detekcja w Czasie Rzeczywistym z Modelem YOLO i Metryką IoU",
                "en": "Conveyor belts travel at speeds of $1.0 - 2.5\\text{ m/s}$. Inspection systems must locate defects within 30 milliseconds to trigger pneumatic rejection arms. Single-stage object detectors like {{term:yolo}} predict bounding box coordinates $[x, y, w, h]$ and defect class probabilities in a single forward pass. Detections are evaluated using {{term:iou}} (Intersection over Union): predictions with $\\text{IoU} \\ge 0.50$ against human expert annotations count as valid True Positives.",
                "pl": "Przenośniki taśmowe poruszają się z prędkością $1.0 - 2.5\\text{ m/s}$. System inspekcji musi zlokalizować wadę w czasie poniżej 30 milisekund, aby pneumatyczny spychacz zdążył odrzucić detal. Jednoetapowe detektory, takie jak {{term:yolo}}, wyznaczają współrzędne ramek $[x, y, w, h]$ i klasy w jednym przejściu sieci. Jakość oceniana jest metryką {{term:iou}} (Intersection over Union): predykcje z $\\text{IoU} \\ge 0.50$ uznawane są za poprawne."
            }
        ],
        "quiz": [
            {
                "id": "q-m6-3-1",
                "questionEn": "On a manufacturing conveyor line moving at 1.5 m/s, what happens if an object detection model has an inference latency of 450 ms?",
                "questionPl": "Na linii produkcyjnej poruszającej się z prędkością 1.5 m/s, co się stanie, jeśli czas wnioskowania modelu detekcji wynosi 450 ms?",
                "optionsEn": [
                    "The part travels 67.5 cm past the rejection actuator before the model finishes inference, causing a missed defect ejection",
                    "The conveyor belt automatically stops and reverses direction",
                    "The image resolution increases to compensate for motion blur",
                    "The bounding box coordinates automatically shift backward in time"
                ],
                "optionsPl": [
                    "Detal przesunie się o 67.5 cm za pneumatyczny spychacz, zanim model zakończy predykcję, co uniemożliwi odrzucenie wadliwej sztuki",
                    "Taśma przenośnika automatycznie zatrzyma się i zacznie cofać",
                    "Rozdzielczość obrazu wzrośnie, aby skompensować rozmycie w ruchu",
                    "Współrzędne ramki ograniczającej automatycznie cofną się w czasie"
                ],
                "correctIndex": 0,
                "explanationEn": "In 450 ms, a 1.5 m/s line travels 0.675 m (67.5 cm). High latency causes pneumatic kickers to strike empty air, missing the defective part.",
                "explanationPl": "W czasie 450 ms detal przemieszcza się o 67.5 cm. Zbyt wysokie opóźnienie sprawia, że odrzutnik uderza w puste miejsce za wyrobem."
            }
        ]
    },
    {
        "id": "m06_l04_exporting_quantizing_onnx_capstone3",
        "module_id": "mod-6",
        "module_number": 6,
        "lesson_number": 4,
        "title_en": "Capstone 3: Exporting & Quantizing Models to ONNX for Edge Hardware",
        "title_pl": "Projekt Zwieńczeniowy 3: Eksport i Kwantyzacja Modeli do ONNX na Urządzenia Brzegowe",
        "summary_en": "Convert deep vision models to open ONNX format, apply INT8 post-training quantization, and benchmark sub-5ms edge inference on industrial IPCs.",
        "summary_pl": "Konwertuj modele do formatu ONNX, zastosuj kwantyzację INT8 i osiągnij opóźnienie poniżej 5ms na komputerach przemysłowych IPC.",
        "visual_widget": "cnn_iou_sandbox",
        "colab_notebook": "m06_l04_exporting_quantizing_onnx_capstone3.ipynb",
        "estimated_minutes": 30,
        "checklist": [
            {"id": "chk-m6-4-1", "textEn": "Export trained PyTorch model to Open Neural Network Exchange (ONNX) graph", "textPl": "Wyeksportuj wytrenowany model PyTorch do otwartego formatu ONNX"},
            {"id": "chk-m6-4-2", "textEn": "Apply INT8 Post-Training Quantization (PTQ) to compress weights and activations", "textPl": "Zastosuj kwantyzację INT8 po treningu (PTQ), redukując wagi i aktywacje"},
            {"id": "chk-m6-4-3", "textEn": "Benchmark latency and throughput (FPS) in ONNX Runtime across FP32 and INT8", "textPl": "Zmierz opóźnienie i przepustowość (FPS) w ONNX Runtime dla wersji FP32 i INT8"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Edge Computing Constraints in Manufacturing Plants",
                "titlePl": "Ograniczenia Przemysłowych Urządzeń Brzegowych (Edge Computing)",
                "en": "Factory shop floors cannot stream high-bandwidth camera feeds to cloud data centers due to cybersecurity air-gapping, unpredictable network jitter, and strict microsecond cycle times. Computer vision models must run locally on DIN-rail industrial PCs (IPCs) or edge embedded accelerators (e.g. Siemens IPC, NVIDIA Jetson, Intel OpenVINO). These ruggedized fanless units possess strict thermal envelopes ($< 25\\text{ W}$) and limited RAM.",
                "pl": "Hale produkcyjne nie mogą przesyłać strumieni wideo do chmury ze względów cyberbezpieczeństwa (odcięcie od Internetu), opóźnień sieciowych oraz wymogów czasu rzeczywistego. Modele wizyjne muszą być uruchamiane lokalnie na przemysłowych komputerach montowanych na szynie DIN (IPC) lub akceleratorach brzegowych (np. Siemens IPC, NVIDIA Jetson). Te pasywnie chłodzone urządzenia charakteryzują się ścisłym budżetem termicznym ($< 25\\text{ W}$) i ograniczoną pamięcią RAM."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "ONNX Graph Optimization & INT8 Quantization",
                "titlePl": "Optymalizacja Grafu ONNX i Kwantyzacja INT8",
                "en": "Exporting models to the Open Neural Network Exchange (ONNX) enables deployment via {{term:onnx_runtime}}, eliminating Python runtime overhead and unlocking hardware-specific C++ SIMD optimizations. Applying {{term:int8_quantization}} maps 32-bit floating point weights into 8-bit signed integers ($[-128, 127]$). This slashes model memory footprint by $75\\%$ and accelerates inference by $3\\times-4\\times$ on edge CPU/VPU cores with negligible ($<0.5\\%$) drop in defect detection accuracy.",
                "pl": "Eksport modeli do formatu ONNX pozwala na ich uruchamianie w silniku {{term:onnx_runtime}}, eliminując narzut interpretera Pythona i wykorzystując sprzętowe instrukcje C++ SIMD. Zastosowanie {{term:int8_quantization}} mapuje 32-bitowe wagi zmiennoprzecinkowe na 8-bitowe liczby całkowite ($[-128, 127]$). Zmniejsza to rozmiar modelu o $75\\%$ i przyspiesza wnioskowanie $3\\times-4\\times$ przy znikomym ($<0.5\\%$) spadku dokładności."
            }
        ],
        "quiz": [
            {
                "id": "q-m6-4-1",
                "questionEn": "What is the primary operational advantage of converting a PyTorch inspection model to an INT8 ONNX Runtime engine?",
                "questionPl": "Jaka jest główna zaleta operacyjna konwersji modelu inspekcyjnego z PyTorch do silnika INT8 w ONNX Runtime?",
                "optionsEn": [
                    "A 3x to 4x reduction in inference latency and 75% memory reduction, enabling high-FPS execution on fanless industrial IPCs",
                    "The ability to run the model without supplying any electricity to the edge computer",
                    "Automatic generation of 3D CAD engineering drawings from camera frames",
                    "Guaranteed 100.0% accuracy on every manufactured component"
                ],
                "optionsPl": [
                    "3-krotne do 4-krotne skrócenie czasu wnioskowania i redukcja pamięci o 75%, umożliwiające pracę na komputerach bezwentylatorowych IPC",
                    "Możliwość zasilania komputera brzegowego bez dostarczania energii elektrycznej",
                    "Automatyczne generowanie rysunków wykonawczych CAD 3D z obrazu kamery",
                    "Gwarancja 100.0% bezbłędności na każdym wyprodukowanym wyrobie"
                ],
                "correctIndex": 0,
                "explanationEn": "INT8 quantization slashes memory bandwidth bottlenecks and activates fast integer arithmetic units, providing major latency reductions on edge hardware.",
                "explanationPl": "Kwantyzacja INT8 eliminuje wąskie gardła przepustowości pamięci i uruchamia szybkie jednostki obliczeń całkowitoliczbowych, drastycznie skracając czas inferencji."
            }
        ]
    },

    # =========================================================================
    # MODULE 7: Industrial MLOps, Model Serving & Executive Dashboards
    # =========================================================================
    {
        "id": "m07_l01_experiment_tracking_mlflow",
        "module_id": "mod-7",
        "module_number": 7,
        "lesson_number": 1,
        "title_en": "Industrial Experiment Tracking & Governance with MLflow",
        "title_pl": "Śledzenie Eksperymentów i Zarządzanie Modelami Przemysłowymi w MLflow",
        "summary_en": "Establish rigorous MLOps experiment tracking and audit trails: log metrics, artifacts, and manage the Model Registry lifecycle.",
        "summary_pl": "Wdróż przemysłowy system MLOps: śledź metryki, rejestruj artefakty i zarządzaj cyklem życia modeli w rejestrze MLflow.",
        "visual_widget": "drift_latency_sandbox",
        "colab_notebook": "m07_l01_experiment_tracking_mlflow.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m7-1-1", "textEn": "Initialize MLflow tracking server and create dedicated manufacturing experiment", "textPl": "Zainicjalizuj serwer śledzenia MLflow i utwórz dedykowany eksperyment produkcyjny"},
            {"id": "chk-m7-1-2", "textEn": "Log hyperparameters, financial loss matrices, and serialized model artifacts", "textPl": "Zarejestruj hiperparametry, macierze strat finansowych i zserializowane artefakty"},
            {"id": "chk-m7-1-3", "textEn": "Promote candidate model across Model Registry stages: Staging to Production", "textPl": "Przeprowadź model przez etapy rejestru modeli: od Staging do Production"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Traceability & Regulatory Governance in Industrial AI",
                "titlePl": "Identyfikowalność i Wymogi Regulacyjne w Przemysłowym AI",
                "en": "In ISO 9001 and IATF 16949 certified manufacturing facilities, every process parameter affecting product quality must be strictly documented and auditable. Ad-hoc Jupyter notebook experiments without version control represent unacceptable operational risk. Open-source MLOps platforms like {{term:mlflow}} provide centralized tracking: every training run logs code commits, exact training dataset hashes, hyperparameters, and operational performance metrics.",
                "pl": "W zakładach certyfikowanych według norm ISO 9001 i IATF 16949 każdy parametr wpływający na jakość wyrobu musi być udokumentowany i audytowalny. Prowadzenie eksperymentów w niesformalizowanych notatnikach Jupyter bez kontroli wersji stanowi niedopuszczalne ryzyko. Platforma {{term:mlflow}} zapewnia centralne repozytorium: każdy trening zapisuje wersję kodu, hash zbioru danych, hiperparametry i metryki jakości."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "The Model Registry: Staging, Production & Rollback",
                "titlePl": "Rejestr Modeli: Fazy Staging, Production i Procedury Rollback",
                "en": "The MLflow Model Registry provides formal lifecycle gates. Newly trained models enter `Staging` for shadow testing against live PLC telemetry. Once reliability engineers verify that False Negative rates remain zero for 72 consecutive hours, the model is promoted to `Production`. If sensor drift or mechanical wear causes model degradation, automated rollback triggers instantaneously reinstate the previous verified model version.",
                "pl": "Rejestr modeli MLflow definiuje formalne bramki wdrożeniowe. Nowe modele trafiają do fazy `Staging` na testy równoległe (shadow testing) z rzeczywistą telemetrią PLC. Dopiero po potwierdzeniu przez inżynierów braku błędów drugiego rodzaju (False Negative) przez 72 godziny, model przechodzi do fazy `Production`. W razie wystąpienia dryfu czujników procedura rollback natychmiast przywraca poprzednią wersję."
            }
        ],
        "quiz": [
            {
                "id": "q-m7-1-1",
                "questionEn": "Why must every industrial ML model training run log the exact dataset hash and git commit hash in MLflow?",
                "questionPl": "Dlaczego każdy trening przemysłowego modelu ML musi rejestrować w MLflow dokładny hash zbioru danych i commitu git?",
                "optionsEn": [
                    "To guarantee full regulatory auditability and exact numerical reproducibility in case of customer quality recalls",
                    "To automatically double the training speed of scikit-learn models",
                    "To compress the size of the production database by 50%",
                    "Because Python requires git hashes to execute mathematical functions"
                ],
                "optionsPl": [
                    "Aby zagwarantować pełną audytowalność i powtarzalność wyników w razie reklamacji jakościowej klienta lub audytu",
                    "Aby automatycznie podwoić prędkość treningu modeli w scikit-learn",
                    "Aby zmniejszyć rozmiar produkcyjnej bazy danych o 50%",
                    "Ponieważ Python wymaga obecności hashy git do wykonywania obliczeń matematycznych"
                ],
                "correctIndex": 0,
                "explanationEn": "Traceability ensures that any quality defect identified months later can be investigated by recreating the exact model state used on that day.",
                "explanationPl": "Identyfikowalność gwarantuje, że w razie wykrycia wady po miesiącach można dokładnie odtworzyć stan modelu używanego w danym dniu."
            }
        ]
    },
    {
        "id": "m07_l02_serving_models_fastapi_rest",
        "module_id": "mod-7",
        "module_number": 7,
        "lesson_number": 2,
        "title_en": "Serving Industrial ML Models via FastAPI REST Endpoints",
        "title_pl": "Serwowanie Modeli Przemysłowych za Pomocą Punktów Końcowych REST w FastAPI",
        "summary_en": "Bridge OT and IT by packaging trained machine learning pipelines into high-performance, asynchronous FastAPI microservices with Pydantic validation.",
        "summary_pl": "Połącz świat OT i IT: wdrażaj potoki uczenia maszynowego jako asynchroniczne mikroserwisy FastAPI z walidacją typów w Pydantic.",
        "visual_widget": "drift_latency_sandbox",
        "colab_notebook": "m07_l02_serving_models_fastapi_rest.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m7-2-1", "textEn": "Define strict Pydantic telemetry input schema with physical engineering bounds", "textPl": "Zdefiniuj ścisły schemat danych telemetrycznych w Pydantic z inżynierskimi limitami fizycznymi"},
            {"id": "chk-m7-2-2", "textEn": "Build asynchronous FastAPI web service with /health and /predict endpoints", "textPl": "Zbuduj asynchroniczny serwis FastAPI z punktami końcowymi /health i /predict"},
            {"id": "chk-m7-2-3", "textEn": "Benchmark sub-5ms HTTP inference response latency under simulated SCADA payload traffic", "textPl": "Zweryfikuj czas odpowiedzi inferencji poniżej 5ms przy symulowanym ruchu zbieżnym z SCADA"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Bridging OT and IT: Industrial REST Architectures",
                "titlePl": "Most Między OT i IT: Przemysłowe Architektury REST API",
                "en": "Factory automation systems (SCADA, MES, Industrial Edge Gateways) communicate over standardized Ethernet protocols. To integrate Python machine learning models into factory workflows, models must be exposed as resilient microservices. {{term:fastapi}} has become the industrial standard due to its asynchronous ASGI architecture, automated OpenAPI documentation, and native C-speed data validation via Pydantic.",
                "pl": "Systemy automatyki fabrycznej (SCADA, MES, przemysłowe bramy brzegowe) komunikują się po protokołach Ethernet. Aby zintegrować modele uczenia maszynowego z infrastrukturą zakładową, modele muszą być wystawione jako niezawodne mikroserwisy. {{term:fastapi}} stanowi standard przemysłowy dzięki asynchronicznej architekturze ASGI, automatycznej dokumentacji OpenAPI i szybkiej walidacji typów w Pydantic."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "Input Validation & Fail-Safe Defaults",
                "titlePl": "Walidacja Danych Wejściowych i Tryby Bezpieczne (Fail-Safe)",
                "en": "In production, sensors occasionally transmit corrupted values (e.g. negative Kelvin temperatures, NaN values from disconnected 4-20mA loops). If a model receives invalid inputs without validation, it might silently output an erroneous 'Healthy' prediction. Pydantic models enforce physical sanity bounds (e.g. $4.0 \\le I \\le 20.0\\text{ mA}$). If an out-of-bounds payload arrives, the API immediately returns an HTTP 422 error and triggers a safe fallback alarm.",
                "pl": "Na produkcji czujniki przesyłają czasami uszkodzone pakiety (np. ujemne temperatury Kelvina, wartości NaN przy zerwaniu pętli 4-20mA). Jeśli model przyjmie takie dane bez walidacji, może błędnie zwrócić status 'Healthy'. Schematy Pydantic wymuszają granice fizyczne (np. $4.0 \\le I \\le 20.0\\text{ mA}$). Przekroczenie limitów powoduje natychmiastowe zwrócenie błędu HTTP 422 i załączenie alarmu bezpieczeństwa."
            }
        ],
        "quiz": [
            {
                "id": "q-m7-2-1",
                "questionEn": "Why is strict Pydantic payload validation essential when serving predictive maintenance models to SCADA systems?",
                "questionPl": "Dlaczego ścisła walidacja danych w Pydantic jest kluczowa przy serwowaniu modeli PdM dla systemów SCADA?",
                "optionsEn": [
                    "It rejects physically impossible sensor values (e.g. -500 bar) before they corrupt model inferences or mask real failures",
                    "It automatically converts Python code into Siemens PLC firmware",
                    "It eliminates the need for HTTP encryption and cybersecurity firewalls",
                    "It increases sensor battery life by reducing transmission voltages"
                ],
                "optionsPl": [
                    "Odrzuca fizycznie niemożliwe wartości pomiarowe (np. -500 bar) zanim zniekształcą one predykcję lub ukryją rzeczywistą awarię",
                    "Automatycznie konwertuje kod Pythona na firmware sterowników Siemens",
                    "Eliminuje potrzebę stosowania szyfrowania HTTP i zapór sieciowych",
                    "Wydłuża żywotność baterii czujników poprzez obniżenie napięcia transmisji"
                ],
                "correctIndex": 0,
                "explanationEn": "Without strict boundary validation, corrupted sensor inputs can lead to silent failures where a broken machine is erroneously classified as healthy.",
                "explanationPl": "Brak walidacji może doprowadzić do sytuacji, w której uszkodzony czujnik spowoduje zaklasyfikowanie uszkodzonej maszyny jako całkowicie sprawnej."
            }
        ]
    },
    {
        "id": "m07_l03_live_executive_oee_dashboards_streamlit",
        "module_id": "mod-7",
        "module_number": 7,
        "lesson_number": 3,
        "title_en": "Building Live Executive OEE & ML Dashboards with Streamlit",
        "title_pl": "Budowa Pulpitów Menedżerskich OEE i Telemetrii ML w Streamlit",
        "summary_en": "Design and build interactive real-time dashboards in Streamlit to visualize machine health, anomaly alerts, and Overall Equipment Effectiveness (OEE).",
        "summary_pl": "Projektuj i twórz interaktywne pulpity w Streamlit do wizualizacji kondycji maszyn, alarmów anomalii i wskaźnika OEE.",
        "visual_widget": "drift_latency_sandbox",
        "colab_notebook": "m07_l03_executive_oee_dashboards_streamlit.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m7-3-1", "textEn": "Calculate Overall Equipment Effectiveness (OEE = Availability x Performance x Quality)", "textPl": "Oblicz wskaźnik OEE (Dostępność x Wydajność x Jakość) dla linii produkcyjnej"},
            {"id": "chk-m7-3-2", "textEn": "Construct multi-column Streamlit dashboard layout with gauges and time-series charts", "textPl": "Zbuduj układ pulpitu w Streamlit z zegarami wskaźnikowymi i wykresami czasowymi"},
            {"id": "chk-m7-3-3", "textEn": "Implement interactive alert acknowledgement table and operator feedback logging", "textPl": "Zaimplementuj interaktywną tabelę potwierdzania alarmów i rejestr uwag operatora"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Operational KPIs: Overall Equipment Effectiveness (OEE)",
                "titlePl": "Wskaźniki Operacyjne: Całkowita Efektywność Wyposażenia (OEE)",
                "en": "Machine learning predictions are useless if factory managers and maintenance superintendents cannot understand them. In world-class manufacturing, line performance is governed by {{term:oee}} (Overall Equipment Effectiveness): $\\text{OEE} = \\text{Availability} \\times \\text{Performance} \\times \\text{Quality}$. Predictive maintenance directly protects Availability by eliminating catastrophic unplanned downtime events and protects Performance by flagging minor speed losses before micro-stops occur.",
                "pl": "Predykcje uczenia maszynowego są bezużyteczne, jeśli dyrekcja i służby utrzymania ruchu nie potrafią ich zinterpretować. W nowoczesnych fabrykach efektywność wyznacza wskaźnik {{term:oee}}: $\\text{OEE} = \\text{Dostępność} \\times \\text{Wydajność} \\times \\text{Jakość}$. Systemy predykcyjne bezpośrednio chronią Dostępność poprzez eliminację nieplanowanych przestojów oraz Wydajność, wykrywając spadki prędkości przed zatrzymaniem linii."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "Rapid Engineering Dashboards with Streamlit",
                "titlePl": "Szybkie Pulpity Inżynierskie w Bibliotece Streamlit",
                "en": "Developing custom web frontends in JavaScript can take months. Python-native frameworks like {{term:streamlit}} allow data scientists and automation engineers to convert telemetry analysis scripts into production-ready web applications in hours. Real-time metric cards, interactive anomaly score timelines, and alarm acknowledgement forms provide a single pane of glass for plant operations.",
                "pl": "Tworzenie dedykowanych interfejsów w JavaScript zajmuje całe miesiące. Framework {{term:streamlit}} pozwala inżynierom automatyki przekształcać skrypty analizy w interaktywne aplikacje webowe w zaledwie kilka godzin. Zegary wskaźnikowe, wykresy anomalii na żywo i formularze potwierdzenia alarmów tworzą zintegrowane centrum dowodzenia dla kierownictwa fabryki."
            }
        ],
        "quiz": [
            {
                "id": "q-m7-3-1",
                "questionEn": "A packaging line has 90% Availability, 85% Performance, and 98% Quality. What is its resulting OEE?",
                "questionPl": "Linia pakująca ma Dostępność 90%, Wydajność 85% oraz Jakość 98%. Jakie jest jej wynikowe OEE?",
                "optionsEn": [
                    "75.0% (0.90 x 0.85 x 0.98 = 0.7497)",
                    "91.0% (simple average of the three percentages)",
                    "100.0% (rounded up to nearest standard plant target)",
                    "60.0% (adjusted for labor efficiency)"
                ],
                "optionsPl": [
                    "75.0% (0.90 x 0.85 x 0.98 = 0.7497)",
                    "91.0% (prosta średnia arytmetyczna trzech wartości)",
                    "100.0% (zaokrąglone w górę do standardowego celu fabrycznego)",
                    "60.0% (skorygowane o wydajność pracy personelu)"
                ],
                "correctIndex": 0,
                "explanationEn": "OEE is strictly multiplicative: 0.90 * 0.85 * 0.98 = 0.7497 (approximately 75.0%).",
                "explanationPl": "Wskaźnik OEE oblicza się wyłącznie jako iloczyn trzech składowych: 0.90 * 0.85 * 0.98 = 74.97% (ok. 75.0%)."
            }
        ]
    },
    {
        "id": "m07_l04_dockerizing_pipeline_presenting_roi_capstone4",
        "module_id": "mod-7",
        "module_number": 7,
        "lesson_number": 4,
        "title_en": "Capstone 4: Dockerizing the Pipeline & Presenting Financial ROI to Management",
        "title_pl": "Projekt Zwieńczeniowy 4: Konteneryzacja w Dockerze i Prezentacja Zwrotu z Inwestycji (ROI) dla Dyrekcji",
        "summary_en": "Containerize the full predictive maintenance stack in Docker and construct an executive financial business case proving ROI, MTBF, and MTTR gains.",
        "summary_pl": "Skonteneryzuj kompletny stos predykcyjnego utrzymania ruchu w Dockerze i przygotuj prezentację biznesową dowodzącą zwrotu z inwestycji (ROI).",
        "visual_widget": "drift_latency_sandbox",
        "colab_notebook": "m07_l04_dockerizing_pipeline_presenting_roi_capstone4.ipynb",
        "estimated_minutes": 30,
        "checklist": [
            {"id": "chk-m7-4-1", "textEn": "Write production multi-stage Dockerfile packaging FastAPI server and trained ONNX models", "textPl": "Napisz produkcyjny wieloetapowy Dockerfile pakujący serwer FastAPI i modele ONNX"},
            {"id": "chk-m7-4-2", "textEn": "Calculate plant reliability impact: Mean Time Between Failures (MTBF) and MTTR", "textPl": "Oblicz wpływ na niezawodność: średni czas między awariami (MTBF) oraz MTTR"},
            {"id": "chk-m7-4-3", "textEn": "Formulate executive financial ROI business case: capital expenditure, annual savings, and payback period", "textPl": "Sformułuj analizę finansową ROI dla dyrekcji: nakłady CAPEX, roczne oszczędności i czas zwrotu"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Industrial Containerization with Docker",
                "titlePl": "Przemysłowa Konteneryzacja za Pomocą Dockera",
                "en": "A machine learning pipeline that only runs on a data scientist's laptop delivers zero factory value. To deploy reliable AI across industrial networks, we containerize our code, dependencies, and ONNX models using {{term:docker}}. A multi-stage Dockerfile compiles dependencies in a builder stage and copies only lightweight binary artifacts into a minimal, hardened Debian runtime image ($< 150\\text{ MB}$), ensuring reproducible, tamper-proof execution on edge IPCs.",
                "pl": "System uczenia maszynowego, który działa jedynie na laptopie programisty, nie przynosi fabryce żadnej wartości. Aby bezpiecznie wdrożyć sztuczną inteligencję w sieci zakładowej, konteneryzujemy kod, biblioteki i modele ONNX w środowisku {{term:docker}}. Wieloetapowy Dockerfile (multi-stage build) kompiluje zależności w pierwszym etapie i przenosi tylko niezbędne pliki do lekkiego obrazu bazowego ($< 150\\text{ MB}$), gwarantując powtarzalność na komputerach IPC."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "Speaking the C-Suite Language: Financial ROI & Reliability Metrics",
                "titlePl": "Język Zarządu: Analiza Zwrotu z Inwestycji (ROI) i Wskaźniki Niezawodności",
                "en": "Plant general managers and Chief Operating Officers (COOs) do not evaluate AI by ROC-AUC scores or loss curves; they invest based on financial Return on Investment ({{term:roi}}), extended Mean Time Between Failures ({{term:mtbf}}), and reduced Mean Time to Repair ({{term:mttr}}). By demonstrating that a \\$85,000 PdM deployment prevents \\$380,000 in catastrophic gearbox downtime with a 3.8-month payback period, engineers secure permanent operational investment.",
                "pl": "Dyrektorzy operacyjni (COO) i zarządy fabryk nie oceniają projektów AI na podstawie metryk ROC-AUC czy funkcji straty; podejmują decyzje w oparciu o finansowy zwrot z inwestycji ({{term:roi}}), wydłużenie średniego czasu bezawaryjnej pracy ({{term:mtbf}}) oraz skrócenie czasu napraw ({{term:mttr}}). Udowodnienie, że inwestycja rzędu \\$85,000 zapobiega awariom wartym \\$380,000 w 3.8 miesiąca, gwarantuje akceptację projektu."
            }
        ],
        "quiz": [
            {
                "id": "q-m7-4-1",
                "questionEn": "A plant invests $90,000 in predictive maintenance, saving $360,000 annually by eliminating 3 turbine breakdowns. What is the payback period?",
                "questionPl": "Fabryka zainwestowała $90,000 w system PdM, oszczędzając rocznie $360,000 dzięki wyeliminowaniu 3 awarii turbin. Jaki jest czas zwrotu inwestycji (payback period)?",
                "optionsEn": [
                    "3.0 months ($90,000 / ($360,000 / 12 months) = 3.0 months)",
                    "3.0 years",
                    "12.0 months",
                    "Immediate (0 days)"
                ],
                "optionsPl": [
                    "3.0 miesiące ($90,000 / ($360,000 / 12 miesięcy) = 3.0 miesiące)",
                    "3.0 lata",
                    "12.0 miesięcy",
                    "Natychmiast (0 dni)"
                ],
                "correctIndex": 0,
                "explanationEn": "Monthly savings are $360,000 / 12 = $30,000/month. The $90,000 initial capital expense is recouped in exactly 90,000 / 30,000 = 3.0 months.",
                "explanationPl": "Miesięczne oszczędności wynoszą $360,000 / 12 = $30,000/miesiąc. Koszt $90,000 zwraca się po dokładnie 90,000 / 30,000 = 3.0 miesiącach."
            }
        ]
    }
]

def main():
    script_path = Path(__file__).resolve().parent / "generate_phase3_lessons.py"
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate where m05_l01 starts and where MODULE_META starts
    m_start = content.find('{"id": "m05_l01')
    if m_start == -1:
        m_start = content.find('{\n        "id": "m05_l01')
    
    meta_start = content.find("MODULE_META = {")
    if meta_start == -1:
        raise ValueError("Could not find MODULE_META in script")

    # Find the end of the lesson array right before MODULE_META
    # Search backwards from meta_start for "]"
    closing_bracket = content.rfind("]", 0, meta_start)
    if closing_bracket == -1 or m_start == -1:
        raise ValueError("Could not find boundaries for Module 5-7 replacement")

    # Format the new modules as JSON string
    modules_json_str = ",\n".join(json.dumps(lesson, indent=4, ensure_ascii=False) for lesson in MODULES_5_TO_7)

    # Reconstruct the content
    new_content = content[:m_start] + modules_json_str + "\n" + content[closing_bracket:]

    # Also update MODULE_META for modules 5, 6, 7
    new_content = re.sub(
        r'5:\s*\{[^}]+\"sandboxType\":\s*\"fft_anomaly_sandbox\"\s*\}',
        '''5: {
        "id": "mod-5",
        "titleEn": "Time-Series Dynamics, Vibration FFT & Capstone 2",
        "titlePl": "Dynamika Szeregów Czasowych, FFT Drgań i Projekt Zwieńczeniowy 2",
        "descriptionEn": "Verify time-series stationarity (ADF test), analyze bearing kinematics via FFT spectral peaks, forecast utility consumption (ARIMA vs XGBoost), and build Capstone 2 (Hydraulic Leak Detector).",
        "descriptionPl": "Badaj stacjonarność (test ADF), analizuj kinematykę łożysk w widmie FFT, prognozuj zużycie mediów (ARIMA vs XGBoost) i zbuduj Capstone 2 (Detektor Wycieków).",
        "sandboxType": "fft_anomaly_sandbox"
    }''',
        new_content
    )

    new_content = re.sub(
        r'6:\s*\{[^}]+\"sandboxType\":\s*\"cnn_iou_sandbox\"\s*\}',
        '''6: {
        "id": "mod-6",
        "titleEn": "Industrial Deep Learning, Edge Vision & Capstone 3",
        "titlePl": "Głębokie Uczenie Przemysłowe, Wizja na Brzegu i Projekt Zwieńczeniowy 3",
        "descriptionEn": "Master neural network mechanics in PyTorch 2.x & Keras 3, detect sheet metal defects with CNNs, run Ultralytics YOLO conveyor inspection, and quantize models to ONNX INT8 (Capstone 3).",
        "descriptionPl": "Poznaj mechanikę sieci w PyTorch 2.x i Keras 3, wykrywaj wady blach z CNN, uruchamiaj detekcję YOLO na przenośniku i kwantyzuj modele do ONNX INT8 (Capstone 3).",
        "sandboxType": "cnn_iou_sandbox"
    }''',
        new_content
    )

    new_content = re.sub(
        r'7:\s*\{[^}]+\"sandboxType\":\s*\"drift_latency_sandbox\"\s*\}',
        '''7: {
        "id": "mod-7",
        "titleEn": "Industrial MLOps, Model Serving & Capstone 4",
        "titlePl": "Przemysłowy MLOps, Serwowanie Modeli i Projekt Zwieńczeniowy 4",
        "descriptionEn": "Track experiments with MLflow, serve models with low-latency FastAPI endpoints, construct live executive OEE dashboards in Streamlit, and dockerize the PdM pipeline for C-level ROI pitch (Capstone 4).",
        "descriptionPl": "Śledź eksperymenty w MLflow, udostępniaj modele przez FastAPI REST, twórz pulpity OEE w Streamlit i konteneryzuj potok w Dockerze pod prezentację ROI (Capstone 4).",
        "sandboxType": "drift_latency_sandbox"
    }''',
        new_content
    )

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Successfully patched scripts/generate_phase3_lessons.py with Phase 3B modules 5-7!")

if __name__ == "__main__":
    main()
