from .criacao import Pacientes, Doenca, Casos, Agente_Saude, Area_Risco, Integer
from .database import _Sessao # Para abrir uma sesão com o banco de dados


# Cadastrar um novo paciente
def cadastra_paciente(cpf: str, nome: str, telefone: str, cep: Integer, rua: str, numero: Integer, bairro: str):
    with _Sessao() as sessao:
        paciente = Pacientes(
            cpf = cpf, 
            nome = nome, 
            telefone = telefone, 
            cep = cep, 
            rua = rua, 
            numero = numero, 
            bairro = bairro
        )
        sessao.add(paciente)
        sessao.commit()

# Consulta um paciente pelo CPF
def get_paciente_por_cpf(cpf: str):
    with _Sessao() as sessao:
        paciente = sessao.query(Pacientes).filter_by(cpf=cpf).first()
        return paciente

# Atualizar os dados de um paciente no banco de dados
def atualizar_paciente(cpf: str, novos_dados: dict):
    with _Sessao() as sessao:
        paciente = sessao.query(Pacientes).filter_by(cpf=cpf).first()
        if paciente:
            for chave, valor in novos_dados.items():
                setattr(paciente, chave, valor)
            sessao.commit()
        

# Deletar um paciente
def deletar_paciente(cpf: str):
    with _Sessao() as sessao:
        paciente = sessao.query(Pacientes).filter_by(cpf=cpf).first()
        sessao.delete(paciente)
        sessao.commit()

def listar_pacientes():
    with _Sessao() as sessao:
        pacientes = sessao.query(Pacientes).all()
        # Retorna lista de dicionários para facilitar montar DataFrame
        return [{
            "Nome": p.nome,
            "CPF": p.cpf,
            "Telefone": p.telefone,
            "CEP": p.cep,
            "Rua": p.rua,
            "Número": p.numero,
            "Bairro": p.bairro
        } for p in pacientes]

