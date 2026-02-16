from fastapi import FastAPI, HTTPException
from Services.PluggyService import PluggyService
from pydantic import BaseModel
from models.TokenResponse import TokenResponse
app = FastAPI()

service = PluggyService()

# ==========================
# 🏠 HOME
# ==========================
@app.get("/")
def home():
    return {"message": "API Financeira do Paulo está rodando!"}


# ==========================
# 🔗 CRIAR CONNECT TOKEN
# ==========================
@app.post("/create-connection", response_model=TokenResponse)
def create_connection_token():

    # 🔐 Garante autenticação
    if not service.api_key:
        auth_success = service.authenticate()
        if not auth_success:
            raise HTTPException(
                status_code=500,
                detail="Falha ao autenticar na Pluggy"
            )

    # 🔑 Agora passa client_user_id
    token = service.create_connect_token()

    if not token:
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar connect token"
        )

    return {"connectToken": token}


# ==========================
# 🏦 LISTAR CONTAS
# ==========================
@app.get("/accounts")
def get_accounts(itemId: str):

    # 🔐 Garante autenticação
    if not service.api_key:
        auth_success = service.authenticate()
        if not auth_success:
            raise HTTPException(
                status_code=500,
                detail="Falha ao autenticar na Pluggy"
            )

    accounts = service.get_accounts(itemId)

    if accounts is None:
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar contas"
        )

    if len(accounts) == 0:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma conta encontrada para esse item"
        )

    return {"accounts": accounts}

# ==========================
# 💳 LISTAR TRANSAÇÕES
# ==========================
@app.get("/transactions")
def get_transactions(account_id: str, page: int = 1, page_size: int = 500):

    # 🔐 Garante autenticação
    if not service.api_key:
        auth_success = service.authenticate()
        if not auth_success:
            raise HTTPException(
                status_code=500,
                detail="Falha ao autenticar na Pluggy"
            )

    transactions = service.get_transactions(account_id, page, page_size)

    if transactions is None:
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar transações"
        )

    return {"transactions": transactions}