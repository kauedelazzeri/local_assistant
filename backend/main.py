import os
import fitz  # PyMuPDF
import requests
from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Generator
import json

app = FastAPI(title="InsightFinder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama2"

class SearchRequest(BaseModel):
    query: str
    folder: str
    extensions: List[str]

class SearchResult(BaseModel):
    file_path: str
    ia_response: str

def ler_arquivo(caminho):
    ext = os.path.splitext(caminho)[1].lower()
    if ext == '.txt':
        for enc in ['utf-8', 'latin1', 'cp1252']:
            try:
                with open(caminho, 'r', encoding=enc) as f:
                    return f.read()
            except:
                continue
        print(f"[!] Erro ao ler {caminho} com os encodings disponíveis.")
        return ""
    elif ext == '.pdf':
        try:
            doc = fitz.open(caminho)
            return "\n".join([page.get_text() for page in doc])
        except Exception as e:
            print(f"[!] Erro ao ler PDF {caminho}: {e}")
            return ""
    return ""

def gerar_resposta(prompt, modelo=OLLAMA_MODEL):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": modelo,
            "prompt": prompt,
            "stream": False
        })
        return response.json()['response'].strip()
    except Exception as e:
        return f"Erro: {str(e)}"

def buscar_stream(req: SearchRequest):
    def generator():
        for root, _, files in os.walk(req.folder):
            for nome_arquivo in files:
                ext = os.path.splitext(nome_arquivo)[1].lower()
                if ext not in req.extensions:
                    continue

                caminho = os.path.join(root, nome_arquivo)
                conteudo = ler_arquivo(caminho)
                if not conteudo.strip():
                    continue

                prompt = f"""
Estou procurando arquivos que tenham relação com esta frase:
"{req.query}"

Abaixo está o conteúdo do arquivo:
{conteudo[:2000]}

Esse conteúdo tem relação direta com a frase acima?
Responda 'Sim' ou 'Não' e justifique em uma linha.
"""

                resposta = gerar_resposta(prompt)
                if "sim" in resposta.lower():
                    yield json.dumps({
                        "file_path": caminho,
                        "ia_response": resposta.strip()
                    }) + "\n"
    return generator()

@app.post("/api/search/stream")
def search_files_stream(req: SearchRequest):
    return StreamingResponse(buscar_stream(req), media_type="application/x-ndjson")

@app.post("/api/search", response_model=List[SearchResult])
async def search_files(req: SearchRequest):
    resultados = []
    for root, _, files in os.walk(req.folder):
        for nome_arquivo in files:
            ext = os.path.splitext(nome_arquivo)[1].lower()
            if ext not in req.extensions:
                continue
            caminho = os.path.join(root, nome_arquivo)
            conteudo = ler_arquivo(caminho)
            if not conteudo.strip():
                continue
            prompt = f"""
Estou procurando arquivos que tenham relação com esta frase:
"{req.query}"

Abaixo está o conteúdo do arquivo:
{conteudo[:2000]}

Esse conteúdo tem relação direta com a frase acima?
Responda 'Sim' ou 'Não' e justifique em uma linha.
"""
            resposta = gerar_resposta(prompt)
            if "sim" in resposta.lower():
                resultados.append(SearchResult(file_path=caminho, ia_response=resposta))
    return resultados

@app.post("/api/open")
async def open_file(file_path: str = Body(..., embed=True)):
    try:
        os.startfile(file_path)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend_main:app", host="0.0.0.0", port=8000, reload=True)
