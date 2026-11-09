#!/usr/bin/env python3
"""
scripts/generate_phase3_lessons.py
Generates the authoritative Phase 3 curriculum in src/data/lessons/ and src/data/syllabus.json
with high precision industrial domain terminology, bilingual sections, and quizzes.
"""

import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = PROJECT_ROOT / "src" / "data" / "lessons"
SYLLABUS_FILE = PROJECT_ROOT / "src" / "data" / "syllabus.json"

LESSONS_DATA = [
    # =========================================================================
    # MODULE 1: Industrial Data Ingestion & High-Speed Processing
    # =========================================================================
    {
        "id": "m01_l01_numpy_4_20ma_telemetry",
        "module_id": "mod-1",
        "module_number": 1,
        "lesson_number": 1,
        "title_en": "Vectorized NumPy on 4-20mA Industrial Telemetry",
        "title_pl": "Wektoryzacja NumPy w Przetwarzaniu Pętli Prądowych 4-20mA",
        "summary_en": "Convert raw 16-bit ADC integer counts into calibrated 4-20mA current loop telemetry with vectorized NumPy, eliminating Python loop bottlenecks.",
        "summary_pl": "Przeliczaj surowe 16-bitowe liczby z przetwornika ADC na pętlę prądową 4-20mA za pomocą wektoryzacji NumPy, eliminując powolne pętle w Pythonie.",
        "visual_widget": "signal_filter_sandbox",
        "colab_notebook": "m01_l01_numpy_4_20ma_telemetry.ipynb",
        "estimated_minutes": 20,
        "checklist": [
            {"id": "chk-m1-1-1", "textEn": "Map 16-bit unsigned ADC counts [0, 65535] linearly to [4.0, 20.0] mA range", "textPl": "Przeskaluj 16-bitowe rejestry ADC [0, 65535] do zakresu pętli prądowej [4.0, 20.0] mA"},
            {"id": "chk-m1-1-2", "textEn": "Benchmark vectorized NumPy operations against native Python loops on 1M samples", "textPl": "Zmierz czas wektoryzacji NumPy w porównaniu do pętli for na 1 milionie próbek"},
            {"id": "chk-m1-1-3", "textEn": "Detect line breaks (< 3.8mA) and short circuits (> 20.5mA) using boolean bitmasks", "textPl": "Zidentyfikuj przerwanie przewodu (< 3.8mA) i zwarcie (> 20.5mA) za pomocą masek binarnych"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Industrial 4-20mA Current Loops in SCADA",
                "titlePl": "Pętla Prądowa 4-20mA w Architekturze SCADA",
                "en": "In heavy industrial automation, {{term:current_loop_4_20ma}} signaling is the dominant physical standard for pressure, flow, and temperature transmitters connected to {{term:plc}} and {{term:scada}} systems. Unlike voltage signals, a 4-20mA current is immune to wire resistance over hundreds of meters. A reading of 4.0 mA corresponds to 0% measurement scale, while 20.0 mA represents 100% full-scale value.",
                "pl": "W przemyśle {{term:current_loop_4_20ma}} to podstawowy standard fizyczny dla czujników ciśnienia, przepływu i temperatury podłączonych do sterowników {{term:plc}} i systemów {{term:scada}}. Sygnał prądowy jest niewrażliwy na spadki napięcia na długich liniach kablowych. Wartość 4.0 mA odpowiada 0% zakresu pomiarowego, a 20.0 mA oznacza 100% skali."
            },
            {
                "id": "sec-2",
                "type": "callout",
                "calloutType": "engineering",
                "titleEn": "Fault Diagnosis: Live Zero",
                "titlePl": "Diagnostyka Linii: 'Żywe Zero' (Live Zero)",
                "en": "The reason the scale starts at 4 mA instead of 0 mA is the 'Live Zero' principle. If a wire snaps or a thermocouple disconnects, the current drops to 0.0 mA. By applying vectorized boolean masks in NumPy, we instantly classify values below 3.6 mA as broken wire faults rather than a genuine physical zero measurement.",
                "pl": "Powodem, dla którego skala zaczyna się od 4 mA, a nie 0 mA, jest zasada 'żywego zera' (Live Zero). Jeśli kabel zostanie przerwany, prąd spada do 0.0 mA. Stosując maski binarne w NumPy, błyskawicznie kategoryzujemy odczyty poniżej 3.6 mA jako awarię linii, a nie rzeczywistą wartość zerową procesu."
            }
        ],
        "quiz": [
            {
                "id": "q-m1-1-1",
                "questionEn": "What does a current reading of 1.2 mA indicate on an industrial 4-20mA pressure transmitter?",
                "questionPl": "Co oznacza odczyt 1.2 mA na przemysłowym przetworniku ciśnienia z pętlą 4-20mA?",
                "optionsEn": [
                    "Zero pressure in the pipeline",
                    "A severed transmitter wire or loose connector fault (drop below 3.8 mA Live Zero)",
                    "Maximum operational pressure (20 mA)",
                    "Normal operation under negative gauge vacuum"
                ],
                "optionsPl": [
                    "Zerowe ciśnienie w rurociągu",
                    "Przerwany kabel lub uszkodzenie przetwornika (spadek poniżej 3.8 mA żywego zera)",
                    "Maksymalne dopuszczalne ciśnienie (20 mA)",
                    "Poprawną pracę w warunkach głębokiego podciśnienia"
                ],
                "correctIndex": 1,
                "explanationEn": "Because 4.0 mA represents true 0% physical scale, any reading below 3.6-3.8 mA is interpreted by the PLC as an open-circuit fault or broken cable.",
                "explanationPl": "Wartość 4.0 mA reprezentuje 0% skali; spadek poniżej 3.8 mA oznacza dla sterownika PLC przerwę w obwodzie lub uszkodzenie zasilania czujnika."
            }
        ]
    },
    {
        "id": "m01_l02_pandas_vs_polars_highspeed_logs",
        "module_id": "mod-1",
        "module_number": 1,
        "lesson_number": 2,
        "title_en": "Pandas 2.x vs Polars for High-Speed Factory Logs",
        "titlePl": "Pandas 2.x kontra Polars w Analizie Szybkich Logów Fabrycznych",
        "summary_en": "Process millions of high-frequency sensor events using Apache Arrow backends in Pandas 2.0 and multithreaded lazy evaluation in Polars.",
        "summary_pl": "Przetwarzaj miliony wierszy logów za pomocą formatu Apache Arrow w Pandas 2.0 oraz wielowątkowych leniwych zapytań w Polars.",
        "visual_widget": "signal_filter_sandbox",
        "colab_notebook": "m01_l02_pandas_vs_polars_highspeed_logs.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m1-2-1", "textEn": "Ingest a 2,000,000 row millisecond vibration CSV log using Pandas with PyArrow engine", "textPl": "Wczytaj 2 miliony wierszy logu wibracji w Pandas przy użyciu silnika PyArrow"},
            {"id": "chk-m1-2-2", "textEn": "Construct a Polars LazyFrame query pipeline with rolling group aggregations", "textPl": "Zbuduj potok Polars LazyFrame z kroczącymi agregacjami czasowymi"},
            {"id": "chk-m1-2-3", "textEn": "Measure memory footprint and execution speed differences between Pandas and Polars", "textPl": "Porównaj zużycie pamięci RAM i czas wykonania zapytań w Pandas i Polars"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Scaling to Multi-Gigabyte Factory Telemetry",
                "titlePl": "Skalowanie Obliczeń dla Wielkich Zbiorów SCADA",
                "en": "Traditional Pandas relies on NumPy memory buffers, causing heavy RAM duplication during joins and rolling window operations. {{term:polars}} is built from the ground up in Rust on Apache Arrow. With query graph optimization and lazy execution, Polars processes multi-million row millisecond telemetry up to 10-30x faster while using 70% less memory.",
                "pl": "Tradycyjny Pandas opiera się na tablicach NumPy, co przy dużych zbiorach powoduje wielokrotne kopiowanie danych w pamięci RAM. {{term:polars}} został stworzony od zera w języku Rust na formacie Apache Arrow. Dzięki optymalizacji grafu obliczeń (LazyFrame) Polars analizuje miliony wierszy z czujników do 30 razy szybciej przy 70% mniejszym zużyciu RAM."
            }
        ],
        "quiz": [
            {
                "id": "q-m1-2-1",
                "questionEn": "Why is Polars LazyFrame (scan_csv) significantly more memory-efficient than Pandas read_csv?",
                "questionPl": "Dlaczego Polars LazyFrame (scan_csv) zużywa znacznie mniej pamięci niż read_csv w Pandas?",
                "optionsEn": [
                    "Polars compresses all numbers into 8-bit integers automatically",
                    "Polars pushes down projection and filter predicates before loading rows into memory",
                    "Pandas is not compatible with multithreaded x86 CPUs",
                    "Polars only reads every tenth row from the disk"
                ],
                "optionsPl": [
                    "Polars automatycznie kompresuje wszystkie liczby do 8-bitowych intów",
                    "Polars stosuje optymalizację predykatów (filter pushdown) i wczytuje z dysku tylko potrzebne kolumny",
                    "Pandas nie potrafi działać na procesorach wielordzeniowych x86",
                    "Polars domyślnie odczytuje z pliku co dziesiąty wiersz"
                ],
                "correctIndex": 1,
                "explanationEn": "Polars query planner optimizes the computation graph, reading only requested columns and applying filters prior to memory allocation.",
                "explanationPl": "Planer zapytań Polars analizuje cały graf operacji, odczytując z pliku wyłącznie niezbędne kolumny i filtrując wiersze jeszcze przed alokacją pamięci."
            }
        ]
    },
    {
        "id": "m01_l03_duckdb_parquet_industrial_archives",
        "module_id": "mod-1",
        "module_number": 1,
        "lesson_number": 3,
        "title_en": "DuckDB & Parquet for Industrial SCADA Historian Archives",
        "titlePl": "DuckDB i Parquet w Archiwizacji Danych Historiana SCADA",
        "summary_en": "Execute blazingly fast SQL aggregations over multi-gigabyte partitioned Parquet directories directly without spinning up heavy database servers.",
        "summary_pl": "Wykonuj błyskawiczne zapytania SQL na wielogigabajtowych archiwach Parquet bez konieczności instalowania ciężkich serwerów bazodanowych.",
        "visual_widget": "signal_filter_sandbox",
        "colab_notebook": "m01_l03_duckdb_parquet_industrial_archives.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m1-3-1", "textEn": "Partition plant telemetry into hierarchical Parquet year/month/machine folders", "textPl": "Podziel dane telemetrii na hierarchiczne partycje Parquet (rok/miesiąc/maszyna)"},
            {"id": "chk-m1-3-2", "textEn": "Query partitioned Parquet files directly using DuckDB vectorized SQL", "textPl": "Wykonaj analityczne zapytanie SQL bezpośrednio na plikach Parquet za pomocą DuckDB"},
            {"id": "chk-m1-3-3", "textEn": "Compute time-weighted rolling machine availability (OEE) metrics in SQL", "textPl": "Oblicz wskaźnik dostępności maszyny (OEE) w oknie czasowym z poziomu SQL"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "The Power of In-Process Columnar OLAP",
                "titlePl": "Zalety Wbudowanej Bazy Kolumnowej OLAP",
                "en": "{{term:parquet}} has replaced CSV as the enterprise storage standard for industrial historians. Combined with {{term:duckdb}}, an engineer can query millions of historical sensor readings using standard SQL without needing a running PostgreSQL or InfluxDB database server. Parquet's snappy/zstd compression slashes disk storage requirements by up to 85%.",
                "pl": "Format {{term:parquet}} wyparł CSV z roli przemysłowego standardu archiwizacji danych w systemach typu historian. W połączeniu z {{term:duckdb}} inżynier może wykonywać zapytania analityczne SQL na gigabajtach danych bez konieczności stawiania serwera bazodanowego. Kompresja Parquet redukuje przestrzeń dyskową o ponad 80%."
            }
        ],
        "quiz": [
            {
                "id": "q-m1-3-1",
                "questionEn": "Why is columnar storage like Parquet dramatically faster than CSV for querying sensor temperature averages?",
                "questionPl": "Dlaczego format kolumnowy Parquet jest wielokrotnie szybszy niż CSV przy wyliczaniu średniej temperatury?",
                "optionsEn": [
                    "Parquet is stored in GPU VRAM memory only",
                    "DuckDB reads only the temperature byte column from disk, skipping all other sensor columns completely",
                    "CSV files cannot store decimal numbers",
                    "Parquet converts strings into XML tokens"
                ],
                "optionsPl": [
                    "Pliki Parquet są przechowywane wyłącznie w pamięci VRAM karty graficznej",
                    "DuckDB odczytuje z dysku wyłącznie kolumnę z temperaturą, całkowicie pomijając pozostałe dane",
                    "Pliki CSV nie potrafią zapisywać liczb zmiennoprzecinkowych",
                    "Parquet zamienia tekst na tokeny XML"
                ],
                "correctIndex": 1,
                "explanationEn": "In columnar storage, each column is stored contiguously on disk. To average one sensor across 10 million rows, only that column is read, bypassing gigabytes of irrelevant data.",
                "explanationPl": "W formacie kolumnowym dane każdej zmiennej leżą ciągle na dysku. Aby policzyć średnią, silnik pobiera z dysku jedynie bajty badanej kolumny, omijając gigabajty pozostałych danych."
            }
        ]
    },
    {
        "id": "m01_l04_data_cleaning_spike_removal",
        "module_id": "mod-1",
        "module_number": 1,
        "lesson_number": 4,
        "title_en": "Industrial Data Cleaning & Telemetry Spike Removal",
        "titlePl": "Czyszczenie Danych Przemysłowych i Usuwanie Szpilek Zakłócających",
        "summary_en": "Implement Hampel filtering (rolling median + MAD), forward-fill state imputation, and cubic spline interpolation on corrupted plant telemetry.",
        "summary_pl": "Zaimplementuj filtr Hampela (krocząca mediana + MAD), uzupełnianie w przód (LOCF) i interpolację sklejaną na uszkodzonej telemetrii.",
        "visual_widget": "signal_filter_sandbox",
        "colab_notebook": "m01_l04_data_cleaning_spike_removal.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m1-4-1", "textEn": "Implement Hampel outlier filter using rolling median and Median Absolute Deviation (MAD)", "textPl": "Zaimplementuj filtr Hampela z kroczącą medianą i odchyleniem medianowym MAD"},
            {"id": "chk-m1-4-2", "textEn": "Handle intermittent wireless packet dropouts using Last Observation Carried Forward (LOCF)", "textPl": "Obsłuż utratę pakietów w sieci bezprzewodowej metodą przenoszenia ostatniej wartości (LOCF)"},
            {"id": "chk-m1-4-3", "textEn": "Interpolate continuous physical pressure drops using cubic splines without edge ripple", "textPl": "Zinterpoluj ubytki ciągłego sygnału ciśnienia funkcjami sklejanymi 3. stopnia"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Robust Outlier Rejection: The Hampel Filter",
                "titlePl": "Odporna Filtracja Szpilek: Filtr Hampela",
                "en": "Standard standard-deviation bounds fail when sensor dropouts create huge {{term:sensor_noise}} and extreme spikes. The {{term:hampel_filter}} computes a rolling window median and replaces samples exceeding $3 \\times 1.4826 \\times \\text{MAD}$. This effectively cleans contact bounce glitches while preserving genuine industrial process step changes.",
                "pl": "Klasyczne reguły oparte na odchyleniu standardowym zawodzą, gdy błędy czujników tworzą silny {{term:sensor_noise}} i gigantyczne piki. {{term:hampel_filter}} wyznacza medianę w oknie kroczącym i zastępuje punkty przekraczające próg $3 \\times 1.4826 \\times \\text{MAD}$. Skutecznie usuwa to zakłócenia elektryczne, zachowując rzeczywiste skoki parametrów technologicznych."
            }
        ],
        "quiz": [
            {
                "id": "q-m1-4-1",
                "questionEn": "Why is Median Absolute Deviation (MAD) superior to standard deviation for detecting electrical contact spikes?",
                "questionPl": "Dlaczego odchylenie medianowe (MAD) jest lepsze od odchylenia standardowego przy wykrywaniu szpilek elektrycznych?",
                "optionsEn": [
                    "MAD runs on 8-bit microcontrollers only",
                    "A single huge spike severely inflates standard deviation, but has zero impact on the median and MAD scale",
                    "MAD is calculated using Fast Fourier Transforms",
                    "Standard deviation cannot be computed on floating point arrays"
                ],
                "optionsPl": [
                    "Wskaźnik MAD działa wyłącznie na 8-bitowych mikrokontrolerach",
                    "Pojedyncza potężna szpilka drastycznie zawyża odchylenie standardowe, ale nie ma wpływu na medianę i wskaźnik MAD",
                    "Wskaźnik MAD jest wyliczany za pomocą Szybkiej Transformaty Fouriera",
                    "Odchylenie standardowe nie może być liczone na liczbach zmiennoprzecinkowych"
                ],
                "correctIndex": 1,
                "explanationEn": "The median has a 50% breakdown point, meaning up to half the points can be contaminated by severe spikes without skewing the scale estimate.",
                "explanationPl": "Mediana ma punkt załamania 50%, co oznacza, że nawet do połowy próbek może być skrajnie zafałszowanych, a estymator skali MAD nadal pozostanie stabilny."
            }
        ]
    },

    # =========================================================================
    # MODULE 2: Exploratory Data Analysis & Robust Feature Engineering
    # =========================================================================
    {
        "id": "m02_l01_eda_hvac_oven_logs",
        "module_id": "mod-2",
        "module_number": 2,
        "lesson_number": 1,
        "title_en": "Exploratory Data Analysis (EDA) on Industrial HVAC & Oven Logs",
        "titlePl": "Eksploracyjna Analiza Danych (EDA) Pieców Hutniczych i HVAC",
        "summary_en": "Analyze industrial thermal profiles, identify heating/cooling hysteresis, and spot thermal sensor cross-correlations across oven zones.",
        "summary_pl": "Badaj profile termiczne pieców, identyfikuj histerezę nagrzewania i chłodzenia oraz wyliczaj korelacje między strefami grzewczymi.",
        "visual_widget": "scaling_outlier_sandbox",
        "colab_notebook": "m02_l01_eda_hvac_oven_logs.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m2-1-1", "textEn": "Visualize multi-zone oven temperature telemetry over a continuous 24-hour shift", "textPl": "Zwizualizuj profile temperatury stref pieca w trakcie 24-godzinnej zmiany roboczej"},
            {"id": "chk-m2-1-2", "textEn": "Calculate thermal cross-correlation matrix across all 12 heating zones", "textPl": "Oblicz macierz korelacji wzajemnej dla 12 stref grzewczych pieca"},
            {"id": "chk-m2-1-3", "textEn": "Identify thermal lag hysteresis loops between heating element power and thermocouple readings", "textPl": "Zidentyfikuj pętle histerezy termicznej między mocą grzałek a odczytem termopar"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Thermal Inertia & Zone Interactions",
                "titlePl": "Bezwładność Cieplna i Wpływ Stref na Siebie",
                "en": "In glass annealing and semiconductor diffusion furnaces, temperature must be regulated across adjacent heating zones with 0.5°C precision. Because heat conducts through metal baffles, changes in Zone 1 physically influence Zone 2 with a delay of several minutes. Constructing a {{term:correlation_matrix}} reveals which sensor channels provide redundant signals.",
                "pl": "W piecach do obróbki cieplnej szkła i metali temperatura musi być utrzymywana z precyzją do 0.5°C w wielu strefach grzewczych. Ze względu na przewodnictwo cieplne zmiana mocy w Strefie 1 wpływa na Strefę 2 z kilkuminutowym opóźnieniem. Zbudowanie {{term:correlation_matrix}} pozwala wykryć nadmiarowe czujniki i zbadać przenikanie ciepła."
            }
        ],
        "quiz": [
            {
                "id": "q-m2-1-1",
                "questionEn": "If adjacent thermocouple readings correlate at r = 0.985, what feature engineering action is recommended?",
                "questionPl": "Jeśli odczyty sąsiednich termopar korelują na poziomie r = 0.985, jakie działanie inżynierskie jest zalecane?",
                "optionsEn": [
                    "Delete both sensors immediately from the plant SCADA system",
                    "Compute their temperature gradient (delta) or retain one channel to avoid multicollinearity",
                    "Multiply both sensor values together to create an exponential feature",
                    "Invert the sign of the thermocouple readings"
                ],
                "optionsPl": [
                    "Natychmiast usunąć oba czujniki z fizycznej instalacji SCADA",
                    "Wyliczyć ich gradient (różnicę temperatur) lub zachować jeden kanał, eliminując współliniowość",
                    "Przemnożyć odczyty przez siebie, tworząc cechę wykładniczą",
                    "Odwrócić znak odczytów napięcia termopary"
                ],
                "correctIndex": 1,
                "explanationEn": "Extremely correlated features cause unstable weights in regression and tree splits. Computing the gradient (T2 - T1) isolates the actual physical heat transfer.",
                "explanationPl": "Wysoko skorelowane zmienne wywołują niestabilność wag modeli. Zastąpienie ich różnicą (T2 - T1) izoluje rzeczywisty przepływ ciepła."
            }
        ]
    },
    {
        "id": "m02_l02_feature_engineering_lag_variables",
        "module_id": "mod-2",
        "module_number": 2,
        "lesson_number": 2,
        "title_en": "Feature Engineering & Temporal Lag Variables",
        "titlePl": "Inżynieria Cech i Zmienne Opóźnione (Lag Features)",
        "summary_en": "Engineer historical memory into tabular models by creating rolling means, standard deviations, and multi-step lag variables (t-1, t-5, t-30).",
        "summary_pl": "Wprowadź pamięć procesu do modeli tabelarycznych, tworząc kroczące statystyki oraz zmienne opóźnione w czasie (t-1, t-5, t-30).",
        "visual_widget": "scaling_outlier_sandbox",
        "colab_notebook": "m02_l02_feature_engineering_lag_variables.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m2-2-1", "textEn": "Construct temporal lag features (shift by 1, 5, 15, and 30 minutes)", "textPl": "Stwórz cechy opóźnione w czasie (przesunięcia o 1, 5, 15 i 30 minut)"},
            {"id": "chk-m2-2-2", "textEn": "Compute rolling window statistical aggregations (mean, std, min, max, skew)", "textPl": "Oblicz statystyki w oknach przesuwnych (średnia, odchylenie, min, max, skośność)"},
            {"id": "chk-m2-2-3", "textEn": "Prevent temporal data leakage by dropping forward-looking shift operations", "textPl": "Zabezpiecz potok przed wyciekiem danych (data leakage) eliminując przesunięcia w przód"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Encoding Dynamic Process Memory",
                "titlePl": "Kodowanie Dynamiki i Pamięci Układu Fizycznego",
                "en": "Standard machine learning algorithms have no concept of time; they treat each row as independent. In manufacturing physics, an overheating event is dictated by heat input accumulated over the past 30 minutes. Through {{term:lag_features}} and {{term:time_domain_features}}, we feed historical context ($t-1, t-5, t-30$) directly into regression and tree ensemble columns.",
                "pl": "Standardowe modele ML traktują każdy wiersz danych jako niezależny pomiar, nie mając pojęcia o upływie czasu. W fizyce przemysłowej przegrzanie reaktora wynika z energii dostarczanej przez ostatnie 30 minut. Dzięki zastosowaniu {{term:lag_features}} oraz {{term:time_domain_features}} przekazujemy historię procesu ($t-1, t-5, t-30$) bezpośrednio do kolumn modelu."
            }
        ],
        "quiz": [
            {
                "id": "q-m2-2-1",
                "questionEn": "What constitutes temporal data leakage when creating lag features for training machine learning models?",
                "questionPl": "Co stanowi wyciek danych (data leakage) podczas tworzenia cech opóźnionych w modelach szeregów czasowych?",
                "optionsEn": [
                    "Using sensor values from future timestamps t+1 to predict failure at time t",
                    "Using sensor values from t-5 minutes to predict t",
                    "Calculating rolling mean over historical 10-minute windows",
                    "Sorting the dataframe by timestamp in ascending order"
                ],
                "optionsPl": [
                    "Użycie odczytów z przyszłych chwil czasowych t+1 do prognozowania awarii w chwili t",
                    "Użycie odczytów z chwili t-5 minut do predykcji stanu w chwili t",
                    "Obliczenie kroczącej średniej z ostatnich 10 minut pracy",
                    "Posortowanie tabeli danych rosnąco według znacznika czasu"
                ],
                "correctIndex": 0,
                "explanationEn": "Data leakage occurs when features contain information from the future (e.g. shift(-1)) that cannot exist at the moment of live inference.",
                "explanationPl": "Wyciek danych następuje w chwili użycia wartości z przyszłości (np. shift(-1)), które w rzeczywistym wdrożeniu na linii nie są jeszcze znane."
            }
        ]
    },
    {
        "id": "m02_l03_feature_scaling_spikes",
        "module_id": "mod-2",
        "module_number": 2,
        "lesson_number": 3,
        "title_en": "Feature Scaling (Standard, MinMax, Robust) under Sensor Spikes",
        "titlePl": "Odporne Skalowanie Cech w Obecności Szpilek Czujników",
        "summary_en": "Evaluate StandardScaler, MinMaxScaler, and RobustScaler on industrial motor telemetry contaminated with 5,000A electrical short-circuit spikes.",
        "summary_pl": "Porównaj zachowanie StandardScaler, MinMaxScaler i RobustScaler na danych silnika zaburzonych impulsami zwarciowymi o wartości 5000A.",
        "visual_widget": "scaling_outlier_sandbox",
        "colab_notebook": "m02_l03_feature_scaling_spikes.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m2-3-1", "textEn": "Inject severe electrical short-circuit spikes into motor current telemetry", "textPl": "Zasymuluj skrajne piki zwarciowe w telemetrii prądu pobieranego przez silnik"},
            {"id": "chk-m2-3-2", "textEn": "Fit StandardScaler, MinMaxScaler, and RobustScaler pipelines on contaminated data", "textPl": "Dopasuj skalery StandardScaler, MinMaxScaler i RobustScaler do zanieczyszczonych danych"},
            {"id": "chk-m2-3-3", "textEn": "Inspect variance compression and numerical resolution of normal operating data", "textPl": "Zbadaj spłaszczenie wariancji i rozdzielczość poprawnych danych operacyjnych"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Why StandardScaler Fails on Heavy Industrial Spikes",
                "titlePl": "Dlaczego StandardScaler Zawodzi przy Pikach Przemysłowych",
                "en": "{{term:standard_scaler}} normalizes features by subtracting mean and dividing by standard deviation. When an arc fault injects a single 5,000A spike into a 25A baseline signal, the calculated standard deviation explodes from 3.5 to 450. As a result, 99.8% of legitimate operating readings are compressed into a tiny sliver between -0.05 and +0.05.",
                "pl": "{{term:standard_scaler}} normalizuje cechy odejmując średnią i dzieląc przez odchylenie standardowe. Gdy pojedyncze zwarcie wstrzyknie pik 5000A do sygnału o bazie 25A, odchylenie standardowe eksploduje z 3.5 do 450. W rezultacie 99.8% poprawnych danych roboczych zostaje ściśniętych w bezużyteczny pasek między -0.05 a +0.05."
            },
            {
                "id": "sec-2",
                "type": "paragraph",
                "titleEn": "RobustScaler: The Industrial Benchmark",
                "titlePl": "RobustScaler: Złoty Standard w Przemyśle",
                "en": "{{term:robust_scaler}} centers data using median and scales by the {{term:iqr}} ($Q_3 - Q_1$). Because median and IQR ignore data in the extreme upper and lower 25% tails, the scaling multipliers remain pristine and immune to equipment surges.",
                "pl": "{{term:robust_scaler}} centruje dane za pomocą mediany i skaluje przez rozstęp {{term:iqr}} ($Q_3 - Q_1$). Ponieważ mediana i IQR nie zależą od skrajnych 25% wartości brzegowych, parametry skalera pozostają stabilne i niewrażliwe na udary sieciowe."
            }
        ],
        "quiz": [
            {
                "id": "q-m2-3-1",
                "questionEn": "What mathematical properties make RobustScaler resilient against motor startup current spikes?",
                "questionPl": "Jakie właściwości matematyczne zapewniają odporność RobustScaler na piki rozruchowe silnika?",
                "optionsEn": [
                    "It converts numbers to integers",
                    "It uses the median (50th percentile) and IQR (75th - 25th percentile), which completely ignore extreme outer values",
                    "It requires GPU matrix acceleration",
                    "It clips all values strictly between 0 and 1"
                ],
                "optionsPl": [
                    "Zamienia liczby na wartości całkowite",
                    "Używa mediany i rozstępu IQR (75. - 25. percentyl), które ignorują skrajne wartości w ogonach rozkładu",
                    "Wymaga akceleracji macierzowej na GPU",
                    "Przycina wszystkie wartości sztywno do przedziału od 0 do 1"
                ],
                "correctIndex": 1,
                "explanationEn": "Because IQR measures the distance between Q3 and Q1, spikes outside the 25th-75th percentile range have zero influence on the scaling factor.",
                "explanationPl": "Rozstęp IQR mierzy odległość między kwartylami Q3 i Q1; piki leżące poza środkowym pasmem 50% próbek nie mają żadnego wpływu na współczynnik skalowania."
            }
        ]
    },
    {
        "id": "m02_l04_interactive_telemetry_plotting",
        "module_id": "mod-2",
        "module_number": 2,
        "lesson_number": 4,
        "title_en": "Interactive Telemetry Plotting with Matplotlib & Plotly",
        "titlePl": "Interaktywna Wizualizacja Telemetrii z Matplotlib i Plotly",
        "summary_en": "Build synchronized multi-channel dashboards for machine telemetry, overlay threshold alarms, and enable sub-second zoom into high-speed events.",
        "summary_pl": "Twórz zsynchronizowane pulpity telemetryczne maszyn, nakładaj progi alarmowe i badaj szybkie zdarzenia awaryjne w powiększeniu.",
        "visual_widget": "scaling_outlier_sandbox",
        "colab_notebook": "m02_l04_interactive_telemetry_plotting.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m2-4-1", "textEn": "Construct a multi-panel synchronized time-series figure in Matplotlib", "textPl": "Zbuduj wielopanelowy, zsynchronizowany w czasie wykres w Matplotlib"},
            {"id": "chk-m2-4-2", "textEn": "Overlay ISO 10816 machinery vibration severity limit bands (Green, Yellow, Red)", "textPl": "Nałóż strefy alarmowe normy ISO 10816 (Zielona, Żółta, Czerwona)"},
            {"id": "chk-m2-4-3", "textEn": "Render an interactive zoomable Plotly telemetry dashboard for plant operators", "textPl": "Wygeneruj interaktywny wykres Plotly z płynnym zoomem dla operatorów linii"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Industrial Dashboarding & Operator Trust",
                "titlePl": "Wizualizacja Inżynierska i Zaufanie Operatora",
                "en": "In modern smart manufacturing, an algorithm is only as good as the operator's ability to interpret its output. Synchronizing multiple physical axes (Spindle RPM on top, Motor Current in middle, Bearing Vibration on bottom) with interactive pan/zoom enables engineers to immediately confirm whether a detected anomaly represents mechanical tool chatter or electrical drive noise.",
                "pl": "W nowoczesnej fabryce model ML jest tak użyteczny, jak zdolność operatora do zrozumienia jego wyników. Zsynchronizowanie osi czasu dla kilku parametrów (obroty wrzeciona na górze, prąd w środku, drgania łożysk na dole) z interaktywnym zoomem pozwala mechanikowi natychmiast ocenić, czy alarm to wypracowany frez, czy zakłócenie falownika."
            }
        ],
        "quiz": [
            {
                "id": "q-m2-4-1",
                "questionEn": "Why is x-axis time synchronization critical when plotting multi-sensor SCADA streams?",
                "questionPl": "Dlaczego synchronizacja osi czasu jest kluczowa przy wykreślaniu wielu kanałów ze SCADA?",
                "optionsEn": [
                    "It allows zooming into a motor current trip to see the exact millisecond vibration spike that triggered it",
                    "It makes the chart load without CSS styling",
                    "It prevents the GPU from throttling",
                    "It automatically computes the FFT magnitude"
                ],
                "optionsPl": [
                    "Umożliwia przybliżenie momentu zadziałania zabezpieczenia i zbadanie drgań w dokładnej milisekundzie awarii",
                    "Sprawia, że wykres ładuje się bez stylów CSS",
                    "Zapobiega przegrzewaniu układu graficznego",
                    "Automatycznie wylicza widmo amplitudowe FFT"
                ],
                "correctIndex": 0,
                "explanationEn": "Synchronized time axes ensure that when zooming into an electrical fault event, all temperature and vibration channels pan together to pinpoint root cause.",
                "explanationPl": "Wspólna oś czasu gwarantuje, że przybliżając moment przeciążenia elektrycznego, wszystkie wykresy temperatur i drgań przesuwają się wspólnie, ułatwiając analizę przyczyn."
            }
        ]
    },

    # =========================================================================
    # MODULE 3: Supervised Learning & Cost-Sensitive Optimization
    # =========================================================================
    {
        "id": "m03_l01_linear_regularized_regression_energy",
        "module_id": "mod-3",
        "module_number": 3,
        "lesson_number": 1,
        "title_en": "Linear & Regularized Regression for Plant Energy Forecasting",
        "titlePl": "Regresja Liniowa i Regularyzacja w Prognozowaniu Zużycia Energii",
        "summary_en": "Forecast factory electric kilowatt load using Ridge (L2) and Lasso (L1) regression, handling multicollinear sensor tags and physical constraints.",
        "summary_pl": "Prognozuj zapotrzebowanie fabryki na moc (kW) za pomocą regresji Ridge i Lasso, opanowując współliniowość czujników i ograniczenia fizyczne.",
        "visual_widget": "cost_matrix_sandbox",
        "colab_notebook": "m03_l01_linear_regularized_regression_energy.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m3-1-1", "textEn": "Fit Ordinary Least Squares (OLS) regression on plant power consumption telemetry", "textPl": "Dopasuj klasyczną regresję OLS do danych poboru mocy fabryki"},
            {"id": "chk-m3-1-2", "textEn": "Apply Ridge (L2) regression to stabilize weights under high sensor multicollinearity", "textPl": "Zastosuj regularyzację Ridge (L2), stabilizując wagi przy skorelowanych czujnikach"},
            {"id": "chk-m3-1-3", "textEn": "Perform automated feature selection using Lasso (L1) sparsity penalty", "textPl": "Wykonaj selekcję kluczowych parametrów za pomocą rzadkich wag Lasso (L1)"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Industrial Energy Management & Peak Shaving",
                "titlePl": "Zarządzanie Energią i Ścinanie Szczytów Mocy (Peak Shaving)",
                "en": "Industrial electricity contracts impose severe financial penalties when a plant exceeds its contracted power limit (15-minute peak demand). Predicting hourly megawatt demand enables automated scheduling of energy-intensive processes like arc furnaces. Regularization through Ridge (L2) prevents model coefficients from oscillating wildly when multiple sensor channels track similar thermal trends.",
                "pl": "Taryfy przemysłowe nakładają dotkliwe kary finansowe za przekroczenie mocy zamówionej w 15-minutowych oknach rozliczeniowych. Przewidywanie zapotrzebowania na energię pozwala zautomatyzować włączanie energochłonnych pieców łukowych. Regularyzacja Ridge (L2) stabilizuje wagi modelu w obecności wielu skorelowanych czujników."
            }
        ],
        "quiz": [
            {
                "id": "q-m3-1-1",
                "questionEn": "What unique advantage does Lasso (L1) regression offer over Ridge (L2) for industrial sensor selection?",
                "questionPl": "Jaką unikalną przewagę oferuje regularyzacja Lasso (L1) nad Ridge (L2) przy doborze czujników?",
                "optionsEn": [
                    "Lasso drives coefficients of redundant, uninformative sensors exactly to zero, performing automatic feature selection",
                    "Lasso requires zero training data",
                    "Lasso works only on categorical string labels",
                    "Lasso guarantees 100% R-squared accuracy"
                ],
                "optionsPl": [
                    "Lasso zeruje współczynniki nieistotnych, nadmiarowych czujników, dokonując automatycznej selekcji cech",
                    "Lasso nie wymaga żadnych danych uczących",
                    "Lasso działa wyłącznie na etykietach tekstowych",
                    "Lasso gwarantuje 100% dokładności R-kwadrat"
                ],
                "correctIndex": 0,
                "explanationEn": "L1 regularization uses diamond-shaped parameter constraints that force weights of non-predictive variables to absolute zero, simplifying hardware instrumentation.",
                "explanationPl": "Regularyzacja L1 wymusza dokładnie zerowe wagi dla mało istotnych zmiennych, co pozwala zredukować liczbę drogich czujników na instalacji."
            }
        ]
    },
    {
        "id": "m03_l02_classification_decision_trees_faults",
        "module_id": "mod-3",
        "module_number": 3,
        "lesson_number": 2,
        "title_en": "Decision Trees for Interpretable Machine Fault Diagnosis",
        "titlePl": "Drzewa Decyzyjne w Interpretowalnej Diagnostyce Usterek Maszyn",
        "summary_en": "Train white-box decision trees on engineered vibration features, visualize decision boundaries, and export logic directly to PLC ladder rules.",
        "summary_pl": "Trenuj interpretowalne drzewa decyzyjne na cechach drganiowych, wizualizuj granice podziału i eksportuj reguły do logiki drabinkowej PLC.",
        "visual_widget": "cost_matrix_sandbox",
        "colab_notebook": "m03_l02_classification_decision_trees_faults.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m3-2-1", "textEn": "Train a DecisionTreeClassifier to categorize machinery states (Healthy, Unbalance, Bearing Fault)", "textPl": "Wytrenuj klasyfikator drzewa decyzyjnego do podziału stanów maszyny (Sprawna, Niewyważenie, Awaria Łożyska)"},
            {"id": "chk-m3-2-2", "textEn": "Tune tree depth (max_depth) and minimum split samples to prevent overfitting", "textPl": "Dobierz maksymalną głębokość drzewa i min_samples_split, zapobiegając przeuczeniu"},
            {"id": "chk-m3-2-3", "textEn": "Export tree decision path rules into human-readable PLC IF-THEN ladder logic", "textPl": "Wyeksportuj reguły drzewa decyzyjnego do czytelnej logiki IF-THEN dla sterownika PLC"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "White-Box Interpretability for Plant Safety",
                "titlePl": "Interpretowalność Modeli 'White-Box' w Bezpieczeństwie Ruchu",
                "en": "In safety-critical manufacturing, automation engineers cannot accept 'black-box' neural network predictions without explainable physical justification. Decision trees provide transparent, deterministic threshold rules (e.g. IF RMS > 4.5 mm/s AND Kurtosis > 6.2 THEN Alert Bearing Fault). These rules can be audited and embedded directly into PLC safety control loops.",
                "pl": "W krytycznych instalacjach przemysłowych inżynierowie automatyki nie mogą ufać czarnym skrzynkom sieci neuronowych bez fizycznego uzasadnienia decyzji. Drzewa decyzyjne generują w pełni przejrzyste reguły progowe (np. JEŚLI RMS > 4.5 mm/s ORAZ Kurtoza > 6.2 WTEDY Alarm Łożyska), które można wdrożyć wprost do programu sterownika PLC."
            }
        ],
        "quiz": [
            {
                "id": "q-m3-2-1",
                "questionEn": "Why is restricting max_depth essential when training decision trees on industrial telemetry?",
                "questionPl": "Dlaczego ograniczenie parametru max_depth jest kluczowe przy trenowaniu drzew decyzyjnych na telemetrii?",
                "optionsEn": [
                    "Deep trees memorize single electrical noise glitches, creating overly complex, brittle branches that fail in production",
                    "Trees with depth > 5 cannot be saved to disk",
                    "Decision trees only operate when depth is equal to 1",
                    "To increase the training time"
                ],
                "optionsPl": [
                    "Głębokie drzewa zapamiętują pojedyncze szumy czujników, tworząc kruche i przeuczone reguły zawodzące na produkcji",
                    "Drzewa o głębokości > 5 nie mogą być zapisane na dysku",
                    "Drzewa decyzyjne potrafią działać wyłącznie przy głębokości równej 1",
                    "Aby celowo wydłużyć czas uczenia modelu"
                ],
                "correctIndex": 0,
                "explanationEn": "Unconstrained trees grow until every noise point is isolated. Pruning with max_depth forces the tree to capture robust general physical rules.",
                "explanationPl": "Nieograniczone drzewa rozrastają się, aż odizolują każdy pojedynczy szum. Przycinanie parametrem max_depth zmusza model do nauki ogólnych praw fizycznych."
            }
        ]
    },
    {
        "id": "m03_l03_random_forest_xgboost_lightgbm",
        "module_id": "mod-3",
        "module_number": 3,
        "lesson_number": 3,
        "title_en": "Random Forests & Gradient Boosting (XGBoost / LightGBM)",
        "titlePl": "Lasy Losowe i Gradient Boosting w Danych Tabularnych z Czujników",
        "summary_en": "Deploy Random Forests, XGBoost, and LightGBM on multi-sensor telemetry to benchmark defect classification accuracy, training speed, and feature importance.",
        "summary_pl": "Wdróż Lasy Losowe, XGBoost i LightGBM na danych z czujników, porównując precyzję detekcji wad, czas trenowania i wagę cech.",
        "visual_widget": "cost_matrix_sandbox",
        "colab_notebook": "m03_l03_random_forest_xgboost_lightgbm.ipynb",
        "estimated_minutes": 30,
        "checklist": [
            {"id": "chk-m3-3-1", "textEn": "Train a Random Forest classifier with balanced class weights on imbalanced defect logs", "textPl": "Wytrenuj klasyfikator Lasu Losowego z wagami balanced na niezbalansowanym zbiorze awarii"},
            {"id": "chk-m3-3-2", "textEn": "Fit XGBoost and LightGBM models with histogram-based binning", "textPl": "Wytrenuj modele XGBoost i LightGBM z dyskretyzacją histogramową cech"},
            {"id": "chk-m3-3-3", "textEn": "Extract and plot Gini and SHAP feature importance rankings to identify leading failure indicators", "textPl": "Wyznacz i wykreśl ranking istotności cech (SHAP i Gini), identyfikując główne wskaźniki awarii"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Ensemble Domination on Tabular Sensor Data",
                "titlePl": "Dominacja Modeli Zespołowych w Danych Tabularnych",
                "en": "While deep learning excels in computer vision, tree ensemble methods like {{term:random_forest}}, {{term:xgboost}}, and {{term:lightgbm}} dominate tabular industrial telemetry. They handle non-linear sensor relationships, tolerate unscaled columns, and naturally accommodate missing data packets without requiring extensive manual preprocessing.",
                "pl": "Podczas gdy deep learning dominuje w wizji maszynowej, modele drzewiaste, takie jak {{term:random_forest}}, {{term:xgboost}} i {{term:lightgbm}}, są bezkonkurencyjne na tabelarycznych danych z czujników. Doskonale radzą sobie z nieliniowościami, nie wymagają rygorystycznego skalowania i są odporne na pojedyncze braki w transmisji."
            }
        ],
        "quiz": [
            {
                "id": "q-m3-3-1",
                "questionEn": "Why is LightGBM significantly faster than traditional Random Forests on multi-million row sensor archives?",
                "questionPl": "Dlaczego LightGBM trenuje się znacznie szybciej niż klasyczny Las Losowy na wielomilionowych archiwach danych?",
                "optionsEn": [
                    "LightGBM uses feature histogram binning and leaf-wise tree growth rather than sorting continuous values at every split",
                    "LightGBM does not use decision trees",
                    "LightGBM trains on quantum TPU hardware only",
                    "LightGBM discards all sensor data except the first column"
                ],
                "optionsPl": [
                    "LightGBM grupuje ciągłe wartości w dyskretne histogramy i rośnie w sposób liściowy (leaf-wise), unikając ciągłego sortowania liczb",
                    "LightGBM w ogóle nie korzysta z drzew decyzyjnych",
                    "LightGBM wymaga kwantowych procesorów TPU",
                    "LightGBM odrzuca wszystkie kolumny danych poza pierwszą"
                ],
                "correctIndex": 0,
                "explanationEn": "Histogram-based discretization groups continuous sensor floats into discrete bins (e.g. 256 bins), speeding up split evaluations by orders of magnitude.",
                "explanationPl": "Dyskretyzacja histogramowa dzieli ciągłe liczby z czujników na 256 kubełków, przyspieszając testowanie podziałów drzewa o całe rzędy wielkości."
            }
        ]
    },
    {
        "id": "m03_l04_crossval_roc_cost_matrix_optuna",
        "module_id": "mod-3",
        "module_number": 3,
        "lesson_number": 4,
        "title_en": "Cost-Sensitive Evaluation, PR-AUC & Optuna Hyperparameter Tuning",
        "titlePl": "Ewaluacja Kosztowa, Krzywe PR i Optymalizacja Hiperparametrów z Optuna",
        "summary_en": "Implement TimeSeriesSplit cross-validation, align models with real financial failure costs, and run Optuna Bayesian hyperparameter optimization.",
        "summary_pl": "Zaimplementuj walidację krzyżową TimeSeriesSplit, powiąż model z finansowym kosztem awarii i zoptymalizuj hiperparametry z Optuna.",
        "visual_widget": "cost_matrix_sandbox",
        "colab_notebook": "m03_l04_crossval_roc_cost_matrix_optuna.ipynb",
        "estimated_minutes": 30,
        "checklist": [
            {"id": "chk-m3-4-1", "textEn": "Implement TimeSeriesSplit cross-validation to prevent future-data contamination", "textPl": "Zaimplementuj walidację krzyżową TimeSeriesSplit, zapobiegając wyciekom z przyszłości"},
            {"id": "chk-m3-4-2", "textEn": "Calculate Precision-Recall Area Under Curve (PR-AUC) under 99.5% class imbalance", "textPl": "Wylicz pole pod krzywą PR (PR-AUC) przy niezbalansowaniu klas na poziomie 99.5%"},
            {"id": "chk-m3-4-3", "textEn": "Run an Optuna Bayesian study minimizing plant financial loss function ($10,000 FN vs $50 FP)", "textPl": "Przeprowadź badanie bayesowskie w Optuna minimalizujące funkcję strat ($10 000 za FN vs $50 za FP)"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Time-Aware Cross-Validation & Financial Objectives",
                "titlePl": "Walidacja Czasowa i Optymalizacja Strat Finansowych",
                "en": "Standard random K-Fold cross-validation destroys the temporal arrow of time in machine data, causing massive validation leakage. We must use TimeSeriesSplit forward-chaining. Furthermore, by defining a custom loss metric driven by our {{term:asymmetric_cost_matrix}}, we employ {{term:optuna}} Bayesian optimization to tune decision thresholds and tree hyperparameters to minimize dollar costs rather than generic log-loss.",
                "pl": "Standardowa losowa walidacja K-Fold łamie porządek chronologiczny danych maszynowych, prowadząc do zafałszowania wyników testów. Należy stosować podział kroczący TimeSeriesSplit. Dodatkowo, definiując funkcję straty w oparciu o naszą {{term:asymmetric_cost_matrix}}, zaprzęgamy optymalizator {{term:optuna}} do odnalezienia progu decyzyjnego minimalizującego realne straty finansowe fabryki."
            }
        ],
        "quiz": [
            {
                "id": "q-m3-4-1",
                "questionEn": "Why is standard random K-Fold cross-validation forbidden for industrial predictive maintenance models?",
                "questionPl": "Dlaczego standardowa losowa walidacja K-Fold jest niedopuszczalna w modelach predykcyjnego utrzymania ruchu?",
                "optionsEn": [
                    "Random splitting leaks future failure patterns into training folds, yielding unrealistically optimistic test scores that fail in production",
                    "K-Fold only works when all features are normalized between 0 and 1",
                    "K-Fold produces negative probabilities",
                    "Scikit-learn blocks K-Fold on time-series datasets"
                ],
                "optionsPl": [
                    "Losowy podział sprawia, że dane z przyszłości wyciekają do zbioru uczącego, dając złudnie wysokie wyniki testów nieweryfikowalne na produkcji",
                    "K-Fold działa wyłącznie, gdy wszystkie cechy są znormalizowane od 0 do 1",
                    "K-Fold zwraca ujemne prawdopodobieństwa",
                    "Scikit-learn blokuje K-Fold dla szeregów czasowych"
                ],
                "correctIndex": 0,
                "explanationEn": "Predictive maintenance relies on learning degradation trajectories over time. Random shuffling lets the model memorize surrounding time points, creating severe data leakage.",
                "explanationPl": "Diagnostyka maszyn bazuje na trajektoriach postępującego zużycia. Losowe wymieszanie wierszy pozwala modelowi podejmować decyzje na podstawie sąsiadujących chwil czasu."
            }
        ]
    },

    # =========================================================================
    # MODULE 4: Unsupervised Diagnostics, Clustering & Capstone 1
    # =========================================================================
    {
        "id": "m04_l01_kmeans_dbscan_regimes",
        "module_id": "mod-4",
        "module_number": 4,
        "lesson_number": 1,
        "title_en": "K-Means & DBSCAN for Machine Operational Regime Detection",
        "titlePl": "Algorytmy K-Średnich i DBSCAN w Wykrywaniu Reżimów Pracy Maszyn",
        "summary_en": "Discover multi-state CNC operating modes (Idle, Warmup, Full Speed) without human labels using K-Means and isolate anomalous points with DBSCAN.",
        "summary_pl": "Odkrywaj stany pracy obrabiarki (Bieg jałowy, Rozgrzewanie, Pełna moc) bez etykiet za pomocą K-Średnich i izoluj anomalie z DBSCAN.",
        "visual_widget": "clustering_sandbox",
        "colab_notebook": "m04_l01_kmeans_dbscan_regimes.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m4-1-1", "textEn": "Partition multi-sensor CNC machine logs using K-Means across clusters K=2 to K=6", "textPl": "Podziel logi z maszyny CNC algorytmem K-Means dla liczby klastrów od 2 do 6"},
            {"id": "chk-m4-1-2", "textEn": "Compute Elbow curve inertia and Silhouette scores to select the optimal regime count", "textPl": "Wykreśl krzywą inercji (metoda łokcia) i wskaźnik Silhouette, wybierając optymalną liczbę reżimów"},
            {"id": "chk-m4-1-3", "textEn": "Deploy DBSCAN with tuned epsilon (eps) to detect non-spherical clusters and flag noise as anomalies", "textPl": "Zastosuj DBSCAN z dobranym parametrem epsilon do detekcji nieregularnych klastrów i izolacji szumu"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Automatic State Discovery in Manufacturing",
                "titlePl": "Automatyczne Odkrywanie Stanów Pracy Maszyn",
                "en": "Industrial machines rarely operate at a single operating point. An industrial mixer operates in discrete {{term:operational_regime}} modes: Idle Standby, Ingredient Blending, High-Shear Emulsification, and Cleaning-in-Place (CIP). Using {{term:k_means}}, we cluster multidimensional speed and torque telemetry into distinct clusters whose {{term:centroid}} coordinates represent golden operational baselines.",
                "pl": "Maszyny przemysłowe rzadko pracują w jednym punkcie pracy. Mieszalnik przemysłowy działa w odrębnych fazach ({{term:operational_regime}}): Bieg jałowy, Dozowanie, Mieszanie z wysokim ścinaniem i Mycie CIP. Wykorzystując {{term:k_means}}, grupujemy wielowymiarowe sygnały obrotów i momentu w klastry, których {{term:centroid}} wyznacza wzorcowy profil poboru mocy."
            }
        ],
        "quiz": [
            {
                "id": "q-m4-1-1",
                "questionEn": "What does a DBSCAN noise label of -1 signify in machine telemetry clustering?",
                "questionPl": "Co oznacza etykieta -1 w algorytmie DBSCAN w kontekście telemetrii maszynowej?",
                "optionsEn": [
                    "The machine is operating in cluster number 1 backwards",
                    "An anomalous operating state that does not satisfy density criteria of any recognized healthy operating regime",
                    "The sensor has zero electrical current",
                    "The algorithm has failed to converge"
                ],
                "optionsPl": [
                    "Maszyna pracuje w klastrze nr 1 w przeciwnym kierunku",
                    "Anomalny stan pracy, który nie mieści się w żadnym ze znanych, gęstych klastrów poprawnej pracy",
                    "Czujnik wykazuje brak przepływu prądu",
                    "Algorytm nie zbiegł się numerycznie"
                ],
                "correctIndex": 1,
                "explanationEn": "DBSCAN labels points in sparse regions as noise (-1). In predictive maintenance, these isolated noise points represent unmodeled candidate breakdown events.",
                "explanationPl": "DBSCAN oznacza rzadkie, odizolowane punkty etykietą -1 (szum). W diagnostyce maszyn te punkty stanowią bezpośrednich kandydatów na awarie lub nietypowe stany pracy."
            }
        ]
    },
    {
        "id": "m04_l02_isolation_forests_unlabeled_anomalies",
        "module_id": "mod-4",
        "module_number": 4,
        "lesson_number": 2,
        "title_en": "Isolation Forests & Elliptic Envelope for Zero-Label Anomalies",
        "titlePl": "Lasy Izolacyjne w Bezetykietowej Detekcji Anomalii Maszyn",
        "summary_en": "Train tree-based Isolation Forests and Elliptic Envelopes on raw multi-sensor telemetry to assign continuous anomaly health scores without historical failure logs.",
        "summary_pl": "Trenuj Lasy Izolacyjne na danych z czujników, wyliczając ciągły wskaźnik zdrowia maszyny bez konieczności posiadania historii uszkodzeń.",
        "visual_widget": "clustering_sandbox",
        "colab_notebook": "m04_l02_isolation_forests_unlabeled_anomalies.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m4-2-1", "textEn": "Fit sklearn.ensemble.IsolationForest on healthy baseline machine telemetry", "textPl": "Dopasuj IsolationForest do wzorcowych danych ze sprawnych cykli produkcyjnych"},
            {"id": "chk-m4-2-2", "textEn": "Compute decision_function continuous anomaly health scores across operating shifts", "textPl": "Oblicz ciągły wskaźnik anomalii za pomocą decision_function na przestrzeni zmian roboczych"},
            {"id": "chk-m4-2-3", "textEn": "Set dynamic alarm thresholds based on statistical anomaly score percentiles", "textPl": "Skonfiguruj dynamiczne progi alarmowe w oparciu o percentyle wskaźnika anomalii"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Zero-Shot Anomaly Detection in Practice",
                "titlePl": "Detekcja Anomalii 'Zero-Shot' w Praktyce Fabrycznej",
                "en": "On newly commissioned production lines, engineers do not have historical breakdown logs. {{term:isolation_forest}} bypasses this bottleneck: instead of modeling normal density, it isolates anomalies through random feature partitions. Because anomalies are few and structurally distinct, they are separated near the top of the decision trees with short path lengths, yielding an instant {{term:anomaly_score}}.",
                "pl": "Na nowo uruchomionych liniach produkcyjnych inżynierowie nie dysponują bazą historycznych awarii. {{term:isolation_forest}} rozwiązuje ten problem: zamiast modelować profil normalności, izoluje punkty losowymi podziałami cech. Ponieważ awarie są nieliczne i nietypowe, zostają odcięte tuż przy korzeniach drzew decyzyjnych, dając natychmiastowy {{term:anomaly_score}}."
            }
        ],
        "quiz": [
            {
                "id": "q-m4-2-1",
                "questionEn": "Why do anomalous machine measurements exhibit shorter average tree path lengths in an Isolation Forest?",
                "questionPl": "Dlaczego anomalne pomiary mają krótszą średnią długość ścieżki w drzewach Lasu Izolacyjnego?",
                "optionsEn": [
                    "Anomalies reside in sparse, low-density regions far from normal clusters, requiring very few random cuts to isolate",
                    "Anomalous rows are processed on higher-speed CPU cores",
                    "Tree depth is hardcoded to 1 for defects",
                    "Anomalies have higher numerical values than healthy data"
                ],
                "optionsPl": [
                    "Anomalie leżą w rzadkich obszarach przestrzeni cech, więc losowe cięcia odseparowują je w zaledwie 2-3 krokach",
                    "Wiersze z awariami są przetwarzane na szybszych rdzeniach procesora",
                    "Głębokość drzewa jest sztucznie ustawiona na 1 dla wad",
                    "Anomalie przyjmują zawsze wyższe wartości liczbowe niż dane sprawne"
                ],
                "correctIndex": 0,
                "explanationEn": "Points inside dense operational clusters require dozens of splits to isolate, while outliers in empty feature space are isolated within 2-4 splits.",
                "explanationPl": "Punkty w gęstym skupisku normalnej pracy wymagają dziesiątek podziałów do wyizolowania, podczas gdy anomalie w pustej przestrzeni zostają odcięte błyskawicznie."
            }
        ]
    },
    {
        "id": "m04_l03_pca_umap_plc_compression",
        "module_id": "mod-4",
        "module_number": 4,
        "lesson_number": 3,
        "title_en": "Dimensionality Reduction: PCA & UMAP for 50+ PLC Telemetry Tags",
        "titlePl": "Redukcja Wymiarowości: PCA i UMAP dla Ponad 50 Sygnałów PLC",
        "summary_en": "Compress high-dimensional multi-sensor arrays (temperatures, pressures, motor currents) into 2D and 3D visual health manifolds using PCA and non-linear UMAP.",
        "summary_pl": "Zredukuj dziesiątki skorelowanych zmiennych z PLC (temperatury, ciśnienia, prądy) do czytelnych map 2D/3D stanu technicznego za pomocą PCA i UMAP.",
        "visual_widget": "clustering_sandbox",
        "colab_notebook": "m04_l03_pca_umap_plc_compression.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m4-3-1", "textEn": "Fit Principal Component Analysis (PCA) on a 50-channel chemical reactor telemetry array", "textPl": "Dopasuj analizę składowych głównych (PCA) do 50 kanałów pomiarowych reaktora chemicznego"},
            {"id": "chk-m4-3-2", "textEn": "Plot explained variance ratio scree plot to determine the minimum number of principal components", "textPl": "Wykreśl wykres osypiska wariancji wyjaśnionej, dobierając optymalną liczbę składowych"},
            {"id": "chk-m4-3-3", "textEn": "Project complex machine degradation trajectories onto a 2D non-linear UMAP manifold", "textPl": "Zrzutuj trajektorie zużywania się maszyny na dwuwymiarową mapę nieliniową UMAP"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Compressing Multi-Sensor Instrumentation",
                "titlePl": "Kompresja Rozbudowanego Oprzyrządowania Czujnikowego",
                "en": "Modern industrial equipment is blanketed with dozens of sensors that produce high-dimensional multicollinear data streams. {{term:pca}} identifies orthogonal directions of maximum variance, allowing operators to monitor an entire 64-sensor chemical cracker on a single 2D screen. Non-linear techniques like {{term:umap}} preserve complex manifold geometry, showing distinct islands for normal operation versus developing wear.",
                "pl": "Nowoczesne instalacje przemysłowe są opomiarowane dziesiątkami czujników generujących wielowymiarowe, skorelowane strumienie danych. {{term:pca}} wyznacza prostopadłe osie największej wariancji, umożliwiając operatorowi nadzorowanie 64-czujnikowego reaktora na pojedynczym ekranie 2D. Nieliniowy {{term:umap}} zachowuje złożoną geometrię, ukazując stany zużycia jako odrębne wyspy."
            }
        ],
        "quiz": [
            {
                "id": "q-m4-3-1",
                "questionEn": "What does it mean if the top 3 principal components in PCA capture 91.5% of total explained variance?",
                "questionPl": "Co oznacza, że pierwsze 3 składowe główne w PCA wyjaśniają 91.5% całkowitej wariancji?",
                "optionsEn": [
                    "91.5% of the sensors were broken and excluded",
                    "Reducing 50 sensor channels down to 3 coordinates preserves 91.5% of the total informational variance",
                    "The model has a 91.5% error rate",
                    "The machine will break down in 91.5 hours"
                ],
                "optionsPl": [
                    "91.5% czujników uległo awarii i zostało wykluczonych",
                    "Redukcja 50 kanałów pomiarowych do zaledwie 3 współrzędnych zachowuje aż 91.5% całkowitej informacji i dynamiki",
                    "Model popełnia błąd na poziomie 91.5%",
                    "Maszyna ulegnie awarii za 91.5 godziny"
                ],
                "correctIndex": 1,
                "explanationEn": "Explained variance measures the proportion of system information retained after projection; 91.5% confirms that 3 coordinates fully describe the plant's physical state.",
                "explanationPl": "Wariancja wyjaśniona określa stopień zachowania informacji; 91.5% dowodzi, że zaledwie 3 liczby wystarczą do wiernego opisania stanu całej instalacji."
            }
        ]
    },
    {
        "id": "m04_l04_capstone_pdm_pipeline",
        "module_id": "mod-4",
        "module_number": 4,
        "lesson_number": 4,
        "title_en": "Capstone 1: End-to-End Predictive Maintenance Pipeline",
        "titlePl": "Projekt Zwieńczeniowy 1: Kompletny Potok Predykcyjnego Utrzymania Ruchu",
        "summary_en": "Architect a production-grade predictive maintenance pipeline: ingest raw telemetry, clean spikes, extract lag features, cluster operational regimes, and dispatch cost-optimal breakdown warnings.",
        "summary_pl": "Zaprojektuj kompletny przemysłowy potok predykcyjny: wczytaj telemetrię, usuń szpilki, wylicz cechy czasowe, wykryj reżimy pracy i wyślij optymalny kosztowo alert awarii.",
        "visual_widget": "clustering_sandbox",
        "colab_notebook": "m04_l04_capstone_pdm_pipeline.ipynb",
        "estimated_minutes": 35,
        "checklist": [
            {"id": "chk-m4-4-1", "textEn": "Ingest multi-sensor industrial milling machine dataset (vibration, current, temperature)", "textPl": "Wczytaj wielokanałowy zbiór danych frezarki (drgania, prąd, temperatura wrzeciona)"},
            {"id": "chk-m4-4-2", "textEn": "Construct an end-to-end scikit-learn cleaning and feature extraction Pipeline", "textPl": "Zbuduj potok Pipeline w scikit-learn łączący filtrację szpilek i inżynierię cech"},
            {"id": "chk-m4-4-3", "textEn": "Implement regime-aware anomaly scoring and calculate expected financial ROI savings ($)", "textPl": "Wdróż detekcję anomalii zależną od reżimu pracy i wylicz realne oszczędności finansowe ROI ($)"}
        ],
        "sections": [
            {
                "id": "sec-1",
                "type": "paragraph",
                "titleEn": "Synthesizing Modules 1 to 4 into Production ROI",
                "titlePl": "Integracja Modułów 1-4 w Realny Zysk Biznesowy",
                "en": "In this comprehensive Capstone project, we integrate all techniques learned across Modules 1 to 4 into an industrial-grade maintenance engine. Raw 4-20mA sensor data is converted via vectorized NumPy, cleaned of spikes with Hampel filtering, enriched with temporal lag features, partitioned into machine operating regimes, and evaluated with cost-sensitive threshold scoring to deliver measurable plant ROI.",
                "pl": "W tym projekcie zwieńczeniowym łączymy wszystkie techniki z Modułów 1-4 w kompletny silnik predykcyjny. Surowe dane 4-20mA są wektoryzowane w NumPy, oczyszczane filtrem Hampela, wzbogacane o cechy opóźnione w czasie, segmentowane na stany pracy i oceniane progami kosztowymi, dostarczając mierzalny zysk finansowy (ROI) dla fabryki."
            }
        ],
        "quiz": [
            {
                "id": "q-m4-4-1",
                "questionEn": "What is the primary operational metric that demonstrates the business success of a predictive maintenance pipeline?",
                "questionPl": "Jaki jest główny wskaźnik operacyjny dowodzący biznesowego sukcesu wdrożenia systemu predykcyjnego?",
                "optionsEn": [
                    "Reduction in total unplanned downtime hours and eliminated False Negative failure costs ($)",
                    "Number of Python dependencies installed in the virtual environment",
                    "File size of the final model artifact on the hard drive",
                    "Number of print statements executed per second"
                ],
                "optionsPl": [
                    "Redukcja nieplanowanych przestojów linii i eliminacja kosztów przeoczonych awarii (False Negatives)",
                    "Liczba bibliotek Pythona zainstalowanych w środowisku",
                    "Rozmiar pliku modelu na dysku komputera",
                    "Liczba komunikatów drukowanych na konsoli w ciągu sekundy"
                ],
                "correctIndex": 0,
                "explanationEn": "Executive plant management measures ML success strictly by reduced downtime, saved repair expenses, and avoided warranty failures.",
                "explanationPl": "Dyrektorzy fabryk oceniają sukces systemów AI wyłącznie przez pryzmat skróconego czasu awarii, zaoszczędzonych kosztów napraw i wyeliminowanych strat gwarancyjnych."
            }
        ]
    },

    # =========================================================================
    # MODULES 5 TO 7 (Existing Rich Curriculum Retained & Standardized)
    # =========================================================================
    {
        "id": "m05_l01_time_vs_frequency",
        "module_id": "mod-5",
        "module_number": 5,
        "lesson_number": 1,
        "title_en": "Time Domain vs Frequency Domain Vibration",
        "title_pl": "Dziedzina Czasu a Dziedzina Częstotliwości w Drganiach",
        "summary_en": "Discover why microscopic bearing race spalling is completely invisible in time signals but shines brightly in the frequency spectrum.",
        "summary_pl": "Zobacz, dlaczego mikropęknięcie bieżni jest niewidoczne w czasie, lecz tworzy potężny pik w widmie częstotliwości.",
        "visual_widget": "fft_anomaly_sandbox",
        "colab_notebook": "m05_l01_time_vs_frequency.ipynb",
        "estimated_minutes": 20,
        "checklist": [
            {"id": "chk-m5-1-1", "textEn": "Plot continuous accelerometer vibration waveform in time domain", "textPl": "Wykreśl surowy sygnał przyspieszenia drgań w dziedzinie czasu"},
            {"id": "chk-m5-1-2", "textEn": "Superimpose multiple sine waves to observe composite interference", "textPl": "Nałóż na siebie kilka sinusoid, aby zaobserwować interferencję"},
            {"id": "chk-m5-1-3", "textEn": "Demonstrate how spectral decomposition untangles complex machinery vibrations", "textPl": "Pokaż, jak dekompozycja widmowa rozplątuje drgania złożonych maszyn"}
        ],
        "sections": [
            {
                "id": "b1",
                "type": "paragraph",
                "titleEn": "Time Domain vs Frequency Domain",
                "titlePl": "Dziedzina Czasu a Częstotliwości",
                "en": "Looking at raw accelerometer readings in the {{term:time_domain}} often reveals nothing more than a noisy, jagged line. However, complex rotating equipment consists of multiple distinct physical components: the main motor shaft, a 17-tooth gearbox, cooling fans, and rolling element bearings. In the {{term:frequency_domain}}, each rotating element generates a distinct peak at its exact mechanical rotational speed.",
                "pl": "Analiza sygnału z akcelerometru w {{term:time_domain}} ukazuje jedynie zaszumiony, poszarpany wykres. Jednak maszyna wirnikowa składa się z wielu odrębnych części: wału silnika, 17-zębnej przekładni, wentylatora i łożysk tocznych. W {{term:frequency_domain}} każdy z tych podzespołów generuje odrębny, czysty pik odpowiadający jego prędkości mechanicznej."
            }
        ],
        "quiz": [
            {
                "id": "q-m5-1-1",
                "questionEn": "If an industrial motor runs at 1,800 RPM, at what frequency will its fundamental 1X unbalance peak appear?",
                "questionPl": "Jeśli silnik przemysłowy obraca się z prędkością 1800 obr/min, przy jakiej częstotliwości pojawi się jego podstawowy pik niewyważenia 1X?",
                "optionsEn": ["1,800 Hz", "30 Hz", "60 Hz", "100 Hz"],
                "optionsPl": ["1800 Hz", "30 Hz", "60 Hz", "100 Hz"],
                "correctIndex": 1,
                "explanationEn": "Frequency in Hertz is revolutions per second: 1,800 RPM / 60 seconds = 30 Hz.",
                "explanationPl": "Częstotliwość w hercach to liczba obrotów na sekundę: 1800 RPM / 60 sekund = 30 Hz."
            }
        ]
    },
    {
        "id": "m05_l02_fft_and_windowing",
        "module_id": "mod-5",
        "module_number": 5,
        "lesson_number": 2,
        "title_en": "Fast Fourier Transform (FFT) & Windowing",
        "title_pl": "Szybka Transformata Fouriera (FFT) i Okienkowanie",
        "summary_en": "Calculate magnitude spectra using numpy.fft, prevent spectral leakage using Hanning windows, and calibrate frequency bins.",
        "summary_pl": "Obliczaj widmo amplitudowe w numpy.fft, eliminuj przeciek widmowy oknem Hanninga i kalibruj osie częstotliwości.",
        "visual_widget": "fft_anomaly_sandbox",
        "colab_notebook": "m05_l02_fft_and_windowing.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m5-2-1", "textEn": "Compute discrete FFT using numpy.fft.rfft", "textPl": "Wylicz dyskretną transformatę FFT za pomocą numpy.fft.rfft"},
            {"id": "chk-m5-2-2", "textEn": "Construct the exact frequency axis vector using np.fft.rfftfreq", "textPl": "Zbuduj oś częstotliwości za pomocą np.fft.rfftfreq"},
            {"id": "chk-m5-2-3", "textEn": "Apply a Hanning window to eliminate sharp boundary discontinuities", "textPl": "Zastosuj okno Hanninga, aby zlikwidować nieciągłości na brzegach okna"}
        ],
        "sections": [
            {
                "id": "b1",
                "type": "paragraph",
                "titleEn": "Preventing Spectral Leakage with Windowing",
                "titlePl": "Eliminacja Przecieku Widmowego Okienkowaniem",
                "en": "The {{term:fft}} algorithm is one of the greatest mathematical breakthroughs in computing. To apply it accurately in predictive maintenance, one must avoid {{term:leakage_spectral}}: slicing a continuous physical waveform at non-integer cycle boundaries creates artificial discontinuity steps that splatter energy across neighboring frequency bins. Multiplying by a smooth {{term:windowing}} curve like Hanning resolves this issue.",
                "pl": "Algorytm {{term:fft}} to jedno z najważniejszych osiągnięć obliczeniowych w inżynierii. Aby stosować go poprawnie w diagnostyce maszyn, należy unikać zjawiska {{term:leakage_spectral}}: ucięcie sygnału w ułamku cyklu tworzy sztuczny skok na brzegach okna, który rozmywa energię po całym widmie. Zastosowanie funkcji {{term:windowing}} (np. okna Hanninga) eliminuje ten problem."
            }
        ],
        "quiz": [
            {
                "id": "q-m5-2-1",
                "questionEn": "What causes spectral leakage when computing an FFT on an unwindowed signal?",
                "questionPl": "Co jest przyczyną przecieku widmowego (spectral leakage) podczas liczenia FFT na sygnale bez okienka?",
                "optionsEn": [
                    "The GPU overheating during matrix multiplication",
                    "Non-integer periodicity across the window, creating an artificial step discontinuity between start and end",
                    "Too high sampling frequency exceeding 1 MHz",
                    "Using 64-bit floating point numbers"
                ],
                "optionsPl": [
                    "Przegrzanie karty graficznej podczas mnożenia macierzy",
                    "Niepełna liczba cykli w oknie, tworząca sztuczną nieciągłość (skok) między początkiem a końcem próbki",
                    "Zbyt wysoka częstotliwość próbkowania przekraczająca 1 MHz",
                    "Użycie 64-bitowych liczb zmiennoprzecinkowych"
                ],
                "correctIndex": 1,
                "explanationEn": "FFT assumes the analyzed block repeats infinitely. If the end of the block doesn't smoothly match the beginning, the sharp transition splatters energy across all frequencies.",
                "explanationPl": "FFT zakłada, że badany odcinek powtarza się w nieskończoność. Jeśli koniec odcinka nie schodzi się płynnie z początkiem, powstaje sztuczny skok rozmywający energię."
            }
        ]
    },
    {
        "id": "m05_l03_bearing_kinematics",
        "module_id": "mod-5",
        "module_number": 5,
        "lesson_number": 3,
        "title_en": "Bearing Fault Frequencies: BPFO & BPFI Kinematics",
        "title_pl": "Częstotliwości Uszkodzeń Łożysk: Kinematyka BPFO i BPFI",
        "summary_en": "Derive defect impact frequencies from bearing internal geometry: ball count, pitch diameter, roller diameter, and contact angle.",
        "summary_pl": "Wyliczaj częstotliwości uderzeń z geometrii łożyska: liczby kulek, średnicy podziałowej i kąta działania.",
        "visual_widget": "fft_anomaly_sandbox",
        "colab_notebook": "m05_l03_bearing_kinematics.ipynb",
        "estimated_minutes": 30,
        "checklist": [
            {"id": "chk-m5-3-1", "textEn": "Implement kinematic equations for BPFO, BPFI, BSF, and FTF", "textPl": "Zaimplementuj równania kinematyczne dla BPFO, BPFI, BSF oraz FTF"},
            {"id": "chk-m5-3-2", "textEn": "Identify defective outer race peak emergence in real vibration datasets", "textPl": "Zlokalizuj pojawienie się piku uszkodzenia bieżni zewnętrznej w danych"},
            {"id": "chk-m5-3-3", "textEn": "Track harmonic sidebands spaced at running speed (1X)", "textPl": "Śledź wstęgi boczne oddalone o częstotliwość obrotową (1X)"}
        ],
        "sections": [
            {
                "id": "b1",
                "type": "paragraph",
                "titleEn": "Bearing Geometric Fault Signatures",
                "titlePl": "Kinematyka Uszkodzeń Łożysk Tocznych",
                "en": "Rolling element bearings degrade in predictable metallurgical stages: microscopic subsurface fatigue leads to flaking, creating tiny pits on the outer or inner race. Every time a steel roller passes over this defect, it generates a sharp impact pulse. The exact rate of these impacts is governed by bearing geometry, generating the famous {{term:bpfo}} and {{term:bpfi}} frequencies.",
                "pl": "Łożyska toczne ulegają zużyciu w przewidywalny sposób: mikroskopijne zmęczenie podpowierzchniowe prowadzi do wykruszenia materiału (spalling) na bieżni. Każde przetoczenie się wałeczka po wyrwie generuje mikro-uderzenie. Dokładna częstotliwość tych uderzeń wynika z geometrii łożyska i definiuje wskaźniki {{term:bpfo}} oraz {{term:bpfi}}."
            }
        ],
        "quiz": [
            {
                "id": "q-m5-3-1",
                "questionEn": "What does a sharp new spectral peak at exactly BPFO indicate in vibration analysis?",
                "questionPl": "Co oznacza pojawienie się nowego, ostrego piku widmowego przy częstotliwości BPFO w wibrodiagnostyce?",
                "optionsEn": [
                    "The motor is running backwards",
                    "A localized fatigue spall has formed on the bearing outer race",
                    "The cooling fan filter is clogged with dust",
                    "The electrical grid voltage dropped by 10%"
                ],
                "optionsPl": [
                    "Silnik obraca się w przeciwnym kierunku",
                    "Na bieżni zewnętrznej łożyska pojawiło się lokalne wykruszenie zmęczeniowe",
                    "Filtr wentylatora chłodzącego został zatkany kurzem",
                    "Napięcie w sieci zasilającej fabrykę spadło o 10%"
                ],
                "correctIndex": 1,
                "explanationEn": "BPFO stands for Ball Pass Frequency Outer race. Energy concentrating at this exact frequency is empirical proof of outer ring damage.",
                "explanationPl": "BPFO (Ball Pass Frequency Outer race) to częstotliwość przejścia elementów tocznych po bieżni zewnętrznej. Pik w tym punkcie dowodzi uszkodzenia bieżni zewnętrznej."
            }
        ]
    },
    {
        "id": "m05_l04_rul_forecasting",
        "module_id": "mod-5",
        "module_number": 5,
        "lesson_number": 4,
        "title_en": "Remaining Useful Life (RUL) & Wear Forecasting",
        "title_pl": "Szacowanie Pozostałego Czasu Pracy (RUL)",
        "summary_en": "Fit degradation curves and train regression models on NASA C-MAPSS turbofan data to forecast component failure hours.",
        "summary_pl": "Dopasuj krzywe degradacji i trenuj modele regresyjne na danych NASA C-MAPSS do prognozowania godzin do awarii.",
        "visual_widget": "fft_anomaly_sandbox",
        "colab_notebook": "m05_l04_rul_forecasting.ipynb",
        "estimated_minutes": 30,
        "checklist": [
            {"id": "chk-m5-4-1", "textEn": "Construct health index trajectories from multi-sensor degradation", "textPl": "Zbuduj trajektorię wskaźnika stanu technicznego (Health Index)"},
            {"id": "chk-m5-4-2", "textEn": "Fit exponential wear models onto NASA turbofan degradation curves", "textPl": "Dopasuj wykładniczy model zużycia do danych degradacji turbin NASA"},
            {"id": "chk-m5-4-3", "textEn": "Predict Remaining Useful Life (RUL) with confidence intervals", "textPl": "Wylicz pozostały czas eksploatacji (RUL) z przedziałami ufności"}
        ],
        "sections": [
            {
                "id": "b1",
                "type": "paragraph",
                "titleEn": "Forecasting Time-to-Failure",
                "titlePl": "Prognozowanie Czasu do Awarii",
                "en": "Predictive maintenance reaches its full potential when transitioning from binary failure detection to continuous time-to-failure forecasting. {{term:rul}} estimates the exact number of cycles or operating hours remaining before critical breakdown occurs. This allows plant managers to order spare parts just-in-time and schedule overhauls during planned weekend shutdowns.",
                "pl": "Prawdziwa moc predykcyjnego utrzymania ruchu ujawnia się przy przejściu z prostej detekcji wad na prognozowanie czasu do awarii. {{term:rul}} szacuje dokładną liczbę godzin pracy, jaka pozostała do osiągnięcia stanu krytycznego. Umożliwia to zamówienie części zamiennych just-in-time i zaplanowanie serwisu na weekend."
            }
        ],
        "quiz": [
            {
                "id": "q-m5-4-1",
                "questionEn": "Why is piecewise-linear target clipping (e.g. max RUL = 125 cycles) commonly applied when training RUL models?",
                "questionPl": "Dlaczego podczas trenowania modeli RUL stosuje się obcinanie etykiety (np. max RUL = 125 cykli)?",
                "optionsEn": [
                    "Because neural networks cannot represent numbers greater than 125",
                    "A brand new component in early life does not exhibit observable physical degradation; its health is constant until wear begins",
                    "To make the dataset compatible with 8-bit microcontrollers",
                    "It prevents the GPU from running out of CUDA memory"
                ],
                "optionsPl": [
                    "Ponieważ sieci neuronowe nie potrafią przetwarzać liczb większych niż 125",
                    "Nowe urządzenie przez długi czas nie wykazuje oznak zużycia; jego stan jest stały aż do zainicjowania procesu degradacji",
                    "Aby zbiór danych zmieścił się w pamięci 8-bitowego mikrokontrolera",
                    "Zapobiega to przepełnieniu pamięci CUDA karty graficznej"
                ],
                "correctIndex": 1,
                "explanationEn": "Equipment in pristine condition does not show wear in sensor telemetry. Trying to distinguish between 300 vs 400 cycles of remaining life introduces noise; clipping caps the target to observable degradation.",
                "explanationPl": "Nowa maszyna nie wykazuje zmian w telemetrii. Próba rozróżnienia między 300 a 400 cyklami do awarii uczy model szumu; ucięcie skupia model na rzeczywistej fazie zużycia."
            }
        ]
    },

    # =========================================================================
    # MODULE 6: Computer Vision & Edge Optical Quality Inspection
    # =========================================================================
    {
        "id": "m06_l01_industrial_vision_intro",
        "module_id": "mod-6",
        "module_number": 6,
        "lesson_number": 1,
        "title_en": "Industrial Computer Vision & Surface Defects",
        "title_pl": "Wizja Przemysłowa i Wady Powierzchniowe",
        "summary_en": "Formulate optical quality control on moving sheet metal, PCB assemblies, and automotive paint surfaces.",
        "summary_pl": "Projektuj optyczną kontrolę jakości na walcowanej blasze, płytkach PCB i lakierowanych karoseriach.",
        "visual_widget": "cnn_iou_sandbox",
        "colab_notebook": "m06_l01_industrial_vision_intro.ipynb",
        "estimated_minutes": 20,
        "checklist": [
            {"id": "chk-m6-1-1", "textEn": "Inspect factory line-scan camera image pipeline", "textPl": "Zbadaj potok akwizycji obrazu z przemysłowej kamery linijkowej"},
            {"id": "chk-m6-1-2", "textEn": "Label surface scratch, pitting, and void defect classes", "textPl": "Sklasyfikuj wady powierzchniowe: rysy, wżery i pęcherze"},
            {"id": "chk-m6-1-3", "textEn": "Implement color and lighting normalization under shifting plant sunlight", "textPl": "Wdróż normalizację oświetlenia kompensującą światło słoneczne na hali"}
        ],
        "sections": [
            {
                "id": "b1",
                "type": "paragraph",
                "titleEn": "Automated Visual Inspection",
                "titlePl": "Automatyczna Inspekcja Wizyjna",
                "en": "{{term:computer_vision}} has replaced tedious, error-prone human eye inspection in high-speed manufacturing. High-resolution industrial cameras photograph every stamped car door, semiconductor wafer, or fabric roll at speeds up to 50 frames per second to flag microscopic {{term:surface_defect}} formations.",
                "pl": "{{term:computer_vision}} zastępuje męczącą i podatną na pomyłki kontrolę wzrokową na szybkich liniach produkcyjnych. Przemysłowe kamery o wysokiej rozdzielczości fotografują wytłoczki karoserii, krzemowe wafle scalone czy bele tkaniny z prędkością do 50 klatek na sekundę, wykrywając {{term:surface_defect}} w ułamku sekundy."
            }
        ],
        "quiz": [
            {
                "id": "q-m6-1-1",
                "questionEn": "What is the primary operational challenge for computer vision systems deployed on factory shop floors?",
                "questionPl": "Co stanowi największe wyzwanie operacyjne dla systemów wizyjnych na hali produkcyjnej?",
                "optionsEn": [
                    "Cameras cannot record digital pixels in industrial buildings",
                    "Lighting variability: shifting daylight from skylights, shadows from cranes, and oil mist on lenses",
                    "Robots refuse to inspect colored components",
                    "Neural networks only run when connected to cloud data centers"
                ],
                "optionsPl": [
                    "Kamery nie potrafią rejestrować cyfrowych pikseli w budynkach przemysłowych",
                    "Zmienne oświetlenie: słońce wpadające przez świetliki, cienie suwnic i mgła olejowa na obiektywach",
                    "Roboty odmawiają inspekcji kolorowych detali",
                    "Sieci neuronowe działają wyłącznie przy stałym połączeniu z chmurą"
                ],
                "correctIndex": 1,
                "explanationEn": "Factory environments suffer from shifting natural lighting, flickering fluorescent fixtures, vibrations shaking camera mounts, and airborne dust settling on optics.",
                "explanationPl": "Fabryki borykają się ze zmieniającym się światłem dziennym, migotaniem lamp, drganiami konstrukcji i osadzaniem się pyłu oraz oleju na optyce."
            }
        ]
    },
    {
        "id": "m06_l02_bounding_boxes",
        "module_id": "mod-6",
        "module_number": 6,
        "lesson_number": 2,
        "title_en": "Object Detection & Defect Bounding Boxes",
        "title_pl": "Detekcja Obiektów i Ramki Ograniczające (Bounding Boxes)",
        "summary_en": "Master bounding box parameterization [xmin, ymin, xmax, ymax] and understand multi-task classification + regression loss.",
        "summary_pl": "Opanuj parametryzację ramek ograniczających i zrozum łączoną funkcję straty klasyfikacji i regresji pozycji.",
        "visual_widget": "cnn_iou_sandbox",
        "colab_notebook": "m06_l02_bounding_boxes.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m6-2-1", "textEn": "Parse Pascal VOC and YOLO format bounding box coordinate annotations", "textPl": "Wczytaj współrzędne ramek w formatach Pascal VOC oraz YOLO"},
            {"id": "chk-m6-2-2", "textEn": "Render bounding box overlays on defective sheet metal images", "textPl": "Wyrysuj ramki defektów na zdjęciach uszkodzonej blachy"},
            {"id": "chk-m6-2-3", "textEn": "Construct multi-loss target vectors (box coords + defect class)", "textPl": "Zbuduj wektory straty łączące błąd lokalizacji ramki z klasą wady"}
        ],
        "sections": [
            {
                "id": "b1",
                "type": "paragraph",
                "titleEn": "Spatial Defect Coordinates",
                "titlePl": "Przestrzenna Lokalizacja Wad",
                "en": "Simply knowing that an image contains a defect is insufficient for automated plant repair. An object detection network outputs exact {{term:bounding_box}} coordinates identifying the spatial coordinates [x, y, width, height] of each scratch. This spatial coordinate allows a downstream polishing robot to navigate directly to the flaw.",
                "pl": "Sama informacja, że na zdjęciu jest wada, to za mało dla automatycznej linii. Model detekcji wyznacza dokładne współrzędne {{term:bounding_box}} [x, y, szerokość, wysokość] dla każdej rysy. Te współrzędne przestrzenne pozwalają robotowi polerskiemu skierować narzędzie dokładnie w miejsce uszkodzenia."
            }
        ],
        "quiz": [
            {
                "id": "q-m6-2-1",
                "questionEn": "In YOLO format, how are bounding box coordinates normalized?",
                "questionPl": "W jaki sposób normalizowane są współrzędne ramek w formacie YOLO?",
                "optionsEn": [
                    "As raw integer pixel coordinates from 0 to 4096",
                    "As floating point ratios [x_center, y_center, width, height] relative to total image width and height in range [0.0, 1.0]",
                    "In millimeters relative to the robot gripper origin",
                    "As hex strings"
                ],
                "optionsPl": [
                    "Jako surowe całkowite piksele w przedziale od 0 do 4096",
                    "Jako względne wartości zmiennoprzecinkowe [x_środek, y_środek, szerokość, wysokość] w przedziale [0.0, 1.0]",
                    "W milimetrach względem punktu bazowego chwytaka robota",
                    "Jako ciągi znaków szesnastkowych HEX"
                ],
                "correctIndex": 1,
                "explanationEn": "YOLO normalizes coordinates between 0.0 and 1.0 by dividing by image width and height, ensuring independence from camera sensor resolution.",
                "explanationPl": "Format YOLO dzieli współrzędne przez wymiary zdjęcia, dając liczby od 0.0 do 1.0 niezależne od fizycznej rozdzielczości kamery."
            }
        ]
    },
    {
        "id": "m06_l03_iou_evaluation",
        "module_id": "mod-6",
        "module_number": 6,
        "lesson_number": 3,
        "title_en": "Intersection over Union (IoU) & Model Validation",
        "title_pl": "Wskaźnik IoU (Intersection over Union) i Ewaluacja",
        "summary_en": "Compute IoU between ground truth annotations and model predictions to assess defect localization precision.",
        "summary_pl": "Obliczaj wskaźnik IoU między wzorcem a predykcją, by precyzyjnie ocenić jakość lokalizacji wad.",
        "visual_widget": "cnn_iou_sandbox",
        "colab_notebook": "m06_l03_iou_evaluation.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m6-3-1", "textEn": "Implement numpy vectorized IoU calculation function", "textPl": "Zaimplementuj zwektoryzowaną funkcję wyliczania IoU w numpy"},
            {"id": "chk-m6-3-2", "textEn": "Analyze the impact of IoU thresholding (e.g. 0.50 vs 0.75)", "textPl": "Przeanalizuj wpływ progu IoU (np. 0.50 vs 0.75) na wyniki"},
            {"id": "chk-m6-3-3", "textEn": "Calculate mean Average Precision (mAP@0.50) on test inspection batch", "textPl": "Wylicz wskaźnik mean Average Precision (mAP@0.50) na partii testowej"}
        ],
        "sections": [
            {
                "id": "b1",
                "type": "paragraph",
                "titleEn": "Measuring Localization Precision",
                "titlePl": "Mierzenie Precyzji Lokalizacji Wad",
                "en": "{{term:iou}} measures the overlap between the human inspector's {{term:ground_truth}} bounding box and the neural network's predicted box. It is calculated as the area of overlap divided by the area of union. An IoU of 1.0 represents a flawless pixel-perfect match, while an IoU < 0.50 typically fails industrial certification.",
                "pl": "Wskaźnik {{term:iou}} mierzy stopień pokrycia między zaznaczeniem wzorcowym {{term:ground_truth}} inżyniera jakości a ramką wyznaczoną przez sieć neuronową. Wylicza się go jako pole części wspólnej podzielone przez pole sumy obu obszarów. Wartość 1.0 to idealne dopasowanie, natomiast IoU < 0.50 dyskwalifikuje algorytm w testach odbiorczych."
            }
        ],
        "quiz": [
            {
                "id": "q-m6-3-1",
                "questionEn": "What is the IoU of two bounding boxes that touch at a single line edge without overlapping internal area?",
                "questionPl": "Ile wynosi IoU dwóch ramek stykających się jedynie krawędzią bez wspólnego pola wewnętrznego?",
                "optionsEn": ["0.0", "0.5", "1.0", "-1.0"],
                "optionsPl": ["0.0", "0.5", "1.0", "-1.0"],
                "correctIndex": 0,
                "explanationEn": "Because the area of intersection is zero, the numerator is 0, yielding IoU = 0 / Union = 0.0.",
                "explanationPl": "Pole części wspólnej wynosi 0, zatem licznik ułamka jest równy zero, co daje wynik IoU = 0.0."
            }
        ]
    },
    {
        "id": "m06_l04_cnn_transfer_learning",
        "module_id": "mod-6",
        "module_number": 6,
        "lesson_number": 4,
        "title_en": "Transfer Learning with Lightweight CNNs",
        "title_pl": "Uczenie Transferowe z Lekką Siecią CNN",
        "summary_en": "Fine-tune pretrained MobileNetV3 backbones with PyTorch for sub-10ms defect classification on embedded vision hardware.",
        "summary_pl": "Dotrenuj sieć MobileNetV3 w PyTorch, osiągając czas wnioskowania poniżej 10 ms na komputerze brzegowym.",
        "visual_widget": "cnn_iou_sandbox",
        "colab_notebook": "m06_l04_cnn_transfer_learning.ipynb",
        "estimated_minutes": 30,
        "checklist": [
            {"id": "chk-m6-4-1", "textEn": "Load pretrained MobileNetV3 backbone and freeze early convolutional layers", "textPl": "Wczytaj architekturę MobileNetV3 i zamroź początkowe warstwy splotowe"},
            {"id": "chk-m6-4-2", "textEn": "Replace classification head with custom 3-class industrial defect output", "textPl": "Zastąp warstwę wyjściową klasyfikatorem 3 typów wad produkcyjnych"},
            {"id": "chk-m6-4-3", "textEn": "Train with AdamW optimizer and evaluate latency benchmarks", "textPl": "Wytrenuj sieć optymalizatorem AdamW i zmierz czas odpowiedzi (latencję)"}
        ],
        "sections": [
            {
                "id": "b1",
                "type": "paragraph",
                "titleEn": "Fine-Tuning on Scarce Factory Samples",
                "titlePl": "Uczenie Transferowe na Małych Zbiorach Fabrycznych",
                "en": "Manufacturing engineers rarely have the luxury of 100,000 labeled defect images to train deep networks from scratch. Through {{term:transfer_learning}}, we take a network pretrained on ImageNet (which already understands basic geometry, edges, and textures) and fine-tune its final layers using only 50 to 100 factory samples.",
                "pl": "Inżynierowie w fabrykach rzadko mają komfort posiadania 100 000 zdjęć wad do trenowania potężnych sieci od zera. Dzięki metodzie {{term:transfer_learning}} bierzemy model wytrenowany na bazie ImageNet (który potrafi już rozpoznawać krawędzie i cienie) i dostrajamy jego ostatnie warstwy na zaledwie 50-100 fotografiach wad z hali."
            }
        ],
        "quiz": [
            {
                "id": "q-m6-4-1",
                "questionEn": "Why is MobileNet preferred over giant architectures like Vision Transformers for on-line edge sorting?",
                "questionPl": "Dlaczego MobileNet jest lepszym wyborem niż ogromne transformery wizyjne do sortowania detali na linii?",
                "optionsEn": [
                    "MobileNet runs only on solar power",
                    "Depthwise separable convolutions minimize parameter count and memory bandwidth, enabling < 10ms inference on low-power industrial PCs",
                    "Vision Transformers are illegal in automotive manufacturing",
                    "MobileNet does not require backpropagation during training"
                ],
                "optionsPl": [
                    "MobileNet działa wyłącznie na zasilaniu słonecznym",
                    "Sploty separowalne redukują liczbę parametrów i narzut pamięciowy, dając czas odpowiedzi < 10 ms na tanich komputerach przemysłowych",
                    "Transformery wizyjne są prawnie zakazane w przemyśle",
                    "MobileNet nie wymaga propagacji wstecznej podczas nauki"
                ],
                "correctIndex": 1,
                "explanationEn": "MobileNet's depthwise separable convolutions drastically cut floating-point operations (FLOPs), fitting comfortably inside tight factory latency budgets.",
                "explanationPl": "Sploty rozdzielne MobileNet drastycznie redukują liczbę operacji FLOPs, mieszcząc się w rygorystycznym budżecie czasu reakcji linii produkcyjnej."
            }
        ]
    },

    # =========================================================================
    # MODULE 7: MLOps, Model Drift & Factory Deployment
    # =========================================================================
    {
        "id": "m07_l01_drift_fundamentals",
        "module_id": "mod-7",
        "module_number": 7,
        "lesson_number": 1,
        "title_en": "Concept Drift vs Data Drift in Manufacturing",
        "title_pl": "Dryf Pojęcia (Concept Drift) a Dryf Danych w Fabryce",
        "summary_en": "Differentiate between ambient environmental sensor shifts (data drift) and fundamental changes in machine failure physics (concept drift).",
        "summary_pl": "Rozróżniaj wpływ upałów na hali (dryf danych) od fundamentalnej zmiany fizyki awarii maszyny (dryf pojęcia).",
        "visual_widget": "drift_latency_sandbox",
        "colab_notebook": "m07_l01_drift_fundamentals.ipynb",
        "estimated_minutes": 20,
        "checklist": [
            {"id": "chk-m7-1-1", "textEn": "Simulate summer ambient heat shift (+15°C baseline)", "textPl": "Zasymuluj letni wzrost temperatury otoczenia (+15°C na linii bazowej)"},
            {"id": "chk-m7-1-2", "textEn": "Simulate a change in raw material steel hardness (concept drift)", "textPl": "Zasymuluj zmianę twardości stali od nowego dostawcy (dryf pojęcia)"},
            {"id": "chk-m7-1-3", "textEn": "Track degrading model F1-score across production quarters", "textPl": "Zbadaj spadek wskaźnika F1 modelu na przestrzeni kolejnych kwartałów"}
        ],
        "sections": [
            {
                "id": "b1",
                "type": "paragraph",
                "titleEn": "Model Decay in Factory Environments",
                "titlePl": "Degradacja Modeli w Warunkach Przemysłowych",
                "en": "A machine learning model deployed to production immediately begins to decay. In manufacturing, decay takes two forms: {{term:data_drift}} occurs when input sensor distributions shift due to external environmental changes (e.g. summer factory heat). In contrast, {{term:concept_drift}} occurs when the physical relationship between sensor values and breakdown labels fundamentally mutates, such as when tool steel suppliers are switched.",
                "pl": "Model uczenia maszynowego wdrożony na produkcję od pierwszego dnia traci na aktualności. W przemyśle zjawisko to ma dwa oblicza: {{term:data_drift}} ma miejsce, gdy zmienia się rozkład wejść z powodu otoczenia (np. letnie upały na hali). Z kolei {{term:concept_drift}} oznacza fundamentalną zmianę fizycznej relacji między odczytami a awarią, np. po zmianie gatunku obrabianej stali."
            }
        ],
        "quiz": [
            {
                "id": "q-m7-1-1",
                "questionEn": "Which scenario is a classic example of Data Drift rather than Concept Drift?",
                "questionPl": "Który scenariusz jest klasycznym przykładem Dryfu Danych (Data Drift), a nie Dryfu Pojęcia?",
                "optionsEn": [
                    "A new cutting tool geometry completely alters the vibration signature of a dull blade",
                    "Summer temperatures cause all hydraulic oil temperature sensors to read 8°C higher, but the failure threshold relationship remains identical",
                    "The factory rewires from 50 Hz European grid to 60 Hz US generators",
                    "Management redefines what constitutes a quality rejection defect"
                ],
                "optionsPl": [
                    "Nowa geometria frezu całkowicie zmienia charakterystykę drgań stępionego ostrza",
                    "Letnie upały podnoszą odczyt czujników oleju hydraulicznego o 8°C, ale relacja definiująca awarię pozostaje bez zmian",
                    "Fabryka przechodzi z sieci europejskiej 50 Hz na zasilanie 60 Hz",
                    "Zarząd fabryki zmienia normy jakościowe definiujące wadliwy wyrób"
                ],
                "correctIndex": 1,
                "explanationEn": "Data drift (covariate shift) means P(X) changes while P(Y|X) remains constant. Ambient temperature increases input values without changing the mechanical failure physics.",
                "explanationPl": "W dryfie danych zmienia się rozkład wejściowy P(X), podczas gdy funkcja awarii P(Y|X) jest stała. Temperatura podnosi pomiary, nie zmieniając fizyki uszkodzenia pompy."
            }
        ]
    },
    {
        "id": "m07_l02_ks_drift_detection",
        "module_id": "mod-7",
        "module_number": 7,
        "lesson_number": 2,
        "title_en": "Automated Drift Detection with Kolmogorov-Smirnov Tests",
        "title_pl": "Automatyczna Detekcja Dryfu Testem Kołmogorowa-Smirnowa",
        "summary_en": "Run statistical hypothesis tests comparing baseline reference distributions against live production streaming telemetry.",
        "summary_pl": "Wykonuj testy statystyczne porównujące rozkład referencyjny z bieżącą telemetrią produkcyjną.",
        "visual_widget": "drift_latency_sandbox",
        "colab_notebook": "m07_l02_ks_drift_detection.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m7-2-1", "textEn": "Extract reference baseline distribution from verified training set", "textPl": "Wyodrębnij rozkład referencyjny z poprawnego zbioru treningowego"},
            {"id": "chk-m7-2-2", "textEn": "Run scipy.stats.ks_2samp across incoming daily telemetry windows", "textPl": "Uruchamiaj scipy.stats.ks_2samp dla kolejnych dziennych okien danych"},
            {"id": "chk-m7-2-3", "textEn": "Trigger automated alert when KS p-value drops below 0.01", "textPl": "Wywołaj powiadomienie alarmowe, gdy wartość p-value testu KS spadnie poniżej 0.01"}
        ],
        "sections": [
            {
                "id": "b1",
                "type": "paragraph",
                "titleEn": "Statistical Drift Guardrails",
                "titlePl": "Statystyczne Strażniki Dryfu Danych",
                "en": "Plant engineers cannot wait for catastrophic machine breakdowns to discover that an ML model has gone out of calibration. By running the non-parametric {{term:ks_test}} on daily sensor logs, we compare the cumulative distribution function of live telemetry against the golden baseline. When the statistical distance exceeds safety thresholds, an automated maintenance ticket is raised.",
                "pl": "Inżynierowie utrzymania ruchu nie mogą czekać na katastrofalną awarię, by zorientować się, że model utracił dokładność. Uruchamiając nieparametryczny {{term:ks_test}} na dziennych logach, porównujemy dystrybuantę bieżącej telemetrii z profilem wzorcowym. Gdy odległość statystyczna przekroczy normę, system generuje zlecenie kalibracji."
            }
        ],
        "quiz": [
            {
                "id": "q-m7-2-1",
                "questionEn": "What does a Kolmogorov-Smirnov p-value of 0.0001 (alpha = 0.05) indicate?",
                "questionPl": "Co oznacza wynik p-value = 0.0001 (dla poziomu istotności alpha = 0.05) w teście Kołmogorowa-Smirnowa?",
                "optionsEn": [
                    "The distributions are identical and the model is healthy",
                    "Reject the null hypothesis: there is statistically significant drift between the baseline and live telemetry",
                    "The sensor has lost electrical power",
                    "The test has timed out"
                ],
                "optionsPl": [
                    "Rozkłady są identyczne, a model jest w pełni zdatny do pracy",
                    "Odrzucenie hipotezy zerowej: wystąpił istotny statystycznie dryf parametrów między bazą a produkcją",
                    "Czujnik utracił zasilanie elektryczne",
                    "Test przekroczył limit czasu wykonania"
                ],
                "correctIndex": 1,
                "explanationEn": "A very small p-value indicates that the probability of observing this distributional difference under the null hypothesis (identical distributions) is near zero, proving significant data drift.",
                "explanationPl": "Bardzo małe p-value oznacza, że prawdopodobieństwo zaobserwowania takich różnic przy braku dryfu jest bliskie zeru, co stanowi dowód na rozkalibrowanie parametrów."
            }
        ]
    },
    {
        "id": "m07_l03_onnx_quantization",
        "module_id": "mod-7",
        "module_number": 7,
        "lesson_number": 3,
        "title_en": "Edge Model Optimization: ONNX & INT8 Quantization",
        "title_pl": "Optymalizacja Modeli Brzegowych: ONNX i Kwantyzacja INT8",
        "summary_en": "Export PyTorch models to portable ONNX format and quantize weights from FP32 to INT8 to slash inference latency.",
        "summary_pl": "Eksportuj modele do formatu ONNX i kwantyzuj wagi z FP32 do INT8, drastycznie skracając czas odpowiedzi.",
        "visual_widget": "drift_latency_sandbox",
        "colab_notebook": "m07_l03_onnx_quantization.ipynb",
        "estimated_minutes": 30,
        "checklist": [
            {"id": "chk-m7-3-1", "textEn": "Export PyTorch defect classification model to ONNX runtime format", "textPl": "Wyeksportuj model detekcji wad z PyTorch do formatu ONNX"},
            {"id": "chk-m7-3-2", "textEn": "Apply post-training dynamic INT8 quantization using onnxruntime", "textPl": "Zastosuj post-trainingową kwantyzację dynamiczną INT8 w onnxruntime"},
            {"id": "chk-m7-3-3", "textEn": "Benchmark throughput and latency on edge ARM CPU architecture", "textPl": "Zmierz przepustowość i czas odpowiedzi na architekturze procesora ARM"}
        ],
        "sections": [
            {
                "id": "b1",
                "type": "paragraph",
                "titleEn": "Sub-10ms Inference on Industrial PCs",
                "titlePl": "Czas Odpowiedzi Poniżej 10 ms na Komputerach Przemysłowych",
                "en": "Cloud data centers have immense GPU compute, but industrial machines need decisions in milliseconds right on the plant floor. Through model {{term:quantization}}, we convert model weight tensors from 32-bit floating point ({{term:fp32}}) to compact 8-bit integers ({{term:int8}}). Standardized via {{term:onnx}} and {{term:tensorrt}}, this slashes memory footprints by 75% and speeds up inference by 3x on rugged edge controllers.",
                "pl": "Serwery chmurowe oferują olbrzymią moc obliczeniową, lecz maszyny na linii wymagają decyzji w ułamku milisekundy. Dzięki procesowi {{term:quantization}} konwertujemy wagi sieci z 32-bitowych liczb zmiennoprzecinkowych ({{term:fp32}}) do 8-bitowych liczb całkowitych ({{term:int8}}). Standard {{term:onnx}} i silnik {{term:tensorrt}} zmniejszają rozmiar modelu o 75% i przyspieszają działanie 3-krotnie na sterownikach przemysłowych."
            }
        ],
        "quiz": [
            {
                "id": "q-m7-3-1",
                "questionEn": "What is the primary trade-off when applying INT8 post-training quantization?",
                "questionPl": "Jaki jest główny kompromis przy stosowaniu kwantyzacji post-trainingowej INT8?",
                "optionsEn": [
                    "Massive speedup and 4x memory reduction in exchange for a tiny (typically < 0.5%) loss in numerical precision",
                    "The model becomes completely untrainable in Python",
                    "Inference latency increases by 10x",
                    "It can only run on quantum computers"
                ],
                "optionsPl": [
                    "Ogromne przyspieszenie i 4-krotne zmniejszenie pamięci kosztem minimalnej (zazwyczaj < 0.5%) utraty precyzji obliczeń",
                    "Model traci możliwość jakiegokolwiek dalszego trenowania w Pythonie",
                    "Opóźnienie wnioskowania rośnie 10-krotnie",
                    "Działa wyłącznie na komputerach kwantowych"
                ],
                "correctIndex": 0,
                "explanationEn": "Quantization rounds continuous weights to 256 discrete integer values. This slight loss in precision is heavily outweighed by the massive reduction in RAM and cache misses.",
                "explanationPl": "Kwantyzacja zaokrągla wagi do 256 dyskretnych wartości całkowitych. Minimalny spadek dokładności jest z nawiązką rekompensowany 4-krotną redukcją zapotrzebowania na pamięć."
            }
        ]
    },
    {
        "id": "m07_l04_mlops_pipeline",
        "module_id": "mod-7",
        "module_number": 7,
        "lesson_number": 4,
        "title_en": "Factory Deployment & Continuous Retraining Pipelines",
        "title_pl": "Wdrożenie Fabryczne i Zautomatyzowane Potoki Dotrenowania",
        "summary_en": "Architect an end-to-end industrial MLOps loop: stream edge telemetry, trigger drift alerts, and automate retraining on false alarms.",
        "summary_pl": "Zaprojektuj pełną pętlę przemysłowego MLOps: zbieraj telemetrię, wyłapuj dryf i automatycznie dotrenowuj model na fałszywych alarmach.",
        "visual_widget": "drift_latency_sandbox",
        "colab_notebook": "m07_l04_mlops_pipeline.ipynb",
        "estimated_minutes": 25,
        "checklist": [
            {"id": "chk-m7-4-1", "textEn": "Design edge telemetry ingestion queue buffer using MQTT/Kafka", "textPl": "Zaprojektuj kolejkę buforującą odczyty maszyn w oparciu o MQTT/Kafka"},
            {"id": "chk-m7-4-2", "textEn": "Build human-in-the-loop operator feedback interface for false alarms", "textPl": "Stwórz panel operatora do weryfikacji i oznaczania fałszywych alarmów"},
            {"id": "chk-m7-4-3", "textEn": "Automate scheduled weekly retraining and model registry deployment", "textPl": "Zautomatyzuj cotygodniowe dotrenowanie i rejestrację nowego modelu"}
        ],
        "sections": [
            {
                "id": "b1",
                "type": "paragraph",
                "titleEn": "Closing the MLOps Loop on the Shop Floor",
                "titlePl": "Domknięcie Pętli MLOps na Hali Fabrycznej",
                "en": "A successful industrial AI system is not a static Python script—it is a continuous operational lifecycle. By deploying {{term:model_monitoring}}, production telemetry is continuously validated. When the line quality supervisor marks a false alarm, that verified edge sample is queued into the {{term:pipeline_retraining}} workflow, ensuring the model adapts gracefully to mechanical tool wear over the lifespan of the manufacturing line.",
                "pl": "Skuteczny przemysłowy system AI to nie statyczny skrypt w Pythonie, lecz ciągły cykl życia. Wdrażając {{term:model_monitoring}}, nieustannie weryfikujemy telemetrię z hali. Gdy brygadzista jakości zweryfikuje fałszywy alarm, ten sprawdzony przykład trafia do kolejki w {{term:pipeline_retraining}}, dzięki czemu model samoczynnie adaptuje się do naturalnego zużywania się maszyn."
            }
        ],
        "quiz": [
            {
                "id": "q-m7-4-1",
                "questionEn": "Why is 'Human-in-the-Loop' operator feedback essential for automated retraining pipelines in manufacturing?",
                "questionPl": "Dlaczego pętla zwrotna od operatora (Human-in-the-Loop) jest kluczowa w potokach dotrenowania modeli w fabrykach?",
                "optionsEn": [
                    "Operators write the C++ code for the PLC drivers",
                    "Plant technicians provide the ground-truth verification on whether flagged anomalies were genuine breakdowns or harmless false alarms",
                    "Without humans, computers cannot run cron jobs",
                    "To slow down the manufacturing line"
                ],
                "optionsPl": [
                    "Operatorzy piszą kod sterowników PLC w języku C++",
                    "Technicy na linii dostarczają bezspornej prawdy referencyjnej: czy zaalarmowany detal był rzeczywistą wadą, czy nieszkodliwym błędem czujnika",
                    "Bez człowieka serwer nie potrafi uruchomić zaplanowanego zadania w cronie",
                    "Aby celowo spowolnić tempo pracy taśmociągu"
                ],
                "correctIndex": 1,
                "explanationEn": "Automating retraining without human validation causes the model to learn its own errors (feedback loop collapse). Operator confirmation provides the verified ground truth.",
                "explanationPl": "Dotrenowywanie bez ludzkiej weryfikacji prowadzi do utrwalania własnych błędów modelu. Potwierdzenie technika daje wiarygodny punkt odniesienia (ground truth)."
            }
        ]
    }
]

