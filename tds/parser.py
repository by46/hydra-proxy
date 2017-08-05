import logging
from socket import socket

EVENT_LOGIN = "login"
EVENT_LOGOUT = "logout"
EVENT_INPUT = "input"
EVENT_OUTPUT = "output"
EVENT_BATCH = "batch"


class Parser(object):
    def __init__(self, conn, address, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.conn = conn
        self.client_ip, self.client_port = address
        self.conn = None  # type: socket
        self.user = None
        self.database = None
        self.settings = {}

    def run(self):
        pass
