from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://lcrqrxainnruur:a06458298899475eb468a56bd8637706b9c53534f2809e90375be375982fc134@ec2-44-199-9-102.compute-1.amazonaws.com:5432/d4vn6ip4sj7nmg"
   
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()