import os
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

from flask import Flask, render_template, redirect, session
from flask_security import (
    Security,
    current_user,
    auth_required,
    hash_password,
    SQLAlchemySessionUserDatastore,
)
from database import db_session, init_db
from models.auth import User, Role

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename

# Create app
app = Flask(__name__)
app.config["DEBUG"] = True

app.config["UPLOAD_FOLDER"] = "uploads"

# Generate a nice key using secrets.token_urlsafe()
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
)
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
    "SECURITY_PASSWORD_SALT", "146585145368132386173505678016728509634"
)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)


# Support for file upload
def get_upload_folder():
    upload_folder = app.config["UPLOAD_FOLDER"]
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    return upload_folder


def save_file(file_form):
    folder = get_upload_folder()  # Create the upload folder if necessary
    filename = secure_filename(file_form.filename)
    if filename != "":
        file_path = os.path.join(folder, filename)
        file_form.save(file_path)
        return file_path
    return None


# Forms
class MyForm(FlaskForm):
    am_01_equi = FileField("am_01_equi")
    am_01_form = FileField("am_01_form")
    am_01_peukert = FileField("am_01_peukert")
    am_01_qdca_mainres = FileField("am_01_qdca_mainres")
    am_01_qdca = FileField("am_01_qdca")
    am_01_recarga_dhc = FileField("am_01_recarga_dhc")
    am_01_recarga_qdca = FileField("am_01_recarga_qdca")
    am_01_recarga_dch_prot = FileField("am_01_recarga_dch_prot")
    am_02_equi = FileField("am_02_equi")
    am_02_form = FileField("am_02_form")
    am_02_peukert = FileField("am_02_peukert")
    am_02_qdca_mainres = FileField("am_02_qdca_mainres")
    am_02_qdca = FileField("am_02_qdca")
    am_02_alta_dca = FileField("am_02_alta_dca")
    am_02_qdca = FileField("am_02_qdca")
    am_02_dch_prot = FileField("am_02_dch_prot")
    am_03_agua = FileField("am_03_agua")
    am_03_equi = FileField("am_03_equi")
    am_03_form = FileField("am_03_form")
    am_03_pol = FileField("am_03_pol")
    am_04_cons = FileField("am_04_cons")
    am_04_equi = FileField("am_04_equi")
    am_04_form = FileField("am_04_form")
    am_04_pol = FileField("am_04_pol")
    am_05_equi = FileField("am_05_equi")
    am_05_form = FileField("am_05_form")
    am_05_peukert = FileField("am_05_peukert")
    am_05_qdca_mainres = FileField("am_05_qdca_mainres")
    am_05_qdca = FileField("am_05_qdca")
    am_05_rec_alta_dch = FileField("am_05_rec_alta_dch")
    am_05_rec_qdca = FileField("am_05_rec_qdca")
    am_05_alta_dch = FileField("am_05_alta_dch")
    am_06_equi = FileField("am_06_equi")
    am_06_form = FileField("am_06_form")
    am_06_peukert = FileField("am_06_peukert")
    am_06_qdca_mainres = FileField("am_06_qdca_mainres")
    am_06_qdca = FileField("am_06_qdca")
    am_06_rec_alta_dch = FileField("am_06_rec_alta_dch")
    am_06_rec_qdca = FileField("am_06_rec_qdca")
    am_06_alta_dch = FileField("am_06_alta_dch")
    am_07_consu = FileField("am_07_consu")
    am_07_equi = FileField("am_07_equi")
    am_07_form = FileField("am_07_form")
    am_07_pola = FileField("am_07_pola")
    am_08_consu = FileField("am_08_consu")
    am_08_equi = FileField("am_08_equi")
    am_08_form = FileField("am_08_form")
    am_08_pola = FileField("am_08_pola")
    upload = SubmitField("upload")


# Views
@app.route("/dac")
@auth_required()
def dac():
    nome = "Neto"
    resultado = 10 + 10
    return render_template("dac.html", nome=nome, dado=resultado)


@app.route("/polarizacao")
@auth_required()
def polarizacao():
    return render_template("polarizacao.html")


@app.route("/pekeurt")
@auth_required()
def pekeurt():
    
    #------------------- AM01--------------------"
    
