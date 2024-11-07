async function printGraphs(paid_data, unpaid_data) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({
        orientation: 'p',
        unit: 'mm',
        format: 'a4',
        putOnlyUsedFonts: true
    });
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();

    // Add Header
    const header = document.getElementById("header_src").value;
    doc.addImage(header, 'PNG', (pageWidth - 184) / 2, 5, 184, 28);

    // Add Footers
    const footer = document.getElementById("footer_src").value;
    doc.addImage(footer, 'PNG', (pageWidth - 184) / 2, pageHeight - 20, 184, 20);

    doc.setFontSize(18);
    doc.setFont("times", "normal");
    const title = "Data Summary";
    const titleWidth = doc.getTextWidth(title);
    doc.text(title, (pageWidth - titleWidth) / 2, 40); // Centered title

    const program_code = document.getElementById('selected-program').value;
    const year = document.getElementById('selected-year').value;
    const month = document.getElementById('selected-month').value;

    doc.setFontSize(14);
    const dataDescription = `Program Code: ${program_code} | Month: ${month} | Year: ${year}`;
    const dataDescriptionWidth = doc.getTextWidth(dataDescription);
    doc.text(dataDescription, (pageWidth - dataDescriptionWidth) / 2, 50); // Centered Description
    
    const year_levels = ["1st Year", "2nd Year", "3rd Year", "4th Year"];
    const pdata = paid_data;
    const udata = unpaid_data;

    const graphs = document.getElementsByClassName("graph-report");
    const imgWidth = 170; // Width in mm
    let positionY = 55; // Starting position for the first image

    for (let i = 0; i < graphs.length; i++) {
        // Convert each canvas to data URL
        const imgData = await html2canvas(graphs[i]).then(canvas => canvas.toDataURL('image/png'));
        const imgHeight = (graphs[i].height * imgWidth) / graphs[i].width;

        // Add image to PDF
        doc.addImage(imgData, 'PNG', (pageWidth - imgWidth) / 2, positionY, imgWidth, imgHeight);
        
        // Update Y position for the next image
        positionY += imgHeight + 10;

        // Get paid and unpaid data for the current semester
        const pdataUse = i === 0 ? pdata.fcontribution.data : pdata.scontribution.data;
        const udataUse = i === 0 ? udata.fcontribution.data : udata.scontribution.data;

        let labelPosition = (pageWidth - imgWidth) / 2 + 10;
        for (let y = 0; y < year_levels.length; y++) {
            doc.setFontSize(8);
            doc.setTextColor(0, 0, 0);
            const label = year_levels[y] + ":";
            const labelWidth = doc.getTextWidth(label);
            doc.text(label, labelPosition, positionY);

            const paidData = pdataUse[y] + " Students";
            const pdataWidth = doc.getTextWidth(paidData);
            doc.setTextColor(0, 0, 255);
            doc.text(paidData, labelPosition + labelWidth + 5, positionY);

            const unpaidData = udataUse[y] + " Students";
            doc.setTextColor(255, 0, 0);
            doc.text(unpaidData, labelPosition + labelWidth + 5, positionY + 5);

            labelPosition += labelWidth + pdataWidth + 20;
        }

        positionY += 10; // Add extra space for labels
    }
    
    // Save PDF
    doc.save(`Data Summary Report (${program_code}).pdf`);
}

// For generating the student list
function printList(){
    const list_type = document.getElementById("list-type").value;
    const organization_code = document.getElementById("organization_code").value;
    const unpaidUrl = document.getElementById("unpaid_url").value;
    const csrfToken = document.getElementById("_token_csrf").value;
    
    const list = { 
        'organization-code': organization_code,
        'type': list_type
    };

    fetch(unpaidUrl, {
        headers: { 
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        method: "POST",
        body: JSON.stringify(list),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then(data => {
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

        doc.setFontSize(20);
        doc.setFont("times", "bold");
        const title = data['list-type'];
        const titleWidth = doc.getTextWidth(title);
        doc.text(title, (pageWidth - titleWidth) / 2, 40); // Centered title

        let currentY = 50; // Starting Y position for content
        const lineHeight = 10; // Line height for the content
        const startLine = 20;

        // Loop through each program and year level to add students
        // Get all valid program-year combinations with student data
        const validCombinations = [];
        data['programs'].forEach(program => {
            data['year_levels'].forEach(year => {
                const students = data[`${program}-${year}`];
                if (students && students.length > 0) {
                    validCombinations.push({ program, year, students });
                }
            });
        });

        // Iterate over each valid program-year level combination
        validCombinations.forEach(({ program, year, students }, index) => {
            // Add header and footer images
            doc.addImage(header, 'PNG', (pageWidth - 184) / 2, 5, 184, 28);
            doc.addImage(footer, 'PNG', (pageWidth - 184) / 2, pageHeight - 20, 184, 20);

            // Set header for program-year level
            doc.setFontSize(16);
            doc.setFont("times", "bold");
            doc.text(`${program[0]} - ${year}`, startLine, currentY);
            currentY += lineHeight; // Move down for the next line

            // Set font for student entries
            doc.setFontSize(13);
            doc.setFont("times", "normal");
            // Loop through students and add them to the PDF
            students.forEach(student => {
                const studentText = `${student[0]}: ${student[1]}`;
                doc.text(studentText, startLine, currentY);
                currentY += lineHeight;

                // Check if the current Y position is too close to the bottom of the page
                if (currentY > pageHeight - 20) { // Adjust margin as needed
                    doc.addPage(); // Create a new page if necessary
                    doc.addImage(header, 'PNG', (pageWidth - 184) / 2, 5, 184, 28);
                    doc.addImage(footer, 'PNG', (pageWidth - 184) / 2, pageHeight - 20, 184, 20);
                    currentY = 40; // Reset Y position for new page
                }
            });

            // Add a new page after each valid combination except for the last one
            if (index < validCombinations.length - 1) {
                doc.addPage();
                currentY = 40; // Reset Y position for new page
            }
        });
        doc.save(`${data['list-type']}.pdf`);
    })
    .catch(error => {
        console.error("There was a problem with the fetch operation:", error);
    });
}