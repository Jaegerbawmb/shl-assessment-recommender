import argparse, json
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import re
import os

print("🧠 Running UPDATED build_index.py with cleaned extraction logic...")

def load_catalog(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_description(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"Home Products Product Catalog.*?Description\s*", "", text)
    text = re.sub(r"Book a Demo.*$", "", text)
    return text.strip()

def build_text(doc):
    parts = [
        doc.get('name', ''),
        ', '.join(doc.get('job_levels', []) or []),
        ', '.join(doc.get('languages', []) or []),
        ', '.join(doc.get('test_types', []) or []),
        doc.get('assessment_length', '') or '',
        clean_description(doc.get('description', ''))
    ]
    return ' '.join([p for p in parts if p])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='infile', required=True)
    ap.add_argument('--faiss', required=True)
    ap.add_argument('--meta', required=True)
    ap.add_argument('--model', default='sentence-transformers/all-MiniLM-L6-v2')
    args = ap.parse_args()

    data = load_catalog(args.infile)
    df = pd.DataFrame(data)
    df['text'] = df.apply(build_text, axis=1)

    print(f"📘 Items: {len(df)} | Encoding with {args.model}")

    model = SentenceTransformer(args.model)
    emb = model.encode(df['text'].tolist(), batch_size=64, show_progress_bar=True, normalize_embeddings=True)
    emb = np.asarray(emb, dtype='float32')

    index = faiss.IndexFlatIP(emb.shape[1])
    index.add(emb)
    faiss.write_index(index, args.faiss)

    df.drop(columns=['text']).to_parquet(args.meta, index=False)

    print(f"✅ Saved FAISS -> {args.faiss}")
    print(f"✅ Saved metadata -> {args.meta}")

if __name__ == '__main__':
    main()
