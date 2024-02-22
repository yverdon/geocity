
class Prolongation {
  constructor() {
    this.permitDuration = document.querySelector("#id_permit_duration");
    this.expirationReminder = document.querySelector("#id_expiration_reminder");
    this.daysBeforeReminder = document.querySelector("#id_days_before_reminder");
    this.daysBeforeReminderLabel = this.daysBeforeReminder.closest('.row').querySelector("label");
    this.requiredClass = 'required';

    this._init()
    this._addEventListeners();
  }

  _init() {
    if (!this.permitDuration.value) {
      this._toggleField("#id_expiration_reminder", true)
      this._toggleField("#id_days_before_reminder", true)
    }
    if (this.expirationReminder.checked) {
      this.daysBeforeReminder.setAttribute('required', '');
      this.daysBeforeReminderLabel.classList.add(this.requiredClass);
    }
  }

  _toggleField(selector, disabled) {
    const field = document.querySelector(selector);
    field.disabled = disabled;
  }

  _addEventListeners() {
    this.permitDuration.addEventListener("change", () => {
      if (!this.permitDuration.value) {
        this._toggleField("#id_expiration_reminder", true)
        this._toggleField("#id_days_before_reminder", true)
      } else {
        this._toggleField("#id_expiration_reminder", false)
        this._toggleField("#id_days_before_reminder", false)
      }
    });

    this.expirationReminder.addEventListener("change", () => {
      if (this.expirationReminder.checked) {
        this.daysBeforeReminder.setAttribute('required', '');
        this.daysBeforeReminderLabel.classList.add(this.requiredClass);
      } else {
        this.daysBeforeReminder.removeAttribute('required');
        this.daysBeforeReminderLabel.classList.remove(this.requiredClass);
        this.daysBeforeReminder.value = '';
      }

    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new Prolongation();

  const needsDateElement = document.getElementById('id_needs_date');
  const startDelayRow = document.getElementById('id_start_delay').closest('.row');
  const hiddenClass = 'grp-row-hidden';

  function toggleConditionalFields() {
    if (needsDateElement.checked) {
      startDelayRow.classList.remove(hiddenClass);
    } else {
      startDelayRow.classList.add(hiddenClass);
    }
  }

  document.getElementById('id_needs_date').addEventListener('change', function(e) {
    toggleConditionalFields();
  });
  toggleConditionalFields();

  const maxSubmissions = document.getElementById('id_max_submissions');
  const maxSubmissionsMessage = document.getElementById('id_max_submissions_message').closest('.form-group.field-max_submissions_message');

  function hideMaxSubmissions() {
    if (!maxSubmissions.value) {
      maxSubmissionsMessage.style.display = 'none';
    } else {
      maxSubmissionsMessage.style.display = 'block';
    }
  }

  maxSubmissions.addEventListener('input', hideMaxSubmissions);
  hideMaxSubmissions();

  const validationDocument = document.getElementById('id_validation_document');
  const validationDocumentRequiredFor = document.getElementById('id_validation_document_required_for').closest('.form-group.field-validation_document_required_for');

  function hideValidationDocument() {
    if (!validationDocument.checked) {
      validationDocumentRequiredFor.style.display = 'none';
    } else {
      validationDocumentRequiredFor.style.display = 'block';
    }
  }

  validationDocument.addEventListener('input', hideValidationDocument);
  hideValidationDocument();
});
