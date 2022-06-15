from brownie import Cryptids, accounts, network, config

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = Cryptids[len(Cryptids)-1]
    print(cryptids)
    
    # transaction = cryptids.setClaim(address, 0, {"from": dev})

    total_supply = cryptids.totalSupply()

    holder_file = open("holders.txt", "w")

    addresses = []
    for token in range(1,total_supply): 
        address = cryptids.ownerOf(token)
        print(address)
        holder_file.write(address + "\n")
  
    
    # print(f'Claim for {address} removed on: {transaction}')

    # print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}')