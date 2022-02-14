
const { createAlchemyWeb3 } = require("@alch/alchemy-web3");
const web3 = createAlchemyWeb3(process.env.NEXT_PUBLIC_API_URL);
const contract = require(`../../contract/build/deployments/4/0x2F8C0A3da39910Ff83072F330000C93588885Dc5.json`);
const contractAddress = "0x2F8C0A3da39910Ff83072F330000C93588885Dc5";


const nftContract = new web3.eth.Contract(contract.abi, contractAddress);
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
              
export const connectWallet = async () => {
  if (window.ethereum) {
   
    
    try {
      const addressArray = await window.ethereum.request({
        method: "eth_requestAccounts",
      });
      
      const obj = {
        status: "",
        address: addressArray[0]
    
      };

      return obj;
    } catch (err) {
      return {
        address: "",
        status: "😞 Error: " + err.message
    
      };
    }
  } else {
    return {
      address: "",
      status: (
        <span>
          <p>
            {" "}
            🦊{" "}
            <a target="_blank" href="https://metamask.io/download.html" class="alert">
              You must install Metamask, a virtual Ethereum wallet, in your
              browser.
            </a>
          </p>
        </span>
      ),
    };
  }
};



export const getCurrentWalletConnected = async () => {
  if (window.ethereum) {

    // let chainId = await window.ethereum.request({ method: 'eth_chainId'})
    // console.log('Connected to chain:' + chainId)

    // const rinkebyChainId = '0x4'

    // if (chainId !== rinkebyChainId) {
    //   return {
    //     address: "",
    //     status: "😞 Error: You are not connected to the Rinkeby Testnet!"
    //   };
    // }
    
    try {
      const addressArray = await window.ethereum.request({
        method: "eth_accounts",
      });

      if (addressArray.length > 0) {
        return {
          address: addressArray[0],
          status: "",
        };
      } else {
        return {
          address: "",
          status: "🦊 Please connect wallet",
        };
      }
    } catch (err) {
      return {
        address: "",
        status: "😞 Error: " + err.message,
      };
    }
  } else {
    return {
      address: "",
      status: (
        <span>
          <p>
            {" "}
            🦊{" "}
            
            <a target="_blank" href="https://metamask.io/download.html" class="alert">
              You must install Metamask, a virtual Ethereum wallet, in your
              browser.
            </a>
          </p>
        </span>
      ),
    };
  }
};

// Contract Methods

export const getMaxMintAmount = async () => {
  const result = await nftContract.methods.maxMintPerTx().call();
  return result;
};

export const getTotalSupply = async () => {
  const result = await nftContract.methods.totalSupply().call();
  return result;
};

export const getNftPrice = async () => {
  const result = await nftContract.methods.salePrice().call();
  const resultEther = web3.utils.fromWei(result, "ether");
  return resultEther;
};

export const getStage = async () => {
  const result = await nftContract.methods.stage().call();
  return result;
};

export const checkIfClaimed = async () => {
  if (window.ethereum) {
  const result = await nftContract.methods.claimed(window.ethereum.selectedAddress).call();
  return result;
  } 
  return false;
  
};


// export const mintWhitelist = async (account, proof) => {
//   console.log('minting whitelist...');
//   const amount = '0.10';
//     const amountToWei = web3.utils.toWei(amount, 'ether');
//   const result = sampleNFT.methods.whitelistMint(proof).send({ from: account, value: amountToWei }).then((result) => {
//     console.log(`✅ Check out your transaction on Etherscan: https://etherscan.io/tx/` + result);
//       return {
//         success: true,
//         status: `✅ Check out your transaction on Etherscan: https://etherscan.io/tx/` + result
//         };
//   }).catch((err) => {
//     console.log("Mint transaction failed!");
//     return {
//       success: false,
//       status: "😥 Something went wrong: " + err.message
//       }
//   }).finally((result) => {
//     return result;
//   });
//   return result;
// }



export const mintNFT = async (mintAmount) => {
  const result = await nftContract.methods.salePrice().call();
  const resultEther = web3.utils.fromWei(result, "ether");

  if (!window.ethereum.selectedAddress) {
    return {
      success: false,
      status: (
        <p>
          🦊 Connect to Metamask using the{" "}
          <p style="color:blue;" >Connect Wallet</p> button.
        </p>
      ),
    };
  }

  //set up your Ethereum transaction
  const transactionParameters = {
    to: contractAddress, // Required except during contract publications.
    from: window.ethereum.selectedAddress, // must match user's active address.
    value: parseInt(web3.utils.toWei(resultEther, "ether") * mintAmount).toString(
      16
    ), // hex
    gasLimit: "0",
    data: nftContract.methods.whitelistMint(mintAmount).encodeABI(), //make call to NFT smart contract
  };
  //sign the transaction via Metamask
  try {
    const txHash = await window.ethereum.request({
      method: "eth_sendTransaction",
      params: [transactionParameters],
    });
    return {
      success: true,
      status:( 
        <p>
          {" "}
          🦊 Check out your transaction on Etherscan: <a target="_blank" href={`https://rinkeby.etherscan.io/tx/` + txHash} className="alert">
              {"https://rinkeby.etherscan.io/tx/" + txHash}
            </a>
        </p>
        )
    };
  } catch (error) {
    return {
      success: false,
      status: "😥 Something went wrong: " + error.message,
    };
  }
};
