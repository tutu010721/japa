document.addEventListener('DOMContentLoaded', () => {
    // As URLs da nossa API. A de categorias será útil no futuro.
    const apiUrlProdutos = '/api/produtos';
    const apiUrlCategorias = '/api/categorias';

    const productList = document.getElementById('product-list');
    const addProductForm = document.getElementById('add-product-form');
    const editModal = document.getElementById('edit-modal');
    const editProductForm = document.getElementById('edit-product-form');
    const closeModalBtn = document.querySelector('.close-btn');

    // --- FUNÇÃO ATUALIZADA PARA LER A NOVA ESTRUTURA DA API ---
    async function loadProducts() {
        try {
            const response = await fetch(apiUrlProdutos);
            // A API agora retorna uma lista de categorias
            const categories = await response.json();
            
            productList.innerHTML = ''; // Limpa a tabela
            
            // Loop 1: Passa por cada CATEGORIA na lista
            categories.forEach(category => {
                // Loop 2: Passa por cada PRODUTO dentro da categoria atual
                category.produtos.forEach(product => {
                    // O código para criar a linha da tabela é o mesmo de antes!
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${product.id}</td>
                        <td>${product.nome}</td>
                        <td>R$ ${product.preco.toFixed(2).replace('.', ',')}</td>
                        <td class="actions">
                            <button class="edit-btn" data-id="${product.id}">Editar</button>
                            <button class="delete-btn" data-id="${product.id}">Excluir</button>
                        </td>
                    `;
                    productList.appendChild(row);
                });
            });
        } catch (error) { 
            console.error('Erro ao carregar produtos:', error);
            productList.innerHTML = '<tr><td colspan="4">Erro ao carregar produtos.</td></tr>';
        }
    }

    // O restante do código não precisa de grandes mudanças, pois as rotas de POST, PUT e DELETE
    // continuam operando em produtos individuais. Apenas precisamos garantir que a categoria seja tratada.
    // Por enquanto, vamos manter a lógica de adicionar/editar e depois melhoramos o formulário.
    
    // Event listener para o formulário de adicionar produto (sem alterações por enquanto)
    addProductForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        // AINDA PRECISAMOS ADICIONAR UM CAMPO DE CATEGORIA AQUI NO FUTURO
        const newProduct = {
            nome: document.getElementById('nome').value,
            descricao: document.getElementById('descricao').value,
            preco: parseFloat(document.getElementById('preco').value),
            imagem: document.getElementById('imagem').value,
            categoria_id: 1 // Usando um ID fixo por enquanto. Vamos melhorar isso.
        };
        try {
            await fetch(apiUrlProdutos, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newProduct)
            });
            addProductForm.reset();
            loadProducts();
        } catch (error) { console.error('Erro ao adicionar produto:', error); }
    });

    // Lógica para os cliques na lista (sem alterações)
    productList.addEventListener('click', async (event) => {
        const target = event.target;
        const productId = target.dataset.id;

        if (target.classList.contains('delete-btn')) {
            if (confirm(`Tem certeza que deseja excluir o produto ID ${productId}?`)) {
                try {
                    await fetch(`${apiUrlProdutos}/${productId}`, { method: 'DELETE' });
                    loadProducts();
                } catch (error) { console.error('Erro ao excluir produto:', error); }
            }
        }

        if (target.classList.contains('edit-btn')) {
            try {
                const response = await fetch(`${apiUrlProdutos}/${productId}`);
                const product = await response.json();
                
                document.getElementById('edit-id').value = product.id;
                document.getElementById('edit-nome').value = product.nome;
                document.getElementById('edit-descricao').value = product.descricao;
                document.getElementById('edit-preco').value = product.preco;
                document.getElementById('edit-imagem').value = product.imagem;
                // PRECISAMOS ADICIONAR A CATEGORIA AQUI TBM
                
                editModal.style.display = 'block';
            } catch (error) { console.error('Erro ao buscar produto para edição:', error); }
        }
    });

    // Lógica para salvar o formulário de edição (sem alterações por enquanto)
    editProductForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const productId = document.getElementById('edit-id').value;
        const updatedProduct = {
            nome: document.getElementById('edit-nome').value,
            descricao: document.getElementById('edit-descricao').value,
            preco: parseFloat(document.getElementById('edit-preco').value),
            imagem: document.getElementById('edit-imagem').value,
            // PRECISAMOS ADICIONAR A CATEGORIA AQUI TBM
        };

        try {
            await fetch(`${apiUrlProdutos}/${productId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedProduct)
            });
            editModal.style.display = 'none';
            loadProducts();
        } catch (error) { console.error('Erro ao atualizar produto:', error); }
    });

    // Lógica para fechar o modal (sem alterações)
    closeModalBtn.onclick = () => { editModal.style.display = 'none'; }
    window.onclick = (event) => { if (event.target == editModal) { editModal.style.display = 'none'; } }

    // Carrega os produtos ao iniciar
    loadProducts();
});
