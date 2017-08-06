import gevent.monkey

gevent.monkey.patch_all()

import logging
from socket import socket

from gevent.server import StreamServer

from tds import Parser


def handle(sock, address):
    """

    :param socket sock: 
    :param address: 
    :return: 
    """
    logging.error('address %s', address)
    parser = Parser(sock, address)
    parser.run()


if __name__ == '__main__':
    server = StreamServer(('0.0.0.0', 1433), handle=handle)
    server.serve_forever()
