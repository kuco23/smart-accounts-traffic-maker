from qa_lib.components.cmd._cmd import Cmd

cmd = Cmd('/home/kuco23/src/smart-accounts-traffic-maker/smart_accounts_cli', dict())
print(cmd._run('./.venv/bin/python3', './smart_accounts.py', ['encode', 'fxrp-cr', '-w', '0', '-v', '3', '-a', '0']))
