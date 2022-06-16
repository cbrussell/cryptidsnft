from brownie import Contract, accounts, network, config

def main():

    smolbrains = Contract.from_explorer("0x17DaCAD7975960833f374622fad08b90Ed67D1B5")
    


    total_supply = smolbrains.totalSupply()
    print(total_supply)

    holder_file = open("holders_smol_bodies.txt", "w")

    addresses = []
    for token in range(total_supply):
        try:
            address = smolbrains.ownerOf(token)
            print(address)
            holder_file.write(address + "\n")
        except:
            print(f"nonexistant token for ID# {token}")
            continue

    # brownie run scripts/deployment/33_find_holders_smol_brains.py --network arbitrum-main
  
    