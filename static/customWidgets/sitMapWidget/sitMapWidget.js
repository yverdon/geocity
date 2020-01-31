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
        this.wmtsLayer = new ol.layer.Tile({});
        this.wmtsLayerAlternative = new ol.layer.Tile({});
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

        var createTextStyle = function(feature, resolution, dom) {
          var align = dom.align.value;
          var baseline = dom.baseline.value;
          var size = dom.size.value;
          var height = dom.height.value;
          var offsetX = parseInt(dom.offsetX.value, 10);
          var offsetY = parseInt(dom.offsetY.value, 10);
          var weight = dom.weight.value;
          var placement = dom.placement ? dom.placement.value : undefined;
          var maxAngle = dom.maxangle ? parseFloat(dom.maxangle.value) : undefined;
          var overflow = dom.overflow ? (dom.overflow.value == 'true') : undefined;
          var rotation = parseFloat(dom.rotation.value);
          if (dom.font.value == '\'Open Sans\'' && !openSansAdded) {
            var openSans = document.createElement('link');
            openSans.href = 'https://fonts.googleapis.com/css?family=Open+Sans';
            openSans.rel = 'stylesheet';
            document.getElementsByTagName('head')[0].appendChild(openSans);
            openSansAdded = true;
          }
          var font = weight + ' ' + size + '/' + height + ' ' + dom.font.value;
          var fillColor = dom.color.value;
          var outlineColor = dom.outline.value;
          var outlineWidth = parseInt(dom.outlineWidth.value, 10);

          return new Text({
            textAlign: align == '' ? undefined : align,
            textBaseline: baseline,
            font: font,
            text: getText(feature, resolution, dom),
            fill: new Fill({color: fillColor}),
            stroke: new Stroke({color: outlineColor, width: outlineWidth}),
            offsetX: offsetX,
            offsetY: offsetY,
            placement: placement,
            maxAngle: maxAngle,
            overflow: overflow,
            rotation: rotation
          });
        };

        var labelStyle = new ol.style.Style({
          text: new ol.style.Text({
            font: '18px Calibri,sans-serif',
            overflow: true,
            fill: new ol.style.Fill({
              color: '#000'
            }),
            stroke: new ol.style.Stroke({
              color: '#fff',
              width: 3
            })
          })
        });

      var countryStyle = new  ol.style.Style({

        stroke: new  ol.style.Stroke({
          color: '#fcba03',
          width: 2
        })
      });

      var style = [countryStyle, labelStyle];

       this.adminEntities = new ol.layer.Vector({
           opacity: 100,
           source: new ol.source.Vector({
           }),
           style: function(feature) {
              labelStyle.getText().setText(feature.get('name'));
              return style;
            },
       });

        this.administrativeEntityMask = new ol.layer.Tile({
           extent: [420000, 30000, 900000, 350000],
           projection: projection,
           source: new ol.source.TileWMS(({
             // TODO: don't hardcode this!!!
             url: "http://localhost:9096/",
             projection: projection,
             params: {
             "LAYERS": "gpf_administrativeentity",
             "TILED": "true",
             "VERSION": "1.3.0"},
           })),
           title: "gpf_administrativeentity",
           opacity: 1.000000,

         });

        this.administrativeEntityMask .setVisible(true)
        this.map = this.createMap(this.adminEntities, this.administrativeEntityMask);
        this.addBaseLayer();
        this.setupAlternativeBaseLayer();
        this.loadAdminEntities();

        this.featureCollection = new ol.Collection();

        this.featureOverlay = new ol.layer.Vector({
          name: 'featureOverlay',
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

        } else {

            this.map.getView().setCenter(this.options.default_center);
            this.map.getView().setZoom(this.options.default_zoom);
        }

        this.createInteractions();
        if (this.options.edit_geom == 'False') {
            this.disableDrawing();
            this.disableModify();
            this.hideMapButtons();
        }

        this.ready = true;
    }

    var projection = new ol.proj.Projection({
        code: 'EPSG:2056',
        extent: [485869.5728, 76443.1884, 837076.5648, 299941.7864],
        units: 'm'
    });

    ol.proj.addProjection(projection);


    sitMapWidget.prototype.createMap = function(adminEntities, administrativeEntityMask) {


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
            layers: [adminEntities, administrativeEntityMask],
            target: this.options.map_id,
            view: new ol.View({
                zoom: this.options.default_zoom,
                minZoom: this.options.min_zoom,
                projection: projection,
                center: [2538812, 1181380]
            })
        });
        return map;
    };


    sitMapWidget.prototype.loadAdminEntities = function () {

      var _this = this;

      $.ajax({
          url: this.options.administrative_entities_url,
          success: function(response) {

               var gJson = new ol.format.GeoJSON();
                var feats = [];
                for (var i=0; i < response.features.length; i++) {
                  var f = gJson.readFeature(response.features[i]);
                  f.setId(response.features[i].properties.pk)
                  feats.push(f);
                }
                _this.adminEntities.getSource().addFeatures(feats)

             }
       });


   };


    sitMapWidget.prototype.addBaseLayer = function() {

      var wmtsLayerName = this.options.wmts_layer;
      var matrixSet = this.options.map_srid;
      var _this = this;

       $.ajax({
           url: this.options.wmts_capabilities_url,
           success: function(response) {
                var parser = new ol.format.WMTSCapabilities();
                 var result = parser.read(response);
                 var options = ol.source.WMTS.optionsFromCapabilities(result, {
                   layer: wmtsLayerName,
                   matrixSet: matrixSet,
                   projection: 'EPSG:' + matrixSet,
                 });

                 _this.wmtsLayer.setSource(new ol.source.WMTS(/** @type {!olx.source.WMTSOptions} */ (options)));

              }
            });

       this.map.getLayers().insertAt(0, this.wmtsLayer);
       this.wmtsLayer.setVisible(true);
    }


    sitMapWidget.prototype.setupAlternativeBaseLayer = function() {

      var wmtsLayerName = this.options.wmts_layer_alternative;
      var matrixSet = this.options.map_srid;
      var _this = this;

       $.ajax({
           url: this.options.wmts_capabilities_url_alternative,
           success: function(response) {
             var parser = new ol.format.WMTSCapabilities();
             var result = parser.read(response);
             var options = ol.source.WMTS.optionsFromCapabilities(result, {
               layer: wmtsLayerName,
               matrixSet: matrixSet,
               projection: 'EPSG:' + matrixSet
             });

             _this.wmtsLayerAlternative.setSource(new ol.source.WMTS(/** @type {!olx.source.WMTSOptions} */ (options)));

       }});

       this.map.getLayers().insertAt(0, this.wmtsLayerAlternative);
       this.wmtsLayerAlternative.setVisible(false);

    }

    sitMapWidget.prototype.switchBaseLayers = function() {

        if (this.wmtsLayer.getVisible()) {
            this.wmtsLayerAlternative.setVisible(true);
            this.wmtsLayer.setVisible(false);
        } else {
            this.wmtsLayerAlternative.setVisible(false);
            this.wmtsLayer.setVisible(true);
        }

    }


    sitMapWidget.prototype.createInteractions = function() {
        // Initialize the modify interaction
        this.interactions.modify = new ol.interaction.Modify({
            features: this.featureCollection,
            style: new ol.style.Style({})
        });
        // Initialize the draw interaction
        this.interactions.draw = new ol.interaction.Draw({
            features: this.featureCollection,
            type: this.options.geom_name,
            condition: function(evt) {
                if (evt.pointerEvent.type == 'pointerdown' && evt.pointerEvent.buttons == 1
                      && !evt.originalEvent.altKey) {
                    return true;
                } else {
                    return false
                }
            }
        });

        // Initialize the select interaction
        this.interactions.select = new ol.interaction.Select({
          layers: [this.featureOverlay],
          style: new ol.style.Style({
            image: new ol.style.Circle({
              fill: new ol.style.Fill({
                color: 'rgba(255, 238, 0, 1)'
              }),
              stroke: new ol.style.Stroke({
                color: 'rgba(175, 164, 0, 1)',
                width: 1
              }),
              radius: 9
            })
          })
        });

        this.map.addInteraction(this.interactions.draw);
        this.map.addInteraction(this.interactions.modify);
        this.map.addInteraction(this.interactions.select);

        this.map.on("pointermove", function (evt) {
            var hit = evt.map.hasFeatureAtPixel(evt.pixel, {
                layerFilter: function (layer) {
                  if (layer.get('name') === 'featureOverlay') {
                    return true;
                  } else {
                    return false;
                  }
              }
            });

            this.getTargetElement().style.cursor = hit ? 'pointer' : '';
        });

    };


    sitMapWidget.prototype.enableDrawing = function() {
        this.interactions.draw.setActive(true);
    };


    sitMapWidget.prototype.hideMapButtons = function() {
        $('#mapButtons').hide();
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
        this.interactions.select.getFeatures().clear();
        document.getElementById(this.options.id).value = '';
        this.enableDrawing();
    };


    sitMapWidget.prototype.removeLastPoint = function() {

        if (this.featureCollection.getLength() > 0) {
          this.featureCollection.pop();
          this.interactions.select.getFeatures().clear();
        }
        if (this.featureCollection.getLength() > 0) {
          this.serializeFeatures();
        };
    }


    sitMapWidget.prototype.removeSelectedPoint = function() {

        var selectedFeature = this.interactions.select.getFeatures().item(0);
        var sourceF = this.featureCollection;
        var featureToDeleteIndex = -1;
        if (selectedFeature) {
            for (var i=0; i < sourceF.getLength(); i++) {

              if (sourceF.item(i).ol_uid === selectedFeature.ol_uid){
                featureToDeleteIndex = i;
              }
            }
            this.featureCollection.removeAt(featureToDeleteIndex);
            this.interactions.select.getFeatures().clear();
      }
    }


    sitMapWidget.prototype.addPointFeature= function() {

      var east = parseFloat($('#east_coord')[0].value);
      var north = parseFloat($('#north_coord')[0].value);
        var feature = new ol.Feature({
          geometry: new ol.geom.MultiPoint([[east, north]]),
        });

        this.featureCollection.push(feature);
        this.interactions.select.getFeatures().clear();

    };


    sitMapWidget.prototype.zoomToAdminEntity= function(admin_pk) {

      var feature = this.adminEntities.getSource().getFeatureById(admin_pk);
      if (feature) {
        var bounds = feature.getGeometry().getExtent();
        this.map.getView().fit(bounds, this.map.getSize());
      }

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
