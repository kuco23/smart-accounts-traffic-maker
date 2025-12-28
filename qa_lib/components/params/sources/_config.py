from toml import load
from pydantic.dataclasses import dataclass
from dacite import from_dict


@dataclass
class Os:
    python_path: str

@dataclass
class ConfigContracts:
    path: str
    fasset_address: str
    master_account_controller_abi_path: str
    master_account_controller_address: set

@dataclass
class ConfigLoadTest:
    user_config_path: str
    user_target_xrp_balance: int
    user_min_xrp_balance: int

@dataclass
class Config:
    os: Os
    contracts: ConfigContracts
    load_test: ConfigLoadTest

    @classmethod
    def create(cls, config_path: str):
        return from_dict(data_class=Config, data=cls._load_config_toml(config_path))

    @staticmethod
    def _load_config_toml(config_path: str):
        with open(config_path, "r") as f:
            return load(f)
