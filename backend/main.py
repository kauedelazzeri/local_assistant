# backend_main.py

"""
Backend para busca semântica local em arquivos .txt e .pdf usando modelo Ollama.
Expõe uma API via FastAPI para frontend interagir com suporte a stream.
"""

import os
import fitz  # PyMuPDF
import requests
from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Generator

app = FastAPI(title="InsightFinder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
EXTENSOES_SUPORTADAS = ['.txt', '.pdf']
PASTA_BUSCA = r"C:\Users\kaue\Downloads\Nova pasta"  # Altere aqui
EXTENSAO = ".txt"
OLLAMA_MODEL = "llama2"

class SearchRequest(BaseModel):
    query: str
    folder: str
    extensions: List[str]

class Resultado(BaseModel):
    caminho: str
    justificativa: str

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

def gerar_stream_resposta(prompt, modelo="llama2") -> Generator[str, None, None]:
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": modelo,
            "prompt": prompt,
            "stream": True
        }, stream=True)

        for line in response.iter_lines():
            if line:
                yield line.decode('utf-8') + "\n"
    except Exception as e:
        yield f"[Erro ao conectar ao Ollama: {e}]\n"

def gerar_resposta(prompt, modelo=OLLAMA_MODEL):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": modelo,
            "prompt": prompt,
            "stream": False
        })
        return response.json()['response'].strip()
    except Exception as e:
        return "Erro"

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
