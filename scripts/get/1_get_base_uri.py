from brownie import CryptidToken, accounts, config, network
import time

# Check stage of CryptidToken contract

def main():
    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()
    print(f'Ruinnng functions as dev: {dev}')
    print(f'Active network is: {active_network}')
    cryptids = CryptidToken[len(CryptidToken)-1]
    base_uri = cryptids.baseURI()
    print(f'Current baseURI is: {base_uri}') 