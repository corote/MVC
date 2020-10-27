from flask import Flask, request, render_template
from contextlib import closing
import sqlite3

############################
#### Definições da API. ####
############################

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html", mensagem = "")

@app.route("/menu")
def menu():
    return render_template("menu.html", mensagem = "")

@app.route("/chat")
def chat():
    return render_template("chat.html", mensagem = "")

######################################
#### Definições da API Psicologo. ####
######################################

@app.route("/psicologo")
def listar_psicologos_api():
    return render_template("lista_psicologos.html", psicologos = listar_psicologo())

@app.route("/psicologo/novo", methods = ["GET"])
def form_criar_psicologo_api():
    return render_template("formulario_cadastro_psicologos.html", id_psicologo = "novo", nome_psicologo = "", nome_social_psicologo = "", rg_psicologo = "", cpf_psicologo = "", crp = "", sexo = "", email = "", data_nascimento_psicologo = "", data_validade_crp = "", autonomo = "", cnpj = "", usuario = "", senha = "")

@app.route("/psicologo/novo", methods = ["POST"])
def criar_psicologo_api():
    nome_psicologo = request.form["nome_psicologo"]
    nome_social_psicologo = request.form["nome_social_psicologo"]
    rg_psicologo = request.form["rg_psicologo"]
    cpf_psicologo = request.form["cpf_psicologo"]
    crp = request.form["crp"]
    sexo = request.form["sexo"]
    email = request.form["email"]
    data_nascimento_psicologo = request.form["data_nascimento_psicologo"]
    data_validade_crp = request.form["data_validade_crp"]    
    autonomo = request.form["autonomo"]
    cnpj = request.form["cnpj"]
    usuario = request.form["usuario"]
    senha = request.form["senha"]
#    id_psicologo = verificar_usuario(usuario)
#    if id_psicologo != None:
#        return render_template("menu.html", mensagem = f"O usuario já existe.")
    id_psicologo = criar_psicologo(nome_psicologo, nome_social_psicologo, rg_psicologo, cpf_psicologo, crp, sexo, email, data_nascimento_psicologo, data_validade_crp, autonomo, cnpj, usuario, senha)
    return render_template("menu.html", mensagem = f"O psicólogo foi criado com o id {id_psicologo}.")

@app.route("/psicologo/<int:id_psicologo>", methods = ["GET"])
def form_alterar_psicologo_api(id_psicologo):
    psicologo = consultar_psicologo(id_psicologo)
    return render_template("formulario_cadastro_psicologos.html", id_psicologo = id_psicologo, nome_psicologo = psicologo['nome_psicologo'], nome_social_psicologo = psicologo['nome_social_psicologo'], rg_psicologo = psicologo['rg_psicologo'], cpf_psicologo = psicologo['cpf_psicologo'], crp = psicologo['crp'], sexo = psicologo['sexo'], email = psicologo['email'], data_nascimento_psicologo = psicologo['data_nascimento_psicologo'], data_validade_crp = psicologo['data_validade_crp'], autonomo = psicologo['autonomo'], cnpj = psicologo['cnpj'], usuario = psicologo['usuario'], senha = psicologo["senha"])

@app.route("/psicologo/<int:id_psicologo>", methods = ["POST"])
def alterar_psicologo_api(id_psicologo):
    nome_psicologo = request.form["nome_psicologo"]
    nome_social_psicologo = request.form["nome_social_psicologo"]
    rg_psicologo = request.form["rg_psicologo"]
    cpf_psicologo = request.form["cpf_psicologo"]
    crp = request.form["crp"]
    sexo = request.form["sexo"]
    email = request.form["email"]
    data_nascimento_psicologo = request.form["data_nascimento_psicologo"]
    data_validade_crp = request.form["data_validade_crp"]    
    autonomo = request.form["autonomo"]
    cnpj = request.form["cnpj"]
    usuario = request.form["usuario"]
    senha = request.form["senha"]
    psicologo = consultar_psicologo(id_psicologo)
    if psicologo == None:
        return render_template("menu.html", mensagem = f"Esse psicólogo nem mesmo existia mais.")
    editar_psicologo(id_psicologo, nome_psicologo, nome_social_psicologo, rg_psicologo, cpf_psicologo, crp, sexo, email, data_nascimento_psicologo, data_validade_crp, autonomo, cnpj, usuario, senha)
    return render_template("menu.html", mensagem = f"O psicólogo com o id {id_psicologo} foi editado.")

