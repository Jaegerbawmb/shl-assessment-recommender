
# SHL Assessment Recommendation Engine — Approach & Results

## 1) Problem & Goal
Build a system that recommends **5–10 relevant SHL *Individual Test Solutions*** for a given query/JD, excluding *Pre‑packaged Job Solutions*. Output must include **assessment name + catalog URL**. We evaluate by **Mean Recall@10** and ensure **balanced recommendations** (e.g., mix of **K**: Knowledge & Skills and **P**: Personality & Behavior where relevant).

## 2) Data Pipeline
**a. Crawl Catalog**
- Source: SHL Product Catalog (Individual Test Solutions list + pagination).
- Parse for each assessment: **name, URL, description, job levels, languages, assessment time, Test Type tags (A/B/C/D/E/K/P/S)**.
- Exclude entries listed under *Pre‑packaged Job Solutions*.

**b. Representation**
- Build an index of assessment documents: `title + short description + test type tags`.
- Create embeddings with `sentence-transformers/all-MiniLM-L6-v2` (or Gemini/OpenAI embeddings). Store in **FAISS**.

**c. Query Ingestion**
- For each query/JD or JD URL:
  1. If URL → fetch JD text (readability extraction).
  2. Classify demand signals: technical (K), behavioral (P), cognitive (A), SJT (B), etc. (zero-shot labels from LLM or keyword rules).
  3. Embed query and retrieve top 50 candidates by cosine.
  4. **Re-rank** with a cross-encoder (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) or LLM scoring prompt.
  5. **Balancing step:** If query mixes technical + behavioral, ensure final list includes both K & P (e.g., 60/40 split).

**d. Storage**
- Persist raw catalog JSON, embeddings, FAISS index, and a lightweight SQLite for metadata.

## 3) Model & Heuristics
- **Retriever:** all-MiniLM-L6-v2 (fast, robust).  
- **Re-ranker:** cross-encoder or LLM (optional but boosts quality).
- **Balancing:** Hard constraints on K/P mix when classifier indicates multi-domain requirement.
- **Diversity:** MMR (Maximal Marginal Relevance) to reduce near-duplicates.

## 4) API (FastAPI)
- `GET /health` → `{"status":"ok"}`
- `POST /recommend` → input: `{"query": "...", "k": 10}`  
  Output: list of objects with: `name, url, test_type, score`  
  (Plus `rationale` when using LLM re-ranking).

## 5) Frontend (Streamlit)
- Text box for JD/query (+ optional JD URL).
- Toggle: “balance technical + behavioral” and K/P sliders.
- Table view of 5–10 recommendations with name, URL, test type, score; filters by type/language.

## 6) Evaluation
- Use provided **Train-Set** to iterate prompts/weights.
- Compute **Mean Recall@10** vs. labeled URLs for each training query.
- Ablations: retriever only vs. retriever+reranker; with/without balancing; effect of K/P split.

## 7) Baseline Implemented Here
- As a quick baseline for immediacy, we used **TF‑IDF NN** over the labeled training queries: for each test query, find the most similar train query and output its URLs (deduped, up to 10). This produces a valid submission CSV (`submission_baseline.csv`). This is a **placeholder**; production system should use the embedding+re‑rank pipeline above.

## 8) Next Steps to Improve Recall@10
1. Crawl full catalog and build the embedding index.
2. Add K/P classifier + balancing post-processor.
3. Add cross‑encoder re-ranking.
4. Add query expansion (skills synonyms, e.g., “JS” ↔ “JavaScript”).

## 9) Tech Stack
- **Python** (Requests, BeautifulSoup, pandas)
- **FAISS**, **sentence-transformers**, **scikit-learn**
- **FastAPI** (API), **Uvicorn**
- **Streamlit** (UI)
- **SQLite** (metadata), **pydantic**

## 10) Repro Steps
```bash
# 1) Crawl
python scripts/crawl_catalog.py --out data/catalog.json

# 2) Index
python scripts/build_index.py --in data/catalog.json --faiss data/index.faiss --meta data/meta.db

# 3) Serve API
uvicorn app.main:app --reload --port 8000

# 4) Run Frontend
streamlit run ui/app.py
```

---

**Files planned:**
- `scripts/crawl_catalog.py`, `scripts/build_index.py`
- `app/main.py` (FastAPI)
- `ui/app.py` (Streamlit)
- `eval/recall_at_k.py`

**Note:** Replace TF‑IDF baseline with the embedding pipeline before final submission to maximize Mean Recall@10 and achieve balanced K/P recommendations.
