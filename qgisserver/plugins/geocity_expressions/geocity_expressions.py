# -*- coding: utf-8 -*-
from qgis.core import *
from qgis.utils import qgsfunction
from datetime import datetime
import json


@qgsfunction(args="auto", group="Geocity")
def get_permit_amend_properties(feature, parent):
    """
    Function to get an HTML string output from the properties.amend_properties
    element of the GeoJSON object send by the GeoCity REST API.

    Parameters
    ----------
    None

    Returns
    -------
    retval : str
        The HTML string to be displayed in the QGIS print layout.
    """
    get_keys = True
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    amend_properties = json.loads(d["amend_properties"])
    retval = ""
    retval += "<style>body{font-family: arial; font-size: 12px;}th, td{padding: 0px;  text-align: left; font-size: 12px;}</style>"
    # print(f"amend_properties: {amend_properties}")
    lr = "<br>"
    ts = "&#8239;"
    for i, amend_property in amend_properties.items():
        strline = f"<h3>{i}</h3>"
        retval += strline
        retval += "<table>"
        for k, v in amend_property.items():
            if get_keys:
                strline = (
                    f"<tr><th>property_{k}</th> <td>{v}</td></th>"
                    if str(k) == "id"
                    else f"<tr><th>{k}</th> <td>{v}</td></tr>"
                )
            else:
                strline = (
                    f"<tr><th>property_{keys[idx]}</th> <td>{v}</td></th>"
                    if str(k) == "id"
                    else f"<tr><th>{keys[idx]}</th> <td>{v}</td></tr>"
                )
            retval += strline
        retval += "</table>"

    return retval


@qgsfunction(args="auto", group="Geocity")
def get_permit_author(feature, parent):
    """
    Function to get an HTML string output from the properties.author
    element of the GeoJSON object send by the GeoCity REST API.

    Parameters
    ----------
    None

    Returns
    -------
    retval : str
        The HTML string to be displayed in the QGIS print layout.
    """
    get_keys = False
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    author = json.loads(d["author"])
    retval = ""
    retval += "<style>body{font-family: arial; font-size: 12px;}th, td{padding: 0px;  text-align: left; font-size: 12px;}</style>"
    lr = "<br>"
    ts = "&#8239;"
    for idx, (k, v) in enumerate(author.items()):
        retval += "<table>"
        if get_keys:
            strline = (
                f"<tr><th>author_{k}:</th> <td>{v}</td></tr>"
                if str(k) == "id"
                else f"<tr><th>{k}:</th> <td>{v}</td></tr>"
            )
        else:
            keys = [
                f"Prénom{ts}:",
                f"Nom{ts}:",
                f"Adresse{ts}:",
                f"NPA{ts}:",
                f"Localité{ts}:",
                f"Raison sociale{ts}:",
                f"Numéro TVA{ts}:",
                f"Téléphone{ts}:",
                f"Téléphone (2){ts}:",
                f"E-mail{ts}:",
            ]
            # strline = f"{v}{lr}" if str(idx) == 'id' else f"{v}{lr}"
            strline = f"<tr><th>{keys[idx]}</th><td>{v}</td></tr>"
        retval += strline
        retval += "</table>"

    return retval


@qgsfunction(args="auto", group="Geocity")
def get_permit_contacts(pos, feature, parent):
    """
    Function to get an HTML string output from the properties.permit_request_actor
    element of the GeoJSON object send by the GeoCity REST API.
    
    Parameters
    ----------
    pos : int
        The index of the element to retrieve. For example, if there are several
        contacts, 0 will return the first one, 1 the second one, and so on.

    Returns
    -------
    retval : str
        The HTML string to be displayed in the QGIS print layout.
    """
    try:
        pos
    except NameError:
        pos = 0

    get_keys = False
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    permit_request_actors = json.loads(d["permit_request_actor"])
    retval = ""
    retval += "<style>body{font-family: arial; font-size: 12px;}th, td{padding: 0px;  text-align: left; font-size: 12px;}</style>"
    # print(f"permit_request_actors: {permit_request_actors}")
    lr = "<br>"
    ts = "&#8239;"
    for i, (j, actor) in enumerate(permit_request_actors.items()):
        if pos == i:
            strline = f"<h3>{j}</h3>"
            retval += strline
            retval += "<table>"
            for idx, (k, v) in enumerate(actor.items()):
                if get_keys:
                    strline = (
                        f"<tr><th>contact_{k}</th> <td>{v}</td></th>"
                        if str(k) == "id"
                        else f"<tr><th>{k}</th> <td>{v}</td></tr>"
                    )
                else:
                    keys = [
                        f"Type{ts}:",
                        f"Identifiant{ts}:",
                        f"Prénom{ts}:",
                        f"Nom{ts}:",
                        f"Raison sociale{ts}:",
                        f"Numéro TVA{ts}:",
                        f"Adresse{ts}:",
                        f"NPA{ts}:",
                        f"Localité{ts}:",
                        f"Téléphone{ts}:",
                        f"E-mail{ts}:",
                    ]
                    strline = (
                        f"<tr><th>contact_{keys[idx]}</th> <td>{v}</td></tr>"
                        if str(k) == "id"
                        else f"<tr><th>{keys[idx]}</th> <td>{v}</td></tr>"
                    )
                retval += strline
            retval += "</table>"

    return retval


