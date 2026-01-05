from random import randint
from qa_lib.utils import logger
from .._user_base import BaseUserBot


MIN_MINTED_LOTS = 1

class UserMinterAndRedeemer(BaseUserBot):

    def mint(self, max_minted_lots: int, agent_vault: int = 0):
        xrp_balance = self.ripple.get_balance(self.address)
        xrp_balance_lots = self.utils.uba_to_lots(xrp_balance)
        if xrp_balance_lots > MIN_MINTED_LOTS:
            mint_lots = self.get_mint_amount(xrp_balance_lots, max_minted_lots)
            logger.info(
                f"user {self.id} with balance {xrp_balance_lots} lots minting {mint_lots} lots of {self.fassetn}"
            )
            resp = self.cli.mint(mint_lots, agent_vault)
            logger.info(f"user {self.id} minted with transaction {resp.transaction}")
        else:
            logger.info(
                f"user {self.id} skipped minting due to insufficient balance of {xrp_balance} {self.assetn}"
            )

    def redeem_all(self):
        fxrp_balance = self.fasset.balance_of(self.personal_address)
        fxrp_balance_lots = self.utils.uba_to_lots(fxrp_balance)
        if fxrp_balance_lots > 0:
            logger.info( f"user {self.id} redeeming {fxrp_balance_lots} {self.fassetn} lots of {self.fassetn}")
            resp = self.cli.redeem(fxrp_balance_lots)
            logger.info(f"user {self.id} requested redemption via {resp.transaction}")
        else:
            logger.info(
                f"user {self.id} skipped redeeming due to insufficient balance of {fxrp_balance} {self.fassetn}"
            )

    def get_mint_amount(self, balance_lots: int, cap_lots: int):
        return randint(MIN_MINTED_LOTS, min(balance_lots - 1, cap_lots))

    @property
    def fassetn(self):
        return self.params.config.chain.fasset_name

    @property
    def assetn(self):
        return self.params.config.chain.asset_name
