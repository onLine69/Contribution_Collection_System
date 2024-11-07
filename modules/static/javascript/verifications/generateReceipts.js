document.addEventListener('DOMContentLoaded', () => {
    async function generatePDF(data) {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF({
            orientation: 'p',
            unit: 'mm',
            format: 'a4',
            putOnlyUsedFonts: true
        });

        // Add title
        doc.setFontSize(32);
        const title = "Transaction Record";
        const pageWidth = doc.internal.pageSize.getWidth();
        doc.text(title, (pageWidth - doc.getTextWidth(title)) / 2, 20); // Centered title

        // Add details section
        doc.setFontSize(12);
        doc.text("Details:", 10, 35);
        
        const userDetails = [
            `Contribution Name: ${data.contribution_name}`,
            `Block Representative: ${data.block_rep}`,
            `Verification Date: ${data.verification_date}`,
            `Program Code: ${data.program_code}`,
            `Year Level: ${data.year_level}`,
            `Total Amount (in PhP): ${data.total_amount}`
        ];

        userDetails.forEach((detail, index) => {
            doc.text(detail, 15, 45 + (index * 6)); // Adjust position for each detail
        });

        // Add Receipts title
        doc.setFontSize(16);
        doc.text("Receipts", (pageWidth - doc.getTextWidth("Receipts")) / 2, 80);

        // Generate images for each card element
        const cards = document.getElementsByClassName("card");
        const imgWidth = 80; // Image width in PDF
        let positionY = 90; // Starting Y position for the first row
        let positionX = 20; // Starting X position for each image

        for (let i = 0; i < cards.length; i++) {
            // Capture the current card as a canvas
            const canvas = await html2canvas(cards[i], { scale: 2 });
            const imgData = canvas.toDataURL("image/png");
            const imgHeight = (canvas.height * imgWidth) / canvas.width;

            // Check if the image fits on the current page
            const pageHeight = doc.internal.pageSize.getHeight();
            if (positionY + imgHeight > pageHeight) {
                doc.addPage(); // Add new page if image doesn't fit
                positionY = 10;
                positionX = 20;
            }

            // Add the image to PDF
            doc.addImage(imgData, 'PNG', positionX, positionY, imgWidth, imgHeight);
            positionX += imgWidth + 10; // Move X position for the next image in row

            // Arrange in two columns, reset X and increment Y for the next row
            if ((i + 1) % 2 === 0) {
                positionY += imgHeight + 10;
                positionX = 20;
            }
        }

        // Save PDF
        doc.save(`${data.program_code}_${data.year_level}_${data.verification_date}.pdf`);
    }

    // Attach generatePDF to the button
    document.querySelector('input[value="Create PDF"]').onclick = () => {
        const data = JSON.parse(document.getElementById('data-json').textContent);
        generatePDF(data);
    };
});
