document.addEventListener('DOMContentLoaded', function() {

  function toggleMandatoryValue() {
    const hiddenClass = 'd-none';
    const mandatoryElement = document.getElementById('id_is_mandatory');
    const mandatoryRowElement = mandatoryElement.closest('.form-group');
    const placeholderElement = document.getElementById('id_placeholder');
    const inputTypeElement = document.getElementById('id_input_type');
    const value = inputTypeElement.value;
    const disableMandatory = (value === 'title' || value === 'file_download');

    if (disableMandatory) {
      mandatoryElement.checked = false;
      mandatoryElement.disabled = true;
      mandatoryRowElement.classList.add(hiddenClass);
      placeholderElement.style.display = 'none';
    } else {
      mandatoryElement.disabled = false;
      placeholderElement.style.display = '';
      mandatoryRowElement.classList.remove(hiddenClass);
    }
  }

  function toggleConditionalFields() {
    const hiddenClass = 'd-none';
    const requiredClass =  'required';
    const inputType = document.getElementById('id_input_type').value;

    const choicesElement = document.getElementById('id_choices');
    const choicesRowElement = choicesElement.closest('.form-group');
    const choicesLabelElement = choicesRowElement.querySelector('label');
    const isChoicesVisible = inputType === 'list_single' || inputType === 'list_multiple';

    const regexElement = document.getElementById('id_regex_pattern');
    const regexRowElement = regexElement.closest('.form-group');
    const regexLabelElement = regexRowElement.querySelector('label');
    const isRegexPatternVisible = inputType === 'regex';

    const lineNumberForTextareaElement = document.getElementById('id_line_number_for_textarea');
    const lineNumberForTextareaRowElement = lineNumberForTextareaElement.closest('.form-group');
    const lineNumberForTextareaLabelElement = lineNumberForTextareaRowElement.querySelector('label');
    const isLineNumberForTextareaVisible = inputType === 'text';

    const additionalSearchtextForAddressFieldElement = document.getElementById('id_additional_searchtext_for_address_field');
    const additionalSearchtextForAddressFieldRowElement = additionalSearchtextForAddressFieldElement.closest('.form-group');
    const additionalSearchtextForAddressFieldVisible = inputType === 'address';

    const storeGeometryForAddressFieldElement = document.getElementById('id_store_geometry_for_address_field');
    const storeGeometryForAddressFieldRowElement = storeGeometryForAddressFieldElement.closest('.form-group');

    const servicesToNotifyElement = document.getElementById('id_services_to_notify');
    const servicesToNotifyRowElement = servicesToNotifyElement.closest('.form-group');
    const servicesToNotifyLabelElement = servicesToNotifyRowElement.querySelector('label');

    const isServicesToNotifyPatternVisible = inputType === 'checkbox';

    const fileElement = document.getElementById('id_file_download');
    const fileRowElement = fileElement.closest('.form-group');
    const fileLabelElement = fileRowElement.querySelector('label');

    const isFileVisible = inputType === 'file_download';

    choicesElement.removeAttribute('required');
    choicesRowElement.classList.add(hiddenClass);
    choicesLabelElement.classList.remove(requiredClass);

    regexElement.removeAttribute('required');
    regexRowElement.classList.add(hiddenClass);
    regexLabelElement.classList.remove(requiredClass);

    lineNumberForTextareaElement.removeAttribute('required');
    lineNumberForTextareaRowElement.classList.add(hiddenClass);
    lineNumberForTextareaLabelElement.classList.remove(requiredClass);

    additionalSearchtextForAddressFieldElement.removeAttribute('required');
    additionalSearchtextForAddressFieldRowElement.classList.add(hiddenClass);

    storeGeometryForAddressFieldElement.removeAttribute('required');
    storeGeometryForAddressFieldRowElement.classList.add(hiddenClass);

    servicesToNotifyElement.removeAttribute('required');
    servicesToNotifyRowElement.classList.add(hiddenClass);
    servicesToNotifyLabelElement.classList.remove(requiredClass);

    fileElement.removeAttribute('required');
    fileRowElement.classList.add(hiddenClass);
    fileLabelElement.classList.remove(requiredClass);

    if (isChoicesVisible) {
      choicesElement.setAttribute('required', '');
      choicesRowElement.classList.remove(hiddenClass);
      choicesLabelElement.classList.add(requiredClass);
    }
    else if (isRegexPatternVisible) {
      regexElement.setAttribute('required', '');
      regexRowElement.classList.remove(hiddenClass);
      regexLabelElement.classList.add(requiredClass);
    }
    else if (isLineNumberForTextareaVisible) {
      lineNumberForTextareaElement.setAttribute('required', '');
      lineNumberForTextareaRowElement.classList.remove(hiddenClass);
      lineNumberForTextareaLabelElement.classList.add(requiredClass);
    }
    else if (isServicesToNotifyPatternVisible) {
      servicesToNotifyElement.setAttribute('required', '');
      servicesToNotifyRowElement.classList.remove(hiddenClass);
      servicesToNotifyLabelElement.classList.add(requiredClass);
    }
    else if (isFileVisible) {
      fileElement.setAttribute('required', '');
      fileRowElement.classList.remove(hiddenClass);
      fileLabelElement.classList.add(requiredClass);
  }
    else if (additionalSearchtextForAddressFieldVisible) {
      additionalSearchtextForAddressFieldRowElement.classList.remove(hiddenClass);
      storeGeometryForAddressFieldRowElement.classList.remove(hiddenClass);
    }
  }

  function updateFields() {
    toggleConditionalFields();
    toggleMandatoryValue();
  }

  document.getElementById('id_input_type').addEventListener("onchange", updateFields);

  updateFields();
});
