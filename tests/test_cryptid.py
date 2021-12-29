import pytest
import brownie
from brownie import CryptidToken, TestContract, accounts, exceptions;

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

def _nextStage(token):
    owner = accounts[0]
    token.nextStage({'from': owner})

def _whitelistUser(token):
    owner = accounts[0]
    user = accounts[1]
    mints = 5
    token.setWhitelistUsers([user], [mints], {'from': owner})

# ensure whitelist works
def test_whitelist_add(token):
    owner = accounts[0]
    user = accounts[1]
    mints = 5
    mints_before = token.whitelistUsers(user)
    token.setWhitelistUsers([user], [mints], {'from': owner})
    mints_after = token.whitelistUsers(user)
    assert(mints_after == mints_before + mints)

# set whitelist after whitelist sale
def test_whitelist_after_sale(token):
    owner = accounts[0]
    user = accounts[1]
    mints = 5
    _setFreezeProvenance(token)
    _nextStage(token)
    _nextStage(token)
    with brownie.reverts("Whitelist sale is concluded."):
        token.setWhitelistUsers([user], [mints], {'from': owner})

# remove whitelist user
def test_remove_whitelist_mints(token):
    owner = accounts[0]
    user = accounts[1]
    mints = 5
    mints_before = token.whitelistUsers(user)
    token.setWhitelistUsers([user], [mints], {'from': owner})
    mints_after = token.whitelistUsers(user)
    assert(mints_after == mints + mints_before)
    token.removeWhitelistUser(user, {'from': owner})
    mints_after_removal = token.whitelistUsers(user)
    assert(mints_after_removal == 0)


# remove whitelist after whitelist sale
def test_remove_whitelist_after_whitelist_sale(token):
    owner = accounts[0]
    user = accounts[1]
    _whitelistUser(token)
    _setFreezeProvenance(token)
    _nextStage(token)
    _nextStage(token)
    with brownie.reverts("Whitelist sale is concluded."):
        token.removeWhitelistUser(user, {'from': owner})
        
def test_remove_whitelist_after_finished_minting(token):
    owner = accounts[0]
    user = accounts[1]
    mints = 5
    token.setWhitelistUsers([user], [mints], {'from': owner})
    _setFreezeProvenance(token)
    _nextStage(token)
    balance_before = token.balanceOf(user)
    token.mint(mints, {'from': user})
    balance_after = token.balanceOf(user)
    assert(balance_after == balance_before + mints)
    token.removeWhitelistUser(user, {'from': owner})
    assert(token.whitelistUsers(user) == 0)

def test_user_not_on_whitelist(token):
    owner = accounts[0]
    user = accounts[1]
    second_user = accounts[2]
    mints = 5
    token.setWhitelistUsers([user], [mints], {'from': owner})
    _setFreezeProvenance(token)
    _nextStage(token)
    with brownie.reverts("User is not on whitelist."):
        token.removeWhitelistUser(second_user, {'from': owner})

# provenance has is frozen
def test_freeze_provenance(token):
    owner = accounts[0]
    new_provenance = "testing 1 2 3"
    token.setProvenanceHash(new_provenance, {'from': owner})
    token.freezeProvenanceHash({'from': owner})
    assert(token.provenanceHashFrozen() == True)

# initial provenance is unfrozen
def test_freeze_provenance(token):
    assert(token.provenanceHashFrozen() == False)

# assert balances in account 0 and 1
def test_account_balance():
    balance = accounts[0].balance()
    accounts[0].transfer(accounts[1], "10 ether", gas_price=0)
    assert balance - "10 ether" == accounts[0].balance()

# check no minting allowed after deployment as non-wner
def test_mint_after_deploy_non_owner(token):
    user = accounts[1]
    with brownie.reverts("Minting not initiated. Currenly on stage 0 (init)."):
        token.mint(1, {'from': user})

# assert only owner can airdrop      
def test_airdrop_as_non_owner(token):
    user = accounts[1]
    with brownie.reverts("Ownable: caller is not the owner"):
        token.airdropCryptid(1, user, {'from': user})

# mint as owner after deploy
def test_mint_after_deploy_owner(token):
    owner = accounts[0]
    with brownie.reverts("Minting not initiated. Currenly on stage 0 (init)."):
        token.mint(1, {'from': owner})

