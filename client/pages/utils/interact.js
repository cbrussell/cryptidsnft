import { Contract, utils, BigNumber, formatEther } from "ethers";
import { useContractFunction, useContractCall, useCall } from "@usedapp/core"
import cryptidTokenNFT from "../../../contract/build/deployments/4/0x2F8C0A3da39910Ff83072F330000C93588885Dc5.json";

const address = "0x2F8C0A3da39910Ff83072F330000C93588885Dc5";
// const abi = require(`../../../contract/build/deployments/4/0x2F8C0A3da39910Ff83072F330000C93588885Dc5.json`);
const { abi: cryptidTokenABI } = cryptidTokenNFT;

const cryptidTokenNFTInterface = new utils.Interface(cryptidTokenABI);

const nftContract = new Contract(address, cryptidTokenNFTInterface)



export const whitelistMint = async (proof) => {
  const amount = '0.10';
  const amountToWei = utils.parseEther(amount.toString())
  const { state: whitelistMintState, send: whitelistMintSend } = useContractFunction(nftContract, "whitelistMint", {});
  await whitelistMintSend(proof, {value: amountToWei});
  return whitelistMintState;
};


export function getMaxMintAmount() {

  const value =  useCall({ 
    contract: nftContract, 
    method: "maxMintPerTx", 
    args: [],
  });
  return value;
}


export function getSalePrice() {
  const {value, error} =  useCall({ 
    contract: nftContract, 
    method: "salePrice", 
    args: [],
  }) ?? {} ;
  const weiValue = (value?.[0].toString())/(1000000000000000000)

  // const etherValue = formatEther(weiValue)


  if (error) {
    console.error(error.message)
    return undefined;
  } else {

    return weiValue;
  }
}

export function getStage() {

  const { value, error } =  useCall({ 
    contract: nftContract, 
    method: "stage", 
    args: [],
  }) ?? {};
  
  if (error) {
    console.error(error.message)
    return undefined;
  } else {
    return value?.[0]
  }
}


export function getTotalSupply() {

  const { value, error } =  useCall({ 
    contract: nftContract, 
    method: "totalSupply", 
    args: [],
  }) ?? {};
  
  if (error) {
    console.error(error.message)
    return undefined;
  } else {
    return value?.[0]
  }
}


export function getOwner() {

  const value =  useCall({ 
    contract: nftContract, 
    method: "owner", 
    args: [],
  });
  return value;
}

// export const getOwner = async (account) => {
//   if (account) {
//     const owner = await nftContract.methods.owner().call();
//     if (account == owner) {
//       return true;
//     } else {
//       return false;
//     }
//   }
// }


// export const getTotalSupply = async () => {
//   const result = await nftContract.methods.totalSupply().call();
//   return result;
// };


// export const getStage = async () => {
//   const result = await nftContract.methods.stage().call();
//   return result;
// };


// export function getSalePrice() {
//   const { value, error } =  
//     useCall({
//       contract: nftContract, 
//       method: "salePrice", 
//       args: [],
//      }) ?? {};
//      console.log("error is " + error)

//      if (error) {
//        console.error("Error", error.message);
//        return undefined;
//      }1

//      return { error, data: value?.[0] };
//     }



// export function useTotalSupply() {
//   const totalSupply = useContractCall({
//     abi: abiInterface,
//     address: tokenAddress,
//     method: "totalSupply",
//     args: [],
//   });

//   return totalSupply;
// }

// export function getMaxMintAmount() {
//   const result = useCall({
//     contract: createStakeContrcat(process.env.REACT_APP_STAKE_ADDRESS),
//     method: "stakingBalances",
//     args: [address, account],
//   });

//   return result;
// }


// export const getMaxMintAmount = async () => {
//   const result = await nftContract.methods.maxMintPerTx().call();
//   return result;
// };












// export const mintWhitelist = async (account, proof) => {
//   console.log('minting whitelist...');
//   const amount = '0.10';
//   const amountToWei = web3.utils.toWei(amount, 'ether');
//   const result = sampleNFT.methods.whitelistMint(proof).send({ from: account, value: amountToWei }).then((result) => {
//     console.log(`✅ Check out your transaction on Etherscan: https://etherscan.io/tx/` + result);
//     return {
//       success: true,
//       status: `✅ Check out your transaction on Etherscan: https://etherscan.io/tx/` + result
//     };
//   }).catch((err) => {
//     console.log("Mint transaction failed!");
//     return {
//       success: false,
//       status: "😥 Something went wrong: " + err.message
//     }
//   }).finally((result) => {
//     return result;
//   });
//   return result;
// }


