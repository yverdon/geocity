const roResult = document.getElementById("map-ro-result");
const componentDiv = document.getElementById("web-component-advanced");
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

setupMap = (container, options, readonly) => {
  if (options && options.map_widget_configuration) {
    const wc = document.createElement("openlayers-element");
    wc.options = options.map_widget_configuration[0];
    const states = {
      readonly: readonly,
    };
    if (serialized.value) {
      const data = JSON.parse(serialized.value);
      const selections = [];
      data.geometries.forEach((geometry) => {
        selections.push(geometry.coordinates[0]);
      });
      states['currentSelections'] = selections;
    }
    wc.states = states;
    container.appendChild(wc);
  }
}

updateROMap = () => {
  if (roResult) {
    const states = {
      readonly: true,
    };
    if (serialized.value) {
      const data = JSON.parse(serialized.value);
      const selections = [];
      data.geometries.forEach((geometry) => {
        selections.push(geometry.coordinates[0]);
      });
      states['currentSelections'] = selections;
    }
    roResult.lastChild.states = states;
  }
}

createMap = () => {
  if (!mapIsCreated) {
      if (componentDiv) {
        setupMap(componentDiv, options, false)
        mapIsCreated = true;
      }
  }
};

toogleModal = (state) => {
  map.style.display = state;
  overlay.style.display = state;
  if (state == "block") document.body.style.overflow = "hidden";
  else document.body.style.overflow = "visible";
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
  if (selectedValues != "") toogleModal("none");
  {
    serialized.value = selectedValues;
    updateROMap();
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

const isInvalid = document
  .querySelectorAll("[data-geometry-widget]:not([data-initialize='0'])")[0]
  ?.parentNode?.parentNode?.classList.contains("is-invalid");
if (isInvalid) {
  document.getElementById("geo-invalid-content").style.display = "block";
}

setupMap(roResult, options, true);

if (options && !options.edit_geom) {
  buttonModal.style.display = 'none';
} else {
  buttonModal.style.display = 'flex';
}
