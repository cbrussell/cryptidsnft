// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import '@openzeppelin/contracts/token/ERC721/ERC721.sol';
import '@openzeppelin/contracts/access/Ownable.sol';
import '@openzeppelin/contracts/utils/math/SafeMath.sol';
import '@openzeppelin/contracts/utils/Counters.sol';
import '@openzeppelin/contracts/security/Pausable.sol';
import '@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol';

contract CryptidToken is ERC721, Pausable, Ownable, ERC721Burnable{ 
    using Strings for uint256;
    using SafeMath for uint256;
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    string public provenanceHash;
    string public baseURI = "";
    string public defaultURI;
    string public baseExtension = ".json";
    uint8 private stage = 0;
    uint8 public maxMintPerTx;     
    bool public tokenURIFrozen = false;
    bool public provenanceHashFrozen = false;
    address public withdrawDest1 = 0x1953bc1fF76f5e61cD775A4482bd85BAc56aD1Eb;
    address public withdrawDest2 = 0x12B58f5331a6DC897932AA7FB5101667ACdf03e2;
    
    // ~ Sale stages ~
    // stage 0: Init 
    // stage 1: Free Whitelist 
    // stage 2: Presale 
    // stage 3: Team Mint 
    // stage 4: Public Sale

    // Whitelist mint (stage=1)
    mapping(address => uint8) public whitelistUsers;
    mapping(address => uint8) public whitelistMintCount;

    // Presale mint (stage=2)
    mapping(address => bool) public presaleUsers;
    uint256 public presaleSupply;                       
    uint256 public presalePrice = 0.04 ether;
    uint8 public presaleMintMax = 5;                  
    mapping(address => uint8) public presaleMintCount;

    // Team Mint (stage=3)
    uint256 public teamMintSupply;                          
    uint256 public teamMintCount;

    // Public Sale (stage=4)
    uint256 public salePrice = 0.05 ether;
    uint256 public totalSaleSupply;         

    constructor(
        string memory _name,
        string memory _symbol,
        string memory _defaultURI,
        uint256 _presaleSupply,
        uint256 _teamMintSupply,
        uint256 _totalSaleSupply,
        uint8 _maxMintPerTx

    )   ERC721(_name, _symbol) {
        presaleSupply = _presaleSupply;
        teamMintSupply = _teamMintSupply;
        totalSaleSupply = _totalSaleSupply;
        maxMintPerTx = _maxMintPerTx;
        defaultURI = _defaultURI;
        _tokenIdCounter.increment();
    }

    //Public mint function
    function mint(uint8 _mintAmount) public payable whenNotPaused {
        require(stage > 0, "Minting not initiated. Currenly on stage 0 (init).");
        require(_mintAmount > 0, "Mint amount must be greater than 0");
        require(_mintAmount <= maxMintPerTx, "Exceeds max allowed amount per transaction");
        if (stage == 1) {
        // Whitelist
            require(whitelistUsers[msg.sender] > 0, "Minter not whitelisted.");
            require(_mintAmount + whitelistMintCount[msg.sender] <= whitelistUsers[msg.sender], "Transaction exceeds remaining whitelist mints");
            whitelistMintCount[msg.sender] += _mintAmount;
    }   else if (stage == 2) {
        // Presale  
            require(msg.value >= presalePrice.mul(_mintAmount), "Not enough ether sent");
            require(presaleUsers[msg.sender], "Address not on presale list");
            require(totalSupply() + _mintAmount <= presaleSupply, "Transaction exceeds pre-sale supply");
            require(_mintAmount + presaleMintCount[msg.sender] <= presaleMintMax, "Transaction exceeds max allowed presale mints");      
            presaleMintCount[msg.sender] += _mintAmount;
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
        require(stage < 2, "Past whitelist sale.");
        require(_mintAmount <= maxMintPerTx, "Exceeds max allowed amount per transaction");
        require(_mintAmount > 0, "Airdrop amount must be greater than 0");
        require(totalSupply()+ _mintAmount <= presaleSupply, "Mint amount will exceed presale supply.");
       
        for (uint256 i = 1; i <= _mintAmount; i++) {
            _safeMint(_to, _tokenIdCounter.current());
            _tokenIdCounter.increment();
        }
    }

    function setWhitelistUsers(address[] memory _users, uint8[] memory _mints) public onlyOwner {
        require(stage < 2, "Whitelist sale is concluded.");
        for(uint256 i=0;i<_users.length;i++)
        whitelistUsers[_users[i]] = _mints[i];
    }

    function setPresaleUsers(address[] memory _users) public onlyOwner {
        require(stage < 3, "Presale is concluded.");
        for(uint256 i=0;i<_users.length;i++)
        presaleUsers[_users[i]] = true;
    }

    function removeWhitelistUser(address _user) public onlyOwner {
        require(stage < 2, "Whitelist sale is concluded.");
        require(whitelistUsers[_user] > 0, "User is not on whitelist.");
        whitelistUsers[_user] = 0;
    }

    function removePresaleUser(address _user) public onlyOwner {
        require(presaleUsers[_user], "User not on presale list.");
        presaleUsers[_user] = false;
    }

    function setBaseURI(string memory _newBaseURI) public onlyOwner {
        require(!tokenURIFrozen, "BaseURI is frozen.");
        baseURI = _newBaseURI;
    }

    function setDefaultURI(string memory _newDefaultURI) public onlyOwner {
        defaultURI = _newDefaultURI;
    }    
    
    function freezeBaseURI() public onlyOwner {
        require(bytes(baseURI).length > 0, "baseURI cannot be empty");
        require(!tokenURIFrozen, "BaseURI is already frozen.");
        tokenURIFrozen = true;
    }

    function nextStage() public onlyOwner() {
        require(provenanceHashFrozen == true, "Provenance hash must be frozen before minting can start.");
        require(stage < 4, "No stages after public sale");
        stage++;
    }
    
    function setTeamMintSupply(uint256 _newTeamMintSupply) public onlyOwner() {
        teamMintSupply = _newTeamMintSupply;
    }

    function setBaseExtension(string memory _newBaseExtension) public onlyOwner {
        baseExtension = _newBaseExtension;
    }

    function setPresalePrice(uint256 _newPresalePrice) public onlyOwner {
        require(stage < 3, "Presale is concluded.");
        presalePrice = _newPresalePrice;
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
        return bytes(baseURI).length > 0
            ? string(abi.encodePacked(baseURI, tokenId.toString(), baseExtension))
            : defaultURI;
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