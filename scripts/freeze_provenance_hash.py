from brownie import CryptidToken, accounts, network, config
import time

# Freeze provenenace hash

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = CryptidToken[len(CryptidToken)-1]
    transaction = cryptids.freezeProvenanceHash({"from": dev})
    print(f'Provenance hash frozen at: {transaction}')

