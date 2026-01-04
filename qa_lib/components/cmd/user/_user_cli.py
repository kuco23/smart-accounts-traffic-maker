from typing import List
from .._cmd import Cmd
from ._user_cli_parser import UserCliOutputParser


class UserCli(Cmd, UserCliOutputParser):

    def __init__(
        self,
        run_dir: str,
        node_path: str,
        executable: str,
        fasset: str,
        env: dict[str, str],
    ):
        super().__init__(run_dir, env)
        self.node_path = node_path
        self.executable = executable
        self.fasset = fasset

    def mint(self, lots: int, agent_vault: int = 0):
        collateral_reserved = self.reserve_collateral(lots, agent_vault)
        cli_args = self._bridge_mint_args(collateral_reserved.transaction)
        raw_resp = self._run(cli_args)
        resp = self.parse_bridge_mint_response(raw_resp)
        return self._ensure_parser_response(resp)

    def reserve_collateral(self, lots: int, agent_vault: int = 0):
        instruction = self._encode_reserve_collateral(lots, agent_vault)
        return self._bridge_instruction(instruction.encoding)

    def transfer(self, amount: int):
        instruction = self._encode_transfer(amount)
        return self._bridge_instruction(instruction.encoding)

    def redeem(self, lots: int):
        instruction = self._encode_redeem(lots)
        return self._bridge_instruction(instruction.encoding)

    def _encode_reserve_collateral(self, lots: int, agent_vault: int = 0):
        cli_args = self._encode_collateral_reserved_args(lots, agent_vault)
        return self._encode(cli_args)

    def _encode_redeem(self, lots: int):
        cli_args = self._encode_redeem_args(lots)
        return self._encode(cli_args)

    def _encode_transfer(self, amount: int):
        cli_args = self._encode_transfer_args(amount)
        return self._encode(cli_args)

    def _encode(self, cli_args: List[str]):
        raw_resp = self._run(cli_args)
        resp = self.parse_encoding_response(raw_resp)
        return self._ensure_parser_response(resp)

    def _bridge_instruction(self, instruction: str):
        cli_args = self._bridge_instruction_args(instruction)
        raw_resp = self._run(cli_args)
        resp = self.parse_bridge_instruction_response(raw_resp)
        return self._ensure_parser_response(resp)

    def _run(self, commands: List[str]):
        return super()._run(self.node_path, self.executable, commands)

    @staticmethod
    def _bridge_instruction_args(instruction: str):
        return ["bridge", "instruction", instruction]

    @staticmethod
    def _encode_collateral_reserved_args(lots: int, agent_vault: int = 0):
        return ["encode", "fxrp-cr", "-w", "0", "-v", str(lots), "-a", str(agent_vault)]

    @staticmethod
    def _encode_redeem_args(lots: int):
        return ["encode", "fxrp-redeem", "-w", "0", "-v", str(lots)]

    @staticmethod
    def _encode_transfer_args(amount: int):
        return ["encode", "fxrp-transfer", "-w", "0", "-v", str(amount)]

    @staticmethod
    def _bridge_mint_args(transaction: str):
        return ["bridge", "mint-tx", transaction, "-w"]