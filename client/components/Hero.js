import React, { useState, useEffect } from "react";
import Image from "next/image";
import { useStatus } from "../context/statusContext";
import keccak256 from "keccak256";
import MerkleTree from "merkletreejs";

import { useContractFunction, ChainId, useEthers, useEtherBalance, shortenAddress } from "@usedapp/core";
import {
  GetMaxMintAmount,
  GetTotalSupply,
  GetTotalSaleSupply,
  GetStage,
  Verify,
  GetOwner,
  GetSalePrice,
  CheckIfClaimed,
} from "../utils/interact"
import { formatEther } from '@ethersproject/units'
import { Contract, utils } from 'ethers';
import cryptidTokenNFT from "../../contract/build/deployments/4/0xF2dF6f027c2eCb355A219ca1a317c6825A38cAbb.json";
import marshal_leaves from "../data/test_leaves.json";
// import root from "../data/test_root.json";

const Hero = () => {
  const address = "0xF2dF6f027c2eCb355A219ca1a317c6825A38cAbb";
  const { account, chainId: currentChainId, library, BigNumber } = useEthers();
  const { status, setStatus } = useStatus();
  const [count, setCount] = useState(1);
  const [maxMintAmount, setMaxMintAmount] = useState(0);
  const [totalSupply, setTotalSupply] = useState(0);
  const [totalSaleSupply, setTotalSaleSupply] = useState(10000);
  const [nftPrice, setNftPrice] = useState(100000000000000000);
  const [stage, setStage] = useState(0);
  const [minting, setMinting] = useState(false)
  const [claimed, setClaimed] = useState(false);
  const [whitelistClaimable, setWhitelistClaimable] = useState(false);
  const [owner, setOwner] = useState("");

  const maxMintCalculated = GetMaxMintAmount();
  const nftPriceCalculated = GetSalePrice();
  const stageCalculated = GetStage();
  const totalSupplyCalculated = GetTotalSupply();
  const totalSaleSupplyCalculated = GetTotalSaleSupply();
  const ownerCalculated = GetOwner();
  const etherBalance = useEtherBalance(account);

  const claimedCalculated  = CheckIfClaimed(account ?? '0x0000000000000000000000000000000000000000');

  const { abi: cryptidTokenABI } = cryptidTokenNFT;
  const cryptidTokenNFTInterface = new utils.Interface(cryptidTokenABI);
  const [contract, setContract] = useState(new Contract(address, cryptidTokenNFTInterface));
  const [whitelistProof, setWhitelistProof] = useState([])


  const whitelistClaimableCalculated = Verify((account ?? '0x0000000000000000000000000000000000000000'), whitelistProof);

  useEffect(() => {
    if (!account) {
      setWhitelistProof([]);
      return;
    } else {
      const leaves = MerkleTree.unmarshalLeaves(marshal_leaves);
      const tree = new MerkleTree(leaves, keccak256, { sortPairs: true });
      setWhitelistProof(tree.getHexProof(keccak256(account)));
      console.log("New account detected, recalculating Merkle Proof.");
   
    }
 
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [account])

  

  // useEffect(() => {
  //   if (!account) {
  //     setWhitelistProof([]);
  //     return;
  //   }
  //   async function checkIfClaimed() {
  //     tree.getHexProof(keccak256(account)).then((result) => {
  //       setWhitelistProof(result);
  //     }).catch((err) => {
  //       setWhitelistProof([]);
  //     });

  //   }
  //   checkIfClaimed();
  // // eslint-disable-next-line react-hooks/exhaustive-deps
  // }, [whitelistProofCalculated])

  
  // useEffect(() => {
  //   const whitelistProofCalculated = (account ? tree.getHexProof(keccak256(account)) : []);
  //   setWhitelistProof(whitelistProofCalculated);

  // }, [whitelistProofCalculated]);


  useEffect(() => {
    console.log("Current account whitelist verified status is: ", whitelistClaimableCalculated);
    setWhitelistClaimable(whitelistClaimableCalculated);
  }, [whitelistClaimableCalculated]);

  useEffect(() => {
    console.log("Max Mint Per Transaction is " + maxMintCalculated);
    if (maxMintCalculated) setMaxMintAmount(maxMintCalculated);
  }, [maxMintCalculated]);

  useEffect(() => {
    console.log("Sale Price is  ", nftPriceCalculated);
    if (nftPriceCalculated) setNftPrice(nftPriceCalculated);
  }, [nftPriceCalculated]);

  useEffect(() => {
    console.log("Current account claimed status is: ", claimedCalculated);
    setClaimed(claimedCalculated);
  }, [claimedCalculated]);

  useEffect(() => {
    console.log("The Current Stage is " + stageCalculated);
    if (stageCalculated) setStage(stageCalculated);
  }, [stageCalculated]);

  useEffect(() => {
    console.log("Current Minted Supply is " + totalSupplyCalculated);
    if (totalSupplyCalculated) setTotalSupply(totalSupplyCalculated);
  }, [totalSupplyCalculated]);

  useEffect(() => {
    console.log("Total Sale Supply is " + totalSaleSupplyCalculated);
    if (totalSaleSupplyCalculated) setTotalSaleSupply(totalSaleSupplyCalculated);
  }, [totalSaleSupplyCalculated]);

  useEffect(() => {
    console.log("The Owner is " + ownerCalculated);
    if (ownerCalculated) setOwner(ownerCalculated);
  }, [ownerCalculated]);

  

  const incrementCount = () => {
    if (count < maxMintAmount) {
      setCount(count + 1);
    }
  };

  const decrementCount = () => {
    if (count > 1) {
      setCount(count - 1);
    }
  };

  useEffect(() => {
    if (account && library) {
      setContract(new Contract(address, cryptidTokenNFTInterface, library.getSigner()))
    }
    console.log(library);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [account, library])

  const soldOut = totalSaleSupply && totalSupply && totalSaleSupply?.eq(totalSupply);



  const { state: publicMintState, send: sendPublicMint } = useContractFunction(contract, 'publicMint', {})

  const handlePublicMint = async () => {

    const ethTotal = (nftPrice * count).toString()

    if (formatEther(etherBalance) < formatEther((nftPrice * count).toString())) {
      console.log("User Ether Balance is " + formatEther(etherBalance))
      setStatus('Error: Not enough ether for this purchase')
      return
    }
      sendPublicMint(count, { value: ethTotal })
      console.log(publicMintState.status)
    }
  

  const { state: whitelistMintState, send: sendWhitelistMint } = useContractFunction(contract, 'whitelistMint', {})



  const handleWhitelistMint = async () => {

    const ethTotal = (nftPrice).toString()

    if (formatEther(etherBalance) < formatEther((nftPrice * count).toString())) {
      console.log("User Ether Balance is " + formatEther(etherBalance))
      setStatus('Error: Not enough ether for this purchase')
      return
    }

    if (!whitelistClaimable) {
      console.log("Unable to generate valid whitelist proof for account")
      setStatus("Error: Unable to generate valid whitelist proof for account: ", account)
      return
    }

    if (claimed) {
      console.log("Whitelist is already claimed for account ", account);
      setStatus("Error: Whitelist mint is already claimed")
    }
    
    sendWhitelistMint(whitelistProof, { value: ethTotal })
    
    console.log(whitelistMintState.status)
  }

  useEffect(() => {
    if (whitelistMintState.status === 'None' || publicMintState.status === 'None') {
      setMinting(false);
    }

    if (whitelistMintState.status === 'PendingSignature' || publicMintState.status === 'PendingSignature') {
      setStatus(
        <p>{" "}Pending signature<span className="dots"><span>.</span><span>.</span><span>.</span></span>
        </p>
      )
      setMinting(true);
    }
    if (whitelistMintState.status === 'Mining') {
      setStatus((
        <p>
          {" "}
          🦊 Minting Cryptid<span className="dots"><span>.</span><span>.</span><span>.</span></span>Check out your transaction on Etherscan: <a target="_blank" rel="noreferrer" href={`https://rinkeby.etherscan.io/tx/` + whitelistMintState.transaction.hash} className="alert">
            {"https://rinkeby.etherscan.io/tx/" + whitelistMintState.transaction.hash}
          </a>
        </p>
      ))
      setMinting(true);
    }
    if (publicMintState.status === 'Mining') {
      setStatus((
        <p>
          {" "}
          🦊 Minting Cryptid<span className="dots"><span>.</span><span>.</span><span>.</span></span>Check out your transaction on Etherscan: <a target="_blank" rel="noreferrer" href={`https://rinkeby.etherscan.io/tx/` + publicMintState.transaction.hash} className="alert">
            {"https://rinkeby.etherscan.io/tx/" + publicMintState.transaction.hash}
          </a>
        </p>
      ))
      setMinting(true);
    }
    if (whitelistMintState.status === 'Exception') {
      setStatus("Error:" + whitelistMintState.errorMessage)
      setMinting(false);
    }
    if (publicMintState.status === 'Exception') {
      setStatus("Error:" + publicMintState.errorMessage)
      setMinting(false);
    }
    if (whitelistMintState.status === 'Success') {
      setStatus((
        <p>
          {" "}
          🦊 Success! Check out your transaction on Etherscan: <a target="_blank" rel="noreferrer" href={`https://rinkeby.etherscan.io/tx/` + whitelistMintState.receipt.transactionHash} className="alert">
            {"https://rinkeby.etherscan.io/tx/" + whitelistMintState.receipt.transactionHash}
          </a>
        </p>
      ))
      setMinting(false);

    }
    if (publicMintState.status === 'Success') {
      setStatus((
        <p>
          {" "}
          🦊 Success! Check out your transaction on Etherscan: <a target="_blank" rel="noreferrer" href={`https://rinkeby.etherscan.io/tx/` + publicMintState.receipt.transactionHash} className="alert">
            {"https://rinkeby.etherscan.io/tx/" + publicMintState.receipt.transactionHash}
          </a>
        </p>
      ))
      setMinting(false);

    }
    if (whitelistMintState.status === 'Fail' || publicMintState.status === 'Fail') {
      setStatus("There was an error during the transaction")
      setMinting(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [whitelistMintState.status, publicMintState.status])


  // public timers

  const calculateTimeLeftPublic = () => {
    const difference = +new Date('March 25 2022 16:00:00') - +new Date();
    let timeLeftPublic = {};

    if (difference > 0) {
      timeLeftPublic = {
        days: Math.floor(difference / (1000 * 60 * 60 * 24)),
        hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
        minutes: Math.floor((difference / 1000 / 60) % 60),
        seconds: Math.floor((difference / 1000) % 60),
      };
    }

    return timeLeftPublic;
  };

  const [timeLeftPublic, setTimeLeftPublic] = useState(calculateTimeLeftPublic());

  useEffect(() => {
    setTimeout(() => {
      setTimeLeftPublic(calculateTimeLeftPublic());
    }, 1000);
  }, [timeLeftPublic]);

  const timerComponentsPublic = [];

  Object.keys(timeLeftPublic).forEach((interval) => {
    if (!timeLeftPublic[interval]) {
      return;
    }

    timerComponentsPublic.push(
      <span>
        {timeLeftPublic[interval]} {interval}{" "}
      </span>
    );
  })


  // whitelist timer

  const calculateTimeLeftWhitelist = () => {
    const difference = +new Date('March 26 2022 10:00:00') - +new Date();
    let timeLeftWhitelist = {};

    if (difference > 0) {
      timeLeftWhitelist = {
        days: Math.floor(difference / (1000 * 60 * 60 * 24)),
        hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
        minutes: Math.floor((difference / 1000 / 60) % 60),
        seconds: Math.floor((difference / 1000) % 60),
      };
    }

    return timeLeftWhitelist;
  };

  const [timeLeftWhitelist, setTimeLeftWhitelist] = useState(calculateTimeLeftWhitelist());


  useEffect(() => {
    setTimeout(() => {
      setTimeLeftWhitelist(calculateTimeLeftWhitelist());
    }, 1000);
  }, [timeLeftWhitelist]);

  const timerComponentsWhitelist = [];

  Object.keys(timeLeftWhitelist).forEach((interval) => {
    if (!timeLeftWhitelist[interval]) {
      return;
    }

    timerComponentsWhitelist.push(
      <span>
        {timeLeftWhitelist[interval]} {interval}{" "}
      </span>
    );
  })

  return (
    <main id="main" className="h-fit py-10 md:py-0 md:pb-40  bg-pattern ">
      
      <div className="container max-w-6xl mx-auto flex flex-col items-center pt-4">
        <div className="flex flex-col items-center">
          <div className="flex pb-2">
            <Image
              src="/images/BlankCryptid6.png"
              width="270"
              height="270"
              alt="Blank Cryptid 1"
              className="rounded-md"
            />
            <Image
              src="/images/BlankCryptid.png"
              width="300"
              height="300"
              alt="Blank Cryptid 2"
              className="rounded-md"
            />
            <Image
              src="/images/BlankCryptid2.png"
              width="270"
              height="270"
              alt="Blank Cryptid 3"
              className="rounded-md"
            />
          </div>


          {stage < 3 && !account ?
            (
              <p className="text-white text-2xl mt-6 text-center">
                {/* Account: {" "} {shortenAddress(account)} is not whitelisted. <br></br><br></br> */}

                {timerComponentsPublic.length ? <span>Whitelist Sale will begin in... <br></br> {timerComponentsWhitelist}</span> : <span>Whitelist Sale will be starting soon...</span>}

              </p>
            )

            : 
          
          stage < 2 && whitelistClaimable && account && !claimed ?
              (
                <p className="text-white text-2xl mt-8 text-center">
                  Account: {" "} {shortenAddress(account)} has 1 Whitelist Mint Available <br></br><br></br>

                  {timerComponentsWhitelist.length ? <span>Whitelist Sale will begin in... <br></br> {timerComponentsPublic}</span> : <span>Whitelist Sale will be starting soon...</span>}

                </p>
              )

              : stage == 2 && whitelistClaimable && account && !claimed ?
                (
                  <>
                    <p className="text-white text-2xl mt-8 text-center">
                      Account: {" "} {shortenAddress(account)} has 1 Whitelist Mint Available <br></br><br></br>
                    </p>
                    {/* Minted NFT Ratio */}
                    <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                      <span className="text-[#d35c5c]">{`${totalSupply}`}</span> /
                      <span className="text-black">{`${totalSaleSupply}`}</span>
                    </p>

                    <div className="flex items-center mt-6 text-3xl font-bold text-gray-200">


                      <button
                        className="flex items-center justify-center w-12 h-12 bg-white rounded-md hover:bg-gray-200 text-center disabled:bg-slate-50"
                      // onClick={decrementCount}

                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          className="w-6 h-6 text-[#d35c5c] "
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            d="M20 12H4"
                          />
                        </svg>
                      </button>

                      <h2 className="mx-8">{count}</h2>

                      <button
                        className="flex items-center justify-center w-12 h-12 bg-white rounded-md text-black hover:bg-gray-200 text-center "
                      // onClick={incrementCount}
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          className="w-6 h-6 text-[#d35c5c]"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            d="M12 4v16m8-8H4"
                          />
                        </svg>
                      </button>
                    </div>

                    <h4 className="mt-2 font-semibold text-center text-white">

                      {formatEther((nftPrice * count).toString())} ETH{" "}

                      <span className="text-sm text-gray-300"> + GAS</span>
                    </h4>

                    {/* Mint Button */}


                    <button
                      disabled={!currentChainId ||
                        currentChainId !== ChainId.Rinkeby || !account || minting}
                      className="mt-6 py-2 px-4 text-center text-white uppercase bg-[#222222] border-b-4 border-orange-700 rounded  hover:border-orange-400 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none"
                      onClick={handleWhitelistMint}
                    >
                      Mint Cryptid
                    </button>

                  </>) : stage < 3 && whitelistClaimable && account && claimed ?



                  (
                    <p className="text-white text-2xl mt-8 text-center">
                      Account: {" "} {shortenAddress(account)} has claimed their Whitelist Mint. <br></br><br></br>

                      {timerComponentsPublic.length ? <span>Public Sale will begin in... <br></br> {timerComponentsPublic}</span> : <span>Public Sale will be starting soon...</span>}

                    </p>
                  ) : stage < 3 && !whitelistClaimable && account ?



                  (
                    <p className="text-white text-2xl mt-8 text-center">
                      Account: {" "} {shortenAddress(account)} is not on the Whitelist. <br></br><br></br>

                      {timerComponentsPublic.length ? <span>Public Sale will begin in... <br></br> {timerComponentsPublic}</span> : <span>Public Sale will be starting soon...</span>}

                    </p>
                  ) :




                  stage == 4 && !account ? (
                    <>
                      {/* Minted NFT Ratio */}
                      <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                        <span className="text-[#d35c5c]">{`${totalSupply}`}</span> /
                        <span className="text-black"> {`${totalSaleSupply}`}</span>
                      </p>

                      <div className="flex items-center mt-6 text-3xl font-bold text-gray-200">


                        <button
                          className="flex items-center justify-center w-12 h-12 bg-white rounded-md hover:bg-gray-200 text-center disabled:bg-slate-50"
                          onClick={decrementCount}

                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="w-6 h-6 text-[#d35c5c] "
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="2"
                              d="M20 12H4"
                            />
                          </svg>
                        </button>

                        <h2 className="mx-8">{count}</h2>

                        <button
                          className="flex items-center justify-center w-12 h-12 bg-white rounded-md text-black hover:bg-gray-200 text-center "
                          onClick={incrementCount}
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="w-6 h-6 text-[#d35c5c]"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="2"
                              d="M12 4v16m8-8H4"
                            />
                          </svg>
                        </button>
                      </div>

                      <h4 className="mt-2 font-semibold text-center text-white">

                        {formatEther((nftPrice * count).toString())} ETH{" "}

                        <span className="text-sm text-gray-300"> + GAS</span>
                      </h4>

                      {/* Mint Button */}


                      <button
                        disabled={!currentChainId ||
                          currentChainId !== ChainId.Rinkeby || !account || minting}
                        className="mt-6 py-2 px-4 text-center text-white uppercase bg-[#222222] border-b-4 border-orange-700 rounded  hover:border-orange-400 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none"
                        onClick={handlePublicMint}
                      >
                        Mint Cryptid
                      </button>

                    </>
                  ) :
                  




                  stage == 4 && account ? (
                    <>
                      {/* Minted NFT Ratio */}
                      <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                        <span className="text-[#d35c5c]">{`${totalSupply}`}</span> /
                        <span className="text-black"> {`${totalSaleSupply}`}</span>
                        
                      </p>

                      <div className="flex items-center mt-6 text-3xl font-bold text-gray-200">


                        <button
                          className="flex items-center justify-center w-12 h-12 bg-white rounded-md hover:bg-gray-200 text-center disabled:bg-slate-50"
                          onClick={decrementCount}

                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="w-6 h-6 text-[#d35c5c] "
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="2"
                              d="M20 12H4"
                            />
                          </svg>
                        </button>

                        <h2 className="mx-8">{count}</h2>

                        <button
                          className="flex items-center justify-center w-12 h-12 bg-white rounded-md text-black hover:bg-gray-200 text-center "
                          onClick={incrementCount}
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="w-6 h-6 text-[#d35c5c]"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="2"
                              d="M12 4v16m8-8H4"
                            />
                          </svg>
                        </button>
                      </div>

                      <h4 className="mt-2 font-semibold text-center text-white">

                        {formatEther((nftPrice * count).toString())} ETH{" "}

                        <span className="text-sm text-gray-300"> + GAS</span>
                      </h4>

                      {/* Mint Button */}


                      <button
                        disabled={!currentChainId ||
                          currentChainId !== ChainId.Rinkeby || !account || minting}
                        className="mt-6 py-2 px-4 text-center text-white uppercase bg-[#222222] border-b-4 border-orange-700 rounded  hover:border-orange-400 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none"
                        onClick={handlePublicMint}
                      >
                        Mint Cryptid
                      </button>

                    </>
                  ) : soldOut ?



                  (
                    <p className="text-white text-2xl mt-8 text-center">
                      SOLD OUT!

                    </p>
                  ) 
                  : (
                    <p className="text-white text-2xl mt-8 text-center">
                      {/* Whitelist Sale Begins in {" "} <br></br> */}

                      {timerComponentsPublic.length ? <span>Public Sale will begin in... <br></br> {timerComponentsPublic}</span> : <span>Public Sale will be starting soon...</span>}

                    </p>
                  )}

          {/* Status */}
                    
          {status && (
           
            <div className="items-center inline-flex justify-center px-4 py-3 mt-8  font-semibold selection:bg-cryptid-3 text-white bg-cryptid-2 rounded-md">
              {status}
           
            </div>
          )}
          
          <br></br>
        </div>
      </div>
    </main>
  );
};

export default Hero;
