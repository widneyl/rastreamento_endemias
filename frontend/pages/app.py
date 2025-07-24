import panel as pn
import pandas as pd 
import sys
import os
from datetime import datetime


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend/')))
print("Caminho adicionado ao sys.path:", os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))


import insercao

pn.extension()


mensagem = pn.pane.Alert("", alert_type='success', visible=False)
container_mensagem = pn.Column(mensagem, width=700, height=50)

#Cadastro paciente
nome = pn.widgets.TextInput(name="Nome")
cpf = pn.widgets.TextInput(name="CPF")
telefone = pn.widgets.TextInput(name="Telefone")
rua = pn.widgets.TextInput(name="Rua")
numero = pn.widgets.IntInput(name="Numero")
bairro = pn.widgets.TextInput(name="Bairro")
cep = pn.widgets.IntInput(name="CEP")
cadastrar = pn.widgets.Button(name="Cadastrar Paciente", button_type="success")
atualizar = pn.widgets.Button(name="Atualizar Paciente", button_type="primary")


#Buscar paciente, excluir paciente
buscar = pn.widgets.TextInput(name="Digite o CPF do paciente")
buscarPacienteButton = pn.widgets.Button(name="Buscar paciente", button_type="primary")
buscarCasosPaciente = pn.widgets.TextInput(name="Digite o CPF do paciente")
buscarCasosPacienteButton = pn.widgets.Button(name="Buscar casos", button_type="primary")
deletar = pn.widgets.TextInput(name="Digite o CPF do paciente")
deletarPacienteButton = pn.widgets.Button(name="Deletar paciente", button_type="danger")
listar_pacientes_button = pn.widgets.Button(name="Listar pacientes", button_type="primary")
#Cadastro Caso
doencaCaso = pn.widgets.Select(name="Doenças", options=["Dengue", "Zica", "Chikungunya"])
data_diagnostico_caso = pn.widgets.TextInput(name="Data do diagnostico")
status = pn.widgets.Select(name="Status", options=["Ativo", "Curado", "Obito"])
sintomas = pn.widgets.TextInput(name="Sintomas")
cpf_paciente_Caso = pn.widgets.TextInput(name="CPF do paciente")
id_agente_caso = pn.widgets.TextInput(name="ID do agente responsavel")
cadastrarCasoButton = pn.widgets.Button(name="Registrar Caso", button_type="success")
listarCasosButton = pn.widgets.Button(name="Listar Todos os Casos", button_type="primary")

#Cadastrar Doença
# doenca = pn.widgets.TextInput(name="Nome da Doença")
# doencaButton = pn.widgets.Button(name="Cadastrar", button_type='success')
listarDoençasButton = pn.widgets.Button(name="Listar Tados as Doenças", button_type="primary")

#Areas de risco
listarAreasButton = pn.widgets.Button(name="Listar Areas de Risco", button_type='primary')


#Cadastrar Agente de saude
nome_agente = pn.widgets.TextInput(name="Nome do agente")
cargo_agente = pn.widgets.TextInput(name="cargo do agente")
cadastro_agente_Button = pn.widgets.Button(name="Cadastrar", button_type='success')
listar_agentes_button = pn.widgets.Button(name="Listar Todos os Agentes", button_type='primary')

areas_associados_agente_input = pn.widgets.TextInput(name="Listar areas que o agente atua")
areas_associados_agente_button = pn.widgets.Button(name="Listar areas", button_type='primary')
#########################################FUNCÕES##################################
def limpar_foms():
    nome.value = ""
    cpf.value = ""
    telefone.value = ""
    rua.value = ""
    numero.value = ""
    bairro.value = ""
    cep.value = ""
    
def cadastar_paciente(event):
    insercao.cadastra_paciente(
        nome=nome.value,
        cpf=cpf.value,
        telefone=telefone.value,
        rua=rua.value,
        numero=numero.value,
        bairro=bairro.value,
        cep=cep.value
    )
    mensagem.object = "Paciente cadastrado com sucesso!"
    mensagem.visible = True
    limpar_foms()
    

def atualizar_no_banco(event):
    dados = {
    "nome": nome.value,
    "cpf": cpf.value,
    "telefone": telefone.value,
    "rua": rua.value,
    "numero": numero.value,
    "bairro": bairro.value,
    "cep": cep.value
    }
    mensagem.object = "Paciente atualizado com sucesso!"
    mensagem.visible = True
    insercao.atualizar_paciente(cpf.value, dados)
    limpar_foms()

def deletar_paciente(event):
    insercao.deletar_paciente(deletar.value)
    mensagem.object = "Paciente deletado!"
    mensagem.visible = True

def buscar_paciente(event):
   paciente_encontrado =  insercao.buscar_paciente_por_cpf(buscar.value)
   if paciente_encontrado:
        # Cria DataFrame com o único paciente encontrado
        df = pd.DataFrame([{
            "Nome": paciente_encontrado.nome,
            "CPF": paciente_encontrado.cpf,
            "Telefone": paciente_encontrado.telefone,
            "CEP": paciente_encontrado.cep,
            "Rua": paciente_encontrado.rua,
            "Número": paciente_encontrado.numero,
            "Bairro": paciente_encontrado.bairro
        }])
        tabela.value = df
   else:
        tabela.value = pd.DataFrame([], columns=["Nome", "CPF", "Telefone", "CEP", "Rua", "Número", "Bairro"])

