from toml import load
from pydantic.dataclasses import dataclass
from dacite import from_dict


@dataclass
class OsConfig:
    python_path: str

@dataclass
class ContractConfig:
    fasset_address: str
    fasset_abi_path: str
    master_account_controller_abi_path: str
    master_account_controller_address: str

@dataclass
class ChainConfig:
    native_token_name: str
    fasset_name: str
    asset_name: str
    lot_size: str
    fasset_decimals: str

@dataclass
class LoadTestConfig:
    user_config_path: str
    user_target_xrp_balance: int
    user_min_xrp_balance: int

@dataclass
class Config:
    os: OsConfig
    contracts: ContractConfig
    chain: ChainConfig
    load_test: LoadTestConfig

    @classmethod
    def create(cls, config_path: str):
        return from_dict(data_class=Config, data=cls._load_config_toml(config_path))

    @staticmethod
    def _load_config_toml(config_path: str):
        with open(config_path, "r") as f:
            return load(f)
