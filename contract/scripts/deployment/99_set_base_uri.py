from brownie import Cryptids, accounts, network, config

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = Cryptids[len(Cryptids)-1]
    print(cryptids)
    base_uri = "ipfs://QmSA6jdQbyswLgXiYRocR53TENZtL1bBDnpnNNtLs48Bsc" + "/"
    transaction = cryptids.setBaseURI(base_uri, {"from": dev})

    print(f'BaseURI set on: {transaction}')
    print(f'BaseURI set to: {base_uri}')

    print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}')

# QmRieeT9iBqzrzESYC2V94FNdpeS8adSMLA8CDcoQLH1eW

