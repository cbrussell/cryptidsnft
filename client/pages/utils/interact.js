import { Contract, utils} from "ethers";
import { useCall } from "@usedapp/core"
import cryptidTokenNFT from "../../../contract/build/deployments/4/0x09E9A7e35399433f5dfD33D56c4111B982E2D0f7.json";

const address = "0x09E9A7e35399433f5dfD33D56c4111B982E2D0f7";

const { abi: cryptidTokenABI } = cryptidTokenNFT;

const cryptidTokenNFTInterface = new utils.Interface(cryptidTokenABI);

const nftContract = new Contract(address, cryptidTokenNFTInterface)

export function getMaxMintAmount() {
  const {value, error } =  useCall({ 
    contract: nftContract, 
    method: "maxMintPerTx", 
  }) ?? {};
  if (error) {
    console.error(error.message)
    return undefined;
  } else {
    return value?.[0]
  }
}

// export function getSalePrice() {
//   const {value, error} =  useCall({ 
//     contract: nftContract, 
//     method: "salePrice", 
//     args: [],
//   }) ?? {} ;
//   const weiValue = parseInt(value?.[0]).toString()
  // console.log(weiValue)
  // var weiValue = utils.toBigNumber(value?.[0]);
  // const weiValue = parseInt((value?.[0]).toString())


  // const ether = Web3.utils.fromWei(weiValue, 'ether')

//   if (error) {
//     console.error(error.message)
//     return undefined;
//   } else {
//     return weiValue;
//   }
// }

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
  const { value, error } =  useCall({ 
    contract: nftContract, 
    method: "owner", 
    args: [],
  }) ?? {};
  if (error) {
    console.error(error.message)
    return undefined;
  } else {
    return value?.[0]
  }
}

// export const whitelistMint = async (proof) => {
//   const amount = '0.10';
//   const amountToWei = utils.parseEther(amount.toString())
//   const { state: whitelistMintState, send: whitelistMintSend } = useContractFunction(nftContract, "whitelistMint", {});
//   await whitelistMintSend(proof, {value: amountToWei});
//   return whitelistMintState;
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
