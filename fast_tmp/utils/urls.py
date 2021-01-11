from fast_tmp.conf import settings


def get_route_url(prefix: str):
    return settings.SERVER_URL + settings.FAST_TMP_URL + prefix
