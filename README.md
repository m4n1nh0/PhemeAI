# PhemeAI

PhemeAI é uma aplicação Python com FastAPI para detecção e verificação de fake news utilizando OpenSearch e modelos de linguagem.

## ⚙️ Funcionalidades

- Verificação de notícias com embeddings e similaridade vetorial.
- Indexação de novos documentos com campos como título, matéria, autor, link, jornal e flag `fake`.
- Utiliza `llama-cpp-python` para inferência local com modelos como `mistral-7b-instruct`.
- Integração com OpenSearch para busca vetorial com campos estruturados.
- Processamento com FastAPI, totalmente containerizado com Docker.

---

## 🧱 Estrutura do Projeto

```
PhemeAI/ 
├── app/ 
│   ├── main.py # Entrada principal da aplicação 
│   ├── models/ # Definições de dados (Pydantic) 
│   ├── routes/ # Rotas da API 
│   ├── services/ # Lógica de OpenSearch e embeddings 
│   ├── Dockerfile # Dockerfile para containerização 
├── docker-compose.yml # Docker Compose com serviços da app + OpenSearch 
├── requirements.txt # Dependências do projeto 
└── README.md
```
---

## 🚀 Como executar

### 1. Pré-requisitos

- Docker + Docker Compose
- Arquitetura compatível com `llama-cpp` (x86_64 com AVX2 preferencial)

### 2. Configuração

Clone o projeto:

```bash
git clone https://github.com/m4n1nh0/PhemeAI.git
cd PhemeAI
Crie o modelo .gguf no diretório models/ ou configure o caminho.
```
### 3. Execute com Docker Compose
```bash
docker compose up --build
```
A aplicação ficará disponível em: http://localhost:8000/docs

## 🔍 Endpoints principais

Método	Rota	Descrição

POST	/verificar_noticia	Verifica se a notícia é fake

POST	/indexar	Indexa uma nova matéria no índice

## 📦 Tecnologias
FastAPI

OpenSearch

Llama-cpp-python (GGUF model inference)

Docker

## 🧠 Autoria
Projeto inspirado em ThemisAI, adaptado para uso vetorial com OpenSearch, mantendo o foco na verificação automática de fatos em notícias.