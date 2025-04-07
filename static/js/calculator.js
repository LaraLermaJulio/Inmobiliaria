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