document.addEventListener('DOMContentLoaded', function() {
    // Get all profile toggle buttons
    const profileToggles = document.querySelectorAll('.profile-toggle');
    
    // Add click event to each toggle button
    profileToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            // Find the dropdown associated with this toggle
            const dropdown = this.nextElementSibling;
            if (dropdown && dropdown.classList.contains('profile-dropdown')) {
                dropdown.classList.toggle('show');
            }
        });
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.user-profile') && !e.target.closest('.mobile-profile') && !e.target.closest('.profile-toggle')) {
            document.querySelectorAll('.profile-dropdown').forEach(dropdown => {
                dropdown.classList.remove('show');
            });
        }
    });
});