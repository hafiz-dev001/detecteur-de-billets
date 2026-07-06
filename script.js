const productDatabase = [
    { id: 1, name: 'Casque audio', category: 'tech', price: 79, emoji: '🎧', description: 'Son immersif et confort toute la journée.' },
    { id: 2, name: 'Sac minimaliste', category: 'fashion', price: 59, emoji: '👜', description: 'Design épuré pour les bureaux et les trajets.' },
    { id: 3, name: 'Lampe d’appoint', category: 'home', price: 45, emoji: '💡', description: 'Éclairage doux pour vos soirées et lectures.' },
    { id: 4, name: 'Montre connectée', category: 'tech', price: 129, emoji: '⌚', description: 'Suivi de santé et notifications à portée de poignet.' },
    { id: 5, name: 'Tasse premium', category: 'home', price: 24, emoji: '☕', description: 'Matériau robuste et finition élégante.' },
    { id: 6, name: 'Écharpe chaude', category: 'fashion', price: 35, emoji: '🧣', description: 'Douceur et chaleur pour l’hiver.' },
    { id: 7, name: 'Clavier mécanique', category: 'tech', price: 99, emoji: '⌨️', description: 'Retour tactile idéal pour travailler et jouer.' },
    { id: 8, name: 'Mugis de bureau', category: 'home', price: 18, emoji: '🖊️', description: 'Organisation simple pour votre espace de travail.' },
    { id: 9, name: 'Bottes confort', category: 'fashion', price: 89, emoji: '🥾', description: 'Confort au quotidien et look moderne.' },
    { id: 10, name: 'Pack soin visage', category: 'wellness', price: 64, emoji: '🧴', description: 'Routine de bien-être à la maison.' },
    { id: 11, name: 'Bureau pliant', category: 'home', price: 109, emoji: '🪑', description: 'Compact et pratique pour petits espaces.' },
    { id: 12, name: 'Enceinte portable', category: 'tech', price: 89, emoji: '🔊', description: 'Musique et appels partout avec vous.' }
];

const state = {
    filter: 'all',
    cart: [],
    payment: 'card'
};

const productsGrid = document.getElementById('productsGrid');
const filters = document.getElementById('filters');
const cartItems = document.getElementById('cartItems');
const cartCount = document.getElementById('cartCount');
const cartTotal = document.getElementById('cartTotal');
const cartPanel = document.getElementById('cartPanel');
const cartToggle = document.getElementById('cartToggle');
const closeCart = document.getElementById('closeCart');
const paymentStatus = document.getElementById('paymentStatus');
const checkoutBtn = document.getElementById('checkoutBtn');
const contactButton = document.getElementById('contactButton');

function renderFilters() {
    const categories = ['all', ...new Set(productDatabase.map((p) => p.category))];
    filters.innerHTML = categories
        .map((category) => {
            const label = category === 'all' ? 'Tous' : category;
            return `<button class="filter-btn ${state.filter === category ? 'active' : ''}" data-filter="${category}">${label}</button>`;
        })
        .join('');
}

function renderProducts() {
    const visibleProducts = productDatabase.filter((product) => state.filter === 'all' || product.category === state.filter);

    productsGrid.innerHTML = visibleProducts
        .map(
            (product) => `
        <article class="product-card">
          <div class="emoji">${product.emoji}</div>
          <div class="product-meta">
            <strong>${product.name}</strong>
            <span class="price">${product.price} €</span>
          </div>
          <p>${product.description}</p>
          <small>${product.category}</small>
          <button class="add-btn" data-id="${product.id}">Ajouter au panier</button>
        </article>
      `
        )
        .join('');
}

function addToCart(id) {
    const product = productDatabase.find((item) => item.id === Number(id));
    const existing = state.cart.find((item) => item.id === Number(id));

    if (existing) {
        existing.quantity += 1;
    } else {
        state.cart.push({ ...product, quantity: 1 });
    }

    renderCart();
}