# move from stage 0 to 1 without provenance frozen
def test_move_to_stage_1_before_provenance(token):
    owner = accounts[0]
    with brownie.reverts("Provenance hash must be frozen before minting can start."):
        token.nextStage({'from': owner})

def test_move_to_stage_1_after_provenance(token):
    owner = accounts[0]
    _setFreezeProvenance(token)
    stage_before = token.getStage()
    token.nextStage({'from': owner})
    stage_after = token.getStage()
    assert(stage_after == stage_before + 1)

# no stages after 4

def test_only_four_stages(token):
    owner = accounts[0]
    _setFreezeProvenance(token)
    _nextStage(token)
    _nextStage(token)
    _nextStage(token)
    _nextStage(token)
    with brownie.reverts("No stages after public sale"):
        token.nextStage({'from': owner})


# airdrop before provenance is set

def test_airdrop_before_provinence_set(token):
    owner = accounts[0]
    user = accounts[1]
    tokens = 5
    with brownie.reverts("Provenance hash must be frozen before minting can start."):
        token.airdropCryptid(tokens, user, {'from': owner})

# airdrop token 
def test_airdrop(token):
    owner = accounts[0]
    user = accounts[1]
    tokens = 5
    old_user_balance = token.balanceOf(user)
    _setFreezeProvenance(token)
    token.airdropCryptid(tokens, user, {'from': owner})
    new_user_balance = token.balanceOf(user)
    assert(new_user_balance == old_user_balance + tokens)

# airdrop too many token 
def test_airdrop_too_many(token):
    owner = accounts[0]
    user = accounts[1]
    maxTx = token.maxMintPerTx()
    tokens = maxTx + 1
    _setFreezeProvenance(token)
    with brownie.reverts("Exceeds max allowed amount per transaction"):
        token.airdropCryptid(tokens, user, {'from': owner})

def test_airdrop_to_contract(token):
    owner = accounts[0]
    user = accounts[1]
    tokens = 2
    _setFreezeProvenance(token)
    test = accounts[0].deploy(TestContract).address
    # test_address = test.address()
    with brownie.reverts("ERC721: transfer to non ERC721Receiver implementer"):
        token.airdropCryptid(tokens, test, {'from': owner})

def test_airdrop_to_zero(token):
    owner = accounts[0]
    user = "0x0000000000000000000000000000000000000000"
    tokens = 2
    _setFreezeProvenance(token)
    with brownie.reverts():
        token.airdropCryptid(tokens, user, {'from': owner})

# airdrop at whitelist
def test_airdrop_at_whitelist(token):
    owner = accounts[0]
    user = accounts[1]
    tokens = 5
    old_user_balance = token.balanceOf(user)
    _setFreezeProvenance(token)
    _nextStage(token)
    token.airdropCryptid(tokens, user, {'from': owner})
    new_user_balance = token.balanceOf(user)
    assert(new_user_balance == old_user_balance + tokens)

# airdrop at  presale
def test_airdrop_at_presale(token):
    owner = accounts[0]
    user = accounts[1]
    tokens = 5
    _setFreezeProvenance(token)
    _nextStage(token)
    _nextStage(token)
    with brownie.reverts("Past whitelist sale."):
        token.airdropCryptid(tokens, user, {'from': owner})

# airdrop 0 tokens
def test_airdrop_at_whitelist_zero_tokens(token):
    owner = accounts[0]
    user = accounts[1]
    tokens = 0
    _setFreezeProvenance(token)
    _nextStage(token)
    with brownie.reverts("Airdrop amount must be greater than 0"):
        token.airdropCryptid(tokens, user, {'from': owner})

# airdrop too many tokens
def test_airdrop_at_whitelist_too_many_tx(token):
    owner = accounts[0]
    user = accounts[1]
    maxTx = token.maxMintPerTx()
    tokens = maxTx + 1
    _setFreezeProvenance(token)
    _nextStage(token)
    with brownie.reverts("Exceeds max allowed amount per transaction"):
        token.airdropCryptid(tokens, user, {'from': owner})

