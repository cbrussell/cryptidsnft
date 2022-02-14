from brownie import CryptidToken, accounts, network, config
import time

# Set merkle root
# Required to change stages

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = CryptidToken[len(CryptidToken)-1]
    merkle_root = '0x2d995a0eb40245f7900dda563d10b2dd562d4da8a2cb847ca73cbf8bf1c96b7c'
    transaction = cryptids.setMerkleRoot(merkle_root, {"from": dev})
    print(f'Merkle root set at: {transaction}\n')
    print(f'Merkle root set to: {merkle_root}\n')

    print(f'See transaction here: https://rinkeby.etherscan.io/tx/{transaction.txid}\n')


