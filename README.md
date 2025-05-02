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

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## 🚀 Executando

1. Inicie o backend:
```bash
python backend/main.py
```

2. Em outro terminal, inicie o frontend:
```bash
cd frontend
npm run dev
```

3. Acesse a aplicação em `http://localhost:3000`

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

## 🔒 Privacidade

- Toda a processamento é feito localmente
- Nenhum dado é enviado para a internet
- Os arquivos são indexados apenas nas pastas autorizadas

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.