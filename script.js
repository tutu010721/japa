document.addEventListener('DOMContentLoaded', () => {
    // IMPORTANTE: Deixaremos este URL temporário. Vamos atualizá-lo depois com o link do Render.
    const apiUrl = 'http://127.0.0.1:5000/api/produtos'; // URL de desenvolvimento
    const productGrid = document.getElementById('product-grid');

    async function fetchProdutos() {
        // Quando formos fazer o deploy, trocaremos a URL acima pela URL pública do Render
        const publicApiUrl = 'URL_DO_RENDER_VAI_ENTRAR_AQUI';

        try {
            // Por enquanto, vamos manter o erro para sabermos que precisamos trocar a URL
            const response = await fetch(publicApiUrl); 
            if (!response.ok) {
                throw new Error('API URL não configurada.');
            }
            const produtos = await response.json();
            displayProdutos(produtos);
        } catch (error) {
            console.error('Erro ao buscar produtos:', error);
            productGrid.innerHTML = '<p>Erro ao carregar o cardápio. Configure a URL da API no script.js e conecte ao Render.</p>';
        }
    }

    function displayProdutos(produtos) {
        productGrid.innerHTML = '';
        produtos.forEach(produto => {
            const card = document.createElement('div');
            card.className = 'product-card';
            card.innerHTML = `
                <img src="${produto.imagem}" alt="${produto.nome}">
                <div class="product-info">
                    <h3>${produto.nome}</h3>
                    <p class="description">${produto.descricao}</p>
                    <p class="price">R$ ${produto.preco}</p>
                    <button class="add-to-cart-btn">Adicionar</button>
                </div>
            `;
            productGrid.appendChild(card);
        });
    }

    fetchProdutos();
});