# Captura o caminho do arquivo durante a sessão
    caminho_arquivo = session["am_01_equi"] 

# Carrega o arquivo XLSX
    xlsx_file = pd.read_excel(caminho_arquivo)

# Define o caminho do arquivo CSV de saída
    caminho_csv = caminho_arquivo.replace(".xlsx", ".csv")

# Salva o arquivo CSV
    xlsx_file.to_csv(caminho_csv, index=False, sep=',')
        #EQUALIZAÇÃO
     
        # Carrega os dados do arquivo CSV para o DataFrame do pandas
    consultaequalizacaoAm01 = pd.read_csv(caminho_csv, delimiter=',', on_bad_lines='skip', low_memory=False) 
    consultaequalizacaoAm01['Voltage'] = consultaequalizacaoAm01['Voltage'].str.replace(',', '.')
    consultaequalizacaoAm01['Current'] = consultaequalizacaoAm01['Current'].str.replace(',', '.')
        # Converte a coluna 'Voltage' para float, pulando os valores de string
    consultaequalizacaoAm01['Voltage'] = pd.to_numeric(consultaequalizacaoAm01['Voltage'], errors='coerce')
    consultaequalizacaoAm01['Current'] = pd.to_numeric(consultaequalizacaoAm01['Current'], errors='coerce').abs()

        # Arredonda a coluna 'Voltage' para duas casas decimais
    consultaequalizacaoAm01['Voltage'] = consultaequalizacaoAm01['Voltage'].round(3)

        # Filtra as linhas que contém o valor desejado, remove as linhas com valores nulos e em que a coluna 'Current' é igual a zero
    linha_especificaequalizacaoAm01 = consultaequalizacaoAm01.loc[(consultaequalizacaoAm01['Voltage'] == 1.750) & (consultaequalizacaoAm01['Step Time'] != 0.000000) & (consultaequalizacaoAm01['Current'] != 0.000)].drop_duplicates(subset=['Current'])

        # Converte o formato de 'Step Time' para horas
    linha_especificaequalizacaoAm01['Step Time'] = pd.to_timedelta(linha_especificaequalizacaoAm01['Step Time'])
    linha_especificaequalizacaoAm01['Step Time'] = linha_especificaequalizacaoAm01['Step Time'].dt.total_seconds() / 3600

    linha_especificaequalizacaoAm01=(linha_especificaequalizacaoAm01[['Step Time', 'Current']])

        #PEUKERT

 # Captura o caminho do arquivo durante a sessão
    caminho_arquivo1 = session["am_01_peukert"] 

# Carrega o arquivo XLSX
    xlsx_file = pd.read_excel(caminho_arquivo1)

# Define o caminho do arquivo CSV de saída
    caminho_csv1 = caminho_arquivo.replace(".xlsx", ".csv")

# Salva o arquivo CSV
    xlsx_file.to_csv(caminho_csv1, index=False, sep=',')

    consultapeukertAm01 = pd.read_csv(caminho_csv1, delimiter=',', on_bad_lines='skip', low_memory=False)
        # Substitui vírgula por ponto
    consultapeukertAm01['Voltage'] = consultapeukertAm01['Voltage'].str.replace(',', '.')
    consultapeukertAm01['Current'] = consultapeukertAm01['Current'].str.replace(',', '.')
        # Converte a coluna 'Voltage' para float, pulando os valores de string
    consultapeukertAm01['Voltage'] = pd.to_numeric(consultapeukertAm01['Voltage'], errors='coerce')
    consultapeukertAm01['Current'] = pd.to_numeric(consultapeukertAm01['Current'], errors='coerce').abs()

        # Arredonda a coluna 'Voltage' para duas casas decimais
    consultapeukertAm01['Voltage'] = consultapeukertAm01['Voltage'].round(3)

        # Filtra as linhas que contém o valor desejado, remove as linhas com valores nulos e em que a coluna 'Current' é igual a zero
    linha_especificapeukertAm01 = consultapeukertAm01.loc[(consultapeukertAm01['Voltage'] == 1.750) & (consultapeukertAm01['Step Time'] != 0.000000) & (consultapeukertAm01['Current'] != 0.000)].drop_duplicates(subset=['Current'])

        # Converte o formato de 'Step Time' para horas
    linha_especificapeukertAm01['Step Time'] = pd.to_timedelta(linha_especificapeukertAm01['Step Time'])
    linha_especificapeukertAm01['Step Time'] = linha_especificapeukertAm01['Step Time'].dt.total_seconds() / 3600

    linha_especificapeukertAm01=(linha_especificapeukertAm01[['Step Time', 'Current']])


    am01_CBI22076 = pd.concat([linha_especificaequalizacaoAm01, linha_especificapeukertAm01])
    am01_CBI22076['Step Time'] = am01_CBI22076['Step Time'].round(3)
    am01_CBI22076['Current'] = am01_CBI22076['Current'].round(3)
    

    #-----------------------------AM02----------------------------
    # Captura o caminho do arquivo durante a sessão
    caminho_arquivo2 = session["am_02_equi"] 

