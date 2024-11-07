// Attach generatePDF to the button
document.querySelector('button[value="Generate List"]').onclick = () => {
    const data = JSON.parse(document.getElementById('data-json').textContent);
    generateList(data);
};

function generateList(data) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({
        orientation: 'p',
        unit: 'mm',
        format: 'a4',
        putOnlyUsedFonts: true
    });
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const header = document.getElementById("header_src").value;
    const footer = document.getElementById("footer_src").value;

    // Add header and footer images
    doc.addImage(header, 'PNG', (pageWidth - 184) / 2, 5, 184, 28);
    doc.addImage(footer, 'PNG', (pageWidth - 184) / 2, pageHeight - 20, 184, 20);

    doc.setFontSize(20);
    doc.setFont("times", "bold");
    const title = "Transactions";
    const titleWidth = doc.getTextWidth(title);
    doc.text(title, (pageWidth - titleWidth) / 2, 40); // Centered title

    let currentY = 60; // Starting Y position for content
    const lineHeight = 10; // Line height for the content
    const columnWidths = [25, 70, 30, 40, 30]; // Define column widths

    // Define headers and draw them
    const headers = ["ID", "Date and Time", "Student ID", "Payment Mode", "Status"];
    doc.setFontSize(14);
    doc.setFont("times", "bold");

    let startLine = 15; // Starting position for the first column
    headers.forEach((head, index) => {
        doc.text(head, startLine, currentY);
        startLine += columnWidths[index];
    });

    // Move down for content rows
    currentY += lineHeight;

    data['transactions'].forEach((transaction, index) => {
        // Check if the current Y position is too close to the bottom of the page
        if (currentY > pageHeight - 20) { // Adjust margin as needed
            doc.addPage(); // Create a new page if necessary
            doc.addImage(header, 'PNG', (pageWidth - 184) / 2, 5, 184, 28);
            doc.addImage(footer, 'PNG', (pageWidth - 184) / 2, pageHeight - 20, 184, 20);
            currentY = 40; // Reset Y position for new page

            // Redraw headers on new page
            startLine = 15;
            doc.setFontSize(14);
            doc.setFont("times", "bold");
            headers.forEach((head, index) => {
                doc.text(head, startLine, currentY);
                startLine += columnWidths[index];
            });
            currentY += lineHeight;
        }

        let rowData = [
            transaction[0],          // ID
            transaction[1],       // Date and Time (up to minutes)
            transaction[2],          // Student ID
            transaction[4],          // Payment Mode
            transaction[5]           // Status
        ];

        // Draw each cell in the row with fixed column widths
        startLine = 15;
        doc.setFontSize(12);
        doc.setFont("times", "normal");
        rowData.forEach((data, index) => {
            let cellData = String(data);
            doc.text(cellData, startLine, currentY);
            startLine += columnWidths[index];
        });

        // Move down for the next row
        currentY += lineHeight;
    });

    // Save the PDF
    doc.save('Transactions_List.pdf');
}