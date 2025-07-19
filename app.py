# app.py - Versão com rota para ADICIONAR produtos
import os
from flask import Flask, jsonify, request # 'request' foi importado aqui!
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# --- CONFIGURAÇÃO DA APLICAÇÃO ---
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- MODELO DO BANCO DE DADOS ---
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


# --- ROTAS DA API ---

# Rota para OBTER todos os produtos (GET)
@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    produtos_db = Produto.query.all()
    lista_de_produtos = [produto.to_dict() for produto in produtos_db]
    return jsonify(lista_de_produtos)

# --- NOVIDADE AQUI ---
# Rota para ADICIONAR um novo produto (POST)
@app.route('/api/produtos', methods=['POST'])
def add_produto():
    # Pega os dados JSON enviados no corpo da requisição POST
    dados = request.get_json()

    # Verifica se os dados necessários foram enviados
    if not dados or not 'nome' in dados or not 'preco' in dados:
        return jsonify({'erro': 'Dados incompletos'}), 400

    # Cria uma nova instância do nosso modelo Produto com os dados recebidos
    novo_produto = Produto(
        nome=dados['nome'],
        descricao=dados.get('descricao', ''), # .get() é mais seguro, usa '' se a descrição não for enviada
        preco=dados['preco'],
        imagem=dados.get('imagem', '')
    )

    # Adiciona o novo produto à sessão do banco de dados
    db.session.add(novo_produto)
    # Efetiva (salva) as mudanças no banco de dados
    db.session.commit()

    # Retorna o produto recém-criado como confirmação, com o status HTTP 201 (Created)
    return jsonify(novo_produto.to_dict()), 201


@app.route('/')
def home():
    return "<h1>API do Delivery Rodando com Banco de Dados!</h1>"


# Função de setup que não será mais chamada a cada inicialização para não repopular o banco
def setup_database(app):
    with app.app_context():
        db.create_all()

# Apenas para garantir que o banco de dados exista na primeira vez
setup_database(app)

if __name__ == '__main__':
    app.run(debug=True)
