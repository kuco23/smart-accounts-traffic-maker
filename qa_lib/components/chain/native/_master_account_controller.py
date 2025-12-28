from typing import Tuple
from ._native_client import NativeClient


class MasterAccountController:
    def __init__(self, client: NativeClient, abi: object, address: str):
        self.contract = client.get_contract(abi, address)

    def get_personal_account(self, xrpl_address: str) -> Tuple[int, int]:
        return self.contract.functions.getPersonalAccount(xrpl_address).call()
