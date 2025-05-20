# InsightFinder — Busca Inteligente por Arquivos Locais

Uma aplicação local que permite buscar informações em linguagem natural dentro de arquivos do seu computador, funcionando como um "Copilot pessoal" para seus arquivos.

## 📸 Interface da Aplicação

A InsightFinder oferece uma interface web intuitiva e moderna para realizar buscas inteligentes em seus arquivos locais. Veja como ela funciona:

### Página Inicial
![Página Inicial](images/2025-05-03%2017_36_50-.png)
*A interface inicial permite inserir o termo de busca, selecionar a pasta e escolher os tipos de arquivo a serem pesquisados.*

### Resultados da Busca
![Resultados Iniciais](images/2025-05-03%2017_57_02-.png)
*Após iniciar a busca, a aplicação mostra os resultados em tempo real, com a IA (Llama2) analisando cada arquivo e indicando sua relevância para o termo pesquisado.*

### Busca Avançada
![Busca Avançada](images/2025-05-03%2017_57_09-.png)
*Conforme a busca progride, mais arquivos são analisados e exibidos, permitindo uma visão completa dos documentos relevantes encontrados em seu sistema.*

A interface foi projetada para ser simples e eficiente, com:
- Campo de busca em linguagem natural
- Seleção de pasta personalizada
- Filtros por tipo de arquivo
- Resultados em tempo real
- Indicadores visuais de relevância
- Botão para abrir arquivos diretamente
- Justificativas detalhadas da IA para cada resultado

## 🚀 Funcionalidades

- Busca em linguagem natural
- Suporte a múltiplos formatos de arquivo (TXT, PDF)
    - PPTX, XLSX, JPG, PNG em breve
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
npm run start
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
│   ├── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── images/
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
