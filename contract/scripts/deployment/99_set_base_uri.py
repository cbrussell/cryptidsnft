from brownie import CryptidToken, accounts, network, config

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = CryptidToken[len(CryptidToken)-1]
    print(cryptids)
    base_uri = "ipfs://QmTfi1WyXvcqybRaeVcLLxyTeQWcaFtkmHEaEPDQQLjR8N" + "/"
    transaction = cryptids.setBaseURI(base_uri, {"from": dev})
    print(f'BaseURI set on: {transaction}')
    print(f'BaseURI set to: {base_uri}')



# QmRieeT9iBqzrzESYC2V94FNdpeS8adSMLA8CDcoQLH1eW

