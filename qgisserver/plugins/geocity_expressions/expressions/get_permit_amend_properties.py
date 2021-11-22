from qgis.core import *
from qgis.gui import *
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
