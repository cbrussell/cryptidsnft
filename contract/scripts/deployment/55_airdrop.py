from brownie import test, accounts, network, config
import time

# Airdrop token to user

def main():
    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()

    print(f'Ruinnng functions as dev: {dev}')
    print(f'Active network is: {active_network}')
    
    cryptids = test[len(test)-1]
    airdrop_amount = 2
    airdrop_address = "0x12B58f5331a6DC897932AA7FB5101667ACdf03e2"

    transaction = cryptids.airdropTest(airdrop_amount, airdrop_address, {"from": dev})

    balance = cryptids.balanceOf(airdrop_address)

    print(f"Airdropped {airdrop_amount} Cryptids to {airdrop_address} on transaction: {transaction}! Address balance is now: {balance}.")