from src.core.interfaces import IpaymentRepository
from src.adapters.factory import PaymentStrategyFactory
from src.core.entities import Order, Payment

class ProcessPaymentUseCase:
    """
    Caso de Uso: O "cérebro" da operação.
    Ele coordena a Fábrica, a Estratégia e o Repositório.
    Não tem dependência de FastAPI ou SQLAlchemy. É Lógica Pura!
    """
    def __init__(self, repository: IpaymentRepository):
        # Injeção de Dependência: Eu recebo o Repositório (memória) como um contrato (Interface)
        self.repository = repository
        
        # A Fábrica será usada para criar a estratégia correta
        self.factory = PaymentStrategyFactory()
    
    def execute(self, amount: float, method: str) -> dict:
        """
        Executa o fluxo completo de pagamento.
        """
        # 1. Crio a entidade Pedido (Order)
        order = Order(amount=amount)
        
        # 2. Uso a Fábrica para descobrir qual estratégia usar (Pix, Boleto, etc.)
        # Se o método for inválido, a fábrica lança o ValueError que a API vai capturar
        strategy = self.factory.get_strategy(method)
        
        # 3. Executo a estratégia (Polimorfismo: o código aqui não sabe se é Pix ou Cartão, só manda processar)
        result = strategy.process_payment(order)
        
        # 4. Crio a entidade Pagamento com o resultado
        payment = Payment(
            order_id=order.id,
            method=method,
            status=result["status"],
            transaction_id=result.get("transaction_id")   
        )
        
        # 5. Salvo no banco de dados usando o Repositório (que pode ser o real ou o falso)
        self.repository.save(payment)
        
        # Retorno o resultado para quem chamou (a API)
        return result