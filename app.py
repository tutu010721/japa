# app.py - Versão FINAL MESMO com CRUD 100% Completo (GET, POST, PUT, DELETE)
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# --- CONFIGURAÇÃO ---
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELO ---
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200))

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'descricao': self.descricao, 'preco': self.preco, 'imagem': self.imagem}

# --- ROTA PARA LISTAR TODOS (GET) E CRIAR (POST) ---
@app.route('/api/produtos', methods=['GET', 'POST'])
def gerenciar_produtos():
    if request.method == 'GET':
        produtos_db = Produto.query.all()
        return jsonify([produto.to_dict() for produto in produtos_db])

    if request.method == 'POST':
        dados = request.get_json()
        novo_produto = Produto(nome=dados['nome'], descricao=dados.get('descricao', ''), preco=dados['preco'], imagem=dados.get('imagem', ''))
        db.session.add(novo_produto)
        db.session.commit()
        return jsonify(novo_produto.to_dict()), 201

# --- ROTA PARA GERENCIAR UM PRODUTO ESPECÍFICO (GET, PUT, DELETE) ---
# ESTA É A ROTA QUE FOI CORRIGIDA
@app.route('/api/produtos/<int:produto_id>', methods=['GET', 'PUT', 'DELETE'])
def gerenciar_produto_especifico(produto_id):
    produto = Produto.query.get_or_404(produto_id)

    # Se o método for GET, apenas retorna o produto encontrado
    if request.method == 'GET':
        return jsonify(produto.to_dict())

    # Se o método for PUT, atualiza o produto
    if request.method == 'PUT':
        dados = request.get_json()
        produto.nome = dados.get('nome', produto.nome)
        produto.descricao = dados.get('descricao', produto.descricao)
        produto.preco = dados.get('preco', produto.preco)
        produto.imagem = dados.get('imagem', produto.imagem)
        db.session.commit()
        return jsonify(produto.to_dict())

    # Se o método for DELETE, exclui o produto
    if request.method == 'DELETE':
        db.session.delete(produto)
        db.session.commit()
        return jsonify({'mensagem': 'Produto excluído com sucesso'})

# --- ROTA PRINCIPAL ---
@app.route('/')
def home():
    return "<h1>API do Delivery - CRUD Completo</h1>"

# --- SETUP DO BANCO DE DADOS ---
def setup_database(app):
    with app.app_context():
        db.create_all()
        if Produto.query.count() == 0:
            produtos_iniciais = [
                Produto(nome="Combinado Salmão (15 peças)", descricao="5 sashimis, 4 uramakis, 4 hossomakis e 2 niguiris.", preco=35.90, imagem="https://i.imgur.com/k2Ah32D.png"),
                Produto(nome="Temaki Salmão Completo", descricao="Salmão, cream cheese e cebolinha.", preco=28.00, imagem="https://i.imgur.com/k2Ah32D.png"),
                Produto(nome="Yakisoba de Carne", descricao="Macarrão, legumes frescos e pedaços de carne.", preco=32.50, imagem="https://i.imgur.com/k2Ah32D.png")
            ]
            db.session.bulk_save_objects(produtos_iniciais)
            db.session.commit()

setup_database(app)

if __name__ == '__main__':
    app.run(debug=True)
