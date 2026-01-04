from json import load
from .sources import Constants, Config, Env
from ...utils import cached

from os import getcwd


"""
Abstraction over low level parameter fetching,
adding some transformers and utilities.
"""


class ParamLoader(Env, Constants):
    config: Config

    def __init__(self):
        self.config = Config.create(self.config_path)

    @property
    @cached
    def _master_account_controller_abi(self):
        return load(open(self.config.contracts.master_account_controller_abi_path, "r"))["abi"]

    @property
    @cached
    def _fasset_abi(self):
        return load(open(self.config.contracts.fasset_abi_path, "r"))["abi"]
