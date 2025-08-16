# 🚗 API de Carros – Flask + SQLAlchemy (equivalente ao NestJS)

API REST para **marcas**, **modelos** e **carros** com a mesma modelagem, regras e endpoints do projeto NestJS.  
Tecnologias: **Flask**, **SQLAlchemy**, **Flask-Migrate (Alembic)**, **Marshmallow**, **PostgreSQL**.

---

## 📂 Estrutura do Código

- **app/**
  - **modules/**
    - **cars/**
      - `modules.py` → Modelos do SQLAlchemy que representam a tabela de carros no banco.
      - `schemas.py` → Schemas do Marshmallow para validação/serialização de carros.
      - `routes.py` → Rotas REST relacionadas a carros (CRUD).
    - **models/**
      - `modules.py` ...
      - `schemas.py` ...
      - `routes.py` ...
    - **bands/**
      - `modules.py` ...
      - `schemas.py` ...
      - `routes.py` ...
  - **common/**
    - `dto.py` → DTO genérico para paginação.
- **docker**
  - `Dockerfile` e `docker-compose.yml` → Configuração para rodar app + banco via containers.
- **database/**
  - Scripts de migração do banco (criação de tabelas e seeds).

---

## ⚙️ Decisões de Implementação

- **Arquitetura modular** por domínio (`brands`, `models`, `cars`) com Blueprints.
- **Validação forte** (Marshmallow) + normalização de `combustivel` p/ UPPERCASE sem acento.
- **Busca genérica** (`cor`, `combustível`, `ano`, `portas`, `modelo`, `marca`) com `ILIKE` e `ESCAPE`.
- **Paginação** padrão com `page` e `limit` (máx 100).
- **Integridade no DB**: FKs, índices e CHECKs idênticos ao Nest.
- **Endpoint público**: `GET /models/public/cars.json`.

---

## 🔐 Segurança e Boas Práticas

- **Escapando parâmetros no LIKE** → evita SQL Injection nas pesquisas (`ESCAPE '\\'`).
- **Validação forte no DTO** → impede envio de dados inválidos antes do banco.
- **Tratamento de erros com Exceptions** → feedback claro ao cliente (404, 400, etc).
- **Constraints no banco** → mesmo que o app falhe em validar, o banco garante integridade.

---

## 🚀 Endpoints Principais

### Cars

- **POST** `/cars` → Criar carro
- **GET** `/cars` → Listar carros (com paginação e busca)
  - Parâmetros:
    - `limit` → quantidade por página
    - `page` → página desejada
    - `search` → texto ou número para busca genérica
    - `modelId` → filtra por modelo específico
- **GET** `/cars/:id` → Buscar carro por ID
- **PATCH** `/cars/:id` → Atualizar carro
- **DELETE** `/cars/:id` → Remover carro

---

## 🧪 Exemplos de Testes

### Criação de carro válida

```json
{
  "modelo_id": 1,
  "ano": 2020,
  "combustivel": "Gasolina",
  "num_portas": 4,
  "cor": "Preto"
}
```

## Como executar? 

## 📦 Pré-requisitos

Antes de começar, instale:

- [Docker](https://www.docker.com/products/docker-desktop)  
- [Docker Compose](https://docs.docker.com/compose/)  
- [Python 3.12](https://www.python.org/downloads/) _(apenas se quiser rodar fora do Docker)_

---

## ▶️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/GefersonLopes/WS-Work-API.git
cd WS-Work-API
docker compose up --build
