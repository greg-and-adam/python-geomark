import pytest
import json
from geomark.geomark import Geomark
from geomark.config import LOGGER as logger


def strip_variable_properties(data, method='feature'):
    if method in ['feature']:
        del data['properties']['id']
        del data['properties']['url']
        del data['properties']['createDate']
        del data['properties']['expiryDate']

        return data


@pytest.mark.dependency()
def test_create(geo_file):
    # Perhaps the use of the Geomark.feature() method makes this sort of double as a test_feature test...
    expected = geo_file['expected_geom']  # variable properties have already been removed.

    gm = Geomark.create(format=geo_file['format'], body=geo_file['data'])
    geojson = strip_variable_properties(json.loads(gm.feature('geojson')))

    assert expected == geojson


@pytest.mark.dependency(depends=["test_create"])
def test_create_other_formats(geo_files):
    expected = geo_files['expected_geom']  # variable properties have already been removed.

    gm = Geomark.create(format=geo_files['format'], body=geo_files['data'])
    geojson = strip_variable_properties(json.loads(gm.feature('geojson')))

    assert expected == geojson


@pytest.mark.dependency(depends=["test_create"])
def test_bbox(geomark_id):
    gm = Geomark(geomarkId=geomark_id)
    assert gm.boundingBox() is not None


@pytest.mark.dependency(depends=["test_create"])
def test_feature(geomark_id):
    gm = Geomark(geomarkId=geomark_id)
    assert gm.feature()


@pytest.mark.dependency(depends=["test_create"])
def test_info(geomark_id):
    gm = Geomark(geomarkId=geomark_id)
    assert gm.info()


@pytest.mark.dependency(depends=["test_create"])
def test_parts(geomark_id):
    gm = Geomark(geomarkId=geomark_id)
    assert gm.boundingBox()


@pytest.mark.dependency(depends=["test_create"])
def test_point(geomark_id):
    gm = Geomark(geomarkId=geomark_id)
    assert gm.point()


@pytest.mark.dependency(depends=["test_create"])
def test_copy(geomark_id):
    gm = Geomark(geomarkId=geomark_id)
    assert gm.copy()


@pytest.mark.dependency(depends=["test_create"])
def test_copy_multiple(geomark_ids):
    gm1 = Geomark(geomarkId=geomark_ids[0])
    assert gm1.copy(geomarkUrl=[geomark_ids[0], geomark_ids[1]], allowOverlap=True, bufferMetres=0.1)
