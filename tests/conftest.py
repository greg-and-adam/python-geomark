import os
import pytest
from geomark import config


_geomark_ids = ['gm-abcdefghijklmnopqrstuvwxyz0000bc', 'gm-abcdefghijklmnopqrstuv0bcislands']

# The expected geometries for each test file of the matching geom_type
_geo_features = {
    'point': {'type': 'Feature', 'crs': {'type': 'name', 'properties': {'name': 'urn:ogc:def:crs:EPSG::4326'}}, 'geometry': {'type': 'Point', 'coordinates': [-123.37870723365188, 49.96295634587292]}, 'properties': {'id': 'gm-E90C7FC4363D4E5FA41F51CB2EB31BFF', 'url': 'http://apps.gov.bc.ca/pub/geomark/geomarks/gm-E90C7FC4363D4E5FA41F51CB2EB31BFF', 'geometryType': 'Point', 'numPolygons': 1, 'numParts': 1, 'createDate': '2017-12-21', 'expiryDate': '2018-03-21', 'minX': -123.37870723365188, 'minY': 49.96295634587292, 'maxX': -123.37870723365188, 'maxY': 49.96295634587292, 'centroidX': -123.37870723365188, 'centroidY': 49.96295634587292, 'numVertices': 1, 'length': 0, 'area': 0, 'isValid': True, 'isSimple': True, 'isRobust': True, 'minimumClearance': None}},
    'linestring': {'type': 'Feature', 'crs': {'type': 'name', 'properties': {'name': 'urn:ogc:def:crs:EPSG::4326'}}, 'geometry': {'type': 'LineString', 'coordinates': [[-123.27582683416017, 50.03973275790413], [-123.53226005267769, 49.79711929326573]]}, 'properties': {'id': 'gm-E59C2100E5DD49938C2B40ABC44EDC3D', 'url': 'http://apps.gov.bc.ca/pub/geomark/geomarks/gm-E59C2100E5DD49938C2B40ABC44EDC3D', 'geometryType': 'LineString', 'numPolygons': 1, 'numParts': 1, 'createDate': '2017-12-21', 'expiryDate': '2018-03-21', 'minX': -123.53226005267769, 'minY': 49.79711929326573, 'maxX': -123.27582683416017, 'maxY': 50.03973275790413, 'centroidX': -123.40404344341893, 'centroidY': 49.918426025584935, 'numVertices': 2, 'length': 32669.339029919942, 'area': 0, 'isValid': True, 'isSimple': True, 'isRobust': True, 'minimumClearance': 32669.34}},
    'polygon': {'type': 'Feature', 'crs': {'type': 'name', 'properties': {'name': 'urn:ogc:def:crs:EPSG::4326'}}, 'geometry': {'type': 'Polygon', 'coordinates': [[[-123.47698103651241, 50.048945926824196], [-123.59828776745799, 50.030519590901186], [-123.59828777134982, 49.910748381756406], [-123.42937966256794, 49.74951791779005], [-123.1284161225308, 49.92149708232013], [-123.47698103651241, 50.048945926824196]]]}, 'properties': {'id': 'gm-A904DD27E8974F969B20B22C5308ABAD', 'url': 'http://apps.gov.bc.ca/pub/geomark/geomarks/gm-A904DD27E8974F969B20B22C5308ABAD', 'geometryType': 'Polygon', 'numPolygons': 1, 'numParts': 1, 'createDate': '2017-12-21', 'expiryDate': '2018-03-21', 'minX': -123.59828777134982, 'minY': 49.74951791779005, 'maxX': -123.1284161225308, 'maxY': 50.048945926824196, 'centroidX': -123.40793678392268, 'centroidY': 49.914070995317516, 'numVertices': 6, 'length': 101540.46853039399, 'area': 621899992, 'isValid': True, 'isSimple': True, 'isRobust': True, 'minimumClearance': 8928.062}}
}

# The shapes resulting from each {shape_type}.{format} should have the same shapes stored in different formats
_geo_files = [
    {'format': 'kml', 'file': 'point.kml', 'expected_geom': _geo_features['point']},
    {'format': 'kml', 'file': 'line.kml', 'expected_geom': _geo_features['linestring']},
    {'format': 'kml', 'file': 'polygon.kml', 'expected_geom': _geo_features['polygon']},
    {'format': 'geojson', 'file': 'point.geojson', 'expected_geom': _geo_features['point']},
    {'format': 'geojson', 'file': 'line.geojson', 'expected_geom': _geo_features['linestring']},
    {'format': 'geojson', 'file': 'polygon.geojson', 'expected_geom': _geo_features['polygon']}
]


@pytest.fixture(scope='module', params=_geomark_ids)
def geomark_id(request):
    gm_id = request.param
    yield gm_id


@pytest.fixture(scope='module')
def geomark_ids(request):
    yield _geomark_ids


@pytest.fixture(scope='module', params=_geomark_ids)
def geomark_url(request):
    gm_url = config.GEOMARK_ID_BASE_URL.format(
        protocol='http',
        geomarkId=request.param
    )
    yield gm_url


@pytest.fixture(scope='module', params=_geomark_ids)
def geomark_https_url(request):
    gm_url = config.GEOMARK_ID_BASE_URL.format(
        protocol='https',
        geomarkId=request.param
    )
    yield gm_url


@pytest.fixture(scope='module')
def geo_file(request):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    with open(os.path.join(test_dir, _geo_files[0]['file']), 'r') as f:
        yield {'format': _geo_files[0]['format'], 'data': f.read()}


@pytest.fixture(scope='module', params=_geo_files)
def geo_files(request):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    with open(os.path.join(test_dir, request.param['file']), 'r') as f:
        yield {'format': request.param['format'], 'data': f.read()}
