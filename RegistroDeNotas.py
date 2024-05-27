########## SISTEMAS DE REGISTROS DE NOTAS ############

########## IMPORTS  ############
import customtkinter as ctk     
from tkinter import messagebox  
import psycopg2                 
################################

# Função de conexão ao banco de dados
def connect_db():
    conn = psycopg2.connect(
        dbname="dbvr0o2ch6usrn",
        user="u66nm5gukee2rj",
        password="p759baf31cab6ff4e4d54d937499de2b678779d29e1b82b4a0235e4574c5280f9",
        host="ce0lkuo944ch99.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
        port="5432"
    )

    cursor = conn.cursor()
 #Criação da tabela de Alunos   
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        matricula VARCHAR(50) NOT NULL UNIQUE
    )
    ''')

#Criação da tabela de disciplinas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS disciplinas (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        ano INTEGER NOT NULL,
        semestre INTEGER NOT NULL
    )
    ''')

#Criação da tabela responsavel por amazenar as notas e o calculo da nota final do aluno 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notas (
        id SERIAL PRIMARY KEY,
        id_aluno INTEGER NOT NULL REFERENCES alunos(id),
        id_disciplina INTEGER NOT NULL REFERENCES disciplinas(id),
        sm1 REAL,
        sm2 REAL,
        av REAL,
        avs REAL,
        nf REAL,
        situacao VARCHAR(20)
    )
    ''')
#Criação da tabela para vincular as tabelas de alunos e disciplinas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aluno_disciplina (
        id SERIAL PRIMARY KEY,
        id_aluno INTEGER NOT NULL REFERENCES alunos(id),
        id_disciplina INTEGER NOT NULL REFERENCES disciplinas(id)
    )
    ''')
    conn.commit()

    return conn
    
# Função para incluir disciplin
# Função para calcular notas finais



##################################
### FUNCOES PARA A TELA INCIAL ###
# Função para voltar à tela inicial
def voltar(tela):
    tela.destroy()
    root.deiconify()

# Função para abrir a tela de inserção de dados
def abrir_inserir_dados():
    root.withdraw()  # Esconde a tela inicial
    inserir_dados()  # Abre a tela de inserção de dados

# Função para abrir a tela de consulta de dados
def abrir_consultar_dados():
    root.withdraw()  # Esconde a tela inicial
    consultar_dados()  # Abre a tela de consulta de dados

