import os
import pytest

from geomark import config
from . import data


@pytest.fixture(scope='module', params=data.geomark_ids)
def geomark_id(request):
    gm_id = request.param
    yield gm_id


@pytest.fixture(scope='module')
def geomark_ids(request):
    yield data.geomark_ids


@pytest.fixture(scope='module', params=data.geomark_ids)
def geomark_url(request):
    gm_url = config.GEOMARK_ID_BASE_URL.format(
        protocol='http',
        geomarkId=request.param
    )
    yield gm_url


@pytest.fixture(scope='module', params=data.geomark_ids)
def geomark_https_url(request):
    gm_url = config.GEOMARK_ID_BASE_URL.format(
        protocol='https',
        geomarkId=request.param
    )
    yield gm_url


@pytest.fixture(scope='module', params=data.geo_files)
def geo_file(request):
    filename = request.module.__file__
    with open(os.path.join(os.path.dirname(filename), "files/{}".format(request.param['file'])), 'r') as f:
        yield {
            'format': request.param['format'],
            'data': f.read(),
            'expected_geom': request.param['expected_geom']
        }
