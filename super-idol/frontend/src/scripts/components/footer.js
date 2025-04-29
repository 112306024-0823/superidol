export function initFooter() {
    const footer = document.querySelector('.footer');
    if (!footer) return;

    const year = new Date().getFullYear();
    footer.querySelector('p').textContent = `© ${year} Super Idol. All rights reserved.`;
} 