import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv


# LOAD ENV VARIABLES

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


# BASE DECLARATION

Base = declarative_base()

# DATABASE SINGLETON CLASS

class Database:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super(Database, cls).__new__(cls)

            cls._instance._initialize()

        return cls._instance


    def _initialize(self):

        self.engine = create_engine(

            DATABASE_URL,

            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,

            echo=False,

            future=True

        )


        self.SessionLocal = sessionmaker(

            bind=self.engine,

            autocommit=False,

            autoflush=False,

            expire_on_commit=False
        )

    # GET SESSION

    def get_session(self):

        return self.SessionLocal()

# SINGLETON INSTANCE

db_instance = Database()


# FASTAPI DEPENDENCY

def get_db():

    db = db_instance.get_session()

    try:

        yield db

    finally:

        db.close()