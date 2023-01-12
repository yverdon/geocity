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
      }
    }

}