@app.route("/psicologo/<int:id_psicologo>", methods = ["DELETE"])
def deletar_psicologo_api(id_psicologo):
    psicologo = consultar_psicologo(id_psicologo)
    if psicologo == None:
        return render_template("menu.html", mensagem = "Esse psicólogo nem mesmo existia mais.")
    deletar_psicologo(id_psicologo)
    return render_template("menu.html", mensagem = f"O psicólogo com o id {id_psicologo} foi excluído.")

######################################
#### Definições da API Paciente. ####
######################################

@app.route("/paciente")
def listar_pacientes_api():
    return render_template("lista_paciente.html", pacientes = listar_paciente())

@app.route("/paciente/novo", methods = ["GET"])
def form_criar_paciente_api():
    return render_template("formulario_cadastro_paciente.html", id_paciente = "novo", nome_paciente = "", nome_social_paciente = "", rg_paciente = "", cpf_paciente = "", data_nascimento_paciente = "", profissao = "")

@app.route("/paciente/novo", methods = ["POST"])
def criar_paciente_api():
    nome_paciente = request.form["nome_paciente"]
    nome_social_paciente = request.form["nome_social_paciente"]
    rg_paciente = request.form["rg_paciente"]
    cpf_paciente = request.form["cpf_paciente"]
    data_nascimento_paciente = request.form["data_nascimento_paciente"]
    profissao = request.form["profissao"]
    id_paciente = criar_paciente(nome_paciente, nome_social_paciente, rg_paciente, cpf_paciente, data_nascimento_paciente, profissao)
    return render_template("menu.html", mensagem = f"O paciente foi criado com o id {id_paciente}.")

@app.route("/paciente/<int:id_paciente>", methods = ["GET"])
def form_alterar_paciente_api(id_paciente):
    paciente = consultar_paciente(id_paciente)
    return render_template("formulario_cadastro_paciente.html", id_paciente = id_paciente, nome_paciente = paciente['nome_paciente'], nome_social_paciente = paciente['nome_social_paciente'], rg_paciente = paciente['rg_paciente'], cpf_paciente = paciente["cpf_paciente"], data_nascimento_paciente = paciente["data_nascimento_paciente"], profissao = paciente["profissao"])

@app.route("/paciente/<int:id_paciente>", methods = ["POST"])
def alterar_paciente_api(id_paciente):
    nome_paciente = request.form["nome_paciente"]
    nome_social_paciente = request.form["nome_social_paciente"]
    rg_paciente = request.form["rg_paciente"]
    cpf_paciente = request.form["cpf_paciente"]
    data_nascimento_paciente = request.form["data_nascimento_paciente"]
    profissao = request.form["profissao"]
    paciente = consultar_paciente(id_paciente)
    if paciente == None:
        return render_template("menu.html", mensagem = f"Esse paciente nem mesmo existia mais.")
    editar_paciente(id_paciente, nome_paciente, nome_social_paciente, rg_paciente, cpf_paciente, data_nascimento_paciente, profissao)
    return render_template("menu.html", mensagem = f"O paciente com o id {id_paciente} foi editado.")

@app.route("/paciente/<int:id_paciente>", methods = ["DELETE"])
def deletar_paciente_api(id_paciente):
    paciente = consultar_paciente(id_paciente)
    if paciente == None:
        return render_template("menu.html", mensagem = "Esse paciente nem mesmo existia mais.")
    deletar_paciente(id_paciente)
    return render_template("menu.html", mensagem = f"O paciente com o id {id_paciente} foi excluído.")

#######################################
#### Definições da API Prontuario. ####
#######################################

@app.route("/prontuario")
def listar_prontuario_api():
    return render_template("lista_prontuario.html", prontuarios = listar_prontuario())

