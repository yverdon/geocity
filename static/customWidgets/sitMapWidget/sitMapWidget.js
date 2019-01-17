/* global ol */

/*Adapted from geodjango map widget*/

(function() {

    'use strict';

    var jsonFormat = new ol.format.GeoJSON();

    function sitMapWidget(options) {

        var is_collection = false;

        if (options.geom_name.toLowerCase().indexOf('multi') >= 0) {
          var is_collection = true;
        }

        if (!options.geom_name.includes('MULTI')) {
           options.geom_name = options.geom_name.charAt(0).toUpperCase() + options.geom_name.slice(1).toLowerCase();
         } else {
           options.geom_name = "Multi" + options.geom_name.charAt(5).toUpperCase() + options.geom_name.slice(6).toLowerCase();
        }

        this.map = null;
        this.interactions = {draw: null, modify: null};
        this.ready = false;

        // Default options
        this.options = {
            default_center: [2538812, 1181380],
            default_zoom: 5,
            is_collection: is_collection
        };

        // Altering using user-provided options
        for (var property in options) {
            if (options.hasOwnProperty(property)) {
                this.options[property] = options[property];
            }
        }

        this.map = this.createMap();
        this.featureCollection = new ol.Collection();

        this.featureOverlay = new ol.layer.Vector({
          style: new ol.style.Style({
            image: new ol.style.Circle({
              fill: new ol.style.Fill({
                color: 'rgba(252, 50, 0, 0.8)'
              }),
              stroke: new ol.style.Stroke({
                color: 'rgba(230, 30, 0, 0.8)',
                width: 2
              }),
              radius: 8
            }),
            fill: new ol.style.Fill({
              color: 'rgba(252, 50, 0, 0.8)'
            }),
            stroke: new ol.style.Stroke({
              color: 'rgba(230, 30, 0, 0.8)',
              width: 2
            })
          }),
            map: this.map,
            source: new ol.source.Vector({
                features: this.featureCollection,
                useSpatialIndex: false // improve performance
            }),
            updateWhileAnimating: true, // optional, for instant visual feedback
            updateWhileInteracting: true // optional, for instant visual feedback
        });

        // Populate and set handlers for the feature container
        var self = this;
        this.featureCollection.on('add', function(event) {

            var feature = event.element;
            feature.on('change', function() {
                self.serializeFeatures();
            });
            if (self.ready) {
                self.serializeFeatures();
                if (!self.options.is_collection) {
                    self.disableDrawing(); // Only allow one feature at a time
                }
            }
        });

        var initial_value = document.getElementById(this.options.id).value;
        if (initial_value) {

            var features = jsonFormat.readFeatures('{"type": "Feature", "geometry": ' + initial_value + '}');
            var extent = ol.extent.createEmpty();
            features.forEach(function(feature) {
                this.featureOverlay.getSource().addFeature(feature);
                ol.extent.extend(extent, feature.getGeometry().getExtent());
            }, this);
            this.map.getView().fit(extent,  {padding: [100, 100, 100, 100],  minResolution: 1 });
            this.map.getView().setCenter(this.options.default_center);
            this.map.getView().setZoom(this.options.default_zoom);
        } else {

            this.map.getView().setCenter(this.options.default_center);
            this.map.getView().setZoom(this.options.default_zoom);
        }

        this.createInteractions();
        if (initial_value && !this.options.is_collection || this.options.edit_geom == 'False') {
            this.disableDrawing();
            this.disableModify();
        }

        this.ready = true;
    }

    proj4.defs("EPSG:2056", "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs");


    var projection = ol.proj.get('EPSG:2056');
    sitMapWidget.prototype.createMap = function() {
        var map = new ol.Map({
            controls: [
                new ol.control.ScaleLine(),
                new ol.control.Zoom(),
                new ol.control.MousePosition({
                  coordinateFormat: function(coordinate) {
                    return ol.coordinate.format(coordinate, 'Est: {x}, Nord: {y}', 0);
                  }
                })
            ],
            target: this.options.map_id,
            layers: [this.options.base_layer],
            view: new ol.View({
                zoom: this.options.default_zoom,
                minZoom: this.options.min_zoom,
                projection: projection,
                center: [2538812, 1181380]
            })
        });
        return map;
    };

    sitMapWidget.prototype.createInteractions = function() {
        // Initialize the modify interaction
        this.interactions.modify = new ol.interaction.Modify({
            features: this.featureCollection,
            deleteCondition: function(event) {
                return ol.events.condition.shiftKeyOnly(event) &&
                    ol.events.condition.singleClick(event);
            }
        });
        this.interactions.draw = new ol.interaction.Draw({
            features: this.featureCollection,
            type: this.options.geom_name,
            maxPoints: 5
        });

        this.map.addInteraction(this.interactions.draw);
        this.map.addInteraction(this.interactions.modify);
    };

    sitMapWidget.prototype.enableDrawing = function() {
        this.interactions.draw.setActive(true);
    };

    sitMapWidget.prototype.disableDrawing = function() {
        if (this.interactions.draw) {
            this.interactions.draw.setActive(false);
        }
    };

    sitMapWidget.prototype.disableModify = function() {
        if (this.interactions.modify) {
            this.interactions.modify.setActive(false);
        }
    };

    sitMapWidget.prototype.enableModify = function() {
        if (this.interactions.modify) {
            this.interactions.modify.setActive(true);
        }
    };

    sitMapWidget.prototype.clearFeatures = function() {
        this.featureCollection.clear();
        document.getElementById(this.options.id).value = '';
        this.enableDrawing();
    };

    sitMapWidget.prototype.serializeFeatures = function() {
        // Two use cases: multigeometries, and single geometry
        var geometry = null;
        var features = this.featureOverlay.getSource().getFeatures();

        if (this.options.is_collection) {

                geometry = features[0].getGeometry().clone();
                for (var j = 1; j < features.length; j++) {
                    switch(geometry.getType()) {
                        case "MultiPoint":
                            geometry.appendPoint(features[j].getGeometry().getPoint(0));
                            break;
                        case "MultiLineString":
                            geometry.appendLineString(features[j].getGeometry().getLineString(0));
                            break;
                        case "MultiPolygon":
                            geometry.appendPolygon(features[j].getGeometry().getPolygon(0));
                    }
                }
        } else {
            if (features[0]) {
                geometry = features[0].getGeometry();
            }
        }
        document.getElementById(this.options.id).value = jsonFormat.writeGeometry(geometry);
    };

    window.sitMapWidget = sitMapWidget;

})();