# Carrega o arquivo XLSX
    xlsx_file = pd.read_excel(caminho_arquivo2)

# Define o caminho do arquivo CSV de saída
    caminho_csv2 = caminho_arquivo.replace(".xlsx", ".csv")

# Salva o arquivo CSV
    xlsx_file.to_csv(caminho_csv2, index=False, sep=',')
        #EQUALIZAÇÃO
    
        # Carrega os dados do arquivo CSV para o DataFrame do pandas
    consultaequalizacaoAm02 = pd.read_csv(caminho_csv2, delimiter=',', on_bad_lines='skip', low_memory=False)
        # Substitui vírgula por ponto
    consultaequalizacaoAm02['Voltage'] = consultaequalizacaoAm02['Voltage'].str.replace(',', '.')
    consultaequalizacaoAm02['Current'] = consultaequalizacaoAm02['Current'].str.replace(',', '.')
        # Converte a coluna 'Voltage' para float, pulando os valores de string
    consultaequalizacaoAm02['Voltage'] = pd.to_numeric(consultaequalizacaoAm02['Voltage'], errors='coerce')
    consultaequalizacaoAm02['Current'] = pd.to_numeric(consultaequalizacaoAm02['Current'], errors='coerce').abs()
        # Arredonda a coluna 'Voltage' para duas casas decimais
    consultaequalizacaoAm02['Voltage'] = consultaequalizacaoAm02['Voltage'].round(3)

        # Filtra as linhas que contém o valor desejado, remove as linhas com valores nulos e em que a coluna 'Current' é igual a zero
    linha_especificaequalizacaoAm02 = consultaequalizacaoAm02.loc[(consultaequalizacaoAm02['Voltage'] == 1.750) & (consultaequalizacaoAm02['Step Time'] != 0.000000) & (consultaequalizacaoAm02['Current'] != 0.000)].drop_duplicates(subset=['Current'])

        # Converte o formato de 'Step Time' para horas
    linha_especificaequalizacaoAm02['Step Time'] = pd.to_timedelta(linha_especificaequalizacaoAm02['Step Time'])
    linha_especificaequalizacaoAm02['Step Time'] = linha_especificaequalizacaoAm02['Step Time'].dt.total_seconds() / 3600

    linha_especificaequalizacaoAm02=(linha_especificaequalizacaoAm02[['Step Time', 'Current']])

        #PEUKERT

# Captura o caminho do arquivo durante a sessão
    caminho_arquivo3 = session["am_02_peukert"] 

# Carrega o arquivo XLSX
    xlsx_file = pd.read_excel(caminho_arquivo3)

# Define o caminho do arquivo CSV de saída
    caminho_csv3 = caminho_arquivo.replace(".xlsx", ".csv")

