import urllib.request
import urllib.parse
import json, os


def reverse_geocode(east_coordinate, north_coordinate, api_epsg):

    if api_epsg == '21781':
    	east_coordinate = east_coordinate - 2000000
    	north_coordinate = north_coordinate - 1000000

    base_url = 'https://api3.geo.admin.ch/rest/services/api/MapServer/identify'
    params = {
    	'mapExtent': '0,0,100,100',
    	'imageDisplay': '100,100,100',
    	'tolerance': os.environ["REVERSE_ADRESS_GEOCODING_TOLERANCE"],
    	'geometryType':'esriGeometryPoint',
    	'geometry': str(east_coordinate) + ',' + str(north_coordinate),
    	'layers': 'all:ch.bfs.gebaeude_wohnungs_register',
    	'returnGeometry': 'false',
    }

    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(base_url, data)
    json_response_short = None
    with urllib.request.urlopen(req) as response:
    	json_response = json.loads(response.read())

    	if len(json_response['results']) > 0:
            first_feature_attributes = json_response['results'][0]['attributes']
            json_response_short = {
                'street_name': first_feature_attributes['label'],
                'street_number': first_feature_attributes['deinr'],
                'npa': first_feature_attributes['plz4'],
                'administrative_entity_name': first_feature_attributes['plzname'],
                'administrative_entity_ofs_id': first_feature_attributes['gdenr'],
            }
    return json_response_short
