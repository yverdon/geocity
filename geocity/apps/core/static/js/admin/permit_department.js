document.addEventListener('DOMContentLoaded', function() {

  function toggleDuoConfigurationField() {
    const hiddenClass = 'grp-row-hidden';
    const input = document.getElementById('id_permitdepartment-0-mandatory_2fa');
    const RowElement = document.getElementsByClassName('form-row duo_config');

    if (input.checked) {
      RowElement[0].classList.remove(hiddenClass);
    } else {
      RowElement[0].classList.add(hiddenClass);
    }
  };

  document.getElementById('id_permitdepartment-0-mandatory_2fa').addEventListener('change', function(e) {
    toggleDuoConfigurationField();
  });
});
