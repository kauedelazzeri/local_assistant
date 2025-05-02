# backend_main.py

"""
Backend para busca semântica local em arquivos .txt e .pdf usando modelo Ollama.
Interface via linha de comando por enquanto.
"""

import os
import fitz  # PyMuPDF
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
EXTENSOES_SUPORTADAS = ['.txt', '.pdf']


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


def gerar_resposta(prompt, modelo="phi"):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": modelo,
            "prompt": prompt,
            "stream": False
        })
        return response.json().get('response', '').strip()
    except Exception as e:
        print(f"[!] Erro na chamada ao Ollama: {e}")
        return "Erro"


def buscar_semanticamente(termo_busca, pasta_base, extensoes=EXTENSOES_SUPORTADAS):
    resultados = []
    total = 0
    processados = 0

    print(f"\n🔍 Buscando por: '{termo_busca}' em {pasta_base}\n")

    for root, _, files in os.walk(pasta_base):
        for arquivo in files:
            ext = os.path.splitext(arquivo)[1].lower()
            if ext not in extensoes:
                continue

            caminho = os.path.join(root, arquivo)
            total += 1
            print(f"📄 Lendo: {caminho}")
            conteudo = ler_arquivo(caminho)

            if not conteudo.strip():
                print("   ⚠️  Arquivo vazio ou ilegível.\n")
                continue

            if termo_busca.lower() in conteudo.lower():
                print("   ✅ Correspondência exata.\n")
                resultados.append((caminho, "Correspondência exata"))
                continue

            prompt = f"""
Estou procurando arquivos que tenham relação com esta frase:
"{termo_busca}"

Abaixo está o conteúdo do arquivo:
{conteudo[:2000]}

Esse conteúdo tem relação direta com a frase acima?
Responda 'Sim' ou 'Não' e justifique em uma linha.
"""
            resposta = gerar_resposta(prompt)
            print(f"   🤖 Resposta IA: {resposta}\n")
            if "sim" in resposta.lower():
                resultados.append((caminho, resposta))

            processados += 1

    print(f"\n📊 {processados} arquivos processados / {total} encontrados.\n")
    return resultados


if __name__ == "__main__":
    termo = input("🔎 Termo de busca: ").strip()
    pasta = input("📂 Pasta para busca (padrão: Downloads): ").strip() or os.path.expanduser("~/Downloads")
    print("Tipos permitidos: .txt, .pdf")
    tipos = input("Extensões separadas por vírgula (ex: .txt,.pdf): ").strip().split(',')

    resultados = buscar_semanticamente(termo, pasta, [t.strip().lower() for t in tipos if t.strip()])

    if resultados:
        print("✅ Resultados relevantes:\n")
        for path, justificativa in resultados:
            print(f"📂 {path}\n📝 {justificativa}\n")
    else:
        print("❌ Nenhum arquivo relevante encontrado.")
