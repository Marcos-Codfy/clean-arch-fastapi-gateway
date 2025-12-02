from src.core.interfaces import IpaymentStrategy
from src.adapters.strategies import PixStrategy, CreditCardStrategy, BoletoStrategy

class PaymentStrategyFactory:
    """
    Método de fábrica: Responsável por criar a instância de estratégia correta
    com base em uma string (por exemplo, 'pix').
    """
    
    @staticmethod
    def get_strategy(method: str) -> IpaymentStrategy:
        if method == 'pix':
            return PixStrategy()
        elif method == 'credit_card':
            return CreditCardStrategy()
        elif method == 'boleto':
            return BoletoStrategy()
        
        # Gera um erro se o método não existir.
        raise ValueError(f"Payment method '{method}' is not supported.")