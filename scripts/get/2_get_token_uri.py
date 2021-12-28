from brownie import CryptidToken, accounts, config, network
import time

# Check stage of CryptidToken contract
tokenId = 1

def main():
    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()
    print(f'Ruinnng functions as dev: {dev}')
    print(f'Active network is: {active_network}')
    cryptids = CryptidToken[len(CryptidToken)-1]
    tokenURI = cryptids.tokenURI(tokenId)
    print(f'Current tokenURI for {tokenId} is: {tokenURI }') 