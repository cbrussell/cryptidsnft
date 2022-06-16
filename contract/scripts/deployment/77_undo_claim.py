from brownie import Cryptids, accounts, network, config

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = Cryptids[len(Cryptids)-1]
    print(cryptids)

    addresses = ['0x0C9607aE48bC0BA55Da3312D4498297262b1d3c3']


    for address in addresses:

        transaction = cryptids.setClaim(address, 0, {"from": dev})

        claimed_amount = cryptids.claimed(address)

        print(f'Claim for {address} removed on: {transaction}.\n')

                

        print(f"Claimed amount for {address} is now {claimed_amount}.\n")

        print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}')