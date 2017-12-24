import pytest
import json
from shapely.geometry import shape, mapping, box

from geomark.geomark import Geomark
from geomark.config import LOGGER as logger
from . import data as _data


def strip_variable_properties(data, method='feature'):
    """ When a Geomark object is created by Geomark BC, it comes with some variable data such as a unique ID and URL,
    as well as the CreateDate and Expiry date.  We don't need to compare these.

    Presumably the Geomark folks won't change the properties they pass back without alerting their subscribers or
    making such a change a part of a new release, as such there should be ample warning.  If this becomes a problem
    in the future we can discuss simply striping the properties objects since we mostly care about accurate geometries.

    :param data: The data returned by the given Geomark method
    :param method: The method used to obtain data
    :return: a copy of the data object with variable properties removed
    """
    if method in ['feature', 'parts']:
        del data['properties']['id']
        del data['properties']['url']
        del data['properties']['createDate']
        del data['properties']['expiryDate']

    if method == 'boundingBox':
        # These methods return empty properties except for id and url, which are variable.
        data['properties'] = dict()

    if method == 'info':
        del data['id']
        del data['url']
        del data['createDate']
        del data['expiryDate']
        del data['validationError']
        del data['googleMapsUrl']
        del data['googleEarthUrl']
        del data['resourceLinks']

    if method == 'parts':
        del data['properties']['partIndex']

    return data


def test_create(geo_file):
    # Perhaps the use of the Geomark.feature() method makes this sort of double as a test_feature test...
    expected = dict(geo_file['expected_geom'])  # variable properties have already been removed.

    gm = Geomark.create(format=geo_file['format'], body=geo_file['data'])
    geojson = strip_variable_properties(json.loads(gm.feature('geojson').decode('utf8')))

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
    bbox = strip_variable_properties(json.loads(geomark_object['gm'].boundingBox('geojson').decode('utf8')), 'boundingBox')

    assert expected == bbox


@pytest.mark.dependency(depends=_data.depends_create)
def test_feature(geomark_object):
    expected = dict(geomark_object['expected_geom'])  # variable properties have already been removed.
    geojson = strip_variable_properties(json.loads(geomark_object['gm'].feature('geojson').decode('utf8')))

    assert expected == geojson


@pytest.mark.dependency(depends=_data.depends_create)
def test_info(geomark_object):
    geom_type = geomark_object['expected_geom']['geometry']['type']
    expected = dict(geomark_object['expected_geom']['properties'])
    info = strip_variable_properties(json.loads(geomark_object['gm'].info().decode('utf8')), 'info')

    # TODO It seems that the "minimumClearance" property returns inconsistent results from the webservice
    #      when fetching for a Point.  We should follow up with them.
    if geom_type == 'Point':
        info['minimumClearance'] = None

    assert expected == info


@pytest.mark.dependency(depends=_data.depends_create)
def test_parts(geomark_object):
    # Its fine to reuse the same expected geometry, because our test cases use single part geometries that will
    # return the same geometry for parts() as feature() with a single additional property.
    expected = dict(geomark_object['expected_geom'])
    geojson = strip_variable_properties(json.loads(geomark_object['gm'].parts('geojson').decode('utf8')), 'parts')

    assert expected == geojson


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
