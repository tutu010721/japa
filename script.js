document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = 'https://api.deliverypronto.shop/api/produtos';
    const menuContainer = document.getElementById('menu-container');
    
    // Elementos do nosso novo modal de detalhes
    const detailModal = document.getElementById('product-detail-modal');
    const modalBody = document.getElementById('modal-body');
    const closeModalBtn = detailModal.querySelector('.close-btn');

    // --- Função principal para exibir o menu na home ---
    async function fetchAndDisplayMenu() {
        try {
            const response = await fetch(apiUrl);
            if (!response.ok) throw new Error('Falha na rede');
            const categories = await response.json();

            menuContainer.innerHTML = ''; // Limpa a mensagem "Carregando..."

            categories.forEach(category => {
                const categoryTitle = document.createElement('h2');
                categoryTitle.className = 'category-title';
                categoryTitle.textContent = category.nome;
                menuContainer.appendChild(categoryTitle);

                const productGrid = document.createElement('div');
                productGrid.className = 'product-grid';

                category.produtos.forEach(product => {
                    const productCard = document.createElement('div');
                    productCard.className = 'product-card';
                    // Adicionamos um 'data-product-id' para saber em qual produto clicamos
                    productCard.dataset.productId = product.id;
                    
                    productCard.innerHTML = `
                        <div class="product-image">
                            <img src="${product.imagem || 'https://via.placeholder.com/120'}" alt="${product.nome}">
                        </div>
                        <div class="product-info">
                            <h3>${product.nome}</h3>
                            <p class="description">${product.descricao}</p>
                            <p class="price">R$ ${product.preco.toFixed(2).replace('.', ',')}</p>
                        </div>
                    `;
                    productGrid.appendChild(productCard);
                });
                menuContainer.appendChild(productGrid);
            });
        } catch (error) {
            console.error('Erro ao buscar o cardápio:', error);
            menuContainer.innerHTML = '<p class="loading-message">Erro ao carregar o cardápio.</p>';
        }
    }
    
    // --- Nova função para mostrar os detalhes do produto no modal ---
    async function showProductDetail(productId) {
        try {
            // Busca os dados do produto específico na API usando o ID
            const response = await fetch(`https://api.deliverypronto.shop/api/produtos/${productId}`);
            if (!response.ok) throw new Error('Produto não encontrado');
            const product = await response.json();

            // Constrói o HTML para o corpo do modal
            modalBody.innerHTML = `
                <img class="modal-image" src="${product.imagem || 'https://via.placeholder.com/700x300.png?text=Sem+Imagem'}" alt="${product.nome}">
                <div class="modal-info">
                    <h2>${product.nome}</h2>
                    <p class="description">${product.descricao}</p>
                </div>
                <div class="modal-footer">
                    <span class="modal-price">R$ ${product.preco.toFixed(2).replace('.', ',')}</span>
                    <button class="modal-add-btn" data-product-id="${product.id}">Adicionar ao carrinho</button>
                </div>
            `;

            // Exibe o modal
            detailModal.style.display = 'flex';

        } catch (error) {
            console.error('Erro ao buscar detalhes do produto:', error);
        }
    }

    // --- Lógica de Eventos ---

    // Evento para abrir o modal ao clicar em um produto
    menuContainer.addEventListener('click', (event) => {
        const card = event.target.closest('.product-card');
        if (card) {
            const productId = card.dataset.productId;
            showProductDetail(productId);
        }
    });
    
    // Evento para fechar o modal
    const closeEvents = () => { detailModal.style.display = 'none'; };
    closeModalBtn.addEventListener('click', closeEvents);
    detailModal.addEventListener('click', (event) => {
        // Fecha só se clicar no fundo semi-transparente
        if (event.target === detailModal) {
            closeEvents();
        }
    });
    
    // Evento para o botão "Adicionar ao carrinho" dentro do modal (ainda não faz nada, só exibe no console)
    modalBody.addEventListener('click', (event) => {
        if (event.target.classList.contains('modal-add-btn')) {
            const productId = event.target.dataset.productId;
            console.log(`Produto ID ${productId} adicionado ao carrinho! (Lógica do carrinho a ser implementada)`);
            alert(`Produto ${productId} adicionado!`);
        }
    });

    // Inicia tudo
    fetchAndDisplayMenu();
});
