from brownie import Cryptids, accounts, network, config

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = Cryptids[len(Cryptids)-1]
    print(cryptids)

    addresses = ['0x07A4c60c6CcDf6Ff3EA28Bbe8D0C21D6D1260ceD']


    for address in addresses:

        transaction = cryptids.setClaim(address, 0, {"from": dev})

        claimed_amount = cryptids.claimed(address)

        print(f'Claim for {address} removed on: {transaction}.\n')

                

        print(f"Claimed amount for {address} is now {claimed_amount}.\n")

        print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}')