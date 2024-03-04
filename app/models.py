from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP

class ClienteModel(Base):
    __tablename__ = 'clientes'
    _id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String(14), unique=True, index=True)
    nome = Column(String(255))
    endereco = Column(String(255))
    telefone = Column(String(20))