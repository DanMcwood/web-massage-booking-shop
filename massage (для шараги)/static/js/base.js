document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.getElementById('menuItems');
    const links = menuItems.querySelectorAll('a');
    const onlineBookingBtn = document.getElementById('onlineBookingBtn');

    const pathSegments = window.location.pathname.toLowerCase().replace(/^\/|\/$/g, '').split('/');
    let section = pathSegments.length > 0 ? pathSegments[pathSegments.length - 1] : 'home';

    if (pathSegments[0] === 'order') {
        section = 'cart';
    }

    const fromPage = document.body.getAttribute('data-from') || '';

    const profileLink = document.querySelector('#menuItems .menu-profile'); // ограничим только десктоп

    if (profileLink) {
        let from = '';

        if (section === 'store') {
            from = 'store';
        } else if (section === 'cart') {
            from = 'cart';
        } else if (section === 'home') {
            from = 'home';
        } else if (section === 'services') {
            from = 'services';
        } else if (section === 'contacts') {
            from = 'contacts';
        }

        if (from) {
            const baseHref = profileLink.getAttribute('href').split('?')[0];
            profileLink.setAttribute('href', `${baseHref}?from=${from}`);
        }
    }

    function setActiveMenu(section) {
        links.forEach(link => {
            const linkSection = link.getAttribute('data-section');
            if (linkSection === section) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    function applySpecialLayout(section) {
        // НЕ трогаем mobile-nav, меняем только desktop menuItems
        const isShopOrCart = ['store', 'cart'].includes(section);

        if (isShopOrCart) {
            menuItems.querySelector('.menu-services').style.display = 'none';
            menuItems.querySelector('.menu-contacts').style.display = 'none';

            menuItems.querySelector('.menu-shop').style.order = '2';
            menuItems.querySelector('.menu-cart').style.order = '1';
            menuItems.querySelector('.menu-profile').style.order = '3';

            menuItems.querySelector('.menu-shop').style.display = 'flex';
            menuItems.querySelector('.menu-cart').style.display = 'flex';
            menuItems.querySelector('.menu-profile').style.display = 'flex';

            onlineBookingBtn.style.display = 'none';
            menuItems.style.justifyContent = 'space-between';
        } else {
            links.forEach(link => {
                link.style.display = 'flex';
                link.style.order = '0';
            });

            onlineBookingBtn.style.display = (section === 'home') ? 'none' : 'flex';
            menuItems.querySelector('.menu-cart').style.display = 'none';
            menuItems.style.justifyContent = 'center';
        }
    }

    setActiveMenu(section);
    applySpecialLayout(section);
});

// Бургер-меню
const burger = document.getElementById('burgerMenu');
const mobileNav = document.getElementById('mobileNav');

burger.addEventListener('click', () => {
    mobileNav.classList.toggle('open');
    document.body.classList.toggle('mobile-open');
});
