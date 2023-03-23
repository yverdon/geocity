// ------------------ SCHEMA DEFINITION ----------------------------

const baseSchema = {
  "type": "object",
  "keys": {
      "mode": {
          "type": "object",
          "keys": {
              "type": {
                  "type": "string",
                  "enum": [
                      "create",
                      "select",
                      "target",
                      "mix"
                  ],
                  'widget': 'radio'
              }
          }
      },
      "information": {
          "type": "object",
          "keys": {
              "duration": {
                  "type": "integer",
                  "default": 5000
              },
              "title": {
                  "type": "string",
                  "default": "Signaler ..."
              },
              "content": {
                  "type": "string"
              }
          }
      },
      "enableGeolocation": {
          "type": "boolean",
          "title": " Voulez-vous activer la géolocalisation du composant?",
          "default": true
      },
      "enableCenterButton": {
          "type": "boolean",
          "title": " Voulez-vous activer le bouton de recentrage?",
          "default": true
      },
      "enableRotation": {
          "type": "boolean",
          "title": " Voulez-vous permettre la rotation de la carte?",
          "default": true
      },
      "selectionTargetBoxMessage": {
          "type": "string",
          "title": " Message pour la boite informative de position"
      },

      "wmts": {
          "type": "array",
          "items": {
                      "type": "object",
                      "keys": {
                          "capability": {
                              "type": "string",
                              "title": "URL capability",
                              "placeholder": "https://wmts.asit-asso.ch/wmts?&Service=WMTS&Version=1.0.0&Request=GetCapabilities"
                          },
                          "layer": {
                              "type": "string",
                              "title": "Nom du layer",
                              "placeholder": "asitvd.fond_cadastral"
                          },
                          "projection": {
                              "type": "string",
                              "default": "EPSG:2056"
                          },
                          "name": {
                              "type": "string",
                              "title": "URL capability",
                              "placeholder": "Carte de base"
                          },
                          "thumbnail": {
                              "type": "string",
                              "title": "URL capability"
                          }
                      }
          }
      },
      "border": {
          "type": "object",
          "keys": {
              "url": {
                  "type": "string",
                  "placeholder": " http://localhost:9095/submissions/adminentitiesgeojson/1/"
              },
              "notification": {
                  "type": "string",
                  "default": "Veuillez placer votre élément dans les limites autorisées",
                  "placeholder": "Veuillez placer votre élément dans les limites autorisées"
              }
          }
      },
      "inclusionArea": {
          "type": "object",
          "keys": {
              "url": {
                  "type": "string",
                  "placeholder": "https://mapnv.ch/mapserv_proxy?ogcserver=source+for+image%2Fpng&SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&typeName=MO_bf_bien_fonds"
              },
              "filter": {
                  "type": "string",
                  "placeholder": "https://mapnv.ch/mapserv_proxy?ogcserver=source+for+image%2Fpng&SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&typeName=MO_bf_bien_fonds"
              }
          }
      },
      "geolocationInformation": {
          "type": "object",
          "keys": {
              "displayBox": {
                  "type": "boolean",
                  "title": "Afficher le boite d'information sur la géolocalisation des objets créés/sélectionnés",
                  "default": true
              },
              "reverseLocation": {
                  "type": "boolean",
                  "title": "Trouver l'adresse la plus proche",
                  "default": true
              },
              "currentLocation": {
                  "type": "boolean",
                  "title": "Afficher les coordonnées",
                  "default": false
              }
          }
      },
      "notifications": {
        "type": "array",
        "items": {
          "type": "object",
          "keys": {
            "type": {
              "type": "string"
            },
            "message": {
              "type": "string"
            },
            "rule": {
              "type": "object",
              "keys": {
                "type": {
                  "type": "string"
                },
                "minZoom": {
                  "type": "integer"
                },
                "couldBypass": {
                  "type": "boolean"
                },
                "maxElement": {
                  "type": "integer"
                }
              }
            },
          }
        },
      }
  }
}

const createSchema = baseSchema;
const targetSchema = baseSchema;
const selectSchema = baseSchema;
selectSchema.keys["wfs"] = {
  "type": "object",
  "keys": {
      "url": {
          "type": "string",
          "title": "URL de la couche WFS",
          "placeholder": "https://mapnv.ch/mapserv_proxy?ogcserver=source+for+image%2Fpng&SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=ELE_tragwerk_gesco"
      }
  }
};

