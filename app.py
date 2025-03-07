from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicializa o Flask
app = Flask(__name__)

# Configurações do Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plantas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456789'

# Inicializa o SQLAlchemy e o LoginManager
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Configurações do LoginManager
login_manager.login_view = 'login'
login_manager.login_message = "Você precisa estar logado para acessar esta página."

# Importa os modelos e as rotas
from models import Usuario, Planta
from routes import *

# Cria o banco de dados
with app.app_context():
    db.create_all()

# Inicia o aplicativo
if __name__ == '__main__':
    app.run(debug=True)