# 📊 Real-Time Event Analytics Pipeline (Bronze → Silver → Gold)

A **real-time streaming data engineering project** built with **PySpark Structured Streaming**, following the **Medallion Architecture** (Bronze / Silver / Gold).

The pipeline simulates user behavior events, ingests them in real time, cleans and deduplicates them, and produces **business-ready analytical datasets**.

This project is designed to be:
- ✅ Replayable
- ✅ Fault-tolerant
- ✅ Streaming-first
- ✅ Portfolio / interview ready

---

## 🗂️ Project Structure

```
portfolio-project-2/
│
├── src/
│   ├── bronze/
│   │   └── bronze_ingestion.py
│   ├── silver/
│   │   └── silver_transformation.py
│   ├── gold/
│   │   ├── gold_events_per_minute.py
│   │   ├── gold_revenue_per_window.py
│   │   ├── gold_active_users_per_window.py
│   │   └── gold_most_purchases_per_device.py
│   ├── common/
│   │   ├── schema.py
│   │   └── spark_session.py
│   └── utils/
│       └── read_gold.py
│
├── generate_events.py
├── data/                  # ignored by git
│   ├── inbox/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── .gitignore
├── README.md
└── .venv/
```

---

## ⚙️ Requirements

- Python **3.10+**
- Java **11** (required — Java 17 will break Spark)
- PySpark **3.4.x**

Check Java version:
```bash
java -version
```

---

## 🧪 Event Generator

### `generate_events.py`

Simulates real-time user activity by continuously writing JSON files.

**Generated fields**
- `event_id`
- `user_id`
- `event_time`
- `event_type`
- `device_type`
- `event_value` (only for purchases)

Run:
```bash
python generate_events.py
```

Output:
```
data/inbox/
```

---

## 🥉 Bronze Layer – Streaming Ingestion

### `bronze_ingestion.py`

**Purpose**
- Read JSON files as a stream
- Enforce schema
- Persist raw events in Parquet
- Track processed files using checkpoints

Run:
```bash
python src/bronze/bronze_ingestion.py
```

Output:
```
data/bronze/events/
```

---

## 🥈 Silver Layer – Cleaning & Deduplication

### `silver_transformation.py`

**Purpose**
- Read Bronze Parquet as a stream
- Deduplicate events by `event_id`
- Apply event-time watermark
- Produce trusted, clean data

Run:
```bash
python src/silver/silver_transformation.py
```

Output:
```
data/silver/events/
```

---

## 🥇 Gold Layer – Business Metrics

Each Gold pipeline is **independent**, **streaming**, and writes to its own folder.

---

### ⏱ Events per Minute

Counts total events per minute.

Run:
```bash
python src/gold/gold_events_per_minute.py
```

Output:
```
data/gold/events_per_minute/
```

```
=== Events per minute example===
+-------------------+-------------------+-----------+
|minute_start       |minute_end         |event_count|
+-------------------+-------------------+-----------+
|2026-02-02 17:35:00|2026-02-02 17:36:00|221        |
|2026-02-02 17:45:00|2026-02-02 17:46:00|213        |
|2026-02-02 17:29:00|2026-02-02 17:30:00|175        |
|2026-02-02 17:42:00|2026-02-02 17:43:00|184        |
|2026-02-02 17:33:00|2026-02-02 17:34:00|177        |
|2026-02-02 17:43:00|2026-02-02 17:44:00|187        |
|2026-02-02 17:32:00|2026-02-02 17:33:00|190        |
|2026-02-02 17:36:00|2026-02-02 17:37:00|179        |
|2026-02-02 17:34:00|2026-02-02 17:35:00|189        |
|2026-02-02 17:37:00|2026-02-02 17:38:00|185        |
|2026-02-02 17:41:00|2026-02-02 17:42:00|178        |
|2026-02-02 17:28:00|2026-02-02 17:29:00|175        |
|2026-02-02 17:44:00|2026-02-02 17:45:00|194        |
|2026-02-02 17:38:00|2026-02-02 17:39:00|181        |
|2026-02-02 17:40:00|2026-02-02 17:41:00|196        |
|2026-02-02 17:46:00|2026-02-02 17:47:00|182        |
|2026-02-02 17:31:00|2026-02-02 17:32:00|186        |
|2026-02-02 17:47:00|2026-02-02 17:48:00|189        |
|2026-02-02 17:30:00|2026-02-02 17:31:00|167        |
|2026-02-02 17:39:00|2026-02-02 17:40:00|169        |
+-------------------+-------------------+-----------+
```
---

### 💳 Revenue per Time Window

Sums purchase revenue per window.

Run:
```bash
python src/gold/gold_revenue_per_window.py
```

