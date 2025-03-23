document.addEventListener('DOMContentLoaded', function() {
    const filterToggle = document.getElementById('filterToggle');
    const filtersSidebar = document.querySelector('.filters-sidebar');
    
    if (filterToggle && filtersSidebar) {
        filterToggle.addEventListener('click', function() {
            filtersSidebar.classList.toggle('active');
            
            if (filtersSidebar.classList.contains('active')) {
                filterToggle.textContent = 'Ocultar Filtros';
            } else {
                filterToggle.textContent = 'Mostrar Filtros';
            }
        });
    } else {
        console.error('Filter toggle button or sidebar not found');
    }
});
