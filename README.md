# CyberX: Synthetic Auditor

> **Track I Challenge A: "The Synthetic Auditor"** > *Israel-India Global Innovators Students Hackathon 2026*

## Overview
CyberX Synthetic Auditor is a "Strictly Offline" automated reporting tool. It ingests raw network scan data (XML/JSON), analyzes vulnerabilities using a **Local Large Language Model (Ollama)**, and generates professional, context-aware PDF audit reports. 

[cite_start]This tool solves the "Private AI" challenge by ensuring no sensitive vulnerability data ever leaves the local machine[cite: 27].

## Features
* [cite_start]**Zero-Cloud Dependency:** Runs entirely on local CPU/GPU[cite: 49].
* [cite_start]**Context-Aware Analysis:** Unlike standard scanners, it analyzes risks based on the specific business context (e.g., "Financial Bank" vs "University Lab")[cite: 38].
* [cite_start]**Automated Reporting:** Converts technical logs into Executive Summaries and Technical Scoring tables[cite: 39].

## Project Structure
```text
CyberX-Synthetic-Auditor/
├── app.py                  # Main Flask Application
├── core/                   # Logic Modules
│   ├── brain.py            # Local AI Interface (Ollama)
│   ├── ingestor.py         # XML/JSON Parser
│   └── reporter.py         # PDF Generator
├── data/                   # Input/Output directory
└── templates/              # Web Interface