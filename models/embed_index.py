import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss
from typing import List, Tuple

EMBED_MODEL = os.getenv('EMBED_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
CROSS_ENCODER = os.getenv('CROSS_ENCODER', 'cross-encoder/ms-marco-MiniLM-L-6-v2')

class EmbedIndex:
    def __init__(self, faiss_path: str, meta_path: str):
        self.model = SentenceTransformer(EMBED_MODEL)
        self.cross = CrossEncoder(CROSS_ENCODER)
        self.index = faiss.read_index(faiss_path)
        self.meta = pd.read_parquet(meta_path)

    def _encode(self, text: str) -> np.ndarray:
        v = self.model.encode([text], normalize_embeddings=True)
        return np.asarray(v, dtype='float32')

    def retrieve(self, query: str, topn: int = 50) -> Tuple[List[int], List[float]]:
        v = self._encode(query)
        sims, idx = self.index.search(v, topn)
        return idx[0].tolist(), sims[0].tolist()

    def rerank(self, query: str, idxs: List[int]) -> List[int]:
        pairs = [[query, self.meta.iloc[i]['name'] + " \n" + (self.meta.iloc[i].get('description','') or '')] for i in idxs]
        scores = self.cross.predict(pairs).tolist()
        order = sorted(range(len(idxs)), key=lambda i: scores[i], reverse=True)
        return [idxs[i] for i in order]

    def get_items(self, idxs: List[int]):
        return self.meta.iloc[idxs]