MODULE_META = {
    1: {
        "id": "mod-1",
        "titleEn": "Industrial Data Ingestion & High-Speed Processing",
        "titlePl": "Akwizycja Danych Przemysłowych i Szybkie Przetwarzanie",
        "descriptionEn": "Master 4-20mA current loop telemetry with vectorized NumPy, high-speed log analytics with Pandas 2.x & Polars, Parquet archives with DuckDB, and Hampel spike removal.",
        "descriptionPl": "Opanuj pętle prądowe 4-20mA z wektoryzacją NumPy, analizę logów w Pandas 2.x i Polars, archiwa Parquet z DuckDB oraz usuwanie szpilek filtrem Hampela.",
        "sandboxType": "signal_filter_sandbox"
    },
    2: {
        "id": "mod-2",
        "titleEn": "Exploratory Data Analysis & Robust Feature Engineering",
        "titlePl": "Eksploracyjna Analiza Danych i Odporna Inżynieria Cech",
        "descriptionEn": "Perform multi-zone oven EDA, engineer temporal lag variables, compare RobustScaler vs StandardScaler on motor spikes, and plot interactive telemetry.",
        "descriptionPl": "Wykonuj analizę EDA pieców, twórz zmienne opóźnione w czasie, porównuj RobustScaler z StandardScaler na pikach i twórz interaktywne wykresy.",
        "sandboxType": "scaling_outlier_sandbox"
    },
    3: {
        "id": "mod-3",
        "titleEn": "Supervised Learning & Cost-Sensitive Optimization",
        "titlePl": "Uczenie Nadzorowane i Optymalizacja Kosztowa",
        "descriptionEn": "Forecast power with regularized regression, export decision trees to PLC ladder logic, train Random Forests & XGBoost, and optimize cost matrices with Optuna.",
        "descriptionPl": "Prognozuj energię z regularyzacją, eksportuj drzewa do logiki PLC, trenuj Lasy Losowe i XGBoost oraz minimalizuj straty finansowe z Optuna.",
        "sandboxType": "cost_matrix_sandbox"
    },
    4: {
        "id": "mod-4",
        "titleEn": "Unsupervised Diagnostics, Clustering & Capstone 1",
        "titlePl": "Diagnostyka Nienadzorowana, Klastrowanie i Projekt Zwieńczeniowy 1",
        "descriptionEn": "Discover machine operating regimes with K-Means & DBSCAN, score zero-shot anomalies with Isolation Forests, compress 50+ PLC tags with PCA & UMAP, and build Capstone 1.",
        "descriptionPl": "Odkrywaj stany pracy z K-Means i DBSCAN, wykrywaj anomalie bez etykiet z Lasem Izolacyjnym, redukuj wymiary z PCA/UMAP i zbuduj Capstone 1.",
        "sandboxType": "clustering_sandbox"
    },
    5: {
        "id": "mod-5",
        "titleEn": "Frequency Domain & Predictive Maintenance",
        "titlePl": "Analiza Częstotliwościowa i Predykcyjne Utrzymanie Ruchu",
        "descriptionEn": "Transform raw vibration waveforms into spectral signatures using FFT and STFT spectrograms, identify bearing fault frequencies (BPFO/BPFI), and estimate Remaining Useful Life (RUL).",
        "descriptionPl": "Przekształcaj drgania w widmo częstotliwości za pomocą FFT i spektrogramów, wykrywaj uszkodzenia bieżni łożysk (BPFO/BPFI) i szacuj czas do awarii (RUL).",
        "sandboxType": "fft_anomaly_sandbox"
    },
    6: {
        "id": "mod-6",
        "titleEn": "Edge Vision & Surface Quality Inspection",
        "titlePl": "Wizja Komputerowa na Brzegu i Kontrola Powierzchni",
        "descriptionEn": "Deploy automated optical inspection: predict bounding boxes for surface scratches and voids, calculate Intersection over Union (IoU), and fine-tune lightweight CNNs.",
        "descriptionPl": "Wdrażaj automatyczną inspekcję optyczną: lokalizuj rysy i wtrącenia ramkami bounding box, obliczaj metrykę IoU i trenuj lekkie sieci splotowe.",
        "sandboxType": "cnn_iou_sandbox"
    },
    7: {
        "id": "mod-7",
        "titleEn": "MLOps, Concept Drift & Factory Deployment",
        "titlePl": "MLOps, Dryf Modeli i Wdrożenia Fabryczne",
        "descriptionEn": "Monitor production model health against concept and data drift (Kolmogorov-Smirnov tests), optimize inference with INT8 quantization & TensorRT, and automate retraining pipelines.",
        "descriptionPl": "Monitoruj stan modeli produkcyjnych pod kątem dryfu (test Kołmogorowa-Smirnowa), optymalizuj wnioskowanie z INT8 i TensorRT oraz automatyzuj potoki dotrenowania.",
        "sandboxType": "drift_latency_sandbox"
    }
}