@app.route("/prontuario/novo", methods = ["GET"])
def form_criar_prontuario_api():
    return render_template("formulario_cadastro_prontuario.html", id_prontuario = "novo", id_paciente = "", id_psicologo = "", diagnostico = "", data_inicio_tratamento = "", data_final_tratamento = "", pacientes = listar_paciente(), psicologos = listar_psicologo())

@app.route("/prontuario/novo", methods = ["POST"])
def criar_prontuario_api():
    id_paciente = request.form["id_paciente"]
    id_psicologo = request.form["id_psicologo"]
    diagnostico = request.form["diagnostico"]
    data_inicio_tratamento = request.form["data_inicio_tratamento"]
    data_final_tratamento = request.form["data_final_tratamento"]
    id_prontuario = criar_prontuario(id_paciente, id_psicologo, diagnostico, data_inicio_tratamento, data_final_tratamento)
    return render_template("menu.html", mensagem = f"O prontuário foi criado com o id {id_prontuario}.")

@app.route("/prontuario/<int:id_prontuario>", methods = ["GET"])
def form_alterar_prontuario_api(id_prontuario):
    prontuario = consultar_prontuario(id_prontuario)
    return render_template("formulario_cadastro_prontuario.html", id_prontuario = id_prontuario, diagnostico = prontuario['diagnostico'], data_inicio_tratamento = prontuario['data_inicio_tratamento'], data_final_tratamento = prontuario['data_final_tratamento'], pacientes = listar_paciente(), psicologos = listar_psicologo())

@app.route("/prontuario/<int:id_prontuario>", methods = ["POST"])
def alterar_prontuario_api(id_prontuario):
    id_paciente = request.form["nome_paciente"]
    id_psicologo = request.form["nome_psicologo"]
    diagnostico = request.form["diagnostico"]
    data_inicio_tratamento = request.form["data_inicio_tratamento"]
    data_final_tratamento = request.form["data_final_tratamento"]
    prontuario = consultar_prontuario(id_prontuario)
    if prontuario == None:
        return render_template("menu.html", mensagem = f"Essa anotação nem mesmo existia mais.")
    editar_prontuario(id_prontuario, id_paciente, id_psicologo, diagnostico, data_inicio_tratamento, data_final_tratamento)
    return render_template("menu.html", mensagem = f"O prontuário com o id {id_prontuario} foi editado.")

@app.route("/prontuario/<int:id_prontuario>", methods = ["DELETE"])
def deletar_prontuario_api(id_prontuario):
    prontuario = consultar_anotacoes(id_prontuario)
    if prontuario == None:
        return render_template("menu.html", mensagem = "Essa anotação nem mesmo existia mais.")
    deletar_prontuario(id_prontuario)
    return render_template("menu.html", mensagem = f"O prontuário com o id {id_prontuario} foi excluído.")

#####################################
#### Definições da API Consulta. ####
#####################################

@app.route("/consulta")
def listar_consultas_api():
    return render_template("lista_consultas.html", consultas = listar_consultas())

@app.route("/consulta/novo", methods = ["GET"])
def form_criar_consulta_api():
    return render_template("formulario_cadastro_consulta.html", id_consulta = "novo", dataa = "", hora = "", endereco = "", id_paciente = "", id_psicologo = "", pacientes = listar_paciente(), psicologos = listar_psicologo())

@app.route("/consulta/novo", methods = ["POST"])
def criar_consulta_api():
    dataa = request.form["dataa"]
    hora = request.form["hora"]
    endereco = request.form["endereco"]
    id_paciente = request.form["id_paciente"]
    id_psicologo = request.form["id_psicologo"]
    id_consulta = criar_consulta(dataa, hora, endereco, id_paciente, id_psicologo)
    return render_template("menu.html", mensagem = f"A consulta foi criado com o id {id_consulta}.")

@app.route("/consulta/<int:id_consulta>", methods = ["GET"])
def form_alterar_consulta_api(id_consulta):
    consulta = consultar_consulta(id_consulta)
    return render_template("formulario_cadastro_consulta.html", id_consulta = id_consulta, dataa = consulta['dataa'], hora = consulta['hora'], endereco = consulta['endereco'], pacientes = listar_paciente(), psicologos = listar_psicologo())

