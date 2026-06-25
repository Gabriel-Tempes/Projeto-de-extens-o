import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# =========================
# BANCO DE DADOS (SQLite)
# =========================
conexao = sqlite3.connect("extensao.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS participantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER,
    telefone TEXT,
    escolaridade TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS presencas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participante_id INTEGER,
    presente INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS avaliacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participante_id INTEGER,
    nota INTEGER,
    comentario TEXT
)
""")

conexao.commit()

# =========================
# FUNÇÕES
# =========================

def cadastrar():
    nome = entry_nome.get()
    idade = entry_idade.get()
    telefone = entry_telefone.get()
    escolaridade = entry_escolaridade.get()

    if nome == "":
        messagebox.showwarning("Erro", "Nome obrigatório")
        return

    cursor.execute("""
        INSERT INTO participantes (nome, idade, telefone, escolaridade)
        VALUES (?, ?, ?, ?)
    """, (nome, idade, telefone, escolaridade))

    conexao.commit()
    messagebox.showinfo("Sucesso", "Participante cadastrado!")
    listar()

def listar():
    tree.delete(*tree.get_children())

    cursor.execute("SELECT * FROM participantes")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def marcar_presenca():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showwarning("Erro", "Selecione um participante")
        return

    dados = tree.item(selecionado, "values")
    participante_id = dados[0]

    cursor.execute("""
        INSERT INTO presencas (participante_id, presente)
        VALUES (?, 1)
    """, (participante_id,))

    conexao.commit()
    messagebox.showinfo("Sucesso", "Presença registrada!")

def avaliar():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showwarning("Erro", "Selecione um participante")
        return

    nota = entry_nota.get()
    comentario = entry_comentario.get()

    if nota == "":
        messagebox.showwarning("Erro", "Informe a nota")
        return

    dados = tree.item(selecionado, "values")
    participante_id = dados[0]

    cursor.execute("""
        INSERT INTO avaliacoes (participante_id, nota, comentario)
        VALUES (?, ?, ?)
    """, (participante_id, nota, comentario))

    conexao.commit()
    messagebox.showinfo("Sucesso", "Avaliação registrada!")

def relatorio():
    cursor.execute("SELECT COUNT(*) FROM participantes")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM presencas")
    presentes = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(nota) FROM avaliacoes")
    media = cursor.fetchone()[0]

    if media is None:
        media = 0
    else:
        media = round(media, 2)

    messagebox.showinfo(
        "Relatório",
        f"Participantes: {total}\n"
        f"Presenças registradas: {presentes}\n"
        f"Média de avaliação: {media}"
    )

# =========================
# INTERFACE
# =========================
janela = tk.Tk()
janela.title("Sistema de Extensão - Inclusão Digital")
janela.geometry("900x600")

# Campos
tk.Label(janela, text="Nome").grid(row=0, column=0)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1)

tk.Label(janela, text="Idade").grid(row=1, column=0)
entry_idade = tk.Entry(janela)
entry_idade.grid(row=1, column=1)

tk.Label(janela, text="Telefone").grid(row=2, column=0)
entry_telefone = tk.Entry(janela)
entry_telefone.grid(row=2, column=1)

tk.Label(janela, text="Escolaridade").grid(row=3, column=0)
entry_escolaridade = tk.Entry(janela)
entry_escolaridade.grid(row=3, column=1)

# Nota e comentário
tk.Label(janela, text="Nota").grid(row=4, column=0)
entry_nota = tk.Entry(janela)
entry_nota.grid(row=4, column=1)

tk.Label(janela, text="Comentário").grid(row=5, column=0)
entry_comentario = tk.Entry(janela)
entry_comentario.grid(row=5, column=1)

# Botões
tk.Button(janela, text="Cadastrar", command=cadastrar).grid(row=6, column=0)
tk.Button(janela, text="Listar", command=listar).grid(row=6, column=1)
tk.Button(janela, text="Presença", command=marcar_presenca).grid(row=6, column=2)
tk.Button(janela, text="Avaliar", command=avaliar).grid(row=6, column=3)
tk.Button(janela, text="Relatório", command=relatorio).grid(row=6, column=4)

# Tabela
tree = ttk.Treeview(janela, columns=("ID", "Nome", "Idade", "Telefone", "Escolaridade"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Idade", text="Idade")
tree.heading("Telefone", text="Telefone")
tree.heading("Escolaridade", text="Escolaridade")
tree.grid(row=7, column=0, columnspan=5)

listar()

janela.mainloop()
