from brownie import test, accounts, network, config
import time

# Set provenance hash. 
# Required to move to stage 1

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = test[len(test)-1]
    provenance = '13ecf85915c0c913cf660cc6250a126d09e4bf6cab0ed016719056ca5b40544c'
    transaction = cryptids.setProvenanceHash(provenance, {"from": dev})
    print(f'Provenance hash set at: {transaction}')
    print(f'Provenance hash set to: {provenance}')

    print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}\n')

    # brownie run scripts/deployment/2_set_provenance_hash.py --network arb-test 

