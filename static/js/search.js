// Live Autocomplete and Search Handler
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('medicine-search-input');
    const suggestionsBox = document.getElementById('suggestions-box');

    if (!searchInput || !suggestionsBox) return;

    let debounceTimer;

    searchInput.addEventListener('input', function () {
        const query = this.value.trim();
        clearTimeout(debounceTimer);

        if (query.length < 2) {
            suggestionsBox.style.display = 'none';
            suggestionsBox.innerHTML = '';
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/api/search-suggestions?q=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => {
                    suggestionsBox.innerHTML = '';
                    if (data && data.length > 0) {
                        data.forEach(item => {
                            const div = document.createElement('div');
                            div.className = 'suggestion-item d-flex justify-content-between align-items-center';
                            
                            const genericBadge = item.is_generic 
                                ? '<span class="badge badge-generic">Generic</span>'
                                : '<span class="badge badge-brand">Brand</span>';

                            div.innerHTML = `
                                <div>
                                    <strong>${item.name}</strong> 
                                    <small class="text-muted d-block">${item.generic_name} • ${item.strength} (${item.category})</small>
                                </div>
                                <div class="text-end">
                                    ${genericBadge}
                                    <small class="text-muted d-block">MRP: ₹${item.mrp.toFixed(2)}</small>
                                </div>
                            `;

                            div.addEventListener('click', function () {
                                searchInput.value = item.name;
                                suggestionsBox.style.display = 'none';
                                // Auto-submit search form
                                const form = searchInput.closest('form');
                                if (form) form.submit();
                            });

                            suggestionsBox.appendChild(div);
                        });
                        suggestionsBox.style.display = 'block';
                    } else {
                        suggestionsBox.innerHTML = '<div class="p-3 text-muted text-center"><small>No matching medicines found.</small></div>';
                        suggestionsBox.style.display = 'block';
                    }
                })
                .catch(err => console.error('Error fetching suggestions:', err));
        }, 250);
    });

    // Close suggestions on outside click
    document.addEventListener('click', function (e) {
        if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
            suggestionsBox.style.display = 'none';
        }
    });
});

