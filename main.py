from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_utils.tasks import repeat_every 
import secrets
from sqlalchemy.orm import Session
from database import crud, models, schemas
from database.database import SessionLocal, engine
from datetime import time
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText


class UserPassword(BaseModel):
    email: str
    senha_temporaria: str


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title='SELECT MOVIE API', version='1.0.0', description='API para troca de mensagens entre os usuários do sistema')
security = HTTPBasic()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    email_correto = secrets.compare_digest(credentials.username, 'selectmovieapi')
    senha_correta = secrets.compare_digest(credentials.password, 's1e2l3e4c5t6m7o8v9i0e')
    if email_correto and senha_correta:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='not authorized', 
            headers={'WWW-Authenticate': 'Basic'})


@app.get("/", tags=['Início'])
def index():
    return {
        "Documentação Swagger": "https://selectmovietg.herokuapp.com/docs#",
        "Documentação ReDoc": "https://selectmovietg.herokuapp.com/redoc"
    }


@app.post("/email/",
          tags=['E-mail'],
          dependencies=[Depends(get_credentials)])
def send_email_password(user: UserPassword):
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    username = ''
    password = '' 
    from_addr = user.email
    to_addrs = [user.email]
    senha = user.senha_temporaria
    message = MIMEText(f'Sua senha temporária é {senha}')
    message['subject'] = 'Aplicativo SM'
    message['from'] = from_addr
    message['to'] = ', '.join(to_addrs)
    try:
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, message.as_string())
    except:
        return {"dados":"falha ao enviar"}
    finally:
        server.quit()
    return {"dados":"enviados"}


@app.post("/user/create/", 
          response_model=schemas.User,
         tags=['User'],
         dependencies=[Depends(get_credentials)])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user)
    if db_user:
        raise HTTPException(status_code=400, detail="usuario registrado")
    return crud.create_user(db=db, user=user)


@app.post("/user/read/name/email/", 
         response_model=schemas.User,
         tags=['User'],
         dependencies=[Depends(get_credentials)])
def read_user_by_name_and_email(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="usuario sem registro")
    return db_user


@app.get("/user/read/", 
         tags=['User'],
         dependencies=[Depends(get_credentials)])
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_name_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="usuario sem registro")
    return db_user


@app.post("/user/create/message/", 
          response_model=schemas.Message,
         tags=['Message'],
         dependencies=[Depends(get_credentials)])
def create_message_for_user(user: schemas.UserBase, message: schemas.MessageCreate, db: Session = Depends(get_db)):   
    db_user = crud.get_user_by_name(db, user)
    if db_user is None:
        raise HTTPException(status_code=403, detail="usuario sem registro")
    return crud.create_message_user(db, message, user)


@app.get("/read/messages/", 
         response_model=list[schemas.Message],
         tags=['Message'],
         dependencies=[Depends(get_credentials)])
def read_messages_by_time(hora: time, db: Session = Depends(get_db)):
    messages = crud.get_messages(db, hora)
    return messages


@app.get("/delete/messages/", 
         tags=['Início'],
         dependencies=[Depends(get_credentials)])
def delete_database(db: Session = Depends(get_db)):
    crud.delete_message(db)
    lista_users = crud.get_users(db=db)
    for user in lista_users:
        crud.delete_user(db, user.id)
    return {"log":"banco restaurado"}


@app.on_event("startup")
@repeat_every(seconds=86400, wait_first=False)
def delete_bd():
    with SessionLocal() as db:
        crud.delete_message(db)
        lista_users = crud.get_users(db=db)
        for user in lista_users:
            crud.delete_user(db, user.id)