// Configuración de la API
const API_URL = 'http://localhost:8000/api/v1';

// Variables globales
let token = localStorage.getItem('token');
let currentProducts = [];
let editingProductId = null;

// ========== INICIALIZACIÓN ==========
// Si hay token guardado, mostrar dashboard
if (token) {
    showDashboard();
    loadInventory();
}

// ========== LOGIN ==========
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (!username || !password) {
        showError('Por favor ingresa usuario y contraseña');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/users/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            token = data.access_token;
            localStorage.setItem('token', token);
            
            // Decodificar token para obtener info del usuario
            const payload = JSON.parse(atob(token.split('.')[1]));
            document.getElementById('currentUser').textContent = payload.sub;
            
            showDashboard();
            loadInventory();
        } else {
            showError('Usuario o contraseña incorrectos');
        }
    } catch (error) {
        showError('Error al conectar con el servidor');
        console.error('Error en login:', error);
    }
}

// ========== LOGOUT ==========
function logout() {
    token = null;
    localStorage.removeItem('token');
    document.getElementById('loginScreen').style.display = 'block';
    document.getElementById('dashboard').style.display = 'none';
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    document.getElementById('searchInput').value = '';
}

// ========== MOSTRAR DASHBOARD ==========
function showDashboard() {
    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
    
    // Obtener nombre de usuario del token
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        document.getElementById('currentUser').textContent = payload.sub;
    } catch (e) {
        console.error('Error al decodificar token');
    }
}

// ========== MOSTRAR ERROR DE LOGIN ==========
function showError(message) {
    const errorDiv = document.getElementById('loginError');
    errorDiv.innerHTML = `<div class="error">${message}</div>`;
    setTimeout(() => errorDiv.innerHTML = '', 3000);
}

