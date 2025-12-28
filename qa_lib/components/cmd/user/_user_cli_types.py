from pydantic.dataclasses import dataclass


@dataclass
class CliEncodingResponse:
    encoding: str

@dataclass
class CliBridgeResponse:
    transaction: str
