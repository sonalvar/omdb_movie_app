from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI

engine = create_engine(DATABASE_URI, pool_pre_ping=True, pool_recycle=3600, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
