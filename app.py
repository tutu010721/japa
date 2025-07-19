# app.py - Versão CORRIGIDA com rotas unificadas
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
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'imagem': self.imagem
        }

# --- ROTA UNIFICADA PARA PRODUTOS (GET e POST) ---
# Esta é a principal correção. Unimos as duas funções em uma só.
@app.route('/api/produtos', methods=['GET', 'POST'])
def gerenciar_produtos():
    # Se o método da requisição for GET, retorna a lista de produtos
    if request.method == 'GET':
        produtos_db = Produto.query.all()
        lista_de_produtos = [produto.to_dict() for produto in produtos_db]
        return jsonify(lista_de_produtos)

    # Se o método da requisição for POST, cria um novo produto
    if request.method == 'POST':
        dados = request.get_json()
        if not dados or not 'nome' in dados or not 'preco' in dados:
            return jsonify({'erro': 'Dados incompletos'}), 400

        novo_produto = Produto(
            nome=dados['nome'],
            descricao=dados.get('descricao', ''),
            preco=dados['preco'],
            imagem=dados.get('imagem', '')
        )
        db.session.add(novo_produto)
        db.session.commit()
        return jsonify(novo_produto.to_dict()), 201

# --- ROTA PRINCIPAL ---
@app.route('/')
def home():
    return "<h1>API do Delivery Rodando com Banco de Dados!</h1>"

# --- FUNÇÃO DE SETUP DO BANCO DE DADOS (CORRIGIDA) ---
# Garante que o banco seja criado e populado se estiver vazio.
def setup_database(app):
    with app.app_context():
        db.create_all()
        # Esta verificação garante que os dados só sejam adicionados uma vez
        if Produto.query.count() == 0:
            produtos_iniciais = [
                Produto(nome="Combinado Salmão (15 peças)", descricao="5 sashimis, 4 uramakis, 4 hossomakis e 2 niguiris.", preco=35.90, imagem="https://i.imgur.com/k2Ah32D.png"),
                Produto(nome="Temaki Salmão Completo", descricao="Salmão, cream cheese e cebolinha.", preco=28.00, imagem="https://i.imgur.com/k2Ah32D.png"),
                Produto(nome="Yakisoba de Carne", descricao="Macarrão, legumes frescos e pedaços de carne.", preco=32.50, imagem="https://i.imgur.com/k2Ah32D.png")
            ]
            db.session.bulk_save_objects(produtos_iniciais)
            db.session.commit()
            print("Banco de dados populado com dados iniciais.")

# Executa a função de setup ao iniciar
setup_database(app)

if __name__ == '__main__':
    app.run(debug=True)
