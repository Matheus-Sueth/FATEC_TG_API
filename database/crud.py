from sqlalchemy.orm import Session
from . import models, schemas 


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(nome=user.nome, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_name(db: Session, user: schemas.User):
    return db.query(models.User).filter(models.User.nome == user.nome and models.User.email == user.email).first()


def get_name_by_id(db: Session, user_id: int):
    return db.query(models.User.nome).filter(models.User.id == user_id).first()


def delete_user(db: Session, user_id: int):
    db.delete(db.query(models.User).filter(models.User.id == user_id).first())
    db.commit()


def create_message_user(db: Session, message: schemas.MessageCreate, user: schemas.User):
    user = db.query(models.User).filter(models.User.nome == user.nome and models.User.email == user.email).first()
    db_message = models.Message(**message.dict(), owner_id=user.id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages(db: Session, hora):
    return db.query(models.Message).filter(models.Message.hora >= hora).all()


def delete_message(db: Session):
    messages = db.query(models.Message).all()
    for message in messages:
        db.delete(db.query(models.Message).filter(models.Message.id == message.id).first())
        db.commit()