from brownie import Cryptids, accounts, network, config
import time

# Changes stage

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    print(dev.balance())
    cryptids = Cryptids[len(Cryptids)-1]
    print(cryptids)
    stage = 4
    transaction = cryptids.setStage(stage, {"from": dev})
    
    print(f'Success! Stage moved to {transaction}')

    print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}\n')

