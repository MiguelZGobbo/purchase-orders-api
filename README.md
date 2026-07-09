# 📦 Purchase Orders API

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker)
![JWT](https://img.shields.io/badge/Auth-JWT-yellow)
![Tests](https://img.shields.io/badge/tests-17%20passed-green)

API REST para gerenciamento de **pedidos de compra** com autenticação **JWT**.  
Construída com **Flask** e **SQLAlchemy**, containerizada com **Docker** e documentada com **Swagger**.

---

## 📌 Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/users` | Cria um novo usuário |
| POST | `/login` | Autentica e retorna token JWT |
| GET | `/purchase_orders` | Lista todos os pedidos |
| POST | `/purchase_orders` | Cria um pedido |
| GET | `/purchase_orders/{id}` | Retorna pedido por ID |
| GET | `/purchase_orders/{id}/items` | Lista itens de um pedido |
| POST | `/purchase_orders/{id}/items` | Adiciona item a um pedido |
| GET | `/health` | Health check da API |
| GET | `/apidocs` | Documentação Swagger interativa |

---

## 📬 Exemplos

### Criar usuário

```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "123456"}'
```

```json
{
  "id": 1,
  "email": "admin@example.com"
}
```

### Autenticar

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "123456"}'
```

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Criar pedido

```bash
curl -X POST http://localhost:5000/purchase_orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{"description": "Materiais de escritório", "quantity": 100}'
```

```json
{
  "id": 1,
  "description": "Materiais de escritório",
  "quantity": 100
}
```

### Adicionar item ao pedido

```bash
curl -X POST http://localhost:5000/purchase_orders/1/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{"description": "Caneta azul", "price": 2.50, "quantity": 50}'
```

```json
{
  "id": 1,
  "description": "Caneta azul",
  "price": 2.5,
  "quantity": 50,
  "purchase_order_id": 1
}
```

---

## 🧱 Modelo

### PurchaseOrder

```json
{
  "id": 1,
  "description": "Materiais de escritório",
  "quantity": 100
}
```

### PurchaseOrderItem

```json
{
  "id": 1,
  "description": "Caneta azul",
  "price": 2.5,
  "quantity": 50,
  "purchase_order_id": 1
}
```

### User

```json
{
  "id": 1,
  "email": "admin@example.com"
}
```

---

## 🚀 Como executar

### Pré-requisitos
- Python 3.10+ ou Docker
- PostgreSQL (apenas para execução local)

### Com Docker (recomendado)

```bash
docker compose up --build
```

A aplicação estará disponível em **http://localhost:5000**.

### Local (sem Docker)

```bash
# 1. Clonar
git clone https://github.com/MiguelZGobbo/purchase-orders-api.git
cd purchase-orders-api

# 2. Ambiente virtual
python -m venv venv && source venv/bin/activate

# 3. Dependências
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Edite DB_URI com suas credenciais PostgreSQL

# 5. Executar
flask run
```

### Popular banco com dados de exemplo

```bash
make seed
```

---

## 🧪 Testes

```bash
pip install -r requirements/development.txt
pytest
```

---

## ⚙️ Comandos Make

| Comando | Descrição |
|---------|-----------|
| `make test` | Executa testes automatizados |
| `make lint` | Verifica código com Ruff |
| `make format` | Formata código com Ruff |
| `make seed` | Popula banco com dados de exemplo |
| `make docker-up` | Sobe a aplicação com Docker |
| `make docker-down` | Para os containers |
| `make clean` | Remove caches e arquivos temporários |

---

## 🛠️ Tecnologias

- **Python 3.11** — Linguagem principal
- **Flask 3.1** — Framework web
- **Flask-RESTful** — Construção de APIs REST
- **Flask-JWT-Extended** — Autenticação via JWT
- **Flask-SQLAlchemy** — ORM e banco de dados
- **Flask-Migrate / Alembic** — Migrações
- **Flask-CORS** — Cross-Origin Resource Sharing
- **Flasgger** — Documentação Swagger interativa
- **PostgreSQL 16** — Banco de dados relacional
- **Passlib** — Hashing de senhas
- **Docker / Docker Compose** — Containerização
- **Ruff** — Linter e formatador
- **Pre-commit** — Hooks de qualidade
- **Pytest** — Testes automatizados

---

## 📁 Estrutura do Projeto

```
purchase-orders-api/
│
├── exceptions/              # Exceções personalizadas
├── migrations/              # Migrações do banco (Alembic)
├── purchase_orders/         # Módulo de pedidos de compra
├── purchase_orders_items/   # Módulo de itens dos pedidos
├── requirements/            # Dependências organizadas
├── scripts/                 # Scripts utilitários (seed)
├── tests/                   # Testes automatizados
├── users/                   # Módulo de autenticação
│
├── .editorconfig            # Padrões de edição
├── .env.example             # Exemplo de variáveis de ambiente
├── .gitignore               # Arquivos ignorados pelo Git
├── .pre-commit-config.yaml  # Hooks de qualidade
├── Dockerfile               # Imagem Docker da aplicação
├── Makefile                 # Comandos auxiliares
├── README.md                # Documentação
├── app.py                   # Ponto de entrada da aplicação
├── db.py                    # Configuração do SQLAlchemy
├── docker-compose.yml       # Orquestração dos serviços
├── pyproject.toml           # Configuração do projeto
└── requirements.txt         # Dependências (atalho para production)
```

---

## 📬 Postman

[![Postman](https://img.shields.io/badge/Postman-Documentação-FF6C37?logo=postman)](https://documenter.getpostman.com/view/43058130/2sB3WtryNW)

---

## 👤 Autor

**MiguelZGobbo**  
[![GitHub](https://img.shields.io/badge/GitHub-MiguelZGobbo-181717?logo=github)](https://github.com/MiguelZGobbo)
