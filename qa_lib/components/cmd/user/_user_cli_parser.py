from qa_lib.utils import ParserOutput
from .._parser import CmdParser
from ._user_cli_types import *


class UserCliOutputParser(CmdParser):
    _re_encoding = r'^(0x[0-9a-fA-F]{64})$'
    _re_bridge_instruction = r'sent bridge instruction transaction: ([0-9A-F]{64})\n'
    _re_bridge_mint_tx = r'sent mint tx: ([0-9A-F]{64})\n'

    def parse_encoding_response(self, msg: str) -> ParserOutput[CliEncodingResponse]:
        data = self._standardize_regex_output([self._re_encoding], msg)
        if len(data) != 1:
            return ParserOutput(None, msg, True)
        return ParserOutput(CliEncodingResponse(*data), msg, False)

    def parse_bridge_instruction_response(self, msg: str) -> ParserOutput[CliBridgeResponse]:
        data = self._standardize_regex_output([self._re_bridge_instruction], msg)
        if len(data) != 1:
            return ParserOutput(None, msg, True)
        return ParserOutput(CliBridgeResponse(*data), msg, False)

    def parse_bridge_mint_response(self, msg: str) -> ParserOutput[CliBridgeResponse]:
        data = self._standardize_regex_output([self._re_bridge_mint_tx], msg)
        if len(data) != 1:
            return ParserOutput(None, msg, True)
        return ParserOutput(CliBridgeResponse(*data), msg, False)