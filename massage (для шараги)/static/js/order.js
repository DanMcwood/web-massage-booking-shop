document.addEventListener('DOMContentLoaded', () => {
  const nextBtn = document.getElementById('next-btn');
  const prevBtn = document.getElementById('prev-btn');
  const stepText = document.getElementById('step-text');
  const step1 = document.getElementById('step-1');
  const step2 = document.getElementById('step-2');

  const inputsStep1 = step1.querySelectorAll('input[type="text"], input[type="email"]');

  function validateStep1() {
    const allFilled = Array.from(inputsStep1).every(input => input.value.trim() !== '');
    nextBtn.disabled = !allFilled;
  }

  inputsStep1.forEach(input => input.addEventListener('input', validateStep1));

  validateStep1();

  step1.style.display = 'block';
  step2.style.display = 'none';

  nextBtn.addEventListener('click', () => {
    step1.style.display = 'none';
    step2.style.display = 'block';
    stepText.textContent = 'шаг 2 / 2';
  });

  prevBtn.addEventListener('click', () => {
    step2.style.display = 'none';
    step1.style.display = 'block';
    stepText.textContent = 'шаг 1 / 2';
  });

  const optionButtons = document.querySelectorAll('.option-btn');

  optionButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      optionButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const input = btn.querySelector('input[type="radio"]');
      if (input) input.checked = true;
    });
  });

  optionButtons.forEach(btn => {
    const input = btn.querySelector('input[type="radio"]');
    if (input && input.checked) {
      btn.classList.add('active');
    }
  });

  document.getElementById('order-form').addEventListener('submit', (e) => {
    // собираем выбранные товары из страницы (например, чекбоксы или из корзины)
    const selectedItems = [...document.querySelectorAll('input.select-item:checked')];
    const cartObject = {};

    selectedItems.forEach(cb => {
      const pid = cb.value;
      const qtyElem = document.querySelector(`.item-count[data-product-id="${pid}"]`);
      const qty = qtyElem ? parseInt(qtyElem.textContent, 10) : 1;
      cartObject[pid] = qty;
    });

    // если пусто, можно отменить отправку и предупредить
    if (Object.keys(cartObject).length === 0) {
      e.preventDefault();
      alert('Выберите товары для заказа');
      return;
    }

    // обновляем скрытое поле
    document.getElementById('cart_json').value = JSON.stringify(cartObject);
  });

});
