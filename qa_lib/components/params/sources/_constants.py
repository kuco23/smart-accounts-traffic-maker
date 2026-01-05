from os import getcwd
from pathlib import Path

class Constants:

    @property
    def run_dir(self) -> str:
        return str(Path(getcwd()) / 'smart_accounts_cli')

    @property
    def smart_accounts_cli_path(self) -> str:
        return "./smart_accounts.py"
