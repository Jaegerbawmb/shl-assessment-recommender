from typing import List
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TfidfFallback:
    def __init__(self, docs: pd.DataFrame):
        self.docs = docs.reset_index(drop=True)
        self.docs['text'] = (
            self.docs['name'].fillna('') + ' ' + self.docs['description'].fillna('')
        )
        self.vec = TfidfVectorizer(stop_words='english', ngram_range=(1,2), min_df=2)
        self.mat = self.vec.fit_transform(self.docs['text'])

    def retrieve(self, query: str, topn: int = 50) -> List[int]:
        qv = self.vec.transform([query])
        sims = cosine_similarity(qv, self.mat)[0]
        order = sims.argsort()[::-1][:topn]
        return order.tolist()

    def get_items(self, idxs: List[int]):
        return self.docs.iloc[idxs]