// import {
//   useEthers,
//   shortenAddress,
//   ChainId,
//   getChainName,
// } from "@usedapp/core";
// const { account } = useEthers();


// const nftContract = new web3.eth.Contract(contract.abi, address);

// const { account } = useEthers();
// const switchToRinkeby = async () => {
//   if (window.ethereum) {
//       await window.ethereum.request({
//         method: "wallet_switchEthereumChain",
//         params: [{ chainId: "0x4" }],
//       });
//   }
// };

// let chainId = await window.ethereum.request({ method: 'eth_chainId'})
// console.log('Connected to chain:' + chainId)

// const rinkebyChainId = '0x4'

// if (chainId !== rinkebyChainId) {
//   return {
//     address: "",
//     status: (
//       <p>
//         😞 Error: You are not connected to the Rinkeby Testnet! Click {" "}

//         <button onclick={switchToRinkeby}>here</button> to Connect.

//       </p>
//     )

//     ,chainId: chainId
//   };
// }



// export const connectWallet = async () => {
//   if (window.ethereum) {


//     try {
//       const addressArray = await window.ethereum.request({
//         method: "eth_requestAccounts",
//       });

//       const obj = {
//         status: "",
//         address: addressArray[0]

//       };

//       return obj;
//     } catch (err) {
//       return {
//         address: "",
//         status: "😞 Error: " + err.message

//       };
//     }
//   } else {
//     return {
//       address: "",
//       status: (
//         <span>
//           <p>
//             {" "}
//             🦊{" "}
//             <a target="_blank" href="https://metamask.io/download.html" class="alert">
//               You must install Metamask, a virtual Ethereum wallet, in your
//               browser.
//             </a>
//           </p>
//         </span>
//       ),
//     };
//   }
// };




// export const getCurrentWalletConnected = async () => {
//   if (window.ethereum) {

//     let chainId = await window.ethereum.request({ method: 'eth_chainId'})
//     console.log('Connected to chain:' + chainId)

//     const rinkebyChainId = '0x4'

//     if (chainId !== rinkebyChainId) {
//       return {
//         address: "",
//         status: "😞 Error: You are not connected to the Rinkeby Testnet!"
//       };
//     }

//     try {
//       const addressArray = await window.ethereum.request({
//         method: "eth_accounts",
//       });

//       if (addressArray.length > 0) {
//         return {
//           address: addressArray[0],
//           status: "",
//         };
//       } else {
//         return {
//           address: "",
//           status: "🦊 Please connect wallet",
//         };
//       }
//     } catch (err) {
//       return {
//         address: "",
//         status: "😞 Error: " + err.message,
//       };
//     }
//   } else {
//     return {
//       address: "",
//       status: (
//         <span>
//           <p>
//             {" "}
//             🦊{" "}

//             <a target="_blank" href="https://metamask.io/download.html" class="alert">
//               You must install Metamask, a virtual Ethereum wallet, in your
//               browser.
//             </a>
//           </p>
//         </span>
//       ),
//     };
//   }
// };

// Contract Methods








// export const whitelistMint = async (mintAmount) => {
//   const result = await nftContract.methods.salePrice().call();
//   const resultEther = web3.utils.fromWei(result, "ether");

//   //set up your Ethereum transaction
//   const transactionParameters = {
//     to: contractAddress, // Required except during contract publications.
//     from: window.ethereum.selectedAddress, // must match user's active address.
//     value: parseInt(web3.utils.toWei(resultEther, "ether") * mintAmount).toString(
//       16
//     ), // hex
//     gasLimit: "0",
//     data: nftContract.methods.whitelistMint(mintAmount).encodeABI(), //make call to NFT smart contract
//   };
//   //sign the transaction via Metamask
//   try {
//     const txHash = await window.ethereum.request({
//       method: "eth_sendTransaction",
//       params: [transactionParameters],
//     });
//     return {
//       success: true,
//       status: (
//         <p>
//           {" "}
//           🦊 Check out your transaction on Etherscan: <a target="_blank" href={`https://rinkeby.etherscan.io/tx/` + txHash} className="alert">
//             {"https://rinkeby.etherscan.io/tx/" + txHash}
//           </a>
//         </p>
//       )
//     };
//   } catch (error) {
//     return {
//       success: false,
//       status: "😥 Something went wrong: " + error.message,
//     };
//   }
// };
