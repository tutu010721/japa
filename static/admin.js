document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = '/api/produtos';
    const productList = document.getElementById('product-list');
    const addProductForm = document.getElementById('add-product-form');

    // --- NOVOS ELEMENTOS DO MODAL DE EDIÇÃO ---
    const editModal = document.getElementById('edit-modal');
    const editProductForm = document.getElementById('edit-product-form');
    const closeModalBtn = document.querySelector('.close-btn');

    // Função para carregar e exibir os produtos na tabela (sem alterações)
    async function loadProducts() {
        try {
            const response = await fetch(apiUrl);
            const products = await response.json();
            
            productList.innerHTML = '';
            
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
        } catch (error) { console.error('Erro ao carregar produtos:', error); }
    }

    // Event listener para o formulário de adicionar produto (sem alterações)
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
            addProductForm.reset();
            loadProducts();
        } catch (error) { console.error('Erro ao adicionar produto:', error); }
    });

    // --- LÓGICA ATUALIZADA PARA OS CLIQUES NA LISTA DE PRODUTOS ---
    productList.addEventListener('click', async (event) => {
        const target = event.target;
        const productId = target.dataset.id;

        // Se o botão clicado for o de EXCLUIR
        if (target.classList.contains('delete-btn')) {
            if (confirm(`Tem certeza que deseja excluir o produto ID ${productId}?`)) {
                try {
                    await fetch(`${apiUrl}/${productId}`, { method: 'DELETE' });
                    loadProducts();
                } catch (error) { console.error('Erro ao excluir produto:', error); }
            }
        }

        // Se o botão clicado for o de EDITAR
        if (target.classList.contains('edit-btn')) {
            try {
                // 1. Busca os dados atuais do produto na API
                const response = await fetch(`${apiUrl}/${productId}`);
                const product = await response.json();

                // 2. Preenche o formulário do modal com os dados do produto
                document.getElementById('edit-id').value = product.id;
                document.getElementById('edit-nome').value = product.nome;
                document.getElementById('edit-descricao').value = product.descricao;
                document.getElementById('edit-preco').value = product.preco;
                document.getElementById('edit-imagem').value = product.imagem;
                
                // 3. Exibe o modal
                editModal.style.display = 'block';
            } catch (error) { console.error('Erro ao buscar produto para edição:', error); }
        }
    });

    // --- NOVA LÓGICA PARA SALVAR O FORMULÁRIO DE EDIÇÃO ---
    editProductForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const productId = document.getElementById('edit-id').value;
        const updatedProduct = {
            nome: document.getElementById('edit-nome').value,
            descricao: document.getElementById('edit-descricao').value,
            preco: parseFloat(document.getElementById('edit-preco').value),
            imagem: document.getElementById('edit-imagem').value,
        };

        try {
            await fetch(`${apiUrl}/${productId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedProduct)
            });
            editModal.style.display = 'none'; // Esconde o modal
            loadProducts(); // Recarrega a lista de produtos com os dados atualizados
        } catch (error) { console.error('Erro ao atualizar produto:', error); }
    });

    // --- NOVA LÓGICA PARA FECHAR O MODAL ---
    // Fecha ao clicar no 'X'
    closeModalBtn.onclick = () => {
        editModal.style.display = 'none';
    }
    // Fecha ao clicar fora do conteúdo do modal
    window.onclick = (event) => {
        if (event.target == editModal) {
            editModal.style.display = 'none';
        }
    }

    // Carrega os produtos ao iniciar
    loadProducts();
});
