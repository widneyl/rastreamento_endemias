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
        
# Cadastrar um novo agente
def cadastra_agente(nome: str, cargo: str):
    with _Sessao() as sessao:
        agente = Agente_Saude(
            nome = nome, 
            cargo = cargo, 
        )
        sessao.add(agente)
        sessao.commit()
        print("Agente cadastrado")
        
def listar_agentes():
    with _Sessao() as sessao:
        agentes = sessao.query(Agente_Saude).all()
        return[{
            "id_agente": a.id_agente,
            "nome": a.nome,
            "cargo": a.cargo
        }for a in agentes]

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
        
def listar_doencas():
    with _Sessao() as sessao:
        doencas = sessao.query(Doenca).all()
        return [{
            "id_doenca": p.id_doenca,
            "nome": p.nome
        }for p in doencas]
        
def listar_areas():
    with _Sessao() as sessao:
        area = sessao.query(Area_Risco).all()
        return [{
            "id_area": p.id_area,
            "localizacao": p.localizacao,
            "numero_de_casos": p.numero_de_casos,
            "id_agente": p.id_agente,
            "nivel_risco": p.nivel_risco,
        }for p in area]

def registrar_caso(doenca: str, data_diagnostico: str, status: str, sintomas: str, cpf_paciente: str, id_agente: Integer):
    with _Sessao() as sessao:
        caso = Casos(
            doenca = doenca,
            data_diagnostico = data_diagnostico,
            status = status,
            sintomas = sintomas,
            cpf_paciente = cpf_paciente,
            id_agente = id_agente
        )
        
        def definir_nivel_de_risco(qtd):
            if qtd >= 7:
                return "Alto"
            elif qtd >= 4:
                return "Médio"
            else:
                return "Baixo"
        
        localizaca_paciente = sessao.query(Pacientes).filter_by(cpf = cpf_paciente).first()
       
        area = sessao.query(Area_Risco).filter_by(localizacao = localizaca_paciente.cep).first()
        
        if area:
            area.numero_de_casos += 1
        else:
            area = Area_Risco(
                localizacao = localizaca_paciente.cep,
                numero_de_casos=1,
                id_agente = id_agente
            )
            sessao.add(area)
        
        area.nivel_risco = definir_nivel_de_risco(area.numero_de_casos)
        
        
        sessao.add(caso)
        sessao.commit()
        print("Caso registrado")
        
        

def buscar_casos_associados(cpf: str):
     with _Sessao() as sessao:
        return sessao.query(Casos).filter_by(cpf_paciente = cpf).all()


def buscar_areas_associados_a_agentes(id_agente: Integer):
     with _Sessao() as sessao:
        area = sessao.query(Area_Risco).filter_by(id_agente = id_agente).all()
        return [{
            "id_area": p.id_area,
            "localizacao": p.localizacao,
            "numero_de_casos": p.numero_de_casos,
            "id_agente": p.id_agente,
            "nivel_risco": p.nivel_risco,
        }for p in area]
    
    
    
def listar_casos():
    with _Sessao() as sessao:
        casos = sessao.query(Casos).all()
        # Retorna lista de dicionários para facilitar montar DataFrame
        return [{
            "id_caso": p.id_caso,
            "cpf_paciente": p.cpf_paciente,
            "data_diagnostico": p.data_diagnostico,
            "status": p.status,
            "doenca": p.doenca,
            "sintomas": p.sintomas
        } for p in casos]