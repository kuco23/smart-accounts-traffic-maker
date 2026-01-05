from typing import List
from time import sleep
from random import choice
from attrs import frozen
import traceback
from qa_lib.utils import logger
from qa_lib.components.params import ParamLoader
from qa_lib.components.chain import (
    RippleWallet,
    RippleClient,
    NativeClient,
    FAsset,
)
from ..standalone import UserMinterAndRedeemer


MAX_MINTED_LOTS = 4
XRP_DROP_FACTOR = 10**6
NAT_WEI_FACTOR = 10**18
CYCLE_SLEEP_SEC = 10

@frozen
class SimpleUserHive:
    params: ParamLoader
    ripple_rpc: RippleClient
    ripple_root: RippleWallet
    native_rpc: NativeClient
    fasset: FAsset
    users: List[UserMinterAndRedeemer]

    def fund(self):
        root_xrp_balance = self.ripple_rpc.get_balance(self.ripple_root.wallet.address)

        xrp_target = self.params.config.load_test.user_target_xrp_balance * XRP_DROP_FACTOR
        assert root_xrp_balance > xrp_target * len(self.users), (
            "distributor has too little XRP balance"
        )

        xrp_min = self.params.config.load_test.user_min_xrp_balance * XRP_DROP_FACTOR

        for user in self.users:
            user_xrp_balance = self.ripple_rpc.get_balance(user.address)
            user_fxrp_balance = self.fasset.balance_of(user.personal_address)
            if user_xrp_balance <= xrp_min and user_fxrp_balance <= xrp_min:
                fund = xrp_target - user_xrp_balance
                logger.info(
                    f"funding user {user.id} with {fund} {user.utils.assetn}"
                )
                self.ripple_root.send_tx(
                    xrp_target - user_xrp_balance, user.address
                )
                logger.info(
                    f"successfully funded user {user.id} with {fund} {user.utils.assetn}"
                )

    def run_thread(self, i: int):
        while True:
            try:
                self.run_user_step(i)
            except Exception as e:
                logger.error(f"error when running user {i}:", e, traceback.format_exc())
            sleep(CYCLE_SLEEP_SEC)

    def run_user_step(self, i: int):
        user = self.users[i]
        user.mint(MAX_MINTED_LOTS, self.pick_agent())
        user.redeem_all()

    def pick_agent(self):
        return choice(self.params.config.load_test.agent_vault_indices)

    def on_finish(self):
        for user in self.users:
            user.redeem_all()
