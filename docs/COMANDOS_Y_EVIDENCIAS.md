# Pruebas y evidencias del cierre de requisitos 1–6

Ejecutar desde la **raíz** de `primerproyectotopicos`, con el entorno virtual activo.

```powershell
python -m pip install -r requirements.txt
python -m spacy download es_core_news_sm
python -m pip check
python -m pytest tests/ -q
python scripts/run_pipeline.py --quick
python scripts/run_pipeline.py
Get-Content models/final/metrics.json
Import-Csv models/final/experiments.csv | Format-Table
Import-Csv models/final/errors.csv | Select-Object -First 10 | Format-List
python -m uvicorn app.main:app --app-dir backend --reload
```

Usar `python scripts/run_pipeline.py --download` únicamente si no existe `data/raw/reviews.csv` o se desea regenerarlo. El comando `--quick` sobrescribe los resultados en `models/final`, por tanto **ejecutar la modalidad completa después del smoke test**.

Registrar en el informe: Python y versiones (`python --version`, `pip freeze`); resultados completos de pytest; datos de `docs/evidencias/eda/`; tabla comparativa; matriz de confusión; ejemplos anotados de `errors.csv`; modelo que reporta la API y respuestas de Swagger.

Si el instalador falla, corregir el entorno y versiones en un cambio separado y registrar el conflicto; **no considerar reproducible un entorno que no se ha instalado desde cero**.

## Git

Añadir solamente `scripts/`, `tests/test_reproducibilidad.py` y estos documentos, más evidencias pequeñas verificadas. No incluir `data/raw`, `data/processed`, `.venv`, ni Joblib salvo decisión explícita del equipo.