def cadastar_agente(event):
    insercao.cadastra_agente(
        nome = nome_agente.value,
        cargo = cargo_agente.value
    )
    mensagem.object = "Agente de Saude cadastrado com sucesso!"
    mensagem.visible = True
    
def listar_agentes(event):
    agentes_encontrados = insercao.listar_agentes()
    df = pd.DataFrame(agentes_encontrados)
    tabela.value = df
    
# def cadatrar_doenca(event):
#     nova_doenca = insercao.cadastrar_doenca(doenca.value)

def listar_doencas(event):
    doencas_encontradas = insercao.listar_doencas()
    df = pd.DataFrame(doencas_encontradas)
    tabela.value = df

def cadatrar_caso(event):
    data_formatada = datetime.strptime(data_diagnostico_caso.value, '%d%m%Y').date()
    insercao.registrar_caso(
        doenca = doencaCaso.value, 
        data_diagnostico = data_formatada,
        status = status.value, 
        sintomas = sintomas.value, 
        cpf_paciente = cpf_paciente_Caso.value,
        id_agente = id_agente_caso.value,
        )
    mensagem.object = "Caso registrado com sucesso!"
    mensagem.visible = True
    limpar_foms()

def listar_casos(event):
    casos_encontrados = insercao.listar_casos()
    df = pd.DataFrame(casos_encontrados)
    tabela.value = df

def listar_areas(event):
    areas_encontradas = insercao.listar_areas()
    df = pd.DataFrame(areas_encontradas)
    tabela.value = df
        
def buscar_casos_associados(event):
    casos_encontrados = insercao.buscar_casos_associados(buscarCasosPaciente.value)  
    if casos_encontrados:
        df = pd.DataFrame([{
            "id_caso": caso.id_caso,
            "cpf_paciente": caso.cpf_paciente,
            "data_diagnostico": caso.data_diagnostico,
            "status": caso.status,
            "doenca": caso.doenca,
            "sintomas": caso.sintomas,
            "id_agente": caso.id_agente,
        } for caso in casos_encontrados])
        tabela.value = df
    else:
        tabela.value = pd.DataFrame([], columns=["id_caso", "cpf_paciente", "data_diagnostico", "status", "doenca", "sintomas"])

def buscar_areas_associados_a_agentes(event):
    areas_encontradas = insercao.buscar_areas_associados_a_agentes(areas_associados_agente_input.value)  
    df = pd.DataFrame(areas_encontradas)
    tabela.value = df

def listar_pacientes(event):
    pacientes = insercao.listar_pacientes()
    df = pd.DataFrame(pacientes)
    tabela.value = df
    
pacientes = insercao.listar_pacientes()
df = pd.DataFrame(pacientes)
tabela = pn.widgets.DataFrame(df, width=1100, height=300)

listar_pacientes_button.on_click(listar_pacientes)
cadastrar.on_click(cadastar_paciente)
atualizar.on_click(atualizar_no_banco)
buscarPacienteButton.on_click(buscar_paciente)
deletarPacienteButton.on_click(deletar_paciente)
cadastrarCasoButton.on_click(cadatrar_caso)
buscarCasosPacienteButton.on_click(buscar_casos_associados)
listarCasosButton.on_click(listar_casos)
listarDoençasButton.on_click(listar_doencas)
# doencaButton.on_click(cadatrar_doenca)
listarAreasButton.on_click(listar_areas)
cadastro_agente_Button.on_click(cadastar_agente)
listar_agentes_button.on_click(listar_agentes)
areas_associados_agente_button.on_click(buscar_areas_associados_a_agentes)

painel = pn.Column(
    pn.Row(
        pn.Column(
        "## Cadastro de Pacientes",
        nome, cpf, telefone, rua, numero, bairro, cep, 
        pn.Row(cadastrar),
        ),
        pn.Column(
        "## Registro de novos Casos",
        doencaCaso, data_diagnostico_caso, status, sintomas, cpf_paciente_Caso, id_agente_caso,
        cadastrarCasoButton    
        ),
        pn.Column(
        "## Buscar Paciente",
        buscar,
        buscarPacienteButton,
        "## Casos associados ao paciente",
        buscarCasosPaciente,
        buscarCasosPacienteButton, 
        ),
        pn.Column(
        "## Cadastro de Agentes",
        nome_agente, cargo_agente,
        cadastro_agente_Button,
        # "## Cadastrar Doença",
        # doenca,
        # doencaButton,
        ),
        pn.Column(
        "## Areas que o Agente atua",
        areas_associados_agente_input,
        areas_associados_agente_button,
        ),
        # pn.Column(
        # "## Areas que o Agente atua",
        # areas_associados_agente_input,
        # areas_associados_agente_button,
        # ),
        # pn.Column(
        # "## Deletar Paciente",
        # deletar,
        # deletarPacienteButton,
        # ),
    ),
        container_mensagem,
    
    pn.Column(
        pn.Row(
            listarDoençasButton,
            listarCasosButton,
            listarAreasButton,
            listar_agentes_button,
            listar_pacientes_button
            ),
        "## Tabela Resultados",
        tabela,
      
        
    )
).servable()
