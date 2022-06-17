from brownie import Cryptids, accounts, network, config
import time

# Airdrop token to user

def main():
    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()

    print(f'Ruinnng functions as dev: {dev}')
    print(f'Active network is: {active_network}')

    addresses = ['0x1e9A330D6C972Cabb05eE9Aa020b09EC128764E8']



    cryptids = Cryptids[len(Cryptids)-1]
    airdrop_amount = 1
    airdrop_address = "0x27cc5B44FC727f216cdb8a0844Fa433a6117DB87"

    for address in addresses:
        transaction = cryptids.airdropCryptid(airdrop_amount, address, {"from": dev})
        time.sleep(3)
        balance = cryptids.balanceOf(address)

        print(f"Airdropped {airdrop_amount} Cryptids to {address} on transaction: {transaction}! Address balance is now: {balance}.")

        #brownie run scripts/deployment/55_airdrop.py --network arbitrum-main 