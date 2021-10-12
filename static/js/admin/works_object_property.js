document.addEventListener('DOMContentLoaded', function() {

  function toggleMandatoryValue() {
    const mandatoryElement = document.getElementById('id_is_mandatory');
    const inputTypeElement = document.getElementById('id_input_type');
    const value = inputTypeElement.value;
    const disableMandatory = value === 'title';

    if (disableMandatory) {
      mandatoryElement.checked = false;
      mandatoryElement.disabled = true;
    } else {
      mandatoryElement.disabled = false;
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

    choicesElement.removeAttribute('required');
    choicesRowElement.classList.add(hiddenClass);
    choicesLabelElement.classList.remove(requiredClass);

    regexElement.removeAttribute('required');
    regexRowElement.classList.add(hiddenClass);
    regexLabelElement.classList.remove(requiredClass);

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
  }

  document.getElementById('id_input_type').addEventListener('change', function(e) {
    toggleConditionalFields();
    toggleMandatoryValue();
  });

    toggleConditionalFields();
    toggleMandatoryValue();
  });
