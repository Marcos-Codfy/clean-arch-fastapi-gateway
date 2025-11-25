from fastapi.testclient import TestClient
# Agora importamos também o 'db_engine' para poder fechá-lo
from src.main import app, db_engine 
import pytest
import os 
from src.adapters.repository import init_db 

@pytest.fixture
def client():
    """ Fixture que cria um cliente de teste para a API e garante um banco limpo. """
    
    # 1. Cleanup Inicial
    # Forçamos o SQLAlchemy a fechar as conexões abertas pelo import do main.py
    # Isso libera o arquivo no Windows para podermos deletar.
    db_engine.dispose()
    
    # 2. Limpeza do Banco
    # Agora o remove deve funcionar porque o arquivo foi liberado
    if os.path.exists("payments.db"):
        try:
            os.remove("payments.db")
        except PermissionError:
            # Se ainda der erro (raro), avisamos, mas tentamos seguir
            print("Aviso: Não foi possível deletar o DB. Teste pode estar sujo.")
    
    # 3. Recria o banco do zero
    init_db() 
    
    # Crio um cliente de teste
    test_client = TestClient(app)
    
    yield test_client
    
    # Opcional: Limpar depois também, se quiser
    db_engine.dispose()

# --- Integration Tests with the API ---

def test_api_pay_with_card(client):
    """ Testa o fluxo completo: Requisição HTTP -> Caso de Uso -> Repositório SQL. """
    response = client.post('/pagar', json={"amount": 150.0, "method": "credit_card"})

    assert response.status_code == 200 
    json_response = response.json()
    assert json_response["status"] == "approved"
    assert "card_" in json_response["id_transacao"]

def test_api_invalid_method(client):
    """ Testa se a API captura o erro da Fábrica (ValueError) e devolve 400. """
    response = client.post('/pagar', json={"amount": 50.0, "method": "unknown_method"})
    
    assert response.status_code == 400 
    assert "Payment method 'unknown_method' is not supported." in response.json()["detail"]

def test_api_invalid_data_pydantic(client):
    """ Testa se o Pydantic (Camada Externa) rejeita dados mal formatados e devolve 422. """
    response = client.post('/pagar', json={"amount": "one_hundred_reais", "method": "pix"})
    
    assert response.status_code == 422