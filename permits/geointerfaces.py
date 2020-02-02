import urllib.request
import urllib.parse
import json


def reverse_geocode(east_coordinate, north_coordinate, api_epsg):

    print('reverse geocoding...')
    if api_epsg == '21781':
    	east_coordinate = east_coordinate - 2000000
    	north_coordinate = north_coordinate - 1000000

    base_url = 'https://api3.geo.admin.ch/rest/services/api/MapServer/identify'

    params = {
    	'mapExtent': '0,0,100,100',
    	'imageDisplay': '100,100,100',
    	'tolerance': 10,
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

# WIP
def get_cadastre_parcel(east_coordinate, north_coordinate, source_crs, api_crs):

    base_url = 'https://www.geo.vd.ch/main/wsgi/mapserv_proxy'
    params = {
        'LAYERS': 'cad_parcelle',
        'SERVICE': 'WMS',
        'VERSION':'1.1.1',
        'REQUEST': 'GetFeatureInfo',
        'BBOX':'2538680.75%2C1180753.25%2C2538986%2C1181003.25',
        'FEATURE_COUNT':1,
        'HEIGHT':'1000',
        'WIDTH': '1221',
        'FORMAT':'image%2Fpng',
        'INFO_FORMAT': 'application%2Fvnd.ogc.gml',
        'SRS': 'EPSG%3A2056',
        'X': 0,
        'Y': 0,

    }
    print(east_coordinate, north_coordinate, source_crs, api_crs)
    data = urllib.parse.urlencode(params)
    url = base_url + '/?' + data
