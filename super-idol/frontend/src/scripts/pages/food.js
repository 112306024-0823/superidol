import { foodAPI } from '../utils/api.js';
import { initFoodCard } from '../components/food-card.js';
import { debounce } from '../utils/helpers';

class FoodInventoryPage {
  constructor() {
    this.currentPage = 1;
    this.pageSize = 12;
    this.totalPages = 1;
    this.searchTerm = '';
    this.sortBy = 'name';
    this.sortOrder = 'asc';
    
    this.initElements();
    this.setupEventListeners();
    this.loadFoods();
  }

  initElements() {
    this.foodGrid = document.getElementById('foodGrid');
    this.loadingSpinner = document.getElementById('loading');
    this.noResults = document.getElementById('noResults');
    this.prevPageBtn = document.getElementById('prevPage');
    this.nextPageBtn = document.getElementById('nextPage');
    this.currentPageSpan = document.getElementById('currentPage');
    this.searchInput = document.getElementById('searchInput');
    this.sortBySelect = document.getElementById('sortBy');
    this.sortOrderSelect = document.getElementById('sortOrder');
  }

  setupEventListeners() {
    this.searchInput.addEventListener('input', debounce(() => {
      this.currentPage = 1;
      this.searchTerm = this.searchInput.value;
      this.loadFoods();
    }, 300));

    this.sortBySelect.addEventListener('change', () => {
      this.sortBy = this.sortBySelect.value;
      this.loadFoods();
    });

    this.sortOrderSelect.addEventListener('change', () => {
      this.sortOrder = this.sortOrderSelect.value;
      this.loadFoods();
    });

    this.prevPageBtn.addEventListener('click', () => {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.loadFoods();
      }
    });

    this.nextPageBtn.addEventListener('click', () => {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.loadFoods();
      }
    });

    this.foodGrid.addEventListener('edit-food', (event) => {
      const { foodId } = event.detail;
      window.location.href = `/food/edit.html?id=${foodId}`;
    });

    this.foodGrid.addEventListener('delete-food', () => {
      this.loadFoods();
    });
  }

  async loadFoods() {
    try {
      this.showLoading();

      const params = {
        page: this.currentPage,
        limit: this.pageSize,
        search: this.searchTerm,
        sort_by: this.sortBy,
        sort_order: this.sortOrder
      };

      const response = await foodAPI.getAllFoods(params);
      const { items, total, total_pages } = response.data;

      this.totalPages = total_pages;
      this.updatePagination();
      this.renderFoods(items);

      if (items.length === 0) {
        this.showNoResults();
      }
    } catch (error) {
      console.error('Failed to load foods:', error);
      alert('載入食物列表失敗');
    } finally {
      this.hideLoading();
    }
  }

  renderFoods(foods) {
    this.foodGrid.innerHTML = '';
    
    foods.forEach(food => {
      const foodCard = document.createElement('food-card');
      foodCard.setAttribute('food-data', JSON.stringify(food));
      this.foodGrid.appendChild(foodCard);
    });

    // 初始化食物卡片
    initFoodCard();
  }

  updatePagination() {
    this.currentPageSpan.textContent = this.currentPage;
    this.prevPageBtn.disabled = this.currentPage === 1;
    this.nextPageBtn.disabled = this.currentPage === this.totalPages;
  }

  showLoading() {
    this.loadingSpinner.style.display = 'flex';
    this.noResults.style.display = 'none';
  }

  hideLoading() {
    this.loadingSpinner.style.display = 'none';
  }

  showNoResults() {
    this.noResults.style.display = 'block';
  }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
  new FoodInventoryPage();
});

export function initFood() {
    const foodGrid = document.querySelector('.food-grid');
    if (!foodGrid) return;

    // 獲取食物數據
    foodAPI.getFoods()
        .then(foods => {
            // 渲染食物卡片
            foodGrid.innerHTML = foods.map(food => `
                <div class="food-card" data-id="${food.id}">
                    <img src="${food.image}" alt="${food.name}">
                    <div class="food-card-content">
                        <h3>${food.name}</h3>
                        <p>${food.description}</p>
                        <div class="price">$${food.price}</div>
                        <div class="actions">
                            <button class="btn btn-primary">加入購物車</button>
                        </div>
                    </div>
                </div>
            `).join('');

            // 初始化食物卡片
            initFoodCard();
        })
        .catch(error => {
            console.error('Failed to load food data:', error);
            foodGrid.innerHTML = '<p>載入食物數據失敗</p>';
        });
} 