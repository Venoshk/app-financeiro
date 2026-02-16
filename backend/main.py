from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from Services.PluggyService import PluggyService
from pydantic import BaseModel
from db.databese import Base, get_db, engine # Importando o engine correto
from Controller.TransactionsController import TransactionController
import models.Transaction as models

app = FastAPI()

# Inicializa as tabelas no Supabase usando o engine do db/databese.py
try:
    models.Base.metadata.create_all(bind=engine)
    print("✅ Tabelas verificadas/criadas no Supabase")
except Exception as e:
    print(f"❌ Erro ao criar tabelas: {e}")

service = PluggyService()
transaction_controller = TransactionController()

# Modelos Pydantic
class ItemRequest(BaseModel):
    account_id: str

class TokenResponse(BaseModel):
    connectToken: str

# ==========================
# 🏠 HOME
# ==========================
@app.get("/")
def home():
    return {"message": "API Financeira do Paulo está rodando!"}

# ==========================
# 🔄 SINCRONIZAR E PROCESSAR
# ==========================
@app.post("/transaction")
def sync_transactions_endpoint(request: ItemRequest, db: Session = Depends(get_db)):
    return transaction_controller.handle_sync(request.account_id, db)

# ==========================
# 🔗 CRIAR CONNECT TOKEN
# ==========================
@app.post("/create-connection", response_model=TokenResponse)
def create_connection_token():
    if not service.api_key:
        auth_success = service.authenticate()
        if not auth_success:
            raise HTTPException(status_code=500, detail="Falha ao autenticar na Pluggy")

    token = service.create_connect_token()

    if not token:
        raise HTTPException(status_code=500, detail="Erro ao gerar connect token")

    return {"connectToken": token}

# ==========================
# 🏦 LISTAR CONTAS (GET)
# ==========================
@app.get("/accounts")
def get_accounts(itemId: str):
    if not service.api_key:
        service.authenticate()

    accounts = service.get_accounts(itemId)

    if accounts is None:
        raise HTTPException(status_code=500, detail="Erro ao buscar contas")
    
    if len(accounts) == 0:
        raise HTTPException(status_code=404, detail="Nenhuma conta encontrada")

    return {"accounts": accounts}

# ==========================
# 💳 LISTAR TRANSAÇÕES (GET)
# ==========================
@app.get("/transactions")
def get_transactions_list(account_id: str, page: int = 1, page_size: int = 500):
    if not service.api_key:
        service.authenticate()

    transactions = service.get_transactions(account_id, page, page_size)

    if transactions is None:
        raise HTTPException(status_code=500, detail="Erro ao buscar transações")

    return {"transactions": transactions}