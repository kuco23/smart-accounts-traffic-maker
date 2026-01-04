from os import getcwd
from pathlib import Path

class Constants:

    @property
    def run_dir(self) -> str:
        return str(Path(getcwd()) / 'smart_accounts_cli')

    @property
    def smart_accounts_cli_path(self) -> str:
        return "./smart_accounts.py"

    ##########################################################
    # should be configured dynamicaly

    @property
    def native_token_name(self) -> str:
        return "C2FLR"

    @property
    def fasset_name(self) -> str:
        return "FTestXRP"

    @property
    def asset_manager_name(self) -> str:
        return "AssetManager_FTestXRP"

    @property
    def asset_name(self) -> str:
        return "testXRP"

    @property
    def lot_size(self) -> int:
        return 10000000

    @property
    def token_decimals(self) -> int:
        return 6

    @property
    def core_vault_min_redeem_lots(self) -> int:
        return 10
