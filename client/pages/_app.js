import "../styles/globals.css";
import { StatusProvider } from "../context/statusContext";
import { ChainId, DAppProvider } from "@usedapp/core";

import { ToastContainer } from 'react-toastify';

import 'react-toastify/dist/ReactToastify.css';



// const config = {
//   readOnlyChainId: ChainId.Arbitrum,
//   readOnlyUrls: {
//     [ChainId.ArbitrumRinkeby]:
//       "https://arb-rinkeby.g.alchemy.com/v2/PDUCdHLoNrdDJwgVvCNPTx7MrHuQ0uBg",
//     [ChainId.Arbitrum]: `https://arb-mainnet.g.alchemy.com/v2/${process.env.NEXT_PUBLIC_ALCHEMY_KEY}`,
//   },
// };

const config = {
  readOnlyChainId: ChainId.ArbitrumRinkeby,
  readOnlyUrls: {
    [ChainId.ArbitrumRinkeby]: `https://arbitrum-rinkeby.infura.io/v3/${process.env.NEXT_PUBLIC_INFURA_ID}`
    // `https://arbitrum-rinkeby.infura.io/v3/${process.env.NEXT_PUBLIC_INFURA_ID}`
  }
}


function MyApp({ Component, pageProps }) {
  return (
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
  );
}

export default MyApp;
