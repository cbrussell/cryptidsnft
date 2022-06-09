import "../styles/globals.css";
import { StatusProvider } from "../context/statusContext";
import { ChainId, DAppProvider } from "@usedapp/core";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Head from "next/head";

const config = {
  readOnlyChainId: ChainId.Arbitrum,
  readOnlyUrls: {
    [ChainId.Arbitrum]: `https://arbitrum-mainnet.infura.io/v3/${process.env.NEXT_PUBLIC_INFURA_ID}`,
    [ChainId.ArbitrumRinkeby]: `https://arbitrum-rinkeby.infura.io/v3/${process.env.NEXT_PUBLIC_INFURA_ID}`

  }
}

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head id="home">
        <title>Cryptids</title>
        <meta name="title" content="Cryptids" />
        <meta name="description" content="Part storybook fantasy, part science-fiction. CRYPTIDS is a generative art project of 7,777 fantastic mythical creatures. Created by @no__solo and @chrisusselljr." />
        <link rel="icon" href="/favicon.svg" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="http://www.cryptids.app/" />
        <meta property="og:title" content="Cryptids" />
        <meta property="og:description" content="Part storybook fantasy, part science-fiction. CRYPTIDS is a generative art project of 7,777 fantastic mythical creatures. Created by @no__solo and @chrisusselljr." />
        <meta property="og:image" content="https://gateway.pinata.cloud/ipfs/QmX7YrhWoRzTdbSqU65pxn4pS6tUwTQW9WGMPr35iKDpdn" />
        <script async src="https://cdn.splitbee.io/sb.js"></script>
     
        <link
          rel="preload"
          href="/fonts/YkarRegular.woff2"
          as="font"
          crossOrigin="anonymous"
          type="font/woff2"
        />
        <link
          rel="preload"
          href="/fonts/YkarRegular.woff"
          as="font"
          crossOrigin="anonymous"
          type="font/woff"
        /> 
      </Head>
      <DAppProvider config={config}>
        <StatusProvider>
          <Component {...pageProps} />
        </StatusProvider>
        <ToastContainer
          position='bottom-left'
          autoClose={5000}
          autoDismiss={true}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          icon={true}
          theme={'colored'}
          pauseOnHover={false}
          rtl={false}
        />
      </DAppProvider>
    </>
  );
}

export default MyApp;
