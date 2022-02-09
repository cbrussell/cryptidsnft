import pytest
import brownie 
import hexbytes;
from brownie import CryptidToken, TestContract, ReceiverContract, NonreceiverContract, accounts, exceptions;

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

def _initStage(token):
    owner = accounts[0]
    token.setStage({'from': owner,'value': 0})

def _airdropStage(token):
    owner = accounts[0]
    token.setStage({'from': owner,'value': 1})

def _whitelistStage(token):
    owner = accounts[0]
    token.setStage({'from': owner,'value': 2})

def _teamMintStage(token):
    owner = accounts[0]
    token.setStage({'from': owner,'value': 3})

def _publicSaleStage(token):
    owner = accounts[0]
    token.setStage({'from': owner,'value': 4})

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

# def _mint(token, tokenID, owner):
#     owner = accounts[0]
#     tokenID = 1
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     token.mint(tokenID, {'from': owner, 'value': "0.06 ether"})

# Verify that an Approval event has been logged
def _verifyApprovalEvent(txn_receipt, owner, approved, tokenID):
    event = txn_receipt.events['Approval']
    assert(event['tokenId'] == tokenID)
    assert(event['owner'] == owner)
    assert(event['approved'] == approved)

# provenance has is frozen
def test_freeze_provenance(token):
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

    # with brownie.reverts("Provenance hash cannot be empty string."):
    #     token.freezeProvenanceHash({'from':owner})

# # initial provenance is unfrozen
# def test_freeze_provenance(token):
#     assert(token.provenanceHashFrozen() == False)

# # assert balances in account 0 and 1
# def test_account_balance():
#     balance = accounts[0].balance()
#     accounts[0].transfer(accounts[1], "10 ether", gas_price=0)
#     assert balance - "10 ether" == accounts[0].balance()

# # check no minting allowed after deployment as non-owner
# def test_mint_after_deploy_non_owner(token):
#     user = accounts[1]
#     with brownie.reverts("Minting not initiated. Currenly on stage 0 (init)."):
#         token.mint(1, {'from': user})

# # assert only owner can airdrop      
# def test_airdrop_as_non_owner(token):
#     user = accounts[1]
#     with brownie.reverts("Ownable: caller is not the owner"):
#         token.airdropCryptid(1, user, {'from': user})

# # mint as owner after deploy
# def test_mint_after_deploy_owner(token):
#     owner = accounts[0]
#     with brownie.reverts("Minting not initiated. Currenly on stage 0 (init)."):
#         token.mint(1, {'from': owner})

# # move from stage 0 to 1 without provenance frozen
# def test_move_to_stage_1_before_provenance(token):
#     owner = accounts[0]
#     with brownie.reverts("Provenance hash must be frozen before minting can start."):
#         token.nextStage({'from': owner})

# def test_move_to_stage_1_after_provenance(token):
#     owner = accounts[0]
#     _setFreezeProvenance(token)
#     stage_before = token.getStage()
#     token.nextStage({'from': owner})
#     stage_after = token.getStage()
#     assert(stage_after == stage_before + 1)

# # no stages after 4
# def test_only_four_stages(token):
#     owner = accounts[0]
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     with brownie.reverts("No stages after public sale"):
#         token.nextStage({'from': owner})
#     assert(token.getStage() == 4)

# # airdrop before provenance is set

# def test_airdrop_before_provinence_set(token):
#     owner = accounts[0]
#     user = accounts[1]
#     tokens = 5
#     with brownie.reverts("Provenance hash must be frozen before minting can start."):
#         token.airdropCryptid(tokens, user, {'from': owner})

# # airdrop token 
# def test_airdrop(token):
#     owner = accounts[0]
#     user = accounts[1]
#     tokens = 5
#     old_user_balance = token.balanceOf(user)
#     _setFreezeProvenance(token)
#     token.airdropCryptid(tokens, user, {'from': owner})
#     new_user_balance = token.balanceOf(user)
#     assert(new_user_balance == old_user_balance + tokens)

# # airdrop too many token 
# def test_airdrop_too_many(token):
#     owner = accounts[0]
#     user = accounts[1]
#     maxTx = token.maxMintPerTx()
#     tokens = maxTx + 1
#     _setFreezeProvenance(token)
#     with brownie.reverts("Exceeds max allowed amount per transaction"):
#         token.airdropCryptid(tokens, user, {'from': owner})

