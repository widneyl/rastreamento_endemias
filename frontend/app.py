import sys
import os
import panel as pn


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.insercao import cadastra_paciente, listar_pacientes  # você precisará criar essa função

pn.extension()

# --- Formulário de cadastro ---
form1 = pn.widgets.TextInput(name="Nome")
form2 = pn.widgets.TextInput(name="CPF")
form3 = pn.widgets.TextInput(name="Telefone")
form4 = pn.widgets.TextInput(name="CEP")
form5 = pn.widgets.TextInput(name="Rua")
form6 = pn.widgets.TextInput(name="Número")
form7 = pn.widgets.TextInput(name="Bairro")
botao_cadastrar = pn.widgets.Button(name='Cadastrar', button_type='primary', width=200)
mensagem = pn.pane.Markdown("", sizing_mode="stretch_width", margin=(10, 0, 0, 0))

def ao_clicar_cadastrar(event):
    if not form1.value.strip():
        mensagem.object = "⚠️ Preencha o nome."
        return
    if not form2.value.strip():
        mensagem.object = "⚠️ Preencha o CPF."
        return
    if not form4.value.strip():
        mensagem.object = "⚠️ Preencha o CEP."
        return

    cadastra_paciente(
        form1.value.strip(),
        form2.value.strip(),
        form3.value.strip(),
        form4.value.strip(),
        form5.value.strip(),
        form6.value.strip(),
        form7.value.strip()
    )
    mensagem.object = "✅ Paciente cadastrado com sucesso!"
    limpar_formulario()

def limpar_formulario():
    form1.value = ""
    form2.value = ""
    form3.value = ""
    form4.value = ""
    form5.value = ""
    form6.value = ""
    form7.value = ""

botao_cadastrar.on_click(ao_clicar_cadastrar)

form_layout = pn.Column(
    pn.pane.Markdown("## Cadastro de Paciente"),
    form1, form2, form3, form4, form5, form6, form7,
    botao_cadastrar,
    mensagem,
    width=500,
    margin=20
)

form_layout.servable()