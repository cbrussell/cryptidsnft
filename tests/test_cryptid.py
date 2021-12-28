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

def _setFreezeProvenance(token, provenance, owner):
    token.setProvenanceHash(provenance, {'from': owner})
    token.freezeProvenanceHash({'from': owner})

# assert balances in account 0 and 1
def test_account_balance():
    balance = accounts[0].balance()
    accounts[0].transfer(accounts[1], "10 ether", gas_price=0)
    assert balance - "10 ether" == accounts[0].balance()

# check no minting allowed after deployment as non-wner
def test_mint_after_deploy_non_owner(token):
    with brownie.reverts("Minting not initiated. Currenly on stage 0 (init)."):
        token.mint(1, {'from': accounts[1]})

# assert only owner can airdrop      
def test_airdrop_as_non_owner(token):
    with brownie.reverts("Ownable: caller is not the owner"):
        token.airdropCryptid(1, accounts[1], {'from': accounts[1]})

# mint as owner after deploy
def test_mint_after_deploy_owner(token):
    with brownie.reverts("Minting not initiated. Currenly on stage 0 (init)."):
        token.mint(1, {'from': accounts[0]})

# move from stage 0 to 1 without provenance frozen
def test_move_to_stage_1_as_owner(token):
    with brownie.reverts("Provenance hash must be frozen before minting can start."):
        token.nextStage({'from': accounts[0]})

# airdrop token 
def test_airdrop(token):
    provenance = "test provnance"
    owner = accounts[0]
    user = accounts[1]
    tokens = 5
    old_user_balance = token.balanceOf(user)
    _setFreezeProvenance(token, provenance, owner)
    token.airdropCryptid(tokens, user, {'from': owner})
    new_user_balance = token.balanceOf(user)
    assert(new_user_balance == old_user_balance + tokens)

# airdrop too many token 
def test_airdrop_too_many(token):
    provenance = "test provnance"
    owner = accounts[0]
    user = accounts[1]
    tokens = 6
    _setFreezeProvenance(token, provenance, owner)
    with brownie.reverts("Exceeds max allowed amount per transaction"):
        token.airdropCryptid(tokens, user, {'from': owner})
 


