from brownie import CryptidToken, accounts, network, config
import time

# Set merkle root
# Required to change stages

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = CryptidToken[len(CryptidToken)-1]
    merkle_root = '0xe0e7340c3136d7eaf5d68b66ba92650a96de5d45d728047d3174f3e59901c338'
    transaction = cryptids.setMerkleRoot(merkle_root, {"from": dev})
    print(f'Merkle root set at: {transaction}\n')
    print(f'Merkle root set to: {merkle_root}\n')

    print(f'See transaction here: https://rinkeby.etherscan.io/tx/{transaction.txid}\n')


