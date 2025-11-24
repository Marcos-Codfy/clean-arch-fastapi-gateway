from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Importamos nossas novas peças da arquitetura limpa
# o 'payment_use_case' é o cérebro e o 'repository' é a mémoria
from src.core.payment_use_case import ProcessPaymentUseCase
from src.adapters.repository import SqlAlchemyRepository, init_db

# -- Configuração inicial (Injeção de depêndencia) --

# 1. Inicializa o Banco de Dados (cria o arquivo .db se não existir)
db_engine = init_db()

# 2. Cria o repositório real (que sabe se comunicar com o SQL)
repository = SqlAlchemyRepository(db_engine)

# 3. Cria o  caso de uso e entrega o repositório para
# Agora o 'payment_use_case' tem tudo que precisa para funcionar
payment_use_case = ProcessPaymentUseCase(repository)

# -- Configuração da API FastAPI --
app = FastAPI(
    title="Gateway de Pagamentos - FastAPI",
    description="API com FastAPI, SQLAlchemy, Strategy Pattern e Factory Pattern",
    version="2.0.0"
)

# Modelo de dados que chega da internet (JSON)
class CheckoutRequest(BaseModel):
    amount: float
    method: str  # Ex: "pix", "boleto", "credit_card"
    
@app.post("/checkout")
def perfom_checkout(request: CheckoutRequest):
    """
    Endpoint principal
    Recebe a requisição e passa a bola para o "payment_use_case"
    """
    try:
        #A API não sabe a lógica de pagamento, Ela só chama o Caso de uso
        result = payment_use_case.execute(
            amount=request.amount,
            method=request.method
        )
        return {
            "message": "Pagamento processado com sucesso!",
            "payment_result": result
        }
    except ValueError as e:
        # Erro de validação (ex: método de pagamento inválido)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Erro génerico de servidor
        print(f"❌ Erro interno: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Gateway de Pagamentos com FastAPI!"}

