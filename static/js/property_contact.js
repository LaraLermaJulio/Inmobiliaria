document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const showContactFormBtn = document.getElementById('showContactForm');
    const contactForm = document.getElementById('propertyContactForm');
    const cancelBtn = document.getElementById('cancelContactForm');
    const contactPropertyForm = document.getElementById('contactPropertyForm');
    const responseDiv = document.getElementById('contactFormResponse');
    
    // Mostrar formulario al hacer clic en "Contactar ahora"
    if (showContactFormBtn) {
        showContactFormBtn.addEventListener('click', function() {
            contactForm.style.display = 'block';
            showContactFormBtn.style.display = 'none';
        });
    }
    
    // Ocultar formulario al hacer clic en "Cancelar"
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            contactForm.style.display = 'none';
            showContactFormBtn.style.display = 'block';
            responseDiv.innerHTML = '';
            contactPropertyForm.reset();
        });
    }
    
    // Manejar envío del formulario
    if (contactPropertyForm) {
        contactPropertyForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Obtener el ID de la propiedad de la URL
            const pathParts = window.location.pathname.split('/');
            const propertyId = pathParts[pathParts.indexOf('detalle-propiedad') + 1];
            
            // Crear FormData para enviar
            const formData = new FormData(contactPropertyForm);
            
            // Enviar datos mediante fetch
            fetch(`/property/${propertyId}/contact/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    responseDiv.innerHTML = `<div class="success-message">${data.message}</div>`;
                    contactPropertyForm.reset();
                    
                    // Ocultar formulario después de 3 segundos
                    setTimeout(() => {
                        contactForm.style.display = 'none';
                        showContactFormBtn.style.display = 'block';
                        responseDiv.innerHTML = '';
                    }, 3000);
                } else {
                    responseDiv.innerHTML = `<div class="error-message">${data.message}</div>`;
                }
            })
            .catch(error => {
                responseDiv.innerHTML = '<div class="error-message">Error al enviar el mensaje. Inténtalo de nuevo.</div>';
                console.error('Error:', error);
            });
        });
    }
});