# Salva o arquivo CSV
    xlsx_file.to_csv(caminho_csv3, index=False, sep=',')
    
    consultapeukertAm02 = pd.read_csv(caminho_csv3, delimiter=',', on_bad_lines='skip', low_memory=False)
        # Substitui vírgula por ponto
    consultapeukertAm02['Voltage'] = consultapeukertAm02['Voltage'].str.replace(',', '.')
    consultapeukertAm02['Current'] = consultapeukertAm02['Current'].str.replace(',', '.')
        # Converte a coluna 'Voltage' para float, pulando os valores de string
    consultapeukertAm02['Voltage'] = pd.to_numeric(consultapeukertAm02['Voltage'], errors='coerce')
    consultapeukertAm02['Current'] = pd.to_numeric(consultapeukertAm02['Current'], errors='coerce').abs()
        # Arredonda a coluna 'Voltage' para duas casas decimais
    consultapeukertAm02['Voltage'] = consultapeukertAm02['Voltage'].round(3)

        # Filtra as linhas que contém o valor desejado, remove as linhas com valores nulos e em que a coluna 'Current' é igual a zero
    linha_especificapeukertAm02 = consultapeukertAm02.loc[(consultapeukertAm02['Voltage'] == 1.750) & (consultapeukertAm02['Step Time'] != 0.000000) & (consultapeukertAm02['Current'] != 0.000)].drop_duplicates(subset=['Current'])


        # Filtra as linhas que não são nulas e não possuem o valor '0' na coluna 'Current'
    linha_especificapeukertAm02 = linha_especificapeukertAm02.dropna(subset=['Current'])


        # Converte o formato de 'Step Time' para horas
    linha_especificapeukertAm02['Step Time'] = pd.to_timedelta(linha_especificapeukertAm02['Step Time'])
    linha_especificapeukertAm02['Step Time'] = linha_especificapeukertAm02['Step Time'].dt.total_seconds() / 3600

    linha_especificapeukertAm02=(linha_especificapeukertAm02[['Step Time', 'Current']])

    am02_CBI22076 = pd.concat([linha_especificaequalizacaoAm02, linha_especificapeukertAm02])
    am02_CBI22076['Step Time'] = am02_CBI22076['Step Time'].round(3)
    am02_CBI22076['Current'] = am02_CBI22076['Current'].round(3)
    

    #-----------------------------AM05----------------------------
    # Captura o caminho do arquivo durante a sessão
    caminho_arquivo4 = session["am_05_equi"] 

# Carrega o arquivo XLSX
    xlsx_file = pd.read_excel(caminho_arquivo4)

# Define o caminho do arquivo CSV de saída
    caminho_csv4 = caminho_arquivo.replace(".xlsx", ".csv")

# Salva o arquivo CSV
    xlsx_file.to_csv(caminho_csv4, index=False, sep=',')
    
        #EQUALIZAÇÃO
    
        # Carrega os dados do arquivo CSV para o DataFrame do pandas
    consultaequalizacaoAm05 = pd.read_csv(caminho_csv4, delimiter=',', on_bad_lines='skip', low_memory=False)
        # Substitui vírgula por ponto
    consultaequalizacaoAm05['Voltage'] = consultaequalizacaoAm05['Voltage'].str.replace(',', '.')
    consultaequalizacaoAm05['Current'] = consultaequalizacaoAm05['Current'].str.replace(',', '.')

        # Converte a coluna 'Voltage' para float, pulando os valores de string
    consultaequalizacaoAm05['Voltage'] = pd.to_numeric(consultaequalizacaoAm05['Voltage'], errors='coerce')
    consultaequalizacaoAm05['Current'] = pd.to_numeric(consultaequalizacaoAm05['Current'], errors='coerce').abs()
        # Arredonda a coluna 'Voltage' para duas casas decimais
    consultaequalizacaoAm05['Voltage'] = consultaequalizacaoAm05['Voltage'].round(3)

        # Filtra as linhas que contém o valor desejado, remove as linhas com valores nulos e em que a coluna 'Current' é igual a zero
    linha_especificaequalizacaoAm05 = consultaequalizacaoAm05.loc[(consultaequalizacaoAm05['Voltage'] == 1.750) & (consultaequalizacaoAm05['Step Time'] != 0.000000) & (consultaequalizacaoAm05['Current'] != 0.000)].drop_duplicates(subset=['Current'])

        # Converte o formato de 'Step Time' para horas
    linha_especificaequalizacaoAm05['Step Time'] = pd.to_timedelta(linha_especificaequalizacaoAm05['Step Time'])
    linha_especificaequalizacaoAm05['Step Time'] = linha_especificaequalizacaoAm05['Step Time'].dt.total_seconds() / 3600

    linha_especificaequalizacaoAm05=(linha_especificaequalizacaoAm05[['Step Time', 'Current']])

        #PEUKERT
