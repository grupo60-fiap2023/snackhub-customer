from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP

class Cliente(Base):
    __tablename__ = 'clientes'
    _id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, unique=True, index=True)
    nome = Column(String)
    endereco = Column(String)
    telefone = Column(String)