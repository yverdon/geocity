document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.getElementById('id_permit_department-0-uses_generic_email')
    function toggleConditionalFields() {
        const hiddenClass = 'd-none';
        const requiredClass =  'required';
        const checkbox_is_checked = checkbox.checked;
        const emailElement = document.getElementById('id_permit_department-0-generic_email');
        const emailRowElement = emailElement.closest('.form-group');
        const emailLabelElement = emailRowElement.querySelector('label');

        emailElement.removeAttribute('required');
        emailRowElement.classList.add(hiddenClass);
        emailLabelElement.classList.remove(requiredClass);

        if (checkbox_is_checked) {
            emailElement.setAttribute('required', '');
            emailRowElement.classList.remove(hiddenClass);
            emailLabelElement.classList.add(requiredClass);
        }
    };
    checkbox.addEventListener("click", toggleConditionalFields);
    toggleConditionalFields();
});
