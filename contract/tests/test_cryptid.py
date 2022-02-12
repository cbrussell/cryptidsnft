import pytest
import brownie 
import hexbytes;
from brownie import CryptidToken, TestContract, ReceiverContract, NonreceiverContract, accounts, exceptions
from sqlalchemy import true;

# deploy CryptidToken
@pytest.fixture(scope="module", autouse=True)
def token():
    return accounts[0].deploy(CryptidToken, "Cryptids", "CRYPTID", "", 10, 10, 30, 5)


# revert to deployed state after each test
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

# helper function - set and freeze provenance hash
def _setFreezeProvenance(token):
    provenance = "test provenance"
    owner = accounts[0]
    token.setProvenanceHash(provenance, {'from': owner})
    token.freezeProvenanceHash({'from': owner})

# helper function - set and freeze provenance hash
def _setMerkleRoot(token):
    merkleRoot = '0x4196ced928ba4e060068ca9da2c0002ecef3f59d97ca02e0174df477bb60a3a7'
    owner = accounts[0]
    token.setMerkleRoot(merkleRoot, {'from': owner})

def _airdropStage(token):
    owner = accounts[0]
    token.setStage(1, {'from': owner})

def _whitelistStage(token):
    owner = accounts[0]
    token.setStage(2, {'from': owner})

def _teamMintStage(token):
    owner = accounts[0]
    token.setStage(3, {'from': owner})

