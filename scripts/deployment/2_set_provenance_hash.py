from brownie import CryptidToken, accounts, network, config
import time

# Set provenance hash. 
# Required to move to stage 1

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = CryptidToken[len(CryptidToken)-1]
    provenance = 'string to be entered here'
    transaction = cryptids.setProvenanceHash(provenance, {"from": dev})
    print(f'Provenance hash set at: {transaction}')
    provenancehash = cryptids.provenanceHash()
    print(f'Provenance hash set to: {provenance}')

