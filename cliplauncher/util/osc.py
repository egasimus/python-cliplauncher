import socket


__all__ = ('get_free_port',)


def get_free_port():
    s = socket.socket()
    s.bind(("", 0))
    return s.getsockname()[1]

