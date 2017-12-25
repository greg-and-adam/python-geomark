import os
import pytest

from geomark import config, Geomark
from . import data


@pytest.fixture(scope='module')
def geomark_ids(request):
    yield data.geomark_ids


@pytest.fixture(scope='function', params=data.dependency_geo_files)
def geo_file(request):
    filename = request.module.__file__
    with open(os.path.join(os.path.dirname(filename), "files/{}".format(request.param['file'])), 'r') as f:
        yield {
            'format': request.param['format'],
            'data': f.read(),
            'geom_type': request.param['geom_type']
        }


@pytest.fixture(scope='module', params=data.geo_files)
def geomark_object(request):
    filename = request.module.__file__
    with open(os.path.join(os.path.dirname(filename), "files/{}".format(request.param['file'])), 'r') as f:
        yield {
            'gm': Geomark.create(format=request.param['format'], body=f.read()),
            'geom_type': request.param['geom_type']
        }


@pytest.fixture(scope='function')
def geomark_id(geomark_object):
    yield geomark_object.geomarkId
