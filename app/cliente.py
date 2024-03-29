from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ClienteModel
from typing import List
import app.schemas as schemas
from pydantic import BaseModel


class ItemModel(BaseModel):
    id: List[int]

router = APIRouter()

@router.post("/cliente/",)
def criar_cliente(cliente: schemas.ClienteSchema, db: Session = Depends(get_db)):
    try:
        new_cliente = ClienteModel(**cliente.dict())
        db.add(new_cliente)
        db.commit()
        db.refresh(new_cliente)
        return {"message": "Cliente criado com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao registrar Cliente: {e}")

# Endpoint para buscar clientes por lista de _id
@router.get("/cliente/")
def buscar_clientes_por_id(item: ItemModel, db: Session = Depends(get_db)):
    return db.query(ClienteModel).filter(ClienteModel._id.in_(item.id)).all()

# Endpoint para atualizar um cadastro
@router.put("/cliente/{_id}")
def atualizar_cliente(_id: int, cliente: schemas.ClienteSchema, db: Session = Depends(get_db)):
    cliente_db = db.query(ClienteModel).filter(ClienteModel._id == _id).first()
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    if cliente_db.cpf == "Anonimo":
        raise HTTPException(status_code=401, detail="Cliente anonimizado")
    for key, value in cliente.dict().items():
        setattr(cliente_db, key, value)
    db.commit()
    db.refresh(cliente_db)
    return cliente_db

# Endpoint para atualizar todos os campos do _id selecionado para "Anonimo"
@router.put("/cliente/{_id}/anonimizar")
def anonimizar_cliente(_id: int, db: Session = Depends(get_db)):
    cliente_db = db.query(ClienteModel).filter(ClienteModel._id == _id).first()
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    cliente_db.cpf = "Anonimo"
    cliente_db.nome = "Anonimo"
    cliente_db.endereco = "Anonimo"
    cliente_db.telefone = "Anonimo"
    db.commit()
    db.refresh(cliente_db)
    return cliente_db