// static/script.js

// Espera o HTML da página ser completamente carregado para então executar o script.
document.addEventListener('DOMContentLoaded', () => {

    // --- PONTO CRÍTICO ---
    // A URL da nossa API, agora apontando para o seu domínio de produção no Render.
    const apiUrl = 'https://api.deliverypronto.shop/api/produtos';
    // -------------------

    // Pega o elemento da grade de produtos onde vamos inserir os cards.
    const productGrid = document.getElementById('product-grid');

    // Função assíncrona para buscar os produtos da API.
    async function fetchProdutos() {
        // Exibe uma mensagem de carregamento enquanto busca os dados.
        productGrid.innerHTML = '<p>Carregando cardápio, por favor aguarde...</p>';

        try {
            // Tenta fazer a requisição para a nossa API usando o fetch.
            const response = await fetch(apiUrl);
            
            // Se a resposta não for bem-sucedida (ex: erro 404 ou 500), lança um erro.
            if (!response.ok) {
                throw new Error(`Erro na rede: ${response.statusText}`);
            }
            
            // Converte a resposta da API (que está em formato JSON) para um objeto JavaScript.
            const produtos = await response.json();

            // Se a busca for bem-sucedida, chama a função para exibir os produtos na tela.
            displayProdutos(produtos);

        } catch (error) {
            // Se qualquer parte do 'try' falhar, captura o erro aqui.
            console.error('Falha ao buscar produtos:', error);
            // Exibe uma mensagem de erro amigável para o usuário.
            productGrid.innerHTML = '<p>Não foi possível carregar o cardápio. Tente novamente mais tarde.</p>';
        }
    }

    // Função para exibir os produtos na tela, recebendo a lista de produtos como argumento.
    function displayProdutos(produtos) {
        // Primeiro, limpa qualquer conteúdo que já estivesse na grade (como a mensagem de "carregando").
        productGrid.innerHTML = '';

        // Se a lista de produtos estiver vazia, exibe uma mensagem.
        if (produtos.length === 0) {
            productGrid.innerHTML = '<p>Nenhum produto encontrado no momento.</p>';
            return;
        }

        // Para cada produto na lista, cria o HTML do card correspondente.
        produtos.forEach(produto => {
            // Cria um novo elemento <div> para o card.
            const card = document.createElement('div');
            // Adiciona a classe CSS 'product-card' para aplicar os estilos.
            card.className = 'product-card';
            
            // Define o HTML interno do card usando os dados do produto.
            card.innerHTML = `
                <img src="${produto.imagem}" alt="${produto.nome}">
                <div class="product-info">
                    <h3>${produto.nome}</h3>
                    <p class="description">${produto.descricao}</p>
                    <p class="price">R$ ${produto.preco}</p>
                    <button class="add-to-cart-btn">Adicionar</button>
                </div>
            `;
            
            // Adiciona o card recém-criado à grade de produtos na página.
            productGrid.appendChild(card);
        });
    }

    // Finalmente, chama a função principal para iniciar todo o processo.
    fetchProdutos();
});
