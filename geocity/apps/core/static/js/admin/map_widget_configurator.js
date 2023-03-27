// ------------------ SCHEMA DEFINITION ----------------------------

const baseSchema = {
  "type": "object",
  "keys": {
      "mode": {
          "type": "object",
          "keys": {
              "type": {
                  "type": "string",
                  "title": "Modes d’interaction avec la carte",
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
      "wmts": {
        "type": "array",
        "title": "WMTS",
        "items": {
                    "type": "object",
                    "keys": {
                        "capability": {
                            "type": "string",
                            "title": "Lien vers la capability",
                            "placeholder": "https://wmts.asit-asso.ch/wmts?&Service=WMTS&Version=1.0.0&Request=GetCapabilities"
                        },
                        "layer": {
                            "type": "string",
                            "title": "Nom de la couche",
                            "placeholder": "asitvd.fond_cadastral"
                        },
                        "projection": {
                            "type": "string",
                            "title": "Projection",
                            "default": "EPSG:2056"
                        },
                        "name": {
                            "type": "string",
                            "title": "Nom affiché lors de la sélection de la couche",
                            "placeholder": "Carte de base"
                        },
                        "thumbnail": {
                            "type": "string",
                            "title": "Lien vers l'image qui sera affiché lors de la sélection de la couche"
                        }
                    }
        }
      },
      "zoom": {
        "type": "integer",
        "title": "Niveau de zoom par défaut à l’ouverture de la carte",
        "default": 15
      },
      "minZoom": {
        "type": "integer",
        "title": "Niveau de zoom minimum possible",
        "default": 1
      },
      "maxZoom": {
        "type": "integer",
        "title": "Niveau de zoom maximum possible",
        "default": 20
      },
      "defaultCenter": {
        "type": "array",
        "title": "Position centrale de départ: (x, y au format EPSG:2056)",
        "minItems": 2,
        "maxItems": 2,
        'items': {
          'type': "integer",
        }
      },
      "information": {
          "type": "object",
          "keys": {
              "duration": {
                  "type": "integer",
                  "title": "Durée d’apparition de la boite d’information",
                  "default": 5000
              },
              "title": {
                  "type": "string",
                  "title": "Titre la boite d’information",
                  "default": "Signaler ..."
              },
              "content": {
                  "title": "Texte de la boite d’information ",
                  "type": "string",
                  "placeholder": "Sélectionnez un ou plusieurs lampadaire(s) défectueux présent(s) dans l’espace public de la ville."
              }
          }
      },
      "selectionTargetBoxMessage": {
          "type": "string",
          "title": "Message pour la boite informative de position",
          "placeholder": "Éclairage signalé"
      },
      "border": {
          "type": "object",
          "title": "Frontière",
          "keys": {
              "url": {
                  "type": "string",
                  "title": "Lien vers un GeoJSON contenant les informations sur la frontière",
                  "placeholder": " http://localhost:9095/submissions/adminentitiesgeojson/1/"
              },
              "notification": {
                  "type": "string",
                  "title": "Message expliquant pourquoi on ne peut effectuer une action hors des frontières",
                  "default": "Veuillez placer votre élément dans les limites autorisées",
                  "placeholder": "Veuillez placer votre élément dans les limites autorisées"
              }
          }
      },
      "inclusionArea": {
          "type": "object",
          "title": "Zone d’inclusion",
          "keys": {
              "url": {
                  "type": "string",
                  "title": "Lien vers une couche WFS contenant les informations sur la zone d’inclusion",
                  "placeholder": "https://mapnv.ch/mapserv_proxy?ogcserver=source+for+image%2Fpng&SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&typeName=MO_bf_bien_fonds"
              },
              "filter": {
                  "type": "string",
                  "title": "Filtre d’URL pour WFS permettant de filtrer les données de la zone d’inclusion",
                  "placeholder": "https://mapnv.ch/mapserv_proxy?ogcserver=source+for+image%2Fpng&SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&typeName=MO_bf_bien_fonds"
              }
          }
      },
      "notifications": {
        "type": "array",
        "items": {
          "type": "object",
          "keys": {
            "type": {
              "type": "string",
              "readonly": true
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
                  "type": "integer",
                  "minimum": 1
                },
                "couldBypass": {
                  "type": "boolean"
                },
                "maxElement": {
                  "type": "integer",
                  "title": "Maximum d’éléments pouvant être créés/sélectionnés (-1 pour 'autant que l'on souhaite')",
                  "minimum": -1
                }
              }
            },
          }
        },
      },
      "outputFormat": {
        "type": "string",
        "title": "Format des données en sortie du composant web",
        "enum": [
            "GeometryCollection",
            "FeatureCollection",
        ],
        'widget': 'radio',
        "default": "GeometryCollection"
      },
      "interaction": {
        "type": "object",
        "title": "Interactions avec la carte",
        "keys": {
          "displayZoom": {
            "type": "boolean",
            "title": "Voulez-vous afficher les boutons de zoom?",
            "default": true
          },
          "displayScaleLine": {
            "type": "boolean",
            "title": "Voulez-vous afficher la barre d’échelle?",
            "default": false
          },
          "fullscreen": {
            "type": "boolean",
            "title": "Voulez-vous permettre le mode pleine écran?",
            "default": true
          },
          "enableGeolocation": {
              "type": "boolean",
              "title": "Voulez-vous activer la géolocalisation du composant?",
              "default": true
          },
          "enableCenterButton": {
              "type": "boolean",
              "title": "Voulez-vous activer le bouton de recentrage?",
              "default": true
          },
          "enableRotation": {
              "type": "boolean",
              "title": "Voulez-vous permettre la rotation de la carte?",
              "default": true
          }
        }
      },
      "geolocationInformation": {
        "type": "object",
        "title": "Information concernant la géolocalisation des éléments créés/sélectionnés",
        "keys": {
            "displayBox": {
                "type": "boolean",
                "title": "Afficher le boite d'information sur la géolocalisation des éléments créés/sélectionnés",
                "default": true
            },
            "reverseLocation": {
                "type": "boolean",
                "title": "Rechercher et afficher l'adresse la plus proche",
                "default": true
            },
            "currentLocation": {
                "type": "boolean",
                "title": "Afficher les coordonnées",
                "default": false
            }
        }
    }
  }
}

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
  "message": "Le maximum de sélection est limité à {x}.",
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

const infoNotificationTarget = {
  "type": "info",
  "message": "Déplacez la carte pour que l’endroit désiré soit au centre de la cible.",
  "rule": {
    "type": "INFORMATION"
  }
};

const infoNotificationCreate = {
  "type": "info",
  "message": "Cliquez longuement sur la carte à l’endroit désiré pour qu’un élément soit créé.",
  "rule": {
    "type": "INFORMATION"
  }
};

const infoNotificationSelect = {
  "type": "info",
  "message": "Sélectionnez un marqueur sur la carte.",
  "rule": {
    "type": "INFORMATION"
  }
};

const infoNotificationMix = {
  "type": "info",
  "message": "Sélectionnez un marqueur ou cliquez longuement sur la carte pour qu’un élément soit créé.",
  "rule": {
    "type": "INFORMATION"
  }
};

const searchFeature = {
  "type": "object",
  "title": "Configuration pour permettre la recherche d’adresse",
  "keys": {
    "displaySearch": {
        "type": "boolean",
        "title": "Afficher la boite permettant de faire une recherche",
        "default": true
    },
    "requestWithoutCustomValue": {
        "type": "string",
        "title": "URL pour exécuter la recherche",
        "default": "https://api3.geo.admin.ch/rest/services/api/SearchServer?limit=5&&type=locations&sr=2056&lang=fr&origins=address%2Cparcel",
        "placeholder": "https://api3.geo.admin.ch/rest/services/api/SearchServer?limit=5&&type=locations&sr=2056&lang=fr&origins=address%2Cparcel"
    },
    "bboxRestiction": {
        "type": "string",
        "title": "Restriction de la zone de recherche basé sur la bbox",
        "placeholder": "2523099.818000,1167985.282000,2549752.141000,1192697.773000"
    }
  }
}

const wfsOption = {
  "type": "object",
  "keys": {
      "url": {
          "type": "string",
          "title": "URL de la couche WFS",
          "placeholder": "https://mapnv.ch/mapserv_proxy?ogcserver=source+for+image%2Fpng&SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=ELE_tragwerk_gesco"
      }
  }
};

const clusterOption = {
  "type": "object",
  "keys": {
    "distance": {
        "type": "integer",
        "title": "Distance en pixels à l'intérieur de laquelle les caractéristiques seront regroupées",
        "default": 40,
    },
    "minDistance": {
        "type": "integer",
        "title": "Distance minimale en pixels entre les clusters.",
        "default": 35,
    }
  }
}

const targetSchema = JSON.parse(JSON.stringify(baseSchema));
const createSchema = JSON.parse(JSON.stringify(baseSchema));;
createSchema.keys["search"] = searchFeature;
const selectSchema = JSON.parse(JSON.stringify(baseSchema));;
selectSchema.keys["search"] = searchFeature;
selectSchema.keys["wfs"] = wfsOption;
selectSchema.keys["cluster"] = clusterOption;
// ------------------ CODE PART ----------------------------

let form;
let schema = '';

function setupTargetMode(data, isSchemaChanged) {
  schema = targetSchema;
  if (!data.notifications || data.notifications.length == 0) {
    data.notifications = [zoomConstraintNotification,infoNotificationTarget];
  } else if (isSchemaChanged) {
    data.notifications = [zoomConstraintNotification,infoNotificationTarget];
  }
}

function setupSelectionMode(data, isSchemaChanged) {
  schema = selectSchema;
  if (!data.notifications || data.notifications.length == 0) {
    data.notifications = [zoomConstraintNotification,maximumSelectionNotification,infoNotificationSelect];
  } else if (isSchemaChanged) {
    data.notifications = [zoomConstraintNotification,maximumSelectionNotification,infoNotificationSelect];
  }
}

function setupCreateMode(data, isSchemaChanged) {
  schema = createSchema;
  if (!data.notifications || data.notifications.length == 0) {
    data.notifications = [zoomConstraintNotification,maximumSelectionNotification,infoNotificationCreate];
  } else if (isSchemaChanged) {
    data.notifications = [zoomConstraintNotification,maximumSelectionNotification,infoNotificationCreate];
  }
}

function setupMixMode(data, isSchemaChanged) {
  schema = selectSchema;
  if (!data.notifications || data.notifications.length == 0) {
    data.notifications = [zoomConstraintNotification,maximumSelectionNotification,infoNotificationMix];
  } else if (isSchemaChanged) {
    data.notifications = [zoomConstraintNotification,maximumSelectionNotification,infoNotificationMix];
  }
}

function changeSchema(data, isSchemaChange) {
  switch(data.mode.type) {
    case "target": setupTargetMode(data, isSchemaChange); break;
    case "create": setupCreateMode(data, isSchemaChange); break;
    case "select": setupSelectionMode(data, isSchemaChange); break;
    case "mix": setupMixMode(data, isSchemaChange); break;
  }
  form.update({
    schema: schema,
    data: data
  })
}

function setupDisplay(data) {
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
        data.notifications.splice(index, 1);
        form.update({
          schema: schema,
          data: data
        })
      }
    }
  }


  if (data.mode.type != prevData.mode.type) {
    changeSchema(data, true)
  }

  setupDisplay(data)
}

window.addEventListener('load', function() {
  if (window.reactJsonForm) {
      form = reactJsonForm.getFormInstance('id_configuration_jsonform');
      if (form.data.mode.type != '') {
        changeSchema(form.data, false)
        setupDisplay(form.data)
      }
      form.addEventListener('change', onJsonFormChange);
  }
});
