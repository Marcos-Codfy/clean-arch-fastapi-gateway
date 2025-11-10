from strategies import IPaymentStrategy, PixStrategy, CreditCardStategy, BoletoStrategy

class PaymantStrategyFactory:
    """
    A Fábrica. Sua única responsabilidade é saber
    qual classe concreta (qual estratégia) criar.
    """
    
    def get_strategy(self, method: str) -> IPaymentStrategy:
        if method == "pix":
            return PixStrategy()
        elif method == "credit_card":
            return CreditCardStategy()
        elif method == "boleto":
            return BoletoStrategy()
        
        #Se um método desconhecido for solicitado, lançamos um erro.
        raise ValueError(f"Método de pagamento desconhecido: {method} não suportado.")
     