@app.route("/consulta/<int:id_consulta>", methods = ["POST"])
def alterar_consulta_api(id_consulta):
    dataa = request.form["dataa"]
    hora = request.form["hora"]
    endereco = request.form["endereco"]
    id_paciente = request.form["id_paciente"]
    id_psicologo = request.form["id_psicologo"]
    consulta = consultar_consulta(id_consulta)
    if consulta == None:
        return render_template("menu.html", mensagem = f"Essa consulta nem mesmo existia mais.")
    editar_consulta(id_consulta, dataa, hora, endereco, id_paciente, id_psicologo)
    return render_template("menu.html", mensagem = f"A consulta com o id {id_consulta} foi editado.")

@app.route("/consulta/<int:id_consulta>", methods = ["DELETE"])
def deletar_consulta_api(id_consulta):
    consulta = consultar_consulta(id_consulta)
    if consulta == None:
        return render_template("menu.html", mensagem = "Esse psicólogo nem mesmo existia mais.")
    deletar_consulta(id_consulta)
    return render_template("menu.html", mensagem = f"A consulta com o id {id_consulta} foi excluído.")

######################################
#### Definições da API Anotações. ####
######################################

@app.route("/anotacoes")
def listar_anotacoes_api():
    return render_template("lista_anotacoes.html", anotacoes_ = listar_anotacoes())

@app.route("/anotacoes/novo", methods = ["GET"])
def form_criar_anotacoes_api():
    return render_template("formulario_cadastro_anotacoes.html", id_anotacoes = "novo", data_anotacoes = "", texto_anotacoes = "", prontuarios = listar_prontuario())

@app.route("/anotacoes/novo", methods = ["POST"])
def criar_anotacoes_api():
    data_anotacoes = request.form["data_anotacoes"]
    texto_anotacoes = request.form["texto_anotacoes"]
    id_prontuario = request.form["id_prontuario"]
    id_anotacoes = criar_anotacoes(data_anotacoes, texto_anotacoes, id_prontuario)
    return render_template("menu.html", mensagem = f"A anotação foi criada com o id {id_anotacoes}.")

@app.route("/anotacoes/<int:id_anotacoes>", methods = ["GET"])
def form_alterar_anotacoes_api(id_anotacoes):
    anotacoes = consultar_anotacoes(id_anotacoes)
    return render_template("formulario_cadastro_anotacoes.html", id_anotacoes = id_anotacoes, data_anotacoes = anotacoes['data_anotacoes'], texto_anotacoes = anotacoes['texto_anotacoes'], id_prontuario = anotacoes['id_prontuario'], prontuarios = listar_prontuario())

@app.route("/anotacoes/<int:id_anotacoes>", methods = ["POST"])
def alterar_anotacoes_api(id_anotacoes):
    data_anotacoes = request.form["data_anotacoes"]
    texto_anotacoes = request.form["texto_anotacoes"]
    id_prontuario = request.form["id_prontuario"]
    anotacoes = consultar_anotacoes(id_anotacoes)
    if anotacoes == None:
        return render_template("menu.html", mensagem = f"Essa anotação nem mesmo existia mais.")
    editar_anotacoes(id_anotacoes, data_anotacoes, texto_anotacoes, id_prontuario)
    return render_template("menu.html", mensagem = f"A anotação com o id {id_anotacoes} foi editada.")

@app.route("/anotacoes/<int:id_anotacoes>", methods = ["DELETE"])
def deletar_anotacoes_api(id_anotacoes):
    anotacoes = consultar_anotacoes(id_anotacoes)
    if anotacoes == None:
        return render_template("menu.html", mensagem = "Essa anotação nem mesmo existia mais.")
    deletar_anotacoes(id_anotacoes)
    return render_template("menu.html", mensagem = f"A anotação com o id {id_anotacoes} foi excluída.")

###############################################
#### Funções auxiliares de banco de dados. ####
###############################################

# Converte uma linha em um dicionário.
def row_to_dict(description, row):
    if row == None:
        return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

# Converte uma lista de linhas em um lista de dicionários.
def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result

####################################
#### Definições básicas de DAO. ####
####################################

