# app.py - CÓDIGO CORRETO PARA O BACKEND
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Habilita o CORS para permitir que nosso frontend acesse esta API
CORS(app)

# Lista de produtos de exemplo
produtos_exemplo = [
    {
        "id": 1,
        "nome": "Combinado Salmão (15 peças)",
        "descricao": "5 sashimis, 4 uramakis, 4 hossomakis e 2 niguiris.",
        "preco": "35.90",
        "imagem": "https://i.imgur.com/k2Ah32D.png"
    },
    {
        "id": 2,
        "nome": "Temaki Salmão Completo",
        "descricao": "Salmão, cream cheese e cebolinha.",
        "preco": "28.00",
        "imagem": "https://i.imgur.com/k2Ah32D.png"
    },
    {
        "id": 3,
        "nome": "Yakisoba de Carne",
        "descricao": "Macarrão, legumes frescos e pedaços de carne.",
        "preco": "32.50",
        "imagem": "https://i.imgur.com/k2Ah32D.png"
    }
]

# Rota de API que retorna a lista de produtos em formato JSON
@app.route('/api/produtos')
def get_produtos():
    return jsonify(produtos_exemplo)

# Rota principal para um teste rápido
@app.route('/')
def home():
    return "<h1>API do Delivery Rodando!</h1><p>Acesse /api/produtos para ver os dados.</p>"

# Esta parte não é necessária para o Render, mas não causa problema
if __name__ == '__main__':
    app.run(debug=True)
