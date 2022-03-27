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
    <>
      <header className="top-0  container mx-auto  justify-around z-10 h-32 md:h-20  md:flex-row text-white md:flex items-center     ">
        {/* <div className="md:flex items-center justify-around    h-full "> */}
          <div className="flex md:basis-1/3 justify-around ">
            {/* Logo */}
            <Link href="#">
              <a className="text-4xl font-thin w-auto  pt-1 md:pt-0 float-left">
                <span className="element tracking-widest bg-clip-text bg-gradient-to-br text-black">
                  cRyptids
                </span>
              </a>
            </Link>
          </div>

          {/* Synopsis, Docs, FAQ, Links */}

          <nav aria-label="Main Menu" className="basis-1/3">
    
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


             


            </ul>
       
          </nav>
          

          {/* Wallet */}
         


          {account ? (
           <div className="flex basis-1/3 justify-center">
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
            </div>
            
          ) : (
            <div className="flex basis-1/3 justify-around items-center py-2 sm:py-2">

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