# def test_airdrop_to_contract(token):
#     owner = accounts[0]
#     user = accounts[1]
#     tokens = 2
#     _setFreezeProvenance(token)
#     test = accounts[0].deploy(TestContract).address
#     # test_address = test.address()
#     with brownie.reverts("ERC721: transfer to non ERC721Receiver implementer"):
#         token.airdropCryptid(tokens, test, {'from': owner})

# def test_airdrop_to_zero(token):
#     owner = accounts[0]
#     user = "0x0000000000000000000000000000000000000000"
#     tokens = 2
#     _setFreezeProvenance(token)
#     with brownie.reverts("ERC721: mint to the zero address"):
#         token.airdropCryptid(tokens, user, {'from': owner})

# # airdrop at whitelist
# def test_airdrop_at_whitelist(token):
#     owner = accounts[0]
#     user = accounts[1]
#     tokens = 5
#     old_user_balance = token.balanceOf(user)
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     token.airdropCryptid(tokens, user, {'from': owner})
#     new_user_balance = token.balanceOf(user)
#     assert(new_user_balance == old_user_balance + tokens)

# # airdrop at  presale
# def test_airdrop_at_presale(token):
#     owner = accounts[0]
#     user = accounts[1]
#     tokens = 5
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     with brownie.reverts("Past whitelist sale."):
#         token.airdropCryptid(tokens, user, {'from': owner})

# # airdrop 0 tokens
# def test_airdrop_at_whitelist_zero_tokens(token):
#     owner = accounts[0]
#     user = accounts[1]
#     tokens = 0
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     with brownie.reverts("Airdrop amount must be greater than 0"):
#         token.airdropCryptid(tokens, user, {'from': owner})

# # airdrop too many tokens
# def test_airdrop_at_whitelist_too_many_tx(token):
#     owner = accounts[0]
#     user = accounts[1]
#     maxTx = token.maxMintPerTx()
#     tokens = maxTx + 1
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     with brownie.reverts("Exceeds max allowed amount per transaction"):
#         token.airdropCryptid(tokens, user, {'from': owner})

# # airdrop beyond presale amount
# def test_airdrop_at_whitelist_beyone_presale_amount(token):
#     owner = accounts[0]
#     user = accounts[1]
#     tokens = 5
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     token.airdropCryptid(tokens, user, {'from': owner})
#     token.airdropCryptid(tokens, user, {'from': owner})
#     with brownie.reverts("Mint amount will exceed presale supply."): #presale supply is 10
#         token.airdropCryptid(tokens, user, {'from': owner})





# # test mint at stage 0
# def test_mint_stage_zero(token):
#     owner = accounts[0]
#     _setFreezeProvenance(token)
#     with brownie.reverts("Minting not initiated. Currenly on stage 0 (init)."):
#         token.mint(1, {'from': owner})

# # mint zero token as whitelisted - will revert due to overflow error
# def test_mint_exceed_whitelisted(token):
#     owner = accounts[0]
#     user = accounts[1]
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     mints = 2
#     token.setWhitelistUsers([user], [mints], {'from': owner})
#     with brownie.reverts("Transaction exceeds remaining whitelist mints"):
#         token.mint(3, {'from': user})

# # mint as non whitelist user
# def test_whitelist_not_on_list(token):
#     owner = accounts[0]
#     user = accounts[1]
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     mints = 2
#     with brownie.reverts("Minter not whitelisted."):
#         token.mint(mints, {'from': user})


# # whitelist mint
# def test_whitelist_mint(token):
#     owner = accounts[0]
#     user = accounts[1]
#     mints = 5
#     token.setWhitelistUsers([user], [mints], {'from': owner})
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     balance_before = token.balanceOf(user)
#     token.mint(mints, {'from': user})
#     balance_after = token.balanceOf(user)
#     assert(balance_after == balance_before + mints)

# # ownerOf assert
# def test_owner_of(token):
#     owner = accounts[0]
#     user = accounts[1]
#     mints = 1
#     token.setWhitelistUsers([user], [mints], {'from': owner})
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     token.mint(mints, {'from': user})
#     assert(user == token.ownerOf(1))

# # ownerOf assert
# def test_owner_of_nonexistent_token(token):
#     user = accounts[1]
#     with brownie.reverts("ERC721: owner query for nonexistent token"):
#         token.ownerOf(1)


