document.addEventListener('DOMContentLoaded', () => {
  function updateFields() {
    const state = document.getElementById('id_geo_widget_option').value;
    if (state == 1) {
      document.getElementsByClassName('field-map_widget_configuration')[0].classList.add('display-none')
      document.getElementsByClassName('field-geometry_types')[0].classList.remove('display-none')
      document.getElementsByClassName('field-wms_layers')[0].classList.remove('display-none')
      document.getElementsByClassName('field-wms_layers_order')[0].classList.remove('display-none')
      document.getElementsByClassName('field-can_have_multiple_ranges')[0].classList.remove('display-none')
      document.getElementsByClassName('field-geo_step_help_text')[0].classList.remove('display-none')
    }

    if (state == 2) {
      document.getElementsByClassName('field-map_widget_configuration')[0].classList.remove('display-none')
      document.getElementsByClassName('field-geometry_types')[0].classList.add('display-none')
      document.getElementsByClassName('field-wms_layers')[0].classList.add('display-none')
      document.getElementsByClassName('field-wms_layers_order')[0].classList.add('display-none')
      document.getElementsByClassName('field-can_have_multiple_ranges')[0].classList.add('display-none')
      document.getElementsByClassName('field-geo_step_help_text')[0].classList.add('display-none')
    }
  }

  jQuery('#id_geo_widget_option').on("change", updateFields);
  updateFields();
})
