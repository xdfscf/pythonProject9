function toggleForm(formId) {
    var forms = document.querySelectorAll('form');
    forms.forEach(function (form) {
        form.style.display = 'none';
    });

    var selectedForm = document.getElementById(formId);
    selectedForm.style.display = 'flex';
}