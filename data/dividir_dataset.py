"""Divide el dataset en entrenamiento y prueba (estratificado, semilla fija).

Se ejecuta UNA sola vez y todo el grupo usa la misma partición. El conjunto de
prueba no se usa para ajustar nada (ni stop words, ni hiperparámetros).

Uso:
    python data/dividir_dataset.py data/raw/reviews.csv
    python data/dividir_dataset.py data/raw/reviews.csv --prueba 0.2
"""
import argparse
import os
import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

SEMILLA = 42
CARPETA = Path(__file__).resolve().parent  # la carpeta donde está este script


def leer_tabla(ruta: str) -> pd.DataFrame:
    """Lee un .csv o un .xlsx (Excel) como tabla."""
    if ruta.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(ruta, dtype={"review_id": str})
    return pd.read_csv(ruta, dtype={"review_id": str})


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
    df = df.drop_duplicates(subset=[args.texto, args.puntaje])

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