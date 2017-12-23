import pytest
import json
from shapely.geometry import shape, mapping, box

from geomark.geomark import Geomark
from geomark.config import LOGGER as logger
from . import data as _data


def strip_variable_properties(data, method='feature'):
    """ When a Geomark object is created by Geomark BC, it comes with some variable data such as a unique ID and URL,
    as well as the CreateDate and Expiry date.  We don't need to compare these.

    :param data: The data returned by the given Geomark method
    :param method: The method used to obtain data
    :return: a copy of the data object with variable properties removed
    """
    if method in ['feature']:
        del data['properties']['id']
        del data['properties']['url']
        del data['properties']['createDate']
        del data['properties']['expiryDate']

    elif method in ['boundingBox']:
        # These methods return empty properties except for id and url, which are variable.
        data['properties'] = dict()

    return data


def test_create(geo_file):
    # Perhaps the use of the Geomark.feature() method makes this sort of double as a test_feature test...
    expected = dict(geo_file['expected_geom'])  # variable properties have already been removed.

    gm = Geomark.create(format=geo_file['format'], body=geo_file['data'])
    geojson = strip_variable_properties(json.loads(gm.feature('geojson')))

    assert expected == geojson


@pytest.mark.dependency(depends=_data.depends_create)
def test_bbox(geomark_object):
    geom_type = geomark_object['expected_geom']['geometry']['type']

    expected = strip_variable_properties(dict(geomark_object['expected_geom']), 'boundingBox')
    expected_bbox = json.loads(json.dumps(mapping(box(*shape(expected['geometry']).bounds))))

    # This funny shapely method of deriving a bounding box leaves out the closing point if getting the bounds of a Point
    if geom_type == 'Point':
        expected_bbox['coordinates'][0].append(expected_bbox['coordinates'][0][0])

    expected['geometry'] = expected_bbox
    bbox = strip_variable_properties(json.loads(geomark_object['gm'].boundingBox('geojson')), 'boundingBox')

    assert expected == bbox


@pytest.mark.dependency(depends=_data.depends_create)
def test_feature(geomark_object):
    expected = dict(geomark_object['expected_geom'])

    assert geomark_object['gm'].feature()


@pytest.mark.dependency(depends=_data.depends_create)
def test_info(geomark_object):
    expected = dict(geomark_object['expected_geom'])

    assert geomark_object['gm'].info()


@pytest.mark.dependency(depends=_data.depends_create)
def test_parts(geomark_object):
    expected = dict(geomark_object['expected_geom'])

    assert geomark_object['gm'].parts()


@pytest.mark.dependency(depends=_data.depends_create)
def test_point(geomark_object):
    expected = dict(geomark_object['expected_geom'])

    assert geomark_object['gm'].point()


@pytest.mark.dependency(depends=_data.depends_create)
def test_copy(geomark_object):
    assert geomark_object['gm'].copy()


@pytest.mark.dependency(depends=_data.depends_create)
def test_copy_multiple(geomark_ids):
    gm1 = Geomark(geomarkId=geomark_ids[0])
    assert gm1.copy(geomarkUrl=[geomark_ids[0], geomark_ids[1]], allowOverlap=True, bufferMetres=0.1)
