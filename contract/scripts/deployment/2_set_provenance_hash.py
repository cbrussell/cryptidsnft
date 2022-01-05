from brownie import CryptidToken, accounts, network, config
import time

# Set provenance hash. 
# Required to move to stage 1

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = CryptidToken[len(CryptidToken)-1]
    provenance = '19d40dc2c4830ac6ee83fd335d393a8fe5d7bca3d8daa54ff863920d4b0f3f8e'
    transaction = cryptids.setProvenanceHash(provenance, {"from": dev})
    print(f'Provenance hash set at: {transaction}')
    provenancehash = cryptids.provenanceHash()
    print(f'Provenance hash set to: {provenance}')

