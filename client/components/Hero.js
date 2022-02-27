import React, { useState, useEffect } from "react";
import Image from "next/image";
import { useStatus } from "../context/statusContext";
import useSWR from 'swr'
import { useContractFunction, ChainId, useEthers, useEtherBalance } from "@usedapp/core";
import {
  getMaxMintAmount,
  getTotalSupply,
  mintNFT,
  getStage,
  getOwner,
  whitelistMint,
  checkIfClaimed,
} from "../pages/utils/interact"
import { parseEther, formatEther } from '@ethersproject/units'
import { Contract, utils } from 'ethers';
import cryptidTokenNFT from "../../contract/build/deployments/4/0x09E9A7e35399433f5dfD33D56c4111B982E2D0f7.json";

// var Web3 = require('web3');

const Hero = () => {

  const address = "0x09E9A7e35399433f5dfD33D56c4111B982E2D0f7";
  

  const { account, chainId: currentChainId, library, BigNumber } = useEthers();
  const { status, setStatus } = useStatus();
  const [count, setCount] = useState(1);
  const [maxMintAmount, setMaxMintAmount] = useState(0);
  const [totalSupply, setTotalSupply] = useState(0);
  // const [nftPrice, setNftPrice] = useState(10000000000000000);

  const nftPrice = 100000000000000000

  const [stage, setStage] = useState(0);
  const [minting, setMinting] = useState(false)
  const [claimed, setClaimed] = useState(false);
  const [whitelistClaimable, setWhitelistClaimable] = useState(false);
  const [owner, setOwner] = useState("");


  const fetcher = (url) => fetch(url).then((res) => res.json());

  const maxMintCalculated = getMaxMintAmount();

  // const salePriceCalculated = getSalePrice();

  const stageCalculated = getStage();

  const totalSupplyCalculated = getTotalSupply();

  const ownerCalculated = getOwner();






  
  const { abi: cryptidTokenABI } = cryptidTokenNFT;
  const cryptidTokenNFTInterface = new utils.Interface(cryptidTokenABI);


  const [contract, setContract] = useState(new Contract(address, cryptidTokenNFTInterface))



  useEffect(() => {
    console.log("Max Mint Per Transaction is " + maxMintCalculated);
    if (maxMintCalculated) setMaxMintAmount(maxMintCalculated);
  }, [maxMintCalculated]);


  // useEffect(() => {
  //   console.log("Sale price is " + salePriceCalculated + " wei");
  //   if (salePriceCalculated) setNftPrice(salePriceCalculated);
  // }, [salePriceCalculated]);

  useEffect(() => {
    console.log("The Current Stage is " + stageCalculated);
    if (stageCalculated) setStage(stageCalculated);
  }, [stageCalculated]);

  useEffect(() => {
    console.log("Current Minted Supply is " + totalSupplyCalculated);
    if (totalSupplyCalculated) setTotalSupply(totalSupplyCalculated);
  }, [totalSupplyCalculated]);

  useEffect(() => {
    console.log("The Owner is " + ownerCalculated);
    if (ownerCalculated) setOwner(ownerCalculated);
  }, [ownerCalculated]);



  // const updateTotalSupply = async () => {
  //   const mintedCount = await getTotalSupply();
  //   setTotalSupply(mintedCount);
  // };

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

  let whitelistProof = [];
  let whitelistValid = false;
  const whitelistRes = useSWR(stage < 3 && account ? `/api/whitelistProof?address=${account}` : null, {
    fetcher, revalidateIfStale: false, revalidateOnFocus: false, revalidateOnReconnect: false
  });
  if (!whitelistRes.error && whitelistRes.data) {
    const { proof, valid } = whitelistRes.data;
    // console.log(proof)
    whitelistProof = proof;
    whitelistValid = valid;
  }


  const { state: whitelistMintState, send: sendWhitelistMint } = useContractFunction(contract, 'whitelistMint', {})

  useEffect(() => {
    if (account && library) {
      setContract(new Contract(address, cryptidTokenNFTInterface, library.getSigner()))
    }
    console.log(library);
  }, [account, library])


  const price = '0.10';
  // const amountToWei = utils.parseEther(amount)

  const handleWhitelistMint = async () => {
    sendWhitelistMint(proof,{ value: amountToWei} )
  }



  const { state: publicMintState, send: sendPublicMint } = useContractFunction(contract, 'publicMint', { transactionName: 'publicMint' })
  const etherBalance = useEtherBalance(account)
  // const amountToWei = utils.parseEther(price) * count

  const handlePublicMint = async () => {
    const PRICE_PER_MINT = parseEther('0.01');
    const ethTotal = PRICE_PER_MINT.mul(count);

    if ( formatEther(etherBalance) < formatEther((nftPrice * count).toString())) {
      console.log("User Ether Balance is " + etherBalance)
      // console.log("Required amount of Ether to mint is " + Web3.utils.fromWei((nftPrice * count).toString(), 'ether'))
      setStatus('Not enough balance for this purchase')
      return
    }
    let gas;
    try {
      gas = await contract.estimateGas.publicMint(count, {value: ethTotal});
      console.log("Gas estimate is set to " + gas);
    } catch (err) {
      setStatus("😞Error: " + err.message);
    }

    if (gas) {

    console.log("Total required ETH for transaction is " + ethTotal + "wei");
    sendPublicMint(count, { gasLimit: gas.mul(115).div(100), value: ethTotal} )
    console.log("Gas estimate worked!");
    
    } else {
      console.log("Error: Gas estimate DID NOT work.");
      sendPublicMint(count, {value: ethTotal} )

    }
    
  }

  // console.log({state})

  useEffect(() => {
    if (whitelistMintState.status === 'None' || publicMintState.status === 'None') {
      setMinting(false);
    }
    if (whitelistMintState.status === 'PendingSignature' || publicMintState.status === 'PendingSignature') {
      setStatus(
        <p>{" "}Pending signature<span class="dots"><span>.</span><span>.</span><span>.</span></span>
        </p>
      )
      setMinting(true);
    }
    if (whitelistMintState.status === 'Mining' || publicMintState.status === 'Mining') {
      setStatus(
        <p>
          {" "}The transaction is in progress<span class="dots"><span>.</span><span>.</span><span>.</span></span>
        </p>
      )
      setMinting(true);
    }
    if (whitelistMintState.status === 'Exception' || publicMintState.status === 'Exception') {
      setStatus("Error:" + publicMintState.errorMessage)
      setMinting(false);
    }
    if (whitelistMintState.status === 'Success') {
      setStatus((
        <p>
          {" "}
          🦊 Check out your transaction on Etherscan: <a target="_blank" href={`https://rinkeby.etherscan.io/tx/` + whitelistMintState.receipt.transactionHash} className="alert">
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
          🦊 Success! Check out your transaction on Etherscan: <a target="_blank" href={`https://rinkeby.etherscan.io/tx/` + publicMintState.receipt.transactionHash} className="alert">
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
  }, [whitelistMintState, publicMintState]) 


  // const onMintWhitelist = async () => {
  //   const { success, status } = await mintWhitelist(account, whitelistProof);
  //   console.log(status);
  //   setWhitelistMintStatus(success);
  // };


  const onPublicMint = async () => {
    const { success, status } = await mintPublic(account, numToMint);
    console.log(status);
    setPublicMintStatus(success);
  };

  const calculateTimeLeft = () => {
    let year = new Date().getFullYear();
    const difference = +new Date('March 25 2022 16:00:00') - +new Date();
    let timeLeft = {};

    if (difference > 0) {
      timeLeft = {
        days: Math.floor(difference / (1000 * 60 * 60 * 24)),
        hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
        minutes: Math.floor((difference / 1000 / 60) % 60),
        seconds: Math.floor((difference / 1000) % 60),
      };
    }

    return timeLeft;
  };

  const [timeLeft, setTimeLeft] = useState(calculateTimeLeft());
  const [year] = useState(new Date().getFullYear());

  useEffect(() => {
    setTimeout(() => {
      setTimeLeft(calculateTimeLeft());
    }, 1000);
  });

  const timerComponents = [];

  Object.keys(timeLeft).forEach((interval) => {
    if (!timeLeft[interval]) {
      return;
    }

    timerComponents.push(
      <span>
        {timeLeft[interval]} {interval}{" "}
      </span>
    );
  })



  // While before stage 3, check if user is on WL 

  // useEffect(() => {
  //   if (stage > 2 || !whitelistValid) {
  //     setWhitelistClaimable(false);
  //     setClaimed(false);
  //     return;
  //   } else {
  //   async function validateClaim() {
  //     sampleNFT.methods.mintWhitelist(whitelistProof).call({ from: account, value: amountToWei }).then(() => {
  //       setWhitelistClaimable(CLAIMABLE);
  //     }).catch((err) => {
  //       if (err.toString().includes('claimed')) { setWhitelistClaimable(ALREADY_CLAIMED)}
  //       else { setWhitelistClaimable(NOT_CLAIMABLE) }
  //     });
  //   }
  //   validateClaim();
  // // eslint-disable-next-line react-hooks/exhaustive-deps
  // }}, [whitelistProof])


  return (
    <main id="main" className="h-screen py-10 md:py-4  bg-pattern ">
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


          {stage == 4 ? (
            <>
              {/* Minted NFT Ratio */}
              <p className=" bg-gray-100 rounded-md text-gray-800 font-bold text-lg my-4 py-1 px-3">
                <span className="text-[#d35c5c]">{`${totalSupply}`}</span> /
                11,111
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
              {/* {!status || status.toString().includes("Something") || JSON.stringify(status).includes("transaction") ? */}

              <button
                disabled={!currentChainId ||
                  currentChainId !== ChainId.Rinkeby || !account || minting}
                className="mt-6 py-2 px-4 text-center text-white uppercase bg-[#222222] border-b-4 border-orange-700 rounded  hover:border-orange-400 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none"
                onClick={handlePublicMint}
              >
                Mint Cryptid
              </button>

            </>
          ) : (
            <p className="text-white text-2xl mt-8 text-center">
              {/* Whitelist Sale Begins in {" "} <br></br> */}

              {timerComponents.length ? <span>Whitelist Sale will begin in... <br></br> {timerComponents}</span> : <span>Whitelist Sale will be starting soon...</span>}

            </p>
          )}

          {/* Status */}

          {status && (
            <div className="flex items-center  justify-center px-4 py-3 mt-8  font-semibold selection:bg-cryptid-3 text-white bg-cryptid-2 rounded-md ">
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