// ========== CARGAR INVENTARIO ==========
async function loadInventory() {
    try {
        const response = await fetch(`${API_URL}/inventory/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            currentProducts = await response.json();
            displayProducts(currentProducts);
            updateStats();
        } else if (response.status === 401) {
            showNotification('Sesión expirada', 'error');
            logout();
        } else {
            showNotification('Error al cargar inventario', 'error');
        }
    } catch (error) {
        console.error('Error al cargar inventario:', error);
        showNotification('Error de conexión con el servidor', 'error');
    }
}

// ========== MOSTRAR PRODUCTOS EN TABLA ==========
function displayProducts(products) {
    const tbody = document.getElementById('inventoryBody');
    
    if (products.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="empty-state">
                    <h3>📦 No hay productos</h3>
                    <p>Agrega tu primer producto haciendo clic en "Agregar Producto"</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = products.map(product => `
        <tr>
            <td>
                <strong>${escapeHtml(product.name)}</strong>
                ${product.description ? `<br><small style="color: #999;">${escapeHtml(product.description)}</small>` : ''}
            </td>
            <td>${product.quantity} unidades</td>
            <td>$${product.price.toFixed(2)}</td>
            <td><strong>$${(product.price * product.quantity).toFixed(2)}</strong></td>
            <td>
                <button class="btn-small btn-edit" onclick="openEditModal(${product.id})">✏️ Editar</button>
                <button class="btn-small btn-delete" onclick="deleteProduct(${product.id})">🗑️ Eliminar</button>
            </td>
        </tr>
    `).join('');
}

// ========== ACTUALIZAR ESTADÍSTICAS ==========
function updateStats() {
    const totalProducts = currentProducts.length;
    const totalQuantity = currentProducts.reduce((sum, p) => sum + p.quantity, 0);
    const totalValue = currentProducts.reduce((sum, p) => sum + (p.price * p.quantity), 0);
    
    document.getElementById('totalProducts').textContent = totalProducts;
    document.getElementById('totalQuantity').textContent = totalQuantity;
    document.getElementById('totalValue').textContent = `$${totalValue.toFixed(2)}`;
}

// ========== FILTRAR PRODUCTOS ==========
function filterProducts() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filtered = currentProducts.filter(p => 
        p.name.toLowerCase().includes(searchTerm) ||
        (p.description && p.description.toLowerCase().includes(searchTerm))
    );
    displayProducts(filtered);
}

// ========== ABRIR MODAL AGREGAR ==========
function openAddModal() {
    editingProductId = null;
    document.getElementById('modalTitle').textContent = 'Agregar Producto';
    document.getElementById('productName').value = '';
    document.getElementById('productQuantity').value = '';
    document.getElementById('productPrice').value = '';
    document.getElementById('productDescription').value = '';
    document.getElementById('productModal').style.display = 'flex';
}

// ========== ABRIR MODAL EDITAR ==========
function openEditModal(productId) {
    const product = currentProducts.find(p => p.id === productId);
    if (!product) return;
    
    editingProductId = productId;
    document.getElementById('modalTitle').textContent = 'Editar Producto';
    document.getElementById('productName').value = product.name;
    document.getElementById('productQuantity').value = product.quantity;
    document.getElementById('productPrice').value = product.price;
    document.getElementById('productDescription').value = product.description || '';
    document.getElementById('productModal').style.display = 'flex';
}

// ========== CERRAR MODAL ==========
function closeModal() {
    document.getElementById('productModal').style.display = 'none';
    editingProductId = null;
}

// ========== GUARDAR PRODUCTO ==========
async function saveProduct() {
    const name = document.getElementById('productName').value.trim();
    const quantity = parseInt(document.getElementById('productQuantity').value) || 0;
    const price = parseFloat(document.getElementById('productPrice').value) || 0;
    const description = document.getElementById('productDescription').value.trim();
    
    if (!name) {
        showNotification('El nombre del producto es requerido', 'error');
        return;
    }
    
    if (quantity < 0) {
        showNotification('La cantidad no puede ser negativa', 'error');
        return;
    }
    
    if (price < 0) {
        showNotification('El precio no puede ser negativo', 'error');
        return;
    }
    
    const productData = { name, quantity, price, description };
    
    try {
        const url = editingProductId 
            ? `${API_URL}/inventory/${editingProductId}`
            : `${API_URL}/inventory/`;
            
        const method = editingProductId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(productData)
        });
        
        if (response.ok) {
            closeModal();
            loadInventory();
            showNotification(
                editingProductId ? '✅ Producto actualizado exitosamente' : '✅ Producto agregado exitosamente',
                'success'
            );
        } else {
            const errorData = await response.json();
            showNotification(`Error: ${errorData.detail || 'No se pudo guardar el producto'}`, 'error');
        }
    } catch (error) {
        console.error('Error al guardar producto:', error);
        showNotification('Error de conexión con el servidor', 'error');
    }
}

// ========== ELIMINAR PRODUCTO ==========
async function deleteProduct(productId) {
    if (!confirm('⚠️ ¿Estás seguro de eliminar este producto?\n\nEsta acción no se puede deshacer.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/inventory/${productId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            loadInventory();
            showNotification('🗑️ Producto eliminado exitosamente', 'success');
        } else {
            showNotification('Error al eliminar el producto', 'error');
        }
    } catch (error) {
        console.error('Error al eliminar producto:', error);
        showNotification('Error de conexión con el servidor', 'error');
    }
}

// ========== MOSTRAR NOTIFICACIÓN ==========
function showNotification(message, type = 'success') {
    // Remover notificaciones previas
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    // Crear nueva notificación
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Remover después de 3 segundos
    setTimeout(() => notification.remove(), 3000);
}

// ========== SEGURIDAD: ESCAPAR HTML ==========
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ========== EVENT LISTENERS ==========
// Permitir Enter en el campo de contraseña para hacer login
document.getElementById('password').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        login();
    }
});

// Permitir Enter en el campo de usuario para hacer login
document.getElementById('username').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        login();
    }
});

// Cerrar modal al hacer clic fuera
document.getElementById('productModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});

// Consola: Información de desarrollo
console.log('🚀 Sistema de Inventario iniciado');
console.log('📡 API URL:', API_URL);
console.log('🔑 Token presente:', !!token);