from brownie import test, accounts, network, config
import time

# Set merkle root
# Required to change stages

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = test[len(test)-1]
    merkle_root = '0xb64956e4be375dd9a85c71ca10c83d78775a9e2b2c0cadbc72b6cbe3e8a3e302'
    transaction = cryptids.setMerkleRoot(merkle_root, {"from": dev})
    print(f'Merkle root set at: {transaction}\n')
    print(f'Merkle root set to: {merkle_root}\n')

    print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}\n')


