from attrs import define, field
from qa_lib.components.common import CommonUtils
from qa_lib.components.params import ParamLoader
from qa_lib.components.chain import RippleClient, RippleWallet, MasterAccountController, FAsset
from qa_lib.components.cmd import UserCli


@define
class BaseUserBot:
    id: str
    params: ParamLoader
    utils: CommonUtils
    ripple: RippleClient
    fasset: FAsset
    master_account_controller: MasterAccountController
    cli: UserCli

    _wallet: RippleWallet = field(init = False)
    personal_address: str = field(init = False)

    def __attrs_post_init__(self):
        self._wallet = RippleWallet(self.ripple.client.url, self.cli.env['XRPL_SECRET'])
        self.personal_address = self.master_account_controller.get_personal_account(self.address)

    @property
    def address(self) -> str:
        return self._wallet.wallet.address
