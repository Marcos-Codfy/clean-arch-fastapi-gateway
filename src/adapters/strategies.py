from abc import ABC, abstractmethod
#------------------
#Etapa 1: Definir a interface Strategy
#------------------

class IPaymentStrategy(ABC):
    """
    A Interface (Contrato) para todas as estratégias de pagamento.
    Ela obriga todas as classes que herdarem dela a ter um método 'process_payment'.
    """
    @abstractmethod
    def process_payment(self, amount: float) -> dict:
        """
        Processa um pagamento de um determinado valor.
        Retorna um dicionário com os detalhes da transação.
        """
        pass
    
#------------------
#Etapa 2: Implementar estratégias concretas
#------------------

class PixStrategy(IPaymentStrategy):
    ## A implementação (estratégia concreta) para pagamentos via Pix.
    def process_payment(self, amount):
        print(f"Iniciando pagamento via Pix de R${amount:.2f}")
        # --- SIMULAÇÃO ---
        # Aqui entraria a lógica real de se conectar a um gateway
        # (ex: Gerencianet), gerar o QR Code, etc.
        print("Pagamento via Pix Concluído com sucesso")
        return {
            "status": "sucess",
            "method": "pix",
            "transaction_id": "simulacao-qr-code-123456"
        }


class CreditCardStategy(IPaymentStrategy):
    
        """
        A implementação (estratégia concreta) para pagamentos via Cartão.
        """   
        def process_payment(self, amount):
            print(f"Iniciando pagamento com Cartão de Crédito de R${amount:.2f}")
            # --- SIMULAÇÃO ---
            # Aqui entraria a lógica real de se conectar a um gateway
            # (ex: Stripe), enviar os dados do cartão, etc.
            print("Pagamento com o Cartão Concluído com sucesso")
            return {
                "status": "sucess",
                "method": "credit_card",
                "auth_code": "simulacao_auth-78910"
            }
            

class BoletoStrategy(IPaymentStrategy):
    def process_payment(self, amount):
        print(f"Iniciando pagamento via Boleto de R${amount:.2f}")
        # --- SIMULAÇÃO ---
        # Aqui entraria a lógica real de se conectar a um gateway
        # (ex: Gerencianet), gerar o boleto, etc.
        print("Pagamento via Boleto Gerado com sucesso")
        return {
            "status": "sucess",
            "method": "boleto",
            "boleto_number": "simulacao-boleto-654321"
        }
        
        