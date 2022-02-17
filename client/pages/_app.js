import "../styles/globals.css";
import { StatusProvider } from "../context/statusContext";

import { ChainId, DAppProvider } from "@usedapp/core";

// const config = {
//   readOnlyChainId: ChainId.Arbitrum,
//   readOnlyUrls: {
//     [ChainId.ArbitrumRinkeby]:
//       "https://arb-rinkeby.g.alchemy.com/v2/PDUCdHLoNrdDJwgVvCNPTx7MrHuQ0uBg",
//     [ChainId.Arbitrum]: `https://arb-mainnet.g.alchemy.com/v2/${process.env.NEXT_PUBLIC_ALCHEMY_KEY}`,
//   },
// };

const config = {
  readOnlyChainId: ChainId.Rinkeby,
  readOnlyUrls: {
    [ChainId.Rinkeby]: 'https://rinkeby.infura.io/v3/b0d18bbb81f54079b165803b666e2957'
  }
}


function MyApp({ Component, pageProps }) {
  return (
    <DAppProvider config={config}>
      <StatusProvider>
        <Component {...pageProps} />
      </StatusProvider>
      </DAppProvider>
  );
}

export default MyApp;
