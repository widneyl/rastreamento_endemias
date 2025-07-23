from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, Relationship
from database import engine


Base = declarative_base()
# _Sessao = sessionmaker(engine) # Abre uma sessão com o banco de dados que será fechada posteriormente


# As entidades são representadas por classes, no caso temos a entidade tutor representada pela classe Tutor
class Pacientes(Base): 
    __tablename__ = 'paciente' # __tablename__ é usado para nomear a tabela 
    
    cpf = Column(String(15), unique=True, primary_key=True) # Definição do atributo cpf como chave primaria
    nome = Column(String(50)) # Definição do atributo nome
    telefone = Column(String(20), unique=True) # Definição do atributo telefone
    cep = Column(Integer) # Definição do atributo cep
    rua = Column(String(40)) # Definição do atributo rua
    numero = Column(Integer) # Definição do atributo numero
    bairro = Column(String(50)) # Definição do atributo bairro


class Casos(Base): 
    __tablename__ = 'caso'
    id_caso = Column(Integer, primary_key=True) # Definição do id
    cpf_paciente = Column(String(15), ForeignKey('paciente.cpf'))
    data_diagnostico = Column(Date) # Definição do atributo data_diagnostico
    status = Column(String(6)) # Definição do atributo status
    doenca = Column(String(6)) # Definição do atributo doenca
    sintomas = Column(String(100))


class Agente_Saude(Base): 
    __tablename__ = 'agente'
    
    id_agente = Column(Integer, primary_key=True) # Definição do id
    nome = Column(String(40)) # Definição do atributo nome
    cargo = Column(String(40)) # Definição do atributo status


class Area_Risco(Base): 
    __tablename__ = 'area_risco'
    
    id_area = Column(Integer, primary_key=True) # Definição do id
    localizacao = Column(String(40)) # Definição do atributo nome
    nivel_risco = Column(String(10)) # Definição do atributo status


class Doenca(Base): 
    __tablename__ = 'doenca'
    
    id_doenca = Column(Integer, primary_key=True) # Definição do id
    nome = Column(String(40), unique=True, ) # Definição do atributo nome


Base.metadata.create_all(engine) # Cria o banco de dados, se ja existir ignora

    