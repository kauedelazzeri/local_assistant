# InsightFinder — Busca Inteligente por Arquivos Locais

Uma aplicação local que permite buscar informações em linguagem natural dentro de arquivos do seu computador, funcionando como um "Copilot pessoal" para seus arquivos.

## 🚀 Funcionalidades

- Busca em linguagem natural
- Suporte a múltiplos formatos de arquivo (TXT, PDF, PPTX, XLSX, JPG, PNG)
- Processamento local com IA via Ollama
- Interface web amigável
- Privacidade total (tudo roda localmente)

## 📋 Pré-requisitos

- Python 3.8+
- Node.js 16+ (para o frontend)
- Ollama instalado e rodando localmente
- Tesseract OCR instalado (para processamento de imagens)

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/local_assistant.git
cd local_assistant
```
2. Crie e ative um ambiente virtual:
# Windows (cmd) ou PowerShell
```bash
python -m venv venv
venv\Scripts\activate
```
3. Instale as dependências do backend dentro do ambiente virutal:
```bash
cd backend
pip install -r requirements.txt
```
4. Instale as dependências do frontend em outro terminal:
```bash
cd frontend
npm install
```

## ⚙️ Como usar IA local com Ollama

1. Baixe e instale o [Ollama](https://ollama.com/download).
2. Após instalar, rode em outro terminal:
```bash
ollama run llama2
```
3. Para usar outro modelo, como `phi`, `mistral`, ou `llava`, execute:
```bash
ollama run nome-do-modelo
```
4. Para trocar o modelo padrão no código, edite o arquivo:
```bash
backend/main.py
```
E altere a linha:
```python
OLLAMA_MODEL = "llama2"
```

## 🚀 Executando

1. Ative o ambiente virtual (caso ainda não esteja ativo):
# Windows (cmd)
```bash
venv\Scripts\activate
```
2. Inicie o backend com FastAPI no ambiente virtual:
```python
cd backend
uvicorn main:app --reload
```

3. Em outro terminal, inicie o frontend:
```bash
cd frontend
npm start
```
4. Em outro terminal, inicie o servidor llama2:
```bash
ollama serve
```

4. Acesse a aplicação em `http://localhost:3000`, o node deve abrir automaticamente no navegador

## 📁 Estrutura do Projeto

```
insight-finder/
├── backend/
│   ├── main.py
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── requirements.txt
└── README.md
```

## 📂 Caminho padrão de busca

O projeto tenta automaticamente definir a pasta padrão de busca como a pasta de Downloads do sistema (Windows). O campo pode ser editado manualmente na interface.

## 🔒 Privacidade

- Todo o processamento é feito localmente
- Nenhum dado é enviado para a internet
- Os arquivos são indexados apenas nas pastas autorizadas

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