# #set presale user but sale is concluded
# def test_set_presale_but_sale_over(token):
#     owner = accounts[0]
#     user = accounts[1]
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     with brownie.reverts("Presale is concluded."):
#         token.setPresaleUsers([user], {'from': owner})

# #check presale user enabled
# def test_set_presale(token):
#     owner = accounts[0]
#     user = accounts[1]
#     with brownie.reverts("User not on presale list."):
#         token.removePresaleUser(user)
#     token.setPresaleUsers([user], {'from': owner})
#     assert(token.presaleUsers(user) == True)
#     token.removePresaleUser(user)
#     assert(token.presaleUsers(user) == False)

# # mint presale
# def test_presale(token):
#     owner = accounts[0]
#     user = accounts[1]
#     user_2 = accounts[2]
#     user_3 = accounts[3]
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     token.setPresaleUsers([user], {'from': owner})
#     _nextStage(token)
#     mint = 5
#     with brownie.reverts("Not enough ether sent"):
#         token.mint(mint, {'from': user, 'value': "0 ether"})
#     token.mint(mint, {'from': user, 'value': "0.2 ether"})
#     assert(user == token.ownerOf(mint))
#     with brownie.reverts("Transaction exceeds max allowed presale mints"):
#         token.mint(1, {'from': user, 'value': "0.2 ether"})
#     with brownie.reverts("Address not on presale list"):
#         token.mint(mint, {'from': user_2, 'value': "0.2 ether"})
#     token.setPresaleUsers([user_2], {'from': owner})
#     token.mint(mint, {'from': user_2, 'value': "0.2 ether"})
#     token.setPresaleUsers([user_3], {'from': owner})
#     with brownie.reverts("Transaction exceeds pre-sale supply"):
#         token.mint(mint, {'from': user_3, 'value': "0.2 ether"})
#     assert(token.totalSupply() == mint + mint)
#     assert(token.presaleMintCount(user_2) == mint)

# def test_ERC615(token):
#     # ERC721
#     assert(True == token.supportsInterface("0x80ac58cd"))
#     # ERC165 itself
#     assert(True == token.supportsInterface("0x01ffc9a7"))
#     # ERC721 Metadata 
#     assert(True == token.supportsInterface("0x5b5e139f"))

# def test_name_symbol(token):
#     name = token.name()
#     symbol = token.symbol()
#     assert(len(name) > 0)
#     assert(len(symbol) > 0)

# # test team mint
# def test_team_mint(token):
#     owner = accounts[0]
#     user = accounts[1]
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     mint = 5
#     balance_before = token.balanceOf(owner)
#     token.mint(mint, {'from': owner})
#     balance_after = token.balanceOf(owner)
#     assert(balance_after == balance_before + mint)
#     with brownie.reverts("Only Owner can mint at this stage"):
#         token.mint(mint, {'from': user})
#     token.mint(mint, {'from': owner})
#     with brownie.reverts("Transaction exceeds total team-sale supply"):
#         token.mint(mint, {'from': owner})
#     assert(token.teamMintCount() == 10)

# def test_public_sale(token):
#     user = accounts[1]
#     mint = 5
#     _setFreezeProvenance(token)
#     with brownie.reverts("Minting not initiated. Currenly on stage 0 (init)."):
#         token.mint(mint, {'from': user, 'value': "0.3 ether"})
#     _nextStage(token)
#     with brownie.reverts("Mint amount must be greater than 0"):
#         token.mint(0, {'from': user, 'value': "0.3 ether"})
#     with brownie.reverts("Exceeds max allowed amount per transaction"):
#         token.mint(mint + 1, {'from': user, 'value': "0.3 ether"})
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     balance_before = token.balanceOf(user)
#     token.mint(mint, {'from': user, 'value': "0.3 ether"})
#     balance_after = token.balanceOf(user)
#     assert(balance_after == balance_before + mint)
#     token.mint(mint, {'from': user, 'value': "0.3 ether"})
#     token.mint(mint, {'from': user, 'value': "0.3 ether"})
#     token.mint(mint, {'from': user, 'value': "0.3 ether"})
#     token.mint(mint, {'from': user, 'value': "0.3 ether"})
#     token.mint(mint, {'from': user, 'value': "0.3 ether"})
#     with brownie.reverts("Transaction exceeds total sale supply"):
#         token.mint(mint, {'from': user, 'value': "0.3 ether"})
#     with brownie.reverts("Not enough ether sent"):
#         token.mint(mint, {'from': user, 'value': "0.2 ether"})

