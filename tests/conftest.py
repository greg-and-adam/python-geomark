import pytest
from geomark import config


_geomark_ids = ['gm-abcdefghijklmnopqrstuvwxyz0000bc', 'gm-abcdefghijklmnopqrstuv0bcislands']


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
