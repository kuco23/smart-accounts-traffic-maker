from typing import List, TypeVar
from re import findall
from qa_lib.utils import ParserOutput

T = TypeVar("T")


class CmdParser:

    @staticmethod
    def _ensure_parser_response(output: ParserOutput[T]) -> T:
        assert not output.err, f"could not parse:\n{output.origin}"
        return output.resp

    @classmethod
    def _standardize_regex_output(cls, rgxs: List[str], msg: str) -> List[str]:
        parses = []
        for rgx in rgxs:
            parses.extend(findall(rgx, msg))
        return cls.flatten(parses)

    @staticmethod
    def flatten(xss):
        resp = []
        for x in xss:
            if isinstance(x, tuple):
                resp.extend(x)
            else:
                resp.append(x)
        return resp
