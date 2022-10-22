from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
from pydantic import BaseModel
import secrets

class User(BaseModel):
    id: int
    nome:str
    email: str
    senha: str
    

app = FastAPI(title='SELECT MOVIE API', version='1.0.0', description='API para troca de mensagens entre os usuários do sistema')
security = HTTPBasic()

usuario_permitido = User(id=0, nome='Matheus Almeida', email='matheus@gmail.com', senha='1234')

def get_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    usuarios = [usuario_permitido]
    for usuario in usuarios:
        email_correto = secrets.compare_digest(credentials.username, usuario.email)
        senha_correta = secrets.compare_digest(credentials.password, usuario.senha)
        if email_correto and senha_correta:
            return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='not authorized', 
            headers={'WW-Authenticate': 'Basic'})

@app.get("/mensagem/",
         tags=['TG'],
         dependencies=[Depends(get_usuario)])
async def receber_mensagem():
    return {"dados":"not found"}

@app.post("/mensagem/",
         tags=['TG'],
         dependencies=[Depends(get_usuario)])
async def enviar_mensagem():
    return {"dados":"message oky"}