function updateQuantity(id, delta) {
    const item = state.cart.find((entry) => entry.id === id);
    if (!item) return;

    item.quantity += delta;
    if (item.quantity <= 0) {
        state.cart = state.cart.filter((entry) => entry.id !== id);
    }
    renderCart();
}

function updatePaymentLabel() {
    const labels = {
        card: 'Paiement par carte sélectionné.',
        paypal: 'Paiement via PayPal sélectionné.',
        cash: 'Paiement en espèces sélectionné.'
    };
    paymentStatus.textContent = labels[state.payment];
}

function renderCart() {
    cartCount.textContent = state.cart.reduce((sum, item) => sum + item.quantity, 0);
    const total = state.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    cartTotal.textContent = `${total} €`;

    if (!state.cart.length) {
        cartItems.innerHTML = '<div class="empty">Votre panier est vide.</div>';
        return;
    }

    cartItems.innerHTML = state.cart
        .map(
            (item) => `
        <div class="cart-item">
          <div>
            <strong>${item.name}</strong>
            <div>${item.quantity} × ${item.price} €</div>
          </div>
          <div>
            <button data-action="decrease" data-id="${item.id}">−</button>
            <button data-action="increase" data-id="${item.id}">+</button>
          </div>
        </div>
      `
        )
        .join('');
}

filters.addEventListener('click', (event) => {
    const button = event.target.closest('.filter-btn');
    if (!button) return;
    state.filter = button.dataset.filter;
    renderFilters();
    renderProducts();
});

productsGrid.addEventListener('click', (event) => {
    const button = event.target.closest('.add-btn');
    if (!button) return;
    addToCart(button.dataset.id);
});

cartItems.addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (!button) return;
    const id = Number(button.dataset.id);
    if (button.dataset.action === 'increase') {
        updateQuantity(id, 1);
    } else {
        updateQuantity(id, -1);
    }
});

cartToggle.addEventListener('click', () => cartPanel.classList.add('open'));
closeCart.addEventListener('click', () => cartPanel.classList.remove('open'));

document.querySelector('.payment-options')?.addEventListener('click', (event) => {
    const button = event.target.closest('.payment-btn');
    if (!button) return;

    state.payment = button.dataset.payment;
    document.querySelectorAll('.payment-btn').forEach((btn) => btn.classList.toggle('active', btn === button));
    updatePaymentLabel();
});

checkoutBtn.addEventListener('click', () => {
    const methodLabel = state.payment === 'paypal' ? 'PayPal' : state.payment === 'cash' ? 'cash' : 'carte';
    const itemsText = state.cart.length
        ? state.cart.map((item) => `${item.quantity} × ${item.name}`).join(', ')
        : 'Aucun article sélectionné';
    const total = state.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const message = `Bonjour, je souhaite passer commande.\nArticles : ${itemsText}.\nTotal : ${total} €.\nPaiement : ${methodLabel}.`;
    const whatsappUrl = `https://wa.me/75249214?text=${encodeURIComponent(message)}`;

    paymentStatus.textContent = 'Ouverture de WhatsApp en cours...';
    window.location.href = whatsappUrl;
});

contactButton?.addEventListener('click', (event) => {
    event.preventDefault();
    const mailtoUrl = 'mailto:hello@novashop.fr?subject=Bonjour%20NovaShop';
    const whatsappUrl = 'https://wa.me/75249214?text=Bonjour%20NovaShop%2C%20je%20souhaite%20vous%20contacter.';

    window.location.href = mailtoUrl;
    setTimeout(() => {
        window.open(whatsappUrl, '_blank', 'noopener,noreferrer');
    }, 300);
});

document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
        const targetId = link.getAttribute('href');
        const section = document.querySelector(targetId);
        if (!section) return;

        event.preventDefault();
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
});

renderFilters();
renderProducts();
renderCart();
updatePaymentLabel();
