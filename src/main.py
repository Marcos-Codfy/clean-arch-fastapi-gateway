from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Importamos nossas novas peças da arquitetura limpa
# O Caso de Uso é o cérebro e o Repositório é a memória.
# Corrigimos o caminho da importação para 'use_cases'
from src.use_cases.payment_use_case import ProcessPaymentUseCase
from src.adapters.repository import SqlAlchemyRepository, init_db

# --- Configuração inicial (Injeção de dependência) ---

# 1. Inicializo o Banco de Dados (cria o arquivo .db se não existir)
db_engine = init_db()

# 2. Crio o repositório real (que sabe falar com o SQL)
repository = SqlAlchemyRepository(db_engine)

# 3. Crio o Caso de Uso e entrego o repositório para ele. 
# Agora o ProcessPaymentUseCase tem tudo que precisa para funcionar de forma independente.
payment_use_case = ProcessPaymentUseCase(repository)

# --- Configuração da API FastAPI ---
app = FastAPI(
    title="Gateway de Pagamentos - FastAPI",
    description="API com Clean Architecture, Strategy Pattern e Factory Pattern",
    version="2.0.0"
)

# Modelo de dados que chega da internet (JSON), validado automaticamente pelo Pydantic
class CheckoutRequest(BaseModel):
    # O valor que o cliente quer pagar
    amount: float
    # O método que ele escolheu: "pix", "boleto", "credit_card"
    method: str 
    
@app.post("/pagar") # Mudei o endpoint de /checkout para /pagar, conforme o plano
def perform_checkout(request: CheckoutRequest):
    """
    Endpoint principal.
    Recebe a requisição e passa a bola para o Caso de Uso.
    """
    try:
        # A API não sabe a lógica de pagamento, ela só chama o 'cérebro'
        result = payment_use_case.execute(
            amount=request.amount,
            method=request.method
        )
        return {
            "status": result["status"],
            "id_transacao": result["transaction_id"]
        }
    except ValueError as e:
        # Se der erro na Fábrica (ex: método de pagamento inválido), devolvo 400
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Erro genérico de servidor
        print(f"❌ Erro interno: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@app.get("/")
def read_root():
    # Este é o endpoint que você acabou de ver funcionando!
    return {"message": "Bem-vindo ao Gateway de Pagamentos com FastAPI!"}