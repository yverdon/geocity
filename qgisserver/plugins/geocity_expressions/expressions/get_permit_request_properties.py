from qgis.core import *
from qgis.gui import *
import json

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
