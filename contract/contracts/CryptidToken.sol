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
    using MerkleProof for bytes32[];

    Counters.Counter private _tokenIdCounter;
    
    bytes32 public merkleRoot;
    string public provenanceHash;
    string public baseURI = "";
    string public baseExtension = ".json";
    uint8 private stage = 0;
    uint8 public maxMintPerTx;     
    bool public tokenURIFrozen = false;
    bool public provenanceHashFrozen = false;

    address public withdrawDest1 = 0x1953bc1fF76f5e61cD775A4482bd85BAc56aD1Eb; // trust
    address public withdrawDest2 = 0x12B58f5331a6DC897932AA7FB5101667ACdf03e2; // founder 1
    address public withdrawDest3 = 0x1953bc1fF76f5e61cD775A4482bd85BAc56aD1Eb; // founder 2
    address public withdrawDest4 = 0x12B58f5331a6DC897932AA7FB5101667ACdf03e2; // founder 3
    address public withdrawDest5 = 0x12B58f5331a6DC897932AA7FB5101667ACdf03e2; // founder 4
    
    // ~ Sale stages ~
    // stage 0: Airdrops
    // stage 1: Whitelist
    // stage 2: Team Mint 
    // stage 3: Public Sale

    uint256 public salePrice = 0.1 ether;  

    // Whitelist mint (stage=1)
    uint256 public whitelistSupply;                       
    mapping(address => bool) public blacklist;              
    
    // Team Mint (stage=2)
    uint256 public teamMintSupply;                          
    uint256 public teamMintCount;

    // Public Sale (stage=3)
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
    function mint(uint8 _mintAmount, bytes32[] memory proof) public payable whenNotPaused {
        require(stage > 0, "Minting not initiated. Currenly on stage 0.");
        require(_mintAmount > 0, "Mint amount must be greater than 0.");
        require(_mintAmount <= maxMintPerTx, "Exceeds max allowed amount per transaction.");
        if (stage == 1) {
        // Whitelist
            require(proof.verify(merkleRoot, keccak256(abi.encodePacked(msg.sender))), "Address not whitelisted.");
            require(_mintAmount < 2, "Mint amount must be 1.");
            require(msg.value >= salePrice.mul(_mintAmount), "Not enough ether sent.");
            require(totalSupply() + _mintAmount <= whitelistSupply, "Transaction exceeds whitelist supply.");
            require(blacklist[msg.sender] == false, "This whitelisted address was already used for their mint.");    
            blacklist[msg.sender] = true;
    }   else if (stage == 2) {
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
        require(stage < 1, "Past airdrop phase.");
        require(_mintAmount <= maxMintPerTx, "Exceeds max allowed amount per transaction");
        require(_mintAmount > 0, "Airdrop amount must be greater than 0");
        require(totalSupply()+ _mintAmount <= whitelistSupply, "Mint amount will exceed whitelist supply.");
        for (uint256 i = 1; i <= _mintAmount; i++) {
            _safeMint(_to, _tokenIdCounter.current());
            _tokenIdCounter.increment();
        }
    }

    function setMerkleRoot(bytes32 _merkleRoot) public onlyOwner {
        merkleRoot = _merkleRoot;
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

    function setWithdrawAddress(address _dest1, address _dest2, address _dest3, address _dest4, address _dest5) public onlyOwner {
        withdrawDest1 = _dest1;
        withdrawDest2 = _dest2;
        withdrawDest3 = _dest3;
        withdrawDest4 = _dest4;
        withdrawDest5 = _dest5;
    }

    function freezeProvenanceHash() public onlyOwner {
        require(bytes(provenanceHash).length > 0, "Provenance hash cannot be empty.");
        require(!provenanceHashFrozen, "Provenance hash is already frozen.");
        provenanceHashFrozen = true;
    }

    function withdraw() public payable onlyOwner {
        require(address(this).balance > 0, "Contract balance is 0.");
        (bool ms, ) = payable(withdrawDest1).call{value: address(this).balance.mul(700).div(1000)}("");
        require(ms, "withdrawl 1 failed");
        (bool ns, ) = payable(withdrawDest2).call{value: address(this).balance.mul(105).div(1000)}(""); 
        require(ns, "withdrawl 2 failed");
        (bool cr, ) = payable(withdrawDest3).call{value: address(this).balance.mul(105).div(1000)}(""); 
        require(cr, "withdrawl 3 failed");
        (bool sn, ) = payable(withdrawDest4).call{value: address(this).balance.mul(45).div(1000)}("");
        require(sn, "withdrawl 4 failed");
        (bool gr, ) = payable(withdrawDest5).call{value: address(this).balance}("");
        require(gr, "withdrawl 5 failed");
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