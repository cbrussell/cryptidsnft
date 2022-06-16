from brownie import Contract, accounts, network, config

def main():

    smolbrains = Contract.from_explorer("0x6325439389E0797Ab35752B4F43a14C004f22A9c")
    


    total_supply = smolbrains.totalSupply()
    print(total_supply)

    holder_file = open("holders_smol_brains_3.txt", "w")

    addresses = []
    for token in range(6171, total_supply):
        try:
            address = smolbrains.ownerOf(token)
            print(address)
            holder_file.write(address + "\n")
        except:
            print(f"nonexistant token for ID# {token}")
            continue

    # brownie run scripts/deployment/33_find_holders_smol_brains.py --network arbitrum-main
  
    