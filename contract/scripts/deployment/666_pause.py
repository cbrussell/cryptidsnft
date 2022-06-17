from brownie import Cryptids, accounts, network, config
import time

# Airdrop token to user

def main():
    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()

    print(f'Ruinnng functions as dev: {dev}\n')
    print(f'Active network is: {active_network}\n')
    
    cryptids = Cryptids[len(Cryptids)-1]
  

    transaction = cryptids.pause({"from": dev})
    time.sleep(3)
    is_paused = cryptids.paused()

    print(f'Pause transaction sent on: {transaction}\n')
    print(f"Paused status is {is_paused}.\n")




    print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}\n')