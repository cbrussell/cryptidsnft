from brownie import Cryptids, accounts, network, config
import time

# Set merkle root
# Required to change stages

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = Cryptids[len(Cryptids)-1]
    merkle_root = '0x4ee7e82476a1529e3271f56efaa2b7d045c2181d0a8da328a44dfb37e3957b2f'
    transaction = cryptids.setMerkleRoot(merkle_root, {"from": dev})
    print(f'Merkle root set at: {transaction}\n')
    print(f'Merkle root set to: {merkle_root}\n')

    print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}\n')


# brownie run scripts/deployment/4_set_merkle_root.py --network arbitrum-main