from brownie import Cryptids, accounts, network, config

# to update environment variables, use: touch ~/.bash_profile; open ~/.bash_profile
# type 'printenv' or 'evn' in terminal to see all local environment variables

def main():

    dev = accounts.add(config['wallets']['from_key'])
    active_network = network.show_active()

    print(f'Ruinnng functions as dev: {dev}')
    print(f'Active network is: {active_network}')
    
    # network.gas_limit(80000000)
    cryptids = Cryptids.deploy(
        "Cryptids",         # name
        "CRYPTID",         # symbol
        "",             # base
        777,             # team supply
        7777,             # total supply
        {"from": dev},  # 129729334, 139723666 for arb, add:  "gas_limit": 80000000000, "allow_revert": True
        publish_source=True,
    )

    print(f'Success! Contract deployed at {cryptids}')

    return cryptids

    # brownie run scripts/deployment/1_deploy_test_arb_rinkeby.py --network arb-test