import os
import pytest
from geomark import config

_geomark_ids = ['gm-abcdefghijklmnopqrstuvwxyz0000bc', 'gm-abcdefghijklmnopqrstuv0bcislands']
_kml_files = ['point.kml', 'line.kml',  'polygon.kml']


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
                params=_kml_files)
def kmlFile(request):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    with open(os.path.join(test_dir, request.param), 'r') as kml:
        yield kml.read()
