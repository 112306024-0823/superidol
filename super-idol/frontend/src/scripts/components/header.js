export function initHeader() {
    const header = document.querySelector('.header');
    if (!header) return;

    const nav = header.querySelector('.nav');
    if (nav) {
        nav.addEventListener('click', (e) => {
            if (e.target.matches('a[data-link]')) {
                e.preventDefault();
                const href = e.target.getAttribute('href');
                window.location.href = href;
            }
        });
    }
} 