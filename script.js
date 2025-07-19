document.addEventListener('DOMContentLoaded', () => {
    // Apontamos para a nossa API no Render
    const apiUrl = 'https://api.deliverypronto.shop/api/produtos';
    // O container principal onde todo o menu será desenhado
    const menuContainer = document.getElementById('menu-container');

    async function fetchAndDisplayMenu() {
        try {
            // 1. Busca os dados na nossa API
            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error('Não foi possível carregar o cardápio.');
            }
            const categories = await response.json();

            // 2. Limpa a mensagem "Carregando..."
            menuContainer.innerHTML = '';

            // 3. Loop principal: para cada categoria recebida...
            categories.forEach(category => {
                // Cria um título para a categoria
                const categoryTitle = document.createElement('h2');
                categoryTitle.className = 'category-title';
                categoryTitle.textContent = category.nome;
                menuContainer.appendChild(categoryTitle);

                // Cria uma div para ser a grade de produtos desta categoria
                const productGrid = document.createElement('div');
                productGrid.className = 'product-grid';

                // 4. Loop aninhado: para cada produto dentro da categoria atual...
                category.produtos.forEach(product => {
                    // Cria o card do produto
                    const productCard = document.createElement('div');
                    productCard.className = 'product-card';
                    
                    productCard.innerHTML = `
                        <img src="${product.imagem || 'https://via.placeholder.com/300x200.png?text=Sem+Imagem'}" alt="${product.nome}">
                        <div class="product-info">
                            <h3>${product.nome}</h3>
                            <p class="description">${product.descricao}</p>
                            <div class="price-add-row">
                                <span class="price">R$ ${product.preco.toFixed(2).replace('.', ',')}</span>
                                <button class="add-to-cart-btn">Adicionar</button>
                            </div>
                        </div>
                    `;
                    // Adiciona o card do produto na grade da categoria
                    productGrid.appendChild(productCard);
                });

                // Adiciona a grade de produtos completa da categoria ao container principal
                menuContainer.appendChild(productGrid);
            });

        } catch (error) {
            console.error('Erro ao buscar o cardápio:', error);
            menuContainer.innerHTML = '<p class="loading-message">Erro ao carregar o cardápio. Tente novamente mais tarde.</p>';
        }
    }

    // Chama a função principal para iniciar tudo
    fetchAndDisplayMenu();
});
