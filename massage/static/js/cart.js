document.addEventListener('DOMContentLoaded', () => {
  // Получение CSRF из cookie
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
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

  // Обновление счетчика корзины (если есть)
  function updateCartCount(count) {
    const cartCounter = document.getElementById('cart-count');
    if (cartCounter) {
      cartCounter.textContent = count;
    }
  }

  function updateItemUI(productId, newCount) {
    const item = document.querySelector(`.cart-item[data-product-id="${productId}"]`);
    if (!item) return;
    const countEl = item.querySelector('.item-count');
    if (countEl) countEl.textContent = newCount;

    if (newCount <= 0) {
      item.remove();
    }

    updateItemSubtotal(productId);
    updateTotal();
    updateUI();
  }

  function updateQuantity(productId, action) {
    fetch("/store/add_to_cart/", {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ product_id: productId, action: action })
    })
    .then(res => res.json())
    .then(data => {
      if ('count_for_product' in data) {
        updateItemUI(productId, data.count_for_product);
        updateCartCount(data.total_count);
      } else {
        alert('Ошибка обновления количества');
      }
    })
    .catch(() => alert('Ошибка сети'));
  }

  // Кнопки + и -
  const increaseButtons = document.querySelectorAll('.qty-btn.increase');
  const decreaseButtons = document.querySelectorAll('.qty-btn.decrease');

  increaseButtons.forEach(button => {
    button.addEventListener('click', () => {
      const productId = button.dataset.productId;
      updateQuantity(productId, 'add');
    });
  });

  decreaseButtons.forEach(button => {
    button.addEventListener('click', () => {
      const productId = button.dataset.productId;
      updateQuantity(productId, 'remove_one');
    });
  });

  // Удаление товара
  const removeButtons = document.querySelectorAll('.remove-item-btn');
  removeButtons.forEach(button => {
    button.addEventListener('click', () => {
      const productId = button.dataset.productId;
      fetch("/store/remove-from-cart/", {
        method: "POST",
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `product_id=${productId}`
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'ok') {
          document.querySelector(`.cart-item[data-product-id="${productId}"]`)?.remove();
          updateCartCount(data.total_count);
          updateUI();
        } else {
          alert('Ошибка при удалении из корзины');
        }
      })
      .catch(() => alert('Ошибка сети'));
    });
  });

  // Чекбоксы
  const checkboxes = document.querySelectorAll('input.select-item');
  const removeSelectedBtn = document.getElementById('removeSelectedBtn');
  const orderSelectedBtn = document.getElementById('orderSelectedBtn');
  const selectAllCheckbox = document.getElementById('selectAllCheckbox');

  function updateUI() {
    const totalCheckboxes = checkboxes.length;
    const checkedBoxes = [...checkboxes].filter(cb => cb.checked);
    const checkedCount = checkedBoxes.length;

    if (removeSelectedBtn) {
      removeSelectedBtn.style.display = checkedCount > 0 ? 'inline-block' : 'none';
    }

    if (orderSelectedBtn) {
      if (checkedCount === 0) {
        orderSelectedBtn.textContent = 'заказать выбранные';
        orderSelectedBtn.classList.add('disabled');
        orderSelectedBtn.disabled = true;
      } else if (checkedCount === totalCheckboxes) {
        orderSelectedBtn.textContent = 'заказать все';
        orderSelectedBtn.classList.remove('disabled');
        orderSelectedBtn.disabled = false;
      } else {
        orderSelectedBtn.textContent = 'заказать выбранные';
        orderSelectedBtn.classList.remove('disabled');
        orderSelectedBtn.disabled = false;
      }
    }

    if (selectAllCheckbox) {
      selectAllCheckbox.checked = checkedCount === totalCheckboxes;
      selectAllCheckbox.indeterminate = checkedCount > 0 && checkedCount < totalCheckboxes;
    }

    updateTotal();
  }

  checkboxes.forEach(cb => {
    cb.addEventListener('change', updateUI);
  });

  if (selectAllCheckbox) {
    selectAllCheckbox.addEventListener('change', () => {
      const check = selectAllCheckbox.checked;
      checkboxes.forEach(cb => cb.checked = check);
      updateUI();
    });
  }

  if (removeSelectedBtn) {
    removeSelectedBtn.addEventListener('click', () => {
      const selectedIds = [...checkboxes]
        .filter(cb => cb.checked)
        .map(cb => cb.value);

      if (selectedIds.length === 0) return;

      fetch("/store/remove-multiple-from-cart/", {
        method: "POST",
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_ids: selectedIds })
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'ok') {
          selectedIds.forEach(id => {
            document.querySelector(`.cart-item[data-product-id="${id}"]`)?.remove();
          });
          updateCartCount(data.total_count);
          updateUI();
        } else {
          alert('Ошибка при удалении выбранных товаров');
        }
      })
      .catch(() => alert('Ошибка сети'));
    });
  }

  // Обработка отправки заказа с выбранными товарами
  if (orderSelectedBtn) {
  orderSelectedBtn.addEventListener('click', (e) => {
    if (orderSelectedBtn.disabled) return;

    e.preventDefault();

    const selectedItems = [...checkboxes].filter(cb => cb.checked);
    const selectedIds = selectedItems.map(cb => cb.value);

    if (selectedIds.length === 0) return;

    const cartObject = {};

    selectedItems.forEach(cb => {
      const pid = cb.value;  // <-- вот это важно!
      const qtyElem = document.querySelector(`.item-count[data-product-id="${pid}"]`);
      const qty = qtyElem ? parseInt(qtyElem.textContent, 10) : 1;
      cartObject[pid] = qty;
    });

      // Ищем или создаём форму для отправки
      let form = document.getElementById('order-post-form');
      if (!form) {
        form = document.createElement('form');
        form.method = 'POST';
        form.action = '/order/';
        form.id = 'order-post-form';

        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrftoken;
        form.appendChild(csrfInput);

        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'cart_json';
        input.id = 'cart_json';
        form.appendChild(input);

        document.body.appendChild(form);
      }

      form.querySelector('#cart_json').value = JSON.stringify(cartObject);
      form.submit();
    });
  }

  updateUI();

  function updateItemSubtotal(productId) {
    const item = document.querySelector(`.cart-item[data-product-id="${productId}"]`);
    if (!item) return;

    const qtyEl = item.querySelector('.item-count');
    const priceEl = item.querySelector('.item-price');
    const subtotalEl = item.querySelector('.item-subtotal');

    if (qtyEl && priceEl && subtotalEl) {
      const qty = parseInt(qtyEl.textContent, 10) || 0;
      const price = parseFloat(priceEl.dataset.price);

      const subtotal = qty * price;
      subtotalEl.textContent = subtotal.toFixed(2) + ' ₽';
    }
  }

  function updateTotal() {
    let total = 0;

    const selectedCheckboxes = document.querySelectorAll('input.select-item:checked');

    selectedCheckboxes.forEach(checkbox => {
      const productId = checkbox.value;
      const cartItem = document.querySelector(`.cart-item[data-product-id="${productId}"]`);
      if (!cartItem) return;

      const subtotalSpan = cartItem.querySelector('.item-subtotal');
      if (!subtotalSpan) return;

      const text = subtotalSpan.textContent.replace('₽', '').trim().replace(/\s/g, '');
      const value = parseFloat(text);

      if (!isNaN(value)) total += value;
    });

    const totalEl = document.getElementById('cart-total');
    if (totalEl) {
      totalEl.textContent = total.toLocaleString('ru-RU');
    }
  }

});
