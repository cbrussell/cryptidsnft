from brownie import Cryptids, accounts, network, config
import time

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = Cryptids[len(Cryptids)-1]
    print(cryptids)

    addresses = ['0xfdFe0847CD314D7c3855A6F19D83E92355Cd4E8a']


    for address in addresses:

        transaction = cryptids.setClaim(address, 0, {"from": dev})
        time.sleep(3)
        claimed_amount = cryptids.claimed(address)

        print(f'Claim for {address} removed on: {transaction}.\n')

                

        print(f"Claimed amount for {address} is now {claimed_amount}.\n")

        print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}')