from criacao import Pacientes, Doenca, Casos, Agente_Saude, Area_Risco, Integer
from database import _Sessao # Para abrir uma sesão com o banco de dados


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
        print("Paciente cadastrado")

# Consulta um paciente pelo CPF
def buscar_paciente_por_cpf(cpf: str):
    with _Sessao() as sessao:
        paciente = sessao.query(Pacientes).filter_by(cpf=cpf).first()
        print("Buscando")
        print(paciente)
        return paciente

# Atualizar os dados de um paciente no banco de dados
def atualizar_paciente(cpf: str, novos_dados: dict):
    with _Sessao() as sessao:
        paciente = sessao.query(Pacientes).filter_by(cpf=cpf).first()
        if paciente:
            for chave, valor in novos_dados.items():
                setattr(paciente, chave, valor)
            sessao.commit()
            print("Dados atualizados")
        

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

def cadastrar_doenca(nome: str):
    with _Sessao() as sessao:
        doenca = Doenca(nome = nome)
        sessao.add(doenca)
        sessao.commit()
        print("Doença cadastrada")

def registrar_caso(doenca: str, data_diagnostico: str, status: str, sintomas: str, cpf_paciente: str):
    with _Sessao() as sessao:
        caso = Casos(
            doenca = doenca,
            data_diagnostico = data_diagnostico,
            status = status,
            sintomas = sintomas,
            cpf_paciente = cpf_paciente
        )
        sessao.add(caso)
        sessao.commit()
        print("Caso registrado")

def buscar_casos_associados(cpf: str):
     with _Sessao() as sessao:
        return sessao.query(Casos).filter_by(cpf_paciente = cpf).all()
       
        
        