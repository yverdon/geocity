/* global ol */

/*Adapted from geodjango map widget*/

(function () {
  "use strict";

  var geojsonFormat = new ol.format.GeoJSON();

  function geometryWidget(el) {
    let options = JSON.parse(el.dataset.options);
    this.el = el;
    this.serializedEl = el.querySelector("[data-role='serialized']");
    this.map = null;
    this.wmtsLayer = new ol.layer.Tile({});
    this.wmtsLayerAlternative = new ol.layer.Tile({});
    this.interactions = { draw: null, modify: null };
    this.ready = false;
    this.options = {};

    // Altering using user-provided options
    for (var property in options) {
      if (options.hasOwnProperty(property)) {
        this.options[property] = options[property];
      }
    }
    /*
        Drawing restriction area definition
        */
    let restrictionStyle = new ol.style.Style({
      fill: new ol.style.Fill({
        color: "#ffffff00",
      }),
      stroke: new ol.style.Stroke({
        color: "#fc4c9e88",
        width: 1,
      }),
    });

    var layer_list = [];

    this.options.wms_layers.forEach(function (item, index) {
      layer_list.push(
        new ol.layer.Image({
          source: new ol.source.ImageWMS({
            url: item,
            projection: "EPSG:2056",
          }),
          opacity: 1,
        })
      );
    });

    this.wmsLayerGroup = new ol.layer.Group({
      layers: layer_list,
    });

    this.rasterMaskLayer = new ol.layer.Image({
      source: new ol.source.ImageWMS({
        url: this.options.qgisserver_proxy,
        params: {
          LAYERS: "permits_permitadministrativeentity",
          FILTER:
            'permits_permitadministrativeentity:"id" = ' +
            this.options.administrative_entity_id,
        },
        projection: "EPSG:2056",
      }),
      style: restrictionStyle,
      opacity: 0.9,
    });

    this.vectorMaskLayer = new ol.layer.Vector({
      source: new ol.source.Vector({
        url: (e) => {
          return this.options.administrative_entity_url;
        },
        zIndex: 9999,
        format: new ol.format.GeoJSON(),
      }),
      zIndex: 9999,
      style: restrictionStyle,
      opacity: 0.9,
    });

    this.map = this.createMap(
      this.rasterMaskLayer,
      this.vectorMaskLayer,
      this.options.restriction_area_enabled
    );

    this.addBaseLayer();
    this.setupAlternativeBaseLayer();
    this.vectorSource = new ol.source.Vector();

    this.vectorSource.on("addfeature", (e) => {
      this.serializeFeatures();
    });

    this.vectorSource.on("removefeature", (e) => {
      this.serializeFeatures();
    });

    this.vectorSource.on("changefeature", (e) => {
      this.serializeFeatures();
    });

    this.featureOverlay = new ol.layer.Vector({
      name: "featureOverlay",
      style: this.setDrawingStyle(),
      map: this.map,
      source: this.vectorSource,
      updateWhileAnimating: true, // optional, for instant visual feedback
      updateWhileInteracting: true, // optional, for instant visual feedback
    });
    var initial_value = this.serializedEl.value;
    var extent = ol.extent.createEmpty();
    if (this.options.geometry_db_type != "GeometryCollection") {
      $("[data-action='editPoints']", this.el).hide();
      $("[data-action='editLines']", this.el).hide();
      $("[data-action='editPolygons']", this.el).hide();

      if (this.options.geometry_db_type == "MultiPolygon") {
        $("[data-action='setPointManual']", this.el).hide();
        $("[data-action='manualCoordinates']", this.el).hide();
      } else if (this.options.geometry_db_type == "MultiLineString") {
        $("[data-action='setPointManual']", this.el).hide();
        $("[dataction='manualCoordinates']", this.el).hide();
      }
    }
    if (initial_value) {
      var data = JSON.parse(initial_value);
      // If not collection, hide buttons for unsupported geometry types
      if (this.options.geometry_db_type != "GeometryCollection") {
        if (this.options.geometry_db_type == "MultiPoint") {
          var olFeature = new ol.Feature({
            geometry: new ol.geom.MultiPoint(data.coordinates),
          });
        } else if (this.options.geometry_db_type == "MultiLineString") {
          var olFeature = new ol.Feature({
            geometry: new ol.geom.MultiLineString(data.coordinates),
          });
        } else if (this.options.geometry_db_type == "MultiPolygon") {
          var olFeature = new ol.Feature({
            geometry: new ol.geom.MultiPolygon(data.coordinates),
          });
        }

        extent = olFeature.getGeometry().getExtent();

        this.featureOverlay.getSource().addFeature(olFeature);
      } else {
        // GeometryCollection
        var features = data.geometries;

        for (var i = 0; i < features.length; i++) {
          var f = features[i];
          if (f.type == "MultiPoint") {
            var olFeature = new ol.Feature({
              geometry: new ol.geom.MultiPoint(f.coordinates),
            });
          } else if (f.type == "MultiLineString") {
            var olFeature = new ol.Feature({
              geometry: new ol.geom.MultiLineString(f.coordinates),
            });
          } else if (f.type == "MultiPolygon") {
            var olFeature = new ol.Feature({
              geometry: new ol.geom.MultiPolygon(f.coordinates),
            });
          }

          this.featureOverlay.getSource().addFeature(olFeature);
          //update extent
          ol.extent.extend(extent, olFeature.getGeometry().getExtent());
        }
      }
      // zoom to extent of initial geometry that we got from db
      this.map
        .getView()
        .fit(extent, { padding: [100, 100, 100, 100], minResolution: 1 });
    } else {
      this.map.getView().setCenter(this.options.default_center);
      this.map.getView().setZoom(this.options.default_zoom);
      this.vectorMaskLayer.on("change", (e) => {
        var extent = this.vectorMaskLayer.getSource().getExtent();
        this.map
          .getView()
          .fit(extent, { padding: [100, 100, 100, 100], minResolution: 1 });
      });
    }

    this.createInteractions();

    // disable edit (for use in read-only views)
    if (!this.options.edit_geom) {
      this.disableDrawing();
      this.interactions.modify.setActive(false);
      this.hideMapButtons();
    }

    this.clearWarning();

    this._addEventListeners();
    this.ready = true;
  }

  // Add new swiss CRS to proj4js
  proj4.defs(
    "EPSG:2056",
    "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs"
  );
  ol.proj.proj4.register(proj4);

  var projection = new ol.proj.Projection({
    code: "EPSG:2056",
    extent: [2485071.58, 1075346.31, 2828515.82, 1299941.79],
    units: "m",
  });

  ol.proj.addProjection(projection);

  /*
    Create ol.Map instance
    */
  geometryWidget.prototype.createMap = function (
    rasterMaskLayer,
    vectorMaskLayer,
    restriction_area_enabled
  ) {
    var map = new ol.Map({
      controls: [
        new ol.control.ScaleLine(),
        new ol.control.Zoom(),
        new ol.control.Rotate({
          autoHide: false,
        }),
        new ol.control.MousePosition({
          coordinateFormat: function (coordinate) {
            return ol.coordinate.format(coordinate, "Est: {x}, Nord: {y}", 0);
          },
        }),
      ],
      target: this.el.querySelector("[data-role=map]"),
      view: new ol.View({
        zoom: this.options.default_zoom,
        minZoom: this.options.min_zoom,
        projection: projection,
        center: this.options.default_center,
      }),
    });
    if (restriction_area_enabled) {
      map.addLayer(vectorMaskLayer);
      map.addLayer(rasterMaskLayer);
    }

    map.addLayer(this.wmsLayerGroup);

    return map;
  };

  /*
    Add default WMTS base layer
    */
  geometryWidget.prototype.addBaseLayer = function () {
    var wmtsLayerName = this.options.wmts_layer;

    $.ajax({
      url: this.options.wmts_capabilities_url,
      success: (response) => {
        var parser = new ol.format.WMTSCapabilities();
        var result = parser.read(response);
        var options = ol.source.WMTS.optionsFromCapabilities(result, {
          layer: wmtsLayerName,
          matrixSet: "EPSG:2056",
          projection: "EPSG:2056",
        });
        this.wmtsLayer.setSource(
          new ol.source.WMTS(/** @type {!olx.source.WMTSOptions} */ (options))
        );
      },
    });

    this.map.getLayers().insertAt(0, this.wmtsLayer);
    this.wmtsLayer.setVisible(true);
  };

  /*
    Add alternative WMTS base layer
    */
  geometryWidget.prototype.setupAlternativeBaseLayer = function () {
    var wmtsLayerName = this.options.wmts_layer_alternative;

    $.ajax({
      url: this.options.wmts_capabilities_url_alternative,
      success: (response) => {
        var parser = new ol.format.WMTSCapabilities();
        var result = parser.read(response);
        var options = ol.source.WMTS.optionsFromCapabilities(result, {
          layer: wmtsLayerName,
          matrixSet: "EPSG:2056",
          projection: "EPSG:2056",
        });
        this.wmtsLayerAlternative.setSource(
          new ol.source.WMTS(/** @type {!olx.source.WMTSOptions} */ (options))
        );
      },
    });

    this.map.getLayers().insertAt(0, this.wmtsLayerAlternative);
    this.wmtsLayerAlternative.setVisible(false);
  };

  /*
    Function to load KML data
  */
  geometryWidget.prototype.addKML = function () {
    const filePicker = this.el.querySelector("[data-action='addKML']");
    if (!filePicker) {
      return;
    }
    const file = filePicker.files[0];

    if (file) {
      var reader = new FileReader();
      reader.onloadend = () => {
        var kml = new ol.format.KML();
        var features = kml.readFeatures(reader.result);

        if (features.length > 50) {
          this.showWarning("Votre fichier dépasse la limite de 50 entités, il n'a pas été importé!");
        } else {
          for (var i = 0; i < features.length; i++) {
            var coord = features[i].getGeometry().getCoordinates();
            features[i].getGeometry().setCoordinates(coord, "XY");
            features[i].getGeometry().transform("EPSG:4326", "EPSG:2056");

            var geomType = features[i].getGeometry().getType();
            if (geomType == "Polygon") {
              var multiPolygon = new ol.geom.MultiPolygon([
                features[i].getGeometry().getCoordinates(),
              ]);
              features[i].setGeometry(multiPolygon);
            } else if (geomType == "LineString") {
              var MultiLineString = new ol.geom.MultiLineString([
                features[i].getGeometry().getCoordinates(),
              ]);
              features[i].setGeometry(MultiLineString);
            } else if (geomType == "Point") {
              var multiPoint = new ol.geom.MultiPoint([
                features[i].getGeometry().getCoordinates(),
              ]);
              features[i].setGeometry(multiPoint);
            }
            this.vectorSource.addFeature(features[i]);
          }
        }
      };
      reader.readAsText(file);
    }
  };

  /*
    Base layer switcher
    */
  geometryWidget.prototype.switchBaseLayers = function () {
    if (this.wmtsLayer.getVisible()) {
      this.wmtsLayerAlternative.setVisible(true);
      this.wmtsLayer.setVisible(false);
    } else {
      this.wmtsLayerAlternative.setVisible(false);
      this.wmtsLayer.setVisible(true);
    }
  };

  /*
    Dynamic OL style for drawing
    */
  geometryWidget.prototype.setDrawingStyle = function () {
    var imagePoint = new ol.style.Circle({
      radius: 5,
      stroke: new ol.style.Stroke({
        color: "rgba(0, 24, 110, 0.9)",
        width: 2,
      }),
      fill: new ol.style.Fill({
        color: "rgba(0, 48, 220, 0.6)",
      }),
    });
    var imageVertex = new ol.style.Circle({
      radius: 3,
      stroke: new ol.style.Stroke({
        color: "rgba(255, 24, 0, 0.8)",
        width: 2,
      }),
      fill: new ol.style.Fill({
        color: "rgba(255, 24, 0, 0.2)",
      }),
    });
    return [
      new ol.style.Style({
        image: imageVertex,
        geometry: function (feature) {
          const allowedGeometriesTypes = [
            "LineString",
            "MultiLineString",
            "Polygon",
            "MultiPolygon",
          ];
          var geomType = feature.getGeometry().getType();
          if (allowedGeometriesTypes.includes(geomType)) {
            var geomCoords = feature.getGeometry().getCoordinates();
            if (geomType == "MultiLineString") {
              var coordinates = geomCoords[0];
            } else if (geomType == "MultiPolygon") {
              var coordinates = geomCoords[0][0];
            }
          } else {
            return;
          }
          return new ol.geom.MultiPoint(coordinates);
        },
      }),
      new ol.style.Style({
        image: imagePoint,
        stroke: new ol.style.Stroke({
          color: "rgba(0, 64, 255, 0.9)",
          width: 3,
        }),
        fill: new ol.style.Fill({
          color: "rgba(0, 64, 255, 0.2)",
        }),
      }),
    ];
  };

  /*
    Dynamic OL style for selected features
    */
  geometryWidget.prototype.setSelectionStyle = function () {
    var imagePoint = new ol.style.Circle({
      radius: 5,
      stroke: new ol.style.Stroke({
        color: "rgba(255, 244, 0, 0.8)",
        width: 2,
      }),
      fill: new ol.style.Fill({
        color: "rgba(255, 244, 0, 0.2)",
      }),
    });
    var imageVertex = new ol.style.Circle({
      radius: 3,
      stroke: new ol.style.Stroke({
        color: "rgba(255, 128, 0, 0.8)",
        width: 2,
      }),
      fill: new ol.style.Fill({
        color: "rgba(255, 128, 0, 0.2)",
      }),
    });
    return [
      new ol.style.Style({
        image: imageVertex,
        geometry: function (feature) {
          const allowedGeometriesTypes = [
            "LineString",
            "MultiLineString",
            "Polygon",
            "MultiPolygon",
          ];
          var geomType = feature.getGeometry().getType();
          if (allowedGeometriesTypes.includes(geomType)) {
            var geomCoords = feature.getGeometry().getCoordinates();
            if (geomType == "MultiLineString") {
              var coordinates = geomCoords[0];
            } else if (geomType == "MultiPolygon") {
              var coordinates = geomCoords[0][0];
            }
          } else {
            return;
          }
          return new ol.geom.MultiPoint(coordinates);
        },
      }),
      new ol.style.Style({
        image: imagePoint,
        stroke: new ol.style.Stroke({
          color: "rgba(255, 244, 0, 0.8)",
          width: 3,
        }),
        fill: new ol.style.Fill({
          color: "rgba(255, 244, 0, 0.2)",
        }),
      }),
    ];
  };

  /*
    Create OL interactions
    */
  geometryWidget.prototype.createInteractions = function () {
    $("#delete-selected").addClass("disabled");

    // Initialize the modify interaction
    this.interactions.modify = new ol.interaction.Modify({
      source: this.vectorSource,
      style: new ol.style.Style({}),
    });

    // Initialize the select interaction
    this.interactions.select = new ol.interaction.Select({
      layers: [this.featureOverlay],
      style: this.setSelectionStyle(),
    });

    this.interactions.select.on("select", function (e) {
      if (e.selected.length > 0) {
        $("#delete-selected").removeClass("disabled");
      } else {
        $("#delete-selected").addClass("disabled");
      }
    });

    this.map.addInteraction(this.interactions.modify);
    this.map.addInteraction(this.interactions.select);
    if (this.options.geometry_db_type == "GeometryCollection") {
      this.setDrawInteraction("MultiPoint");
    } else {
      this.setDrawInteraction(this.options.geometry_db_type);
    }
    this.map.on("pointermove", function (evt) {
      var hit = evt.map.hasFeatureAtPixel(evt.pixel, {
        layerFilter: function (layer) {
          if (layer.get("name") === "featureOverlay") {
            return true;
          } else {
            return false;
          }
        },
      });

      this.getTargetElement().style.cursor = hit ? "pointer" : "";
    });
  };

  /*
    Draw interactions setting for Points, Lines & Polygons
    */
  geometryWidget.prototype.setDrawInteraction = function (geotype) {
    if (this.interactions.draw) {
      this.map.removeInteraction(this.interactions.draw);
    }

    this.interactions.draw = new ol.interaction.Draw({
      source: this.vectorSource,
      type: geotype,
      condition: (e) => {
        if (this.options.restriction_area_enabled) {
          this.clearWarning();
          let coords = e.coordinate;
          let features = this.map.getFeaturesAtPixel(e.pixel, {
            layerFilter: (layer) => {
              return layer === this.vectorMaskLayer;
            },
          });
          if (features && features.length > 0) {
            return true;
          } else {
            this.showWarning("Votre saisie sort du territoire du territoire concerné");
            return false;
          }
        } else {
          return true;
        }
      },
    });

    this.map.addInteraction(this.interactions.draw);
  };

  /*
    Enable drawing & modify interactions
    */
  geometryWidget.prototype.enableDrawing = function () {
    this.interactions.draw.setActive(true);
    this.interactions.modify.setActive(false);
    this.interactions.select.setActive(false);
  };

  /*
    Disable drawing & modify interactions
    */
  geometryWidget.prototype.disableDrawing = function () {
    if (this.interactions.draw) {
      this.interactions.draw.setActive(false);
    }
  };

  /*
    hide map buttons for readonly views
    */
  geometryWidget.prototype.hideMapButtons = function () {
    $("#delete-selected").addClass("disabled");
  };

  geometryWidget.prototype.clearWarning = function() {
    $("[data-role='outOfAdministrativeLimits']", this.el).hide();
  };

  geometryWidget.prototype.showWarning = function(text) {
    const $node = $("[data-role='outOfAdministrativeLimits']", this.el);
    $node.text(text);
    $node.show();
  };

  /*
    Enable feature selection and disable other interactions
    */
  geometryWidget.prototype.selectFeatures = function () {
    this.disableDrawing();
    this.interactions.modify.setActive(true);
    this.interactions.select.setActive(true);
  };

  /*
    Remove features selected on the map
    */
  geometryWidget.prototype.removeSelectedFeatures = function () {
    var selectedFeatures = this.interactions.select.getFeatures().getArray();

    for (var i = 0; i < selectedFeatures.length; i++) {
      this.vectorSource.removeFeature(selectedFeatures[i]);
    }
    this.interactions.select.getFeatures().clear();
    $("#delete-selected").addClass("disabled");
  };

  /*
    Add point from manuelly edited coordinates (ch1903+)
    */
  geometryWidget.prototype.addPointFeature = function () {
    var east = parseFloat(this.el.querySelector("[name='east_coord']").value);
    var north = parseFloat(this.el.querySelector("[name='north_coord']")[0].value);
    var feature = new ol.Feature({
      geometry: new ol.geom.MultiPoint([[east, north]]),
    });

    this.vectorSource.addFeature(feature);
    this.interactions.select.getFeatures().clear();

    this.map.getView().fit(this.vectorSource.getExtent(), {
      padding: [100, 100, 100, 100],
      minResolution: 1,
    });
  };

  /*
    Serialize geometries into geojson collections
  */
  geometryWidget.prototype.serializeFeatures = function () {
    var features = this.vectorSource.getFeatures();
    if (features.length == 0) {
      this.serializedEl.value = "";
      return;
    }
    var geometries = [];
    for (var i = 0; i < features.length; i++) {
      if (this.options.geometry_db_type == "GeometryCollection") {
        geometries.push(features[i].getGeometry());
      } else {
        geometries.push(features[i].getGeometry().getCoordinates()[0]);
      }
    }
    if (this.options.geometry_db_type == "GeometryCollection") {
      var geometry = new ol.geom.GeometryCollection(geometries);
    } else if (this.options.geometry_db_type == "MultiPolygon") {
      var geometry = new ol.geom.MultiPolygon(geometries);
    } else if (this.options.geometry_db_type == "MultiLineString") {
      var geometry = new ol.geom.MultiLineString(geometries);
    } else if (this.options.geometry_db_type == "MultiPoint") {
      var geometry = new ol.geom.MultiPoint(geometries);
    }

    var geojsongeom = geojsonFormat.writeGeometry(geometry, {
      decimals: 2,
    });
    this.serializedEl.value = geojsongeom;
  };

  geometryWidget.prototype._addEventListeners = function () {
    const widget = this;
    const clickActions = {
      enableDrawing: e => this.enableDrawing(),
      selectFeatures: e => this.selectFeatures(),
      removeSelectedFeatures: e => this.removeSelectedFeatures(),
      setDrawInteraction: e => this.setDrawInteraction(e.originalTarget.dataset.interactionType),
      switchBaseLayers: e => this.switchBaseLayers(),
    };

    for (let clickAction in clickActions) {
      [...this.el.querySelectorAll(`[data-action='${clickAction}']`)].forEach(node => {
        node.addEventListener("click", clickActions[clickAction]);
      });
    }


    [...this.el.querySelectorAll("[data-action='addKML']")].forEach(node => {
      node.addEventListener("change", () => widget.addKML());
    });
  };

  function geometryWidgetManager() {
    this.boundNodes = {};
  }

  geometryWidgetManager.prototype.rebind = function() {
    [...document.querySelectorAll("[data-geometry-widget]:not([data-initialize='0'])")].forEach(node => {
      if (node.attributes.id.value in this.boundNodes) {
        return;
      }

      let widget = new geometryWidget(node);
      this.boundNodes[node.attributes.id.value] = widget;
    });
  }

  geometryWidgetManager.prototype.updateSize = function() {
    for (let elem in this.boundNodes) {
      this.boundNodes[elem].map.updateSize();
    }
  }

  window.geometryWidget = geometryWidget;
  window.geometryWidgetManager = new geometryWidgetManager();
})();
