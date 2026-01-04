from xrpl.clients import JsonRpcClient
from xrpl.models import AccountInfo


class RippleClient:

    def __init__(self, rpc_url: str, rpc_api_key: str) -> None:
        xapikey = ('?x-apikey=' + rpc_api_key) if rpc_api_key else ''
        self.client = JsonRpcClient(rpc_url + xapikey)

    def get_balance(self, xrpl_address: str) -> int:
        response = self.client.request(AccountInfo(account=xrpl_address))
        if response.result.get('error') == 'actNotFound': return 0
        return int(response.result["account_data"]["Balance"])
