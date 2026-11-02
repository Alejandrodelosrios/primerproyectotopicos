"""Pruebas del saneamiento previo al split y del EDA (sin descargar datos)."""
from pathlib import Path
import pandas as pd
import pytest
from scripts.run_pipeline import clean_reviews
from scripts.eda_report import analyze


def test_clean_removes_normalized_duplicates_and_conflicts(tmp_path: Path):
    rows=[]
    for label in range(1,6):
        rows.extend([{'review_text':f'Reseña única de clase {label} número {i}', 'rating':label} for i in range(3)])
    rows += [{'review_text':'La misma reseña', 'rating':1},
             {'review_text':' LA MISMA RESEÑA ', 'rating':5},
             {'review_text':'Texto duplicado', 'rating':2},
             {'review_text':' texto duplicado ', 'rating':2}]
    source=tmp_path/'raw.csv';out=tmp_path/'clean.csv'
    pd.DataFrame(rows).to_csv(source,index=False)
    result=clean_reviews(source,out)
    cleaned=pd.read_csv(out)
    assert result['conflicting_text_keys']==1
    assert len(cleaned)==16
    assert cleaned['rating'].value_counts().min()>=2


def test_eda_produces_summary_and_top_words(tmp_path:Path):
    source=tmp_path/'reviews.csv'
    pd.DataFrame({'review_text':['Muy bueno','No me gustó','Muy bueno'],'rating':[5,1,5]}).to_csv(source,index=False)
    data=analyze(source,tmp_path/'report',5)
    assert data['rows']==3
    assert data['duplicate_text_exact']==1
    assert (tmp_path/'report'/'eda_summary.json').exists()
    assert (tmp_path/'report'/'top_words.csv').exists()


def test_eda_rejects_bad_schema(tmp_path:Path):
    source=tmp_path/'invalid.csv';pd.DataFrame({'text':['hola']}).to_csv(source,index=False)
    with pytest.raises(ValueError,match='review_text'):
        analyze(source,tmp_path/'report')
