# gevent.monkey.patch_all()

import logging
from socket import socket

from gevent.server import StreamServer

from tds import Parser
from tds.logger import BetterRotatingFileHandler

logger = logging.getLogger('tds')
max_byte = 1024 * 1024 * 10
backup_count = 3
filename = "logs/error.log"
handler = BetterRotatingFileHandler(filename=filename, maxBytes=max_byte, backupCount=backup_count)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
handler.setLevel('NOTSET')
logger.addHandler(handler)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
handler.setLevel('NOTSET')
# logger.addHandler(handler)
logger.setLevel('INFO')


def handle(sock, address):
    """

    :param socket sock: 
    :param address: 
    :return: 
    """
    logger.info('address %s', address)
    parser = Parser(sock, address, logger=logger)
    parser.run()


if __name__ == '__main__':
    server = StreamServer(('0.0.0.0', 1433), handle=handle)
    server.serve_forever()
