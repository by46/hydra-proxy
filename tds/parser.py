import logging
from datetime import datetime
from io import BytesIO
from socket import socket
from time import time

from bunch import Bunch

import user
from pool import manager
from tds import mq
from tds.exceptions import AbortException
from tds.packets import PACKET_HEADER_LEN
from tds.packets import PacketHeader
from tds.request import LoginRequest
from tds.request import PreLoginRequest
from tds.request import SQLBatchRequest
from tds.response import LoginResponse
from tds.tokens import Collation
from tds.tokens import DoneStream
from tds.tokens import EnvChangeStream
from tds.tokens import InfoStream
from tds.tokens import LoginAckStream
from tds.tokens import PreLoginStream
from tds.tokens import parse_error

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
                self.logger.exception(e)
                if self.user:
                    self._send_logout_event()
                break

    def parse_message_header(self, conn=None):
        """
        
        :param socket conn: 
        :rtype: (PacketHeader, BytesIO)
        """
        # TODO(benjamin): add logical
        conn = conn or self.conn
        header = conn.recv(PACKET_HEADER_LEN)
        if len(header) < PACKET_HEADER_LEN:
            # TODO(benjamin): process disconnection
            raise AbortException()
        packet_header = PacketHeader()
        packet_header.unmarshal(header)
        length = packet_header.length - PACKET_HEADER_LEN
        data = None
        if length:
            data = conn.recv(length)
        return packet_header, BytesIO(data)

    def on_pre_login(self, header, buf):
        """

        :param PacketHeader header: 
        :param BytesIO buf: 
        """
        request = PreLoginRequest(buf)
        response = PreLoginStream()
        response.version = (1426128904, 0)
        response.encryption = PreLoginStream.ENCRYPT_NOT_SUP
        response.inst_opt = ''
        response.thread_id = 1234
        header = PacketHeader()
        content = header.marshal(response)
        self.conn.sendall(content)

    def on_login(self, header, buf):
        """

        :param PacketHeader header: 
        :param BytesIO buf: 
        """
        packet = LoginRequest(buf)
        self.database = packet.database
        self.user = packet.username
        info = user.login(packet.username, packet.password)
        if info is None:
            # TODO(benjamin): process login failed
            pass
        self.settings = {
            "user": info.user,
            "password": info.password,
            "instance": "{0}\\{1}".format(info.server_name, info.database),
            "database": self.database,
            "ip": info.server_name,
            "port": info.port
        }
        self.user = packet.username
        self.database = packet.database
        self._send_login_event()

        self.logger.info('logging password %s', packet.password)
        response = LoginResponse()
        env1 = EnvChangeStream()
        env1.add(1, 'CTI', 'master')
        sql_collation = Collation()
        env2 = EnvChangeStream()
        env2.add_bytes(EnvChangeStream.ENV_SQL_COLLATION, sql_collation.marshal())
        env3 = EnvChangeStream()
        env3.add(EnvChangeStream.ENV_LANGUAGE, 'us_english')
        ack = LoginAckStream()
        ack.program_name = "TDS"
        env = EnvChangeStream()
        env.add(EnvChangeStream.ENV_DATABASE, '4096', '4096')
        done = DoneStream()
        info = InfoStream()
        info.msg = "Changed database context to 'CTI'."
        info.server_name = 'S1DSQL04\\EHISSQL'
        info.line_number = 10

        response.add_component(env1)
        response.add_component(info)
        response.add_component(ack)
        response.add_component(env)
        response.add_component(done)

        header = PacketHeader()
        content = header.marshal(response)
        self.conn.sendall(content)

    def on_batch(self, header, buf):
        """

        :param PacketHeader header: 
        :param BytesIO buf: 
        :return: 
        """
        cur = time()
        request = SQLBatchRequest(buf)
        response_buf = self.on_transfer(header, buf)
        elapse = int((time() - cur) * 1000)
        error_stream = parse_error(response_buf)
        error_message = None
        if error_stream:
            self.logger.error('error occur')
            error_message = "{0}DB-Lib error message {1}, severity {2}".format(error_stream.msg,
                                                                               error_stream.error_number,
                                                                               error_stream.error_level)

        self.logger.info('batch sql elapse %s ms: %s', elapse, request.text)
        # TODO(benjamin): process batch error
        self._send_batch_event(elapse, request.text, error=error_message)

    def on_transfer(self, header, buf, parse_token=False):
        """

        :param PacketHeader header: 
        :param BytesIO buf: 
        :param bool parse_token: 
        :rtype: [StreamSerializer]
        """
        message = header.marshal(buf)
        pool = manager.get_connection(self.settings)
        with pool.get() as conn:
            conn.sendall(message)
            self._send_input_event(message)
            header, response_buf = self.parse_message_header(conn)
        message = header.marshal(response_buf)
        self.conn.sendall(message)
        self._send_output_event(message)

        return response_buf

    def _make_event(self, event):
        stamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3]

        return Bunch(event=event,
                     user=self.user,
                     database=self.database,
                     client_ip=self.client_ip,
                     stamp=stamp)

    def _send_output_event(self, message):
        event = self._make_event(event=EVENT_OUTPUT)
        event.size = len(message)
        mq.send(event)

    def _send_input_event(self, message):
        event = self._make_event(event=EVENT_INPUT)
        event.size = len(message)
        mq.send(event)

    def _send_batch_event(self, elapse, text, error):
        event = self._make_event(event=EVENT_BATCH)
        event.elapse = elapse
        event.text = text
        event.error = error
        mq.send(event)

    def _send_login_event(self):
        event = self._make_event(event=EVENT_LOGIN)
        mq.send(event)

    def _send_logout_event(self):
        event = self._make_event(event=EVENT_LOGOUT)
        mq.send(event)
