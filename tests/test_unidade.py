import pytest
from src.adapters.factory import PaymentStrategyFactory
from src.use_cases.payment_use_case import ProcessPaymentUseCase
# Repositório Falso para isolar o teste
from tests.fake_repository import FakePaymentRepository 
from src.adapters.strategies import PIxStrategy

# --- Unit Tests for Factory Pattern ---

def test_factory_creates_pix_strategy():
    """ Testo se a Fábrica cria a estratégia PIX correta. """
    factory = PaymentStrategyFactory()
    strategy = factory.get_strategy("pix")
    # Verifico se o objeto criado é uma instância da classe PIxStrategy
    assert isinstance(strategy, PIxStrategy)

def test_factory_raises_error_for_unknown_method():
    """ Testo se a Fábrica lança um erro se o método for inválido. """
    factory = PaymentStrategyFactory()
    with pytest.raises(ValueError):
        # Tenta criar um método que não existe
        factory.get_strategy("unknown_method")

# --- Unit Test for Use Case ---

def test_use_case_executes_and_saves_with_pix():
    """ 
    Testo se o Caso de Uso executa a estratégia e salva o resultado.
    (Usamos o Repositório Falso para este teste!) 
    """
    # 1. Configuração (Arrange)
    fake_repo = FakePaymentRepository()
    
    # Injeto a dependência (o Repositório Falso) no Caso de Uso
    use_case = ProcessPaymentUseCase(fake_repo)

    # 2. Ação (Act)
    result = use_case.execute(amount=100.0, method="pix")

    # 3. Verificação (Assert)
    # Verifico o resultado que o Caso de Uso devolveu
    assert result["status"] == "approved"
    
    # Verifico se o Repositório Falso realmente salvou o pagamento
    assert len(fake_repo.payments) == 1 
    # Acessa o primeiro pagamento salvo para verificar o método e status
    assert fake_repo.payments[0].method == "pix"
    assert fake_repo.payments[0].status == "approved"