from app import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    plantas = db.relationship('Planta', backref='dono', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

class Planta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    nome_cientifico = db.Column(db.String(100), nullable=False)
    agua = db.Column(db.String(100), nullable=False)
    luz_solar = db.Column(db.String(100), nullable=False)
    nivel_cuidado = db.Column(db.String(100), nullable=False, default='N/A')
    tipo_solo = db.Column(db.String(100), nullable=False)
    imagem_url = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    ciclo_vida = db.Column(db.String(50), nullable=True)
    tamanho_medio = db.Column(db.String(50), nullable=True)
    toxicidade = db.Column(db.String(50), nullable=True)
    temperatura_ideal = db.Column(db.String(50), nullable=True)
    dicas_cultivo = db.Column(db.Text, nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f'<Planta {self.nome}>'