# airdrop beyond presale amount
def test_airdrop_at_whitelist_beyone_presale_amount(token):
    owner = accounts[0]
    user = accounts[1]
    tokens = 5
    _setFreezeProvenance(token)
    _nextStage(token)
    token.airdropCryptid(tokens, user, {'from': owner})
    token.airdropCryptid(tokens, user, {'from': owner})
    with brownie.reverts("Mint amount will exceed presale supply."): #presale supply is 10
        token.airdropCryptid(tokens, user, {'from': owner})

# freeze provenance hash with nothing set
def test_freeze_empty_provenance(token):
    owner = accounts[0]
    new_provenance = ""
    token.setProvenanceHash(new_provenance, {'from': owner})
    with brownie.reverts("Provenance hash cannot be empty."):
        token.freezeProvenanceHash({'from':owner})

# freeze already frozen provnance hash
def test_freeze_already_frozen_provenance(token):
    owner = accounts[0]
    new_provenance = "test provenance hash"
    token.setProvenanceHash(new_provenance, {'from': owner})
    token.freezeProvenanceHash({'from':owner})
    with brownie.reverts("Provenance hash is already frozen."):
        token.freezeProvenanceHash({'from':owner})

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

# test mint at stage 0
def test_mint_stage_zero(token):
    owner = accounts[0]
    _setFreezeProvenance(token)
    with brownie.reverts("Minting not initiated. Currenly on stage 0 (init)."):
        token.mint(1, {'from': owner})

# mint zero token as whitelisted - will revert due to overflow error
def test_mint_exceed_whitelisted(token):
    owner = accounts[0]
    user = accounts[1]
    _setFreezeProvenance(token)
    _nextStage(token)
    mints = 2
    token.setWhitelistUsers([user], [mints], {'from': owner})
    with brownie.reverts("Transaction exceeds remaining whitelist mints"):
        token.mint(3, {'from': user})

# mint as non whitelist user
def test_whitelist_not_on_list(token):
    owner = accounts[0]
    user = accounts[1]
    _setFreezeProvenance(token)
    _nextStage(token)
    mints = 2
    with brownie.reverts("Minter not whitelisted."):
        token.mint(mints, {'from': user})


# whitelist mint
def test_whitelist_mint(token):
    owner = accounts[0]
    user = accounts[1]
    mints = 5
    token.setWhitelistUsers([user], [mints], {'from': owner})
    _setFreezeProvenance(token)
    _nextStage(token)
    balance_before = token.balanceOf(user)
    token.mint(mints, {'from': user})
    balance_after = token.balanceOf(user)
    assert(balance_after == balance_before + mints)

# ownerOf assert
def test_owner_of(token):
    owner = accounts[0]
    user = accounts[1]
    mints = 1
    token.setWhitelistUsers([user], [mints], {'from': owner})
    _setFreezeProvenance(token)
    _nextStage(token)
    token.mint(mints, {'from': user})
    assert(user == token.ownerOf(1))

# ownerOf assert
def test_owner_of_nonexistent_token(token):
    user = accounts[1]
    with brownie.reverts("ERC721: owner query for nonexistent token"):
        token.ownerOf(1)


#set presale user but sale is concluded
def test_set_presale_but_sale_over(token):
    owner = accounts[0]
    user = accounts[1]
    _setFreezeProvenance(token)
    _nextStage(token)
    _nextStage(token)
    _nextStage(token)
    with brownie.reverts("Presale is concluded."):
        token.setPresaleUsers([user], {'from': owner})

#check presale user enabled
def test_set_presale(token):
    owner = accounts[0]
    user = accounts[1]
    token.setPresaleUsers([user], {'from': owner})
    assert(token.presaleUsers(user) == True)

