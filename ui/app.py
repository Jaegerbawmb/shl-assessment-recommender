# ui/app.py

import streamlit as st
import sys, os, re
import pandas as pd

# --- Add project root to sys.path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Import local modules ---
from models.embed_index import EmbedIndex
from models.tfidf_fallback import TfidfFallback
from app.balancer import balance_kp
from utils.text import normalize_space

# --- Page setup ---
st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")
st.title("🔍 SHL Assessment Recommender")

# --- Load data and models once ---
@st.cache_resource(show_spinner=True)
def load_engines():
    FAISS_PATH = os.getenv("FAISS_PATH", "data/index.faiss")
    META_PATH = os.getenv("META_PATH", "data/meta.parquet")

    meta = pd.read_parquet(META_PATH)

    try:
        embed = EmbedIndex(FAISS_PATH, META_PATH)
        st.success("✅ FAISS index loaded successfully.")
    except Exception as e:
        embed = None
        st.warning(f"⚠️ FAISS not available, falling back to TF-IDF. ({e})")

    tfidf = TfidfFallback(meta)
    return embed, tfidf, meta

embed, tfidf, meta = load_engines()

# --- Input section ---
query = st.text_area(
    "Enter Job Description or Query",
    height=180,
    value="Need a Java developer who can collaborate with external stakeholders."
)
k = st.slider("How many results?", 1, 10, 5)

# --- Recommend button ---
if st.button("Recommend"):
    if not query.strip():
        st.warning("Please enter a query first.")
        st.stop()

    with st.spinner("Generating recommendations..."):
        query_norm = normalize_space(query)

        # use FAISS or fallback TF-IDF
        if embed is not None:
            idxs, _ = embed.retrieve(query_norm, topn=50)
            reranked = embed.rerank(query_norm, idxs)[:50]
            candidates = embed.get_items(reranked).copy()
        else:
            order = tfidf.retrieve(query_norm, topn=50)
            candidates = tfidf.get_items(order).copy()

        balanced = balance_kp(query_norm, candidates, k=k)

        results = []
        for _, r in balanced.iterrows():
            desc = (r.get('description') or '').strip()
            if len(desc) > 250:
                cut = desc[:250]
                last_period = cut.rfind('.')
                desc = cut[:last_period + 1] if last_period > 100 else cut.strip() + "..."

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
            t_types = r.get('test_types', [])
            if isinstance(t_types, str):
                t_types = re.findall(r'[A-Z]', t_types)
            mapped_types = [test_map.get(x, x) for x in t_types]

            results.append({
                "name": r.get('name', ''),
                "url": r.get('url', ''),
                "description": desc,
                "test_type": mapped_types
            })

        st.session_state['results'] = results

# --- Show results ---
results = st.session_state.get('results', [])
if results:
    st.markdown("---")
    st.subheader("Recommended Assessments")
    for rec in results:
        with st.container(border=True):
            st.markdown(f"### [{rec['name']}]({rec['url']})")
            st.write(f"**Test Type:** {', '.join(rec['test_type'])}")
            st.write(rec['description'])
