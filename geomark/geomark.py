import os
import requests
# from six.moves.urllib.parse import urlparse

from . import config as _config

_base_url = "{protocol}://apps.gov.bc.ca/pub/geomark"
_gm_id_base = _base_url + '/geomarks/{geomarkId}'


class Geomark:

    def __init__(self, geomarkId=None, geomarkUrl=None, config=_config):
        self.config = config

        self.logger = self.config.LOGGER

        if not geomarkId and not geomarkUrl:
            raise SyntaxError("One of geomarkId or geomarkUrl are required kwargs")

        if geomarkId:
            self.geomarkUrl = self.config.GEOMARK_ID_BASE_URL.format(
                protocol=config.PROTOCOL,
                geomarkId=geomarkId,
            )
            self.geomarkId = geomarkId
        else:
            self.geomarkId, self.geomarkUrl, self.config.PROTOCOL = self._parse_geomark_url(geomarkUrl)

        self.logger.info('Initiated Geomark object with the following parameters: '
                         'geomarkId={geomarkId}; '
                         'geomarkUrl={geomarkUrl}; '
                         'protocol={protocol}; '
                         'custom_config: {custom_config}'.format(

            geomarkId=geomarkId,
            geomarkUrl=geomarkUrl,
            protocol=config.PROTOCOL,
            custom_config='YES' if config is _config else 'NO')
        )

    def _parse_geomark_url(self, url):
        """
        Parse the geomarkUrl for GeomarkId, protocol, and strip off the format specifier if one is present
        :param url:
        :return: GeomarkId, GeomarkUrl (no format), PROTOCOL
        """
        parsed = requests.compat.urlparse(url)
        tail = parsed.path.split('/')[-1]
        gmid, format = os.path.splitext(tail)
        if format:
            url = url.replace(format, '')

        return gmid, url, parsed.scheme

    def boundingBox(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '/boundingBox.{fileFormatExtension}'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_get(requests.get(url, params={'srid': srid} if srid else None))

    def feature(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '/feature.{fileFormatExtension}'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_get(requests.get(url, params={'srid': srid} if srid else None))

    def info(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '.{fileFormatExtension}?'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_get(requests.get(url, params={'srid': srid} if srid else None))

    def parts(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '/parts.{fileFormatExtension}'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_get(requests.get(url, params={'srid': srid} if srid else None))

    def point(self, fileFormatExtension='json', srid=None):
        url = self.geomarkUrl + '/point.{fileFormatExtension}'.format(
            fileFormatExtension=fileFormatExtension,
        )
        return self._handle_get(requests.get(url, params={'srid': srid} if srid else None))

    def copy(self, **kwargs):
        """
        This is almost the same as create but provides the geomarkUrl kwarg and a different post url.
        TIP: If you do a straight copy without altering any of the parameters the geomark
        server will notice that the geometry is identical and instead of giving you back a new Geomark
        instance you will simply be given back the original. The workaround is to specify a tiny buffer
        on the geometry using the bufferMeters kwarg.
        :param kwargs:
        :return:
        """
        # Todo: allow sourcing from multiple geomarks, ie geomark_url as a list.
        # Todo: put allow overlap into formData, NOT as a query param

        url = self.config.GEOMARK_BASE_URL.format(protocol=self.config.PROTOCOL) + '/geomarks/copy'
        kwargs.update({'geomarkUrl': self.geomarkUrl})
        params = self._validate_post_kwargs(**kwargs)
        r = requests.post(url, params=params)
        return Geomark._handle_post(r)

    @staticmethod
    def create(
            format=None,
            srid=4326,
            resultFormat='geojson',
            multiple=False,
            allowOverlap=False,
            # callback              ---- Not supported
            # redirectUrl           ---- Not supported
            # failureRedirectUrl    ---- Not supported
            bufferMetres=None,
            bufferJoin=None,
            bufferCap=None,
            bufferMitreLimit=None,
            bufferSegments=None,
            body=None,
            extra_kwargs={}):
        """
        Create a Geomark layer
        :param format:
        :param srid:
        :param resultFormat:
        :param multiple:
        :param allowOverlap:
        :param bufferMetres:
        :param bufferJoin:
        :param bufferCap:
        :param bufferMitreLimit:
        :param bufferSegments:
        :param body:
        :param extra_kwargs: put the overridden config object here, key: "config"
        :return:
        """
        import inspect
        kwargs = inspect.getargvalues(inspect.currentframe()).locals  # collect the method's named args
        form_data = Geomark._validate_post_kwargs(**kwargs)

        config = extra_kwargs.get("config", _config)
        url = config.GEOMARK_BASE_URL.format(protocol=config.PROTOCOL) + '/geomarks/new'

        return Geomark._handle_post(requests.post(url, data=form_data))

    @staticmethod
    def _handle_get(response):
        if response.ok:
            return response.content
        else:
            response.raise_for_status()

    @staticmethod
    def _handle_post(response):
        if response.ok:
            url = response.url
            response.close()
            return Geomark(geomarkUrl=url)
        else:
            response.raise_for_status()

    @staticmethod
    def _validate_post_kwargs(**kwargs):
        """
        Used by both create() and copy()
        Doesn't do anything right now.
        We don't need to pull out Nones because requests will do that for us.
        :param kwargs:
        :return:
        """
        # TODO Actually validate post kwargs.
        return kwargs