# Função para criar a tela de consulta de dados (exemplo)
def consultar_dados():
    consulta_root = ctk.CTk()
    consulta_root.title("Consultar Dados")
    consulta_root.geometry("800x500")
    consulta_root.resizable(False, False)
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Função para consultar inscrições
    def consultar_inscricoes():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id_inscricao, id_aluno, id_disciplina, sm1, sm2, av, avs, nf, situacao FROM inscricao")
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        if resultados:
            relatorio = "\n".join([f"ID: {id_inscricao}, Aluno: {id_aluno}, Disciplina: {id_disciplina}, SM1: {sm1}, SM2: {sm2}, AV: {av}, AVS: {avs}, NF: {nf}, Situação: {situacao}" for id_inscricao, id_aluno, id_disciplina, sm1, sm2, av, avs, nf, situacao in resultados])
            messagebox.showinfo("Consulta de Inscrições", relatorio)
        else:
            messagebox.showinfo("Consulta de Inscrições", "Nenhuma inscrição encontrada.")

    

    # Função para consultar alunos
    

    # Função para calcular a nota final e atualizar a situação
    def calcular_nf():
        inscricao_id = entry_id_inscricao_nf.get()
        if inscricao_id:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT sm1, sm2, av, avs FROM inscricao WHERE id_inscricao = %s", (inscricao_id,))
            result = cursor.fetchone()
            if result:
                sm1, sm2, av, avs = result
                nf = (sm1 or 0) + (sm2 or 0) + max(av or 0, avs or 0)
                situacao = 'Aprovado' if nf >= 6.0 else 'Reprovado'
                cursor.execute("UPDATE inscricao SET nf = %s, situacao = %s WHERE id_inscricao = %s", (nf, situacao, inscricao_id))
                conn.commit()
                messagebox.showinfo("Sucesso", "Nota final calculada e atualizada com sucesso!")
            else:
                messagebox.showinfo("Erro", "Inscrição não encontrada.")
            cursor.close()
            conn.close()
            entry_id_inscricao_nf.delete(0, ctk.END)
        else:
            messagebox.showwarning("Erro", "Por favor, insira o ID da inscrição.")

    # Função para consultar notas e situação
    def consultar_notas():
        aluno_id = entry_id_aluno_consulta.get()
        disciplina_id = entry_id_disciplina_consulta.get()
        if aluno_id and disciplina_id:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT sm1, sm2, av, avs, nf, situacao FROM inscricao WHERE id_aluno = %s AND id_disciplina = %s", (aluno_id, disciplina_id))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result:
                sm1, sm2, av, avs, nf, situacao = result
                messagebox.showinfo("Consulta de Notas", f"SM1: {sm1}\nSM2: {sm2}\nAV: {av}\nAVS: {avs}\nNF: {nf}\nSituação: {situacao}")
            else:
                messagebox.showinfo("Consulta de Notas", "Nenhum registro encontrado.")
        else:
            messagebox.showwarning("Erro", "Por favor, insira o ID do aluno e da disciplina.")

    # Função para emitir relatório
    def emitir_relatorio():
        disciplina_id = entry_id_disciplina_relatorio.get()
        if disciplina_id:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT a.nome, i.sm1, i.sm2, i.av, i.avs, i.nf, i.situacao FROM inscricao i JOIN aluno a ON i.id_aluno = a.id_aluno WHERE i.id_disciplina = %s", (disciplina_id,))
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            if results:
                relatorio = "\n".join([f"{nome} - SM1: {sm1}, SM2: {sm2}, AV: {av}, AVS: {avs}, NF: {nf}, Situação: {situacao}" for nome, sm1, sm2, av, avs, nf, situacao in results])
                messagebox.showinfo("Relatório de Notas", relatorio)
            else:
                messagebox.showinfo("Relatório de Notas", "Nenhum registro encontrado.")
        else:
            messagebox.showwarning("Erro", "Por favor, insira o ID da disciplina.")

    # Adicione aqui os widgets para consulta de dados
    frame_consulta = ctk.CTkFrame(consulta_root, corner_radius=10, border_width=2, border_color="lightblue")
    frame_consulta.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    label_consulta = ctk.CTkLabel(frame_consulta, text="Consultar Dados", font=("Arial", 16))
    label_consulta.grid(row=0, column=0, columnspan=2, pady=10)

    button_consultar_inscricoes = ctk.CTkButton(frame_consulta, text="Consultar Inscrições", command=consultar_inscricoes)
    button_consultar_inscricoes.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    # Novo botão para calcular a nota final
    label_id_inscricao_nf = ctk.CTkLabel(frame_consulta, text="ID Inscrição:")
    label_id_inscricao_nf.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_id_inscricao_nf = ctk.CTkEntry(frame_consulta)
    entry_id_inscricao_nf.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    button_calcular_nf = ctk.CTkButton(frame_consulta, text="Calcular Nota Final", command=calcular_nf)
    button_calcular_nf.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Novo botão para consultar notas e situação
    label_id_aluno_consulta = ctk.CTkLabel(frame_consulta, text="ID Aluno:")
    label_id_aluno_consulta.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    entry_id_aluno_consulta = ctk.CTkEntry(frame_consulta)
    entry_id_aluno_consulta.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

    label_id_disciplina_consulta = ctk.CTkLabel(frame_consulta, text="ID Disciplina:")
    label_id_disciplina_consulta.grid(row=7, column=0, padx=10, pady=5, sticky="w")
    entry_id_disciplina_consulta = ctk.CTkEntry(frame_consulta)
    entry_id_disciplina_consulta.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

    button_consultar_notas = ctk.CTkButton(frame_consulta, text="Consultar Notas", command=consultar_notas)
    button_consultar_notas.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Novo botão para emitir relatório
    label_id_disciplina_relatorio = ctk.CTkLabel(frame_consulta, text="ID Disciplina Relatório:")
    label_id_disciplina_relatorio.grid(row=9, column=0, padx=10, pady=5, sticky="w")
    entry_id_disciplina_relatorio = ctk.CTkEntry(frame_consulta)
    entry_id_disciplina_relatorio.grid(row=9, column=1, padx=10, pady=5, sticky="ew")

    button_emitir_relatorio = ctk.CTkButton(frame_consulta, text="Emitir Relatório", command=emitir_relatorio)
    button_emitir_relatorio.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    button_voltar = ctk.CTkButton(consulta_root, text="Voltar", command=lambda: voltar(consulta_root))
    button_voltar.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

    consulta_root.mainloop()

