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

// Create a label to replace .form-control without .extra-form in classes inside of forms-container
window.addEventListener('load', function () {
  var forms_control = document.querySelectorAll("[id=forms-container] select[class=form-control]");
  for (form_control of forms_control) {
    let elem = document.createElement('label');
    let text = form_control.querySelector("option[selected]").text
    let div = form_control.closest('.col-md-9');

    elem.innerHTML = text;
    elem.classList.add('col-form-label', 'bold');
    div.appendChild(elem);
  }

  // Hide .extra-form and show first hidden .extra-form on click of .show-extra-form
  var extra_forms = document.querySelectorAll("[id=forms-container] select.form-control.extra-form");
  for (extra_form of extra_forms) {
    let form = extra_form.closest("[class=contact-form]")
    form.setAttribute("hidden", true)
  }

  // addEventListener for button .show-extra-form
  var button = document.querySelector("button.show-extra-form");
  if (button != null) {
    button.addEventListener("click", (event) => {
      var hidden_extra_forms = document.querySelector(".contact-form[hidden]")
      if (hidden_extra_forms == null){
        document.getElementById('contact-alert').style.display = "block"
      }
      hidden_extra_forms.removeAttribute("hidden")
    });
  };
});
