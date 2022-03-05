from brownie import test, accounts, network, config
import time

# Changes stage

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    print(dev.balance())
    cryptids = test[len(test)-1]
    print(cryptids)
    stage = 4
    transaction = cryptids.setStage(stage, {"from": dev})
    
    print(f'Success! Stage moved toat {transaction}')

    print(f'See transaction here: https://testnet.arbiscan.io//tx/{transaction.txid}\n')