sql_create = """
CREATE TABLE IF NOT EXISTS psicologo (
    id_psicologo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_psicologo VARCHAR(100) NOT NULL,
    nome_social_psicologo VARCHAR(50) NOT NULL,
    rg_psicologo VARCHAR(11) NOT NULL,
    cpf_psicologo VARCHAR(14) NOT NULL,
    crp VARCHAR(50) NOT NULL,
    sexo VARCHAR(1) NOT NULL,
    email VARCHAR(30) NOT NULL,
    data_nascimento_psicologo date NOT NULL,
    data_validade_crp date NOT NULL,    
    autonomo VARCHAR(1) NOT NULL,
    cnpj VARCHAR(20),
    usuario VARCHAR(20) NOT NULL,
    senha VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS paciente (
    id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_paciente VARCHAR(50) NOT NULL,
    nome_social_paciente VARCHAR(50) NOT NULL,
    rg_paciente VARCHAR(50) NOT NULL,
    cpf_paciente VARCHAR(50) NOT NULL,
    data_nascimento_paciente date NOT NULL,    
    profissao VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS prontuario (
    id_prontuario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_paciente INTEGER NOT NULL,
    id_psicologo INTEGER NOT NULL,
    diagnostico VARCHAR(50) NOT NULL,
    data_inicio_tratamento date NOT NULL,
    data_final_tratamento date NOT NULL,
    FOREIGN KEY(id_psicologo) REFERENCES psicologo(id_prontuario),
    FOREIGN KEY(id_paciente) REFERENCES paciente(id_prontuario)
);

CREATE TABLE IF NOT EXISTS consulta (
    id_consulta INTEGER PRIMARY KEY AUTOINCREMENT,
    dataa date NOT NULL,
    hora time NOT NULL,
    endereco VARCHAR(50) NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_psicologo INTEGER NOT NULL,
    FOREIGN KEY(id_paciente) REFERENCES paciente(id_consulta),
    FOREIGN KEY(id_psicologo) REFERENCES psicologo(id_consulta)
);

CREATE TABLE IF NOT EXISTS anotacoes (
    id_anotacoes INTEGER PRIMARY KEY AUTOINCREMENT,
    data_anotacoes VARCHAR(10) NOT NULL,
    texto_anotacoes VARCHAR(255) NOT NULL,
    id_prontuario INTEGER NOT NULL,
    FOREIGN KEY(id_prontuario) REFERENCES prontuario(id_anotacoes)
);
"""
##  acresentar no BD paciente depois
# "tipo_sanguineo VARCHAR(50) NOT NULL,"
## -------------

def conectar():
    return sqlite3.connect('banco.db')

def criar_bd():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.executescript(sql_create)
        con.commit()

################################
#### Funções do Psicologo. ####
################################

def listar_psicologo():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT p.id_psicologo, p.nome_psicologo, p.nome_social_psicologo, p.rg_psicologo, p.cpf_psicologo, p.crp, p.sexo, p.email, p.data_nascimento_psicologo, p.data_validade_crp, p.autonomo, p.cnpj, p.usuario FROM psicologo p")
        return rows_to_dict(cur.description, cur.fetchall())

def consultar_psicologo(id_psicologo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT p.id_psicologo, p.nome_psicologo, p.nome_social_psicologo, p.rg_psicologo, p.cpf_psicologo, p.crp, p.sexo, p.email, p.data_nascimento_psicologo, p.data_validade_crp, p.autonomo, p.cnpj, p.usuario, p.senha FROM psicologo p WHERE id_psicologo = ?", (id_psicologo, ))
        return row_to_dict(cur.description, cur.fetchone())

def criar_psicologo(nome_psicologo, nome_social_psicologo, rg_psicologo, cpf_psicologo, crp, sexo, email, data_nascimento_psicologo, data_validade_crp, autonomo, cnpj, usuario, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO psicologo (nome_psicologo, nome_social_psicologo, rg_psicologo, cpf_psicologo, crp, sexo, email, data_nascimento_psicologo, data_validade_crp, autonomo, cnpj, usuario, senha) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome_psicologo, nome_social_psicologo, rg_psicologo, cpf_psicologo, crp, sexo, email, data_nascimento_psicologo, data_validade_crp, autonomo, cnpj, usuario, senha))
        id_psicologo = cur.lastrowid
        con.commit()
        return id_psicologo

