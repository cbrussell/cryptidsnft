import Head from "next/head";
import Link from "next/link";
import { useState, useEffect } from "react";
import { useStatus } from "../context/statusContext";
import { connectWallet, getCurrentWalletConnected } from "../utils/interact";
require('typeface-exo')

const Header = () => {

  const { setStatus } = useStatus();

  const [walletAddress, setWalletAddress] = useState("");

  const connectWalletPressed = async () => {
    const walletResponse = await connectWallet();
    setWalletAddress(walletResponse.address);
    setStatus(walletResponse.status);
  };



  useEffect(() => {
    async function fetchData() {
      const walletResponse = await getCurrentWalletConnected();
      setWalletAddress(walletResponse.address);
      setStatus(walletResponse.status);
      addWalletListener();
    }
    fetchData();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const addWalletListener = () => {
    if (window.ethereum) {
      window.ethereum.on("accountsChanged", async (accounts) => {
        if (accounts.length > 0) {
          setWalletAddress(accounts[0]);
          setStatus("");
        } else {
          setWalletAddress("");
          setStatus("🦊 Connect to Metamask using Connect Wallet button.");
        }
      });
    }
  };

  return (

    <>
      <Head>

        <title>Cryptids</title>
        <meta name="description" content="Adminstrators of the Metaverse." />
        <link rel="icon" href="/favicon.svg" />

      </Head>

      <header className="sticky inset-x-5 top-0 z-10 h-32 md:h-20 min-w-full justify-center space-x-6 text-white  backdrop-filter bg-cryptid-1 ">
        <div className="md:flex items-center container justify-around  mx-auto max-w-7xl  h-full">
          <div className="flex justify-around">
            {/* Logo */}
            <Link href="#">
              <a className="text-4xl font-thin w-auto md:w-40 lg:w-80">
                <span className="element tracking-widest bg-clip-text bg-gradient-to-br text-black">
                  cRyptids
                </span>
              </a>
            </Link>
          </div>

          {/* Synopsis, Docs, FAQ, Links */}

          <nav aria-label="Main Menu">
            <ul className="flex justify-around items-center space-x-10" >

              <li className="text-black text-semibold exo-font hover:text-orange-900">
                <Link href="#synopsis">
                  <a>synopsis</a>
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

             

              {/* <li>
                <a href="https://cryptids.gitbook.io/" target="_blank" rel="noreferrer">
                  <svg
                    className="w-7 h-7"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M10.802 17.77a.703.703 0 1 1-.002 1.406a.703.703 0 0 1 .002-1.406m11.024-4.347a.703.703 0 1 1 .001-1.406a.703.703 0 0 1-.001 1.406m0-2.876a2.176 2.176 0 0 0-2.174 2.174c0 .233.039.465.115.691l-7.181 3.823a2.165 2.165 0 0 0-1.784-.937c-.829 0-1.584.475-1.95 1.216l-6.451-3.402c-.682-.358-1.192-1.48-1.138-2.502c.028-.533.212-.947.493-1.107c.178-.1.392-.092.62.027l.042.023c1.71.9 7.304 3.847 7.54 3.956c.363.169.565.237 1.185-.057l11.564-6.014c.17-.064.368-.227.368-.474c0-.342-.354-.477-.355-.477c-.658-.315-1.669-.788-2.655-1.25c-2.108-.987-4.497-2.105-5.546-2.655c-.906-.474-1.635-.074-1.765.006l-.252.125C7.78 6.048 1.46 9.178 1.1 9.397C.457 9.789.058 10.57.006 11.539c-.08 1.537.703 3.14 1.824 3.727l6.822 3.518a2.175 2.175 0 0 0 2.15 1.862a2.177 2.177 0 0 0 2.173-2.14l7.514-4.073c.38.298.853.461 1.337.461A2.176 2.176 0 0 0 24 12.72a2.176 2.176 0 0 0-2.174-2.174"
                      fill="#000"
                    ></path>
                  </svg>
                </a>
              </li> */}

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
          <nav aria-label="Wallet Button">
            <ul className="items-center space-x-6 text-center w-auto md:w-40 lg:w-80" >
              
                <li className="px-8 py-2 font-extrabold text-black border inline-block exo-font border-black rounded-lg cursor-pointer mt-2 md:mt-0" onClick={connectWalletPressed}>
                  <a

                    id="walletButton"




                  >
                    {walletAddress.length > 0 ? (
                      "Connected: " +
                      String(walletAddress).substring(0, 6) +
                      "..." +
                      String(walletAddress).substring(38)
                    ) : (
                      <span>Connect Wallet</span>
                    )}
                  </a>
                </li>
              
            </ul>
          </nav>
        </div>
      </header>
    </>
  )
};
export default Header;
