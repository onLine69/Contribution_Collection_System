document.getElementById('file-upload').addEventListener('change', function() {
    // Check if there is a file
    if (this.files.length > 0) {
        document.getElementById('upload-form').submit();
    }
});