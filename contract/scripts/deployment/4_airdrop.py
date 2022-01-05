from brownie import CryptidToken, accounts, network, config
import time

# Airdrop token to user

def main():
    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()

    print(f'Ruinnng functions as dev: {dev}')
    print(f'Active network is: {active_network}')
    
    cryptids = CryptidToken[len(CryptidToken)-1]
    airdrop_amount = 3
    airdrop_address = "0x1953bc1fF76f5e61cD775A4482bd85BAc56aD1Eb"
    # "0x1953bc1fF76f5e61cD775A4482bd85BAc56aD1Eb"

    transaction = cryptids.airdropCryptid(airdrop_amount, airdrop_address, {"from": dev})

    balance = cryptids.balanceOf(airdrop_address)

    print(f"Airdropped {airdrop_amount} Cryptids to {airdrop_address}! Address balance is now: {balance}.")