# # mint as zero address during public sale - will revert
# def test_public_sale_to_non_erc_contract(token):
#     owner = accounts[0]
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     tokens = 5
#     test = accounts[0].deploy(TestContract).address
#     accounts[0].transfer(test, "10 ether", gas_price=0)
#     with brownie.reverts("ERC721: transfer to non ERC721Receiver implementer"):
#         token.mint(tokens, {'from': test, 'value': "0.3 ether"})

# def test_set_frozen_base_uri(token):
#     owner = accounts[0]
#     user = accounts[1]
#     with brownie.reverts("baseURI cannot be empty"):
#         token.freezeBaseURI({'from': owner})
#     baseUri = "http://testuri.io/"
#     token.setBaseURI(baseUri, {'from': owner})
#     assert(token.baseURI() == baseUri)
#     with brownie.reverts("Ownable: caller is not the owner"):
#         token.setBaseURI(baseUri, {'from': user})
#     token.freezeBaseURI({'from': owner})
#     assert(token.tokenURIFrozen() == True)
#     with brownie.reverts("BaseURI is already frozen."):
#         token.freezeBaseURI({'from': owner})
#     with brownie.reverts("BaseURI is frozen."):
#         token.setBaseURI(baseUri, {'from': owner})




# # mint a token to a receiver contract
# def test_public_sale_to_contract(token):
#     owner = accounts[0]
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     tokens = 1
#     test = accounts[0].deploy(ReceiverContract).address
#     accounts[0].transfer(test, "10 ether", gas_price=0)
#     txn_receipt = token.mint(tokens, {'from': test, 'value': "0.3 ether"})
#     assert(test == token.ownerOf(tokens))
#     event = txn_receipt.events['Transfer']
#     assert(event['tokenId'] == tokens)
#     assert(event['from'] == "0x"+"0"*40)
#     assert(event['to'] == test)
#     token.pause({'from':owner})
#     with brownie.reverts('Pausable: paused'):
#         token.mint(tokens, {'from': test, 'value': "0.3 ether"})


# def test_mint_four_person(token):
#     user_1 = accounts[1]
#     user_2 = accounts[2]
#     user_3 = accounts[3]
#     user_4 = accounts[4]
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     txn_1 = token.mint(1, {'from': user_1, 'value': "0.06 ether"})
#     txn_2 = token.mint(1, {'from': user_2, 'value': "0.06 ether"})
#     txn_3 = token.mint(1, {'from': user_3, 'value': "0.06 ether"})
#     txn_4 = token.mint(1, {'from': user_4, 'value': "0.06 ether"})
#     assert(user_1 == token.ownerOf(1))
#     assert(user_2 == token.ownerOf(2))
#     assert(user_3 == token.ownerOf(3))
#     assert(user_4 == token.ownerOf(4))

#     event = txn_1.events['Transfer']
#     assert(event['tokenId'] == 1)
#     assert(event['from'] == "0x"+"0"*40)
#     assert(event['to'] == user_1)

#     event = txn_2.events['Transfer']
#     assert(event['tokenId'] == 2)
#     assert(event['from'] == "0x"+"0"*40)
#     assert(event['to'] == user_2)

#     event = txn_3.events['Transfer']
#     assert(event['tokenId'] == 3)
#     assert(event['from'] == "0x"+"0"*40)
#     assert(event['to'] == user_3)

#     event = txn_4.events['Transfer']
#     assert(event['tokenId'] == 4)
#     assert(event['from'] == "0x"+"0"*40)
#     assert(event['to'] == user_4)        

# # Inquire the balance for the zero address - this should raise an exception
# def test_balanceOfZeroAddress(token):
#     with brownie.reverts('ERC721: balance query for the zero address'):
#         balance = token.balanceOf("0x"+"0"*40)

# # Inquire the balance for a non-zero address 
# def test_balance_of_non_zero_address(token):
#     balance = token.balanceOf("0x1"+"0"*39)
#     assert(0 == balance);   

# # Burn a token
# def test_burn(token):
#     user = accounts[1]
#     tokens = 1
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     token.mint(1, {'from': user, 'value': "0.06 ether"})
#     txn_receipt = token.burn(tokens, {"from": user})
#     _verifyTransferEvent(txn_receipt, user, "0x"+40*"0", tokens)

