import tkinter as tk
import customtkinter as ctk
import json

# Nome do arquivo JSON onde os votos serão armazenados
arquivo_json = 'votos.json'
total_votos_permitidos = 50  # Limite de votos total
max_candidatos = 3  # Limite máximo de candidatos

# Função para carregar os votos do arquivo JSON
def carregar_dados(arquivo):
    try:
        with open(arquivo, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Função para salvar os votos no arquivo JSON
def salvar_dados(dados, arquivo):
    with open(arquivo, 'w') as file:
        json.dump(dados, file, indent=4)

# Função para contar o número total de votos já realizados
def contar_votos_totais():
    return sum(votos.values())

# Função para contar o número de candidatos
def contar_candidatos():
    return len(votos)

# Função para adicionar um novo candidato
def adicionar_candidato():
    nome_candidato = entry_candidato_adicionar.get()
    if nome_candidato and nome_candidato not in votos:
        if contar_candidatos() < max_candidatos:
            votos[nome_candidato] = 0
            salvar_dados(votos, arquivo_json)
            criar_botao_candidato(nome_candidato)
            entry_candidato_adicionar.delete(0, 'end')
        else:
            ctk.CTkMessageBox.show_info("Limite de Candidatos", "O número máximo de candidatos foi atingido.")
    else:
        ctk.CTkMessageBox.show_info("Erro", "O candidato já existe ou o nome está vazio.")

# Função para criar um botão e label para o candidato
def criar_botao_candidato(nome):
    button = ctk.CTkButton(app, text=f"Votar em {nome}", command=lambda: votar(nome))
    button.pack(pady=5)
    label = ctk.CTkLabel(app, text=f"Votos para {nome}: {votos[nome]}")
    label.pack(pady=2)
    botoes_labels[nome] = (button, label)

# Função chamada ao clicar em um botão de voto
def votar(candidato):
    votos_totais = contar_votos_totais()
    if votos_totais < total_votos_permitidos:
        votos[candidato] += 1
        salvar_dados(votos, arquivo_json)
        atualizar_interface()
        if votos_totais + 1 == total_votos_permitidos:
            declarar_vencedor()
    else:
        declarar_vencedor()

# Função para atualizar a interface gráfica com os votos atuais
def atualizar_interface():
    for candidato, (button, label) in botoes_labels.items():
        label.configure(text=f"Votos para {candidato}: {votos.get(candidato, 0)}")

# Função para declarar o vencedor
def declarar_vencedor():
    if votos:
        vencedor = max(votos, key=votos.get)
        label_vencedor.configure(text=f"Votação Encerrada! Vencedor: {vencedor} com {votos[vencedor]} votos!")
        for button, _ in botoes_labels.values():
            button.configure(state="disabled")

# Função para lidar com o evento da tecla "Enter"
def tecla_enter(event):
    adicionar_candidato()

# Carrega os votos iniciais
votos = carregar_dados(arquivo_json)

# Dicionário para armazenar os botões e labels dos candidatos
botoes_labels = {}

# Configuração da interface gráfica
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sistema de Votação")
app.geometry("350x500")

# Campo para inserir o nome do candidato para adicionar
entry_candidato_adicionar = ctk.CTkEntry(app, placeholder_text="Nome do candidato para adicionar")
entry_candidato_adicionar.pack(pady=10)

# Botão para adicionar um novo candidato
button_adicionar = ctk.CTkButton(app, text="Adicionar Candidato", command=adicionar_candidato)
button_adicionar.pack(pady=10)

# Bind a tecla Enter ao campo de entrada
app.bind("<Return>", tecla_enter)

# Label para exibir o vencedor
label_vencedor = ctk.CTkLabel(app, text="")
label_vencedor.pack(pady=20)

# Cria os botões e labels para candidatos existentes no arquivo JSON
for candidato in votos:
    criar_botao_candidato(candidato)

app.mainloop()
