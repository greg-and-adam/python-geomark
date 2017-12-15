import pytest


_geomark_ids = ['gm-abcdefghijklmnopqrstuvwxyz0000bc', 'gm-abcdefghijklmnopqrstuv0bcislands']
_base_url = "apps.gov.bc.ca/pub/geomark/geomarks"


@pytest.fixture(scope='module',
                params=_geomark_ids)
def geomarkId(request):
    gm_id = request.param
    yield gm_id


@pytest.fixture(scope='module',
                params=_geomark_ids)
def geomarkUrl(request):
    # TODO get the config system setup and use the base_url from config instead of providing it here.
    gm_url = "{}{}/{}".format('http://', _base_url, request.param)
    yield gm_url


@pytest.fixture(scope='module',
                params=_geomark_ids)
def geomarkHttpsUrl(request):
    # TODO get the config system setup and use the base_url from config instead of providing it here.
    gm_url = "{}{}/{}".format('https://', _base_url, request.param)
    yield gm_url
