const app = {
    state: {
        table: null,
        cart: [],
        menu: []
    },

    init: async () => {
        try {
            const res = await fetch('/api/menu');
            app.state.menu = await res.json();
            app.renderMenu();
        } catch (e) {
            console.error("Failed to load menu", e);
        }
    },

    startSession: () => {
        const tableInput = document.getElementById('input-table');
        if (!tableInput.value) {
            alert("Please enter a table number");
            return;
        }
        app.state.table = tableInput.value;
        document.getElementById('lbl-table').innerText = app.state.table;
        document.getElementById('table-indicator').classList.remove('hidden');

        app.switchView('view-menu');
        document.getElementById('cart-float').classList.remove('hidden');
    },

    switchView: (viewId) => {
        ['view-scan', 'view-menu', 'view-checkout', 'view-success'].forEach(id => {
            document.getElementById(id).classList.add('hidden');
        });
        document.getElementById(viewId).classList.remove('hidden');
        window.scrollTo(0, 0);
    },

    renderMenu: () => {
        const container = document.getElementById('menu-list');
        container.innerHTML = app.state.menu.map(item => `
            <div class="card menu-item">
                <img src="${item.image}" class="menu-img" alt="${item.name}">
                <div class="menu-info">
                    <div style="font-weight: 600;">${item.name}</div>
                    <div style="color: var(--text-secondary); font-size: 14px;">${item.category}</div>
                    <div class="price">$${item.price.toFixed(2)}</div>
                </div>
                <div class="add-btn" onclick="app.addToCart('${item.id}')">
                    +
                </div>
            </div>
        `).join('');
    },

    addToCart: (itemId) => {
        const item = app.state.menu.find(i => i.id === itemId);
        const existing = app.state.cart.find(i => i.id === itemId);

        if (existing) {
            existing.quantity += 1;
        } else {
            app.state.cart.push({ ...item, quantity: 1 });
        }
        app.updateCartUI();
    },

    updateCartUI: () => {
        const count = app.state.cart.reduce((sum, i) => sum + i.quantity, 0);
        const total = app.state.cart.reduce((sum, i) => sum + (i.price * i.quantity), 0);

        document.getElementById('cart-count').innerText = count;
        document.getElementById('cart-total').innerText = '$' + total.toFixed(2);
        document.getElementById('lbl-total').innerText = '$' + total.toFixed(2);
    },

    showMenu: () => {
        app.switchView('view-menu');
        document.getElementById('cart-float').classList.remove('hidden');
    },

    showCheckout: () => {
        if (app.state.cart.length === 0) return;

        const container = document.getElementById('cart-items');
        container.innerHTML = app.state.cart.map(item => `
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <div>${item.quantity}x ${item.name}</div>
                <div>$${(item.price * item.quantity).toFixed(2)}</div>
            </div>
        `).join('');

        app.switchView('view-checkout');
        document.getElementById('cart-float').classList.add('hidden');
    },

    submitOrder: async () => {
        const paymentMethod = document.getElementById('payment-method').value;
        const total = app.state.cart.reduce((sum, i) => sum + (i.price * i.quantity), 0);

        const payload = {
            items: app.state.cart,
            total: total,
            table_number: parseInt(app.state.table),
            payment_method: paymentMethod
        };

        try {
            const res = await fetch('/api/order', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                app.switchView('view-success');
                app.state.cart = [];
                app.updateCartUI();
            }
        } catch (e) {
            alert("Error submitting order");
        }
    }
};

app.init();