# Função para criar a tela de inserção de dados
def inserir_dados():
    inserir_root = ctk.CTk()
    inserir_root.title("Inserir Dados")
    inserir_root.geometry("1100x770")
    inserir_root.resizable(False, False)
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    def criar_tabela(frame, dados):
            for i, linha in enumerate(dados):
                for j, valor in enumerate(linha):
                    label = ctk.CTkLabel(frame, text=valor)
                    label.grid(row=i+1, column=j, padx=5, pady=5, sticky="nsew")

    def consultar_alunos():
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, matricula FROM alunos")
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()
            print(resultados)
            return resultados
    
    # Função para consultar disciplinas
    def consultar_disciplinas():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, ano, semestre FROM disciplinas")
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    def inscrever_aluno():
        idAluno = int(entry_id_aluno.get())
        idDisciplina = int(entry_id_disciplina.get())

        print("ID Aluno:", idAluno)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO aluno_disciplina (id_aluno, id_disciplina) VALUES (%s, %s)", (idAluno, idDisciplina))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Sucesso", "Aluno inscrito com sucesso!")



    def incluir_disciplina():
        nome = entry_nome_disciplina.get()
        ano = entry_ano.get()
        semestre = entry_semestre.get()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO disciplinas (nome, ano, semestre) VALUES (%s, %s, %s)", (nome, ano, semestre))
        conn.commit()
        cursor.close()
        conn.close()
        CriarFrameConsultaDisciplina()
        entry_nome_disciplina.delete(0, ctk.END)
        entry_ano.delete(0, ctk.END)
        entry_semestre.delete(0, ctk.END)

     # Função para incluir aluno
    def incluir_aluno():
        nome = entry_nome_aluno.get()
        matricula = entry_matricula.get()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alunos (nome, matricula) VALUES (%s, %s)", (nome, matricula))
        conn.commit()
        cursor.close()
        conn.close()
        CriarFrameConsultaAluno()
        entry_nome_aluno.delete(0, ctk.END)
        entry_matricula.delete(0, ctk.END)
        
    # Função para incluir notas
    def incluir_notas():
        sm1 = entry_sm1.get() if entry_sm1.get() else 0
        sm2 = entry_sm2.get() if entry_sm2.get() else 0
        av = entry_av.get() if entry_av.get() else 0
        avs = entry_avs.get() if entry_avs.get() else 0
        id_aluno = entry_id_inscricao_aluno.get() 
        id_disciplina = entry_id_inscricao_disciplina.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notas (id_aluno, id_disciplina, sm1, sm2, av, avs) VALUES (%s, %s, %s, %s, %s, %s)",
            (id_aluno, id_disciplina, sm1, sm2, av, avs)
        )
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Sucesso", "Notas incluídas com sucesso!")
        entry_id_aluno.delete(0, ctk.END)
        entry_id_disciplina.delete(0, ctk.END)
        entry_sm1.delete(0, ctk.END)
        entry_sm2.delete(0, ctk.END)
        entry_av.delete(0, ctk.END)
        entry_avs.delete(0, ctk.END)

    # Frame para inclusão de disciplinas
    frame_disciplina = ctk.CTkFrame(inserir_root, corner_radius=10, border_width=2, border_color="lightblue")
    frame_disciplina.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    label_titulo_disciplina = ctk.CTkLabel(frame_disciplina, text="Incluir Disciplina", font=("Arial", 16))
    label_titulo_disciplina.grid(row=0, column=0, columnspan=2, pady=10)

    label_nome_disciplina = ctk.CTkLabel(frame_disciplina, text="Nome da Disciplina:")
    label_nome_disciplina.grid(row=1, column=0, padx=10, pady=5)
    entry_nome_disciplina = ctk.CTkEntry(frame_disciplina, width=200)
    entry_nome_disciplina.grid(row=1, column=1, padx=10, pady=5)

    label_ano = ctk.CTkLabel(frame_disciplina, text="Ano:")
    label_ano.grid(row=2, column=0, padx=10, pady=5)
    entry_ano = ctk.CTkEntry(frame_disciplina, width=200)
    entry_ano.grid(row=2, column=1, padx=10, pady=5)

    label_semestre = ctk.CTkLabel(frame_disciplina, text="Semestre:")
    label_semestre.grid(row=3, column=0, padx=10, pady=5)
    entry_semestre = ctk.CTkEntry(frame_disciplina, width=200)
    entry_semestre.grid(row=3, column=1, padx=10, pady=5)
    button_incluir_disciplina = ctk.CTkButton(frame_disciplina, text="Incluir Disciplina", command=incluir_disciplina)
    button_incluir_disciplina.grid(row=4, column=0, columnspan=2, pady=10)
    

    
    def CriarFrameConsultaDisciplina():
        # Frame para consulta de Disciplina
        frame_consulta_disciplina = ctk.CTkFrame(inserir_root, corner_radius=10, border_width=2, border_color="lightblue")
        frame_consulta_disciplina.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        label_consulta_titulo_aluno = ctk.CTkLabel(frame_consulta_disciplina, text="Consultar Disciplina", font=("Arial", 16))
        label_consulta_titulo_aluno.grid(row=0, column=0, columnspan=2, pady=10)

        result = consultar_disciplinas()
        criar_tabela(frame_consulta_disciplina, result)

    CriarFrameConsultaDisciplina()

    # Frame para consulta de Disciplina
    def CriarFrameConsultaAluno():
        frame_consulta_aluno = ctk.CTkFrame(inserir_root, corner_radius=10, border_width=2, border_color="lightblue")
        frame_consulta_aluno.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        label_consulta_titulo_discuplina = ctk.CTkLabel(frame_consulta_aluno, text="Consultar Aluno", font=("Arial", 16))
        label_consulta_titulo_discuplina.grid(row=0, column=0, columnspan=2, pady=10)

        result = consultar_alunos()
        criar_tabela(frame_consulta_aluno, result)

    CriarFrameConsultaAluno()
    
    # Frame para inclusão de alunos
    frame_aluno = ctk.CTkFrame(inserir_root, corner_radius=10, border_width=2, border_color="lightblue")
    frame_aluno.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    label_titulo_aluno = ctk.CTkLabel(frame_aluno, text="Incluir Aluno", font=("Arial", 16))
    label_titulo_aluno.grid(row=0, column=0, columnspan=2, pady=10)

    label_nome_aluno = ctk.CTkLabel(frame_aluno, text="Nome do Aluno:")
    label_nome_aluno.grid(row=1, column=0, padx=10, pady=5)
    entry_nome_aluno = ctk.CTkEntry(frame_aluno, width=200)
    entry_nome_aluno.grid(row=1, column=1, padx=10, pady=5)

    label_matricula = ctk.CTkLabel(frame_aluno, text="Número de Matrícula:")
    label_matricula.grid(row=2, column=0, padx=10, pady=5)
    entry_matricula = ctk.CTkEntry(frame_aluno, width=200)
    entry_matricula.grid(row=2, column=1, padx=10, pady=5)

    button_incluir_aluno = ctk.CTkButton(frame_aluno, text="Incluir Aluno", command=incluir_aluno)
    button_incluir_aluno.grid(row=3, column=0, columnspan=2, pady=10)

    label_inscricao = ctk.CTkLabel(frame_aluno, text="Inscrever Aluno em Disciplina", font=("Arial", 16))
    label_inscricao.grid(row=5, column=0, columnspan=2, pady=10)

    label_id_aluno = ctk.CTkLabel(frame_aluno, text="ID do Aluno:")
    label_id_aluno.grid(row=6, column=0, pady=5)
    entry_id_aluno = ctk.CTkEntry(frame_aluno)
    entry_id_aluno.grid(row=6, column=1, pady=5)

    label_id_disciplina = ctk.CTkLabel(frame_aluno, text="ID da Disciplina:")
    label_id_disciplina.grid(row=7, column=0, pady=5)
    entry_id_disciplina = ctk.CTkEntry(frame_aluno)
    entry_id_disciplina.grid(row=7, column=1, pady=5)

    button_inscrever_aluno = ctk.CTkButton(frame_aluno, text="Inscrever", command=inscrever_aluno)
    button_inscrever_aluno.grid(row=8, column=0, columnspan=2, pady=10)
    
    # Frame para inserir notas
    frame_notas = ctk.CTkFrame(inserir_root, corner_radius=10, border_width=2, border_color="lightblue")
    frame_notas.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")

    label_titulo_notas = ctk.CTkLabel(frame_notas, text="Inserir Notas", font=("Arial", 16))
    label_titulo_notas.grid(row=0, column=0, columnspan=2, pady=10)

    label_id_inscricao = ctk.CTkLabel(frame_notas, text="ID do aluno:")
    label_id_inscricao.grid(row=1, column=0, padx=10, pady=5)
    entry_id_inscricao_aluno = ctk.CTkEntry(frame_notas, width=200)
    entry_id_inscricao_aluno.grid(row=1, column=1, padx=10, pady=5)

    label_id_inscricao = ctk.CTkLabel(frame_notas, text="ID do disciplina:")
    label_id_inscricao.grid(row=2, column=0, padx=10, pady=5)
    entry_id_inscricao_disciplina = ctk.CTkEntry(frame_notas, width=200)
    entry_id_inscricao_disciplina.grid(row=2, column=1, padx=10, pady=5)

    label_sm1 = ctk.CTkLabel(frame_notas, text="Nota SM1:")
    label_sm1.grid(row=3, column=0, padx=10, pady=5)
    entry_sm1 = ctk.CTkEntry(frame_notas, width=200)
    entry_sm1.grid(row=3, column=1, padx=10, pady=5)

    label_sm2 = ctk.CTkLabel(frame_notas, text="Nota SM2:")
    label_sm2.grid(row=4, column=0, padx=10, pady=5)
    entry_sm2 = ctk.CTkEntry(frame_notas, width=200)
    entry_sm2.grid(row=4, column=1, padx=10, pady=5)

    label_av = ctk.CTkLabel(frame_notas, text="Nota AV:")
    label_av.grid(row=5, column=0, padx=10, pady=5)
    entry_av = ctk.CTkEntry(frame_notas, width=200)
    entry_av.grid(row=5, column=1, padx=10, pady=5)

    label_avs = ctk.CTkLabel(frame_notas, text="Nota AVS:")
    label_avs.grid(row=6, column=0, padx=10, pady=5)
    entry_avs = ctk.CTkEntry(frame_notas, width=200)
    entry_avs.grid(row=6, column=1, padx=10, pady=5)

    button_incluir_notas = ctk.CTkButton(frame_notas, text="Incluir Notas", command=incluir_notas)
    button_incluir_notas.grid(row=7, column=0, columnspan=2, pady=10)
    
    

    #############    BOTAO De Consulta #########################
    button_voltar = ctk.CTkButton(inserir_root, text="Consultar", command=lambda: voltar(inserir_root))
    button_voltar.grid(row=4, column=0, columnspan=1, pady=10, padx=10, sticky="ew")

    
    #############    BOTAO VOLTAR #########################
    button_voltar = ctk.CTkButton(inserir_root, text="Voltar", command=lambda: voltar(inserir_root))
    button_voltar.grid(row=4, column=2, columnspan=1, pady=10, padx=10, sticky="ew")

    inserir_root.mainloop()

# Função principal para criar a tela inicial

connect_db()

root = ctk.CTk()
root.title("Sistema de Registro de Notas")
root.geometry("400x200")
root.resizable(False, False)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

label_titulo = ctk.CTkLabel(root, text="Sistema de Registro de Notas", font=("Arial", 20))
label_titulo.pack(pady=20)

button_inserir_dados = ctk.CTkButton(root, text="Inserir Dados", command=abrir_inserir_dados)
button_inserir_dados.pack(pady=10)

button_consultar_dados = ctk.CTkButton(root, text="Consultar Dados", command=abrir_consultar_dados)
button_consultar_dados.pack(pady=10)

root.mainloop()