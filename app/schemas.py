from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.sql import func


class ClienteSchema(BaseModel):
    _id: int = 0
    cpf: str = "None"
    nome: str = "None"
    endereco: str = "None"
    telefone: str = "None"
    