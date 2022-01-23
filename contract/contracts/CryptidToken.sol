// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import '@openzeppelin/contracts/token/ERC721/ERC721.sol';
import '@openzeppelin/contracts/access/Ownable.sol';
import '@openzeppelin/contracts/utils/math/SafeMath.sol';
import '@openzeppelin/contracts/utils/Counters.sol';
import '@openzeppelin/contracts/security/Pausable.sol';
import '@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol';
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";

contract CryptidToken is ERC721, Pausable, Ownable, ERC721Burnable{ 
    using Strings for uint256;
    using SafeMath for uint256;
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    bytes32 public merkleRoot;
    string public provenanceHash;
    string public baseURI = "";
    string public baseExtension = ".json";
    uint8 private stage = 0;
    uint8 public maxMintPerTx;     
    bool public tokenURIFrozen = false;
    bool public provenanceHashFrozen = false;
    address public withdrawDest1 = 0x1953bc1fF76f5e61cD775A4482bd85BAc56aD1Eb;
    address public withdrawDest2 = 0x12B58f5331a6DC897932AA7FB5101667ACdf03e2;
    
    // ~ Sale stages ~
    // stage 0: Init 
    // stage 1: Free Mints
    // stage 2: Whitelist
    // stage 3: Team Mint 
    // stage 4: Public Sale

    // Free mint (stage=1)
    mapping(address => uint8) public freeUsers;
    mapping(address => uint8) public freeMintCount;

    // Whitelist mint (stage=2)
    mapping(address => bool) public whitelistUsers;
    uint256 public whitelistSupply;                       
    uint256 public whitelistPrice = 0.08 ether;
    uint8 public whitelistMintMax = 2;                  
    mapping(address => uint8) public whitelistMintCount;

    // Team Mint (stage=3)
    uint256 public teamMintSupply;                          
    uint256 public teamMintCount;

    // Public Sale (stage=4)
    uint256 public salePrice = 0.08 ether;
    uint256 public totalSaleSupply;         

    constructor(
        string memory _name,
        string memory _symbol,
        string memory _baseURI,
        uint256 _whitelistSupply,
        uint256 _teamMintSupply,
        uint256 _totalSaleSupply,
        uint8 _maxMintPerTx

    )   ERC721(_name, _symbol) {
        whitelistSupply = _whitelistSupply;
        teamMintSupply = _teamMintSupply;
        totalSaleSupply = _totalSaleSupply;
        maxMintPerTx = _maxMintPerTx;
        baseURI = _baseURI;
        _tokenIdCounter.increment();
    }

    //Public mint function
    function mint(uint8 _mintAmount) public payable whenNotPaused {
        require(stage > 0, "Minting not initiated. Currenly on stage 0 (init).");
        require(_mintAmount > 0, "Mint amount must be greater than 0.");
        require(_mintAmount <= maxMintPerTx, "Exceeds max allowed amount per transaction.");
        if (stage == 1) {
        // Free Mint
            require(freeUsers[msg.sender] > 0, "Minter not awarded free mints.");
            require(_mintAmount + freeMintCount[msg.sender] <= freeUsers[msg.sender], "Transaction exceeds remaining free mints.");
            freeMintCount[msg.sender] += _mintAmount;
    }   else if (stage == 2) {
        // Whitelist
            
            require(msg.value >= whitelistPrice.mul(_mintAmount), "Not enough ether sent.");
            require(whitelistUsers[msg.sender], "Address not on whitelist.");
            require(totalSupply() + _mintAmount <= whitelistSupply, "Transaction exceeds whitelist supply.");
            require(_mintAmount + whitelistMintCount[msg.sender] <= whitelistMintMax, "Transaction exceeds max allowed whitelist mints.");      
            whitelistMintCount[msg.sender] += _mintAmount;
    }   else if (stage == 3) {
        // Team Sale
            require(owner() == msg.sender, "Only Owner can mint at this stage");
            require(_mintAmount + teamMintCount <= teamMintSupply, "Transaction exceeds total team-sale supply");      
            teamMintCount += _mintAmount;
    }   else {
        // Public Sale
            require(msg.value >= salePrice.mul(_mintAmount), "Not enough ether sent");
            require(totalSupply()  + _mintAmount <= totalSaleSupply, "Transaction exceeds total sale supply");
        }
        for (uint256 i = 1; i <= _mintAmount; i++) {
            _safeMint(msg.sender, _tokenIdCounter.current());
            _tokenIdCounter.increment();
        }
    }

    //Owner functions
    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    function airdropCryptid(uint8 _mintAmount, address _to) public onlyOwner {
        require(provenanceHashFrozen == true, "Provenance hash must be frozen before minting can start.");
        require(stage < 2, "Past free mint sale.");
        require(_mintAmount <= maxMintPerTx, "Exceeds max allowed amount per transaction");
        require(_mintAmount > 0, "Airdrop amount must be greater than 0");
        require(totalSupply()+ _mintAmount <= whitelistSupply, "Mint amount will exceed whitelist supply.");
        for (uint256 i = 1; i <= _mintAmount; i++) {
            _safeMint(_to, _tokenIdCounter.current());
            _tokenIdCounter.increment();
        }
    }

    function setfreeUsers(address[] memory _users, uint8[] memory _mints) public onlyOwner {
        require(stage < 2, "Whitelist sale is concluded.");
        for(uint256 i=0;i<_users.length;i++)
        freeUsers[_users[i]] = _mints[i];
    }

    function setWhitelistUsers(address[] memory _users) public onlyOwner {
        require(stage < 3, "Whitelist is concluded.");
        for(uint256 i=0;i<_users.length;i++)
        whitelistUsers[_users[i]] = true;
    }

    function removeFreetUser(address _user) public onlyOwner {
        require(stage < 2, "Free mint sale is concluded.");
        require(freeUsers[_user] > 0, "User not awarded free mint.");
        freeUsers[_user] = 0;
    }

    function removeWhitelistUser(address _user) public onlyOwner {
        require(whitelistUsers[_user], "User not on whitelist list.");
        whitelistUsers[_user] = false;
    }

    function setBaseURI(string memory _newBaseURI) public onlyOwner {
        require(!tokenURIFrozen, "BaseURI is frozen.");
        baseURI = _newBaseURI;
    } 
    
    function freezeBaseURI() public onlyOwner {
        require(bytes(baseURI).length > 0, "baseURI cannot be empty");
        require(!tokenURIFrozen, "BaseURI is already frozen.");
        tokenURIFrozen = true;
    }

    function nextStage() public onlyOwner {
        require(provenanceHashFrozen == true, "Provenance hash must be frozen before minting can start.");
        require(stage < 4, "No stages after public sale");
        stage++;
    }

    function prevStage() public onlyOwner {
        require(provenanceHashFrozen == true, "Provenance hash must be frozen before minting can start.");
        require(stage > 0, "No stages before init");
        stage--;
    }
    
    function setTeamMintSupply(uint256 _newTeamMintSupply) public onlyOwner {
        teamMintSupply = _newTeamMintSupply;
    }

    function setBaseExtension(string memory _newBaseExtension) public onlyOwner {
        baseExtension = _newBaseExtension;
    }

    function setWhitelistPrice(uint256 _newWhitelistPrice) public onlyOwner {
        require(stage < 3, "Whitelist is concluded.");
        whitelistPrice = _newWhitelistPrice;
    }

    function setPublicSalePrice(uint256 _newSalePrice) public onlyOwner {
        salePrice = _newSalePrice;
    }

    function setMaxMintPerTx(uint8 _newmaxMintPerTx) public onlyOwner {
        maxMintPerTx = _newmaxMintPerTx;
    }

    function setProvenanceHash(string memory _provenanceHash) public onlyOwner {
        require(!provenanceHashFrozen, "Provenance hash is frozen.");
        provenanceHash = _provenanceHash;
    }

    function setWithdrawAddress(address _dest1, address _dest2) public onlyOwner {
        withdrawDest1 = _dest1;
        withdrawDest2 = _dest2;
    }

    function freezeProvenanceHash() public onlyOwner {
        require(bytes(provenanceHash).length > 0, "Provenance hash cannot be empty.");
        require(!provenanceHashFrozen, "Provenance hash is already frozen.");
        provenanceHashFrozen = true;
    }

    function withdraw() public payable onlyOwner {
        require(address(this).balance > 0, "Contract balance is 0.");
        (bool hs, ) = payable(withdrawDest1).call{value: address(this).balance.mul(50).div(100)}("");
        require(hs, "withdrawl 1 failed");
        (bool os, ) = payable(withdrawDest2).call{value: address(this).balance}("");
        require(os, "withdrawl 2 failed");
    }

    // Public view functions
    function lastMintAddress() public view returns (address){
        require(totalSupply() > 0, "No cryptid exists yet.");
        return ownerOf(totalSupply());
    }

    function lastMintID() public view returns (uint256){
        require(totalSupply() > 0, "No cryptid exists yet.");
        return(totalSupply());
    }

    function totalSupply() public view returns (uint256) {
        return _tokenIdCounter.current() - 1;
    }

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");
        return string(abi.encodePacked(baseURI, tokenId.toString(), baseExtension));
            
    }

    function getTokensLeft() public view returns (uint256) {
        return totalSaleSupply - totalSupply();
    }
    
    function getStage() public view returns (uint8) {
        return stage;
    }

    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal whenNotPaused override(ERC721) {
        super._beforeTokenTransfer(from, to, tokenId);
    }

}