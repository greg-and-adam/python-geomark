import requests
from . import config as _config


class Geomark:

    def __init__(self, geomarkId=None, geomarkUrl=None, protocol='https', config=_config):
        self.config = config
        self.protocol = protocol

        self.logger = self.config.LOGGER

        if not geomarkId and not geomarkUrl:
            raise SyntaxError("One of geomarkId or geomarkUrl are required kwargs")

        if geomarkId:
            self.geomarkUrl = self.config.GEOMARK_ID_BASE_URL.format(
                protocol=self.protocol,
                geomarkId=geomarkId,
            )
            self.geomarkId = geomarkId
        else:
            self.geomarkId = self._parse_geomark_url()
            self.geomarkUrl = geomarkUrl

        self.logger.info('Initiated Geomark object with the following parameters: '
                         'geomarkId={geomarkId}; '
                         'geomarkUrl={geomarkUrl}; '
                         'protocol={protocol}; '
                         'custom_config: {custom_config}'.format(

            geomarkId=geomarkId,
            geomarkUrl=geomarkUrl,
            protocol=protocol,
            custom_config='YES' if config is _config else 'NO'
        ))

    def _parse_geomark_url(self, url):
        raise NotImplementedError("_parse_geomark_url() method has not yet been implemented")
        # return url

    def _handle_request(self, request):
        if request.ok:
            return request.content
        else:
            raise ValueError("A non-ok status code ({}) was returned from the server.".format(request.status_code))

    def boundingBox(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '/boundingBox.{fileFormatExtension}'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_request(requests.get(url, params={'srid': srid} if srid else None))

    def feature(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '/feature.{fileFormatExtension}'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_request(requests.get(url, params={'srid': srid} if srid else None))

    def info(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '.{fileFormatExtension}?'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_request(requests.get(url, params={'srid': srid} if srid else None))

    def parts(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '/parts.{fileFormatExtension}'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_request(requests.get(url, params={'srid': srid} if srid else None))

    def point(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '/point.{fileFormatExtension}'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_request(requests.get(url, params={'srid': srid} if srid else None))

    def copy(self, **kwargs):
        copy_url = self.config.GEOMARK_BASE_URL + '/geomarks/copy'
        raise NotImplementedError("copy is not implemented")

    @classmethod
    def create(cls, config=_config, **kwargs):
        create_url = config.GEOMARK_BASE_URL + '/geomarks/new'
        raise NotImplementedError("create is not implemented")
