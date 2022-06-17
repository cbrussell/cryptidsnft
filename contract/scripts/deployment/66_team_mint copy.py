from brownie import Cryptids, accounts, network, config
import time

# Airdrop token to user

def main():
    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()

    print(f'Ruinnng functions as dev: {dev}\n')
    print(f'Active network is: {active_network}\n')
    
    cryptids = Cryptids[len(Cryptids)-1]
    amount = 77

    transaction = cryptids.teamMint(amount, {"from": dev})
    time.sleep(3)
    balance = cryptids.teamMintCount()
    owner = cryptids.owner()
    print(f'Team mint sent at: {transaction}\n')
    print(f"Airdropped {amount} Cryptids to owner: {owner}! Team Mint balance is now: {balance}.\n")




    print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}\n')