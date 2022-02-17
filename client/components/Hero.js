import React, { useState, useEffect } from "react";
import Image from "next/image";
import { useStatus } from "../context/statusContext";
import useSWR from 'swr'
import { ChainId, useEthers } from "@usedapp/core";
import {
  getMaxMintAmount,
  getTotalSupply,
  getNftPrice,
  mintNFT,
  getStage,
  checkIfClaimed,
} from "../utils/interact";

// const contract = require(`../../contract/build/deployments/4/0x2F8C0A3da39910Ff83072F330000C93588885Dc5.json`);
const Hero = () => {
  // const contract = require(`../../contract/build/deployments/4/0x2F8C0A3da39910Ff83072F330000C93588885Dc5.json`);
  // const nftContract = new web3.eth.Contract(contract.abi, process.env.NFT_ADDRESS);
  const {account, chainId: currentChainId} = useEthers();

  const { status, setStatus } = useStatus();

  const [count, setCount] = useState(1);
  const [maxMintAmount, setMaxMintAmount] = useState(0);
  const [totalSupply, setTotalSupply] = useState(0);
  const [nftPrice, setNftPrice] = useState("0.10");
  const [stage, setStage] = useState(0);
  const [claimed, setClaimed] = useState(false);
  
  
  const [correctNetwork, setCorrectNetwork] = useState(false)
  const fetcher = (url) => fetch(url).then((res) => res.json());

  useEffect(() => {
    async function fetchData() {
      // if (stage == 2 ) {
      // setClaimed(await checkIfClaimed());
      // }
      setMaxMintAmount(await getMaxMintAmount());
      setNftPrice(await getNftPrice());
      setStage(await getStage());
      await updateTotalSupply();
    }
    fetchData();
  }, []);


  // useEffect(() => {
  //   async function fetchData() {
  //     if (stage == 2 ) {
  //       setClaimed(await checkIfClaimed());
  //     }
  //   }
  //   fetchData();
  // }, [account]);



  const updateTotalSupply = async () => {
    const mintedCount = await getTotalSupply();
    setTotalSupply(mintedCount);
  };

  const incrementCount = () => {
    if (count < maxMintAmount) {
      setCount(count + 1);
    }
  };

  // const checkIfClaimed = async () => {
  
  //   if (account) {
  //   const result = await nftContract.methods.claimed(account).call();
  //   return result;
  //   } 
  //   return false;
    
  // };


  const decrementCount = () => {
    if (count > 1) {
      setCount(count - 1);
    }
  };

  const mintCryptid = async () => {
    const { status } = await mintNFT(count);
    setStatus(status);

    // We minted a new Cryptid, so we need to update the total supply
    updateTotalSupply();
  };


  // useEffect(() => {
  //   async function fetchData() {
  //   if (stage == 2 ) {
  //     setClaimed(await checkIfClaimed());
  //     return;
  //   }
  //   setClaimed(await checkIfClaimed());
    
  // }
  // fetchData();
    
    // async function checkIfClaimed() {
    //   sampleNFT.methods.claimed(window.ethereum.selectedAddress).call({ from: window.ethereum.selectedAddress }).then((result) => {
    //     setAlreadyClaimed(result);
    //     console.log(result);
    //   }).catch((err) => {
    //     setAlreadyClaimed(false);
    //   });
    // }
    // checkIfClaimed();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  // }, []);


  let whitelistProof = [];

  let whitelistValid = false;

  const whitelistRes = useSWR(stage == 2 && window.ethereum.selectedAddress ? `/api/whitelistProof?address=${window.ethereum.selectedAddress}` : null, {
    fetcher, revalidateIfStale: false, revalidateOnFocus: false, revalidateOnReconnect: false });
  if (!whitelistRes.error && whitelistRes.data) {
    const { proof, valid } = whitelistRes.data;
    whitelistProof = proof;
    whitelistValid = valid;
    // console.log(whitelistProof);
  }


  // useEffect(() => {
  //   if (stage == 2 || !whitelistValid) {
  //     setWhitelistClaimable(NOT_CLAIMABLE);
  //     return;
  //   } else if (alreadyClaimed) {
  //     setWhitelistClaimable(ALREADY_CLAIMED);
  //     return;
  //   }
  //   async function validateClaim() {
  //     const amount = '0.10';
  //     const amountToWei = web3.utils.toWei(amount, 'ether');
  //     sampleNFT.methods.whitelistMint(whitelistProof).call({ from: account, value: amountToWei }).then(() => {
  //       setWhitelistClaimable(CLAIMABLE);
  //     }).catch((err) => {
  //       if (err.toString().includes('claimed')) { setWhitelistClaimable(ALREADY_CLAIMED)}
  //       else { setWhitelistClaimable(NOT_CLAIMABLE) }
  //     });
  //   }
  //   validateClaim();
  // // eslint-disable-next-line react-hooks/exhaustive-deps
  // }, [whitelistProof])



  return (
    <main id="main" className="h-screen py-10 md:py-8  bg-pattern ">
      <div className="container max-w-6xl mx-auto flex flex-col items-center pt-4">
        <div className="flex flex-col items-center">
          <div className="flex pb-2">
            <Image
              src="/images/BlankCryptid6.png"
              width="300"
              height="300"
              alt="Blank Cryptid 1"
              className="rounded-md"
            />
            <Image
              src="/images/BlankCryptid.png"
              width="350"
              height="350"
              alt="Blank Cryptid 2"
              className="rounded-md"
            />
            <Image
              src="/images/BlankCryptid2.png"
              width="300"
              height="300"
              alt="Blank Cryptid 3"
              className="rounded-md"
            />
          </div>

          {stage > 1 && !claimed ? (
            <>
              {/* Minted NFT Ratio */}
              <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                <span className="text-[#d35c5c]">{`${totalSupply}`}</span> /
                11,111
              </p>

              <div className="flex items-center mt-6 text-3xl font-bold text-gray-200">


                <button
                  className="flex items-center justify-center w-12 h-12 bg-white rounded-md hover:bg-gray-200 text-center"
                  onClick={decrementCount}
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
                      d="M20 12H4"
                    />
                  </svg>
                </button>

                <h2 className="mx-8">{count}</h2>

                <button
                  className="flex items-center justify-center w-12 h-12 bg-white rounded-md text-black hover:bg-gray-200 text-center"
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
                {nftPrice} ETH{" "}
                <span className="text-sm text-gray-300"> + GAS</span>
              </h4>

              {/* Mint Button */}
              {/* {!status || status.toString().includes("Something") || JSON.stringify(status).includes("transaction") ? */}
                <button
                  disabled={!currentChainId ||
                    currentChainId !== ChainId.Rinkeby || status || !account}
                  className="mt-6 py-2 px-4 text-center text-white uppercase bg-[#222222] border-b-4 border-orange-700 rounded  hover:border-orange-400 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none"
                  onClick={mintCryptid}
                >
                  Mint Cryptid
                </button>
                
            </>
          ) : (
            <p className="text-white text-2xl mt-8">
              {" "}
              Sale is not active yet!
            </p>
          )}

          {/* Status */}

          {status && (
            <div className="flex items-center  justify-center px-4 py-4 mt-8 font-semibold selection:bg-cryptid-3 text-white bg-cryptid-2 rounded-md ">
              {status}
            </div>
          )}
        </div>
      </div>
    </main>
  );
};

export default Hero;
