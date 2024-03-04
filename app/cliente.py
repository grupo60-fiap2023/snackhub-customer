from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ClienteModel
from typing import List
import app.schemas as schemas

router = APIRouter()

@router.post("/cliente/",)
def criar_cliente(cliente: schemas.ClienteSchema, db: Session = Depends(get_db)):
    try:
        new_cliente = ClienteModel(**cliente.dict())
        db.add(new_cliente)
        db.commit()
        db.refresh(new_cliente)
        return {"message": "Pedido criado com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao registrar pedido: {e}")

# Endpoint para buscar clientes por lista de _id
@router.get("/clientes/", response_model=List[schemas.ClienteSchema])
def buscar_clientes_por_id(_id: List[int] = Query(...), db: Session = Depends(get_db)):
    return db.query(ClienteModel).filter(ClienteModel._id.in_(_id)).all()

# Endpoint para atualizar um cadastro
@router.put("/cliente/{_id}")
def atualizar_cliente(_id: int, cliente: schemas.ClienteSchema, db: Session = Depends(get_db)):
    cliente_db = db.query(ClienteModel).filter(ClienteModel._id == _id).first()
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
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