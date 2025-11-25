from src.core.interfaces import IpaymentRepository
from src.core.entities import Payment
from typing import List

class FakePaymentRepository(IpaymentRepository):
    """
    Este é nosso Repositório Falso (Mock). 
    Ele implementa a mesma interface (contrato) do repositório SQL, 
    mas armazena os pagamentos em uma lista Python (em memória), 
    não tocando no banco de dados real. Perfeito para Testes de Unidade!
    """
    def __init__(self):
        # A lista onde guardamos os pagamentos de forma temporária.
        self.payments: List[Payment] = []
        
    def save(self, payment: Payment) :
        """
        Simula o salvamento no banco, apenas adicionando à lista.
        """
        self.payments.append(payment)
        print(f"Pagamento {payment.id} salvo no repositório falso.")