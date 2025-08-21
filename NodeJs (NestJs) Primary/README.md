# 🚗 API de Carros - NestJS + TypeORM

Este projeto implementa uma API REST para gerenciamento de carros, modelos e marcas, utilizando **NestJS**, **TypeORM** e **PostgreSQL**.  
O foco principal é manter uma arquitetura limpa, testável e organizada, além de boas práticas de segurança e validação.

---

## 📂 Estrutura do Código

- **src/**
  - **modules/**
    - **cars/**
      - `cars.controller.ts` → Define os endpoints da API relacionados a carros.
      - `cars.service.ts` → Contém a lógica de negócio (CRUD, filtros, paginação).
      - **dto/** → Objetos de transferência de dados (validação de entrada).
      - **entities/** → Entidades do TypeORM mapeando tabelas do banco.
    - **models/** → Estrutura relacionada a modelos de carro.
    - **brands/** → Estrutura relacionada a marcas.
  - **common/**
    - `pagination.dto.ts` → DTO genérico para paginação.
- **docker/**
  - `Dockerfile` e `docker-compose.yml` → Configuração para rodar app + banco via containers.
- **migrations/**  
  - Scripts de migração do banco (criação de tabelas e seeds).

---

## ⚙️ Decisões de Implementação

- **NestJS + TypeORM**: escolhidos pela robustez, tipagem forte e facilidade de trabalhar com relações.
- **DTOs + ValidationPipe**: garante que entradas inválidas não alcancem a camada de serviço.
- **Repository Pattern**: uso do `@InjectRepository` para melhor desacoplamento e testabilidade.
- **Paginação Padrão**: evita sobrecarga de consultas grandes, limitando itens por página.
- **QueryBuilder para busca**: flexível e seguro, permite pesquisa em múltiplos campos (`cor`, `combustível`, `ano`, `número de portas`, `nome do modelo`, `marca`).
- **Constraints no banco (CHECK, FK)**: asseguram integridade dos dados (ex.: combustível válido).

---

## 🔐 Segurança e Boas Práticas

- **Escapando parâmetros no LIKE** → evita SQL Injection nas pesquisas (`ESCAPE '\\'`).
- **Validação forte no DTO** → impede envio de dados inválidos antes do banco.
- **Tratamento de erros com Exceptions do NestJS** → feedback claro ao cliente (404, 400, etc).
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

Antes de começar, instale:

- [Docker](https://www.docker.com/products/docker-desktop)  
- [Docker Compose](https://docs.docker.com/compose/)  
- [NodeJS](https://nodejs.org/pt) _(apenas se quiser rodar fora do Docker)_

---

## ▶️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/GefersonLopes/WS-Work-API.git
cd WS-Work-API
cd NodeJs\ \(NestJs\)\ Primary/
docker compose up --build
```
### 3. Abra o link:

[Aplicação Back-End](http://localhost:3000) 