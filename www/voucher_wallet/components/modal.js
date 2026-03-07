// modal.js — a simple overlay that wraps any content element
// Click outside the content to close it

export function createModal(content) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.appendChild(content);

    // Close when the user clicks on the dark background (not on the content)
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) overlay.remove();
    });

    return overlay;
}
