from brownie import CryptidToken, accounts, network, config
import time

# Airdrop token to user

def main():
    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()

    print(f'Ruinnng functions as dev: {dev}')
    print(f'Active network is: {active_network}')
    
    cryptids = CryptidToken[len(CryptidToken)-1]
    airdrop_amount = 5
    airdrop_address = "0xB2aa6e21ED6B1307Dd5467Ce191a984285957ba1"

    transaction = cryptids.airdropCryptid(airdrop_amount, airdrop_address, {"from": dev})