"""from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="t5-small",
    tokenizer="t5-small",
    framework="pt"
)

def summarize_text(text):
    word_count = len(text.split())

    # Very short text → return as-is
    if word_count < 20:
        return text

    # Dynamically decide summary length
    max_new_tokens = min(60, word_count // 2)

    summary = summarizer(
        text,
        max_new_tokens=max_new_tokens,
        do_sample=False
    )

    return summary[0]["summary_text"]"""

from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Better model for summarization
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    framework="pt"
)

def extract_key_sentences(text, top_k=6):
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]

    if len(sentences) <= top_k:
        return text

    tfidf = TfidfVectorizer(stop_words="english")
    X = tfidf.fit_transform(sentences)

    scores = np.array(X.sum(axis=1)).ravel()
    top_idx = scores.argsort()[-top_k:]

    selected = [sentences[i] for i in sorted(top_idx)]
    return ". ".join(selected)

def summarize_text(text):
    if len(text.split()) < 40:
        return text

    important_text = extract_key_sentences(text)

    summary = summarizer(
        important_text,
        max_new_tokens=120,
        do_sample=False
    )

    return summary[0]["summary_text"]


