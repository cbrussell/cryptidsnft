from brownie import Cryptids, accounts, network, config
import time

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = Cryptids[len(Cryptids)-1]
    print(cryptids)

    addresses = ['0xbe2CD4dee97a857FC5b43075eb9103b364eD5C95']


    for address in addresses:

        pre_claimed_amount = cryptids.claimed(address)

        print(f"Account {address} has claimed {pre_claimed_amount} Cryptids.\n")

        transaction = cryptids.setClaim(address, 0, {"from": dev})
        time.sleep(3)
        claimed_amount = cryptids.claimed(address)

        print(f'Claim for {address} removed on: {transaction}.\n')

                

        print(f"Claimed amount for {address} is now {claimed_amount}.\n")

        print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}')