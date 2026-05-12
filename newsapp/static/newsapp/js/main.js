document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.querySelector('.theme-toggle');
    const searchForm = document.getElementById('searchForm');
    const loadingOverlay = document.querySelector('.loading-overlay');
    const dropdowns = document.querySelectorAll('.custom-dropdown');

    // Theme toggle icon update (design stays dark-first)
    function updateThemeIcon(theme) {
        const isDark = theme === 'dark' || theme === null;
        themeToggle.innerHTML = isDark
            ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>`
            : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
    }

    // This design is dark by default; light mode is optional
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    themeToggle.addEventListener('click', () => {
        const current = document.body.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.body.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        updateThemeIcon(next);
    });

    // Custom Dropdown Logic
    dropdowns.forEach(dropdown => {
        const header = dropdown.querySelector('.dropdown-header');
        const list = dropdown.querySelector('.dropdown-list');
        const hiddenInput = dropdown.querySelector('input[type="hidden"]');
        const items = dropdown.querySelectorAll('.dropdown-item');
        const headerSpan = header.querySelector('span');

        header.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdowns.forEach(d => {
                if (d !== dropdown) d.querySelector('.dropdown-list').style.display = 'none';
            });
            list.style.display = list.style.display === 'block' ? 'none' : 'block';
        });

        items.forEach(item => {
            item.addEventListener('click', (e) => {
                e.stopPropagation();
                headerSpan.textContent = item.textContent.trim();
                hiddenInput.value = item.getAttribute('data-value');
                items.forEach(i => i.classList.remove('selected'));
                item.classList.add('selected');
                list.style.display = 'none';
            });
        });
    });

    document.addEventListener('click', () => {
        dropdowns.forEach(d => {
            d.querySelector('.dropdown-list').style.display = 'none';
        });
    });

    // Loading state
    if (searchForm) {
        searchForm.addEventListener('submit', () => {
            loadingOverlay.style.display = 'flex';
        });
    }

    // Image fallback
    document.querySelectorAll('.card-image img').forEach(img => {
        img.onerror = function () {
            this.src = 'https://images.unsplash.com/photo-1504711432869-53c035651372?q=80&w=1471&auto=format&fit=crop';
            this.onerror = null;
        };
    });

    // Staggered card entrance animation
    const cards = document.querySelectorAll('.news-card');
    cards.forEach((card, i) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(16px)';
        card.style.transition = `opacity 0.4s ease ${i * 0.05}s, transform 0.4s ease ${i * 0.05}s, border-color 0.3s, box-shadow 0.3s`;
        requestAnimationFrame(() => {
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 60 + i * 50);
        });
    });
});