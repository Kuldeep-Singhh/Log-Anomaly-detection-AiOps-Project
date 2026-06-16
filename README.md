# Log-Anomaly-detection-AiOps-Project

An intelligent DevOps observability tool that applies unsupervised machine learning and statistical profiling to automate server log analysis. This application ingests uploaded log files, isolates anomalous execution patterns, flags silent performance bottlenecks, and maps detected issues directly to troubleshooting runbook insights.

---

## 📌 Project Overview

In enterprise production environments, systems generate millions of lines of unstructured log data daily. Traditional log management relies heavily on manual keyword searches (`Ctrl+F` or basic grep rules) which fail to catch complex, non-linear error patterns. Furthermore, rule-based systems completely miss **silent performance degradation**—incidents where an application server continues to return a successful `200 OK` status code but takes an unacceptable amount of time to respond due to resource deadlocks or thread contention.

This project implements an offline, self-contained analytics engine that bridges the gap between raw data science and systems operations. By parsing unstructured text streams into structured tables, the system isolates system anomalies without requiring pre-labeled training datasets or active external cloud connections.

---

## 🚀 Core Features

* **File Ingestion Layer:** Features an interactive drag-and-drop file uploader supporting standard `.log`, `.txt`, and `.csv` server log formats.
* **Flexible Regex-Driven Parsing:** Automatically structures raw log strings into organized, tokenized metrics (Timestamps, Log Levels, Messages, Status Codes, and Latencies).
* **Unsupervised Text Clustering:** Converts unstructured log messages into high-dimensional numerical matrices using **TF-IDF Vectorization** and applies **K-Means Clustering (`n_clusters=2`)**. The pipeline programmatically isolates the lower-cardinality cluster as the abnormal text signature group.
* **Statistical Performance Profiling (3-Sigma Rule):** Implements a Gaussian distribution boundary calculation ($\mu \pm 3\sigma$) on server response times. Any log line passing this dynamic threshold is flagged as a statistical latency outlier, capturing silent application hang-ups regardless of textual error keywords.
* **Interactive Operational Runbook Viewer:** Displays a filtered dashboard table featuring ONLY the isolated anomalies. Selecting a flagged row dynamically renders targeted troubleshooting insights and mitigation steps directly below the interface.

---

## 🛠️ Tech Stack

* **Programming Language:** Python
* **Dashboard Interface:** Streamlit
* **Machine Learning Pipelines:** Scikit-Learn (TF-IDF, K-Means Clustering)
* **Mathematical Operations:** NumPy
* **Data Processing & Analytics:** Pandas

---

## ⚙️ Local Installation & Setup

Follow these steps to spin up the environment and run the application locally on your machine.

### 1. Initialize an Isolated Virtual Environment
Create a localized environment instance to lock dependencies and prevent system-level interpreter conflicts:
```bash
python -m venv env
```
### 2. Activate the Environment
--On Windows:
```bash
.\env\Scripts\activate
```
--On macOS/Linux:
```Bash
source env/bin/activate
```
### 3. Install Dependencies
Compile the required core computational and visualization libraries inside your active environment container:
```Bash
pip install streamlit pandas numpy scikit-learn
```
### 4. Launch the Dashboard
Run the Streamlit server to boot the application interface automatically inside your default web browser:
```Bash
streamlit run app.py
```
---
