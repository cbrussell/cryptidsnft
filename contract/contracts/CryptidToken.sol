// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import '@openzeppelin/contracts/token/ERC721/ERC721.sol';
import '@openzeppelin/contracts/access/Ownable.sol';
import '@openzeppelin/contracts/security/ReentrancyGuard.sol';
import '@openzeppelin/contracts/utils/math/SafeMath.sol';
import '@openzeppelin/contracts/utils/Counters.sol';
import '@openzeppelin/contracts/security/Pausable.sol';
import '@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol';
import @openzeppelin/contracts/utils/cryptography/MerkleProof.sol';

contract CryptidToken is ERC721, Pausable, Ownable, ReentrancyGuard, ERC721Burnable{ 
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
    // stage 0: Init
    // stage 1: Airdrops for Trivia/Contest Winners
    // stage 2: Whitelist
    // stage 3: Team Mint 
    // stage 4: Public Sale

    // Whitelist mint (stage=1)
    uint256 public whitelistSupply;                       
    mapping(address => bool) public claimed;              
    
    // Team Mint (stage=2)
    uint256 public teamMintSupply;                          
    uint256 public teamMintCount;

    // Public Sale (stage=3)
    uint256 public totalSaleSupply;         
    uint256 public salePrice = 0.10 ether;  

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

    modifier isValidMerkleProof(bytes32[] calldata _proof, bytes32 _root) {
        require(MerkleProof.verify(_proof, _root, keccak256(abi.encodePacked(msg.sender))), "Address not in whitelist.");
        _;
    }

    modifier isCorrectPayment(uint256 _price, uint256 _numberOfTokens) {
        require(_price * _numberOfTokens == msg.value, "Incorrect ETH value sent.");
        _;
    }

    modifier callerIsUser() {
        require(tx.origin == msg.sender, "The caller is another contract.");
        _;
    }

    // Stage 1 - Airdrops
    function airdropCryptid(uint8 _mintAmount, address _to) public onlyOwner {
        require(stage < 3, "Past airdrop phase.");
        require(_mintAmount > 0, "Airdrop amount must be greater than 0");
        require(totalSupply() + _mintAmount <= whitelistSupply, "Mint amount will exceed whitelist supply.");
        for (uint256 i = 1; i <= _mintAmount; i++) {
            _mint(_to, _tokenIdCounter.current());
            _tokenIdCounter.increment();
        }
    }

    // Stage 2 - Whitelist Mint
    function whitelistMint(
        bytes32[] calldata _merkleProof
    ) 
        public 
        payable 
        isValidMerkleProof(_merkleProof, merkleRoot) 
        isCorrectPayment(salePrice, 1) 
        callerIsUser
        nonReentrant 
        whenNotPaused 
    {
        require(stage == 2, "Whitelist minting not initiated.");
        require(claimed[msg.sender] == false, "Whitelist mint already claimed."); 
        require(totalSupply() + 1 <= whitelistSupply, "Mint amount will exceed whitelist supply.");
        claimed[msg.sender] = true;
        _mint(msg.sender, _tokenIdCounter.current());
        _tokenIdCounter.increment();
    }

    // Stage 3 - Team Mint
    function teamMint(
        uint8 _mintAmount
    ) 
        external 
        onlyOwner 
    {
        require(stage == 3, "Team sale not initiated.");
        require(_mintAmount + teamMintCount <= teamMintSupply, "Transaction exceeds total team-sale supply");      
        teamMintCount += _mintAmount;
        for (uint256 i = 1; i <= _mintAmount; i++) {
            _mint(msg.sender, _tokenIdCounter.current());
            _tokenIdCounter.increment();
        }
    }


    // Stage 4 - Public Mint
    function publicMint(
        uint8 _mintAmount
    ) 
        public 
        payable 
        isCorrectPayment(salePrice, _mintAmount) 
        callerIsUser
        nonReentrant 
        whenNotPaused  
    {
        require(stage == 4, "Public mint not initiaited.");
        require(totalSupply()  + _mintAmount <= totalSaleSupply, "Transaction exceeds total sale supply");
        require(_mintAmount > 0, "Mint amount must be greater than 0.");
        require(_mintAmount <= maxMintPerTx, "Exceeds max allowed mints per transaction.");  

        for (uint256 i = 1; i <= _mintAmount; i++) {
            _mint(msg.sender, _tokenIdCounter.current());
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

    // to be used in case of manual override
    function overrideClaim(address _wlAddress) public onlyOwner{
        claimed[_wlAddress] = true;
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
        require(merkleRoot[0] != 0, "Merkle root must be set beefore whitelist minting can begin");
        require(stage < 4, "No stages after public sale");
        stage++;
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
        require(bytes(_provenanceHash).length > 0, "Provenance hash cannot be empty string.");
        require(!provenanceHashFrozen, "Provenance hash is frozen.");
        provenanceHash = _provenanceHash;
    }

    function freezeProvenanceHash() public onlyOwner {
        require(bytes(provenanceHash).length > 0, "Provenance hash cannot be empty.");
        require(!provenanceHashFrozen, "Provenance hash is already frozen.");
        provenanceHashFrozen = true;
    }

    function setWithdrawAddress(address _dest1, address _dest2, address _dest3, address _dest4, address _dest5) public onlyOwner {
        withdrawDest1 = _dest1;
        withdrawDest2 = _dest2;
        withdrawDest3 = _dest3;
        withdrawDest4 = _dest4;
        withdrawDest5 = _dest5;
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