from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Optional
import os

app = FastAPI(title="Operadoras de Saúde API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df_operadoras = pd.read_csv('../../data/processed/relatorio_cadop.csv', delimiter=';', encoding='utf-8', quotechar='"')
df_operadoras = df_operadoras.astype(str)

@app.get("/operadoras/")
async def list_operadoras(limit: int = 10, offset: int = 0):
    if df_operadoras is None:
        raise HTTPException(status_code=400, detail="Nenhum arquivo CSV foi carregado ainda")
    
    records = df_operadoras.iloc[offset:offset+limit].to_dict(orient='records')
    return {"data": records, "total": len(df_operadoras)}

@app.get("/operadoras/search/")
async def search_operadoras(
    query: str,
    campo: Optional[str] = None,
    uf: Optional[str] = None,
    modalidade: Optional[str] = None,
    limit: int = 10
):
    if df_operadoras is None:
        raise HTTPException(status_code=400, detail="Nenhum arquivo CSV foi carregado ainda")
    
    filtered_df = df_operadoras
    if uf:
        filtered_df = filtered_df[filtered_df['UF'].str.upper() == uf.upper()]
    
    if modalidade:
        filtered_df = filtered_df[filtered_df['Modalidade'].str.contains(modalidade, case=False, na=False)]
    
    if campo:
        result = filtered_df[filtered_df[campo].str.contains(query, case=False, na=False)]
    else:
        text_columns = filtered_df.select_dtypes(include=['object']).columns
        mask = filtered_df[text_columns].apply(lambda x: x.str.contains(query, case=False, na=False)).any(axis=1)
        result = filtered_df[mask]
    
    result = result.head(limit)
    
    return {"data": result.to_dict(orient='records'), "total_results": len(result)}

@app.get("/operadoras/{registro_ans}")
async def get_operadora_by_id(registro_ans: str):
    if df_operadoras is None:
        raise HTTPException(status_code=400, detail="Nenhum arquivo CSV foi carregado ainda")
    
    operadora = df_operadoras[df_operadoras['Registro_ANS'] == registro_ans]
    if operadora.empty:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    
    return operadora.iloc[0].to_dict()

@app.get("/operadoras/ufs/")
async def list_ufs():
    if df_operadoras is None:
        raise HTTPException(status_code=400, detail="Nenhum arquivo CSV foi carregado ainda")
    
    ufs = df_operadoras['UF'].unique().tolist()
    return {"ufs": sorted([uf for uf in ufs if uf != 'nan'])}  

@app.get("/operadoras/modalidades/")
async def list_modalidades():
    if df_operadoras is None:
        raise HTTPException(status_code=400, detail="Nenhum arquivo CSV foi carregado ainda")
    
    modalidades = df_operadoras['Modalidade'].unique().tolist()
    return {"modalidades": sorted([m for m in modalidades if m != 'nan'])}  