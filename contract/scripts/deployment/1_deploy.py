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
        "Cryptids",     # name
        "CRYPTID",      # symbol
        "ipfs://QmUDYY47FW4DH5aCLPgy4EnZmCEAtuwdAvtNfhkiN77Bkg",             # defaulturi
        3000,           # presale supply
        500,            # team supply
        10000,          # total supply
        5,              # max mint per tx
        {"from": dev},  # 129729334, 139723666 for arb, add:  "gas_limit": 80000000000, "allow_revert": True
        publish_source=True,
    )
    return cryptids