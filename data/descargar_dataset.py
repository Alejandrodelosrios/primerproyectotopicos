"""Descarga reseñas en español con puntaje de 1 a 5 y las guarda como CSV.

Fuente por defecto: SetFit/amazon_reviews_multi_es (copia en Hugging Face del
corpus MARC de Amazon). Verifica la licencia antes de usarlo: MARC permite uso
solo para investigación académica.

Uso (desde la raíz del repo):
    pip install huggingface_hub pandas
    python data/descargar_dataset.py
    python data/descargar_dataset.py --maximo 20000

Qué hace:
  1. Descarga train.jsonl del repositorio en Hugging Face.
  2. Detecta las columnas de texto y de puntaje.
  3. Si el puntaje viene como 0-4 lo pasa a 1-5. Si ya viene 1-5 lo deja igual.
     Si viene otra cosa, se detiene para que lo revises a mano.
  4. Toma una muestra estratificada y guarda data/raw/reviews.csv.
"""
import argparse
import os
import sys
from pathlib import Path

import pandas as pd

REPO = "SetFit/amazon_reviews_multi_es"
ARCHIVO = "train.jsonl"
SEMILLA = 42
CARPETA = Path(__file__).resolve().parent  # la carpeta donde está este script


def main() -> int:
    parser = argparse.ArgumentParser(description="Descarga el dataset de reseñas")
    parser.add_argument("--repo", default=REPO)
    parser.add_argument("--archivo", default=ARCHIVO)
    parser.add_argument("--maximo", type=int, default=20000, help="Máximo de reseñas a conservar")
    parser.add_argument("--salida", default=str(CARPETA / "raw" / "reviews.csv"), help="Por defecto: raw/reviews.csv junto al script")
    args = parser.parse_args()

    from huggingface_hub import hf_hub_download

    ruta = hf_hub_download(repo_id=args.repo, filename=args.archivo, repo_type="dataset")
    df = pd.read_json(ruta, lines=True)
    print(f"Descargado: {len(df)} filas. Columnas: {list(df.columns)}")

    if "text" not in df.columns or "label" not in df.columns:
        print("ERROR: no encontré las columnas 'text' y 'label'. Revisa el archivo a mano.")
        return 1

    etiquetas = set(df["label"].dropna().unique().tolist())
    print(f"Valores distintos de 'label': {sorted(etiquetas)}")
    if etiquetas == {0, 1, 2, 3, 4}:
        df["rating"] = df["label"] + 1
        print("Las etiquetas venían de 0 a 4: se sumó 1 para dejarlas de 1 a 5.")
    elif etiquetas == {1, 2, 3, 4, 5}:
        df["rating"] = df["label"]
    else:
        print("ERROR: las etiquetas no son 0-4 ni 1-5. No convierto nada; revísalo antes de seguir.")
        return 1

    df = df.rename(columns={"text": "review_text"})
    columnas = [c for c in ("id", "review_text", "rating") if c in df.columns]
    df = df[columnas].rename(columns={"id": "review_id"})

    if len(df) > args.maximo:
        por_clase = args.maximo // 5
        partes = [
            df[df["rating"] == r].sample(
                min(int((df["rating"] == r).sum()), por_clase), random_state=SEMILLA
            )
            for r in sorted(df["rating"].unique())
        ]
        df = pd.concat(partes).reset_index(drop=True)
        print(f"Muestra estratificada: {len(df)} filas (hasta {por_clase} por puntaje).")

    os.makedirs(os.path.dirname(args.salida), exist_ok=True)
    df.to_csv(args.salida, index=False)
    print(f"Guardado en {args.salida}")
    print("\nAhora corre: python data/revisar_dataset.py", args.salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())