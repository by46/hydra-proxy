import logging
from io import BytesIO
from socket import socket

from tds.packets import PACKET_HEADER_LEN
from tds.packets import PacketHeader
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
                header, data = self.parse_message_header()

                method_name = self.PROCESS.get(header.packet_type, 'on_transfer')
                method = getattr(self, method_name)
                method(header, data)
            except AbortException as e:
                # TODO(benjamin): process abort exception
                self.logger.exception(e)
                # TODO(benjamin): send logout event
                break

    def parse_message_header(self, conn=None):
        """
        
        :param socket conn: 
        :rtype: (PacketHeader, BytesIO)
        """
        # TODO(benjamin): add logical
        conn = conn or self.conn
        header = conn.recv(PACKET_HEADER_LEN)
        if len(header) < self.PACKET_HEADER_LENGTH:
            # TODO(benjamin): process disconnection
            raise AbortException()
        packet_header = PacketHeader()
        packet_header.unmarshal(header)
        length = packet_header.length - self.PACKET_HEADER_LENGTH
        data = None
        if length:
            data = conn.recv(length)
        return packet_header, BytesIO(data)

    def on_transfer(self, header, buf, parse_token=False):
        pass
