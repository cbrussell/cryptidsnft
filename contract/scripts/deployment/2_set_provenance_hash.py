from brownie import Cryptids, accounts, network, config
import time

# Set provenance hash. 
# Required to move to stage 1

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = Cryptids[len(Cryptids)-1]
    provenance = '420d3b4f01ac304039c2ed49d3f61e123bab3eb2eb2c3c960da51cf23883b6d1'
    transaction = cryptids.setProvenanceHash(provenance, {"from": dev})
    print(f'Provenance hash set at: {transaction}')
    print(f'Provenance hash set to: {provenance}')

    print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}\n')

    # brownie run scripts/deployment/2_set_provenance_hash.py --network arb-test 

