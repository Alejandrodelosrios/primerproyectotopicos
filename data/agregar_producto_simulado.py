"""Agrega product_id y category SIMULADOS a train.csv y test.csv.

La fuente no trae ninguno, así que se inventan:
  product_id = "SIM-" + número del review_id
  category   = una de CATEGORIAS, elegida al azar pero fija para cada review_id
No toca data/processed/; escribe en data/processed_con_producto/.

Uso: python data/agregar_producto_simulado.py
"""
import argparse
import sys
import zlib
from pathlib import Path

import pandas as pd

CARPETA = Path(__file__).resolve().parent
CATEGORIAS = [
    "hogar", "ropa", "electrónica", "belleza", "cocina",
    "juguetes", "deportes", "automotriz", "mascotas", "oficina",
]


def id_simulado(review_id: str) -> str:
    numeros = "".join(c for c in str(review_id) if c.isdigit())
    if not numeros:
        raise ValueError(f"El review_id '{review_id}' no tiene números")
    return "SIM-" + numeros.zfill(7)


def categoria_simulada(review_id: str) -> str:
    return CATEGORIAS[zlib.crc32(str(review_id).encode()) % len(CATEGORIAS)]


def agregar(ruta_entrada: Path, ruta_salida: Path) -> int:
    df = pd.read_csv(ruta_entrada, dtype={"review_id": str})
    if "review_id" not in df.columns:
        raise ValueError(f"{ruta_entrada}: falta review_id")
    for col in ("product_id", "category"):
        if col in df.columns:
            raise ValueError(f"{ruta_entrada}: ya tiene {col}")
    pos = df.columns.get_loc("review_id") + 1
    df.insert(pos, "product_id", df["review_id"].map(id_simulado))
    df.insert(pos + 1, "category", df["review_id"].map(categoria_simulada))
    df.to_csv(ruta_salida, index=False)
    return len(df)


def main() -> int:
    parser = argparse.ArgumentParser(description="Agrega product_id y category simulados")
    parser.add_argument("--entrada", default=str(CARPETA / "processed"))
    parser.add_argument("--salida", default=str(CARPETA / "processed_con_producto"))
    args = parser.parse_args()

    entrada, salida = Path(args.entrada), Path(args.salida)
    if entrada.resolve() == salida.resolve():
        print("ERROR: la salida no puede ser la carpeta de entrada.")
        return 1
    salida.mkdir(parents=True, exist_ok=True)

    for nombre in ("train.csv", "test.csv"):
        filas = agregar(entrada / nombre, salida / nombre)
        print(f"{nombre}: {filas} filas -> {salida / nombre}")

    print("\nOjo: product_id y category son SIMULADOS. Decirlo en el README y en el informe.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
