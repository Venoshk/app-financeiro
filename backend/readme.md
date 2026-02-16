# 💰 Financeiro Pro - Backend (Python)

Este é o serviço de backend responsável pela integração com a API da Pluggy através do protocolo Open Finance. O sistema gerencia a autenticação, geração de tokens de conexão para o frontend (React Native) e a recuperação de dados bancários (contas e transações) de instituições como o Nubank.

## 🚀 Tecnologias Utilizadas

- **Python 3.10+** — Linguagem base para o desenvolvimento
- **FastAPI** — Framework web de alta performance para a criação das rotas
- **Uvicorn** — Servidor ASGI para rodar a aplicação em tempo real
- **Requests** — Biblioteca para consumo da API REST da Pluggy
- **Pydantic** — Validação de dados e criação de schemas (Data Models)
- **Python-dotenv** — Gerenciamento de variáveis de ambiente e segurança

## 📋 Pré-requisitos

Antes de iniciar, você precisará configurar suas credenciais. Crie um arquivo `.env` na raiz da pasta `backend/` seguindo o modelo:

```env
PLUGGY_CLIENT_ID=seu_client_id_aqui
PLUGGY_CLIENT_SECRET=seu_client_secret_aqui
PLUGGY_URL=https://api.pluggy.ai
```

## 🔧 Instalação e Execução

### 1. Crie e ative o ambiente virtual

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\Activate
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Instale as dependências

```bash
pip install fastapi uvicorn requests python-dotenv pydantic
```

### 3. Inicie o servidor para desenvolvimento

```bash
# Permite acesso externo 
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📂 Estrutura do Projeto

```
backend/
├── Controller/
│   └── AuthController.py         # Controlador de autenticação
├── Services/
│   └── PluggyService.py          # Classe com a lógica de negócio e integração
├── .env                          # Chaves de acesso (Ignorado pelo Git)
├── .gitignore                    # Filtro de arquivos para o repositório
├── main.py                       # Definição das rotas e controllers (FastAPI)
├── requirements.txt              # Dependências do projeto
└── README.md                     # Documentação do projeto
```

## 🛣️ Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/create-connection` | Gera o token temporário para abrir o Widget no Mobile |
| `GET` | `/accounts` | Lista todas as contas (corrente, crédito) vinculadas a um itemId |
| `POST` | `/sync-transactions` | Sincroniza dados e calcula o total de gastos do cartão |

## 🛠️ Roadmap de Desenvolvimento

- [x] Integração base com API Pluggy
- [x] Fluxo de autenticação e geração de Connect Token
- [ ] Persistência de dados com Supabase (PostgreSQL)
- [ ] Filtros avançados de gastos por categoria e porcentagem

---

Desenvolvido por **Paulo Henrique (Venoshk)** — Full Stack Developer | Java & Python Enthusiast