from rank_bm25 import BM25Okapi
import re


def tokenize(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text.split()


class BM25Search:
    def __init__(self, chunks: list[str]):
        self.chunks = chunks
        tokenized = [tokenize(c) for c in chunks]
        self.bm25 = BM25Okapi(tokenized)

    def search(self, query: str, top_k=5):
        scores = self.bm25.get_scores(tokenize(query))
        ranked = sorted(
            zip(self.chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )
        return [chunk for chunk, score in ranked[:top_k] if score > 0]
