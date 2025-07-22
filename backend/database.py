from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()
db_url = os.getenv("DB_URL")
if not db_url:
    raise ValueError("A variável DB_URL não está definida no arquivo .env")


engine = create_engine(db_url)
_Sessao = sessionmaker(engine) # Abre uma sessão com o banco de dados que será fechada posteriormente
