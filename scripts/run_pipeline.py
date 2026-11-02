"""Un comando reproducible: descarga opcional, control de duplicados, split, EDA y ML.

Ejecutar desde la raíz: python scripts/run_pipeline.py
No altera los archivos ni scripts de la rama data; crea una copia intermedia saneada.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def clean_reviews(source: str | Path, target: str | Path) -> dict:
    source, target=Path(source),Path(target)
    df=pd.read_csv(source, dtype={'review_text':'string'})
    if not {'review_text','rating'}.issubset(df.columns):
        raise ValueError('Se requieren columnas review_text y rating')
    start=len(df)
    df=df.dropna(subset=['review_text','rating']).copy()
    df['review_text']=df['review_text'].str.strip()
    ratings=pd.to_numeric(df['rating'], errors='coerce')
    df=df[(df.review_text.str.len()>0)&ratings.isin([1,2,3,4,5])].copy()
    df['rating']=pd.to_numeric(df.rating).astype('int64')
    # La misma clave que la validación de train.py.
    from src.nlp.preprocessing import normalize_text
    df['_key']=df.review_text.map(normalize_text)
    conflict=df.groupby('_key')['rating'].nunique()
    ambiguous=set(conflict[conflict>1].index)
    df=df[~df['_key'].isin(ambiguous)].drop_duplicates('_key').drop(columns='_key')
    if set(df.rating.unique()) != {1,2,3,4,5} or df.rating.value_counts().min() < 2:
        raise ValueError('Tras saneamiento se requieren al menos dos reseñas por clase')
    target.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(target,index=False)
    return {'raw_rows':start,'clean_rows':len(df),'removed':start-len(df),'conflicting_text_keys':len(ambiguous)}


def run(args):
    def execute(*argv):
        print('EJECUTANDO:',sys.executable,*argv,flush=True)
        subprocess.run([sys.executable,*argv],check=True)
    if args.download:
        execute('data/descargar_dataset.py','--maximo',str(args.maximo))
    raw=Path(args.raw)
    if not raw.is_file():
        raise FileNotFoundError(f'{raw} no existe. Usa --download o descarga el dataset primero')
    execute('data/revisar_dataset.py',str(raw))
    execute('scripts/eda_report.py','--input',str(raw),'--output',str(Path(args.output)/'eda'))
    stats=clean_reviews(raw, args.clean)
    print('SANEAMIENTO:',json.dumps(stats,ensure_ascii=False))
    execute('data/dividir_dataset.py',str(args.clean),'--prueba',str(args.test_size),'--salida',str(args.splits))
    train=Path(args.splits)/'train.csv';test=Path(args.splits)/'test.csv'
    # Prevalidar antes del entrenamiento para detectar fugas.
    from src.models.train import load_reviews,validate_splits
    validate_splits(load_reviews(train),load_reviews(test))
    if args.quick:
        execute('-m','src.models.experiments','--train',str(train),'--test',str(test),
                '--output-dir',str(Path(args.output)/'final'),'--methods','stemming','--c-values','1','--folds','2')
    else:
        execute('-m','src.models.experiments','--train',str(train),'--test',str(test),
                '--output-dir',str(Path(args.output)/'final'),'--folds','3')
    print('OK. Resultados:',Path(args.output)/'final')


def main():
    p=argparse.ArgumentParser(description='Orquestación reproducible data -> NLP -> ML')
    p.add_argument('--download',action='store_true',help='Descarga/reemplaza data/raw/reviews.csv')
    p.add_argument('--maximo',type=int,default=20000)
    p.add_argument('--raw',default='data/raw/reviews.csv')
    p.add_argument('--clean',default='data/processed/clean_reviews.csv')
    p.add_argument('--splits',default='data/processed')
    p.add_argument('--output',default='models')
    p.add_argument('--test-size',type=float,default=.20)
    p.add_argument('--quick',action='store_true',help='Smoke test, no usar para reportar el mejor modelo')
    args=p.parse_args()
    if not 0<args.test_size<1:p.error('--test-size debe estar entre 0 y 1')
    run(args)

if __name__=='__main__':
    main()