def main():
    LESSONS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Clear out any old lesson files in LESSONS_DIR
    for existing_file in LESSONS_DIR.glob("*.json"):
        existing_file.unlink()

    modules_dict = {m: [] for m in range(1, 8)}

    # 2. Normalize and write individual lesson JSON files
    for lesson in LESSONS_DATA:
        m_num = lesson["module_number"]

        # Ensure all required snake_case and camelCase fields exist
        title_en = lesson.get("title_en") or lesson.get("titleEn")
        title_pl = lesson.get("title_pl") or lesson.get("titlePl")
        summary_en = lesson.get("summary_en") or lesson.get("summaryEn") or ""
        summary_pl = lesson.get("summary_pl") or lesson.get("summaryPl") or ""
        visual_widget = lesson.get("visual_widget") or lesson.get("sandboxType") or "signal_filter_sandbox"
        colab_notebook = lesson.get("colab_notebook") or lesson.get("notebook") or f"{lesson['id']}.ipynb"
        sections = lesson.get("sections") or lesson.get("contentBlocks") or []
        est_min = lesson.get("estimated_minutes") or lesson.get("estimatedMinutes") or 25

        lesson["title_en"] = title_en
        lesson["titleEn"] = title_en
        lesson["title_pl"] = title_pl
        lesson["titlePl"] = title_pl
        lesson["summary_en"] = summary_en
        lesson["summaryEn"] = summary_en
        lesson["summary_pl"] = summary_pl
        lesson["summaryPl"] = summary_pl
        lesson["visual_widget"] = visual_widget
        lesson["sandboxType"] = visual_widget
        lesson["colab_notebook"] = colab_notebook
        lesson["notebook"] = colab_notebook
        lesson["sections"] = sections
        lesson["contentBlocks"] = sections
        lesson["estimated_minutes"] = est_min
        lesson["estimatedMinutes"] = est_min

        modules_dict[m_num].append(lesson)

        # Write to src/data/lessons/{id}.json
        file_path = LESSONS_DIR / f"{lesson['id']}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(lesson, f, indent=2, ensure_ascii=False)
        print(f"  [✓] Wrote {file_path.name}")

    # 3. Assemble syllabus.json with dual-compatible naming
    syllabus = []
    for m_num in range(1, 8):
        meta = MODULE_META[m_num]
        mod_lessons = []
        for l in modules_dict[m_num]:
            mod_lessons.append(dict(l))

        mod_entry = {
            "id": meta["id"],
            "number": m_num,
            "titleEn": meta["titleEn"],
            "titlePl": meta["titlePl"],
            "descriptionEn": meta["descriptionEn"],
            "descriptionPl": meta["descriptionPl"],
            "sandboxType": meta["sandboxType"],
            "lessons": mod_lessons
        }
        syllabus.append(mod_entry)

    with open(SYLLABUS_FILE, "w", encoding="utf-8") as f:
        json.dump(syllabus, f, indent=2, ensure_ascii=False)

    print(f"\nSuccessfully generated {len(LESSONS_DATA)} lessons in {LESSONS_DIR} and updated {SYLLABUS_FILE}")

if __name__ == "__main__":
    main()
