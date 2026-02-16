from sqlalchemy.orm import Session
from Services.TransactionService import TransactionService

class TransactionController:
    def __init__(self):
        self.transaction_service = TransactionService()

    def handle_sync(self, account_id: str, db: Session):
        return self.transaction_service.sync_and_process_data(account_id, db)