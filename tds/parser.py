import logging
from socket import socket

from .exceptions import AbortException

EVENT_LOGIN = "login"
EVENT_LOGOUT = "logout"
EVENT_INPUT = "input"
EVENT_OUTPUT = "output"
EVENT_BATCH = "batch"


class Parser(object):
    PROCESS = {
        0x01: 'on_batch',
        0x10: 'on_login',
        0x12: 'on_pre_login'
    }

    def __init__(self, conn, address, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.conn = conn
        self.client_ip, self.client_port = address
        self.conn = None  # type: socket
        self.user = None
        self.database = None
        self.settings = {}

    def run(self):
        while True:
            try:
                pass
            except AbortException as e:
                # TODO(benjamin): process abort exception
                self.logger.exception(e)
                # TODO(benjamin): send logout event
                pass

    def parse_message_header(self, conn=None):
        """
        
        :param socket conn: 
        """
        # TODO(benjamin): add logical
