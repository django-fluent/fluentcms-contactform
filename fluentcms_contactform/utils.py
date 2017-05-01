"""
Util functions
"""


def get_remote_ip(request):
    """
    Find the IP address of the current request.
    This may require reading a different request header depending on the server setup.
    However, we recommend using wsgiunproxy instead,
    so all packages can read the same header consistently.
    """
    return request.META.get('REMOTE_ADDR', None)
