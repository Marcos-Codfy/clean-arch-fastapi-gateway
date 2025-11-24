from src.core.interfaces import IpaymentRepository
from src.adapters.factory import PaymentStrategyFactory
from src.core.entities import Order, Payment

class ProcessPaymentUseCase:
    """
    Caso de Uso: O "cérebro" da operção
    Ele coordena a Fábrica, a Estratégia e o Repositório
    """
    def __init__(self, repository: IpaymentRepository):
        self.repository = repository
        #A fabrica pode ser instaciada aqui ou injetada via construtor
        self.factory = PaymentStrategyFactory()
    
    def execute(self, amount: float, method: str) -> dict:
        """
        Executa o fluxo completo de pagamento
        """
        # 1. Cria a entidade Pedido (Order)
        order = Order(amount=amount)
        
        # 2.Usa a Fábrica para descobrir qual estrátegia usar (Pix, Boleto, etc)
        strategy = self.factory.get_strategy(method)
        
        # 3. Executa a estrategia (Polimorfismo: ocodigo não sabe qual é, só manda processar)
        result = strategy.process_payment(order)
        
        #4. Cria a entidade Pagamento como o resultado
        payment = Payment(
         order_id=order.id,
            method=method,
            status=result["status"],
            transaction_id=result.get("transaction_id")   
        )
        
        # 5. Salva no banco de dados usando o repositorio
        self.repository.save(payment)
        
        #Retorna o resultado para quem chamou (API)
        return result
    