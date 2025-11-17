document.addEventListener('DOMContentLoaded', () => {
  const buttonsWrapper = document.getElementById('buttons-wrapper');

  const tabs = {
    'appointments-tab': document.getElementById('appointments-tab'),
    'purchases-tab': document.getElementById('purchases-tab'),
    'settings-form': document.getElementById('settings-form'),
  };

  const buttons = {
    'btn-appointments': 'appointments-tab',
    'btn-purchases': 'purchases-tab',
    'btn-settings': 'settings-form',
  };

  const backButtons = {
    'btn-back-appointments': 'appointments-tab',
    'btn-back-purchases': 'purchases-tab',
    'btn-back-from-settings': 'settings-form',
  };

  function hideAllTabs() {
    Object.values(tabs).forEach(tab => {
      tab.classList.remove('active');
      tab.classList.add('hidden');
    });
  }

  function showMainButtons() {
    buttonsWrapper.classList.remove('hidden');
  }

  function hideMainButtons() {
    buttonsWrapper.classList.add('hidden');
  }

  // Навешиваем обработчики на кнопки перехода
  for (const [btnId, tabId] of Object.entries(buttons)) {
    const btn = document.getElementById(btnId);
    if (btn && tabs[tabId]) {
      btn.addEventListener('click', () => {
        hideAllTabs();
        hideMainButtons();
        tabs[tabId].classList.remove('hidden');
        tabs[tabId].classList.add('active');
      });
    }
  }

  // Навешиваем обработчики на кнопки "назад"
  for (const [btnId, tabId] of Object.entries(backButtons)) {
    const btn = document.getElementById(btnId);
    if (btn && tabs[tabId]) {
      btn.addEventListener('click', () => {
        hideAllTabs();
        showMainButtons();
      });
    }
  }
});
