from brownie import test, accounts, network, config
import time

# Freeze provenenace hash

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = test[len(test)-1]
    transaction = cryptids.freezeProvenanceHash({"from": dev})
    print(f'Provenance hash frozen at: {transaction}')

 # brownie run scripts/deployment/3_freeze_provenance_hash.py --network arb-test