from brownie import test, accounts, network, config
import time

# Sets Sale Price

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    print(dev.balance())
    cryptids = test[len(test)-1]
    print(cryptids)
    salePrice = '0.1 ether'
    transaction = cryptids.setSalePrice(salePrice, {"from": dev})
    
    print(f'Success! Sale Price to set {salePrice} at {transaction}')

    print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}\n')

