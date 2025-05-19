function calculateMortgage(propertyPrice) {
    const downPaymentPercent = document.getElementById('down-payment').value / 100;
    const loanTerm = document.getElementById('loan-term').value;
    const interestRate = document.getElementById('interest-rate').value / 100;

    const downPayment = propertyPrice * downPaymentPercent;
    const loanAmount = propertyPrice - downPayment;
    const monthlyRate = interestRate / 12;
    const numberOfPayments = loanTerm * 12;

    const monthlyPayment = (loanAmount * monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments)) / 
                          (Math.pow(1 + monthlyRate, numberOfPayments) - 1);

    const totalPayment = monthlyPayment * numberOfPayments;

    const resultElement = document.getElementById('mortgage-result');
    resultElement.innerHTML = `
        <h4>Resumen del Préstamo</h4>
        <div class="result-grid">
            <div class="result-item">
                <h4>Pago Mensual</h4>
                <p>$${monthlyPayment.toFixed(2)} MXN</p>
            </div>
            <div class="result-item">
                <h4>Enganche</h4>
                <p>$${downPayment.toFixed(2)} MXN</p>
            </div>
            <div class="result-item">
                <h4>Monto del Préstamo</h4>
                <p>$${loanAmount.toFixed(2)} MXN</p>
            </div>
            <div class="result-item">
                <h4>Costo Total</h4>
                <p>$${totalPayment.toFixed(2)} MXN</p>
            </div>
        </div>
    `;
    resultElement.classList.add('active');
}

// Función para validar campos numéricos
function validateNumericInput(input, min, max) {
    // Eliminar caracteres no numéricos (excepto punto decimal)
    input.value = input.value.replace(/[^\d.]/g, '');
    
    // Asegurar que solo haya un punto decimal
    const parts = input.value.split('.');
    if (parts.length > 2) {
        input.value = parts[0] + '.' + parts.slice(1).join('');
    }
    
    // Convertir a número para validar rango
    let value = parseFloat(input.value);
    
    // Si no es un número, establecer a valor mínimo
    if (isNaN(value)) {
        input.value = min;
        return;
    }
    
    // Validar rango
    if (value < min) {
        input.value = min;
    } else if (value > max) {
        input.value = max;
    }
}

// Inicializar validaciones cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencias a los campos
    const downPaymentInput = document.getElementById('down-payment');
    const loanTermInput = document.getElementById('loan-term');
    const interestRateInput = document.getElementById('interest-rate');
    
    // Si los elementos existen, agregar validaciones
    if (downPaymentInput) {
        downPaymentInput.addEventListener('input', function() {
            validateNumericInput(this, 0, 100);
        });
    }
    
    if (loanTermInput) {
        loanTermInput.addEventListener('input', function() {
            validateNumericInput(this, 1, 30);
        });
    }
    
    if (interestRateInput) {
        interestRateInput.addEventListener('input', function() {
            validateNumericInput(this, 0, 100);
        });
    }
});
