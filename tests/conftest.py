import os
import pytest
from geomark import config

_geomark_ids = ['gm-abcdefghijklmnopqrstuvwxyz0000bc', 'gm-abcdefghijklmnopqrstuv0bcislands']
_geo_files = [
    {'format': 'kml', 'file': 'point.kml'},
    {'format': 'kml', 'file': 'line.kml'},
    {'format': 'kml', 'file': 'polygon.kml'},
    {'format': 'geojson', 'file': 'point.geojson'},
    {'format': 'geojson', 'file': 'line.geojson'},
    {'format': 'geojson', 'file': 'polygon.geojson'}
]


@pytest.fixture(scope='module',
                params=_geomark_ids)
def geomarkId(request):
    gm_id = request.param
    yield gm_id


@pytest.fixture(scope='module',
                params=_geomark_ids)
def geomarkUrl(request):
    gm_url = config.GEOMARK_ID_BASE_URL.format(
        protocol='http',
        geomarkId=request.param
    )
    yield gm_url


@pytest.fixture(scope='module',
                params=_geomark_ids)
def geomarkHttpsUrl(request):
    gm_url = config.GEOMARK_ID_BASE_URL.format(
        protocol='https',
        geomarkId=request.param
    )
    yield gm_url


@pytest.fixture(scope='module',
                params=_geo_files)
def geoFile(request):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    with open(os.path.join(test_dir, request.param['file']), 'r') as f:
        yield {'format':request.param['format'], 'data': f.read()}
