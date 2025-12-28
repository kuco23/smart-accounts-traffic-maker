from typing import Dict, List
from .utils import cached, Singleton
from .components.params import ParamLoader
from .components.common import CommonUtils
from .components.chain import (
    RippleClient,
    RippleWallet,
    NativeClient,
    NativeWallet,
    MasterAccountController,
    FAsset,
)
from .components.cmd import UserCli
from .components.actors.standalone import UserMinterAndRedeemer
from .components.actors.hive import SimpleUserHive


class DependencyManager(metaclass=Singleton):
    @property
    @cached
    def params(self):
        return ParamLoader()

    @property
    @cached
    def utils(self):
        return CommonUtils(self.params)

    @property
    @cached
    def native_chain_client(self):
        return NativeClient(self.params.rpc_url, self.params.rpc_api_key)

    @property
    @cached
    def ripple_rpc(self):
        return RippleClient(self.params.ripple_rpc_url, self.params.ripple_rpc_api_key)

    @property
    @cached
    def ripple_fund_distributer_wallet(self):
        return RippleWallet(self.ripple_rpc, self.params.load_test_xrp_distributor_seed)

    @property
    @cached
    def native_fund_distributor_wallet(self):
        return NativeWallet(
            self.native_chain_client, self.params.load_test_nat_distributor_pvk
        )

    @property
    @cached
    def master_account_controller(self):
        return MasterAccountController(
            self.native_chain_client,
            self.params._asset_manager_abi,
            self.params.get_address(self.params.asset_manager_name),
        )

    @property
    @cached
    def fasset(self):
        return FAsset(
            self.native_chain_client,
            self.params._fasset_abi,
            self.params.get_address(self.params.fasset_name),
        )

    @property
    @cached
    def simple_user_bots(self) -> List[UserMinterAndRedeemer]:
        ret = []
        for i, user_config in enumerate(self.utils.user_bots_env()):
            user_cli = self._user_cli(user_config)
            user_actor = self._get_user_actor(str(i), user_cli)
            ret.append(user_actor)
        return ret

    @property
    @cached
    def simple_user_hive(self):
        return SimpleUserHive(
            self.params,
            self.ripple_rpc,
            self.ripple_fund_distributer_wallet,
            self.native_chain_client,
            self.native_fund_distributor_wallet,
            self.fasset,
            self.simple_user_bots,
        )

    def _user_cli(self, env: Dict[str, str]):
        return UserCli(
            self.params.run_dir,
            self.params.config.os.python_path,
            self.params.smart_accounts_cli_path,
            self.params.fasset_name,
            env,
        )

    def _get_user_actor(self, _id: str, user_cli: UserCli):
        return UserMinterAndRedeemer(
            _id,
            self.params,
            self.utils,
            self.ripple_rpc,
            self.fasset,
            self.master_account_controller,
            user_cli,
        )
