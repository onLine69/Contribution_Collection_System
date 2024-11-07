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

document.querySelector('.transact-button').addEventListener('click', function() {
    const checkboxes = document.querySelectorAll('input[name="rowSelect"]:checked');
    const transactionBody = document.getElementById('transaction-body');
    const amountInput = document.getElementById('item-amount');
    const contributionAmount = Number(document.getElementById('contribution-amount').value)

    // Clear existing rows
    transactionBody.innerHTML = '';
    let totalAmount = 0;

    checkboxes.forEach((checkbox) => {
        const row = checkbox.closest('tr');
        const studentId = row.querySelector('td:nth-child(3)').textContent; // Get Student ID
        const studentName = row.querySelector('td:nth-child(2)').textContent; // Get Student Name

        // Create a new table row with inputs for the note
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td><input type="text" name="student-id" value="${studentId}" class="form-control" readonly/></td>
            <td><input type="text" name="student_name" value="${studentName}" class="form-control" readonly/></td>
            <td><input type="text" name="transaction-message" value="None" class="form-control" maxlength="255"/></td>
        `;
        transactionBody.appendChild(newRow);
        totalAmount++; // Increment total amount based on the number of transactions
    });

    // Update the amount field
    amountInput.value = totalAmount * contributionAmount;
});