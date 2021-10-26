(function() {
  class PermitsGeoTime {
    constructor(node) {
      this.node = node;
      this.formsContainerNode = node.querySelector("[data-geo-time-role='forms']");
      this.emptyFormNode = node.querySelector("[data-geo-time-role='emptyForm']");
      this.addButtonNode = node.querySelector("[data-geo-time-role='addForm']");
      this.totalFormsInputNode = node.querySelector("[data-geo-time-role='managementForm'] input[name$='-TOTAL_FORMS']");
      this.permitDurationMax = this.formsContainerNode.dataset.permitDurationMax
      this.fixEndsAt()

      if (!this.emptyFormNode) {
        throw "No empty form node. Make sure there’s a node with `data-geo-time-role=\"emptyForm\"`.";
      }

      if (!this.addButtonNode) {
        throw "No add form node. Make sure there’s a node with `data-geo-time-role=\"addForm\"`.";
      }

      if (!this.totalFormsInputNode) {
        throw "No total forms input node. Make sure there’s a node with `data-geo-time-role=\"managementForm\"` which contains the management form.";
      }

      this._addEventListeners();

      // If you add some forms and then refresh the page, the browser restores
      // the inputs values but not the dynamic data (the added forms), which
      // means the TOTAL_FORMS input will be out of sync
      this._fixTotalForms();
    }

    addForm() {
      let newNode = this.emptyFormNode.children[0].cloneNode(true);
      let newNodeId = parseInt(this.totalFormsInputNode.value);
      newNode.innerHTML = newNode.innerHTML.replace(/__prefix__/g, newNodeId);
      let geometryWidgetNode = newNode.querySelector("[data-geometry-widget]");

      // Flag the widget to be initialized by the geometry widget manager
      if (geometryWidgetNode !== null) {
        geometryWidgetNode.dataset.initialize = "1";
      }
      // Set the correct form number to appear in the form title
      newNode.querySelector("[data-geo-time-role='formNumber']").textContent = newNodeId + 1;

      // Manually set bindings for the datepickers
      // See https://github.com/monim67/django-bootstrap-datepicker-plus/blob/22c4299019cb6328eed2938598e323c0d43c5e9a/bootstrap_datepicker_plus/static/bootstrap_datepicker_plus/js/datepicker-widget.js
      newNode.querySelectorAll("[dp_config]").forEach(function(node) {
        let $picker = jQuery(node).datetimepicker(JSON.parse(node.attributes.dp_config.value).options);

        $picker.next('.input-group-addon').on('click', function(){
          $picker.data("DateTimePicker").show();
        });
      });
      this._copyFormData(
        [...this.formsContainerNode.querySelectorAll("[data-geo-time-role='form']")].pop(),
        newNode,
        newNodeId
      );

      this.formsContainerNode.appendChild(newNode);

      this._getCollapses().forEach(node => {
        jQuery(node).collapse("hide");
      });

      let collapseNode = newNode.querySelector("[data-geo-time-role='form'].collapse");
      this._fixMapSizeOnCollapseOpen(collapseNode);
      jQuery(collapseNode).collapse("show");

      // Initialize `geometryWidget` on the newly created element
      if (window.geometryWidgetManager) {
        window.geometryWidgetManager.rebind();
      }

      this.totalFormsInputNode.value++;
    }

    fixEndsAt() {
      let allStarts = document.querySelectorAll("[id*='starts_at']")
      let allEnds = document.querySelectorAll("[id*='ends_at']")
      if (this.permitDurationMax !== "None"){
        allStarts.forEach((node) => {
          let $picker = jQuery(node).datetimepicker(JSON.parse(node.attributes.dp_config.value).options)
          $picker.on("dp.change", (e) => {
            let chosen_start_date = e.date
            let max_end_date = moment(chosen_start_date, "DD.MM.YYYY hh:mm").add(this.permitDurationMax, 'days')

            allEnds.forEach((node2)=> {
              let pickerAttributes = JSON.parse(node2.attributes.dp_config.value)

              pickerAttributes.options.minDate = chosen_start_date.format("YYYY/MM/DD")
              pickerAttributes.options.maxDate = max_end_date.format("YYYY/MM/DD")
              jQuery(node2).datetimepicker("destroy")

               let $picker2 = jQuery(node2).datetimepicker(pickerAttributes.options)
              $picker2.data("DateTimePicker").minDate(chosen_start_date);
              $picker2.data("DateTimePicker").maxDate(max_end_date);
            })
          })
        });

      }

    }

    _addEventListeners() {
      this.addButtonNode.addEventListener("click", this.addForm.bind(this));

      this._getCollapses().forEach(this._fixMapSizeOnCollapseOpen);
    }

    _getCollapses() {
      return [...this.formsContainerNode.querySelectorAll("[data-geo-time-role='form'].collapse")];
    }

    _fixMapSizeOnCollapseOpen(collapseNode) {
      jQuery(collapseNode).on("shown.bs.collapse", (e) => {
        // When sub-collapses are shown, this event seems to bubble up to the
        // parent collapse, in that case we can safely ignore it
        if (e.target.dataset.geoTimeRole !== "form") {
          return;
        }

        let geometryWidgetNode = collapseNode.querySelector("[data-geometry-widget]");
        let elementId;

        if (!geometryWidgetNode) {
          return;
        }

        elementId = geometryWidgetNode.attributes.id.value;

        if (elementId && window.geometryWidgetManager && elementId in window.geometryWidgetManager.boundNodes) {
          window.geometryWidgetManager.boundNodes[elementId].map.updateSize();
        }
      });
    }

    _fixTotalForms() {
      let nbForms = this.formsContainerNode.dataset.nbForms;

      if (nbForms !== undefined) {
        this.totalFormsInputNode.value = nbForms;
      }
    }

    _copyFormData(from, to, newFormId) {
      let fromInputs = [...from.querySelectorAll("input, textarea")];
      let fromMapping = {};

      for (let input of fromInputs) {
        // Skip invalid inputs
        if (!input.name) {
          continue;
        }

        // Formset inputs have names like `prefix-X-fieldName`
        let newName = input.name.replace(/-(\d+)-/, `-${newFormId}-`);
        let inputNode = to.querySelector("[name='" + newName + "']");

        if (inputNode) {
          inputNode.value = input.value;
        }
      }
    }
  }

  window.PermitsGeoTime = PermitsGeoTime;
})();
