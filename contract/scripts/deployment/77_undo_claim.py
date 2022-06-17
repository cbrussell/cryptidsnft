from brownie import Cryptids, accounts, network, config
import time

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = Cryptids[len(Cryptids)-1]
    print(cryptids)

    addresses = ['0xca8EAE37FC023EfE7728f0a0a4e20e627e9D3b63']


    for address in addresses:

        transaction = cryptids.setClaim(address, 0, {"from": dev})
        time.sleep(3)
        claimed_amount = cryptids.claimed(address)

        print(f'Claim for {address} removed on: {transaction}.\n')

                

        print(f"Claimed amount for {address} is now {claimed_amount}.\n")

        print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}')