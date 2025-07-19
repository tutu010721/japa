# app.py - Versão FINAL com correção de CORS para produção
import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

# --- CONFIGURAÇÃO ---
app = Flask(__name__)

# --- CORREÇÃO DE CORS ---
# Em vez de um CORS genérico, especificamos quais "origens" (sites) podem acessar nossa API.
# Adicionamos tanto o seu domínio principal quanto o com "www" por segurança.
origins = [
    "https://deliverypronto.shop",
    "https://www.deliverypronto.shop"
]
CORS(app, resources={r"/api/*": {"origins": origins}})
# -------------------------

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# --- CREDENCIAIS DE ADMIN ---
users = { os.environ.get('ADMIN_USERNAME'): os.environ.get('ADMIN_PASSWORD') }
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# --- MODELOS DE BANCO DE DADOS (não muda) ---
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    produtos = db.relationship('Produto', backref='categoria', lazy=True)
    def to_dict(self):
        return {'id': self.id, 'nome': self.nome}

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'descricao': self.descricao, 'preco': self.preco, 'imagem': self.imagem, 'categoria_id': self.categoria_id}

# --- ROTAS DA API (não mudam) ---
@app.route('/api/categorias', methods=['GET', 'POST'])
def gerenciar_categorias():
    # ... (código existente)
    if request.method == 'GET':
        categorias = Categoria.query.all()
        return jsonify([c.to_dict() for c in categorias])
    if request.method == 'POST':
        dados = request.get_json()
        nova_categoria = Categoria(nome=dados['nome'])
        db.session.add(nova_categoria)
        db.session.commit()
        return jsonify(nova_categoria.to_dict()), 201

@app.route('/api/produtos', methods=['GET', 'POST'])
def gerenciar_produtos():
    # ... (código existente)
    if request.method == 'GET':
        categorias = Categoria.query.order_by(Categoria.id).all()
        resultado = []
        for categoria in categorias:
            produtos_da_categoria = [produto.to_dict() for produto in categoria.produtos]
            if produtos_da_categoria:
                categoria_dict = categoria.to_dict()
                categoria_dict['produtos'] = produtos_da_categoria
                resultado.append(categoria_dict)
        return jsonify(resultado)
    if request.method == 'POST':
        dados = request.get_json()
        if not dados or not all(k in dados for k in ['nome', 'preco', 'categoria_id']):
            return jsonify({'erro': 'Dados incompletos'}), 400
        novo_produto = Produto(nome=dados['nome'], descricao=dados.get('descricao', ''), preco=dados['preco'], imagem=dados.get('imagem', ''), categoria_id=dados['categoria_id'])
        db.session.add(novo_produto)
        db.session.commit()
        return jsonify(novo_produto.to_dict()), 201

@app.route('/api/produtos/<int:produto_id>', methods=['GET', 'PUT', 'DELETE'])
def gerenciar_produto_especifico(produto_id):
    # ... (código existente)
    produto = Produto.query.get_or_404(produto_id)
    if request.method == 'GET':
        return jsonify(produto.to_dict())
    if request.method == 'PUT':
        dados = request.get_json()
        produto.nome = dados.get('nome', produto.nome)
        produto.descricao = dados.get('descricao', produto.descricao)
        produto.preco = dados.get('preco', produto.preco)
        produto.imagem = dados.get('imagem', produto.imagem)
        produto.categoria_id = dados.get('categoria_id', produto.categoria_id)
        db.session.commit()
        return jsonify(produto.to_dict())
    if request.method == 'DELETE':
        db.session.delete(produto)
        db.session.commit()
        return jsonify({'mensagem': 'Produto excluído com sucesso'})

# --- ROTAS DAS PÁGINAS (não mudam) ---
@app.route('/')
def home():
    return "<h1>API do Delivery - CRUD Completo</h1><p>Acesse <a href='/admin'>/admin</a> para gerenciar os produtos.</p>"

@app.route('/admin')
@auth.login_required
def admin_panel():
    return render_template('admin.html')

# --- SETUP DO BANCO DE DADOS (não muda) ---
def setup_database(app):
    with app.app_context():
        db.create_all()

setup_database(app)

if __name__ == '__main__':
    app.run(debug=True)
