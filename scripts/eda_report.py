"""EDA reproducible para reseñas en español (sin modificar datos de entrada)."""
from __future__ import annotations
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

import pandas as pd

# Esta lista es exclusivamente descriptiva: las stop words de entrenamiento se mantienen en src/nlp.
WORDS = re.compile(r"[^\W\d_]+", re.UNICODE)


def analyze(path: str | Path, output: str | Path, top_n: int = 30) -> dict:
    frame = pd.read_csv(path)
    if not {'review_text', 'rating'}.issubset(frame.columns):
        raise ValueError('El CSV requiere review_text y rating')
    if top_n < 1:
        raise ValueError('top_n debe ser positivo')
    text = frame['review_text'].fillna('').astype(str)
    words_per_review = text.map(lambda s: len(WORDS.findall(s)))
    counts = Counter(w.lower() for t in text for w in WORDS.findall(t))
    ratings = pd.to_numeric(frame['rating'], errors='coerce')
    report = {
        'source_csv': str(path),
        'rows': int(len(frame)),
        'missing_review_text': int(frame['review_text'].isna().sum()),
        'empty_review_text': int(text.str.strip().eq('').sum()),
        'missing_or_invalid_rating': int((~ratings.isin([1,2,3,4,5])).sum()),
        'duplicate_text_exact': int(text.duplicated().sum()),
        'rating_distribution': {str(k): int(v) for k,v in ratings.value_counts().sort_index().items()},
        'length_words': {key: float(value) for key, value in words_per_review.describe().items()},
        'top_words': [{'word': word, 'count': count} for word,count in counts.most_common(top_n)],
        'note': 'Frecuencias descriptivas sin filtrar stop words. No son características aprendidas del modelo.'
    }
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    (out/'eda_summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    with (out/'top_words.csv').open('w', encoding='utf-8', newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['word','count'])
        writer.writeheader();writer.writerows(report['top_words'])
    return report


def main():
    p=argparse.ArgumentParser(description='Análisis exploratorio reproducible de reseñas')
    p.add_argument('--input', default='data/raw/reviews.csv')
    p.add_argument('--output', default='docs/evidencias/eda')
    p.add_argument('--top-n', type=int, default=30)
    a=p.parse_args()
    result=analyze(a.input,a.output,a.top_n)
    print(json.dumps({'rows':result['rows'],'output':a.output,'top_words':result['top_words'][:5]},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
