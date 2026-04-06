document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const themeToggle = document.querySelector('.theme-toggle');
    const body = document.body;
    const searchForm = document.getElementById('searchForm');
    const loadingOverlay = document.querySelector('.loading-overlay');
    const dropdowns = document.querySelectorAll('.custom-dropdown');

    // Theme Management
    const savedTheme = localStorage.getItem('theme') || 'light';
    body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    themeToggle.addEventListener('click', () => {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        themeToggle.innerHTML = theme === 'light' ? '🌙' : '☀️';
    }

    // Custom Dropdown Logic
    dropdowns.forEach(dropdown => {
        const header = dropdown.querySelector('.dropdown-header');
        const list = dropdown.querySelector('.dropdown-list');
        const hiddenInput = dropdown.querySelector('input[type="hidden"]');
        const items = dropdown.querySelectorAll('.dropdown-item');
        const headerText = header.querySelector('span');

        header.addEventListener('click', (e) => {
            e.stopPropagation();
            // Close other dropdowns
            dropdowns.forEach(d => {
                if (d !== dropdown) d.querySelector('.dropdown-list').style.display = 'none';
            });
            const isOpen = list.style.display === 'block';
            list.style.display = isOpen ? 'none' : 'block';
        });

        items.forEach(item => {
            item.addEventListener('click', (e) => {
                e.stopPropagation();
                const value = item.getAttribute('data-value');
                const text = item.textContent;

                // Update UI
                headerText.textContent = text;
                hiddenInput.value = value;
                
                // Update selection state
                items.forEach(i => i.classList.remove('selected'));
                item.classList.add('selected');

                // Close list
                list.style.display = 'none';
            });
        });
    });

    // Close dropdowns on outside click
    document.addEventListener('click', () => {
        dropdowns.forEach(d => {
            d.querySelector('.dropdown-list').style.display = 'none';
        });
    });

    // Loading State
    if (searchForm) {
        searchForm.addEventListener('submit', () => {
            loadingOverlay.style.display = 'flex';
        });
    }

    // Image Fallback Handling
    const newsImages = document.querySelectorAll('.card-image img');
    newsImages.forEach(img => {
        img.onerror = function() {
            this.src = 'https://images.unsplash.com/photo-1504711432869-53c035651372?q=80&w=1471&auto=format&fit=crop';
            this.onerror = null; // Prevent infinite loop
        };
    });
});
