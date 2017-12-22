import pytest
import json
from geomark.geomark import Geomark


@pytest.mark.dependency()
def test_create(geo_file):
    assert Geomark.create(format=geo_file['format'], body=geo_file['data'])


@pytest.mark.dependency(depends=["test_create"])
def test_create_other_formats(geo_files):
    assert Geomark.create(format=geo_files['format'], body=geo_files['data'])


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
