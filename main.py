from fastapi import FastAPI, HTTPException
from pydantic import BaseMode
from typing import List
from datetime import datetime

app = FastAPI()
class Cliente(BaseModel):
    nome: str
    tipo_atendimento: str  # N para normal ou P para prioritario
    data_chegada: datetime
    atendido: bool = False

fila: List[Cliente] = []

@app.get("/fila", response_model=List[Cliente])
async def obter_fila():
    if not fila:
        return []
    return fila

@app.get("/fila/{id}", response_model=Cliente)
async def obter_cliente_por_id(id: int):
    if id < 0 or id >= len(fila):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return fila[id]

@app.post("/fila", response_model=Cliente)
async def adicionar_cliente(nome: str, tipo_atendimento: str):
    if len(nome) > 20:
        raise HTTPException(status_code=400, detail="O nome não pode ter mais de 20 caracteres.")
    if tipo_atendimento not in ['N', 'P']:
        raise HTTPException(status_code=400, detail="O tipo de atendimento deve ser 'N' ou 'P'.")
    
    cliente = Cliente(
        nome = nome,
        tipo_atendimento = tipo_atendimento,
        data_chegada = datetime.now(),
        atendido =  False
    )
    
    fila.append(cliente)
    
    fila.sort(key=lambda c: (c.tipo_atendimento != 'P', c.data_chegada))
    
    return cliente

@app.put("/fila")
async def atualizar_fila():
    if not fila:
        raise HTTPException(status_code=400, detail="Não há clientes na fila para atualizar.")

    for i in range(len(fila)):
        if fila[i].atendido:
            continue
        
        if i == 0:
            fila[i].atendido = True  
            fila[i] = fila[i]  
    
    return {"message": "Fila atualizada com sucesso."}

@app.delete("/fila/{id}")
async def remover_cliente(id: int):
    if id < 0 or id >= len(fila):
        raise HTTPException(status_code=404, detail="Cliente não encontrado na fila.")
    
    cliente_removido = fila.pop(id)
    
    for i in range(id, len(fila)):
        fila[i] = fila[i]
    
    return {"message": f"Cliente {cliente_removido.nome} removido da fila."}