Output:
```
data/gold/revenue_per_hour/
```
```
=== Revenue per window example ===
+-------------------+-------------------+-------+
|minute_start       |minute_end         |revenue|
+-------------------+-------------------+-------+
|2026-02-02 17:30:00|2026-02-02 17:35:00|2968.70|
|2026-02-02 17:25:00|2026-02-02 17:30:00|2171.68|
|2026-02-02 17:35:00|2026-02-02 17:40:00|3386.45|
|2026-02-02 17:40:00|2026-02-02 17:45:00|3454.81|
+-------------------+-------------------+-------+
```
---

### 👥 Active Users per Time Window

Counts approximate distinct users per window using a streaming-safe aggregation.

Run:
```bash
python src/gold/gold_active_users_per_window.py
```

Output:
```
data/gold/active_users_per_hour/
```
```
=== Active users per window example ===
+-------------------+-------------------+------------+                          
|minute_start       |minute_end         |active_users|
+-------------------+-------------------+------------+
|2026-02-02 17:30:00|2026-02-02 17:35:00|857         |
|2026-02-02 17:25:00|2026-02-02 17:30:00|679         |
|2026-02-02 17:35:00|2026-02-02 17:40:00|884         |
|2026-02-02 17:40:00|2026-02-02 17:45:00|932         |
+-------------------+-------------------+------------+
```
---

### 📱 Purchases per Device

Aggregates revenue and purchase count by device type per window.

Run:
```bash
python src/gold/gold_most_purchases_per_device.py
```

Output:
```
data/gold/most_purchases_per_device/
```
```
=== Most purchases per device example ===
+-------------------+-------------------+-----------+------------------+--------------+
|minute_start       |minute_end         |device_type|revenue_per_device|purchase_count|
+-------------------+-------------------+-----------+------------------+--------------+
|2026-02-02 17:30:00|2026-02-02 17:35:00|desktop    |897.09            |19            |
|2026-02-02 17:35:00|2026-02-02 17:40:00|desktop    |684.24            |14            |
|2026-02-02 17:25:00|2026-02-02 17:30:00|desktop    |677.17            |14            |
|2026-02-02 17:25:00|2026-02-02 17:30:00|tablet     |473.78            |7             |
|2026-02-02 17:25:00|2026-02-02 17:30:00|laptop     |621.00            |11            |
|2026-02-02 17:40:00|2026-02-02 17:45:00|laptop     |1056.05           |17            |
|2026-02-02 17:30:00|2026-02-02 17:35:00|laptop     |918.41            |14            |
|2026-02-02 17:30:00|2026-02-02 17:35:00|mobile     |574.59            |13            |
|2026-02-02 17:30:00|2026-02-02 17:35:00|tablet     |578.61            |12            |
|2026-02-02 17:40:00|2026-02-02 17:45:00|tablet     |789.85            |20            |
|2026-02-02 17:40:00|2026-02-02 17:45:00|mobile     |494.06            |12            |
|2026-02-02 17:35:00|2026-02-02 17:40:00|tablet     |906.60            |19            |
|2026-02-02 17:35:00|2026-02-02 17:40:00|laptop     |880.17            |17            |
|2026-02-02 17:35:00|2026-02-02 17:40:00|mobile     |915.44            |15            |
|2026-02-02 17:25:00|2026-02-02 17:30:00|mobile     |399.73            |9             |
|2026-02-02 17:40:00|2026-02-02 17:45:00|desktop    |1114.85           |19            |
+-------------------+-------------------+-----------+------------------+--------------+
```
---

## ▶️ Recommended Run Order (Demo Mode)

Open **multiple terminals**:

```bash
# 1️⃣ Generate events
python generate_events.py

# 2️⃣ Bronze ingestion
python src/bronze/bronze_ingestion.py

# 3️⃣ Silver transformation
python src/silver/silver_transformation.py

# 4️⃣ Gold pipelines (each in its own terminal)
python src/gold/gold_events_per_minute.py
python src/gold/gold_revenue_per_window.py
python src/gold/gold_active_users_per_window.py
python src/gold/gold_most_purchases_per_device.py
```

Let everything run for **10–15 minutes**.

---

## 📊 Reading Final Results

### `read_gold.py`

Reads all Gold datasets and prints them.

Run:
```bash
python src/utils/read_gold.py
```

Example output:
```
=== Active users per hour ===
| minute_start | minute_end | active_users |

=== Revenue per hour ===
| minute_start | minute_end | revenue |

=== Most purchases per device ===
| device_type | revenue_per_device | purchase_count |

=== Events per minute ===
| minute_start | minute_end | event_count |
```

---

## 🧠 Key Concepts Demonstrated

- PySpark Structured Streaming
- Event-time processing
- Watermarks
- Deduplication
- Checkpointing
- Streaming aggregations
- Approximate distinct counting
- Medallion Architecture
- Production-grade folder layout

---

## 🚀 Why This Project Matters

This is **not a toy project**.

The same design works with:
- Kafka instead of JSON
- S3 instead of local storage
- Airflow instead of manual execution

It demonstrates **real-world data engineering patterns** used in production streaming systems.

---

## 👤 Author

Built as a **Data Engineering project** to showcase real-time analytics using PySpark Structured Streaming.