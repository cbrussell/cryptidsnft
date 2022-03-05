from brownie import test, accounts, network, config
import time

# Set merkle root
# Required to change stages

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = test[len(test)-1]
    merkle_root = '0x4f2aef5b43120d851034784f3b06481a5b309896f39cd9a6a41e344c3b51467a'
    transaction = cryptids.setMerkleRoot(merkle_root, {"from": dev})
    print(f'Merkle root set at: {transaction}\n')
    print(f'Merkle root set to: {merkle_root}\n')

    print(f'See transaction here: https://testnet.arbiscan.io//tx/{transaction.txid}\n')


