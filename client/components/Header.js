import Head from "next/head";
import Link from "next/link";
import { useState, useEffect, Fragment } from "react";
import { SpeakerphoneIcon } from "@heroicons/react/outline";
import { useStatus } from "../context/statusContext";
import { Dialog, Transition } from '@headlessui/react'
import Image from "next/image";
import { formatEther } from '@ethersproject/units'
import MetaMaskSvg from "../public/images/metamask.svg";
import WalletConnectSvg from "../public/images/walletconnect.svg";
import Coinbase from "../public/images/coinbase.png";
import { useEthers, shortenAddress, getChainName, ChainId, chainName, useEtherBalance, useTokenBalance, useLookupAddress} from "@usedapp/core";
import { WalletLinkConnector } from "@web3-react/walletlink-connector";
import { WalletConnectConnector } from "@web3-react/walletconnect-connector";
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
require('typeface-exo')

const walletLink = new WalletLinkConnector({
  url: 'https://arb1.arbitrum.io/rpc',
  appName: "CRYPTIDS",
  supportedChainIds: [ChainId.Arbitrum, ChainId.ArbitrumRinkeby],
});

const walletconnect = new WalletConnectConnector({
  rpc: {
    [ChainId.Arbitrum]: `https://arbitrum-mainnet.infura.io/v3/${process.env.NEXT_PUBLIC_INFURA_ID}`,
    [ChainId.ArbitrumRinkeby]: `https://arbitrum-rinkeby.infura.io/v3/${process.env.NEXT_PUBLIC_INFURA_ID}`,
  },
  bridge: 'https://bridge.walletconnect.org',
  infuraId: process.env.NEXT_PUBLIC_INFURA_ID,
  qrcode: true,
});


