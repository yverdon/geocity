from qgis.core import *
from qgis.gui import *
import json

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
    for i, (j, actor) in enumerate(permit_request_actors.items()):
        if (pos==i):
            strline = f"<h3>{j}</h3>"
            retval += strline
            for k, v in actor.items():
                if get_keys:
                    strline = f"{lr}contact_{k}: {v}{lr}" if str(k) == 'id' else f"{k}: {v}{lr}"
                else:
                    strline = f"{v}{lr}" if str(k) == 'id' else f"{v}{lr}"
                retval += strline

    return(retval)
