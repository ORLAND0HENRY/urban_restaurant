// Global window object is needed for jsPDF UMD module
const { jsPDF } = window.jspdf;

document.getElementById('download-pdf-button').addEventListener('click', () => {
    const receiptContent = document.getElementById('receipt-content');

    // Use html2canvas to render the HTML as a canvas image
    html2canvas(receiptContent, {
        scale: 2, // Increase scale for better resolution
        logging: false
    }).then(canvas => {
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('p', 'mm', 'a4'); // Portrait, mm unit, A4 size
        const imgWidth = 210; // A4 width in mm
        const pageHeight = 297; // A4 height in mm
        const imgHeight = canvas.height * imgWidth / canvas.width;
        let heightLeft = imgHeight;
        let position = 0;

        // Add the image to the PDF
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;

        // Handle multiple pages if content is too long (for future proofing)
        while (heightLeft >= 0) {
            position = heightLeft - imgHeight;
            pdf.addPage();
            pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;
        }

        pdf.save(`urban_palate_receipt_${receiptContent.querySelector('.text-3xl').textContent.split('#')[1].trim()}.pdf`);
    });
});