# mint presale
def test_presale(token):
    owner = accounts[0]
    user = accounts[1]
    user_2 = accounts[2]
    user_3 = accounts[3]
    _setFreezeProvenance(token)
    _nextStage(token)
    token.setPresaleUsers([user], {'from': owner})
    _nextStage(token)
    mint = 5
    with brownie.reverts("Not enough ether sent"):
        token.mint(mint, {'from': user, 'value': "0 ether"})
    token.mint(mint, {'from': user, 'value': "0.2 ether"})
    assert(user == token.ownerOf(mint))
    with brownie.reverts("Transaction exceeds max allowed presale mints"):
        token.mint(1, {'from': user, 'value': "0.2 ether"})
    with brownie.reverts("Address not on presale list"):
        token.mint(mint, {'from': user_2, 'value': "0.2 ether"})
    token.setPresaleUsers([user_2], {'from': owner})
    token.mint(mint, {'from': user_2, 'value': "0.2 ether"})
    token.setPresaleUsers([user_3], {'from': owner})
    with brownie.reverts("Transaction exceeds pre-sale supply"):
        token.mint(mint, {'from': user_3, 'value': "0.2 ether"})
    assert(token.totalSupply() == mint + mint)
    assert(token.presaleMintCount(user_2) == mint)

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

# test team mint
def test_team_mint(token):
    owner = accounts[0]
    user = accounts[1]
    _setFreezeProvenance(token)
    _nextStage(token)
    _nextStage(token)
    _nextStage(token)
    mint = 5
    balance_before = token.balanceOf(owner)
    token.mint(mint, {'from': owner})
    balance_after = token.balanceOf(owner)
    assert(balance_after == balance_before + mint)
    with brownie.reverts("Only Owner can mint at this stage"):
        token.mint(mint, {'from': user})
    token.mint(mint, {'from': owner})
    with brownie.reverts("Transaction exceeds total team-sale supply"):
        token.mint(mint, {'from': owner})
    assert(token.teamMintCount() == 10)

def test_public_sale(token):
    user = accounts[1]
    mint = 5
    _setFreezeProvenance(token)
    with brownie.reverts("Minting not initiated. Currenly on stage 0 (init)."):
        token.mint(mint, {'from': user, 'value': "0.3 ether"})
    _nextStage(token)
    with brownie.reverts("Mint amount must be greater than 0"):
        token.mint(0, {'from': user, 'value': "0.3 ether"})
    with brownie.reverts("Exceeds max allowed amount per transaction"):
        token.mint(mint + 1, {'from': user, 'value': "0.3 ether"})
    _nextStage(token)
    _nextStage(token)
    _nextStage(token)
    balance_before = token.balanceOf(user)
    token.mint(mint, {'from': user, 'value': "0.3 ether"})
    balance_after = token.balanceOf(user)
    assert(balance_after == balance_before + mint)
    token.mint(mint, {'from': user, 'value': "0.3 ether"})
    token.mint(mint, {'from': user, 'value': "0.3 ether"})
    token.mint(mint, {'from': user, 'value': "0.3 ether"})
    token.mint(mint, {'from': user, 'value': "0.3 ether"})
    token.mint(mint, {'from': user, 'value': "0.3 ether"})
    with brownie.reverts("Transaction exceeds total sale supply"):
        token.mint(mint, {'from': user, 'value': "0.3 ether"})
    with brownie.reverts("Not enough ether sent"):
        token.mint(mint, {'from': user, 'value': "0.2 ether"})

# mint as zero address during public sale - will revert
def test_public_sale_to_contract(token):
    owner = accounts[0]
    _setFreezeProvenance(token)
    _nextStage(token)
    _nextStage(token)
    _nextStage(token)
    _nextStage(token)
    tokens = 5
    test = accounts[0].deploy(TestContract).address
    accounts[0].transfer(test, "10 ether", gas_price=0)
    with brownie.reverts():
        token.mint(tokens, {'from': test, 'value': "0.3 ether"})

def test_set_frozen_base_uri(token):
    owner = accounts[0]
    with brownie.reverts("baseURI cannot be empty"):
        token.freezeBaseURI({'from': owner})
    baseUri = "http://testuri.io/"
    token.setBaseURI(baseUri, {'from': owner})
    assert(token.baseURI() == baseUri)
    token.freezeBaseURI({'from': owner})
    assert(token.tokenURIFrozen() == True)
    with brownie.reverts("BaseURI is already frozen."):
        token.freezeBaseURI({'from': owner})

def test_set_default_uri(token):
    owner = accounts[0]
    new_defaultURI = "test"
    token.setDefaultURI(new_defaultURI, {'from':owner})
    assert(token.defaultURI() == new_defaultURI)
