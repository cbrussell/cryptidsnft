import React, { useState, useEffect } from "react";
import Image from "next/image";
import { useStatus } from "../context/statusContext";
import keccak256 from "keccak256";
import MerkleTree from "merkletreejs";
import { ContractAddress } from '../data/contract';

import { useContractFunction, ChainId, useEthers, shortenAddress } from "@usedapp/core";
import {
  GetTotalSupply,
  GetTotalSaleSupply,
  GetStage,
  Verify,
  CheckIfClaimed,
} from "../utils/interact"
import { Contract, utils } from 'ethers';
import cryptidTokenNFT from "../../contract/build/deployments/42161/0x5A39174e7F2B669a51Ec179eF49b3eca7ddB96AB.json";
import marshal_leaves from "../data/test_leaves.json";
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Hero = () => {
  const { account, chainId: currentChainId, library, BigNumber } = useEthers();
  const { status, setStatus } = useStatus();
  const [nftPrice, setNftPrice] = useState(100000000000000000);

  const [stage, setStage] = useState(0);

  const [minting, setMinting] = useState(false)
  const [claimed, setClaimed] = useState(0);
  const [whitelistClaimable, setWhitelistClaimable] = useState(false);

  const stageCalculated = GetStage();

  const totalSupplyCalculated = GetTotalSupply();
  const totalSaleSupplyCalculated = GetTotalSaleSupply();

  const claimedCalculated = CheckIfClaimed(account ?? '0x0000000000000000000000000000000000000000');

  const { abi: cryptidTokenABI } = cryptidTokenNFT;
  const cryptidTokenNFTInterface = new utils.Interface(cryptidTokenABI);
  const [contract, setContract] = useState(new Contract(ContractAddress, cryptidTokenNFTInterface));
  const [whitelistProof, setWhitelistProof] = useState([])


  const whitelistClaimableCalculated = Verify((account ?? '0x0000000000000000000000000000000000000000'), whitelistProof);

  const switchToArbitrum = async () => {
    if (window.ethereum) {
      try {
        await window.ethereum.request({
          method: "wallet_switchEthereumChain",
          params: [{ chainId: "0xa4b1" }],
        });
      } catch (switchError) {
        if (switchError.code === 4902) {
          try {
            await window.ethereum.request({
              method: "wallet_addEthereumChain",
              params: [
                {
                  chainId: "0xa4b1",
                  rpcUrls: ["https://arb1.arbitrum.io/rpc"],
                  chainName: "Arbitrum One",
                  blockExplorerUrls: ["https://arbiscan.io"],
                  nativeCurrency: {
                    name: "ETH",
                    symbol: "ETH",
                    decimals: 18,
                  },
                },
              ],
            });
          } catch (addError) {
            toast.error("Something went wrong while switching networks.");
          }
        }
      }
    }
  };

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
  }, [account, currentChainId])

  useEffect(() => {
    console.log("Current account whitelist verified status is: ", whitelistClaimableCalculated);
    setWhitelistClaimable(whitelistClaimableCalculated);
  }, [whitelistClaimableCalculated, currentChainId]);


  useEffect(() => {
    console.log("Current account claimed is: ", claimedCalculated);
    setClaimed(claimedCalculated);
  }, [claimedCalculated]);

  useEffect(() => {
    console.log("The Current Stage is " + stageCalculated);
    if (stageCalculated) setStage(stageCalculated);
  }, [stageCalculated]);

  useEffect(() => {
    if (account && library) {
      setContract(new Contract(ContractAddress, cryptidTokenNFTInterface, library.getSigner()))
    }
    console.log(library);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [account, library])


  const soldOut = totalSaleSupplyCalculated && totalSupplyCalculated && totalSaleSupplyCalculated?.eq(totalSupplyCalculated);


  const { state: publicMintState, send: sendPublicMint } = useContractFunction(contract, 'publicMint', {})

  const handlePublicMint = async () => {

    sendPublicMint()
    console.log(publicMintState.status)
  }


  const { state: whitelistMintState, send: sendWhitelistMint } = useContractFunction(contract, 'whitelistMint', {})



  const handleWhitelistMint = async () => {

    const ethTotal = (nftPrice).toString()

    if (!whitelistClaimable) {
      console.log("Unable to generate valid whitelist proof for account")
      setStatus("Error: Unable to generate valid whitelist proof for account: ", account)
      return
    }

    if (claimed === 1) {
      console.log("Whitelist is already claimed for account ", account);
      setStatus("Error: Whitelist mint is already claimed")
    }

    sendWhitelistMint(whitelistProof)

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
        <p className="text-center">
          {" "}
          🦊 Minting Cryptid<span className="dots"><span>.</span><span>.</span><span>.</span></span><br></br>
        </p>
      ))
      setMinting(true);
    }
    if (publicMintState.status === 'Mining') {
      setStatus((
        <p className="text-center">
          {" "}
          🦊 Minting Cryptid<span className="dots"><span>.</span><span>.</span><span>.</span></span><br></br>
        </p>
      ))
      setMinting(true);
    }
    if (whitelistMintState.status === 'Exception') {
      setStatus("Error: " + whitelistMintState.errorMessage)
      setMinting(false);
    }
    if (publicMintState.status === 'Exception') {
      setStatus("Error: " + publicMintState.errorMessage)
      setMinting(false);
    }
    if (whitelistMintState.status === 'Success') {
      setStatus((
        <p className="text-center">
          {" "}
          ✅ Success!<br></br>Check out your <a target="_blank" rel="noreferrer" href={`https://arbiscan.io/tx/` + whitelistMintState.receipt.transactionHash} className="alert">
            transaction
          </a>
          &#160;on Arbiscan!
        </p>
      ))
      setMinting(false);

    }
    if (publicMintState.status === 'Success') {
      setStatus((
        <p className="text-center">
          {" "}
          ✅ Success!<br></br>Check out your <a target="_blank" rel="noreferrer" href={`https://arbiscan.io/tx/` + publicMintState.receipt.transactionHash} className="alert">
            transaction
          </a>
          &#160;on Arbiscan!
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
    const difference = +new Date(Date.UTC(2022,5,16,23,0,0)) - +new Date();
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
    const difference = +new Date(Date.UTC(2022,5,13,17,0,0)) - +new Date();
  
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

  const mainImages = [
    '/images/10_blank.png',
    '/images/11_blank.png',
    '/images/12_blank.png',
    '/images/13_blank.png',
    '/images/14_blank.png',
    '/images/15_blank.png',
    '/images/26_blank.png',
    '/images/27_blank.png',
    '/images/28_blank.png',
    '/images/29_blank.png',
    '/images/30_blank.png',
  ];



  const leftImages = [
    '/images/1_blank.png',
    '/images/2_blank.png',
    '/images/3_blank.png',
    '/images/4_blank.png',
    '/images/5_blank.png',
    '/images/6_blank.png',
    '/images/7_blank.png',
    '/images/8_blank.png',
    '/images/9_blank.png',

  ];

  const rightImages = [
    '/images/16_blank.png',
    '/images/17_blank.png',
    '/images/18_blank.png',
    '/images/19_blank.png',
    '/images/20_blank.png',
    '/images/21_blank.png',
    '/images/22_blank.png',
    '/images/23_blank.png',
    '/images/24_blank.png',
    '/images/25_blank.png'
  ];

  const [randomMainImage, setRandomMainImage] = useState('/images/10_blank.png');
  const [randomLeftImage, setRandomLeftImage] = useState('/images/1_blank.png');
  const [randomRightImage, setRandomRightImage] = useState('/images/2_blank.png');



  useEffect(() => {

    setRandomMainImage(mainImages[Math.floor(Math.random() * mainImages.length)]);
    setRandomLeftImage(leftImages[Math.floor(Math.random() * leftImages.length)]);
    setRandomRightImage(rightImages[Math.floor(Math.random() * rightImages.length)]);

  }, []);

  return (
    <main id="main" className="h-fit py-10 md:py-0 md:pb-40  bg-pattern ">

      <div className="container max-w-6xl mx-auto flex flex-col items-center pt-4">
        <div className="flex flex-col items-center">
          <div className="flex pb-2">
            <div className="pt-5">
              <Image
                src={randomLeftImage}
                width="300"
                height="300"
                unoptimized='true'
                alt="Blank Cryptid 1"
                className="self-center"
              />
            </div>

            <div className="pt-2">
              <Image
                src={randomMainImage}
                width="310"
                height="310"
                alt="Blank Cryptid 2"
                unoptimized='true'
                className="rounded-md "
              />
            </div>
            <div className="pt-5">
              <Image
                src={randomRightImage}
                width="300"
                height="300"
                unoptimized='true'
                alt="Blank Cryptid 3"
                className="rounded-md"
              />
            </div>
          </div>
          

          {
            currentChainId && stage < 2 &&
              currentChainId !== ChainId.Arbitrum && !soldOut ?
              (
                <p className="text-white text-xl mt-6 text-center">
                  You are connected to Mainnet. Please <button className="text-yellow-400 underline hover:text-yellow-200" onClick={switchToArbitrum}> switch to Arbitrum. </button><br></br>
                  <p className="text-lg">  (If you are on mobile, switch networks in the wallet app.)</p>

                  <br></br>
                  {timerComponentsPublic.length ? <span>Whitelist Sale will begin in... <br></br> {timerComponentsWhitelist}</span> : <span>Whitelist Sale will be starting soon...</span>}
                
                </p>
              )

              :
              currentChainId && stage == 2 &&
                currentChainId !== ChainId.Arbitrum && !soldOut ?
                (
                  <p className="text-white text-xl mt-6 text-center">
                    You are connected to Mainnet. Please <button className="text-yellow-400 underline hover:text-yellow-200" onClick={switchToArbitrum}> switch to Arbitrum. </button><br></br>
                    <p className="text-lg">  (If you are on mobile, switch networks in the wallet app.)</p>


                    <p className="text-white text-xl mt-8 text-center">
                      Whitelist Sale is <b>Active</b> <br></br><br></br>
                    </p>
                  </p>
                )

                :

                currentChainId && stage == 3 &&
                  currentChainId !== ChainId.Arbitrum && !soldOut ?
                  (
                    <p className="text-white text-xl mt-6 text-center">
                      You are connected to Mainnet. Please <button className="text-yellow-400 underline hover:text-yellow-200" onClick={switchToArbitrum}> switch to Arbitrum. </button><br></br>
                      <p className="text-lg">  (If you are on mobile, switch networks in the wallet app.)</p>

                      <br></br>

                      {timerComponentsPublic.length ? <span>Public Sale will begin in... <br></br> {timerComponentsPublic}</span> : <span>Public Sale will be starting soon...</span>}
                      {/* Launching Ealy June 2022 */}
                    </p>
                  )

                  :
                  currentChainId && stage == 4 &&
                    currentChainId !== ChainId.Arbitrum && !soldOut ?
                    (
                      <p className="text-white text-xl mt-6 text-center">
                        You are connected to Mainnet. Please <button className="text-yellow-400 underline hover:text-yellow-200" onClick={switchToArbitrum}> switch to Arbitrum. </button><br></br>
                        <p className="text-lg">  (If you are on mobile, switch networks in the wallet app.)</p>


                        <p className="text-white text-xl mt-8 text-center">
                          Public Sale is <b>Active</b> <br></br><br></br>
                        </p>
                      </p>
                    )

                    :
                    stage < 2 && !account && !soldOut ?
                      (
                        <p className="text-white text-xl mt-6 text-center">

                          <br></br>
                          {timerComponentsPublic.length ? <span>Whitelist Sale will begin in... <br></br> {timerComponentsWhitelist}</span> : <span>Whitelist Sale will be starting soon...</span>}
                          {/* Launching Early June 2022 */}
                        </p>
                      )

                      :

                      stage < 2 && whitelistClaimable && account && claimed === 0 ?
                        (
                          <p className="text-white text-xl mt-8 text-center">
                            Account: {" "} {shortenAddress(account)} has 1 Whitelist Mint Available <br></br><br></br>

                            {timerComponentsWhitelist.length ? <span>Whitelist Sale will begin in... <br></br> {timerComponentsWhitelist}</span> : <span>Whitelist Sale will be starting soon...</span>}
                            {/* Launching Early June 2022 */}
                          </p>
                        )



                        : stage == 2 && !account ?
                          (
<>
                                <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                                  <span className="text-[#d35c5c]">{`${totalSupplyCalculated}`}</span> /
                                  <span className="text-black">{`${totalSaleSupplyCalculated}`}</span>
                                </p>
                            <p className="text-white text-xl mt-8 text-center">
                              Whitelist Sale is <b>Active</b> <br></br><br></br>
                            </p>
                            </>
                          ) : stage == 2 && whitelistClaimable && account && claimed === 0 ?
                            (
                              <>
                                <p className="text-white text-xl mt-8 text-center">
                                  Account: {" "} {shortenAddress(account)} has 1 Whitelist Mint Available <br></br><br></br>
                                </p>
                                {/* Minted NFT Ratio */}
                                <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                                  <span className="text-[#d35c5c]">{`${totalSupplyCalculated}`}</span> /
                                  <span className="text-black">{`${totalSaleSupplyCalculated}`}</span>
                                </p>

        

                                <h4 className="mt-2 font-semibold text-center mb-2 text-white">
                                  0.00 ETH

                                  <span className="text-sm text-gray-300"> + GAS</span>
                                </h4>

                                {/* Mint Button */}


                                <button
                                  disabled={!currentChainId ||
                                    currentChainId !== ChainId.Arbitrum || !account || minting}
                                  className="mt-6 py-2 px-4 text-center text-white uppercase bg-[#222222] border-b-4 border-orange-700 rounded  hover:border-orange-400 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none"
                                  onClick={handleWhitelistMint}
                                >
                                  Mint Cryptid
                                </button>

                              </>) : stage < 3 && whitelistClaimable && account && claimed === 1 ?



                              (
                                <>
                                <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                                  <span className="text-[#d35c5c]">{`${totalSupplyCalculated}`}</span> /
                                  <span className="text-black">{`${totalSaleSupplyCalculated}`}</span>
                                </p>
                                <p className="text-white text-xl mt-8 text-center">
                                  Account: {" "} {shortenAddress(account)} has claimed their Whitelist Mint 😊 <br></br><br></br>

                                  {timerComponentsPublic.length ? <span>Public Sale will begin in... <br></br> {timerComponentsPublic}</span> : <span>Public Sale will be starting soon...</span>}

                                </p>
                                
                                </>
                                
                              ) : stage < 3 && !whitelistClaimable && account ?
                                

                                (
                                  <>
                                <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                                  <span className="text-[#d35c5c]">{`${totalSupplyCalculated}`}</span> /
                                  <span className="text-black">{`${totalSaleSupplyCalculated}`}</span>
                                </p>
                                  <p className="text-white text-xl mt-8 text-center">
                                    Account: {" "} {shortenAddress(account)} is not on the Whitelist 😔 <br></br><br></br>

                                    {timerComponentsPublic.length ? <span>Public Sale will begin in... <br></br> {timerComponentsPublic}</span> : <span>Public Sale will be starting soon...</span>}
                                    {/* Launching Early June 2022 */}
                                  </p>
                                  </>
                                ) :




                                stage == 4 && !account && !soldOut ? (
                                  <>
                                    {/* Minted NFT Ratio */}
                                    <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                                      <span className="text-[#d35c5c]">{`${totalSupplyCalculated}`}</span> /
                                      <span className="text-black"> {`${totalSaleSupplyCalculated}`}</span>
                                    </p>

                                   

                                    <h4 className="mt-2 font-semibold text-center text-white">

                                     0.00 ETH

                                      <span className="text-sm text-gray-300"> + GAS</span>
                                    </h4>

                                    {/* Mint Button */}


                                    <button
                                      disabled={!currentChainId ||
                                        currentChainId !== ChainId.Arbitrum || !account || minting}
                                      className="mt-6 py-2 px-4 text-center text-white uppercase bg-[#222222] border-b-4 border-orange-700 rounded  hover:border-orange-400 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none"
                                      onClick={handlePublicMint}
                                    >
                                      Mint Cryptid
                                    </button>

                                  </>
                                ) 
                                :





                                  stage == 4 && account && !soldOut && currentChainId && claimed === 0 ? (
                                    <>
                                      {/* Minted NFT Ratio */}
                                      <p className="text-white text-xl mt-8 text-center">
                                  2 mints remaining <br></br><br></br>

                                  

                                </p>

                                      <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                                        <span className="text-[#d35c5c]">{`${totalSupplyCalculated}`}</span> /
                                        <span className="text-black"> {`${totalSaleSupplyCalculated}`}</span>

                                      </p>

                                    
                                      <h4 className="mt-2 font-semibold text-center text-white">

                                       0.00 ETH

                                        <span className="text-sm text-gray-300"> + GAS</span>
                                      </h4>

                                      {/* Mint Button */}


                                      <button
                                        disabled={!currentChainId ||
                                          currentChainId !== ChainId.Arbitrum || !account || minting || claimed === 2 }
                                        className="mt-6 py-2 px-4 text-center text-white uppercase bg-[#222222] border-b-4 border-orange-700 rounded  hover:border-orange-400 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none"
                                        onClick={handlePublicMint}
                                      >
                                        Mint Cryptid
                                      </button>

                                    </>
                                  ) 
                                  :





                                  stage == 4 && account && !soldOut && currentChainId && claimed === 1 ? (
                                    <>
                                      {/* Minted NFT Ratio */}
                                      <p className="text-white text-xl mt-8 text-center">
                                 1 mint remaining<br></br><br></br>

                                  

                                </p>

                                      <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                                        <span className="text-[#d35c5c]">{`${totalSupplyCalculated}`}</span> /
                                        <span className="text-black"> {`${totalSaleSupplyCalculated}`}</span>

                                      </p>

                                    
                                      <h4 className="mt-2 font-semibold text-center text-white">

                                       0.00 ETH

                                        <span className="text-sm text-gray-300"> + GAS</span>
                                      </h4>

                                      {/* Mint Button */}


                                      <button
                                        disabled={!currentChainId ||
                                          currentChainId !== ChainId.Arbitrum || !account || minting || claimed === 2 }
                                        className="mt-6 py-2 px-4 text-center text-white uppercase bg-[#222222] border-b-4 border-orange-700 rounded  hover:border-orange-400 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none"
                                        onClick={handlePublicMint}
                                      >
                                        Mint Cryptid
                                      </button>

                                    </>
                                  ) 
                                :





                                  stage == 4 && account && !soldOut && currentChainId && claimed === 2 ? (
                                    <>
                                      {/* Minted NFT Ratio */}
                                      <p className="text-white text-xl mt-8 text-center">
                                  0 mints remaining <br></br><br></br>

                                  

                                </p>

                                      <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                                        <span className="text-[#d35c5c]">{`${totalSupplyCalculated}`}</span> /
                                        <span className="text-black"> {`${totalSaleSupplyCalculated}`}</span>

                                      </p>

                                    
                                      <h4 className="mt-2 font-semibold text-center text-white">

                                       0.00 ETH

                                        <span className="text-sm text-gray-300"> + GAS</span>
                                      </h4>

                                      {/* Mint Button */}


                                      <button
                                        disabled={!currentChainId ||
                                          currentChainId !== ChainId.Arbitrum || !account || minting || claimed === 2 }
                                        className="mt-6 py-2 px-4 text-center text-white uppercase bg-[#222222] border-b-4 border-orange-700 rounded  hover:border-orange-400 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none"
                                        onClick={handlePublicMint}
                                      >
                                        Mint Cryptid
                                      </button>

                                    </>
                                  ) 
                                  :





                                  stage == 4 && account && !soldOut && currentChainId ? (
                                    <>
                                      {/* Minted NFT Ratio */}
                                      <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                                        <span className="text-[#d35c5c]">{`${totalSupplyCalculated}`}</span> /
                                        <span className="text-black"> {`${totalSaleSupplyCalculated}`}</span>

                                      </p>

                                    
                                      <h4 className="mt-2 font-semibold text-center text-white">

                                       0.00 ETH

                                        <span className="text-sm text-gray-300"> + GAS</span>
                                      </h4>

                                      {/* Mint Button */}


                                      <button
                                        disabled={!currentChainId ||
                                          currentChainId !== ChainId.Arbitrum || !account || minting }
                                        className="mt-6 py-2 px-4 text-center text-white uppercase bg-[#222222] border-b-4 border-orange-700 rounded  hover:border-orange-400 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none"
                                        onClick={handlePublicMint}
                                      >
                                        Mint Cryptid
                                      </button>

                                    </>
                                  ) 
                                  : soldOut ?
<>
                                      {/* Minted NFT Ratio */}
                                      <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                                        <span className="text-[#d35c5c]">{`${totalSupplyCalculated}`}</span> /
                                        <span className="text-black"> {`${totalSaleSupplyCalculated}`}</span>

                                      </p>


                                    

                                      <p className="text-white text-3xl mt-8 pb-3 text-bold  text-center">
                                        sold out

                                      </p>




                                    
                                    </>
                                    : (

                                      <>
                                <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                                  <span className="text-[#d35c5c]">{`${totalSupplyCalculated}`}</span> /
                                  <span className="text-black">{`${totalSaleSupplyCalculated}`}</span>
                                </p>
                                      <p className="text-white text-xl mt-8 text-center">


                                        {timerComponentsPublic.length ? <span>Public Sale will begin in... <br></br> {timerComponentsPublic}</span> : <span>Public Sale will be starting soon...</span>}
                                  
                                      </p>
                                      </>
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
