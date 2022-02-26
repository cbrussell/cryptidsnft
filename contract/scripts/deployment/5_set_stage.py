from brownie import CryptidToken, accounts, network, config
import time

# Moves Cryptid contract to next stage


    # ~ Sale stages ~
    # stage 0: Init
    # stage 1: Airdrop
    # stage 2: Whitelist
    # stage 3: Team Mint 
    # stage 4: Public Sale


def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    print(dev.balance())
    cryptids = CryptidToken[len(CryptidToken)-1]
    print(cryptids)
    stage = 2
    transaction = cryptids.setStage(stage, {"from": dev})
    
    print(f'Success! Stage moved at {transaction}')

    print(f'See transaction here: https://rinkeby.etherscan.io/tx/{transaction.txid}\n')

