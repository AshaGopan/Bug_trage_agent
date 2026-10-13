# 🤖 Multi-Modal Bug-Report Triage & Routing Agent

An end-to-end, leakage-free AI system for automated bug triage, duplicate detection, diagnostic auditing, and maintainer comment drafting on `kubernetes/kubernetes`.

Combines **Dense Text Embeddings**, **Inductive Graph Neural Networks (GraphSAGE)**, and **Temporal Label Awareness** inside an orchestrating **LangGraph** workflow with a **FastAPI** backend and **Streamlit** maintainer dashboard.

---

## 🌟 Key Highlights

- **Leakage-Free Chronological Splitting**: Enforces strict temporal ordering ($\max(\text{train}) \le \min(\text{val}) \le \min(\text{test})$) across all splits and neighbor aggregations.
- **Multi-Modal Feature Fusion**:
  - Semantic text representation via `all-MiniLM-L6-v2` (384 dimensions).
  - Inductive structural representation via 2-layer GraphSAGE GNN (128 dimensions).
  - Historical training-neighbor empirical label distribution (7 dimensions).
- **Cold-Start Inductive Graph Embedding**: Handles unlinked new bug reports by dynamically linking them to their $K=5$ nearest ChromaDB semantic neighbors to compute GraphSAGE representations at inference time.
- **LangGraph Agentic State Machine**:
  - `intake_node` $\to$ `missing_info_node` $\to$ `cold_start_node` $\to$ `classifier_node` $\to$ Conditional Branch ($\ge 60\%$ confidence) $\to$ `writer_high_node` / `writer_low_node`.
- **Maintainer-in-the-Loop Workspace**: Interactive Streamlit UI connected to a production-ready FastAPI REST service.

---

## 📁 Repository Structure

```
bug-triage-agent/
├── agents/                     # LangGraph Agentic Pipeline
│   ├── graph.py                # StateGraph workflow definition & runner
│   ├── nodes.py                # Individual agent processing nodes
│   ├── prompts.py              # System prompts for diagnostic audit & drafting
│   └── state.py                # TypedDict TriageState schema
├── backend/                    # REST API Serving Layer (FastAPI)
│   ├── main.py                 # FastAPI application endpoints
│   └── schemas.py              # Pydantic request/response schemas
├── frontend/                   # Maintainer Frontend (Streamlit)
│   └── streamlit_app.py        # Streamlit interactive triage dashboard
├── collect/                    # GitHub Data Collection & Label Verification
│   ├── fetch_github_data.py    # GitHub search pagination & issue caching
│   └── verify_labels.py        # Label frequency & threshold validation
├── data/                       # Data storage
│   ├── cache/                  # Cached raw GitHub API JSON responses
│   ├── chroma_db/              # ChromaDB vector index
│   ├── processed/              # SQLite database (triage.db)
│   └── raw/                    # Raw JSONL issue dump
├── docs/                       # Project Documentation
│   └── architecture.md         # Detailed system design & architecture
├── eval/                       # Benchmarks & Evaluations
│   ├── confusion_matrix.txt    # Confusion matrix on test split
│   ├── evaluate_retrieval.py   # Recall@5 duplicate retrieval benchmark
│   └── results_comparison.csv  # Model performance comparison
├── features/                   # Feature Engineering & Preprocessing
│   ├── build_graph.py          # SQLite ingestion & temporal train/val/test split
│   ├── clean_text.py           # Markdown & template boilerplate cleaning
│   ├── db.py                   # SQLite database connection & schema
│   ├── embed_graph.py          # PyTorch Geometric GraphSAGE model & training
│   ├── embed_text.py           # SentenceTransformers embedding generation
│   ├── label_awareness.py      # Training-neighbor label distribution computation
│   └── vector_store.py         # ChromaDB indexing & querying
├── models/                     # Machine Learning Models
│   ├── baseline_tfidf.py       # TF-IDF + Logistic Regression & LinearSVC
│   ├── saved/                  # Serialized PyTorch & LightGBM model weights
│   │   ├── graphsage.pt        # GraphSAGE weights
│   │   └── hybrid_model.joblib # LightGBM hybrid model
│   └── train_hybrid.py         # LightGBM multi-modal model training
├── tests/                      # Automated Test Suite
│   ├── test_leakage.py         # Chronological split & label leakage verification
│   └── verify_cpu.py           # CPU PyTorch execution check
└── requirements.txt            # Python dependencies
```

---

## 🚀 Quick Start

### 1. Prerequisites & Environment Setup

Create and activate a virtual environment, then install dependencies:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```
*(Optionally provide `GITHUB_TOKEN` for fetching new GitHub issues and `GEMINI_API_KEY` or `HF_TOKEN` for LLM drafting.)*

---

### 2. Running Tests

Run the test suite to ensure zero data leakage and temporal split validity:

```bash
pytest tests/ -v
```

---

### 3. Launching the Services

#### Start the FastAPI Backend:
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
API docs will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

#### Start the Streamlit Dashboard:
In a separate terminal:
```bash
streamlit run frontend/streamlit_app.py
```
Open your browser at [http://localhost:8501](http://localhost:8501).

---

### 4. Running the Agent Directly (CLI)

You can run the LangGraph triage pipeline directly from the command line:

```bash
python agents/graph.py
```

---

## 📊 Benchmark Results

| Model | Modality | Test Macro-F1 |
| :--- | :--- | :---: |
| TF-IDF + Logistic Regression | Text (BoW) | 0.7020 |
| TF-IDF + LinearSVC | Text (BoW) | 0.7645 |
| LightGBM (Text-Only) | Dense MiniLM-L6-v2 (384d) | 0.6247 |
| LightGBM (Graph-Only) | GraphSAGE Structural (128d) | 0.7399 |
| LightGBM (Hybrid) | Text (384d) + Graph (128d) | 0.7485 |
| **Hybrid + Label Awareness** | **Text (384d) + Graph (128d) + Label Dist (7d)** | **0.7485** |

For complete architectural details, see [docs/architecture.md](docs/architecture.md).