def _mint(token):
    owner = accounts[0]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _whitelistStage(token)
    proof = ["0x33560271ea4ed1cb8a138801d47678e3894cd778efa9e9ede13b045b43d629c8","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    token.whitelistMint(proof, {'from': owner, 'value': '0.10 ether'})

def _publicSaleStage(token):
    owner = accounts[0]
    token.setStage(4, {'from': owner})

def _verifyTransferEvent(txn_receipt, _from, to, tokenID):
    event = txn_receipt.events['Transfer']
    assert(event['tokenId'] == tokenID)
    assert(event['to'] == to)
    assert(event['from'] == _from)

# Verify that an ApprovalForAll event has been logged
def _verifyApprovalForAllEvent(txn_receipt, owner, operator, approved):
    event = txn_receipt.events['ApprovalForAll']
    assert(event['owner'] == owner)
    assert(event['operator'] == operator)
    assert(event['approved'] == approved)


# Verify that an Approval event has been logged
def _verifyApprovalEvent(txn_receipt, owner, approved, tokenID):
    event = txn_receipt.events['Approval']
    assert(event['tokenId'] == tokenID)
    assert(event['owner'] == owner)
    assert(event['approved'] == approved)

# provenance has is frozen
def test_freeze_provenance_test(token):
    owner = accounts[0]
    new_provenance = "testing 1 2 3"
    token.setProvenanceHash(new_provenance, {'from': owner})
    token.freezeProvenanceHash({'from': owner})
    assert(token.provenanceHashFrozen() == True)

# freeze already frozen provnance hash
def test_freeze_already_frozen_provenance(token):
    owner = accounts[0]
    new_provenance = "test provenance hash"
    token.setProvenanceHash(new_provenance, {'from': owner})
    token.freezeProvenanceHash({'from':owner})
    with brownie.reverts("Provenance hash is already frozen."):
        token.freezeProvenanceHash({'from':owner})

# freeze provenance hash with nothing set
def test_freeze_empty_provenance(token):
    owner = accounts[0]
    new_provenance = ""
    with brownie.reverts("Provenance hash cannot be empty string."):
        token.setProvenanceHash(new_provenance, {'from': owner})

# try to set frozen provenance hash
def test_set_already_frozen_hash(token):
    owner = accounts[0]
    new_provenance = "test provenance hash"
    token.setProvenanceHash(new_provenance, {'from': owner})
    token.freezeProvenanceHash({'from':owner})
    second_provenance = "second provenance hash"
    with brownie.reverts("Provenance hash is frozen."):
        token.setProvenanceHash(second_provenance, {'from':owner})

# set provenance
def test_set_provenance(token):
    owner = accounts[0]
    new_provenance = "test provenance hash"
    token.setProvenanceHash(new_provenance, {'from': owner})
    set_provenance = token.provenanceHash()
    assert(set_provenance == new_provenance)
   
#set after frozen
def test_set_already_frozen_hash_two(token):
    owner = accounts[0]
    new_provenance = "test provenance hash"
    token.setProvenanceHash(new_provenance, {'from': owner})
    token.freezeProvenanceHash({'from':owner})
    second_provenance = "second provenance hash"
    with brownie.reverts("Provenance hash is frozen."):
        token.setProvenanceHash(second_provenance, {'from':owner})

#set after frozen
def test_freeze_empty_provenance_three(token):
    owner = accounts[0]
    with brownie.reverts("Provenance hash is not set."):
        token.freezeProvenanceHash({'from':owner})

#set after frozen
def test_freeze_empty_provenance_two(token):
    owner = accounts[0]
    new_provenance = ""
    with brownie.reverts("Provenance hash cannot be empty string."):
        token.setProvenanceHash(new_provenance, {'from':owner})


# assert only owner can airdrop      
def test_airdrop_at_init(token):
    owner = accounts[0]
    user = accounts[1]
    with brownie.reverts("No airdrops at init."):
        token.airdropCryptid(1, user, {'from': owner})

# assert only owner can airdrop      
def test_airdrop_as_user(token):
    owner = accounts[0]
    user = accounts[1]
    with brownie.reverts("Ownable: caller is not the owner"):
        token.airdropCryptid(1, user, {'from': user})

# airdrop token 
def test_airdrop(token):
    owner = accounts[0]
    user = accounts[1]
    tokens = 5
    old_user_balance = token.balanceOf(user)
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _airdropStage(token)
    token.airdropCryptid(tokens, user, {'from': owner})
    new_user_balance = token.balanceOf(user)
    assert(new_user_balance == old_user_balance + tokens)

# move from stage 0 to 1 without provenance frozen
def test_move_to_stage_1_before_provenance(token):
    owner = accounts[0]
    with brownie.reverts("Provenance hash must be frozen before minting can start."):
        token.setStage(1, {'from': owner})

# move from stage 0 to 1 without provenance frozen
def test_move_to_stage_1_before_merkle(token):
    owner = accounts[0]
    _setFreezeProvenance(token)
    with brownie.reverts("Merkle root must be set beefore minting can start."):
        token.setStage(1, {'from': owner})

def test_move_to_stage_1_after_provenance(token):
    owner = accounts[0]
    stage_before = token.stage()
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _airdropStage(token)
    token.setStage(1, {'from': owner})
    stage_after = token.stage()
    assert(stage_after == stage_before + 1)

def test_move_to_stage_4_after_provenance(token):
    owner = accounts[0]
    stage_before = token.stage()
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    token.setStage(4, {'from': owner})
    stage_after = token.stage()
    assert(stage_after == stage_before + 4)

def test_airdrop_to_contract(token):
    owner = accounts[0]
    user = accounts[1]
    tokens = 2
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _airdropStage(token)
    test = accounts[0].deploy(TestContract).address
    # test_address = test.address()
    with brownie.reverts("ERC721: transfer to non ERC721Receiver implementer"):
        token.airdropCryptid(tokens, test, {'from': owner})
    test = accounts[0].deploy(ReceiverContract).address
    old_owner_balance = token.balanceOf(test)
    accounts[0].transfer(test, "10 ether", gas_price=0)

    token.airdropCryptid(5, test, {'from': owner})
    assert(token.balanceOf(test) == 5)
    new_owner_balance = token.balanceOf(test)
    assert(new_owner_balance == old_owner_balance + 5)

# airdrop too many token 
def test_airdrop_too_many(token):
    owner = accounts[0]
    user = accounts[1]
    maxTx = token.totalSaleSupply()
    tokens = maxTx + 1
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _airdropStage(token)
    with brownie.reverts("Mint amount will exceed total sale supply."):
        token.airdropCryptid(tokens, user, {'from': owner})



def test_airdrop_to_zero(token):
    owner = accounts[0]
    user = "0x0000000000000000000000000000000000000000"
    tokens = 2
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _airdropStage(token)
    with brownie.reverts("ERC721: mint to the zero address"):
        token.airdropCryptid(tokens, user, {'from': owner})

# initial provenance is unfrozen
def test_freeze_provenance(token):
    assert(token.provenanceHashFrozen() == False)

# assert balances in account 0 and 1
def test_account_balance():
    balance = accounts[0].balance()
    accounts[0].transfer(accounts[1], "10 ether", gas_price=0)
    assert balance - "10 ether" == accounts[0].balance()

# mint as owner after deploy
def test_wl_before_wl(token):
    owner = accounts[0]
    user = accounts[1]
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    with brownie.reverts("Whitelist sale not initiated."):
        token.whitelistMint(proof, {'from': owner,'value': "0.10 ether"})

# mint as owner after deploy
def test_public_before_public(token):
    owner = accounts[0]
    user = accounts[1]
    with brownie.reverts("Public Sale not initiated."):
        token.publicMint(1, {'from': user,'value': "0.10 ether"})



# team mint

def test_team_mints(token):
    owner = accounts[0]
    user = accounts[1]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    with brownie.reverts("Team mint not initiated."):
        token.teamMint(5, {'from': owner})
    _teamMintStage(token)
    mint = 5
    balance_before = token.balanceOf(owner)
    token.teamMint(mint, {'from': owner})
    balance_after = token.balanceOf(owner)
    assert(balance_after == balance_before + mint)
    with brownie.reverts("Ownable: caller is not the owner"):
        token.teamMint(mint, {'from': user})
    token.teamMint(mint, {'from': owner})
    with brownie.reverts("Transaction exceeds total team sale supply."):
        token.teamMint(mint, {'from': owner})
    assert(token.teamMintCount() == 10)

def test_whitelist_mints_attempt_four(token):
    owner = accounts[0]
    user = accounts[1]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    with brownie.reverts("Whitelist sale not initiated."):
        token.whitelistMint(proof, {'from': owner, 'value': '0.10 ether'})
    _whitelistStage(token)
    mint = 1
    balance_before = token.balanceOf(user)
    with brownie.reverts("Address not in whitelist."):
        token.whitelistMint(proof, {'from': owner, 'value': '0.1 ether'})
    token.whitelistMint(proof, {'from': user, 'value': '0.1 ether'}) 
    balance_after = token.balanceOf(user)
    assert(balance_after == balance_before + mint)
    assert(token.totalSupply() == mint)
    assert(token.claimed(user) == True)

def test_public__two_mints_two(token):
    owner = accounts[0]
    user = accounts[1]
    with brownie.reverts('Provenance hash must be frozen before minting can start.'):
        _publicSaleStage(token)
    _setFreezeProvenance(token)
    with brownie.reverts('Merkle root must be set beefore minting can start.'):
        _publicSaleStage(token)
    _setMerkleRoot(token)

    with brownie.reverts("Public Sale not initiated."):
        token.publicMint(5, {'from': owner, 'value': '0.50 ether'})
    _publicSaleStage(token)
    assert(token.stage() == 4)
    mint = 5
    balance_before = token.balanceOf(owner)
    with brownie.reverts("Incorrect ETH value sent."):
        token.publicMint(mint, {'from': owner, 'value': '0.4 ether'})
    token.publicMint(5, {'from': owner, 'value': '0.5 ether'}) 
    balance_after = token.balanceOf(owner)
    assert(balance_after == balance_before + mint)
    with brownie.reverts("Exceeds max allowed mints per transaction."):
        token.publicMint(6, {'from': owner, 'value': '0.6 ether'}) 
    token.publicMint(5, {'from': owner, 'value': '0.5 ether'}) 
    token.publicMint(5, {'from': owner, 'value': '0.5 ether'}) 
    token.publicMint(5, {'from': owner, 'value': '0.5 ether'}) 
    token.publicMint(5, {'from': owner, 'value': '0.5 ether'}) 
    token.publicMint(5, {'from': owner, 'value': '0.5 ether'})
    with brownie.reverts("Transaction exceeds total sale supply."):
        token.publicMint(5, {'from': owner, 'value': '0.5 ether'}) 
    assert(token.totalSupply() == 30)
    assert(token.totalSaleSupply() == token.totalSupply())



# mint as owner after deploy
def test_address_not_in_wl(token):
    owner = accounts[0]
    user = accounts[1]
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _whitelistStage(token)
    with brownie.reverts("Address not in whitelist."):
        token.whitelistMint(proof, {'from': owner,'value': "0.1 ether"})

# mint as owner after deploy
def test_wl_wrong_payment(token):
    owner = accounts[0]
    user = accounts[1]
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _whitelistStage(token)
    with brownie.reverts("Incorrect ETH value sent."):
        token.whitelistMint(proof, {'from': user, 'value': "1 ether"})

# whitelist mint
def test_whitelist_mint(token):
    owner = accounts[0]
    user = accounts[1]
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _whitelistStage(token)
    balance_before = token.balanceOf(user)
    token.whitelistMint(proof, {'from': user, 'value': "0.1 ether"})
    balance_after = token.balanceOf(user)
    assert(balance_after == balance_before + 1)
    bool = token.claimed(user)
    assert(bool == True)
    with brownie.reverts("Whitelist mint already claimed."):
        token.whitelistMint(proof, {'from': user, 'value': "0.1 ether"})

def test_whitelist_mint_double(token):
    owner = accounts[0]
    user = accounts[1]
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _whitelistStage(token)
    token.whitelistMint(proof, {'from': user, 'value': "0.1 ether"})
    with brownie.reverts("Whitelist mint already claimed."):
        token.whitelistMint(proof, {'from': user, 'value': "0.1 ether"})

# double whitelist mint
def test_whitelist_mint_three(token):
    owner = accounts[0]
    user = accounts[1]
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _whitelistStage(token)
    balance_before = token.balanceOf(user)
    token.whitelistMint(proof, {'from': user, 'value': "0.1 ether"})
    balance_after = token.balanceOf(user)
    assert(balance_after == balance_before + 1)
    assert(token.claimed(user) == True)


# double whitelist mint
def test_public_mint_three(token):
    owner = accounts[0]
    user = accounts[1]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    tokens = 1
    balance_before = token.balanceOf(user)
    token.publicMint(tokens, {'from': user, 'value': "0.1 ether"})
    balance_after = token.balanceOf(user)
    assert(balance_after == balance_before + tokens)
    assert(token.balanceOf(user) == tokens)
    assert(token.totalSupply() == tokens)
    assert(token.lastMintID() == tokens)
    assert(token.getTokensLeft() == token.totalSaleSupply() - tokens)
    assert(token.walletOfOwner(user) == [tokens])
    assert(token.lastMintAddress() == user)
    assert(user == token.ownerOf(tokens))

# wl before merkle
def test_whitelist_merkle_error_three(token):
    owner = accounts[0]
    user = accounts[1]
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _whitelistStage(token)
    with brownie.reverts("Address not in whitelist."):
        token.whitelistMint(proof, {'from': owner, 'value': "0.1 ether"})

# wl before merkle
def test_whitelist_mint_before_merkle(token):
    owner = accounts[0]
    user = accounts[1]
    proof = ["0xe58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x29abd47fcc3f75d7585a8471d4057d5b5dabcbc6e87cd65a567a5c0626243539"]
    _setFreezeProvenance(token)
    with brownie.reverts('Merkle root must be set beefore minting can start.'):
        _whitelistStage(token)

# wl before merkle
def test_whitelist_merkle_error(token):
    owner = accounts[0]
    user = accounts[1]
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    with brownie.reverts("Whitelist sale not initiated."):
        token.whitelistMint(proof, {'from': user, 'value': "0.1 ether"})

# ownerOf assert
def test_owner_of(token):
    owner = accounts[0]
    user = accounts[1]
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _whitelistStage(token)
    token.whitelistMint(proof, {'from': user, 'value': "0.1 ether"})
    assert(user == token.ownerOf(1))
    token.pause({'from':owner})
    with brownie.reverts('Pausable: paused'):
        token.whitelistMint(proof, {'from': user, 'value': "0.1 ether"})

# ownerOf assert
def test_owner_two_of_public(token):
    owner = accounts[0]
    user = accounts[1]
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    token.publicMint(1, {'from': user, 'value': "0.1 ether"})
    assert(user == token.ownerOf(1))
    token.pause({'from':owner})
    with brownie.reverts('Pausable: paused'):
        token.publicMint(1, {'from': user, 'value': "0.1 ether"})


# mint a token to a receiver contract
def test_public_sale_to_contract(token):
    owner = accounts[0]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    tokens = 1
    test = accounts[0].deploy(ReceiverContract).address
    accounts[0].transfer(test, "10 ether", gas_price=0)
    txn_receipt = token.publicMint(tokens, {'from': test, 'value': "0.1 ether"})
    assert(test == token.ownerOf(tokens))
    event = txn_receipt.events['Transfer']
    assert(event['tokenId'] == tokens)
    assert(event['from'] == "0x"+"0"*40)
    assert(event['to'] == test)
    token.pause({'from':owner})
    with brownie.reverts('Pausable: paused'):
        token.publicMint(tokens, {'from': test, 'value': "0.1 ether"})
    token.unpause({'from':owner})
    token.publicMint(tokens, {'from': test, 'value': "0.1 ether"})
    assert(test == token.ownerOf(2))


# test mint at stage 0
def test_mint_at_init(token):
    owner = accounts[0]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    user = accounts[1]
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    with brownie.reverts('Incorrect ETH value sent.'):
        token.whitelistMint(proof, {'from': user, 'value': '0.09 ether'})
    with brownie.reverts("Whitelist sale not initiated."):
        token.whitelistMint(proof, {'from': user, 'value': '0.10 ether'})
    _whitelistStage(token)
    token.whitelistMint(proof, {'from': user, 'value': "0.1 ether"})
    with brownie.reverts("Whitelist mint already claimed."):
        token.whitelistMint(proof, {'from': user, 'value': "0.1 ether"})
    with brownie.reverts("Address not in whitelist."):
        token.whitelistMint(proof, {'from': owner, 'value': "0.1 ether"})
    token.undoClaim(user, {'from': owner})
    token.whitelistMint(proof, {'from': user, 'value': "0.1 ether"})

def test_mint_four_person(token):
    user_1 = accounts[1]
    user_2 = accounts[2]
    user_3 = accounts[3]
    user_4 = accounts[4]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    txn_1 = token.publicMint(1, {'from': user_1, 'value': "0.1 ether"})
    txn_2 = token.publicMint(1, {'from': user_2, 'value': "0.1 ether"})
    txn_3 = token.publicMint(1, {'from': user_3, 'value': "0.1 ether"})
    txn_4 = token.publicMint(1, {'from': user_4, 'value': "0.1 ether"})
    assert(user_1 == token.ownerOf(1))
    assert(user_2 == token.ownerOf(2))
    assert(user_3 == token.ownerOf(3))
    assert(user_4 == token.ownerOf(4))

    event = txn_1.events['Transfer']
    assert(event['tokenId'] == 1)
    assert(event['from'] == "0x"+"0"*40)
    assert(event['to'] == user_1)

    event = txn_2.events['Transfer']
    assert(event['tokenId'] == 2)
    assert(event['from'] == "0x"+"0"*40)
    assert(event['to'] == user_2)

    event = txn_3.events['Transfer']
    assert(event['tokenId'] == 3)
    assert(event['from'] == "0x"+"0"*40)
    assert(event['to'] == user_3)

    event = txn_4.events['Transfer']
    assert(event['tokenId'] == 4)
    assert(event['from'] == "0x"+"0"*40)
    assert(event['to'] == user_4)   

def test_whitelist_mint_asserts(token):
    owner = accounts[0]
    tokenID = 1
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    user = accounts[1]
    proof = ["0xd58ec672f132365ae3f63a025bdb2b21ab3682bb1e599e56c7c542dd42b5699e","0x9cefd68b762d62f3cbf277fc0c90031add3b2365bcb6d9335e56ab84ba3cf0e1","0x930f5668a4e5af398528616d4afe4b128860a6b5c8a6e3d3ac7598f86db33e3b","0x01f557f5923ebd689504fe96c9a0578f2fd4f9592903b0eddb96f569002d5f79"]
    
    _whitelistStage(token)

    oldBalance = token.balanceOf(user)
    txn_receipt = token.whitelistMint(proof, {"from": user, 'value': '0.1 ether'})
    newBalance = token.balanceOf(user)
    assert(newBalance == oldBalance + 1)
    assert(user == token.ownerOf(tokenID))

    # Verify that minting has created an event
    event = txn_receipt.events['Transfer']
    assert(event['tokenId'] == tokenID)
    assert(event['from'] == "0x"+"0"*40)
    assert(event['to'] == user)

def test_whitelist_test_mint_asserts_public(token):
    owner = accounts[0]
    tokenID = 1
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    user = accounts[1]
    _publicSaleStage(token)

    oldBalance = token.balanceOf(user)
    txn_receipt = token.publicMint(1, {"from": user, 'value': '0.1 ether'})
    newBalance = token.balanceOf(user)
    assert(newBalance == oldBalance + 1)
    assert(user == token.ownerOf(tokenID))

    # Verify that minting has created an event
    event = txn_receipt.events['Transfer']
    assert(event['tokenId'] == tokenID)
    assert(event['from'] == "0x"+"0"*40)
    assert(event['to'] == user)


# mint as zero address during public sale - will revert
def test_public_sale_to_non_erc_contract_public(token):
    owner = accounts[0]
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    tokens = 5
    test = accounts[0].deploy(TestContract).address
    accounts[0].transfer(test, "10 ether", gas_price=0)
    with brownie.reverts("ERC721: transfer to non ERC721Receiver implementer"):
        token.publicMint(tokens, {'from': test, 'value': "0.5 ether"})



# airdrop at whitelist
def test_airdrop_at_public_sale(token):
    owner = accounts[0]
    user = accounts[1]
    tokens = 5
    old_user_balance = token.balanceOf(user)
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    token.publicMint(tokens, {'from': user, 'value':'0.5 ether'})
    new_user_balance = token.balanceOf(user)
    assert(new_user_balance == old_user_balance + tokens)


# ownerOf assert
def test_owner_of_nonexistent_token(token):
    user = accounts[1]
    with brownie.reverts("ERC721: owner query for nonexistent token"):
        token.ownerOf(1)


def public_mint(token):
    user = accounts[1]
    tokenID = 5
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    with brownie.reverts("Incorrect ETH value sent."):
        token.publicMint(tokenID, {'from': user, 'value': '0.40 ether'})

# airdrop at whitelist
def test_public_mints(token):
    owner = accounts[0]
    user = accounts[1]
    tokens = 6
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    old_user_balance = token.balanceOf(user)
    with brownie.reverts("Exceeds max allowed mints per transaction."):
        token.publicMint(tokens, {'from': user, 'value':'0.6 ether'})
    tokens_five = 5
    token.publicMint(tokens_five, {'from': user, 'value':'0.5 ether'})
    new_user_balance = token.balanceOf(user)
    assert(new_user_balance == old_user_balance + tokens_five)
    token.publicMint(tokens_five, {'from': user, 'value':'0.5 ether'})
    token.publicMint(0, {'from': user, 'value':'0.0 ether'})
    token.publicMint(tokens_five, {'from': user, 'value':'0.5 ether'})
    token.publicMint(tokens_five, {'from': user, 'value':'0.5 ether'})
    token.publicMint(tokens_five, {'from': user, 'value':'0.5 ether'})
    with brownie.reverts("Incorrect ETH value sent."):
        token.publicMint(tokens_five, {'from': user, 'value':'0.6 ether'})
    token.publicMint(tokens_five, {'from': user, 'value':'0.5 ether'})
    with brownie.reverts("Transaction exceeds total sale supply."):
        token.publicMint(tokens_five, {'from': user, 'value':'0.5 ether'})



def test_set_frozen_base_uri(token):
    owner = accounts[0]
    user = accounts[1]
    with brownie.reverts("BaseURI cannot be empty."):
        token.freezeBaseURI({'from': owner})
    baseUri = "http://testuri.io/"
    token.setBaseURI(baseUri, {'from': owner})
    assert(token.baseURI() == baseUri)
    with brownie.reverts("Ownable: caller is not the owner"):
        token.setBaseURI(baseUri, {'from': user})
    token.freezeBaseURI({'from': owner})
    assert(token.tokenURIFrozen() == True)
    with brownie.reverts("BaseURI is already frozen."):
        token.freezeBaseURI({'from': owner})
    with brownie.reverts("BaseURI is frozen."):
        token.setBaseURI(baseUri, {'from': owner})


# Inquire the balance for the zero address - this should raise an exception
def test_balanceOfZeroAddress(token):
    with brownie.reverts('ERC721: balance query for the zero address'):
        balance = token.balanceOf("0x"+"0"*40)

# Inquire the balance for a non-zero address 
def test_balance_of_non_zero_address(token):
    balance = token.balanceOf("0x1"+"0"*39)
    assert(0 == balance);   



def test_ERC615(token):
    # ERC721
    assert(True == token.supportsInterface("0x80ac58cd"))
    # ERC165 itself
    assert(True == token.supportsInterface("0x01ffc9a7"))
    # ERC721 Metadata 
    assert(True == token.supportsInterface("0x5b5e139f"))

def test_name_symbol(token):
    name = token.name()
    symbol = token.symbol()
    assert(len(name) > 0)
    assert(len(symbol) > 0)

# Test a valid transfer, initiated by the current owner of the token
def test_transfer_from(token):
    owner = accounts[0]
    user = accounts[1]
    tokenID = 1
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    token.publicMint(tokenID, {'from': owner, 'value': "0.10 ether"})
    oldBalanceMe = token.balanceOf(owner)
    oldBalanceAlice = token.balanceOf(user)
    txn_receipt = token.transferFrom(owner, user, tokenID, {"from": owner})
    assert(user == token.ownerOf(tokenID))
    newBalanceMe = token.balanceOf(owner)
    newBalanceAlice = token.balanceOf(user)
    assert (newBalanceMe + 1 == oldBalanceMe)
    assert (oldBalanceAlice + 1 == newBalanceAlice)
    _verifyTransferEvent(txn_receipt, owner, user, tokenID)

# transfer from non-owner
def test_transfer_from_non_owner(token):
    owner = accounts[0]
    user = accounts[1]
    user_2 = accounts[2]
    tokenID = 1
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    token.publicMint(tokenID, {'from': owner, 'value': "0.10 ether"})
    with brownie.reverts("ERC721: transfer caller is not owner nor approved"):
        token.transferFrom(user_2, user, tokenID,{"from": user_2})

# Test an invalid transfer - to is the zero address
def test_transfer_to_zero_address(token):
    owner = accounts[0]
    tokenID = 1
    _mint(token)
    # Now do the transfer
    with brownie.reverts('ERC721: transfer to the zero address'):
        token.transferFrom(owner, "0x"+40*"0", tokenID, {"from": owner})

# transfer from non owner
def test_transfer_from_non_approved_owner(token):
    owner = accounts[0]
    user = accounts[1]
    user_2 = accounts[2]
    tokenID = 1
    _mint(token)
    with brownie.reverts("ERC721: transfer caller is not owner nor approved"):
        token.transferFrom(owner, user, tokenID,{"from": user})

# Test a valid safe transfer, initiated by the current owner of the token
def test_safe_transfer_from(token):
    owner = accounts[0]
    alice = accounts[1]
    tokenID = 1
    _mint(token)
    # Remember balances
    oldBalanceMe = token.balanceOf(owner)
    oldBalanceAlice = token.balanceOf(alice)
    # Now do the transfer
    txn_receipt = token.safeTransferFrom(owner, alice, tokenID, hexbytes.HexBytes(""), {"from": owner})
    # check owner of NFT
    assert(alice == token.ownerOf(tokenID))
    # Check balances
    newBalanceMe = token.balanceOf(owner)
    newBalanceAlice = token.balanceOf(alice)
    assert (newBalanceMe + 1 == oldBalanceMe)
    assert (oldBalanceAlice + 1 == newBalanceAlice)
    # Verify that an Transfer event has been logged
    _verifyTransferEvent(txn_receipt, owner, alice, tokenID)

# Test an invalid safe transfer - from is not current owner
def test_safe_transfer_from_not_owner(token):
    me = accounts[0]
    alice = accounts[1]
    bob = accounts[2]
    tokenID = 1
    _mint(token)
    # Now do the transfer
    with brownie.reverts("ERC721: transfer caller is not owner nor approved"):
        token.safeTransferFrom(bob, alice, tokenID, hexbytes.HexBytes(""), {"from": bob})

# Test an safe invalid transfer - to is the zero address
def test_safe_transfer_from_to_zero_address(token):
    me = accounts[0]
    tokenID = 1
    _mint(token)
    # Now do the transfer
    with brownie.reverts("ERC721: transfer to the zero address"):
        token.safeTransferFrom(me, "0x"+40*"0", tokenID, hexbytes.HexBytes(""), {"from": me})

# Test an invalid safe transfer - not authorized
def test_safe_transfer_from_not_authorized(token):
    me = accounts[0]
    alice = accounts[1]
    bob = accounts[2]
    tokenID = 1
    _mint(token)
    # Now do the transfer
    with brownie.reverts("ERC721: transfer caller is not owner nor approved"):
        token.safeTransferFrom(me, alice, tokenID, hexbytes.HexBytes(""), {"from": bob})

# Test a valid safe transfer to a contract returning the proper magic value
def test_safe_transfer_from_test(token):
    data = "0x1234"
    me = accounts[0]
    tokenID = 1
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _airdropStage(token)
    token.airdropCryptid(tokenID, me, {'from': me})
    tokenReceiver = accounts[0].deploy(ReceiverContract)
    oldInvocationCount = tokenReceiver.getInvocationCount()
    # Remember balances
    oldBalanceMe = token.balanceOf(me)
    oldBalanceToken = token.balanceOf(tokenReceiver.address)
    # Make sure that the contract returns the correct magic value
    tokenReceiver.setReturnCorrectValue(True)
    # Now do the transfer
    txn_receipt = token.safeTransferFrom(me, tokenReceiver.address, tokenID, hexbytes.HexBytes(data), {"from": me})
    # check owner of NFT
    assert(tokenReceiver.address == token.ownerOf(tokenID))
    # Check balances
    newBalanceMe = token.balanceOf(me)
    newBalanceToken = token.balanceOf(tokenReceiver.address)
    assert (newBalanceMe + 1 == oldBalanceMe)
    assert (oldBalanceToken + 1 == newBalanceToken)
    # get current invocation count of test contract
    newInvocationCount = tokenReceiver.getInvocationCount()
    assert(oldInvocationCount + 1 == newInvocationCount)
    # Check that data has been stored
    assert(tokenReceiver.getData() == data)
    # Verify that an Transfer event has been logged
    _verifyTransferEvent(txn_receipt, me, tokenReceiver.address, tokenID)

#
# Test a valid safe transfer to a contract returning the wrong proper magic value
#
def test_safe_transfer_from_wrong_magic_value(token):
    me = accounts[0]
    tokenID = 1

    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _airdropStage(token)
    token.airdropCryptid(tokenID, me, {'from': me})


    tokenReceiver = accounts[0].deploy(ReceiverContract)
    # Make sure that the contract returns the wrong magic value
    tokenReceiver.setReturnCorrectValue(False)
    # Now do the transfer
    with brownie.reverts("ERC721: transfer to non ERC721Receiver implementer"):
        token.safeTransferFrom(me, tokenReceiver.address, tokenID, hexbytes.HexBytes(""), {"from": me})
    # Reset behaviour of test contract
    tokenReceiver.setReturnCorrectValue(True)

# Test a valid safe transfer to a contract returning the proper magic value - no data
def test_safe_transfer_from_no_data(token):
    me = accounts[0]
    tokenID = 1
    _mint(token)
    tokenReceiver = accounts[0].deploy(ReceiverContract)
    # get current invocation count of test contract
    oldInvocationCount = tokenReceiver.getInvocationCount()
    # Remember balances
    oldBalanceMe = token.balanceOf(me)
    oldBalanceToken = token.balanceOf(tokenReceiver.address)
    # Make sure that the contract returns the correct magic value
    tokenReceiver.setReturnCorrectValue(True)
    # Now do the transfer
    txn_receipt = token.safeTransferFrom(me, tokenReceiver.address, tokenID,  {"from": me})
    # check owner of NFT
    assert(tokenReceiver.address == token.ownerOf(tokenID))
    # Check balances
    newBalanceMe = token.balanceOf(me)
    newBalanceToken = token.balanceOf(tokenReceiver.address)
    assert (newBalanceMe + 1 == oldBalanceMe)
    assert (oldBalanceToken + 1 == newBalanceToken)
    # get current invocation count of test contract
    newInvocationCount = tokenReceiver.getInvocationCount()
    assert(oldInvocationCount + 1 == newInvocationCount)
    # Verify that an Transfer event has been logged
    _verifyTransferEvent(txn_receipt, me, tokenReceiver.address, tokenID)

# Test an approval which is not authorized
def test_approval_not_authorized(token):
    me = accounts[0]
    alice = accounts[1]
    tokenID = 1
    _mint(token)
    with brownie.reverts("ERC721: approve caller is not owner nor approved for all"):
        token.approve(alice, tokenID, {"from": alice})

# Test setting and getting approval
def test_approval(token):
    me = accounts[0]
    bob = accounts[2]
    tokenID = 1
    # Get approval - should raise
    with brownie.reverts("ERC721: approved query for nonexistent token"):
        token.getApproved(tokenID)
    # Approve - should raise
    with brownie.reverts("ERC721: owner query for nonexistent token"):
        token.approve(bob, tokenID, {"from": me})
    # Mint
    _mint(token)
    # Approve for bob 
    txn_receipt = token.approve(bob, tokenID, {"from": me})
    # Check
    assert(bob == token.getApproved(tokenID))
    # Verify events
    _verifyApprovalEvent(txn_receipt, me, bob, tokenID) # owner, approved, tokenID

# Test that approval is reset to zero address if token is transferred
def test_approval_reset_upon_transfer(token):
    me = accounts[0]
    alice = accounts[1]
    bob = accounts[2]
    tokenID = 1
    _mint(token)
    # Approve for bob 
    token.approve(bob, tokenID, {"from": me})
    # Check
    assert(bob == token.getApproved(tokenID))
    # Do transfer
    token.transferFrom(me, alice, tokenID, {"from": bob})
    # Check that approval has been reset
    assert(("0x"+40*"0") == token.getApproved(tokenID))

# Test setting and clearing the operator flag
def test_set_get_operator(token):
    me = accounts[0]
    alice = accounts[1]
    bob = accounts[2]
    assert(False == token.isApprovedForAll(me, bob))
    assert(False == token.isApprovedForAll(me, alice))
    # Declare bob as operator for me 
    txn_receipt = token.setApprovalForAll(bob, True, {"from": me})
    # Check
    assert(True == token.isApprovedForAll(me, bob))
    assert(False == token.isApprovedForAll(me, alice))
    # Check events
    _verifyApprovalForAllEvent(txn_receipt, me, bob, True)
    # Do the same for alice
    txn_receipt = token.setApprovalForAll(alice, True, {"from": me})
    # Check
    assert(True == token.isApprovedForAll(me, bob))
    assert(True == token.isApprovedForAll(me, alice))
    # Check events
    _verifyApprovalForAllEvent(txn_receipt, me, alice, True)
    # Reset both
    txn_receipt = token.setApprovalForAll(bob, False, {"from": me})
    # Check events
    _verifyApprovalForAllEvent(txn_receipt, me, bob, False)
    txn_receipt = token.setApprovalForAll(alice, False, {"from": me})
    # Check events
    _verifyApprovalForAllEvent(txn_receipt, me, alice, False)
    # Check
    assert(False == token.isApprovedForAll(me, bob))
    assert(False == token.isApprovedForAll(me, alice))

# Test authorization logic for setting and getting approval
def test_approval_authorization(token):
    me = accounts[0]
    alice = accounts[1]
    bob = accounts[2]
    tokenID = 1
    _mint(token)
    # Try to approve for bob while not being owner or operator - this should raise an exception
    with brownie.reverts("ERC721: approve caller is not owner nor approved for all"):
        token.approve(bob, tokenID, {"from": alice})
    # Now make alice an operator for me
    token.setApprovalForAll(alice, True, {"from": me})
    # Approve for bob again - this should now work
    txn_receipt = token.approve(bob, tokenID, {"from": alice})
    # Check
    assert(bob == token.getApproved(tokenID))
    # Verify events
    _verifyApprovalEvent(txn_receipt, me, bob, tokenID)
    # Reset
    token.setApprovalForAll(alice, False, {"from": me})

# Test a valid transfer, initiated by an operator for the current owner of the token
def test_transfer_from_operator(token):
    me = accounts[0]
    alice = accounts[1]
    bob = accounts[2]
    tokenID = 1
    _mint(token)
    # Now make bob an operator for me
    token.setApprovalForAll(bob, True, {"from": me})
    # Remember balances
    oldBalanceMe = token.balanceOf(me)
    oldBalanceAlice = token.balanceOf(alice)
    # Now do the transfer
    txn_receipt = token.transferFrom(me, alice, tokenID, {"from": bob})
    # Reset
    token.setApprovalForAll(bob, False, {"from": me})
    # check owner of NFT
    assert(alice == token.ownerOf(tokenID))
    # Check balancesf
    newBalanceMe = token.balanceOf(me)
    newBalanceAlice = token.balanceOf(alice)
    assert (newBalanceMe + 1 == oldBalanceMe)
    assert (oldBalanceAlice + 1 == newBalanceAlice)
    # Verify that an Transfer event has been logged
    _verifyTransferEvent(txn_receipt, me, alice, tokenID)

def test_last_mint_address(token):
    me = accounts[0]
    tokenID = 1
    with brownie.reverts('ERC721: owner query for nonexistent token'):
            token.lastMintAddress()
    _mint(token)
    assert(token.lastMintAddress() == me)

def test_last_mint_id(token):
    me = accounts[0]
    tokenID = 1
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    token.publicMint(tokenID, {'from': me, 'value':'0.1 ether'})
    assert(token.lastMintID() == tokenID)


def test_token_uri(token):
    owner = accounts[0]
    _mint(token)
    with brownie.reverts('ERC721Metadata: URI query for nonexistent token.'):
        token.tokenURI(2)
    token.setBaseURI("http://baseuri.com/", {'from': owner})
    assert(token.tokenURI(1) == "http://baseuri.com/1.json")

def test_withdraw(token):
    owner = accounts[0]
    chris = accounts[1]
    chris_before = chris.balance()
    steph = accounts[2]
    tokenID = 1
    with brownie.reverts("Ownable: caller is not the owner"):
        token.withdraw({'from': chris})
    with brownie.reverts("Contract balance is 0."):
        token.withdraw({'from': owner})
    _mint(token)
    token.setWithdrawlAddress(chris, {'from':owner})
    assert(token.balance() == "0.10 ether")
    token.withdraw({'from':owner})
    assert(chris.balance() == chris_before + "0.1 ether")
    with brownie.reverts("Contract balance is 0."):
        token.withdraw({'from':owner})

    test = accounts[0].deploy(NonreceiverContract).address
    token.setWithdrawlAddress(test, {'from':owner})
    _publicSaleStage(token)
    token.publicMint(1, {'from': owner, 'value': "0.10 ether"})
    with brownie.reverts("Withdrawl failed."):
        token.withdraw({'from':owner})

def test_transfer_ownership(token):
    owner = accounts[0]
    chris = accounts[1]
    steph = accounts[2]
    with brownie.reverts("Ownable: caller is not the owner"):
        token.transferOwnership(chris, {'from':steph})
    token.transferOwnership(chris, {'from':owner})
    assert(token.owner() == chris)
    with brownie.reverts("Ownable: new owner is the zero address"):
        token.transferOwnership(("0x"+"0"*40), {'from':chris})

def test_public_not_initiated(token):
    owner = accounts[0]
    user = accounts[1]
    tokenID = 5
    with brownie.reverts("Public Sale not initiated."):
        token.publicMint(tokenID, {"from": owner, 'value': '0.50 ether'})

def test_provenance_not_set(token):
    owner = accounts[0]
    user = accounts[1]
    tokenID = 5
    with brownie.reverts("Provenance hash must be frozen before minting can start."):
        _publicSaleStage(token)

def test_public_too_many_tx(token): 
    owner = accounts[0]
    user = accounts[1]
    tokenID = 5
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    assert(token.stage() == 4)
    with brownie.reverts("Exceeds max allowed mints per transaction."):
        token.publicMint(6, {"from": owner, 'value': '0.60 ether'})

def test_public_wrong_eth(token): 
    owner = accounts[0]
    user = accounts[1]
    tokenID = 5
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)
    with brownie.reverts("Incorrect ETH value sent."):
        token.publicMint(1, {"from": owner, 'value': '0.05 ether'})


