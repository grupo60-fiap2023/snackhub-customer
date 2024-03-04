from pydantic import BaseModel
from typing import List

class ClienteSchema(BaseModel):
    _id: int = 0
    cpf: str = "None"
    nome: str = "None"
    endereco: str = "None"
    telefone: str = "None"

class ClienteRequest(BaseModel):
    _id : List[int]
    