# app.py - Versão com Categorias
import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

# --- CONFIGURAÇÃO ---
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# --- CREDENCIAIS (não muda) ---
users = { os.environ.get('ADMIN_USERNAME'): os.environ.get('ADMIN_PASSWORD') }
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# --- NOVOS MODELOS DE BANCO DE DADOS ---
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    # O 'backref' cria uma "coluna virtual" nos produtos para podermos acessar a categoria de um produto.
    # O 'lazy=True' significa que os produtos de uma categoria serão carregados sob demanda.
    produtos = db.relationship('Produto', backref='categoria', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome}

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200))
    # Esta é a Chave Estrangeira. Ela liga o produto a um ID da tabela Categoria.
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'imagem': self.imagem,
            'categoria_id': self.categoria_id
        }

# --- ROTAS DA API ATUALIZADAS ---
@app.route('/api/produtos')
def get_produtos_agrupados():
    # Esta rota agora retorna os produtos agrupados por categoria
    categorias = Categoria.query.order_by(Categoria.id).all()
    resultado = []
    for categoria in categorias:
        produtos_da_categoria = [produto.to_dict() for produto in categoria.produtos]
        categoria_dict = categoria.to_dict()
        categoria_dict['produtos'] = produtos_da_categoria
        resultado.append(categoria_dict)
    return jsonify(resultado)

# ... (as rotas de POST, PUT, DELETE de produtos e as de admin continuam as mesmas por enquanto) ...
# As rotas de gerenciar produtos precisarão ser atualizadas para lidar com a categoria_id.
# Mas vamos fazer isso no próximo passo para não sobrecarregar.

# --- ROTA PRINCIPAL ---
@app.route('/')
def home():
    return "<h1>API do Delivery - Versão com Categorias</h1>"

# ... (outras rotas como /admin continuam aqui, mas as omiti para encurtar) ...
# COLE O RESTANTE DO SEU CÓDIGO A PARTIR DAQUI (gerenciar_produtos, gerenciar_produto_especifico, admin_panel, etc.)
# POR ENQUANTO, DEIXE-OS COMO ESTÃO. VAMOS ATUALIZÁ-LOS DEPOIS.

# --- SETUP DO BANCO DE DADOS ---
def setup_database(app):
    with app.app_context():
        # Apaga o banco de dados antigo para recriar com a nova estrutura.
        # CUIDADO: Isso apaga todos os dados existentes. Só fazemos isso em desenvolvimento.
        # db.drop_all()
        db.create_all()

setup_database(app)

if __name__ == '__main__':
    app.run(debug=True)