# Captura o caminho do arquivo durante a sessão
    caminho_arquivo5 = session["am_05_peukert"] 

# Carrega o arquivo XLSX
    xlsx_file = pd.read_excel(caminho_arquivo5)

# Define o caminho do arquivo CSV de saída
    caminho_csv5 = caminho_arquivo.replace(".xlsx", ".csv")

# Salva o arquivo CSV
    xlsx_file.to_csv(caminho_csv5, index=False, sep=',')

    consultapeukertAm05 = pd.read_csv(caminho_csv5, delimiter=',', on_bad_lines='skip', low_memory=False)
        # Substitui vírgula por ponto
    consultapeukertAm05['Voltage'] = consultapeukertAm05['Voltage'].str.replace(',', '.')
    consultapeukertAm05['Current'] = consultapeukertAm05['Current'].str.replace(',', '.')
        # Converte a coluna 'Voltage' para float, pulando os valores de string
    consultapeukertAm05['Voltage'] = pd.to_numeric(consultapeukertAm05['Voltage'], errors='coerce')
    consultapeukertAm05['Current'] = pd.to_numeric(consultapeukertAm05['Current'], errors='coerce').abs()
        # Arredonda a coluna 'Voltage' para duas casas decimais
    consultapeukertAm05['Voltage'] = consultapeukertAm05['Voltage'].round(3)

        # Filtra as linhas que contém o valor desejado, remove as linhas com valores nulos e em que a coluna 'Current' é igual a zero
    linha_especificapeukertAm05 = consultapeukertAm05.loc[(consultapeukertAm05['Voltage'] == 1.750) & (consultapeukertAm05['Step Time'] != 0.000000) & (consultapeukertAm05['Current'] != 0.000)].drop_duplicates(subset=['Current'])

        # Filtra as linhas que não são nulas e não possuem o valor '0' na coluna 'Current'
    linha_especificapeukertAm05 = linha_especificapeukertAm05.dropna(subset=['Current'])

        # Converte o formato de 'Step Time' para horas
    linha_especificapeukertAm05['Step Time'] = pd.to_timedelta(linha_especificapeukertAm05['Step Time'])
    linha_especificapeukertAm05['Step Time'] = linha_especificapeukertAm05['Step Time'].dt.total_seconds() / 3600

    linha_especificapeukertAm05=(linha_especificapeukertAm05[['Step Time', 'Current']])

    am05_CBI22077 = pd.concat([linha_especificaequalizacaoAm05, linha_especificapeukertAm05])
    am05_CBI22077['Step Time'] = am05_CBI22077['Step Time'].round(3)
    am05_CBI22077['Current'] = am05_CBI22077['Current'].round(3)
    

    #-----------------------------AM06----------------------------

    # Captura o caminho do arquivo durante a sessão
    caminho_arquivo6 = session["am_06_equi"] 

# Carrega o arquivo XLSX
    xlsx_file = pd.read_excel(caminho_arquivo6)

# Define o caminho do arquivo CSV de saída
    caminho_csv6 = caminho_arquivo.replace(".xlsx", ".csv")