# # Burn a token when not owner, willr evert
# def test_burn_as_not_owner(token):
#     owner = accounts[0]
#     user = accounts[1]
#     tokens = 1
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     token.mint(1, {'from': user, 'value': "0.06 ether"})
#     with brownie.reverts('ERC721Burnable: caller is not owner nor approved'):
#         token.burn(tokens, {"from": owner})

# # Test a valid transfer, initiated by the current owner of the token
# def test_transfer_from(token):
#     owner = accounts[0]
#     user = accounts[1]
#     tokenID = 1
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     token.mint(tokenID, {'from': owner, 'value': "0.06 ether"})
#     oldBalanceMe = token.balanceOf(owner)
#     oldBalanceAlice = token.balanceOf(user)
#     txn_receipt = token.transferFrom(owner, user, tokenID, {"from": owner})
#     assert(user == token.ownerOf(tokenID))
#     newBalanceMe = token.balanceOf(owner)
#     newBalanceAlice = token.balanceOf(user)
#     assert (newBalanceMe + 1 == oldBalanceMe)
#     assert (oldBalanceAlice + 1 == newBalanceAlice)
#     _verifyTransferEvent(txn_receipt, owner, user, tokenID)

# # transfer from non-owner
# def test_transfer_from_non_owner(token):
#     owner = accounts[0]
#     user = accounts[1]
#     user_2 = accounts[2]
#     tokenID = 1
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     token.mint(tokenID, {'from': owner, 'value': "0.06 ether"})
#     with brownie.reverts("ERC721: transfer caller is not owner nor approved"):
#         token.transferFrom(user_2, user, tokenID,{"from": user_2})

# # Test an invalid transfer - to is the zero address
# def test_transfer_to_zero_address(token):
#     owner = accounts[0]
#     tokenID = 1
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     token.mint(tokenID, {'from': owner, 'value': "0.06 ether"})
#     # Now do the transfer
#     with brownie.reverts('ERC721: transfer to the zero address'):
#         token.transferFrom(owner, "0x"+40*"0", tokenID, {"from": owner})

# # transfer from non owner
# def test_transfer_from_non_approved_owner(token):
#     owner = accounts[0]
#     user = accounts[1]
#     user_2 = accounts[2]
#     tokenID = 1
#     _setFreezeProvenance(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     _nextStage(token)
#     token.mint(tokenID, {'from': owner, 'value': "0.06 ether"})
#     with brownie.reverts("ERC721: transfer caller is not owner nor approved"):
#         token.transferFrom(owner, user, tokenID,{"from": user})

# # Test a valid safe transfer, initiated by the current owner of the token
# def test_safe_transfer_from(token):
#     owner = accounts[0]
#     alice = accounts[1]
#     tokenID = 1
#     _mint(token, tokenID, owner)
#     # Remember balances
#     oldBalanceMe = token.balanceOf(owner)
#     oldBalanceAlice = token.balanceOf(alice)
#     # Now do the transfer
#     txn_receipt = token.safeTransferFrom(owner, alice, tokenID, hexbytes.HexBytes(""), {"from": owner})
#     # check owner of NFT
#     assert(alice == token.ownerOf(tokenID))
#     # Check balances
#     newBalanceMe = token.balanceOf(owner)
#     newBalanceAlice = token.balanceOf(alice)
#     assert (newBalanceMe + 1 == oldBalanceMe)
#     assert (oldBalanceAlice + 1 == newBalanceAlice)
#     # Verify that an Transfer event has been logged
#     _verifyTransferEvent(txn_receipt, owner, alice, tokenID)

# # Test an invalid safe transfer - from is not current owner
# def test_safe_transfer_from_not_owner(token):
#     me = accounts[0]
#     alice = accounts[1]
#     bob = accounts[2]
#     tokenID = 1
#     _mint(token, tokenID, me)
#     # Now do the transfer
#     with brownie.reverts("ERC721: transfer caller is not owner nor approved"):
#         token.safeTransferFrom(bob, alice, tokenID, hexbytes.HexBytes(""), {"from": bob})

# # Test an safe invalid transfer - to is the zero address
# def test_safe_transfer_from_to_zero_address(token):
#     me = accounts[0]
#     tokenID = 1
#     _mint(token, tokenID, me)
#     # Now do the transfer
#     with brownie.reverts("ERC721: transfer to the zero address"):
#         token.safeTransferFrom(me, "0x"+40*"0", tokenID, hexbytes.HexBytes(""), {"from": me})

