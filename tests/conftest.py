import os
import pytest
from geomark import config

_geomark_ids = ['gm-abcdefghijklmnopqrstuvwxyz0000bc', 'gm-abcdefghijklmnopqrstuv0bcislands']

# The expected geometries for each test file of the matching geom_type
_geo_features = {
    'point': {
        'type': 'Point',
        'coordinates': [-123.37870723365188, 49.96295634587292]
    },
    'linestring': {
        'type': 'LineString',
        'coordinates': [[-123.27582683416017, 50.03973275790413], [-123.53226005267769, 49.79711929326573]]
    },
    'polygon': {
        'type': 'Polygon',
        'coordinates': [[[-123.47698103651241, 50.048945926824196], [-123.59828776745799, 50.030519590901186], [-123.59828777134982, 49.910748381756406], [-123.42937966256794, 49.74951791779005], [-123.1284161225308, 49.92149708232013], [-123.47698103651241, 50.048945926824196]]]
    }
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
def geomarkId(request):
    gm_id = request.param
    yield gm_id


@pytest.fixture(scope='module')
def geomarkIds(request):
    yield _geomark_ids


@pytest.fixture(scope='module', params=_geomark_ids)
def geomarkUrl(request):
    gm_url = config.GEOMARK_ID_BASE_URL.format(
        protocol='http',
        geomarkId=request.param
    )
    yield gm_url


@pytest.fixture(scope='module', params=_geomark_ids)
def geomarkHttpsUrl(request):
    gm_url = config.GEOMARK_ID_BASE_URL.format(
        protocol='https',
        geomarkId=request.param
    )
    yield gm_url


@pytest.fixture(scope='module', params=_geo_files)
def geoFile(request):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    with open(os.path.join(test_dir, request.param['file']), 'r') as f:
        yield {'format': request.param['format'], 'data': f.read()}
