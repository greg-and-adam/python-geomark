import pytest
import json
from geomark.geomark import Geomark


@pytest.fixture(scope='class')
def geomarkId(request):
    request.cls.geomarkId = 'gm-abcdefghijklmnopqrstuvwxyz0000bc'
    yield


@pytest.mark.usefixtures('geomarkId')
class TestGeoMark(object):

    def test_bbox(self):
        gm = Geomark(geomarkId=self.geomarkId)
        assert gm.boundingBox()

    def test_feature(self):
        gm = Geomark(geomarkId=self.geomarkId)
        assert gm.feature()

    def test_info(self):
        gm = Geomark(geomarkId=self.geomarkId)
        assert gm.info()

    def test_parts(self):
        gm = Geomark(geomarkId=self.geomarkId)
        assert gm.boundingBox()

    def test_point(self):
        gm = Geomark(geomarkId=self.geomarkId)
        assert gm.point()

    def test_copy(self):
        gm = Geomark(geomarkId=self.geomarkId)
        assert gm.copy()

    def test_create(self):
        assert Geomark.create()
