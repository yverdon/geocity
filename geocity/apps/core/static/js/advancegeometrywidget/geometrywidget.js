
function initMapWidget (fieldId) {
  "use strict";
  const readOnlyMap = document.getElementById(`map-ro-result-${fieldId}`);
  readOnlyMap.style.display = 'none';
  const editableMap = document.getElementById(`web-component-advanced-${fieldId}`);
  const serialized = document.querySelector(`[data-role='serialized-${fieldId}']`);
  const buttonModal = document.getElementById(`map-custom-modal-button-${fieldId}`);
  const crossButton = document.getElementById(`modal-close-button-${fieldId}`);
  const validationButton = document.getElementById(`modal-validation-button-${fieldId}`);
  const optionsDiv = document.querySelectorAll(
    `[data-geometry-widget-${fieldId}]:not([data-initialize='0'])`
  );
  const parentDjangoFieldDiv = document.getElementById(`div_${fieldId}`);
  const validationDiv = document.getElementById(`geo-invalid-content-${fieldId}`);
  validationButton.style.opacity = 0.5;
  const map = document.getElementById(`map-custom-modal-${fieldId}`);
  const overlay = document.getElementById(`map-custom-modal-overlay-${fieldId}`);
  let isModalOpen = false;
  let mapIsCreated = false;
  let selectedValues = "";
  let options = undefined;

  if (
    optionsDiv &&
    optionsDiv[0] &&
    optionsDiv[0].dataset &&
    optionsDiv[0].dataset.options
  ) {
    options = JSON.parse(optionsDiv[0].dataset.options);
  }

  let setupReadOnlyMap = () => {
    readOnlyMap.style.display = 'block';
    setupMap(readOnlyMap, options, true);
  }

  let parseCoordinates = (data) => {
    const selections = [];
    if (options.map_widget_configuration[0].outputFormat == 'GeometryCollection') {
      data.geometries.forEach((geometry) => {
        selections.push(geometry.coordinates[0]);
      });
    } else {
      data.features.forEach((feature) => {
        selections.push(feature.geometry.coordinates[0]);
      })
    }
    return selections;
  }

  let setupMap = (container, options, readonly) => {
    if (options && options.map_widget_configuration) {
      const wc = document.createElement("openlayers-element");
      wc.options = options.map_widget_configuration[0];
      const states = {
        readonly: readonly,
      };
      if (serialized.value) {
        const data = JSON.parse(serialized.value);
        const selections = parseCoordinates(data);
        states['currentSelections'] = selections;
      }
      wc.states = states;
      container.appendChild(wc);
      const modalHeight = window.innerHeight;
      container.style.setProperty('--window-modal-size', modalHeight + 'px');
    }
  }

  let updateReadOnlyMap = () => {
    // update map only if exists. If there is no value when the form is set.
    // The read-only map is not instanciated but created when data is set.
    if (readOnlyMap && readOnlyMap.lastChild && serialized.value) {
      const states = {
        readonly: true,
      };
      const data = JSON.parse(serialized.value);
      const selections = parseCoordinates(data);
      states['currentSelections'] = selections;
      readOnlyMap.lastChild.states = states;
    } else if (serialized.value) {
      setupReadOnlyMap();
    }

  }

  let createMap = () => {
    if (!mapIsCreated) {
        if (editableMap) {
          setupMap(editableMap, options, false)
          mapIsCreated = true;
        }
    } else if (editableMap.lastChild) {
      if (serialized.value) {
        const states = {
          readonly: false,
        };
        const data = JSON.parse(serialized.value);
        const selections = parseCoordinates(data);
        states['currentSelections'] = selections;
        editableMap.lastChild.states = states;
      }
    }
  };

  let toogleModal = (state) => {

    map.style.display = state;
    overlay.style.display = state;
    if (state == "block") document.body.style.overflow = "hidden";
    else {
      document.body.style.overflow = "visible"
      editableMap.lastChild.states = {
        readonly: true,
        currentSelections: []
      }
    };
  };
  buttonModal.addEventListener("click", () => {
    if (isModalOpen) {
      toogleModal("none");
    } else {
      toogleModal("block");
      createMap();
    }
  });

  let closeModal = () => {
    toogleModal("none");
  };

  crossButton.addEventListener("click", () => {
    closeModal();
  });

  overlay.addEventListener("click", () => {
    closeModal();
  });

  validationButton.addEventListener("click", () => {
    if (selectedValues != "")
    {
      serialized.value = selectedValues;
      buttonModal.innerHTML = `<i class="fa fa-map"></i> Modifier sur la carte`
      toogleModal("none");
      updateReadOnlyMap();
      validationDiv.style.display = "none";
    }
  });

  window.addEventListener("position-selected", (event) => {
    if (event.detail) {
      validationButton.style.opacity = 1;
      selectedValues = event.detail;
    } else {
      validationButton.style.opacity = 0.5;
      selectedValues = "";
    }
  });

  window.addEventListener('resize', () => {
    const modalHeight = window.innerHeight;
    editableMap.style.setProperty('--window-modal-size', modalHeight + 'px');
  })

  // Ensure field has a value and is required
  let updateValidationMessage = () => {
    const geomFieldValue = document.getElementById(fieldId).value;
    if (parentDjangoFieldDiv) {
    // Widget is used on detail step
      if (geomFieldValue == '' && parentDjangoFieldDiv && parentDjangoFieldDiv.classList.contains("required")) {
        validationDiv.style.display = "block";
        }
    } else {
    // Widget is used on geotime step
      if (geomFieldValue == '') {
        validationDiv.style.display = "block";
      }
    }
  }
  updateValidationMessage();

  if (serialized.value) {
    setupReadOnlyMap();
    buttonModal.innerHTML = `<i class="fa fa-map"></i> Modifier sur la carte`
  }

  if (options && !options.edit_geom) {
    buttonModal.style.display = 'none';
  } else {
    buttonModal.style.display = 'flex';
  }

};
