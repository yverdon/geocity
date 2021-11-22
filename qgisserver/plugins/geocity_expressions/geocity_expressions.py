# -*- coding: utf-8 -*-
from qgis.core import *
from qgis.utils import qgsfunction
from datetime import datetime
import json


@qgsfunction(args='auto', group='Geocity')
def get_permit_amend_properties(feature, parent):
    """
    Function to get a string output from a list of actors
    """
    get_keys = True
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    amend_properties = json.loads(d['amend_properties'])
    retval = ''
    print(f"amend_properties: {amend_properties}")
    lr = '<br>'
    for i, amend_property in amend_properties.items():
        strline = f"<h3>{i}</h3>"
        retval += strline
        for k, v in amend_property.items():
            if get_keys:
                strline = f"<dl><dt>{lr}property_{k}:</dt> <dd>{v}{lr}</dd></dl>" if str(k) == 'id' else f"<dl><dt>{k}:</dt> <dd>{v}{lr}</dd></dl>"
            else:
                strline = f"<dl><dt>property_{v}{lr}</dt></dl>" if str(k) == 'id' else f"<dl><dt>{v}{lr}</dt></dl>"
            retval += strline

    return(retval)


@qgsfunction(args='auto', group='Geocity')
def get_permit_author(feature, parent):
    """
    Function to get a string output from a list of actors
    """
    get_keys = False
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    author = json.loads(d['author'])
    retval = ''
    lr = '<br>'
    ts = '&#8239;'
    for i, (k, author) in enumerate(author.items()):
        if get_keys:
            strline = f"{lr}author_{k}: {author}{lr}" if str(k) == 'id' else f"{k}: {author}{lr}"
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
                f"E-mail{ts}:"
            ]
            strline = f"{keys[i]} {author}{lr}"
        retval += strline

    return(retval)


@qgsfunction(args='auto', group='Geocity')
def get_permit_contacts(pos, feature, parent):
    """
    Function to get a string output from a list of actors
    """
    try:
        pos
    except NameError:
        pos = 0

    get_keys = False
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    permit_request_actors = json.loads(d['permit_request_actor'])
    retval = ''
    print(f"permit_request_actors: {permit_request_actors}")
    lr = '<br>'
    ts = '&#8239;'
    for i, (j, actor) in enumerate(permit_request_actors.items()):
        if (pos==i):
            strline = f"<h3>{j}</h3>"
            retval += strline
            for idx, (k, v) in enumerate(actor.items()):
                if get_keys:
                    strline = f"{lr}contact_{k}: {v}{lr}" if str(k) == 'id' else f"{k}: {v}{lr}"
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
                        f"E-mail{ts}:"
                    ]
                    strline = f"{keys[idx]} contact_{v}{lr}" if str(k) == 'id' else f"{keys[idx]} {v}{lr}"
                retval += strline

    return(retval)


@qgsfunction(args='auto', group='Geocity')
def get_permit_request_properties(feature, parent):
    """
    Function to get a string output from a list of actors
    """
    get_keys = True
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    request_properties = json.loads(d['request_properties'])
    retval = ''
    print(f"request_properties: {request_properties}")
    lr = '<br>'
    for i, request_property in request_properties.items():
        strline = f"<h3>{i}</h3>"
        retval += strline
        for k, v in request_property.items():
            if get_keys:
                strline = f"{lr}property_{k}: {v}{lr}" if str(k) == 'id' else f"{k}: {v}{lr}"
            else:
                strline = f"{v}{lr}" if str(k) == 'id' else f"{v}{lr}"
            retval += strline

    return(retval)


@qgsfunction(args='auto', group='Geocity')
def get_permit_validations(feature, parent):
    """
    Function to get a string output from a list of actors
    """
    get_keys = False
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    validations = json.loads(d['validations'])
    retval = ''
    lr = '<br>'
    ts = '&#8239;'
    for i, (j, validation) in enumerate(validations.items()):
        strline = f"<h3>{j}</h3>"
        retval += strline
        for idx, (k, v) in enumerate(validation.items()):
            if get_keys:
                strline = f"<dl><dt>{lr}validation_{k}:</dt> <dd>{v}{lr}</dd></dl>" if str(k) == 'id' else f"<dl><dt>{k}:</dt> <dd>{v}{lr}</dd></dl>"
            else:
                keys = [
                    f"Statut{ts}:",
                    f"Commentaire (avant){ts}:",
                    f"Commentaire (pendant){ts}:",
                    f"Commentaire (après){ts}:"
                ]
                strline = f"<dl><dt>{keys[idx]}</dt><dd>validation_{v}{lr}</dd></dl>" if str(k) == 'id' else f"<dl><dt>{keys[idx]}</dt><dd>{v}{lr}</dd></dl>"
            retval += strline

    return(retval)


class GeocityExpressions:
    def __init__(self, serverIface):
        QgsMessageLog.logMessage(
            "******Loading expressions********", "GeocityExpressions", Qgis.Info
        )
        QgsExpression.registerFunction(get_permit_amend_properties)
        QgsExpression.registerFunction(get_permit_author)
        QgsExpression.registerFunction(get_permit_contacts)
        QgsExpression.registerFunction(get_permit_request_properties)
        QgsExpression.registerFunction(get_permit_validations)
