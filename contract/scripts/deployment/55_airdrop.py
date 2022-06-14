from brownie import Cryptids, accounts, network, config
import time

# Airdrop token to user

def main():
    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()

    print(f'Ruinnng functions as dev: {dev}')
    print(f'Active network is: {active_network}')

    addresses = ['0xB5BBeB36b38D025f6dfb7D3f7458fF5BeE89058D']


    
    cryptids = Cryptids[len(Cryptids)-1]
    airdrop_amount = 1
    airdrop_address = "0xFf634F9ED1005198F3Ae614328d2274c97e97B56"

    for address in addresses:
        transaction = cryptids.airdropCryptid(airdrop_amount, address, {"from": dev})

        balance = cryptids.balanceOf(address)

        print(f"Airdropped {airdrop_amount} Cryptids to {address} on transaction: {transaction}! Address balance is now: {balance}.")