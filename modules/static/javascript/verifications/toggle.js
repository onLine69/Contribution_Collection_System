function toggleAll(source) {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="rowSelect"]');
    checkboxes.forEach((checkbox) => {
        if (!checkbox.disabled) {  // Only change the state of enabled checkboxes
            checkbox.checked = source.checked;
        }
    });
    
    // Uncheck all disabled checkboxes
    checkboxes.forEach((checkbox) => {
        if (checkbox.disabled) {
            checkbox.checked = false; // Uncheck disabled checkboxes
        }
    });
}

function updateSelectAll() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="rowSelect"]');
    const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked && !checkbox.disabled);
    document.getElementById('selectAll').checked = allChecked;
}

document.querySelector('.verify-button').addEventListener('click', function() {
    const checkboxes = document.querySelectorAll('input[name="rowSelect"]:checked');
    const transactionBody = document.getElementById('transaction-body');
    const amountInput = document.getElementById('item-total_amount');
    const contributionAmount = Number(document.getElementById('contribution-amount').value)
    // Clear existing rows
    transactionBody.innerHTML = '';
    let totalAmount = 0;

    checkboxes.forEach((checkbox) => {
        const row = checkbox.closest('tr');
        const transactionId = row.querySelector('td:nth-child(2)').textContent; // Get Transaction ID
        const studentId = row.querySelector('td:nth-child(4)').textContent; // Get Student ID
        const studentName = row.querySelector('td:nth-child(5)').textContent; // Get Student Name
        const note = row.querySelector('td:nth-child(7)').textContent; // Get Note from verification[5]

        // Create a new table row with inputs for the note
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${transactionId}</td>
            <td><input type="text" name="student_id" value="${studentId}" class="form-control" readonly/></td>
            <td><input type="text" name="student_name" value="${studentName}" class="form-control" readonly/></td>
            <td><input type="text" name="transaction_message" value="${note}" class="form-control" maxlength="255"/></td>
        `;
        transactionBody.appendChild(newRow);
        totalAmount++; // Increment total amount based on the number of transactions
    });

    // Update the amount field
    amountInput.value = totalAmount * contributionAmount;
});