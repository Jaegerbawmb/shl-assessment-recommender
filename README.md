# SHL Assessment Recommender


An AI-powered assessment recommendation system for SHL — built to surface the most relevant assessments from SHL's product catalog given any query, job description, or hiring requirement.

---

## Overview

This project uses semantic search and fast vector retrieval to match hiring queries with the right SHL assessments. It exposes a clean REST API and includes a Streamlit UI for interactive exploration.

**Stack:** FastAPI · FAISS · Sentence Transformers · Streamlit · scikit-learn

---

## Features

| Feature | Description |
|---|---|
| **Semantic Search** | Uses `all-MiniLM-L6-v2` embeddings to capture contextual meaning beyond keyword matching |
| **FAISS Indexing** | Fast, scalable similarity search across assessment metadata |
| **TF-IDF Fallback** | Backup retrieval engine when embeddings are unavailable |
| **Re-ranking & Balancing** | Prioritizes diverse test types (Knowledge, Personality, Simulation, etc.) |
| **REST API** | Clean `/recommend` endpoint returning structured JSON |
| **Streamlit UI** | Interactive front-end for querying and demonstration |

---

## Project Structure

```
shl-assessment-recommender/
│
├── app/
│   ├── main.py             # FastAPI backend (API endpoint)
│   ├── schemas.py          # Request/response models
│   └── balancer.py         # Balances assessment types in results
│
├── scripts/
│   ├── crawl_catalog.py    # Crawls SHL catalog pages
│   ├── build_index.py      # Builds FAISS index and metadata
│   ├── query_recommender.py # CLI for testing the recommender
│   └── fetch_details.py    # Fetches detailed assessment info
│
├── models/
│   ├── embed_index.py      # Embedding & FAISS retrieval
│   └── tfidf_fallback.py   # TF-IDF retrieval backup
│
├── utils/
│   ├── text.py             # Text cleaning helpers
│   ├── jd_extract.py       # Job description extraction
│   └── taxonomy.py         # Taxonomy/tag mapping
│
├── ui/
│   └── app.py              # Streamlit front-end app
│
├── data/
│   ├── catalog_full.json   # Crawled catalog data
│   ├── index.faiss         # FAISS vector index
│   ├── meta.parquet        # Metadata for FAISS
│   ├── test_dataset.xlsx   # Unlabeled test queries
│   └── submission_results.csv
│
├── test_api.py             # Automated API testing
└── README.md
```

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/shl-assessment-recommender.git
cd shl-assessment-recommender
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI Server

```bash
uvicorn app.main:app --reload
```

API available at: `http://127.0.0.1:8000/recommend`

### 5. Run the Streamlit UI

```bash
streamlit run ui/app.py
```

---

## API Reference

### `POST /recommend`

Returns a ranked list of SHL assessments matching the query.

**Request**

```json
{
  "query": "Looking to hire a Java developer for backend applications",
  "k": 5
}
```

**Response**

```json
{
  "recommended_assessments": [
    {
      "name": "Java Developer Test",
      "url": "https://www.shl.com/products/java-developer-test/",
      "description": "Multiple-choice test assessing Java knowledge...",
      "duration": 30,
      "remote_support": "Yes",
      "test_type": ["Knowledge & Skills", "Aptitude"]
    }
  ]
}
```

---

## Deliverables

- **Web App** — Interactive Streamlit interface for user queries
- **API Endpoint** — `POST /recommend` returning JSON recommendations
- **Report** — `Approach_and_Optimization.pdf` (2-page technical write-up)
- **Results** — `submission_results.csv` and `submission_results_final.csv`

---

## Notes & Future Work

- Recommendation quality can be improved by enriching catalog metadata or fine-tuning embedding reranking.
- Potential future additions:
  - Multilingual query support
  - Adaptive scoring based on role seniority
  - LLM-based reranking for better domain adaptability
