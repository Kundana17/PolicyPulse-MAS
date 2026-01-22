# 🧬 PolicyPulse: Civic Intelligence MAS

PolicyPulse is a **Multi-Agent System (MAS)** designed to bridge the gap between **government policy intent** and **real-world impact**. By utilizing a **vector-database-driven memory** and **LLM-powered reasoning**, the system analyzes whether policies are *drifting* from their original goals.

---

## 🤖 Agentic Architecture

The system operates through three specialized agents:

### 📚 Archivist Agent (Retrieval)
- Uses **Qdrant** and **all-MiniLM-L6-v2**
- Performs semantic searches across **1,100+ policy records**
- Retrieves the most relevant legislation for a user's query
- Regional Fallback capability - if a state policy is missing, it intelligently pulls national or cross-regional data.

### 🔍 Auditor Agent (Analysis)
- Cross-references policy text with **live field impact data** from **data.gov.in**
- Computes a **Drift Score** to evaluate whether a policy is meeting its intended outcomes
- Classifies drift into None (In Sync), Low, or High categories


### 🧠 Strategist Agent (Reasoning)
- Powered by **Llama-3.3-70B**
- Synthesizes findings into **actionable governance insights**
- Extracts **cross-jurisdictional lessons** for policymakers

---

## 🧩 Qdrant Usage

PolicyPulse uses **Qdrant as the primary vector search engine** for long-term policy memory.

- **Embeddings:** Policy intent and impact records are embedded using `all-MiniLM-L6-v2`
- **Metadata:** Vectors are stored in a local Qdrant collection with metadata:
  - sector, state, year, scope
- **Operations:** All agent retrieval and comparison operations are performed using Qdrant. No in-memory or short-term vector storage is used
- Qdrant serves as the system’s long-term policy memory across all queries


---

## 📂 Project Structure

```plaintext
backend/
├── api.py                 # FastAPI Server & Agent Orchestrator
├── pipeline.py            # Unified Data Ingestion (1,100+ Records)
├── drift_detector.py      # Auditor Agent Logic
├── recommender.py         # Archivist Agent Logic
├── qdrant_client_local.py # Vector Database Configuration-
├── feedback_logs.json     # Manual User Feedback Store
├── data.py                # Static Policy Datasets
└── requirements.txt       # System Dependencies
```

---

## ⚡ Quick Start

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file and add your API key:
```env
GROQ_API_KEY=your_api_key_here
```

Initialize the vector database:
```bash
python pipeline.py
```

Start the backend server:
```bash
uvicorn api:app --reload --port 8000
```

---

### 2. Frontend Setup

Navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Run the application:
```bash
npm run dev
```

Access the UI in your browser:
```
http://localhost:5173 or http://localhost:5174
```

## 🔐 API Notes

- LLM-based reasoning uses Groq (Llama-3.3-70B) when an API key is provided
- If the API key is unavailable, the system falls back to deterministic logic
- Core policy retrieval and drift detection do not depend on external APIs

### Data Ingestion Note

- `pipeline.py` always ingests bundled static policy data
- Live data from data.gov.in is optional and requires an API key
- If no API key is provided, the pipeline skips live ingestion and completes successfully

---
## 🔁 Reproducibility

This project is fully reproducible and runs end-to-end locally.

- No cloud deployment is required
- Qdrant runs locally
- Sample policies are ingested automatically via `pipeline.py`
- The system produces drift scores and agent outputs without manual intervention

Anyone can clone this repository, follow the setup steps, and reproduce the results shown in the report.

---

## 🛠️ Key Features

- **Semantic Fallback**  
  If a specific state policy is not found, the Archivist Agent provides a fallback match from another region to ensure the user still receives relevant information.

- **Live Data Sync**  
  The pipeline fetches real-time indicators from the **Government of India's Open Data Platform**.

- **Human-in-the-Loop**  
  Users can submit feedback for missing policies, which are logged in `feedback_logs.json` for administrative review and future database expansion.

---

## 📌 Metadata

**PolicyPulse | MAS-PP-2026**  
Built for **Convolve 4.0**