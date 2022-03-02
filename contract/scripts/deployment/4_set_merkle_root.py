from brownie import CryptidToken, accounts, network, config
import time

# Set merkle root
# Required to change stages

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = CryptidToken[len(CryptidToken)-1]
    merkle_root = '0x105c11b0cfd49980c18a6f3bb8e6fb490e97bafc8e8d0e6eeb50350dc26ca13c'
    transaction = cryptids.setMerkleRoot(merkle_root, {"from": dev})
    print(f'Merkle root set at: {transaction}\n')
    print(f'Merkle root set to: {merkle_root}\n')

    print(f'See transaction here: https://rinkeby.etherscan.io/tx/{transaction.txid}\n')


