from brownie import CryptidToken, accounts, network, config

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = CryptidToken[len(CryptidToken)-1]
    print(cryptids)
    presaleUsers = ["0x12B58f5331a6DC897932AA7FB5101667ACdf03e2"]
    transaction = cryptids.setPresaleUsers(presaleUsers, {"from": dev})
    print(f'Presale users set on: {transaction}')