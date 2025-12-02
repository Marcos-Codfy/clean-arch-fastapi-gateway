from sqlalchemy import create_engine, Column, String, Table, MetaData
from sqlalchemy.orm import sessionmaker, registry
from src.core.interfaces import IpaymentRepository
from src.core.entities import Payment

# --- Configuração do SQLAlchemy ---
mapper_registry = registry()
metadata = MetaData()

# Tabela definida apenas com String
payment_table = Table(
 'pagamentos',
 metadata,
    Column('id', String(50), primary_key=True),
    Column('order_id', String(50)),
    Column('method', String(50)),
    Column('status', String(20)),
    Column('transaction_id', String(50), nullable=True),
)

try:
    mapper_registry.map_imperatively(Payment, payment_table)
except Exception:
    pass

class SqlAlchemyRepository(IpaymentRepository):
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)
        
    def save(self, payment: Payment) -> None:
        session = self.Session()
        try:
            session.add(payment)
            session.commit()
            print(f"Pagamento {payment.id} salvo no SQLite com sucesso!.")
        except Exception as e:
            session.rollback()
            print(f"❌ Erro ao salvar no banco: {e}")
            raise e
        finally:
            session.close()

def init_db():
    engine = create_engine('sqlite:///payments.db', echo=False)
    metadata.create_all(engine)
    return engine