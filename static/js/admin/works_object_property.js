document.addEventListener('DOMContentLoaded', function() {

  function toggleMandatoryValue() {
    const mandatoryElement = document.getElementById('id_is_mandatory');
    const placeholderElement = document.querySelector('div.placeholder');
    const inputTypeElement = document.getElementById('id_input_type');
    const value = inputTypeElement.value;
    const disableMandatory = value === 'title';

    if (disableMandatory) {
      mandatoryElement.checked = false;
      mandatoryElement.disabled = true;
      placeholderElement.style.display = 'none';
    } else {
      mandatoryElement.disabled = false;
      placeholderElement.disabled = true;
      placeholderElement.style.display = '';
    }
  }

  function toggleConditionalFields() {
    const hiddenClass = 'grp-row-hidden';
    const requiredClass =  'required';
    const inputType = document.getElementById('id_input_type').value;

    const choicesElement = document.getElementById('id_choices');
    const choicesRowElement = choicesElement.closest('.form-row.choices');
    const choicesLabelElement = choicesRowElement.querySelector('label');

    const isChoicesVisible = inputType === 'list_single' || inputType === 'list_multiple';

    const regexElement = document.getElementById('id_regex_pattern');
    const regexRowElement = regexElement.closest('.form-row.regex_pattern');
    const regexLabelElement = regexRowElement.querySelector('label');

    const isRegexPatternVisible = inputType === 'regex';

    const lineNumberForTextareaElement = document.getElementById('id_line_number_for_textarea');
    const lineNumberForTextareaRowElement = lineNumberForTextareaElement.closest('.form-row.line_number_for_textarea');
    const lineNumberForTextareaLabelElement = lineNumberForTextareaRowElement.querySelector('label');

    const isLineNumberForTextareaVisible = inputType === 'text';

    const servicesToNotifyElement = document.getElementById('id_services_to_notify');
    const servicesToNotifyRowElement = servicesToNotifyElement.closest('.form-row.services_to_notify');
    const servicesToNotifyLabelElement = servicesToNotifyRowElement.querySelector('label');
    
    const isServicesToNotifyPatternVisible = inputType === 'checkbox';

    choicesElement.removeAttribute('required');
    choicesRowElement.classList.add(hiddenClass);
    choicesLabelElement.classList.remove(requiredClass);

    regexElement.removeAttribute('required');
    regexRowElement.classList.add(hiddenClass);
    regexLabelElement.classList.remove(requiredClass);

    lineNumberForTextareaElement.removeAttribute('required');
    lineNumberForTextareaRowElement.classList.add(hiddenClass);
    lineNumberForTextareaLabelElement.classList.remove(requiredClass);

    servicesToNotifyElement.removeAttribute('required');
    servicesToNotifyRowElement.classList.add(hiddenClass);
    servicesToNotifyLabelElement.classList.remove(requiredClass);

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
  }

  document.getElementById('id_input_type').addEventListener('change', function(e) {
    toggleConditionalFields();
    toggleMandatoryValue();
  });

    toggleConditionalFields();
    toggleMandatoryValue();
  });
