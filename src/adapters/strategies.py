from typing import Dict
from src.core.interfaces import IpaymentStrategy
from src.core.entities import Order

class PixStrategy(IpaymentStrategy):
    def process_payment(self, order: Order) -> Dict[str, any]:
        # Operação simulada de registro
        print(f"Processing Pix payment for Order {order.id} - Amount R${order.amount:.2f}")
        
        #Simulação de integração de API bancária
        return {
            "status": "approved",
            "method": "pix",
            "transaction_id": f"pix_{order.id}_123"
        }
        
class CreditCardStrategy(IpaymentStrategy):
    def process_payment(self, order: Order) -> Dict[str, any]:
        print(f"Processing Credit Card payment for Order {order.id} of amount R${order.amount:.2f}")
        
        return {
            "status": "approved",
            "method": "credit_card",
            "transaction_id": f"card_{order.id}_456",
            "auth_code": "auth_xyz"
        }
        
class BoletoStrategy(IpaymentStrategy):
    def process_payment(self, order: Order) -> Dict[str, any]:
        print(f"Processing Boleto payment for Order {order.id} of amount R${order.amount:.2f}")
        
        return {
            "status": "pending",
            "method": "boleto",
            "transaction_id": f"boleto_{order.id}_789",
            "boleto_number": "23791.38628 60000.000008 12345.678901 2 34560000010000"
        }