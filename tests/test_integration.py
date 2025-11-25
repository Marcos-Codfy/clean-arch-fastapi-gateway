from fastapi.testclient import TestClient
from src.main import app # Importo a nossa aplicação FastAPI
import pytest
import os 
from src.adapters.repository import init_db 

@pytest.fixture
def client():
    """ Fixture que cria um cliente de teste para a API e garante um banco limpo. """
    # Crio um cliente de teste que simula um navegador ou outra aplicação
    test_client = TestClient(app)
    
    # Limpo o banco de dados antes dos testes para garantir que sempre começa 'limpo'
    # Em um projeto real, você usaria um banco de dados de teste separado!
    if os.path.exists("payments.db"):
        os.remove("payments.db")
    init_db() # Inicializa o banco (cria o arquivo .db vazio)
    
    # Retorna o cliente para ser usado pelos testes
    yield test_client

# --- Integration Tests with the API ---

def test_api_pay_with_card(client):
    """ Testa o fluxo completo: Requisição HTTP -> Caso de Uso -> Repositório SQL. """
    
    # 1. Ação (Act): O TestClient faz a chamada HTTP POST para /pagar
    response = client.post('/pagar', json={"amount": 150.0, "method": "credit_card"})

    # 2. Verificação (Assert)
    assert response.status_code == 200 # A API respondeu OK?
    json_response = response.json()
    assert json_response["status"] == "approved"
    assert "card_" in json_response["id_transacao"] # A transação de Cartão foi criada?

def test_api_invalid_method(client):
    """ Testa se a API captura o erro da Fábrica (ValueError) e devolve 400. """
    
    response = client.post('/pagar', json={"amount": 50.0, "method": "unknown_method"})
    
    assert response.status_code == 400 # Verifico se a API deu o erro correto (Bad Request)
    assert "Payment method 'unknown_method' is not supported." in response.json()["detail"]

def test_api_invalid_data_pydantic(client):
    """ Testa se o Pydantic (Camada Externa) rejeita dados mal formatados e devolve 422. """
    
    # O Pydantic deve falhar aqui, pois "amount" não é um float
    response = client.post('/pagar', json={"amount": "one_hundred_reais", "method": "pix"})
    
    assert response.status_code == 422 # Erro de validação do Pydantic (Unprocessable Entity)