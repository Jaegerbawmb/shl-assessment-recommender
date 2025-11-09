# SHL Assessment Recommender

End-to-end system for recommending **SHL Individual Test Solutions** from a JD/query.
- Meets API spec: `/health`, `/recommend`
- Outputs 5–10 assessments with name, URL, test_type, score
- Balances **technical (K)** vs **behavioral (P)** when the query demands

## Quickstart

```bash
# 0) Python
python -V   # 3.10+

# 1) Install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Environment (optional LLM rerank)
cp .env.example .env
# Fill keys if you want LLM scoring. Otherwise system uses local cross-encoder fallback.

# 3) Crawl SHL catalog (Individual Test Solutions only)
python scripts/crawl_catalog.py --out data/catalog_raw.json

# 4) Build index (FAISS + metadata parquet)
python scripts/build_index.py   --in data/catalog_raw.json   --faiss data/index.faiss   --meta data/meta.parquet

# 5) Run API
uvicorn app.main:app --port 8000 --reload
# GET  /health
# POST /recommend {"query": "Need Java dev who collaborates with stakeholders", "k": 10}

# 6) Streamlit UI
streamlit run ui/app.py

# 7) Evaluate Mean Recall@10 (using provided Train-Set)
python scripts/eval_recall.py --train_xlsx "data/Gen_AI Dataset.xlsx" --pred_csv path/to/submission.csv
```
