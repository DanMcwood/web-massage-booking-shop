document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('#bottomTabs a');
    const cards = document.querySelectorAll('.card-service');
    const selectedBar = document.getElementById('selectedServiceBar');
    const selectedName = document.getElementById('selectedServiceName');
    function activateTab(slug) {
        tabs.forEach(tab => tab.classList.toggle('active', tab.dataset.type === slug));

        cards.forEach(card => {
            card.style.display = (card.dataset.type === slug) ? 'flex' : 'none';
        });

        selectedBar.style.display = 'none';
    }

    tabs.forEach(tab => {
        tab.addEventListener('click', function (e) {
            e.preventDefault(); 
            const slug = tab.dataset.type; 
            activateTab(slug);
            window.location.hash = 'services-' + slug;
        });
    });

    window.showRelated = function (el) {
        const category = el.dataset.serviceCategory; 
        const serviceName = el.dataset.serviceName;  
        const isPriceOnly = el.classList.contains('price-no-sessions');
        selectedBar.style.display = 'flex';
        selectedName.textContent = serviceName;

        const deliveryBlock = document.getElementById('deliveryOptionsBlock');
        const serviceNameText = document.getElementById('selectedServiceNameText');

        if (isPriceOnly) {
            cards.forEach(card => card.style.display = 'none');
            deliveryBlock.style.display = 'flex';
            serviceNameText.textContent = serviceName;
        } else {
            cards.forEach(card => {
                card.style.display = (card.dataset.type === category && card !== el) ? 'flex' : 'none';
            });
            deliveryBlock.style.display = 'none';
        }
        tabs.forEach(tab => tab.classList.remove('active'));
    }

    window.resetView = function () {
        selectedBar.style.display = 'none';

        const deliveryBlock = document.getElementById('deliveryOptionsBlock');
        if (deliveryBlock) deliveryBlock.style.display = 'none';
        const slug = tabs[0] ? tabs[0].dataset.type : null;
        if (slug) activateTab(slug);
    }

    if (tabs.length > 0) {
        activateTab(tabs[0].dataset.type);
    }
});