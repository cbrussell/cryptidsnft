from brownie import CryptidToken, accounts, network, config
import time

# Moves Cryptid contract to next stage

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    print(dev.balance())
    cryptids = CryptidToken[len(CryptidToken)-1]
    print(cryptids)
    transaction = cryptids.nextStage({"from": dev})
    print(f'Success! Stage moved at {transaction}')

