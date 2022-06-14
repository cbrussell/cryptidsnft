from brownie import Cryptids, accounts, network, config
import time

# Airdrop token to user

def main():
    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()

    print(f'Ruinnng functions as dev: {dev}')
    print(f'Active network is: {active_network}')

    addresses = [
'0x27f8712689de87b9f1de1d7ee0f9622c299d8ed4',
'0x4F2a53034185E5F676450D6a236e73Efe230FD4B',
'0xa956DD448DfD87f2BC2453Aa3aC5b2eaEe2e77Ca',
'0x22a6aADD4e084576022273c7ecc939a996Ff3657',
'0x32F5Bc8b89a183cB82171d5DBabABaeF1b0FA0e9']

    
    cryptids = Cryptids[len(Cryptids)-1]
    airdrop_amount = 1
    airdrop_address = "0xFf634F9ED1005198F3Ae614328d2274c97e97B56"

    for address in addresses:
        transaction = cryptids.airdropCryptid(airdrop_amount, address, {"from": dev})

        balance = cryptids.balanceOf(address)

        print(f"Airdropped {airdrop_amount} Cryptids to {address} on transaction: {transaction}! Address balance is now: {balance}.")