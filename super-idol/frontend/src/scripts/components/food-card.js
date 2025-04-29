import { formatNumber } from '../utils/helpers';
import { foodAPI } from '../utils/api';

class FoodCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  static get observedAttributes() {
    return ['food-data'];
  }

  async connectedCallback() {
    await this.loadTemplate();
    this.setupEventListeners();
  }

  async loadTemplate() {
    const response = await fetch('/components/food-card.html');
    const text = await response.text();
    const template = document.createElement('template');
    template.innerHTML = text;
    
    // Add styles
    const linkElem = document.createElement('link');
    linkElem.setAttribute('rel', 'stylesheet');
    linkElem.setAttribute('href', '/styles/components/food-card.css');
    
    this.shadowRoot.appendChild(linkElem);
    this.shadowRoot.appendChild(template.content.cloneNode(true));
  }

  setupEventListeners() {
    const editBtn = this.shadowRoot.querySelector('.edit-btn');
    const deleteBtn = this.shadowRoot.querySelector('.delete-btn');

    editBtn?.addEventListener('click', () => this.handleEdit());
    deleteBtn?.addEventListener('click', () => this.handleDelete());
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'food-data' && newValue !== oldValue) {
      this.updateContent(JSON.parse(newValue));
    }
  }

  updateContent(foodData) {
    if (!this.shadowRoot) return;

    const img = this.shadowRoot.querySelector('.food-card__image img');
    const title = this.shadowRoot.querySelector('.food-card__title');
    const description = this.shadowRoot.querySelector('.food-card__description');
    const calories = this.shadowRoot.querySelector('.calories');
    const protein = this.shadowRoot.querySelector('.protein');
    const carbs = this.shadowRoot.querySelector('.carbs');
    const fat = this.shadowRoot.querySelector('.fat');

    if (foodData.image) {
      img.src = foodData.image;
      img.alt = foodData.name;
    }

    title.textContent = foodData.name;
    description.textContent = foodData.description;
    calories.textContent = `${formatNumber(foodData.calories)} kcal`;
    protein.textContent = `${formatNumber(foodData.protein)}g`;
    carbs.textContent = `${formatNumber(foodData.carbs)}g`;
    fat.textContent = `${formatNumber(foodData.fat)}g`;
  }

  async handleEdit() {
    const foodData = JSON.parse(this.getAttribute('food-data'));
    const event = new CustomEvent('edit-food', {
      detail: { foodId: foodData.id },
      bubbles: true,
      composed: true
    });
    this.dispatchEvent(event);
  }

  async handleDelete() {
    if (!confirm('確定要刪除這個食物嗎？')) return;

    try {
      const foodData = JSON.parse(this.getAttribute('food-data'));
      await foodAPI.deleteFood(foodData.id);
      
      const event = new CustomEvent('delete-food', {
        detail: { foodId: foodData.id },
        bubbles: true,
        composed: true
      });
      this.dispatchEvent(event);
      
      this.remove();
    } catch (error) {
      console.error('Failed to delete food:', error);
      alert('刪除食物失敗');
    }
  }
}

customElements.define('food-card', FoodCard);

export function initFoodCard() {
    const foodCards = document.querySelectorAll('.food-card');
    if (!foodCards.length) return;

    foodCards.forEach(card => {
        const addToCartBtn = card.querySelector('.btn-primary');
        if (addToCartBtn) {
            addToCartBtn.addEventListener('click', () => {
                const foodId = card.dataset.id;
                const foodName = card.querySelector('h3').textContent;
                const foodPrice = card.querySelector('.price').textContent;
                
                // 添加到購物車的邏輯
                console.log(`Added ${foodName} (${foodId}) to cart. Price: ${foodPrice}`);
            });
        }
    });
} 