from brownie import Contract, accounts, network, config

def main():

    smolbrains = Contract.from_explorer("0x1f245E83fB88A1e85b4A1c3e4B3c16660d54319a")
    


    total_supply = smolbrains.totalSupply()
    print(total_supply)

    holder_file = open("holders_smol_brains_wrapped.txt", "w")

    addresses = []
    for token in range(total_supply):
        try:

            address = smolbrains.ownerOf(token)
            print(address)
            holder_file.write(address + "\n")
        except:
            print(f'no wrapped token found for smol #{token}')
            continue

    # brownie run scripts/deployment/33_find_holders_smol_brains.py --network arbitrum-main
  
    