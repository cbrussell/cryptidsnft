from brownie import test, accounts, network, config
import time

# Sets Sale Price

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    print(dev.balance())
    cryptids = test[len(test)-1]
    print(cryptids)
    maxTx = 100
    transaction = cryptids.setMaxMintPerTx(maxTx, {"from": dev})
    
    print(f'Success! Max Mint pet Transaction set to {maxTx} at {transaction}')

    print(f'See transaction here: https://testnet.arbiscan.io//tx/{transaction.txid}\n')

