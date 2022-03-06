import "../styles/globals.css";
import { StatusProvider } from "../context/statusContext";
import { ChainId, DAppProvider } from "@usedapp/core";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const config = {
  readOnlyChainId: ChainId.Arbitrum,
  readOnlyUrls: {
    [ChainId.Arbitrum]: `https://arbitrum-mainnet.infura.io/v3/${process.env.NEXT_PUBLIC_INFURA_ID}`
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
