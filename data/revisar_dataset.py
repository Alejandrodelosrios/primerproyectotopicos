"""Revisa la calidad de un dataset de reseñas (texto + puntaje 1 a 5).

Uso:
    python data/revisar_dataset.py data/raw/reviews.csv
    python data/revisar_dataset.py data/raw/reviews.csv --texto review_text --puntaje rating

Imprime: filas, columnas, valores faltantes, puntajes inválidos, duplicados,
distribución de puntajes y longitud de los textos. No modifica el archivo.
"""
import argparse
import sys

import pandas as pd


def leer_tabla(ruta: str) -> pd.DataFrame:
    """Lee un .csv o un .xlsx (Excel) como tabla."""
    if ruta.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(ruta, dtype={"review_id": str})
    return pd.read_csv(ruta, dtype={"review_id": str})


def main() -> int:
    parser = argparse.ArgumentParser(description="Revisión rápida de un dataset de reseñas")
    parser.add_argument("ruta", help="Ruta del archivo (.csv o .xlsx)")
    parser.add_argument("--texto", default="review_text", help="Columna con el texto")
    parser.add_argument("--puntaje", default="rating", help="Columna con el puntaje 1-5")
    args = parser.parse_args()

    df = leer_tabla(args.ruta)
    print(f"Archivo: {args.ruta}")
    print(f"Filas: {len(df)} | Columnas: {list(df.columns)}")

    faltan = [c for c in (args.texto, args.puntaje) if c not in df.columns]
    if faltan:
        print(f"ERROR: faltan las columnas obligatorias {faltan}")
        return 1

    print("\n== Valores faltantes por columna ==")
    print(df.isna().sum().to_string())

    textos = df[args.texto].fillna("").astype(str).str.strip()
    vacios = int((textos == "").sum())
    print(f"\nTextos vacíos: {vacios}")

    puntajes = pd.to_numeric(df[args.puntaje], errors="coerce")
    invalidos = int((~puntajes.isin([1, 2, 3, 4, 5])).sum())
    print(f"Puntajes inválidos (no son 1, 2, 3, 4 ni 5): {invalidos}")

    duplicados = int(df.duplicated(subset=[args.texto, args.puntaje]).sum())
    print(f"Reseñas duplicadas (mismo texto y puntaje): {duplicados}")

    print("\n== Distribución de puntajes ==")
    conteo = puntajes.value_counts().sort_index()
    total = int(conteo.sum()) or 1
    for valor, n in conteo.items():
        print(f"  {valor}: {n} ({100 * n / total:.1f}%)")

    palabras = textos.str.split().str.len()
    print("\n== Longitud de los textos (en palabras) ==")
    print(palabras.describe().round(1).to_string())
    print(f"Textos de menos de 3 palabras: {int((palabras < 3).sum())}")

    if "product_category" in df.columns:
        print("\n== Reseñas por categoría ==")
        print(df["product_category"].value_counts().to_string())

    return 0


if __name__ == "__main__":
    sys.exit(main())