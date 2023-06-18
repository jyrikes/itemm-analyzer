import os

from flask import Flask, render_template, redirect
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


# def save_file(file_form):
#     folder = get_upload_folder()  # Create the upload folder if necessary
#     filename = secure_filename(file_form.filename)
#     file_path = os.path.join(folder, filename)
#     file_form.save(file_path)


# Forms
class MyForm(FlaskForm):
    csv = FileField("csv")
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
    am_05_rec_alta_dch = FileField("am_05_rec_alta_dch")
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
    return render_template("pekeurt.html")


@app.route("/consumo")
@auth_required()
def consumo():
    return render_template("consumo.html")


@app.route("/success")
@auth_required()
def success():
    return render_template("success.html")


# am_01_equi
#     am_01_form
#     am_01_peukert
#     am_01_qdca_mainres
#     am_01_qdca
#     am_01_recarga_dhc
#     am_01_recarga_qdca
#     am_01_recarga_dch_prot
#     am_02_equi
#     am_02_form
#     am_02_peukert
#     am_02_qdca_mainres
#     am_02_qdca
#     am_02_alta_dca
#     am_02_qdca
#     am_02_dch_prot
#     am_03_agua
#     am_03_equi
#     am_03_form
#     am_03_pol
#     am_04_cons
#     am_04_equi
#     am_04_form
#     am_04_pol
#     am_05_equi
#     am_05_form
#     am_05_peukert
#     am_05_qdca_mainres
#     am_05_qdca
#     am_05_rec_alta_dch
#     am_05_rec_qdca
#     am_05_rec_alta_dch
#     am_06_equi
#     am_06_form
#     am_06_peukert
#     am_06_qdca_mainres
#     am_06_qdca
#     am_06_rec_alta_dch
#     am_06_rec_qdca
#     am_06_alta_dch
#     am_07_consu
#     am_07_equi
#     am_07_form
#     am_07_pola
#     am_08_consu
#     am_08_equi
#     am_08_form
#     am_08_pola


@app.route("/", methods=["GET", "POST"])
@app.route("/home")
@auth_required()
def home():
    form = MyForm()

    if form.validate_on_submit():
        # file_list = [form.am_01_equi.data]
        # for file in file_list:
        #     save_file(file)
        folder = get_upload_folder()  # Create the upload folder if necessary
        file = form.csv.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(folder, filename)
        file.save(file_path)
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
