export function setupRouter() {
    // 攔截所有連結點擊
    document.addEventListener('click', (e) => {
        if (e.target.matches('[data-link]')) {
            e.preventDefault();
            const href = e.target.getAttribute('href');
            navigateTo(href);
        }
    });
}

export function navigateTo(path) {
    window.history.pushState(null, null, path);
    window.dispatchEvent(new PopStateEvent('popstate'));
} 