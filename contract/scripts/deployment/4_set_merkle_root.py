from brownie import CryptidToken, accounts, network, config
import time

# Set merkle root
# Required to change stages

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = CryptidToken[len(CryptidToken)-1]
    merkle_root = '0x31c97f6351c16d614ba35d29315c47d9d1a7d47f5903535840338d7a8b241b63'
    transaction = cryptids.setMerkleRoot(merkle_root, {"from": dev})
    print(f'Merkle root set at: {transaction}\n')
    print(f'Merkle root set to: {merkle_root}\n')

    print(f'See transaction here: https://rinkeby.etherscan.io/tx/{transaction.txid}\n')


