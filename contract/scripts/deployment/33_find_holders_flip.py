from brownie import Contract, accounts, network, config

def main():

    flip = Contract.from_explorer("0x31d2678ed8ea62fc63d5ecff713920f75167d062")



    total_supply = flip.totalSupply()
    print(total_supply)

    holder_file = open("holders_flip_domain_final_2.txt", "w")

    addresses = []
    for token in range(1, total_supply+1)[::-1]:
        address = flip.ownerOf(token)
        print(address)
        holder_file.write(address + "\n")
  