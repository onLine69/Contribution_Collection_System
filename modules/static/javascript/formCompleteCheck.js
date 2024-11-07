function validateForm() {
    const programSelect = document.getElementById('programs');
    const yearSelect = document.getElementById('years');
    const monthSelect = document.getElementById('months');

    if (programSelect.value === "" || yearSelect.value === "" || monthSelect.value === "") {
        alert("Please select a value for all fields.");
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}