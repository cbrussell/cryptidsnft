from brownie import test, accounts, network, config

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = test[len(test)-1]
    print(cryptids)
    address = "0x12B58f5331a6DC897932AA7FB5101667ACdf03e2"
    transaction = cryptids.undoClaim(address, {"from": dev})
    
    print(f'Claim for {address} removed on: {transaction}')

    print(f'See transaction here: https://testnet.arbiscan.io//tx/{transaction.txid}')