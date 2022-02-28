from brownie import CryptidToken, accounts, network, config
import time

# Set merkle root
# Required to change stages

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = CryptidToken[len(CryptidToken)-1]
    merkle_root = '0xade69b399bb576615cbb16ca0ad0e17b4b55c5fdf9a8037c0bdee954ae39dc72'
    transaction = cryptids.setMerkleRoot(merkle_root, {"from": dev})
    print(f'Merkle root set at: {transaction}\n')
    print(f'Merkle root set to: {merkle_root}\n')

    print(f'See transaction here: https://rinkeby.etherscan.io/tx/{transaction.txid}\n')


