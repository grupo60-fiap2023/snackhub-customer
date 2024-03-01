from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Cliente
from typing import List

router = APIRouter()

@router.post("/cliente/", response_model=Cliente)
def criar_cliente(cliente: Cliente, db: Session = Depends(get_db)):
    try:
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return {"message": "Pedido criado com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao registrar pedido: {e}")

# Endpoint para buscar clientes por lista de _id
@router.get("/clientes/", response_model=List[Cliente])
def buscar_clientes_por_id(_id: List[int] = Query(...), db: Session = Depends(get_db)):
    return db.query(Cliente).filter(Cliente._id.in_(_id)).all()

# Endpoint para atualizar um cadastro
@router.put("/cliente/{_id}", response_model=Cliente)
def atualizar_cliente(_id: int, cliente: Cliente, db: Session = Depends(get_db)):
    cliente_db = db.query(Cliente).filter(Cliente._id == _id).first()
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    for key, value in cliente.dict().items():
        setattr(cliente_db, key, value)
    db.commit()
    db.refresh(cliente_db)
    return cliente_db

# Endpoint para atualizar todos os campos do _id selecionado para "Anonimo"
@router.put("/cliente/{_id}/anonimizar", response_model=Cliente)
def anonimizar_cliente(_id: int, db: Session = Depends(get_db)):
    cliente_db = db.query(Cliente).filter(Cliente._id == _id).first()
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    cliente_db.cpf = "Anonimo"
    cliente_db.nome = "Anonimo"
    cliente_db.endereco = "Anonimo"
    cliente_db.telefone = "Anonimo"
    db.commit()
    db.refresh(cliente_db)
    return cliente_db