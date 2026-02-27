// Marketplace JavaScript

class MarketplaceCart {
  constructor() {
    this.cartCount = 0;
    this.init();
  }

  init() {
    this.updateCartCount();
    this.setupEventListeners();
  }

  setupEventListeners() {
    // Add to cart buttons
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
      button.addEventListener('click', (e) => this.handleAddToCart(e));
    });

    // Quantity controls
    document.querySelectorAll('.quantity-btn').forEach(button => {
      button.addEventListener('click', (e) => this.handleQuantityChange(e));
    });

    // Remove from cart buttons
    document.querySelectorAll('.remove-from-cart-btn').forEach(button => {
      button.addEventListener('click', (e) => this.handleRemoveFromCart(e));
    });

    // Update quantity on input change
    document.querySelectorAll('.quantity-input').forEach(input => {
      input.addEventListener('change', (e) => this.handleQuantityUpdate(e));
    });
  }

  async handleAddToCart(event) {
    const button = event.currentTarget;
    const productId = button.dataset.productId;
    const productName = button.dataset.productName;
    
    try {
      button.disabled = true;
      button.innerHTML = '<i class="bi bi-spinner"></i> Adding...';

      const response = await fetch(`/marketplace/cart/add/${productId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': this.getCSRFToken()
        },
        body: `product_id=${productId}`,
        credentials: 'same-origin'
      });

      const data = await response.json();
      
      if (data.success) {
        this.cartCount = data.cart_count;
        this.updateCartUI();
        this.showNotification(`${productName} added to cart!`, 'success');
        
        // Update button state
        button.classList.add('added');
        button.innerHTML = '<i class="bi bi-check"></i> Added';
        setTimeout(() => {
          button.classList.remove('added');
          button.innerHTML = '<i class="bi bi-cart-plus"></i> Add to Cart';
          button.disabled = false;
        }, 2000);
      } else {
        throw new Error(data.error || 'Failed to add to cart');
      }
    } catch (error) {
      console.error('Error adding to cart:', error);
      this.showNotification('Error adding to cart', 'error');
      button.innerHTML = '<i class="bi bi-cart-plus"></i> Add to Cart';
      button.disabled = false;
    }
  }

  async handleQuantityChange(event) {
    const button = event.currentTarget;
    const action = button.dataset.action;
    const productId = button.dataset.productId;
    const input = document.querySelector(`#quantity-${productId}`);
    const currentQuantity = parseInt(input.value);
    
    let newQuantity = currentQuantity;
    if (action === 'increase') {
      newQuantity = currentQuantity + 1;
    } else if (action === 'decrease' && currentQuantity > 1) {
      newQuantity = currentQuantity - 1;
    }
    
    if (newQuantity !== currentQuantity) {
      await this.updateQuantity(productId, newQuantity);
    }
  }

  async handleQuantityUpdate(event) {
    const input = event.currentTarget;
    const productId = input.dataset.productId;
    const newQuantity = parseInt(input.value);
    
    if (newQuantity > 0) {
      await this.updateQuantity(productId, newQuantity);
    }
  }

  async updateQuantity(productId, quantity) {
    try {
      const response = await fetch(`/marketplace/api/update-quantity/?product_id=${productId}&quantity=${quantity}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();
      
      if (data.success) {
        this.cartCount = data.cart_count;
        this.updateCartUI();
        this.updateCartTotals();
        this.showNotification(`${data.product_name} updated to ${quantity} in cart`, 'success');
      } else {
        throw new Error(data.error || 'Failed to update quantity');
      }
    } catch (error) {
      console.error('Error updating quantity:', error);
      this.showNotification('Error updating quantity', 'error');
    }
  }

  async removeFromCart(productId, productName = null) {
    try {
      const response = await fetch('/marketplace/api/cart/remove/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken()
        },
        body: JSON.stringify({
          product_id: productId,
          product_name: productName
        })
      });

      const data = await response.json();
      
      if (data.success) {
        this.cartCount = data.cart_count;
        this.updateCartUI();
        this.updateCartTotals();
        this.showNotification(`${productName || 'Product'} removed from cart`, 'success');
      } else {
        throw new Error(data.error || 'Failed to remove from cart');
      }
    } catch (error) {
      console.error('Error removing from cart:', error);
      this.showNotification('Failed to remove item from cart', 'error');
    }
  }

  async handleRemoveFromCart(event) {
    const button = event.currentTarget;
    const productId = button.dataset.productId;
    const productName = button.dataset.productName;
    
    if (!confirm(`Are you sure you want to remove ${productName} from your cart?`)) {
      return;
    }

    try {
      button.disabled = true;
      button.innerHTML = '<i class="bi bi-spinner"></i> Removing...';

      const response = await fetch('/marketplace/cart/remove/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': this.getCSRFToken()
        },
        body: `product_id=${productId}`
      });

      const data = await response.json();
      
      if (data.success) {
        this.cartCount = data.cart_count;
        this.updateCartUI();
        this.showNotification(`${productName} removed from cart`, 'success');
        
        // Remove item from DOM
        const cartItem = document.querySelector(`#cart-item-${productId}`);
        if (cartItem) {
          cartItem.style.opacity = '0';
          setTimeout(() => cartItem.remove(), 300);
        }
        
        this.updateCartTotals();
        
        // Check if cart is empty
        const remainingItems = document.querySelectorAll('.cart-item');
        if (remainingItems.length === 0) {
          this.showEmptyCart();
        }
      } else {
        throw new Error(data.error || 'Failed to remove from cart');
      }
    } catch (error) {
      console.error('Error removing from cart:', error);
      this.showNotification('Error removing from cart', 'error');
      button.innerHTML = '<i class="bi bi-trash"></i> Remove';
      button.disabled = false;
    }
  }

  async updateCartCount() {
    try {
      const response = await fetch('/marketplace/api/cart-count/');
      const data = await response.json();
      this.cartCount = data.count;
      this.updateCartUI();
    } catch (error) {
      console.error('Error fetching cart count:', error);
    }
  }

  updateCartUI() {
    const cartBadges = document.querySelectorAll('.cart-count');
    cartBadges.forEach(badge => {
      badge.textContent = this.cartCount;
      badge.style.display = this.cartCount > 0 ? 'inline' : 'none';
    });
  }

  updateCartTotals() {
    // This would typically be updated via server response
    // For now, we can trigger a page reload or make an API call
    window.location.reload();
  }

  showEmptyCart() {
    const cartItems = document.querySelector('.cart-items');
    if (cartItems) {
      cartItems.innerHTML = `
        <div class="empty-cart text-center py-5">
          <i class="bi bi-cart-x" style="font-size: 3rem; color: #dee2e6;"></i>
          <h3 class="mt-3">Your cart is empty</h3>
          <p class="text-muted">Add some products to get started!</p>
          <a href="/marketplace/" class="btn btn-primary mt-3">
            <i class="bi bi-shop"></i> Browse Products
          </a>
        </div>
      `;
    }
  }

  showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `cart-notification show ${type}`;
    notification.innerHTML = `
      <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
      ${message}
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }

  getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : this.getCookie('csrftoken');
  }

  getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
}

// Initialize marketplace cart when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.marketplaceCart = new MarketplaceCart();
});

// Export for use in other scripts
window.MarketplaceCart = MarketplaceCart;
