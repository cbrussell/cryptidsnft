from brownie import CryptidToken, accounts, network, config

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = CryptidToken[len(CryptidToken)-1]
    print(cryptids)
    whitelistUsers = ["0xB2aa6e21ED6B1307Dd5467Ce191a984285957ba1"]
    whitelistMints = [100]
    transaction = cryptids.setWhitelistUsers(whitelistUsers, whitelistMints, {"from": dev})
    
    print(f'whitelistUsers set on: {transaction}')

    print(f'See transaction here: https://testnet.arbiscan.io//tx/{transaction.txid}')