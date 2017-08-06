from io import BytesIO

from tds.base import StreamSerializer
from .alt_metadata import ALTMetadataStream
from .alt_row import ALTRowStream
from .col_info import ColumnInfoStream
from .col_metadata import ColumnMetadataStream
from .collation import Collation
from .done import DoneStream
from .done_in_proc import DoneInProcedureStream
from .done_proc import DoneProcedureStream
from .envchange import EnvChangeStream
from .error import ErrorStream
from .feature_ext_ack import FeatureExtAckStream
from .fed_auth_info import FedAuthInfoStream
from .info import InfoStream
from .login import Login7Stream
from .login import LoginAckStream
from .nbc_row import NBCRowStream
from .offset import OffsetStream
from .order import OrderStream
from .pre_login import PreLoginStream
from .return_status import ReturnStatusStream
from .return_value import ReturnValueStream
from .row import RowStream
from .session_state import SessionStateStream
from .sql_batch import SQLBatchStream
from .sspi import SSPIStream
from .tab_name import TableNameStream
from .tvp_row import TVPRowStream

tokens = [ALTMetadataStream, ALTRowStream, ColumnInfoStream,
          ColumnMetadataStream, DoneStream, DoneInProcedureStream, DoneProcedureStream,
          EnvChangeStream, ErrorStream, FeatureExtAckStream, FedAuthInfoStream,
          InfoStream, LoginAckStream, NBCRowStream, OffsetStream, OrderStream,
          ReturnStatusStream, ReturnValueStream,
          RowStream, SessionStateStream,
          SSPIStream, TableNameStream, TVPRowStream]

MAPPINGS = {token.TOKEN_TYPE: token for token in tokens}


def parse_tokens(buf):
    """
    Parse all tokens 
    :param BytesIO buf: 
    :rtype: [StreamSerializer]
    """
    items = []
    while True:
        token_type = buf.read(1)
        buf.seek(-1, 1)
        if not token_type:
            break
        token_type = ord(token_type)
        if token_type not in MAPPINGS:
            raise Exception()
        stream_class = MAPPINGS.get(token_type)
        print stream_class, buf.tell()
        stream = stream_class()  # type: StreamSerializer
        stream.unmarshal(buf)
        items.append(stream)
    return items


def parse_error(buf):
    """
    Parse all tokens 
    :param BytesIO buf: 
    :rtype: ErrorStream
    """
    token_type = buf.read(1)
    buf.seek(-1, 1)
    if not token_type:
        return None
    token_type = ord(token_type)
    if token_type not in MAPPINGS:
        raise Exception()
    if token_type == ErrorStream.TOKEN_TYPE:

        stream = ErrorStream()  # type: StreamSerializer
        stream.unmarshal(buf)
        return stream