# # Test an invalid safe transfer - invalid token ID
# def test_safe_transfer_from_to_zero_address(token):
#     me = accounts[0]
#     alice = accounts[1]
#     tokenID = 1
#     with brownie.reverts("ERC721: operator query for nonexistent token"):
#         token.safeTransferFrom(me, alice, tokenID, hexbytes.HexBytes(""), {"from": me})

# # Test an invalid safe transfer - not authorized
# def test_safe_transfer_from_not_authorized(token):
#     me = accounts[0]
#     alice = accounts[1]
#     bob = accounts[2]
#     tokenID = 1
#     _mint(token, tokenID, me)
#     # Now do the transfer
#     with brownie.reverts("ERC721: transfer caller is not owner nor approved"):
#         token.safeTransferFrom(me, alice, tokenID, hexbytes.HexBytes(""), {"from": bob})

# # Test a valid safe transfer to a contract returning the proper magic value
# def test_safe_transfer_from(token):
#     data = "0x1234"
#     me = accounts[0]
#     tokenID = 1
#     _mint(token, tokenID, me)
#     tokenReceiver = accounts[0].deploy(ReceiverContract)
#     oldInvocationCount = tokenReceiver.getInvocationCount()
#     # Remember balances
#     oldBalanceMe = token.balanceOf(me)
#     oldBalanceToken = token.balanceOf(tokenReceiver.address)
#     # Make sure that the contract returns the correct magic value
#     tokenReceiver.setReturnCorrectValue(True)
#     # Now do the transfer
#     txn_receipt = token.safeTransferFrom(me, tokenReceiver.address, tokenID, hexbytes.HexBytes(data), {"from": me})
#     # check owner of NFT
#     assert(tokenReceiver.address == token.ownerOf(tokenID))
#     # Check balances
#     newBalanceMe = token.balanceOf(me)
#     newBalanceToken = token.balanceOf(tokenReceiver.address)
#     assert (newBalanceMe + 1 == oldBalanceMe)
#     assert (oldBalanceToken + 1 == newBalanceToken)
#     # get current invocation count of test contract
#     newInvocationCount = tokenReceiver.getInvocationCount()
#     assert(oldInvocationCount + 1 == newInvocationCount)
#     # Check that data has been stored
#     assert(tokenReceiver.getData() == data)
#     # Verify that an Transfer event has been logged
#     _verifyTransferEvent(txn_receipt, me, tokenReceiver.address, tokenID)

# #
# # Test a valid safe transfer to a contract returning the wrong proper magic value
# #
# def test_safe_transfer_from_wrong_magic_value(token):
#     me = accounts[0]
#     tokenID = 1
#     _mint(token, tokenID, me)
#     tokenReceiver = accounts[0].deploy(ReceiverContract)
#     # Make sure that the contract returns the wrong magic value
#     tokenReceiver.setReturnCorrectValue(False)
#     # Now do the transfer
#     with brownie.reverts("ERC721: transfer to non ERC721Receiver implementer"):
#         token.safeTransferFrom(me, tokenReceiver.address, tokenID, hexbytes.HexBytes(""), {"from": me})
#     # Reset behaviour of test contract
#     tokenReceiver.setReturnCorrectValue(True)

# # Test a valid safe transfer to a contract returning the proper magic value - no data
# def test_safe_transfer_from_no_data(token):
#     me = accounts[0]
#     tokenID = 1
#     _mint(token, tokenID, me)
#     tokenReceiver = accounts[0].deploy(ReceiverContract)
#     # get current invocation count of test contract
#     oldInvocationCount = tokenReceiver.getInvocationCount()
#     # Remember balances
#     oldBalanceMe = token.balanceOf(me)
#     oldBalanceToken = token.balanceOf(tokenReceiver.address)
#     # Make sure that the contract returns the correct magic value
#     tokenReceiver.setReturnCorrectValue(True)
#     # Now do the transfer
#     txn_receipt = token.safeTransferFrom(me, tokenReceiver.address, tokenID,  {"from": me})
#     # check owner of NFT
#     assert(tokenReceiver.address == token.ownerOf(tokenID))
#     # Check balances
#     newBalanceMe = token.balanceOf(me)
#     newBalanceToken = token.balanceOf(tokenReceiver.address)
#     assert (newBalanceMe + 1 == oldBalanceMe)
#     assert (oldBalanceToken + 1 == newBalanceToken)
#     # get current invocation count of test contract
#     newInvocationCount = tokenReceiver.getInvocationCount()
#     assert(oldInvocationCount + 1 == newInvocationCount)
#     # Verify that an Transfer event has been logged
#     _verifyTransferEvent(txn_receipt, me, tokenReceiver.address, tokenID)

