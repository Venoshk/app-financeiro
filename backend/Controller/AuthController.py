from Services.PluggyService import PluggyService

class AuthController:
    def __init__(self):
        # Injeção de dependência simples
        self.service = PluggyService()

    def handle_login(self):
        print("--- Iniciando Processo de Login ---")
        
        is_authenticated = self.service.authenticate()

        if is_authenticated:
            print("✅ SUCESSO: Conexão estabelecida.")
            print(f"🔑 Token gerado (Mascarado): {self.service.api_key[:10]}...")
        else:
            print("❌ ERRO: Não foi possível autenticar.")
            print("-> Verifique se o CLIENT_ID e CLIENT_SECRET no .env estão corretos.")