# Salva o arquivo CSV
    xlsx_file.to_csv(caminho_csv6, index=False, sep=',')

        #EQUALIZAÇÃO
    caminho_arquivo6 = session["am_06_equi"]
        # Carrega os dados do arquivo CSV para o DataFrame do pandas
    consultaequalizacaoAm06 = pd.read_csv(caminho_csv6, delimiter=',', on_bad_lines='skip', low_memory=False)
        # Substitui vírgula por ponto
    consultaequalizacaoAm06['Voltage'] = consultaequalizacaoAm06['Voltage'].str.replace(',', '.')
    consultaequalizacaoAm06['Current'] = consultaequalizacaoAm06['Current'].str.replace(',', '.')
        # Converte as colunas 'Voltage' e 'Current' para float, pulando os valores de string
    consultaequalizacaoAm06['Voltage'] = pd.to_numeric(consultaequalizacaoAm06['Voltage'], errors='coerce')
    consultaequalizacaoAm06['Current'] = pd.to_numeric(consultaequalizacaoAm06['Current'], errors='coerce').abs()
        # Arredonda a coluna 'Voltage' para duas casas decimais
    consultaequalizacaoAm06['Voltage'] = consultaequalizacaoAm06['Voltage'].round(3)

        # Filtra as linhas que contém o valor desejado, remove as linhas com valores nulos e em que a coluna 'Current' é igual a zero
    linha_especificaequalizacaoAm06 = consultaequalizacaoAm06.loc[(consultaequalizacaoAm06['Voltage'] == 1.750) & (consultaequalizacaoAm06['Step Time'] != 0.000000) & (consultaequalizacaoAm06['Current'] != 0.000)].drop_duplicates(subset=['Current'])

        # Converte o formato de 'Step Time' para horas
    linha_especificaequalizacaoAm06['Step Time'] = pd.to_timedelta(linha_especificaequalizacaoAm06['Step Time'])
    linha_especificaequalizacaoAm06['Step Time'] = linha_especificaequalizacaoAm06['Step Time'].dt.total_seconds() / 3600

    linha_especificaequalizacaoAm06 = linha_especificaequalizacaoAm06[['Step Time', 'Current']]


        #PEUKERT
# Captura o caminho do arquivo durante a sessão
    caminho_arquivo7 = session["am_06_peukert"] 

# Carrega o arquivo XLSX
    xlsx_file = pd.read_excel(caminho_arquivo7)

# Define o caminho do arquivo CSV de saída
    caminho_csv7 = caminho_arquivo.replace(".xlsx", ".csv")

# Salva o arquivo CSV
    xlsx_file.to_csv(caminho_csv7, index=False, sep=',')

    consultapeukertAm06 = pd.read_csv(caminho_csv7, delimiter=',', on_bad_lines='skip', low_memory=False)
        # Substitui vírgula por ponto
    consultapeukertAm06['Voltage'] = consultapeukertAm06['Voltage'].str.replace(',', '.')
    consultapeukertAm06['Current'] = consultapeukertAm06['Current'].str.replace(',', '.')
        # Converte a coluna 'Voltage' para float, pulando os valores de string
    consultapeukertAm06['Voltage'] = pd.to_numeric(consultapeukertAm06['Voltage'], errors='coerce')
    consultapeukertAm06['Current'] = pd.to_numeric(consultapeukertAm06['Current'], errors='coerce').abs()
    consultapeukertAm06['Voltage'] = consultapeukertAm06['Voltage'].round(3)


        # Filtra as linhas que contém o valor desejado, remove as linhas com valores nulos e em que a coluna 'Current' é igual a zero
    linha_especificapeukertAm06 = consultapeukertAm06.loc[(consultapeukertAm06['Voltage'] == 1.750) & (consultapeukertAm06['Step Time'] != 0.000000) & (consultapeukertAm06['Current'] != 0.000)].drop_duplicates(subset=['Current'])

        # Filtra as linhas que não são nulas e não possuem o valor '0' na coluna 'Current'
    linha_especificapeukertAm06 = linha_especificapeukertAm06.dropna(subset=['Current'])

        # Converte o formato de 'Step Time' para horas
    linha_especificapeukertAm06['Step Time'] = pd.to_timedelta(linha_especificapeukertAm06['Step Time'])
    linha_especificapeukertAm06['Step Time'] = linha_especificapeukertAm06['Step Time'].dt.total_seconds() / 3600
    linha_especificapeukertAm06 = linha_especificapeukertAm06[['Step Time','Current']]

    am06_CBI22077 = pd.concat([linha_especificaequalizacaoAm06, linha_especificapeukertAm06])
    am06_CBI22077['Step Time'] = am06_CBI22077['Step Time'].round(3)

    #url_imagem1 = '/static/Figure_1.png'
    #url_imagem2 = '/static/Figure_2.png'

    return render_template("pekeurt.html",consulta1=am01_CBI22076, 
                consulta2=am02_CBI22076, consulta3=am05_CBI22077,
                consulta4=am06_CBI22077)


@app.route("/consumo")
@auth_required()
def consumo():
    return render_template("consumo.html")


@app.route("/success")
@auth_required()
def success():
    check_file = os.path.exists(session["am_01_equi"])
    print(f"the file exists? {check_file}")
    return render_template("success.html")


