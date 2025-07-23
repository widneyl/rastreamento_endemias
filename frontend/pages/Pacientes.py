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
container_mensagem = pn.Column(mensagem, width=700)

############INPUTS E BUTTONS#####################################
nome = pn.widgets.TextInput(name="Nome")
cpf = pn.widgets.TextInput(name="CPF")
telefone = pn.widgets.TextInput(name="Telefone")
rua = pn.widgets.TextInput(name="Rua")
numero = pn.widgets.IntInput(name="Numero")
bairro = pn.widgets.TextInput(name="Bairro")
cep = pn.widgets.IntInput(name="CEP")
cadastrar = pn.widgets.Button(name="Cadastrar Paciente", button_type="success")
atualizar = pn.widgets.Button(name="Atualizar Paciente", button_type="primary")
buscar = pn.widgets.TextInput(name="Digite o CPF do paciente")
buscarPacienteButton = pn.widgets.Button(name="Buscar paciente", button_type="primary")
buscarCasosPaciente = pn.widgets.TextInput(name="Digite o CPF do paciente")
buscarCasosPacienteButton = pn.widgets.Button(name="Buscar casos", button_type="primary")
deletar = pn.widgets.TextInput(name="Digite o CPF do paciente")
deletarPacienteButton = pn.widgets.Button(name="Deletar paciente", button_type="danger")
doencaCaso = pn.widgets.TextInput(name="Doença")
data_diagnostico_caso = pn.widgets.TextInput(name="Data do diagnostico")
status = pn.widgets.TextInput(name="Status do paciente")
sintomas = pn.widgets.TextInput(name="Sintomas")
cpf_paciente_Caso = pn.widgets.TextInput(name="CPF do paciente")
cadastrarCasoButton = pn.widgets.Button(name="Registrar Caso", button_type="success")
##########################DOENÇA################################
doenca = pn.widgets.TextInput(name="Nome da Doença")
doencaButton = pn.widgets.Button(name="Cadastrar", button_type='primary')
##########################CASOS#################################



#########################################FUNCÕES##################################
def limpar_foms():
    nome.value = ""
    cpf.value = ""
    telefone.value = ""
    rua.value = ""
    numero.value = ""
    bairro.value = ""
    cep.value = ""
    
def cadastar_no_banco(event):
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
        
    
def cadatrar_doenca(event):
    nova_doenca = insercao.cadastrar_doenca(doenca.value)
    

def cadatrar_caso(event):
    data_formatada = datetime.strptime(data_diagnostico_caso.value, '%d%m%Y').date()
    insercao.registrar_caso(
        doenca = doencaCaso.value, 
        data_diagnostico = data_formatada,
        status = status.value, 
        sintomas = sintomas.value, 
        cpf_paciente = cpf_paciente_Caso.value
        )
    mensagem.object = "Caso registrado com sucesso!"
    mensagem.visible = True
    limpar_foms()
    
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
        } for caso in casos_encontrados])
        tabela.value = df
    else:
        tabela.value = pd.DataFrame([], columns=["id_caso", "cpf_paciente", "data_diagnostico", "status", "doenca", "sintomas"])

    
    
    
    
    
    
pacientes = insercao.listar_pacientes()
df = pd.DataFrame(pacientes)
tabela = pn.widgets.DataFrame(df, width=1200, height=350)

cadastrar.on_click(cadastar_no_banco)
atualizar.on_click(atualizar_no_banco)
buscarPacienteButton.on_click(buscar_paciente)
deletarPacienteButton.on_click(deletar_paciente)
cadastrarCasoButton.on_click(cadatrar_caso)
buscarCasosPacienteButton.on_click(buscar_casos_associados)

doencaButton.on_click(cadatrar_doenca)

painel = pn.Column(
    pn.Row(
        pn.Column(
        "## Cadastro de Pacientes",
        nome, cpf, telefone, rua, numero, bairro, cep, 
        pn.Row(cadastrar, atualizar),
        ),
        pn.Column(
        "## Buscar Paciente",
        buscar,
        buscarPacienteButton,
        "## Casos associados ao paciente",
        buscarCasosPaciente,
        buscarCasosPacienteButton, 
        "## Deletar Paciente",
        deletar,
        deletarPacienteButton,
        ),
        pn.Column(
        "## Cadastrar Doença",
        doenca,
        doencaButton
        ),
        pn.Column(
        "## Registrar novo Caso",
        doencaCaso, data_diagnostico_caso, status, sintomas, cpf_paciente_Caso,
        cadastrarCasoButton    
        )
    ),
        container_mensagem,
    
    pn.Column(
        "## Tabela Resultados",
        tabela,
      
        
    )
).servable()