@qgsfunction(args="auto", group="Geocity")
def get_permit_geotime(feature, parent):
    """
    Function to get an HTML string output from the properties.geotime_aggregated
    element of the GeoJSON object send by the GeoCity REST API.

    Parameters
    ----------
    None

    Returns
    -------
    retval : str
        The HTML string to be displayed in the QGIS print layout.
    """
    get_keys = False
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    geotime = json.loads(d["geotime_aggregated"])
    retval = ""
    retval += "<style>body{font-family: arial; font-size: 12px;}th, td{padding: 0px;  text-align: left; font-size: 12px;}</style>"
    lr = "<br>"
    ts = "&#8239;"
    for idx, (k, v) in enumerate(geotime.items()):
        retval += "<table>"
        if get_keys:
            strline = (
                f"<tr><th>geotime_{k}:</th> <td>{v}</td></tr>"
                if str(k) == "id"
                else f"<tr><th>{k}:</th> <td>{v}</td></tr>"
            )
        else:
            keys = [
                f"Date de début{ts}:",
                f"Date de fin{ts}:",
                f"Commentaire{ts}:",
                f"Lien externe{ts}:",
            ]
            # strline = f"{v}{lr}" if str(idx) == 'id' else f"{v}{lr}"
            strline = f"<tr><th>{keys[idx]}</th><td>{v}</td></tr>"
        retval += strline
        retval += "</table>"

    return retval


def translate_boolean(v):
    """
    Function to translate a boolean value to the french [Oui/Non] equivalent.

    Parameters
    ----------
    v : bool
        The input boolean to convert.

    Returns
    -------
    retval : v
        The corresponding translated string.
    """
    if isinstance(v, bool) and v:
        v = "Oui"
    if isinstance(v, bool) and not v:
        v = "Non"

    return v


@qgsfunction(args="auto", group="Geocity")
def get_permit_request_properties(feature, parent):
    """
    Function to get an HTML string output from the properties.request_properties
    element of the GeoJSON object send by the GeoCity REST API.

    Parameters
    ----------
    None

    Returns
    -------
    retval : str
        The HTML string to be displayed in the QGIS print layout.
    """
    get_keys = True
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    request_properties = json.loads(d["request_properties"])
    retval = ""
    retval += "<style>body{font-family: arial; font-size: 12px;}th, td{padding: 0px;  text-align: left; font-size: 12px;}</style>"
    # print(f"request_properties: {request_properties}")
    lr = "<br>"
    ts = "&#8239;"
    for i, request_property in request_properties.items():
        strline = f"<h3>{i}</h3>"
        retval += strline
        retval += "<table>"
        for idx, (k, v) in enumerate(request_property.items()):
            v = translate_boolean(v)
            if get_keys:
                strline = (
                    f"<tr><th>property_{k}{ts}:</th> <td>{v}</td></th>"
                    if str(k) == "id"
                    else f"<tr><th>{k}{ts}:</th> <td>{v}</td></tr>"
                )
            else:
                keys = [
                    f"Largeur [m]{ts}:",
                    f"Longueur [m]{ts}:",
                    f"Marquage routier endommmagé{ts}:",
                    f"Moins de 3m d'un tronc d'arbre ou haie{ts}:",
                    f"Sur la chaussée{ts}:",
                    f"Sur une surface verte{ts}:",
                    f"Sur un trottoir{ts}:",
                    f"Description{ts}:",
                    f"Documents complémentaires{ts}:",
                ]
                # strline = f"<tr><th>{v}</th></tr>" if str(k) == 'id' else f"<tr><th>{v}</th></tr>"
                strline = f"""<tr><th>property_{keys[idx]}</th> <td>{v}</td></th>" if str(k) == 'id' else f"<tr><th>{keys[idx]}</th> <td>{v}</td></tr>"""
            retval += strline
        retval += "</table>"

    return retval


@qgsfunction(args="auto", group="Geocity")
def get_permit_validations(feature, parent):
    """
    Function to get an HTML string output from the properties.validations
    element of the GeoJSON object send by the GeoCity REST API.

    Parameters
    ----------
    None

    Returns
    -------
    retval : str
        The HTML string to be displayed in the QGIS print layout.
    """
    get_keys = False
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    validations = json.loads(d["validations"])
    retval = ""
    retval += "<style>body{font-family: arial; font-size: 12px;}th, td{padding: 0px;  text-align: left; font-size: 12px;}</style>"
    lr = "<br>"
    ts = "&#8239;"
    for i, (j, validation) in enumerate(validations.items()):
        strline = f"<h3>{j}</h3>"
        retval += strline
        retval += "<table>"
        for idx, (k, v) in enumerate(validation.items()):
            if get_keys:
                strline = (
                    f"<tr><th>validation_{k}</th> <td>{v}</td></th>"
                    if str(k) == "id"
                    else f"<tr><th>{k}</th> <td>{v}</td></tr>"
                )
            else:
                keys = [
                    f"Statut{ts}:",
                    f"Commentaire (avant){ts}:",
                    f"Commentaire (pendant){ts}:",
                    f"Commentaire (après){ts}:",
                ]
                strline = (
                    f"<tr><th>validation_{keys[idx]}</th> <td>{v}</td></tr>"
                    if str(k) == "id"
                    else f"<tr><th>{keys[idx]}</th> <td>{v}</td></tr>"
                )
            retval += strline
        retval += "</table>"

    return retval


class GeocityExpressions:
    def __init__(self, serverIface):
        QgsMessageLog.logMessage(
            "******Loading expressions********", "GeocityExpressions", Qgis.Info
        )
        QgsExpression.registerFunction(get_permit_amend_properties)
        QgsExpression.registerFunction(get_permit_author)
        QgsExpression.registerFunction(get_permit_contacts)
        QgsExpression.registerFunction(get_permit_geotime)
        QgsExpression.registerFunction(get_permit_request_properties)
        QgsExpression.registerFunction(get_permit_validations)