const zoomConstraintNotification = {
  "type": "warning",
  "message": "Veuillez zoomer davantage avant de pouvoir sélectionner un emplacement.",
  "rule": {
    "type": "ZOOM_CONSTRAINT",
    "minZoom": 16
  }
};

const maximumSelectionNotification = {
  "type": "warning",
  "message": "Le maximum de sélections est limité à {x}.",
  "rule": {
      "type": "MAX_SELECTION",
      "maxElement": 1
  }
};

const areaConstraintNotification = {
  "type": "warning",
  "message": "L’emplacement sélectionné se situe en dehors des zones autorisées.",
  "rule": {
      "type": "AREA_CONSTRAINT",
      "couldBypass": false
  }
};

const infoNotification  = {
  "type": "info",
  "message": "",
  "rule": {
    "type": "MOVE_TARGET"
  }
};
// ------------------ CODE PART ----------------------------

let form;
let schema = '';

function setupTargetMode(data) {
  schema = targetSchema;
  if (!data.notifications || data.notifications.length == 0) {
    data.notifications = [zoomConstraintNotification,infoNotification];
  }
}

function setupSelectionMode(data) {
  schema = selectSchema;
  if (!data.notifications || data.notifications.length == 0) {
    data.notifications = [zoomConstraintNotification,maximumSelectionNotification,infoNotification];
  }
}

function setupCreateMode(data) {
  schema = createSchema;
  if (!data.notifications || data.notifications.length == 0) {
    data.notifications = [zoomConstraintNotification,maximumSelectionNotification,infoNotification];
  }
}

function setupMixMode(data) {
  schema = selectSchema;
  if (!data.notifications || data.notifications.length == 0) {
    data.notifications = [zoomConstraintNotification,maximumSelectionNotification,infoNotification];
  }
}

function changeSchema(data) {
  switch(data.mode.type) {
    case "target": setupTargetMode(data); break;
    case "create": setupCreateMode(data); break;
    case "select": setupSelectionMode(data); break;
    case "mix": setupMixMode(data); break;
  }
  form.update({
    schema: schema,
    data: data
  })
}

window.addEventListener('load', function() {
  if (window.reactJsonForm) {
      form = reactJsonForm.getFormInstance('id_configuration_jsonform');
      if (form.data.mode.type != '')
        changeSchema(form.data)
      form.addEventListener('change', onJsonFormChange);
  }
});


function onJsonFormChange(e) {
  const data = e.data;
  const prevData = e.prevData;

  if (prevData.inclusionArea && data.inclusionArea) {
    if (prevData.inclusionArea.url == '' && data.inclusionArea.url != '') {
      data.notifications.push(areaConstraintNotification)
      form.update({
        schema: schema,
        data: data
      })
    } else if (prevData.inclusionArea.url != '' && data.inclusionArea.url == '') {
      const index = data.notifications.findIndex((notification) => notification.rule.type == "AREA_CONSTRAINT");
      if (index != -1) {
        data.notifications.splice(index, -1);
        form.update({
          schema: schema,
          data: data
        })
      }
    }
  }


  if (data.mode.type != prevData.mode.type) {
    changeSchema(data)
  }

  if (data.notifications && data.notifications.length > 0) {
    for (let i = 0; i < data.notifications.length; i++) {
      const ruleType = document.getElementsByName(`rjf§notifications§${i}§rule§type`)
      if (ruleType && ruleType.length > 0 ) {
        if (ruleType[0].value !== "ZOOM_CONSTRAINT") {
          const minZoom = document.getElementsByName(`rjf§notifications§${i}§rule§minZoom`)
          if (minZoom) {
            minZoom[0].parentElement.parentElement.parentElement.parentElement.style.display = 'none'
          }
        }
        if (ruleType[0].value !== "AREA_CONSTRAINT") {
          const couldBypass = document.getElementsByName(`rjf§notifications§${i}§rule§couldBypass`)
          if (couldBypass) {
            couldBypass[0].parentElement.parentElement.parentElement.parentElement.style.display = 'none'
          }
        }
        if (ruleType[0].value !== "MAX_SELECTION") {
          const maxElement = document.getElementsByName(`rjf§notifications§${i}§rule§maxElement`)
          if (maxElement) {
            maxElement[0].parentElement.parentElement.parentElement.parentElement.style.display = 'none'
          }
        }
      }
    }
  }
}
