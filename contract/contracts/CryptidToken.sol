// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import '@openzeppelin/contracts/token/ERC721/ERC721.sol';
import '@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol';
import '@openzeppelin/contracts/access/Ownable.sol';
import '@openzeppelin/contracts/security/ReentrancyGuard.sol';
import '@openzeppelin/contracts/utils/Counters.sol';
import '@openzeppelin/contracts/security/Pausable.sol';
import '@openzeppelin/contracts/utils/cryptography/MerkleProof.sol';

/// @title CryptidToken NFT Contract
/// @author @chrisrusselljr
/// @notice You can use this contract to mint, sent, and interact with CRYPTIDS
/// @dev All function calls are currently implemented without side effects
contract CryptidToken is ERC721, ERC721Enumerable, Pausable, Ownable, ReentrancyGuard{ 
    using Strings for uint256;
    using Counters for Counters.Counter;
    using MerkleProof for bytes32[];

    enum Stage {
        Init,
        Airdrop,
        Whitelist,
        TeamMint,
        PublicSale
    }

    Counters.Counter private _tokenIdCounter;
    
    bytes32 public merkleRoot;
    string public provenanceHash;
    string public baseURI = "";
    string public baseExtension = ".json";
    uint8 public maxMintPerTx;     
    bool public tokenURIFrozen = false;
    bool public provenanceHashFrozen = false;

    address public withdrawlAddress = 0x12B58f5331a6DC897932AA7FB5101667ACdf03e2;

    // ~ Sale stages ~
    // stage 0: Init
    // stage 1: Airdrop
    // stage 2: Whitelist
    // stage 3: Team Mint 
    // stage 4: Public Sale

    // Whitelist mint (stage=2)
    uint256 public whitelistSupply;                       
    mapping(address => bool) public claimed;              
    
    // Team Mint (stage=3)
    uint256 public teamMintSupply;                          
    uint256 public teamMintCount;

    // Public Sale (stage=4)
    uint256 public totalSaleSupply;         
    uint256 public salePrice = 0.1 ether;  

    Stage public stage;

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

    modifier isValidMerkleProof(bytes32[] calldata proof, bytes32 root) {
        require(proof.verify(root, keccak256(abi.encodePacked(msg.sender))), "Address not in whitelist.");
        _;
    }

    modifier isCorrectPayment(uint256 price, uint256 numberOfTokens) {
        require(price * numberOfTokens == msg.value, "Incorrect ETH value sent.");
        _;
    }
    
    // Stage 1 - Airdrop
    function airdropCryptid(
        uint8 mintAmount, 
        address to
    ) 
        external
        onlyOwner 
    {
        require(stage > Stage.Init, "No airdrops at init.");
        require(totalSupply()  + mintAmount <= totalSaleSupply, "Mint amount will exceed total sale supply.");
        for (uint256 i = 1; i <= mintAmount; i++) {
            _safeMint(to, _tokenIdCounter.current());
            _tokenIdCounter.increment();
        }
    }

    // Stage 2 - Whitelist Sale
    function whitelistMint(
        bytes32[] calldata merkleProof
    ) 
        external
        payable 
        isValidMerkleProof(merkleProof, merkleRoot) 
        isCorrectPayment(salePrice, 1) 
        nonReentrant 
        whenNotPaused 
    {
        require(stage == Stage.Whitelist, "Whitelist sale not initiated.");
        require(claimed[msg.sender] == false, "Whitelist mint already claimed."); 
        require(totalSupply() + 1 <= whitelistSupply, "Mint amount will exceed whitelist supply.");
        claimed[msg.sender] = true;
        _safeMint(msg.sender, _tokenIdCounter.current());
        _tokenIdCounter.increment();
    }

    // Stage 3 - Team Mint
    function teamMint(
        uint8 mintAmount
    ) 
        external 
        onlyOwner 
    {
        require(stage == Stage.TeamMint, "Whitelist sale not initiated.");
        require(mintAmount + teamMintCount <= teamMintSupply, "Transaction exceeds total team sale supply.");     
        teamMintCount += mintAmount;
        for (uint256 i = 1; i <= mintAmount; i++) {
            _safeMint(msg.sender, _tokenIdCounter.current());
            _tokenIdCounter.increment();
        }
    }

    // Stage 4 - Public Mint
    function publicMint(
        uint8 mintAmount
    ) 
        external
        payable 
        isCorrectPayment(salePrice, mintAmount) 
        nonReentrant 
        whenNotPaused  
    {
        require(stage == Stage.PublicSale, "Public Sale not initiated.");
        require(totalSupply()  + mintAmount <= totalSaleSupply, "Transaction exceeds total sale supply.");
        require(mintAmount <= maxMintPerTx, "Exceeds max allowed mints per transaction.");  
        for (uint256 i = 1; i <= mintAmount; i++) {
            _safeMint(msg.sender, _tokenIdCounter.current());
            _tokenIdCounter.increment();
        }
    }

    //Owner functions
    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }

    // to be used in case of manual override
    function setClaim(address wlAddress) external onlyOwner{
        claimed[wlAddress] = true;
    }

    // to be used in case of WL error
    function undoClaim(address wlAddress) external onlyOwner{
        claimed[wlAddress] = false;
    }

    function setMerkleRoot(bytes32 _merkleRoot) external onlyOwner {
        merkleRoot = _merkleRoot;
    }

    function setBaseURI(string memory _newBaseURI) external onlyOwner {
        require(!tokenURIFrozen, "BaseURI is frozen.");
        baseURI = _newBaseURI;
    } 
    
    function freezeBaseURI() external onlyOwner {
        require(bytes(baseURI).length > 0, "BaseURI cannot be empty.");
        require(!tokenURIFrozen, "BaseURI is already frozen.");
        tokenURIFrozen = true;
    }

    function setTeamMintSupply(uint256 _newTeamMintSupply) external onlyOwner {
        teamMintSupply = _newTeamMintSupply;
    }

    function setBaseExtension(string memory _newBaseExtension) external onlyOwner {
        baseExtension = _newBaseExtension;
    }

    function setPublicSalePrice(uint256 _newSalePrice) external onlyOwner {
        salePrice = _newSalePrice;
    }

    function setMaxMintPerTx(uint8 _newmaxMintPerTx) external onlyOwner {
        maxMintPerTx = _newmaxMintPerTx;
    }

    function setProvenanceHash(string memory _provenanceHash) external onlyOwner {
        require(bytes(_provenanceHash).length > 0, "Provenance hash cannot be empty string.");
        require(!provenanceHashFrozen, "Provenance hash is frozen.");
        provenanceHash = _provenanceHash;
    }

    function freezeProvenanceHash() external onlyOwner {
        require(bytes(provenanceHash).length > 0, "Provenance hash cannot be empty string.");
        require(!provenanceHashFrozen, "Provenance hash is already frozen.");
        provenanceHashFrozen = true;
    }

    function setWithdrawlAddress(address _withdrawlAddress) external onlyOwner {
        withdrawlAddress = _withdrawlAddress;
    }

    function withdraw() external payable onlyOwner {
        require(address(this).balance > 0, "Contract balance is 0.");
        (bool success, ) = payable(withdrawlAddress).call{value: address(this).balance}("");
        require(success, "Withdrawl failed.");
    }

    function setStage(Stage _stage) external onlyOwner {
        require(provenanceHashFrozen == true, "Provenance hash must be frozen before minting can start.");
        require(merkleRoot != 0, "Merkle root must be set beefore minting can start.");
        stage = _stage;
    }

    // External view functions
    function lastMintAddress() external view returns (address){
        return ownerOf(totalSupply());
    }

    function lastMintID() external view returns (uint256){
        return(totalSupply());
    }

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token.");
        return string(abi.encodePacked(baseURI, tokenId.toString(), baseExtension));
    }

    function getTokensLeft() external view returns (uint256) {
        return totalSaleSupply - totalSupply();
    }
    
    function walletOfOwner(address owner) external view returns (uint256[] memory) {
        uint256 ownerTokenCount = balanceOf(owner);
        uint256[] memory tokensIds = new uint256[](ownerTokenCount);
        for (uint256 i; i < ownerTokenCount; i++) {
            tokensIds[i] = tokenOfOwnerByIndex(owner, i);
        }
        return tokensIds;
    }
    
    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal whenNotPaused override(ERC721, ERC721Enumerable) {
        super._beforeTokenTransfer(from, to, tokenId);
    }

    // The following functions are overrides required by Solidity.

    function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721Enumerable) returns (bool) {
        return super.supportsInterface(interfaceId);
    }

}