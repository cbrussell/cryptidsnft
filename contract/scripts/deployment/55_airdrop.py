from brownie import Cryptids, accounts, network, config
import time

# Airdrop token to user

def main():
    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()

    print(f'Ruinnng functions as dev: {dev}')
    print(f'Active network is: {active_network}')

    addresses = ['0x932e9A2AFA81c365e375Ffca5349E136046bf97D',
'0xd3e32b5caa4c5b3ba83f42d24f3ac828159a8efe',
'0x913D83761Ff529f487623aB6EAdE611DDcda4790',
'0x8b1b0E98cc5B1FAE2011C2E8a7a527079c763AeC',
'0xe19558d2b3fabb5c045ddf3b44dc15de18e9cd20',
'0x1069A65F9346Bd46c2Bd741A5113a2831ffFcce5']



    cryptids = Cryptids[len(Cryptids)-1]
    airdrop_amount = 1
    airdrop_address = "0x27cc5B44FC727f216cdb8a0844Fa433a6117DB87"

    for address in addresses:
        transaction = cryptids.airdropCryptid(airdrop_amount, address, {"from": dev})

        balance = cryptids.balanceOf(address)

        print(f"Airdropped {airdrop_amount} Cryptids to {address} on transaction: {transaction}! Address balance is now: {balance}.")

        #brownie run scripts/deployment/55_airdrop.py --network arbitrum-main 