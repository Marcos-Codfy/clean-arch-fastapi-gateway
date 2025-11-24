import uuid
from datetime import datetime

class Order:
    """
    Representa um Pedido que precisa ser Pago
    Apenas Entidade pura, sem regras de negócio
    Ou bibliotecas externas
    """
    def __init__(self, amount: float):
            self.id = str(uuid.uuid4())
            self.amount = amount
            self.created_at = datetime.now()
        
class Payment:
    """
    Representa o resultado de um Pagamento Processado
    """
    def __init__(self, order_id: str, method: str,
                 status: str, transaction_id: str = None):
            self.id = str(uuid.uuid4())
            self.order_id = order_id
            self.method = method
            self.status = status
            self.transaction_id = transaction_id
            self.processed_at = datetime.now()