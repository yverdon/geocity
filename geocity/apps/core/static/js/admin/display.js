document.addEventListener('DOMContentLoaded', () => {
  function updateFields() {
    const state = document.getElementById('id_geo_widget_option').value;
    if (state == 1) {
      document.getElementsByClassName('field-map_widget_configuration')[0].classList.add('hide')
      document.getElementsByClassName('field-geometry_types')[0].classList.remove('hide')
      document.getElementsByClassName('field-wms_layers')[0].classList.remove('hide')
      document.getElementsByClassName('field-wms_layers_order')[0].classList.remove('hide')
    }

    if (state == 2) {
      document.getElementsByClassName('field-map_widget_configuration')[0].classList.remove('hide')
      document.getElementsByClassName('field-geometry_types')[0].classList.add('hide')
      document.getElementsByClassName('field-wms_layers')[0].classList.add('hide')
      document.getElementsByClassName('field-wms_layers_order')[0].classList.add('hide')
    }
  }

  jQuery('#id_geo_widget_option').on("change", updateFields);
  updateFields();
})