@app.route("/", methods=["GET", "POST"])
@app.route("/home")
@auth_required()
def home():
    form = MyForm()

    if form.validate_on_submit():
        file_list = [
            ("am_01_equi", form.am_01_equi.data),
            ("am_01_form", form.am_01_form.data),
            ("am_01_peukert", form.am_01_peukert.data),
            ("am_01_qdca_mainres", form.am_01_qdca_mainres.data),
            ("am_01_qdca", form.am_01_qdca.data),
            ("am_01_recarga_dhc", form.am_01_recarga_dhc.data),
            ("am_01_recarga_qdca", form.am_01_recarga_qdca.data),
            ("am_01_recarga_dch_prot", form.am_01_recarga_dch_prot.data),
            ("am_02_equi", form.am_02_equi.data),
            ("am_02_form", form.am_02_form.data),
            ("am_02_peukert", form.am_02_peukert.data),
            ("am_02_qdca_mainres", form.am_02_qdca_mainres.data),
            ("am_02_alta_dca", form.am_02_alta_dca.data),
            ("am_02_qdca", form.am_02_qdca.data),
            ("am_02_dch_prot", form.am_02_dch_prot.data),
            ("am_03_agua", form.am_03_agua.data),
            ("am_03_equi", form.am_03_equi.data),
            ("am_03_form", form.am_03_form.data),
            ("am_03_pol", form.am_03_pol.data),
            ("am_04_cons", form.am_04_cons.data),
            ("am_04_equi", form.am_04_equi.data),
            ("am_04_form", form.am_04_form.data),
            ("am_04_pol", form.am_04_pol.data),
            ("am_05_equi", form.am_05_equi.data),
            ("am_05_form", form.am_05_form.data),
            ("am_05_peukert", form.am_05_peukert.data),
            ("am_05_qdca_mainres", form.am_05_qdca_mainres.data),
            ("am_05_qdca", form.am_05_qdca.data),
            ("am_05_rec_alta_dch", form.am_05_rec_alta_dch.data),
            ("am_05_rec_qdca", form.am_05_rec_qdca.data),
            ("am_05_rec_alta_dch", form.am_05_rec_alta_dch.data),
            ("am_06_equi", form.am_06_equi.data),
            ("am_06_form", form.am_06_form.data),
            ("am_06_peukert", form.am_06_peukert.data),
            ("am_06_qdca_mainres", form.am_06_qdca_mainres.data),
            ("am_06_qdca", form.am_06_qdca.data),
            ("am_06_rec_alta_dch", form.am_06_rec_alta_dch.data),
            ("am_06_rec_qdca", form.am_06_rec_qdca.data),
            ("am_06_alta_dch", form.am_06_alta_dch.data),
            ("am_07_consu", form.am_07_consu.data),
            ("am_07_equi", form.am_07_equi.data),
            ("am_07_form", form.am_07_form.data),
            ("am_07_pola", form.am_07_pola.data),
            ("am_08_consu", form.am_08_consu.data),
            ("am_08_equi", form.am_08_equi.data),
            ("am_08_form", form.am_08_form.data),
            ("am_08_pola", form.am_08_pola.data),
        ]
        for file in file_list:
            path = save_file(file[1])
            session[file[0]] = path
        return redirect("/success")
    return render_template("index.html", form=form, name=current_user.email)


# one time setup
with app.app_context():
    # Create a user to test with
    init_db()
    if not app.security.datastore.find_user(email="test@me.com"):
        app.security.datastore.create_user(
            email="test@me.com", password=hash_password("password")
        )
    db_session.commit()
    db_session.close()

if __name__ == "__main__":
    # run application (can also use flask run)
    app.run()


@app.cli.command("create-user")
def create_user():
    """Criar um usuario."""
    email = input("Coloque o seu email: ")
    password = hash_password(input("Coloque o password: "))
    confirm_password = hash_password(input("Coloque o password novamente: "))
    if password != confirm_password:
        print("Passwords diferentes")
        return 1
    try:
        app.security.datastore.create_user(email=email, password=password)
        db_session.commit()
        print(f"Usuario com email {email} criado com sucesso!")
    except Exception as e:
        print("Nao foi possivel criar o usuario.")
        print(e)


