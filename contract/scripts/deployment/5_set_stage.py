from brownie import CryptidToken, accounts, network, config
import time

# Changes stage

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    print(dev.balance())
    cryptids = CryptidToken[len(CryptidToken)-1]
    print(cryptids)
    stage = 0
    transaction = cryptids.setStage(stage, {"from": dev})
    
    print(f'Success! Stage moved at {transaction}')

    print(f'See transaction here: https://rinkeby.etherscan.io/tx/{transaction.txid}\n')

