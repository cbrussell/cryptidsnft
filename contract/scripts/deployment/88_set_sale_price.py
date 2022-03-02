from brownie import CryptidToken, accounts, network, config
import time

# Sets Sale Price

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    print(dev.balance())
    cryptids = CryptidToken[len(CryptidToken)-1]
    print(cryptids)
    salePrice = '0.1 ether'
    transaction = cryptids.setSalePrice(salePrice, {"from": dev})
    
    print(f'Success! Sale Price to set {salePrice} at {transaction}')

    print(f'See transaction here: https://rinkeby.etherscan.io/tx/{transaction.txid}\n')