# # Test an approval which is not authorized
# def test_approval_not_authorized(token):
#     me = accounts[0]
#     alice = accounts[1]
#     tokenID = 1
#     _mint(token, tokenID, me)
#     with brownie.reverts("ERC721: approve caller is not owner nor approved for all"):
#         token.approve(alice, tokenID, {"from": alice})

# # Test setting and getting approval
# def test_approval(token):
#     me = accounts[0]
#     bob = accounts[2]
#     tokenID = 1
#     # Get approval - should raise
#     with brownie.reverts("ERC721: approved query for nonexistent token"):
#         token.getApproved(tokenID)
#     # Approve - should raise
#     with brownie.reverts("ERC721: owner query for nonexistent token"):
#         token.approve(bob, tokenID, {"from": me})
#     # Mint
#     _mint(token, tokenID, me)
#     # Approve for bob 
#     txn_receipt = token.approve(bob, tokenID, {"from": me})
#     # Check
#     assert(bob == token.getApproved(tokenID))
#     # Verify events
#     _verifyApprovalEvent(txn_receipt, me, bob, tokenID) # owner, approved, tokenID

# # Test that approval is reset to zero address if token is transferred
# def test_approval_reset_upon_transfer(token):
#     me = accounts[0]
#     alice = accounts[1]
#     bob = accounts[2]
#     tokenID = 1
#     _mint(token, tokenID, me)
#     # Approve for bob 
#     token.approve(bob, tokenID, {"from": me})
#     # Check
#     assert(bob == token.getApproved(tokenID))
#     # Do transfer
#     token.transferFrom(me, alice, tokenID, {"from": bob})
#     # Check that approval has been reset
#     assert(("0x"+40*"0") == token.getApproved(tokenID))

# # Test setting and clearing the operator flag
# def test_set_get_operator(token):
#     me = accounts[0]
#     alice = accounts[1]
#     bob = accounts[2]
#     assert(False == token.isApprovedForAll(me, bob))
#     assert(False == token.isApprovedForAll(me, alice))
#     # Declare bob as operator for me 
#     txn_receipt = token.setApprovalForAll(bob, True, {"from": me})
#     # Check
#     assert(True == token.isApprovedForAll(me, bob))
#     assert(False == token.isApprovedForAll(me, alice))
#     # Check events
#     _verifyApprovalForAllEvent(txn_receipt, me, bob, True)
#     # Do the same for alice
#     txn_receipt = token.setApprovalForAll(alice, True, {"from": me})
#     # Check
#     assert(True == token.isApprovedForAll(me, bob))
#     assert(True == token.isApprovedForAll(me, alice))
#     # Check events
#     _verifyApprovalForAllEvent(txn_receipt, me, alice, True)
#     # Reset both
#     txn_receipt = token.setApprovalForAll(bob, False, {"from": me})
#     # Check events
#     _verifyApprovalForAllEvent(txn_receipt, me, bob, False)
#     txn_receipt = token.setApprovalForAll(alice, False, {"from": me})
#     # Check events
#     _verifyApprovalForAllEvent(txn_receipt, me, alice, False)
#     # Check
#     assert(False == token.isApprovedForAll(me, bob))
#     assert(False == token.isApprovedForAll(me, alice))

# # Test authorization logic for setting and getting approval
# def test_approval_authorization(token):
#     me = accounts[0]
#     alice = accounts[1]
#     bob = accounts[2]
#     tokenID = 1
#     _mint(token, tokenID, me)
#     # Try to approve for bob while not being owner or operator - this should raise an exception
#     with brownie.reverts("ERC721: approve caller is not owner nor approved for all"):
#         token.approve(bob, tokenID, {"from": alice})
#     # Now make alice an operator for me
#     token.setApprovalForAll(alice, True, {"from": me})
#     # Approve for bob again - this should now work
#     txn_receipt = token.approve(bob, tokenID, {"from": alice})
#     # Check
#     assert(bob == token.getApproved(tokenID))
#     # Verify events
#     _verifyApprovalEvent(txn_receipt, me, bob, tokenID)
#     # Reset
#     token.setApprovalForAll(alice, False, {"from": me})

