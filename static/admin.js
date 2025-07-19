
document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = '/api/produtos'; // Como a página é servida pelo mesmo domínio da API, podemos usar o caminho relativo
    const productList = document.getElementById('product-list');
    const addProductForm = document.getElementById('add-product-form');

    // Função para carregar e exibir os produtos na tabela
    async function loadProducts() {
        try {
            const response = await fetch(apiUrl);
            const products = await response.json();
            
            productList.innerHTML = ''; // Limpa a lista antes de adicionar os itens
            
            products.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.id}</td>
                    <td>${product.nome}</td>
                    <td>R$ ${product.preco.toFixed(2)}</td>
                    <td class="actions">
                        <button class="edit-btn" data-id="${product.id}">Editar</button>
                        <button class="delete-btn" data-id="${product.id}">Excluir</button>
                    </td>
                `;
                productList.appendChild(row);
            });
        } catch (error) {
            console.error('Erro ao carregar produtos:', error);
        }
    }

    // Event listener para o formulário de adicionar produto
    addProductForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const newProduct = {
            nome: document.getElementById('nome').value,
            descricao: document.getElementById('descricao').value,
            preco: parseFloat(document.getElementById('preco').value),
            imagem: document.getElementById('imagem').value,
        };

        try {
            await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newProduct)
            });
            addProductForm.reset(); // Limpa o formulário
            loadProducts(); // Recarrega a lista de produtos
        } catch (error) {
            console.error('Erro ao adicionar produto:', error);
        }
    });

    // Event listener para os botões de excluir (usando delegação de eventos)
    productList.addEventListener('click', async (event) => {
        if (event.target.classList.contains('delete-btn')) {
            const productId = event.target.dataset.id;
            
            if (confirm(`Tem certeza que deseja excluir o produto ID ${productId}?`)) {
                try {
                    await fetch(`${apiUrl}/${productId}`, { method: 'DELETE' });
                    loadProducts(); // Recarrega a lista
                } catch (error) {
                    console.error('Erro ao excluir produto:', error);
                }
            }
        }
    });

    // Carrega os produtos assim que a página é aberta
    loadProducts();
});
