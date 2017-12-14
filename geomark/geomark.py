import requests


_base_url = "{protocol}://apps.gov.bc.ca/pub/geomark"
_gm_id_base = _base_url + '/geomarks/{geomarkId}'


class Geomark:

    def __init__(self, geomarkId=None, geomarkUrl=None, protocol='https'):
        self.protocol = protocol

        if not geomarkId and not geomarkUrl:
            raise SyntaxError("One of geomarkId or geomarkUrl are required kwargs")

        if geomarkId:
            self.geomarkUrl = _gm_id_base.format(
                protocol=self.protocol,
                geomarkId=geomarkId,
            )
            self.geomarkId = geomarkId
        else:
            self.geomarkId = self._parse_geomark_url()
            self.geomarkUrl = geomarkUrl

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
        copy_url = _base_url + '/geomarks/copy'
        raise NotImplementedError("copy is not implemented")

    @classmethod
    def create(cls, **kwargs):
        create_url = _base_url + '/geomarks/new'
        raise NotImplementedError("create is not implemented")
