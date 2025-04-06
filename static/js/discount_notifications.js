// Discount notification system
document.addEventListener('DOMContentLoaded', function() {
    // Track which notifications have been shown in this session
    const shownNotifications = new Set();
    
    // Track the last time we checked for discounts
    let lastCheckTime = Date.now();
    
    // Function to fetch discounted properties
    function checkForDiscountedProperties() {
        fetch('/api/discounted-properties/')
            .then(response => response.json())
            .then(data => {
                if (data.properties && data.properties.length > 0) {
                    const currentTime = Date.now();
                    
                    // Show notification for each discounted property
                    data.properties.forEach(property => {
                        // Only show if not already shown in this session and not closed before
                        // or if the discount percentage has changed since it was closed
                        if (!shownNotifications.has(property.id) && shouldShowAlert(property.id, property.discount_percentage)) {
                            showDiscountAlert(property);
                            shownNotifications.add(property.id); // Mark as shown in this session
                        }
                    });
                    
                    // Update last check time
                    lastCheckTime = currentTime;
                }
            })
            .catch(error => console.error('Error fetching discounted properties:', error));
    }

    // Function to mark an alert as closed in localStorage with its current discount
    function markAlertAsClosed(propertyId, discountPercentage) {
        const closedAlerts = JSON.parse(localStorage.getItem('closedDiscountAlerts') || '{}');
        closedAlerts[propertyId] = {
            timestamp: Date.now(),
            discountPercentage: discountPercentage
        };
        localStorage.setItem('closedDiscountAlerts', JSON.stringify(closedAlerts));
    }
    
    // Check if we should show alerts based on closed status and discount changes
    function shouldShowAlert(propertyId, currentDiscountPercentage) {
        const closedAlerts = JSON.parse(localStorage.getItem('closedDiscountAlerts') || '{}');
        
        // If property was never closed, show it
        if (!closedAlerts.hasOwnProperty(propertyId)) {
            return true;
        }
        
        // If the discount percentage has changed, show it again
        const closedData = closedAlerts[propertyId];
        if (typeof closedData === 'object' && 
            closedData.discountPercentage !== undefined && 
            parseFloat(closedData.discountPercentage) !== parseFloat(currentDiscountPercentage)) {
            return true;
        }
        
        // For backward compatibility with old format
        if (typeof closedData === 'number') {
            return true; // Show it if the format has changed
        }
        
        return false;
    }
    
    // Function to show discount alert
    function showDiscountAlert(property) {
        // Check if alert for this property already exists on the page
        if (document.querySelector(`.discount-alert[data-property-id="${property.id}"]`)) {
            return; // Don't show duplicate alerts
        }
        
        // Create the alert div
        const alertDiv = document.createElement('div');
        alertDiv.className = 'discount-alert';
        alertDiv.setAttribute('data-property-id', property.id);
        
        // Calculate position based on existing alerts
        const existingAlerts = document.querySelectorAll('.discount-alert');
        const alertHeight = 180; // Approximate height of each alert
        const spacing = 30; // Increased spacing between alerts
        const bottomPosition = 20 + (existingAlerts.length * (alertHeight + spacing));
        
        alertDiv.style.bottom = `${bottomPosition}px`;
        
        alertDiv.innerHTML = `
            <div class="discount-alert-content">
                <span class="discount-alert-close">&times;</span>
                <h3>¡Oferta Especial!</h3>
                <p>La propiedad "${property.title}" ahora tiene un descuento del ${property.discount_percentage}%</p>
                <p>Precio original: $${property.price} MXN</p>
                <p>Precio con descuento: $${property.discounted_price} MXN</p>
                <a href="/detalle-propiedad/${property.id}/" class="discount-alert-button">Ver Propiedad</a>
            </div>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Show the alert with animation
        setTimeout(() => {
            alertDiv.classList.add('show');
        }, 100);
        
        // Close button functionality
        const closeButton = alertDiv.querySelector('.discount-alert-close');
        closeButton.addEventListener('click', function() {
            alertDiv.classList.remove('show');
            setTimeout(() => {
                alertDiv.remove();
                // Reposition remaining alerts
                repositionAlerts();
            }, 300);
            
            // Store in localStorage that this alert was closed with its current discount
            markAlertAsClosed(property.id, property.discount_percentage);
        });
        
        // Add click event to the "Ver Propiedad" button
        const viewButton = alertDiv.querySelector('.discount-alert-button');
        viewButton.addEventListener('click', function() {
            // Store in localStorage that this alert was closed with its current discount
            markAlertAsClosed(property.id, property.discount_percentage);
        });
    }
    
    // Function to reposition alerts after one is closed
    function repositionAlerts() {
        const alerts = document.querySelectorAll('.discount-alert');
        const alertHeight = 180; // Approximate height of each alert
        const spacing = 30; // Increased spacing between alerts
        
        alerts.forEach((alert, index) => {
            const bottomPosition = 20 + (index * (alertHeight + spacing));
            alert.style.bottom = `${bottomPosition}px`;
        });
    }
    
    // Check for discounted properties when page loads
    checkForDiscountedProperties();
    
    // Periodically check for new discounted properties (every 30 seconds)
    setInterval(checkForDiscountedProperties, 30000);
});