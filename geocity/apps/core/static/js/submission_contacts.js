let update_form_value = function(item, userprofile) {

  if (document.getElementById(`self_contact_${parseInt(item) + 1}`).checked == true) {
    document.getElementById(`id_form-${item}-first_name`).value = userprofile.first_name;
    for (const [key, value] of Object.entries(userprofile)) {
      document.getElementById(`id_form-${item}-${key}`).value = value;
      document.getElementById(`id_form-${item}-${key}`).readOnly = true;
    }
  } else {
    for (const [key, value] of Object.entries(userprofile)) {
      document.getElementById(`id_form-${item}-${key}`).value = '';
      document.getElementById(`id_form-${item}-${key}`).readOnly = false;
    }
  }
}

// Create a label to replace "readonly hidden select" readonly
window.addEventListener('load', function () {
  var selects = document.querySelectorAll("select[readonly][hidden]");
  for (select of selects) {
    let elem = document.createElement('label');
    let text = select.querySelector("option[selected]").text
    let div = select.closest('.col-md-9');

    elem.innerHTML = text;
    elem.classList.add('col-form-label', 'bold');
    div.appendChild(elem);
  }
});