def test_public_mint_function_check(token): 
    owner = accounts[0]
    user = accounts[1]
    tokenID = 5
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)    
    old_owner_balance = token.balanceOf(owner)
    token.publicMint(tokenID, {"from": owner, 'value': '0.5 ether'})
    assert(token.balanceOf(owner) == 5)
    new_owner_balance = token.balanceOf(owner)
    assert(new_owner_balance == old_owner_balance + 5)

def test_public_mint_while_paused(token): 
    owner = accounts[0]
    user = accounts[1]
    tokenID = 5
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)    
    with brownie.reverts("Ownable: caller is not the owner"):
        token.pause({'from':user})
    token.pause({'from':owner})
    with brownie.reverts('Pausable: paused'):
        token.publicMint(tokenID, {"from": owner, 'value': '0.5 ether'})
    
    
def test_public_mint_bad_receiver(token): 
    owner = accounts[0]
    user = accounts[1]
    tokenID = 5
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)       
    test = accounts[0].deploy(TestContract).address
    accounts[0].transfer(test, "10 ether", gas_price=0)
    with brownie.reverts("ERC721: transfer to non ERC721Receiver implementer"):
        token.publicMint(tokenID, {"from": test, 'value': '0.5 ether'})


def test_public_mint_good_receiver(token): 
    owner = accounts[0]
    user = accounts[1]
    tokenID = 5
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)       

    test = accounts[0].deploy(ReceiverContract).address
    old_owner_balance = token.balanceOf(test)
    accounts[0].transfer(test, "10 ether", gas_price=0)

    token.publicMint(tokenID, {"from": test, 'value': '0.5 ether'})
    assert(token.balanceOf(test) == 5)
    new_owner_balance = token.balanceOf(test)
    assert(new_owner_balance == old_owner_balance + 5)

def test_public_too_many(token): 
    owner = accounts[0]
    user = accounts[1]
    tokenID = 5
    _setFreezeProvenance(token)
    _setMerkleRoot(token)
    _publicSaleStage(token)  
    token.publicMint(tokenID, {"from": owner, 'value': '0.5 ether'})
    assert(token.tokenOfOwnerByIndex(owner, 0) == 1)
    assert(token.tokenByIndex(0) == 1)
    token.publicMint(tokenID, {"from": owner, 'value': '0.5 ether'})
    token.publicMint(tokenID, {"from": owner, 'value': '0.5 ether'})
    token.publicMint(tokenID, {"from": user, 'value': '0.5 ether'})
    token.publicMint(tokenID, {"from": owner, 'value': '0.5 ether'})
    token.publicMint(tokenID, {"from": owner, 'value': '0.5 ether'})
    with brownie.reverts("Transaction exceeds total sale supply."):
        token.publicMint(tokenID, {"from": owner, 'value': '0.5 ether'})
    assert(token.totalSupply() == 30)

def test_base_extension(token):
    new_base_extension = 'new base'
    token.setBaseExtension(new_base_extension)
    assert(token.baseExtension() == new_base_extension)

    
