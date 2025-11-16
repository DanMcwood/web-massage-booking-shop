// Получение CSRF из куков
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Фильтр по имени товара
const searchInput = document.getElementById('shop-search-input');
searchInput.addEventListener('input', () => {
  const filter = searchInput.value.toLowerCase();
  document.querySelectorAll('.product-card').forEach(card => {
    card.style.display = card.dataset.name.includes(filter) ? 'block' : 'none';
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('productDetailModal');
  const detailImage = document.getElementById('detailImage');
  const detailName = document.getElementById('detailName');
  const detailDescription = document.getElementById('detailDescription');
  const detailPrice = document.getElementById('detailPrice');
  const detailCartControl = document.getElementById('detailCartControl');
  const modalCloseBtn = modal.querySelector('.modal-close-btn');

  function updateCounter(container, count) {
    const cartControl = container.querySelector('.cart-control');
    if (count > 0) {
      cartControl.innerHTML = `
        <div class="counter">
          <button class="counter-btn minus">−</button>
          <span class="count">${count}</span>
          <button class="counter-btn plus">+</button>
        </div>`;
    } else {
      cartControl.innerHTML = `<button class="add-to-cart-btn" data-product-id="${container.dataset.productId}">в корзину</button>`;
    }
  }

  function updateCounterModal(container, count) {
    if (count > 0) {
      container.innerHTML = `
        <div class="counter">
          <button class="counter-btn minus">−</button>
          <span class="count">${count}</span>
          <button class="counter-btn plus">+</button>
        </div>`;
    } else {
      container.innerHTML = `<button class="add-to-cart-btn" data-product-id="${modal.dataset.productId}">в корзину</button>`;
    }
  }

  function updateCartCount(count) {
    const cartCounter = document.getElementById('cart-count');
    if (cartCounter) {
      cartCounter.textContent = count;
    }
  }

  // Управление кнопками в каталоге
  document.querySelector('.products-grid').addEventListener('click', async e => {
    const target = e.target;
    if (!target.classList.contains('add-to-cart-btn') && !target.classList.contains('counter-btn')) return;

    const container = target.closest('.price-and-cart');
    const productId = container.dataset.productId;
    let action = null;

    if (target.classList.contains('add-to-cart-btn') || target.classList.contains('plus')) {
      action = 'add';
    } else if (target.classList.contains('minus')) {
      action = 'remove_one';
    }
    if (!action) return;

    const response = await fetch('/store/add_to_cart/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ product_id: productId, action }),
    });

    if (response.ok) {
      const data = await response.json();
      updateCounter(container, data.count_for_product);
      updateCartCount(data.total_count);

      if (!modal.classList.contains('hidden') && modal.dataset.productId === productId) {
        updateCounterModal(detailCartControl, data.count_for_product);
      }
    }
  });

  // Открытие модалки по клику на карточку (кроме кликов по кнопкам корзины)
  document.querySelectorAll('.product-card').forEach(card => {
    card.addEventListener('click', e => {
      if (e.target.closest('.price-and-cart')) return;

      const imgEl = card.querySelector('.product-images img');
      detailImage.src = imgEl.src;
      detailImage.alt = imgEl.alt;

      detailName.textContent = card.querySelector('h3').textContent;
      detailDescription.textContent = card.querySelector('.description').textContent;
      detailPrice.textContent = card.querySelector('.price-and-cart .price').textContent;

      modal.dataset.productId = card.querySelector('.price-and-cart').dataset.productId;
      detailCartControl.innerHTML = card.querySelector('.cart-control').innerHTML;

      modal.classList.remove('hidden');
    });
  });

  modalCloseBtn.addEventListener('click', () => {
    modal.classList.add('hidden');
  });

  modal.addEventListener('click', e => {
    if (e.target === modal) {
      modal.classList.add('hidden');
    }
  });

  // Кнопки в модалке
  detailCartControl.addEventListener('click', async e => {
    const target = e.target;
    if (!target.classList.contains('add-to-cart-btn') && !target.classList.contains('counter-btn')) return;

    const productId = modal.dataset.productId;
    let action = null;

    if (target.classList.contains('add-to-cart-btn') || target.classList.contains('plus')) {
      action = 'add';
    } else if (target.classList.contains('minus')) {
      action = 'remove_one';
    }
    if (!action) return;

    const response = await fetch('/store/add_to_cart/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ product_id: productId, action }),
    });

    if (response.ok) {
      const data = await response.json();
      updateCounterModal(detailCartControl, data.count_for_product);
      updateCartCount(data.total_count);

      const productCard = document.querySelector(`.price-and-cart[data-product-id="${productId}"]`);
      if (productCard) updateCounter(productCard, data.count_for_product);
    }
  });
});
