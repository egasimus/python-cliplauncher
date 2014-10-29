import socket


def get_free_port():
    s = socket.socket()
    s.bind(("", 0))
    return s.getsockname()[1]
