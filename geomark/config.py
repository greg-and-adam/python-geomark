import logging

# TODO set LOG_LEVEL to info when we don't actively need debugging anymore.
LOG_LEVEL = logging.DEBUG  # Options include... CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)
# Default logger writes to stderr
# TODO Decide on and implement a good default handler.

GEOMARK_BASE_URL = '{protocol}://apps.gov.bc.ca/pub/geomark'
GEOMARK_ID_BASE_URL = GEOMARK_BASE_URL + '/geomarks/{geomarkId}'
GEOMARK_GROUP_BASE_URL = GEOMARK_BASE_URL + '/geomarkGroups/{geomarkGroupId}'
