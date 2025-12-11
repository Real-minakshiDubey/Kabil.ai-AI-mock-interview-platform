# ml/scoring_model.py
# Lightweight scoring: TF-IDF similarity + keyword match + heuristics
from typing import List, Dict
import math
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize

# simple normalization
def normalize_text(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# compute cosine similarity via TF-IDF
_vectorizer = None
def _tfidf_cosine(a: str, b: str) -> float:
    global _vectorizer
    texts = [a, b]
    if _vectorizer is None:
        try:
            _vectorizer = TfidfVectorizer().fit(texts)
        except Exception:
            _vectorizer = None
    if _vectorizer is None:
        sa = set(a.split()); sb = set(b.split())
        if not sa or not sb:
            return 0.0
        return len(sa & sb) / len(sa | sb)
    tfidf = _vectorizer.transform(texts)
    v1 = tfidf[0].toarray()[0]
    v2 = tfidf[1].toarray()[0]
    num = float((v1 * v2).sum())
    den = math.sqrt((v1 * v1).sum()) * math.sqrt((v2 * v2).sum())
    if den == 0.0:
        return 0.0
    return float(num / den)

def keyword_score(answer: str, keywords: List[str]) -> float:
    if not keywords:
        return 0.0
    ans = normalize_text(answer)
    tokens = set(word_tokenize(ans))
    if not tokens:
        return 0.0
    found = 0
    for k in keywords:
        k_norm = normalize_text(k)
        if all(tok in tokens for tok in k_norm.split()):
            found += 1
    return (found / len(keywords)) * 100.0

def score_answer(question: str, answer: str, expected_keywords: List[str] = None) -> Dict:
    qn = normalize_text(question)
    ans = normalize_text(answer)
    relevance = _tfidf_cosine(qn, ans) * 100.0
    kw_score = keyword_score(answer, expected_keywords or [])
    length = len(ans.split())
    length_score = min(100.0, (length / 20.0) * 100.0)
    overall = 0.6 * relevance + 0.3 * kw_score + 0.1 * length_score
    overall = max(0.0, min(100.0, overall))
    return {
        "overall": round(overall, 2),
        "breakdown": {
            "relevance": round(relevance, 2),
            "keywords": round(kw_score, 2),
            "length": round(length_score, 2),
        },
        "comments": [
            "Mention key points more explicitly." if kw_score < 50 else "Good use of expected keywords.",
            "Try to expand answer if it's too short." if length < 8 else "Length is good."
        ]
    }