# # Test a valid transfer, initiated by an operator for the current owner of the token
# def test_transfer_from_operator(token):
#     me = accounts[0]
#     alice = accounts[1]
#     bob = accounts[2]
#     tokenID = 1
#     _mint(token, tokenID, me)
#     # Now make bob an operator for me
#     token.setApprovalForAll(bob, True, {"from": me})
#     # Remember balances
#     oldBalanceMe = token.balanceOf(me)
#     oldBalanceAlice = token.balanceOf(alice)
#     # Now do the transfer
#     txn_receipt = token.transferFrom(me, alice, tokenID, {"from": bob})
#     # Reset
#     token.setApprovalForAll(bob, False, {"from": me})
#     # check owner of NFT
#     assert(alice == token.ownerOf(tokenID))
#     # Check balances
#     newBalanceMe = token.balanceOf(me)
#     newBalanceAlice = token.balanceOf(alice)
#     assert (newBalanceMe + 1 == oldBalanceMe)
#     assert (oldBalanceAlice + 1 == newBalanceAlice)
#     # Verify that an Transfer event has been logged
#     _verifyTransferEvent(txn_receipt, me, alice, tokenID)

# def test_last_mint_address(token):
#     me = accounts[0]
#     tokenID = 1
#     with brownie.reverts("No cryptid exists yet."):
#             token.lastMintAddress()
#     _mint(token, tokenID, me)
#     assert(token.lastMintAddress() == me)

# def test_last_mint_id(token):
#     me = accounts[0]
#     tokenID = 1
#     with brownie.reverts("No cryptid exists yet."):
#             token.lastMintID()
#     _mint(token, tokenID, me)
#     assert(token.lastMintID() == tokenID)

# def test_set_presale_price(token):
#     me = accounts[0]
#     alice = accounts[1]
#     bob = accounts[2]
#     tokenID = 1
#     presale_price = 50000000000000000
#     token.setPresalePrice(presale_price)
#     assert(token.presalePrice() == presale_price)

# def test_token_uri(token):
#     owner = accounts[0]
#     tokenID = 1
#     _mint(token, tokenID, owner)
#     with brownie.reverts("ERC721Metadata: URI query for nonexistent token"):
#         token.tokenURI(2)
#     token.setBaseURI("http://baseuri.com/", {'from': owner})
#     assert(token.tokenURI(1) == "http://baseuri.com/1.json")

# def test_withdraw(token):
#     owner = accounts[0]
#     chris = accounts[1]
#     chris_before = chris.balance()
#     steph = accounts[2]
#     steph_before = steph.balance()
#     tokenID = 1
#     with brownie.reverts("Ownable: caller is not the owner"):
#         token.withdraw({'from': chris})
#     with brownie.reverts("Contract balance is 0."):
#         token.withdraw({'from': owner})
#     _mint(token, tokenID, owner)
#     token.setWithdrawAddress(chris, steph, {'from':owner})
#     assert(token.balance() == "0.06 ether")
#     token.withdraw({'from':owner})
#     assert(steph.balance() == steph_before + "0.03 ether")
#     assert(chris.balance() == chris_before + "0.03 ether")
#     with brownie.reverts("Contract balance is 0."):
#         token.withdraw({'from':owner})
#     test = accounts[0].deploy(NonreceiverContract).address
#     token.mint(tokenID, {'from': owner, 'value': "0.06 ether"})
#     token.setWithdrawAddress(test, steph, {'from':owner})
#     pre_balance = token.balance()
#     with brownie.reverts("withdrawl 1 failed"):
#         token.withdraw({'from':owner})
#     assert(token.balance() == "0.06 ether")
#     token.setWithdrawAddress(steph, test, {'from':owner})
#     with brownie.reverts("withdrawl 2 failed"):
#         token.withdraw({'from':owner})

# def test_transfer_ownership(token):
#     owner = accounts[0]
#     chris = accounts[1]
#     steph = accounts[2]
#     with brownie.reverts("Ownable: caller is not the owner"):
#         token.transferOwnership(chris, {'from':steph})
#     token.transferOwnership(chris, {'from':owner})
#     assert(token.owner() == chris)
