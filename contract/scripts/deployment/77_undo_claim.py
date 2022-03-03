from brownie import CryptidToken, accounts, network, config

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = CryptidToken[len(CryptidToken)-1]
    print(cryptids)
    address = "0x3668FfF9416fadE4831D2136cba30e74557E2198"
    transaction = cryptids.undoClaim(address, {"from": dev})
    
    print(f'Claim for {address} removed on: {transaction}')

    print(f'See transaction here: https://rinkeby.etherscan.io/tx/{transaction.txid}')