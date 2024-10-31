// Prepare the form for adding student
function clearModal() {
    document.getElementById('student-full_name').value = ''; // Clear hidden ID field
    document.getElementById('student-id_number').value = ''; // Clear name field
    document.getElementById('student-gender').value = ''; // Clear hidden ID field
    document.getElementById('student-year_level').value = ''; // Clear name field
    document.getElementById('student-program_code').value = ''; // Clear hidden ID field

    document.getElementById('formModalLabel').innerText = 'Add New Student'; // Set title for adding
    document.getElementById('modal-submit-button').innerText = 'Add'; // Set button text for adding
}

document.querySelectorAll('.edit-item').forEach(button => {
    button.addEventListener('click', function () {
        const full_name = this.getAttribute('data-full_name');
        const id_number = this.getAttribute('data-id_number');
        const gender = this.getAttribute('data-gender');
        const year_level = this.getAttribute('data-year_level');
        const program_code = this.getAttribute('data-program_code');

        // Populate fields for editing
        document.getElementById('student-full_name').value = full_name;
        document.getElementById('student-id_number').value = id_number;
        document.getElementById('student-gender').value = gender;
        document.getElementById('student-year_level').value = year_level;
        document.getElementById('student-program_code').value = program_code;

        // Save the original id for editing
        document.getElementById('student-id').value = id_number;

        // Change title and button text for editing
        document.getElementById('formModalLabel').innerText = 'Edit Student';
        document.getElementById('modal-submit-button').innerText = 'Update';
    });
});