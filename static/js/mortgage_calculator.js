// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    console.log('Calculadora de hipoteca cargada');
    
    // Inicializar jsPDF
    window.jspdf = window.jspdf || {};
    window.jspdf.jsPDF = window.jsPDF;
    
    // Obtener referencias a los elementos del DOM
    const calculateButton = document.getElementById('calculateButton');
    const printButton = document.getElementById('printButton');
    
    // Verificar si los elementos existen
    if (calculateButton) {
        console.log('Botón de cálculo encontrado');
        calculateButton.addEventListener('click', function() {
            // Obtener el precio de la propiedad
            let propertyPrice = 0;
            const priceElement = document.querySelector('.property-price');
            if (priceElement) {
                const priceText = priceElement.textContent;
                propertyPrice = parseFloat(priceText.replace(/[^\d.]/g, ''));
            } else {
                const discountPriceElement = document.querySelector('.property-discount-price');
                if (discountPriceElement) {
                    const priceText = discountPriceElement.textContent;
                    propertyPrice = parseFloat(priceText.replace(/[^\d.]/g, ''));
                }
            }
            
            if (propertyPrice > 0) {
                console.log('Precio de propiedad encontrado:', propertyPrice);
                calculateMortgage(propertyPrice);
            } else {
                alert('No se pudo determinar el precio de la propiedad');
            }
        });
    } else {
        console.error('Botón de cálculo no encontrado');
    }
    
    // Agregar event listener al botón de impresión si existe
    if (printButton) {
        console.log('Botón de impresión encontrado');
        printButton.addEventListener('click', generateMortgagePDF);
    } else {
        console.error('Botón de impresión no encontrado');
    }
});

// Función para calcular la hipoteca
function calculateMortgage(propertyPrice) {
    console.log('Calculando hipoteca para precio:', propertyPrice);
    
    const downPaymentPercent = parseFloat(document.getElementById('down-payment').value);
    const loanTerm = parseInt(document.getElementById('loan-term').value);
    const interestRate = parseFloat(document.getElementById('interest-rate').value);
    
    // Calcular el enganche en cantidad
    const downPayment = (downPaymentPercent / 100) * propertyPrice;
    
    // Calcular el monto del préstamo
    const loanAmount = propertyPrice - downPayment;
    
    // Calcular la tasa de interés mensual
    const monthlyInterestRate = (interestRate / 100) / 12;
    
    // Calcular el número de pagos
    const numberOfPayments = loanTerm * 12;
    
    // Calcular el pago mensual
    const monthlyPayment = (loanAmount * monthlyInterestRate * Math.pow(1 + monthlyInterestRate, numberOfPayments)) / 
                          (Math.pow(1 + monthlyInterestRate, numberOfPayments) - 1);
    
    // Calcular el costo total
    const totalCost = monthlyPayment * numberOfPayments;
    
    // Mostrar los resultados
    const resultDiv = document.getElementById('mortgage-result');
    resultDiv.innerHTML = `
        <h4>Resumen del Préstamo</h4>
        <p><strong>Pago Mensual:</strong> $${monthlyPayment.toFixed(2)} MXN</p>
        <p><strong>Enganche:</strong> $${downPayment.toFixed(2)} MXN</p>
        <p><strong>Monto del Préstamo:</strong> $${loanAmount.toFixed(2)} MXN</p>
        <p><strong>Costo Total:</strong> $${totalCost.toFixed(2)} MXN</p>
    `;
    
    // Mostrar el botón de imprimir
    const printButton = document.getElementById('printButton');
    if (printButton) {
        printButton.style.display = 'block';
    }
    
    // Guardar los resultados para el PDF
    window.mortgageData = {
        propertyTitle: document.querySelector('.property-header h1').textContent,
        propertyPrice: propertyPrice,
        downPayment: downPayment,
        loanAmount: loanAmount,
        monthlyPayment: monthlyPayment,
        totalCost: totalCost,
        interestRate: interestRate,
        loanTerm: loanTerm
    };
    
    console.log('Cálculo de hipoteca completado');
}

// Función para generar el PDF
function generateMortgagePDF() {
    console.log('Generando PDF');
    
    if (!window.mortgageData) {
        alert('Por favor, calcula la hipoteca primero');
        return;
    }
    
    try {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF({
            orientation: 'portrait',
            unit: 'mm',
            format: 'a4'
        });
        
        // Añadir título
        doc.setFontSize(16);
        doc.text('Resumen del Préstamo', 105, 20, { align: 'center' });
        
        // Añadir información de la propiedad
        doc.setFontSize(12);
        doc.text(`Propiedad: ${window.mortgageData.propertyTitle}`, 20, 40);
        doc.text(`Precio: $${window.mortgageData.propertyPrice.toFixed(2)} MXN`, 20, 50);
        
        // Añadir tabla con detalles del préstamo
        const tableData = [
            ['Pago Mensual', `$${window.mortgageData.monthlyPayment.toFixed(2)} MXN`],
            ['Enganche', `$${window.mortgageData.downPayment.toFixed(2)} MXN`],
            ['Monto del Préstamo', `$${window.mortgageData.loanAmount.toFixed(2)} MXN`],
            ['Costo Total', `$${window.mortgageData.totalCost.toFixed(2)} MXN`]
        ];
        
        doc.autoTable({
            startY: 60,
            head: [['Concepto', 'Valor']],
            body: tableData,
            theme: 'grid',
            headStyles: { fillColor: [181, 169, 154], textColor: [255, 255, 255] },
            columnStyles: {
                0: { cellWidth: 100 },
                1: { cellWidth: 60, halign: 'right' }
            },
            margin: { left: 20, right: 20 }
        });
        
        // Añadir información adicional
        const finalY = doc.lastAutoTable.finalY + 10;
        doc.text(`Tasa de interés anual: ${window.mortgageData.interestRate}%`, 20, finalY);
        doc.text(`Plazo del préstamo: ${window.mortgageData.loanTerm} años`, 20, finalY + 10);
        
        // Añadir pie de página
        doc.setFontSize(8);
        doc.setTextColor(100, 100, 100);
        doc.text('Este documento es solo una estimación y no constituye una oferta de préstamo.', 105, 280, { align: 'center' });
        
        // Guardar PDF
        doc.save('resumen-prestamo.pdf');
        console.log('PDF generado correctamente');
    } catch (error) {
        console.error('Error al generar PDF:', error);
        alert('Error al generar el PDF: ' + error.message);
    }
}