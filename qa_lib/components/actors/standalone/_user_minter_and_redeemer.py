from datetime import datetime
from time import sleep
from random import randint
from qa_lib.utils import logger
from .._user_base import BaseUserBot


MIN_MINTED_LOTS = 1
MINT_WAIT_CYCLE_SLEEP = 30

class UserMinterAndRedeemer(BaseUserBot):

    def mint(self, max_minted_lots: int, agent_vault: int):
        logger.info(f"attempting to mint with user {self.id} and agent {agent_vault}")
        xrp_balance = self.ripple.get_balance(self.address)
        xrp_balance_lots = self.utils.uba_to_lots(xrp_balance)
        if xrp_balance_lots > MIN_MINTED_LOTS:
            mint_lots = self.get_mint_amount(xrp_balance_lots, max_minted_lots)
            logger.info(
                f"user {self.id} with balance {xrp_balance_lots} lots minting {mint_lots} lots of {self.utils.fassetn}"
            )
            resp = self.cli_mint(mint_lots, agent_vault)
            logger.info(f"user {self.id} minted with transaction {resp.transaction}")
        else:
            logger.info(
                f"user {self.id} skipped minting due to insufficient balance of {xrp_balance} {self.utils.assetn}"
            )

    def redeem_all(self):
        fxrp_balance = self.fasset.balance_of(self.personal_address)
        fxrp_balance_lots = self.utils.uba_to_lots(fxrp_balance)
        if fxrp_balance_lots > 0:
            logger.info( f"user {self.id} redeeming {fxrp_balance_lots} {self.utils.fassetn} lots of {self.utils.fassetn}")
            resp = self.cli.redeem(fxrp_balance_lots)
            logger.info(f"user {self.id} requested redemption via {resp.transaction}")
        else:
            logger.info(
                f"user {self.id} skipped redeeming due to insufficient balance of {fxrp_balance} {self.utils.fassetn}"
            )

    def get_mint_amount(self, balance_lots: int, cap_lots: int):
        return randint(MIN_MINTED_LOTS, min(balance_lots - 1, cap_lots))

    def cli_mint(self, lots: int, agent_vault: int):
        collateral_reserved = self.cli.reserve_collateral(lots, agent_vault)
        # retry
        initial = datetime.now().timestamp()
        last = 0
        while last < initial + self.params.config.load_test.operator_wait_time:
            sleep(MINT_WAIT_CYCLE_SLEEP)
            last = datetime.now().timestamp()
            try:
                return self.cli.mint(collateral_reserved.transaction)
            except Exception as e:
                if self.cli.collateral_reservation_not_found(str(e)):
                    break
                logger.warning(f'collateral reservation not yet found')
        raise Exception(f'mint for {lots} lots failed')

