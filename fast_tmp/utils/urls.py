from fast_tmp.conf import settings


def get_route_url(prefix: str):
    return settings.SERVER_URL + settings.ADMIN_URL + prefix