def editar_psicologo(id_psicologo, nome_psicologo, nome_social_psicologo, rg_psicologo, cpf_psicologo, crp, sexo, email, data_nascimento_psicologo, data_validade_crp, autonomo, cnpj, usuario, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE psicologo SET nome_psicologo = ?, nome_social_psicologo = ?, rg_psicologo = ?, cpf_psicologo = ?, crp = ?, sexo = ?, email = ?, data_nascimento_psicologo = ?, data_validade_crp = ?, autonomo = ?, cnpj = ?, usuario = ?, senha = ? WHERE id_psicologo = ?", (nome_psicologo, nome_social_psicologo, rg_psicologo, cpf_psicologo, crp, sexo, email, data_nascimento_psicologo, data_validade_crp, autonomo, cnpj, usuario, senha, id_psicologo))
        con.commit()

def deletar_psicologo(id_psicologo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM psicologo WHERE id_psicologo = ?", (id_psicologo, ))
        con.commit()

##############################
#### Funções do Paciente ####
##############################

def listar_paciente():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT p.id_paciente, p.nome_paciente, p.nome_social_paciente, p.rg_paciente, p.cpf_paciente, p.data_nascimento_paciente, p.profissao FROM paciente p")
        return rows_to_dict(cur.description, cur.fetchall())

def consultar_paciente(id_paciente):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT p.id_paciente, p.nome_paciente, p.nome_social_paciente, p.rg_paciente, p.cpf_paciente, p.data_nascimento_paciente, p.profissao FROM paciente p WHERE id_paciente = ?", (id_paciente, ))
        return row_to_dict(cur.description, cur.fetchone())

def criar_paciente(nome_paciente, nome_social_paciente, rg_paciente, cpf_paciente, data_nascimento_paciente, profissao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO paciente (nome_paciente, nome_social_paciente, rg_paciente, cpf_paciente, data_nascimento_paciente, profissao) VALUES (?, ?, ?, ?, ?, ?)", (nome_paciente, nome_social_paciente, rg_paciente, cpf_paciente, data_nascimento_paciente, profissao))
        id_paciente = cur.lastrowid
        con.commit()
        return id_paciente

def editar_paciente(id_paciente, nome_paciente, nome_social_paciente, rg_paciente, cpf_paciente, data_nascimento_paciente, profissao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE paciente SET nome_paciente = ?, nome_social_paciente = ?, rg_paciente = ?, cpf_paciente = ?, data_nascimento_paciente = ?, profissao = ? WHERE id_paciente = ?", (nome_paciente, nome_social_paciente, rg_paciente, cpf_paciente, data_nascimento_paciente, profissao, id_paciente))
        con.commit()

def deletar_paciente(id_paciente):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM paciente WHERE id_paciente = ?", (id_paciente, ))
        con.commit()

###############################
#### Funções do Prontuario ####
###############################

def listar_prontuario():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT pron.id_prontuario, pac.nome_paciente, psi.nome_psicologo, pron.diagnostico, pron.data_inicio_tratamento, pron.data_final_tratamento FROM prontuario pron, paciente pac, psicologo psi")
        return rows_to_dict(cur.description, cur.fetchall())

def consultar_prontuario(id_prontuario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT pron.id_prontuario, pac.nome_paciente, psi.nome_psicologo, pron.diagnostico, pron.data_inicio_tratamento, pron.data_final_tratamento FROM prontuario pron INNER JOIN paciente pac ON pron.id_paciente = pac.id_paciente INNER JOIN psicologo psi ON pron.id_psicologo = psi.id_psicologo WHERE id_prontuario = ? ", (id_prontuario, ))
        return row_to_dict(cur.description, cur.fetchone())

def criar_prontuario(id_paciente, id_psicologo, diagnostico, data_inicio_tratamento, data_final_tratamento):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO prontuario (id_paciente, id_psicologo, diagnostico, data_inicio_tratamento, data_final_tratamento) VALUES (?, ?, ?, ?, ?)", (id_paciente, id_psicologo, diagnostico, data_inicio_tratamento, data_final_tratamento))
        id_prontuario = cur.lastrowid
        con.commit()
        return id_prontuario

def editar_prontuario(id_prontuario, id_paciente, id_psicologo, diagnostico, data_inicio_tratamento, data_final_tratamento):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE prontuario SET id_paciente = ?, id_psicologo = ?, diagnostico = ?, data_inicio_tratamento = ?, data_final_tratamento = ? WHERE id_anotacoes = ?", (id_paciente, id_psicologo, diagnostico, data_inicio_tratamento, data_final_tratamento, id_prontuario))
        con.commit()

def deletar_prontuario(id_prontuario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM prontuario WHERE id_prontuario = ?", (id_prontuario, ))
        con.commit()

#############################
#### Funções da Consulta ####
#############################

def listar_consultas():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT con.id_consulta, pac.nome_paciente, con.dataa, con.hora, con.endereco, psi.nome_psicologo FROM consulta con , paciente pac, psicologo psi")
        return rows_to_dict(cur.description, cur.fetchall())

def consultar_consulta(id_consulta):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT con.id_consulta, pac.nome_paciente, con.dataa, con.hora, con.endereco, psi.nome_psicologo FROM consulta con INNER JOIN paciente pac ON con.id_paciente = pac.id_paciente INNER JOIN psicologo psi ON con.id_psicologo = psi.id_psicologo WHERE id_consulta = ?", (id_consulta, ))
        return row_to_dict(cur.description, cur.fetchone())

def criar_consulta(dataa, hora, endereco, id_paciente, id_psicologo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO consulta (dataa, hora, endereco, id_paciente, id_psicologo) VALUES (?, ?, ?, ?, ?)", (dataa, hora, endereco, id_paciente, id_psicologo))
        id_consulta = cur.lastrowid
        con.commit()
        return id_consulta

def editar_consulta(id_consulta, dataa, hora, endereco, id_paciente, id_psicologo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE consulta SET dataa = ?, hora = ?, endereco = ?, id_paciente = ?, id_psicologo = ? WHERE id_consulta = ?", (dataa, hora, endereco, id_paciente, id_psicologo, id_consulta))
        con.commit()

def deletar_consulta(id_consulta):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM consulta WHERE id_consulta = ?", (id_consulta, ))
        con.commit()

##############################
#### Funções da Anotações ####
##############################

def listar_anotacoes():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT an.id_anotacoes, an.data_anotacoes, an.texto_anotacoes, pron.id_prontuario FROM anotacoes an, prontuario pron")
        return rows_to_dict(cur.description, cur.fetchall())

def consultar_anotacoes(id_anotacoes):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT an.id_anotacoes, an.data_anotacoes, an.texto_anotacoes, pron.id_prontuario FROM anotacoes an INNER JOIN prontuario pron ON an.id_prontuario = pron.id_prontuario WHERE id_anotacoes = ? ", (id_anotacoes, ))
        return row_to_dict(cur.description, cur.fetchone())

def criar_anotacoes(data_anotacoes, texto_anotacoes, id_prontuario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO anotacoes (data_anotacoes, texto_anotacoes, id_prontuario) VALUES (?, ?, ?)", (data_anotacoes, texto_anotacoes, id_prontuario))
        id_anotacoes = cur.lastrowid
        con.commit()
        return id_anotacoes

def editar_anotacoes(id_anotacoes, data_anotacoes, texto_anotacoes, id_prontuario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE anotacoes SET data_anotacoes = ?, texto_anotacoes = ?, id_prontuario = ? WHERE id_anotacoes = ?", (data_anotacoes, texto_anotacoes, id_prontuario, id_anotacoes))
        con.commit()

def deletar_anotacoes(id_anotacoes):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM anotacoes WHERE id_anotacoes = ?", (id_anotacoes, ))
        con.commit()

########################
#### Inicialização. ####
########################

if __name__ == "__main__":
    criar_bd()
    app.run(host='localhost', port=8080, debug=True)