from brownie import test, accounts, network, config
import time

# Airdrop token to user

def main():
    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()

    print(f'Ruinnng functions as dev: {dev}\n')
    print(f'Active network is: {active_network}\n')
    
    cryptids = test[len(test)-1]
    amount = 25

    transaction = cryptids.teamMint(amount, {"from": dev})

    balance = cryptids.teamMintCount()
    owner = cryptids.owner()
    print(f'Team mint sent at: {transaction}\n')
    print(f"Airdropped {amount} Cryptids to owner: {owner}! Team Mint balance is now: {balance}.\n")




    print(f'See transaction here: https://testnet.arbiscan.io//tx/{transaction.txid}\n')