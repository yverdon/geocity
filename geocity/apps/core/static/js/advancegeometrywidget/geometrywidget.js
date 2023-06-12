const readOnlyMap = document.getElementById("map-ro-result");
readOnlyMap.style.display = 'none';
const editableMap = document.getElementById("web-component-advanced");
const serialized = document.querySelector("[data-role='serialized']");
const buttonModal = document.getElementById("map-custom-modal-button");
const crossButton = document.getElementById("modal-close-button");
const validationButton = document.getElementById("modal-validation-button");
const optionsDiv = document.querySelectorAll(
  "[data-geometry-widget]:not([data-initialize='0'])"
);
validationButton.style.opacity = 0.5;
const map = document.getElementById("map-custom-modal");
const overlay = document.getElementById("map-custom-modal-overlay");
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

setupReadOnlyMap = () => {
  readOnlyMap.style.display = 'block';
  setupMap(readOnlyMap, options, true);
}

parseCoordinates = (data) => {
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

setupMap = (container, options, readonly) => {
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

updateReadOnlyMap = () => {
  // update map only if exists. If there is no value when the form is set.
  // The read-only map is not instancitated but create when data is set.
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

createMap = () => {
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

toogleModal = (state) => {
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

closeModal = () => {
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

const isInvalid = document
  .querySelectorAll("[data-geometry-widget]:not([data-initialize='0'])")[0]
  ?.parentNode?.parentNode?.classList.contains("is-invalid");
if (isInvalid) {
  document.getElementById("geo-invalid-content").style.display = "block";
}

if (serialized.value) {
  setupReadOnlyMap();
  buttonModal.innerHTML = `<i class="fa fa-map"></i> Modifier sur la carte`
}

if (options && !options.edit_geom) {
  buttonModal.style.display = 'none';
} else {
  buttonModal.style.display = 'flex';
}
