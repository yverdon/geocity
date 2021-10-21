document.addEventListener('DOMContentLoaded', function() {

  const needsDateElement = document.getElementById('id_needs_date');
  const startDelayRow = document.getElementById('id_start_delay').closest('.form-row');
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
});
