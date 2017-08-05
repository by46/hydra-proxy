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
        """
        
        :param socket conn: 
        :param (str, int) address: 
        :param logger: 
        """
        self.logger = logger or logging.getLogger(__name__)
        self.conn = conn
        self.client_ip, self.client_port = address
        self.conn = conn
        self.user = None
        self.database = None
        self.settings = {}

    def run(self):
        while True:
            try:
                # TODO(benjamin): testing code
                client_content = self.conn.recv(10)
                self.logger.info('Receive from client, %s', client_content)
                self.conn.send('1234567890')
                self.conn.close()
                raise AbortException()
            except AbortException as e:
                # TODO(benjamin): process abort exception
                self.logger.exception(e)
                # TODO(benjamin): send logout event
                break

    def parse_message_header(self, conn=None):
        """
        
        :param socket conn: 
        """
        # TODO(benjamin): add logical
