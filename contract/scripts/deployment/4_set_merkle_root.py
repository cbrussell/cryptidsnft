from brownie import Cryptids, accounts, network, config
import time

# Set merkle root
# Required to change stages

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = Cryptids[len(Cryptids)-1]
    merkle_root = '0x9547bf9c82f8622d5d2b85368bd947823d22f4a516596f229829ac9ae7ce234f'
    transaction = cryptids.setMerkleRoot(merkle_root, {"from": dev})
    print(f'Merkle root set at: {transaction}\n')
    print(f'Merkle root set to: {merkle_root}\n')

    print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}\n')


# brownie run scripts/deployment/4_set_merkle_root.py --network arbitrum-main