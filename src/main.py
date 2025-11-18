from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from factory import PaymantStrategyFactory
from context import PaymentContext

#1. Crie a aplicação FastAPI
app = FastAPI(
    title="API de Gateway de Pagamentos",
    description="Um Projeto de POO com Padrões Strategy e Factory Method",
    version="1.0.0"
)

#2. Crie a instância da nossa Fábrica
#(Pode ser global, pois não guarda estado)
factory = PaymantStrategyFactory()

#3. Defina o "Model (o que a API espera receber no corpo da requisição)"
class CheckoutRequest(BaseModel):
    amount: float
    method: str  # "pix", "credit_card", "boleto"



# 4.  Crie o COntroller (o endpoint da API)
@app.post("/checkout")
def perfom_checkout(request: CheckoutRequest):
    """
    Recebe um pedido de checkout, seleciona a estratégia de
    pagamento e executa a transação.
    """
    
    try:
        #5. A API (Controller) pede à Fábrica a estratégia 
        # <--- CORRIGIDO AQUI (era request.payment_method)
        strategy = factory.get_strategy(request.method) 
        
        #6. A API (O Controller) cria o Contexto com a estratégia escolhida
        context = PaymentContext(strategy)
        
        #7. A API (COntroler) manda o CONtexto executar
        result = context.execute_payment(request.amount)
        
        return result
    
    except ValueError as e:
        #Se a fábrica lançar um erro (Método não suportado)
        raise HTTPException(status_code=400, detail=str(e))