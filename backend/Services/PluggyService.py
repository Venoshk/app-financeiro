import os
import requests
from dotenv import load_dotenv

load_dotenv()

class PluggyService:
    def __init__(self):
        self.base_url = os.getenv('PLUGGY_URL', 'https://api.pluggy.ai')
        self.client_id = os.getenv('PLUGGY_CLIENT_ID') 
        self.client_secret = os.getenv('PLUGGY_CLIENT_SECRET')
        self.api_key = None

    # ==========================
    # 🔐 AUTHENTICATION
    # ==========================
    def authenticate(self) -> bool:
        """
        Tenta autenticar e guarda a apiKey.
        Retorna: True (Sucesso) ou False (Falha)
        """
        url = f"{self.base_url}/auth"

        payload = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status() 
            
            data = response.json()
            self.api_key = data.get("apiKey") 

            return True 
            
        except requests.exceptions.RequestException as e:
            print(f"[Service Log] Erro técnico na requisição: {e}")
            return False

    # ==========================
    # 🔑 HEADERS PADRÃO
    # ==========================
    def _get_headers(self):
        if not self.api_key:
            # Tenta autenticar se a chave sumiu da memória
            if not self.authenticate():
                raise Exception("Falha crítica: Não foi possível autenticar na Pluggy.")

        # A Pluggy prefere X-API-KEY para a maioria das rotas de dados
        return {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

    # ==========================
    # 🔗 CONNECT TOKEN (FRONTEND)
    # ==========================
    def create_connect_token(self) -> str:
        """
        Cria um token de conexão usando a apiKey.
        Retorna: O token de conexão ou None se falhar.
        """

        if not self.api_key:
            print("[Service Log] Erro: apiKey não disponível. Autentique primeiro.")
            return None

        url = f"{self.base_url}/connect_token"

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
             "clientUserId": os.getenv('CLIENT_USER_ID')
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status() 
            
            data = response.json()
            
            # --- CORREÇÃO AQUI ---
            # A Pluggy devolve "accessToken", não "connectToken"
            token = data.get("accessToken") 
            
            if token:
                print(f"✅ [Service] Connect Token gerado: {token}")
                return token
            else:
                print(f"⚠️ [Service] Token veio vazio. Resposta completa: {data}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ [Service] Erro ao criar Connect Token: {e}")
            if hasattr(response, 'text'): 
                 print(f"Detalhe do erro: {response.text}")
            return None
    
    def get_accounts(self, itemId: str):
        """
        Busca as contas conectadas de um Item.
        Retorna: Lista de contas ou None se falhar.
        """
        if not self.api_key:
            print("[Service Log] Erro: apiKey não disponível. Autentique primeiro.")
            return None

        url = f"{self.base_url}/accounts"

        params = {
            "itemId": itemId
        }

        try:
            response = requests.get(
                url, 
                headers=self._get_headers(), 
                params=params
            )
            response.raise_for_status() 
            
            data = response.json()
            accounts = data.get("results", [])
            
            print(f"✅ [Service] Contas obtidas para Item {itemId}: {accounts}")
            return accounts

        except requests.exceptions.RequestException as e:
            print(f"❌ [Service] Erro ao buscar contas para Item {itemId}: {e}")
            if hasattr(response, 'text'): 
                 print(f"Detalhe do erro: {response.text}")
            return None
    
    # ==========================
    # 💳 LISTAR TRANSAÇÕES
    # ==========================
    def get_transactions(self, account_id: str,
                         page: int = 1,
                         page_size: int = 500):
        """
        Retorna transações de uma conta específica.
        """
        url = f"{self.base_url}/transactions"

        params = {
            "accountId": account_id,
            "page": page,
            "pageSize": page_size
        }

        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params
            )
            response.raise_for_status()

            data = response.json()
            transactions = data.get("results", [])

            print(f"✅ {len(transactions)} transação(ões) encontrada(s).")
            return transactions

        except requests.RequestException as e:
            print(f"❌ Erro ao buscar transações: {e}")
            return None

            