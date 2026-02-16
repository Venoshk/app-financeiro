from sqlalchemy.orm import Session
import models.Transaction as models
import pandas as pd
from fastapi import HTTPException
from Services.PluggyService import PluggyService

class TransactionService:
    def __init__(self):
        self.pluggy_service = PluggyService()

    def sync_and_process_data(self, account_id: str, db: Session):
        # 1. Busca os dados brutos através da PluggyService
        transactions_data = self.pluggy_service.get_transactions(account_id)

        if not transactions_data:
            raise HTTPException(
                status_code=404, 
                detail="Não foram encontradas transações para o item especificado."
            )
        
        new_records = 0

        # 2. Loop de Persistência com Upsert
        for t in transactions_data:
            # Verificamos se a transação já existe pelo ID externo da Pluggy
            existing = db.query(models.Transaction).filter(
                models.Transaction.external_id == t['id']
            ).first()

            if not existing:
                db_transaction = models.Transaction(
                    external_id=t['id'],
                    description=t['description'],
                    amount=t['amount'],
                    category=t['category'],
                    date=t['date'],
                    type=t['type'],
                    item_id=account_id
                )
                db.add(db_transaction)
                new_records += 1
                
        db.commit()
        print(f"✅ Processamento concluído. {new_records} novas transações adicionadas. Total processado: {len(transactions_data)}")
        # 3. Lógica de Negócio para o Gráfico (Pandas)
        df = pd.DataFrame(transactions_data)
        
        # Filtramos apenas débitos e ignoramos transferências entre suas próprias contas
        # conforme vimos no seu JSON (Same person transfer)
        df_gastos = df[(df['amount'] < 0) & (df['category'] != 'Same person transfer')]
        
        # Agrupamos por categoria e pegamos o valor absoluto para o gráfico
        resumo_grafico = df_gastos.groupby('category')['amount'].sum().abs().to_dict()

        return {
            "novos_registros": new_records,
            "total_processado": len(transactions_data),
            "grafico_dados": resumo_grafico,
            "total_gasto_real": sum(resumo_grafico.values())
        }