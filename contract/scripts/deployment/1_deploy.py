from brownie import CryptidToken, accounts, network, config

# to update environment variables, use: touch ~/.bash_profile; open ~/.bash_profile
# type 'printenv' or 'evn' in terminal to see all local environment variables

def main():

    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()

    print(f'Ruinnng functions as dev: {dev}')
    print(f'Active network is: {active_network}')
    
    # network.gas_limit(80000000)
    cryptids = CryptidToken.deploy(
        "test",     # name
        "test",      # symbol
        "ipfs://QmW4kLda1gmhFKnBU1qJvyCvDm8g9P4GKoiNcEB972Q9rD/",             # base
        100,           # presale supply
        100,            # team supply
        300,          # total supply
        5,              # max mint per tx
        {"from": dev},  # 129729334, 139723666 for arb, add:  "gas_limit": 80000000000, "allow_revert": True
        publish_source=True,
    )

    print(f'Success! Contract deployed at {cryptids}')

    return cryptids