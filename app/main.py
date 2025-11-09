import os, re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import RecommendRequest, RecommendResponse, Recommendation
from utils.jd_extract import extract_text_from_url
from utils.text import normalize_space
from models.embed_index import EmbedIndex
from models.tfidf_fallback import TfidfFallback
from app.balancer import balance_kp
import pandas as pd

app = FastAPI(title="SHL Assessment Recommender", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FAISS_PATH = os.getenv('FAISS_PATH', 'data/index.faiss')
META_PATH = os.getenv('META_PATH', 'data/meta.parquet')

_embed = None
_tfidf = None
_meta = None

@app.on_event("startup")
def _load():
    global _embed, _tfidf, _meta
    _meta = pd.read_parquet(META_PATH)
    try:
        _embed = EmbedIndex(FAISS_PATH, META_PATH)
    except Exception:
        _embed = None
    _tfidf = TfidfFallback(_meta)

@app.get('/health')
def health():
    return {"status": "ok"}

def _maybe_read_url(text: str) -> str:
    if re.match(r"^https?://", text.strip(), flags=re.I):
        try:
            return extract_text_from_url(text.strip())
        except Exception:
            return text
    return text

@app.post('/recommend')
def recommend(req: RecommendRequest):
    query = normalize_space(_maybe_read_url(req.query))
    k = req.k

    if _embed is not None:
        idxs, _ = _embed.retrieve(query, topn=50)
        reranked = _embed.rerank(query, idxs)[:50]
        candidates = _embed.get_items(reranked).copy()
        candidates['score'] = list(range(len(candidates), 0, -1))
    else:
        order = _tfidf.retrieve(query, topn=50)
        candidates = _tfidf.get_items(order).copy()
        candidates['score'] = list(range(len(candidates), 0, -1))

    balanced = balance_kp(req.query, candidates, k=k)

    out = []
    for _, r in balanced.iterrows():
        raw_desc = r.get('description', '') or ''
        desc = raw_desc.strip()

        
        if len(desc) > 250:
            
            cut = desc[:250]
            last_period = cut.rfind('.')
            if last_period > 100:  
                desc = cut[:last_period + 1]
            else:
                desc = cut.strip() + "..."

        
            duration = None
            match = re.search(
                r"(?:in\s*)?(\d+)\s*(?:minutes|min)\b|=\s*(\d+)\s*(?:minutes|min)",
                raw_desc,
                flags=re.I
            )
            if match:
                num_str = match.group(1) or match.group(2)
                try:
                    duration = int(num_str)
                except (ValueError, TypeError):
                    duration = None


        
        test_map = {
            "K": "Knowledge & Skills",
            "P": "Personality & Behaviour",
            "C": "Competencies",
            "S": "Simulation",
            "A": "Aptitude",
            "B": "Behavioural",
            "E": "Emotional Intelligence",
            "D": "Decision Making",
            "R": "Remote Testing"
        }

        test_types_value = r.get('test_types', [])
        if isinstance(test_types_value, (list, tuple)):
            types_list = test_types_value
        elif hasattr(test_types_value, 'tolist'):
            types_list = test_types_value.tolist()
        elif isinstance(test_types_value, str):
            types_list = re.findall(r'[A-Z]', test_types_value)
        else:
            types_list = []
        mapped_types = [test_map.get(x, x) for x in types_list]

        remote_support = "Yes" if re.search(r"remote\s*testing", raw_desc, flags=re.I) else "No"

   
        out.append({
            "url": r.get('url', ''),
            "name": r.get('name', ''),
            "adaptive_support": "No",
            "description": desc,
            "duration": duration,
            "remote_support": remote_support,
            "test_type": mapped_types
        })

    return {"recommended_assessments": out[:k]}