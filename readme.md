# 📦 Purchase Orders API

API REST desenvolvida em **Python** com **Flask**, projetada para gerenciar **pedidos de compra** e realizar autenticação de usuários utilizando **JWT (JSON Web Token)**.  
Projeto criado como estudo prático sobre desenvolvimento de APIs com Flask e boas práticas de autenticação e persistência de dados.

---

## Tecnologias Utilizadas

- Python 3  
- Flask  
- Flask-RESTful  
- Flask-JWT-Extended  
- MySQL (padrão, mas compatível com outros bancos via SQLAlchemy)  
- SQLAlchemy  
- python-dotenv  
- Postman

---

## Como Executar o Projeto

### Pré-requisitos
- Python 3 instalado  
- MySQL (ou outro banco SQL compatível)  
- Arquivo `.env` configurado (baseado em `.env.example`)

### Passos para execução

1. Clonar o repositório  
   `git clone https://github.com/MiguelZGobbo/python-course-first-API.git`

2. Acessar o diretório do projeto  
   `cd python-course-first-API`

3. (Opcional) Criar e ativar um ambiente virtual  
   - Windows: `python -m venv venv && venv\Scripts\activate`  
   - Linux/Mac: `python3 -m venv venv && source venv/bin/activate`

4. Instalar as dependências  
   `pip install -r requirements.txt`

5. Criar o arquivo `.env` a partir do exemplo  
   `cp .env.example .env`

6. Executar a aplicação  
   `flask run`

A aplicação será iniciada por padrão em:  
**http://localhost:5000**

---

## Endpoints Principais

| Método | Endpoint | Descrição |
|:------:|:--------:|:---------|
| POST   | `/login`                      | Autentica um usuário e retorna um token JWT |
| GET    | `/purchase_orders`            | Retorna todos os pedidos de compra |
| GET    | `/purchase_orders/{id}`       | Retorna um pedido de compra específico |
| GET    | `/purchase_orders/{id}/items` | Retorna todos os itens vinculados a um pedido de compra |

---

## Documentação Completa

A documentação detalhada dos endpoints está disponível no Postman:  
[Visualizar Documentação da API](https://documenter.getpostman.com/view/43058130/2sB3WtryNW)

---

## Estrutura do Projeto

```bash
python-course-first-API/
│
├── app.py                # Ponto de entrada principal
├── models/               # Modelos de dados (ORM)
├── routes/               # Definição de endpoints
├── database/             # Configuração do banco e inicialização
├── .env.example          # Exemplo de variáveis de ambiente
├── requirements.txt      # Dependências
└── README.md             # Documentação do projeto

---

## Autenticação

A API utiliza **JWT (JSON Web Token)**.  
Após o login bem-sucedido, um token é retornado e deve ser incluído no cabeçalho das requisições protegidas:

```bash
Authorization: Bearer <seu_token_jwt>
