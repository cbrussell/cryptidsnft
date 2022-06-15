from brownie import Cryptids, accounts, network, config

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(dev)
    cryptids = Cryptids[len(Cryptids)-1]
    print(cryptids)

    contract = '0xE0d972817e94c5FF9BDc49a63d8927A0bA833E4f'
    
    # transaction = cryptids.setClaim(address, 0, {"from": dev})

    # total_supply = cryptids.totalSupply()
    # print(total_supply)

    holder_file = open("holders_smol_domain.txt", "w")

    addresses = []
    for token in range(0, 2876)[::-1]:
        address = contract.ownerOf(token)
        print(address)
        holder_file.write(address + "\n")
  
    
    # print(f'Claim for {address} removed on: {transaction}')

    # print(f'See transaction here: https://arbiscan.io/tx/{transaction.txid}')