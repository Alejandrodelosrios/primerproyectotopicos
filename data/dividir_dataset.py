"""Divide el dataset en train y test (80/20, estratificado, semilla 42).

Uso:
    python data/dividir_dataset.py data/raw/reviews.csv
    python data/dividir_dataset.py data/raw/reviews.csv --prueba 0.2
"""
import argparse
import os
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

SEMILLA = 42
CARPETA = Path(__file__).resolve().parent  # la carpeta donde está este script


URL_RE = re.compile(r"(?i)\b(?:https?://|www\.)[^\s<>]+")


def leer_tabla(ruta: str) -> pd.DataFrame:
    """Lee un .csv o un .xlsx (Excel) como tabla."""
    if ruta.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(ruta, dtype={"review_id": str})
    return pd.read_csv(ruta, dtype={"review_id": str})


def clave_texto(texto: str) -> str:
    """Misma normalización que normalize_text del modelo (src/nlp/preprocessing.py)."""
    texto = unicodedata.normalize("NFC", str(texto))
    texto = URL_RE.sub(" url ", texto)
    return re.sub(r"\s+", " ", texto.lower()).strip()


def quitar_repetidas(df: pd.DataFrame, texto: str, puntaje: str):
    """Mismo texto y puntaje: deja una. Mismo texto y distinto puntaje: quita todas."""
    df = df.copy()
    df["_clave"] = df[texto].map(clave_texto)
    puntajes_distintos = df.groupby("_clave")[puntaje].transform("nunique")

    en_conflicto = puntajes_distintos > 1
    df = df[~en_conflicto]
    antes = len(df)
    df = df.drop_duplicates(subset="_clave", keep="first")
    return df.drop(columns="_clave"), antes - len(df), int(en_conflicto.sum())


def main() -> int:
    parser = argparse.ArgumentParser(description="División estratificada train/test")
    parser.add_argument("ruta", help="CSV o Excel limpio con las columnas review_text y rating")
    parser.add_argument("--salida", default=str(CARPETA / "processed"), help="Carpeta de salida (por defecto: processed/ junto al script)")
    parser.add_argument("--prueba", type=float, default=0.2, help="Proporción de prueba")
    parser.add_argument("--texto", default="review_text")
    parser.add_argument("--puntaje", default="rating")
    args = parser.parse_args()

    df = leer_tabla(args.ruta)
    df = df.dropna(subset=[args.texto, args.puntaje])
    df = df[df[args.texto].astype(str).str.strip() != ""]
    df = df[df[args.puntaje].isin([1, 2, 3, 4, 5])]
    filas_antes = len(df)
    df, repetidas, en_conflicto = quitar_repetidas(df, args.texto, args.puntaje)
    print(f"Filas leídas (ya sin vacías ni puntajes inválidos): {filas_antes}")
    print(f"Repetidas quitadas (mismo texto y puntaje): {repetidas}")
    print(f"Quitadas por mismo texto con distinto puntaje: {en_conflicto}")

    train, test = train_test_split(
        df,
        test_size=args.prueba,
        stratify=df[args.puntaje],
        random_state=SEMILLA,
    )

    os.makedirs(args.salida, exist_ok=True)
    train.to_csv(os.path.join(args.salida, "train.csv"), index=False)
    test.to_csv(os.path.join(args.salida, "test.csv"), index=False)

    print(f"Total tras limpieza: {len(df)}")
    print(f"Entrenamiento: {len(train)} | Prueba: {len(test)} | Semilla: {SEMILLA}")
    print("\nDistribución en entrenamiento (%):")
    print((train[args.puntaje].value_counts(normalize=True).sort_index() * 100).round(1).to_string())
    print("\nDistribución en prueba (%):")
    print((test[args.puntaje].value_counts(normalize=True).sort_index() * 100).round(1).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
