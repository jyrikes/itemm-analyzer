import os

from flask import Flask, render_template
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
def create_upload_folder():
    upload_folder = app.config["UPLOAD_FOLDER"]
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)


# Forms
class MyForm(FlaskForm):
    csv = FileField("csv")
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


@app.route("/", methods=["GET", "POST"])
@app.route("/home")
@auth_required()
def home():
    form = MyForm()

    if form.validate_on_submit():
        create_upload_folder()  # Create the upload folder if necessary
        file = form.csv.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        return f"Filename: { filename }"
    return render_template("index.html", form=form, name=current_user.email)
    # return render_template_string("Hello {{email}} !", email=current_user.email)


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
