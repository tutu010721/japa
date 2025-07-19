# app.py - Versão com Banco de Dados SQLite
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# --- CONFIGURAÇÃO DA APLICAÇÃO ---
app = Flask(__name__)
CORS(app)

# Define o caminho base do nosso projeto
basedir = os.path.abspath(os.path.dirname(__file__))

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
# Diz ao SQLAlchemy onde nosso banco de dados estará localizado.
# 'sqlite:///' significa que é um arquivo SQLite.
# 'database.db' é o nome do arquivo que será criado.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desativa um recurso desnecessário

# Cria a instância do banco de dados, conectando-o com nossa app Flask
db = SQLAlchemy(app)


# --- MODELO DO BANCO DE DADOS ---
# Um "Modelo" é uma classe Python que representa uma tabela no banco de dados.
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ID único para cada produto
    nome = db.Column(db.String(100), nullable=False) # Nome do produto, não pode ser nulo
    descricao = db.Column(db.String(200), nullable=True) # Descrição, pode ser nula
    preco = db.Column(db.Float, nullable=False) # Preço, não pode ser nulo
    imagem = db.Column(db.String(200), nullable=True) # URL da imagem, pode ser nula

    # Função para converter nosso objeto Produto em um dicionário (formato JSON)
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'imagem': self.imagem
        }


# --- ROTAS DA API ---
# Rota para obter todos os produtos do banco de dados
@app.route('/api/produtos')
def get_produtos():
    # Pega todos os registros da tabela Produto
    produtos_db = Produto.query.all() 
    # Converte cada produto da lista para o formato de dicionário
    lista_de_produtos = [produto.to_dict() for produto in produtos_db]
    # Retorna a lista em formato JSON
    return jsonify(lista_de_produtos)

@app.route('/')
def home():
    return "<h1>API do Delivery Rodando com Banco de Dados!</h1>"


# --- FUNÇÃO PARA CRIAR O BANCO DE DADOS E DADOS INICIAIS ---
# Esta função cria o arquivo do banco de dados e adiciona alguns produtos
# na primeira vez que a aplicação é executada.
def setup_database(app):
    with app.app_context():
        # Cria todas as tabelas definidas nos modelos (no caso, apenas a tabela Produto)
        db.create_all()

        # Verifica se a tabela de produtos está vazia
        if Produto.query.count() == 0:
            # Cria instâncias da classe Produto
            produto1 = Produto(nome="Combinado Salmão (15 peças)", descricao="5 sashimis, 4 uramakis, 4 hossomakis e 2 niguiris.", preco=35.90, imagem="https://i.imgur.com/k2Ah32D.png")
            produto2 = Produto(nome="Temaki Salmão Completo", descricao="Salmão, cream cheese e cebolinha.", preco=28.00, imagem="https://i.imgur.com/k2Ah32D.png")
            produto3 = Produto(nome="Yakisoba de Carne", descricao="Macarrão, legumes frescos e pedaços de carne.", preco=32.50, imagem="https://i.imgur.com/k2Ah32D.png")
            
            # Adiciona os novos produtos à "sessão" do banco de dados
            db.session.add(produto1)
            db.session.add(produto2)
            db.session.add(produto3)

            # Efetiva as mudanças no banco de dados
            db.session.commit()
            print("Banco de dados criado e populado com dados iniciais.")

# Executa a função de setup ao iniciar
setup_database(app)

if __name__ == '__main__':
    app.run(debug=True)
