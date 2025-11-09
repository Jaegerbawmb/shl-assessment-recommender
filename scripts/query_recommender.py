import argparse, faiss, pandas as pd
from sentence_transformers import SentenceTransformer

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--faiss", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    ap.add_argument("--topk", type=int, default=5)
    args = ap.parse_args()

    print("Loading model and index...")
    model = SentenceTransformer(args.model)
    index = faiss.read_index(args.faiss)
    meta = pd.read_parquet(args.meta)

    while True:
        query = input("\n🔎 Enter your query (or 'exit'): ").strip()
        if query.lower() in ["exit", "quit"]:
            break

        emb = model.encode([query], normalize_embeddings=True)
        scores, ids = index.search(emb.astype("float32"), args.topk)

        print("\nTop recommendations:")
        for i, idx in enumerate(ids[0]):
            row = meta.iloc[idx]
            print(f"\n{i+1}. {row['name']}")
            print(f"   URL: {row['url']}")
            snippet = row['description'][:250].strip().replace("\n", " ")
            print(f"   Description: {snippet}...")

if __name__ == "__main__":
    main()