const Header = () => {

  
  const [myEther, setMyEther] = useState("0");


  const { activateBrowserWallet, account, activate, deactivate, chainId: currentChainId } = useEthers();


  const etherBalance = useEtherBalance(account)

  useEffect(() => {
    if (etherBalance) setMyEther(Number(formatEther(etherBalance)).toFixed(3));
  }, [etherBalance, currentChainId]);


  const accountName = useLookupAddress();




  useEffect(() => {
    if (!account) {
      setStatus("🦊 Connect to Metamask using the Connect Wallet button.") 
    } else {
      setStatus("")
    }
    
  }, [account]); // eslint-disable-line react-hooks/exhaustive-deps


  const { setStatus } = useStatus();

 



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
                    name: "AETH",
                    symbol: "AETH",
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

  const onClose = () => setIsOpenWalletModal(false);

  const [isOpenWalletModal, setIsOpenWalletModal] = useState(false);


  useEffect(() => {
    if (!account) {
      setStatus("🦊 Connect to Metamask using the Connect Wallet button.") 
    } else {
      setStatus("")
    }
    
  }, [account]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleClipboard = () => {
    navigator.clipboard.writeText(account || 'clipboard');
    toast.info('Wallet Address copied to Clipboard.');
  };

  return (

    // <>

    //   {currentChainId &&
    //     currentChainId !== ChainId.Arbitrum && (
    //       <div className="bg-cryptid-6">
    //         <div className="max-w-7xl mx-auto py-3 px-3 sm:px-6 lg:px-8">
    //           <div className="flex sm:items-center lg:justify-between flex-col space-y-2 sm:space-y-0 sm:flex-row">
    //             <div className="flex-1 flex items-center">
    //               <span className="flex p-2 rounded-lg bg-cryptid-3">
    //                 <SpeakerphoneIcon
    //                   className="h-6 w-6 text-white"
    //                   aria-hidden="true"
    //                 />
    //               </span>
    //               <p className="ml-3 font-medium text-white truncate">
    //                 <span className="lg:hidden">
    //                   Please switch to Arbitrum Mainnet.
    //                 </span>
    //                 <span className="hidden lg:block exo-font">
    //                   You are currently on the {getChainName(currentChainId)}{" "}
    //                   Network. Please switch to Arbitrum Mainnet.
    //                 </span>
    //               </p>
    //             </div>
    //             <div className="flex-shrink-0 w-full sm:mt-0 sm:w-auto">
    //               <button
    //                 onClick={switchToArbitrum}
    //                 className="w-full flex items-center justify-center exo-font px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-yellow-600 bg-white hover:bg-yellow-50"
    //               >
    //                 Switch Networks
    //               </button>
    //             </div>
    //           </div>
    //         </div>
    //       </div>
    //     )}
    <>
      <header className=" inset-x-5 top-0 z-10 h-32 md:h-20 min-w-full justify-center space-x-6 text-white  backdrop-filter ">
        <div className="md:flex items-center container justify-around  mx-auto max-w-7xl  h-full ">
          <div className="flex justify-around">
            {/* Logo */}
            <Link href="#">
              <a className="text-4xl font-thin w-auto md:w-40 lg:w-80 pt-1 md:pt-0">
                <span className="element tracking-widest bg-clip-text bg-gradient-to-br text-black">
                  cRyptids
                </span>
              </a>
            </Link>
          </div>

          {/* Synopsis, Docs, FAQ, Links */}

          <nav aria-label="Main Menu">
            <ul className="flex justify-around items-center space-x-10 pt-1 md:pt-0  px-2 sm:px-3" >

              <li className="text-black text-semibold exo-font hover:text-orange-900">
                <Link href="#synopsis">
                  <a>synopsis</a>
                </Link>
              </li>

              <li className="text-black text-semibold exo-font hover:text-orange-900">
                <Link href="#team">
                  <a>team</a>
                </Link>
              </li>

              <li className="text-black text-semibold exo-font hover:text-orange-900">
                <Link href="#faq">
                  <a>faq</a>
                </Link>
              </li>

              <li className="text-black text-semibold exo-font hover:text-orange-900">
                <a href="https://cryptids.gitbook.io/" target="_blank" rel="noreferrer" >
                  <a>docs</a>
                </a>
              </li>


              <li>
                <a href="https://twitter.com/cryptidsnft" target="_blank" rel="noreferrer">
                  <svg
                    className="w-7 h-7"
                    stroke="currentColor"
                    fill="currentColor"
                    strokeWidth="0"
                    viewBox="0 0 512 512"
                    xmlns="http://www.w3.org/2000/svg"
                  // fill="fill-blue-500"


                  >
                    <path d="M459.37 151.716c.325 4.548.325 9.097.325 13.645 0 138.72-105.583 298.558-298.558 298.558-59.452 0-114.68-17.219-161.137-47.106 8.447.974 16.568 1.299 25.34 1.299 49.055 0 94.213-16.568 130.274-44.832-46.132-.975-84.792-31.188-98.112-72.772 6.498.974 12.995 1.624 19.818 1.624 9.421 0 18.843-1.3 27.614-3.573-48.081-9.747-84.143-51.98-84.143-102.985v-1.299c13.969 7.797 30.214 12.67 47.431 13.319-28.264-18.843-46.781-51.005-46.781-87.391 0-19.492 5.197-37.36 14.294-52.954 51.655 63.675 129.3 105.258 216.365 109.807-1.624-7.797-2.599-15.918-2.599-24.04 0-57.828 46.782-104.934 104.934-104.934 30.213 0 57.502 12.67 76.67 33.137 23.715-4.548 46.456-13.32 66.599-25.34-7.798 24.366-24.366 44.833-46.132 57.827 21.117-2.273 41.584-8.122 60.426-16.243-14.292 20.791-32.161 39.308-52.628 54.253z"
                      fill="#000"
                    ></path>

                  </svg>
                </a>
              </li>

              <li>
                <a href="https://discord.gg/cryptids" target="_blank" rel="noreferrer">
                  <svg
                    className="w-7 h-7"
                    stroke="currentColor"
                    fill="currentColor"
                    strokeWidth="0"
                    viewBox="0 0 448 512"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path d="M297.216 243.2c0 15.616-11.52 28.416-26.112 28.416-14.336 0-26.112-12.8-26.112-28.416s11.52-28.416 26.112-28.416c14.592 0 26.112 12.8 26.112 28.416zm-119.552-28.416c-14.592 0-26.112 12.8-26.112 28.416s11.776 28.416 26.112 28.416c14.592 0 26.112-12.8 26.112-28.416.256-15.616-11.52-28.416-26.112-28.416zM448 52.736V512c-64.494-56.994-43.868-38.128-118.784-107.776l13.568 47.36H52.48C23.552 451.584 0 428.032 0 398.848V52.736C0 23.552 23.552 0 52.48 0h343.04C424.448 0 448 23.552 448 52.736zm-72.96 242.688c0-82.432-36.864-149.248-36.864-149.248-36.864-27.648-71.936-26.88-71.936-26.88l-3.584 4.096c43.52 13.312 63.744 32.512 63.744 32.512-60.811-33.329-132.244-33.335-191.232-7.424-9.472 4.352-15.104 7.424-15.104 7.424s21.248-20.224 67.328-33.536l-2.56-3.072s-35.072-.768-71.936 26.88c0 0-36.864 66.816-36.864 149.248 0 0 21.504 37.12 78.08 38.912 0 0 9.472-11.52 17.152-21.248-32.512-9.728-44.8-30.208-44.8-30.208 3.766 2.636 9.976 6.053 10.496 6.4 43.21 24.198 104.588 32.126 159.744 8.96 8.96-3.328 18.944-8.192 29.44-15.104 0 0-12.8 20.992-46.336 30.464 7.68 9.728 16.896 20.736 16.896 20.736 56.576-1.792 78.336-38.912 78.336-38.912z"
                      fill="#000"
                    ></path>
                  </svg>
                </a>
              </li>


            </ul>
          </nav>

          {/* Wallet */}
         


          {account ? (
            <div className="py-1 w-auto md:w-auto items-center rounded-lg bg-cryptid-6 mt-2 md:mt-0  p-0.5   exo-font font-bold select-none pointer-events-auto mx-2 justify-around sm:transform-none flex md:flex">
              <div className="px-2 py-1 sm:py-2 items-center  flex  md:text-center  container justify-center ">
                <span className="text-white block exo-font sm:text-base text-lg ">

                  {myEther && myEther}
               


                </span>{" "}
                <span className="text-white ml-2  exo-font flex items-center justify-center sm:text-base text-lg  md:text-center ">
                  ETH
                </span>
              </div>

              <button
              className="flex relative items-center px-5 overflow-hidden group justify-center container md:text-center py-1 rounded-lg active:border-neutral-800 active:shadow-none shadow-lg bg-gradient-to-tr from-neutral-800 to-neutral-700 border-neutral-900  text-white text-semibold exo-font border-b-4 border-l-2 sm:text-base text-lg"
              onClick={handleClipboard}>
                 <span className='absolute w-0 h-0 transition-all duration-300 ease-out bg-white rounded-full group-hover:w-48 group-hover:h-40 opacity-10'></span>
                {accountName ?? shortenAddress(account)}
                </button>


              <button
              className='rounded-lg relative flex w-full  sm:px-3 exo-font group items-center md:text-center  py-1 justify-center px-3 sm:text-base text-lg  m-1 cursor-pointer text-semibold border-b-4 border-l-2 active:border-indigo-600 active:shadow-none shadow-lg bg-gradient-to-tr from-indigo-600 to-indigo-500 border-indigo-700 text-white overflow-hidden'
              onClick={() => deactivate()}
            >
              <span className='absolute w-0 h-0 transition-all duration-300 ease-out bg-white rounded-full group-hover:w-32 group-hover:h-32 opacity-10'></span>
              Disconnect
            </button>
            </div>
          ) : (
            <div className="flex justify-around items-center py-2 sm:py-2">

            {/* <button
              className="flex items-center mx-2   px-6 py-2.5 justify-center  md:w-auto sm:w-1/2 text-center  exo-font  border rounded text-semibold  font-bold text-white   bg-cryptid-5 hover:bg-gray-700 focus:outline-none  focus:ring-1 focus:ring-offset-2 focus:ring-gray-900"
              onClick={() => setIsOpenWalletModal(true)}
            >
              Connect Wallet
            </button> */}

            <button
            className='rounded-lg relative inline-flex exo-font group mx-2  items-center md:w-auto sm:w-1/2   justify-center px-6 py-2 m-1 cursor-pointer text-semibold  font-bold border-b-4 border-l-2 active:border-indigo-600 active:shadow-none shadow-lg bg-gradient-to-tr from-indigo-600 to-indigo-500 border-indigo-700 text-white overflow-hidden'
            onClick={() => setIsOpenWalletModal(true)}
          >
            <span className='absolute w-0 h-0 transition-all duration-300 ease-out bg-white rounded-full group-hover:w-52 group-hover:h-32 opacity-10'></span>
            Connect Wallet
          </button>


            </div>
          )}


        </div>

        <Transition show={isOpenWalletModal} as={Fragment}>
          <Dialog
            as="div"
            className="fixed inset-0 z-10 overflow-y-auto"
            open={isOpenWalletModal}
            onClose={() => setIsOpenWalletModal(false)}>
            <div className="min-h-screen px-4 text-center">
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0"
                enterTo="opacity-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100"
                leaveTo="opacity-0"
              >
                <Dialog.Overlay className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
              </Transition.Child>
              {/* This element is to trick the browser into centering the modal contents. */}
              <span
                className="inline-block h-screen align-middle"
                aria-hidden="true"
              >
                &#8203;
              </span>
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 scale-95"
                enterTo="opacity-100 scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 scale-100"
                leaveTo="opacity-0 scale-95"
              >
                <div className="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl">
                 
                  {/* <Dialog.Title
                    as="h3"
                    className="text-lg font-medium leading-6 text-gray-900"
                  >
                    Payment successful
                  </Dialog.Title>
                  <div className="mt-2">
                    <p className="text-sm text-gray-500">
                      Your payment has been successfully submitted. We’ve sent you
                      an email with all of the details of your order.
                    </p>
                  </div>
                 
                  <div className="mt-4">
                    <button
                      type="button"
                      className="inline-flex justify-center px-4 py-2 text-sm font-medium text-blue-900 bg-blue-100 border border-transparent rounded-md hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
                      onClick={onClose}
                    >
                      Got it, thanks!
                    </button>

                  </div>
                </div> */}
                <div className="grid grid-cols-1 divide-y-[1px] sm:divide-y-0 sm:grid-cols-2">
          <div className="flex justify-center px-4 py-3">
            <button
              className="flex items-center justify-center flex-col  hover:bg-gray-700 rounded-md"
              onClick={() => {
                activateBrowserWallet();
                onClose();
              }}
            >
              <p className="md:text-xl sm:text-lg mb-2 ">MetaMask</p>
              <p className="text-gray-400  sm:text-sm text-xs mb-8 font-exo">
                Connect to your MetaMask Wallet
              </p>
              <Image
                src={MetaMaskSvg.src}
                alt="MetaMask"
                height={48}
                width={48}
              />
            </button>
          </div>
          <div className="flex justify-center px-4 py-3">
            <button
              className="flex items-center justify-center flex-col  hover:bg-gray-700 rounded-md"
              onClick={async () => {
                try {
                  await activate(walletconnect);
                } catch (err) {
                  setStatus("😞 Error: " + err.message);
                } finally {
                  onClose();
                }
              }}
              
            >
              <p className="md:text-xl sm:text-lg mb-2">WalletConnect</p>
              <p className="text-gray-400  sm:text-sm text-xs mb-8">
                Scan with WalletConnect to connect
              </p>
              <Image
                src={WalletConnectSvg.src}
                alt="WalletConnect"
                height={48}
                width={48}
              />
            </button>
          </div>
          <div className="sm:col-span-2 sm:mt-2 flex justify-center px-4 py-3">
            <button
              className="flex items-center justify-center flex-col  hover:bg-gray-700 rounded-md"
              onClick={async () => {
                try {
                  await activate(walletLink);
                } catch (err) {
                  setStatus("😞 Error: " + err.message);
                } finally {
                  onClose();
                }
              }}
            >
              <p className="md:text-xl sm:text-lg mb-2">Coinbase Wallet</p>
              <p className="text-gray-400  sm:text-sm text-xs mb-8">
                Scan with Coinbase Wallet to connect
              </p>
              <Image
                src={Coinbase.src}
                alt="Coinbase Wallet"
                height={48}
                width={48}
              />
            </button>
          </div>
        </div>
        </div>
              </Transition.Child>
            </div>
          </Dialog>
        </Transition>

      </header>

    </>
  )
};
export default Header;
