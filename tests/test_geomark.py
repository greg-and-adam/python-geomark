import pytest
import json
from geomark.geomark import Geomark


def test_bbox(geomarkId):
    gm = Geomark(geomarkId=geomarkId)
    assert gm.boundingBox()


def test_feature(geomarkId):
    gm = Geomark(geomarkId=geomarkId)
    assert gm.feature()


def test_info(geomarkId):
    gm = Geomark(geomarkId=geomarkId)
    assert gm.info()


def test_parts(geomarkId):
    gm = Geomark(geomarkId=geomarkId)
    assert gm.boundingBox()


def test_point(geomarkId):
    gm = Geomark(geomarkId=geomarkId)
    assert gm.point()


def test_copy(geomarkId):
    gm = Geomark(geomarkId=geomarkId)
    assert gm.copy()


def test_copy_multiple(geomarkIds):
    gm1 = Geomark(geomarkId=geomarkIds[0])
    assert gm1.copy(geomarkUrl=[geomarkIds[0], geomarkIds[1]], allowOverlap=True, bufferMetres=0.1)


def test_create(geoFile):
    assert Geomark.create(format=geoFile['format'], body=geoFile['data'])
