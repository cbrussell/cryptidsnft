import pytest
import brownie
from brownie import CryptidToken, accounts, exceptions;

# deploy CryptidToken
@pytest.fixture(scope="module", autouse=True)
def token():
    return accounts[0].deploy(CryptidToken, "Cryptids", "CRYPTID", "", 30, 10, 100, 5)

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
def test_move_to_stage_1_as_owner(token):
    owner = accounts[0]
    with brownie.reverts("Provenance hash must be frozen before minting can start."):
        token.nextStage({'from': owner})

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