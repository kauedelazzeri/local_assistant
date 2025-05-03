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
git clone https://github.com/seu-usuario/insight-finder.git
cd insight-finder
```

2. Instale as dependências do backend:
```bash
pip install -r requirements.txt
```

3. Instale as dependências do frontend:
```bash
cd frontend
npm install
```

## ⚙️ Como usar IA local com Ollama

1. Baixe e instale o [Ollama](https://ollama.com/download).
2. Após instalar, rode no terminal:
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

1. Inicie o backend:
```bash
python backend/main.py
```

2. Em outro terminal, inicie o frontend:
```bash
cd frontend
npm start
```
2. Em outro terminal, inicie o servidor llama2:
```bash
ollama serve
```

4. Acesse a aplicação em `http://localhost:3000`

## 📁 Estrutura do Projeto

```
insight-finder/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── services/
│   └── utils/
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
