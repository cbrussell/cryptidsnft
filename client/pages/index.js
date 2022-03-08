import Head from "next/head";
import Image from "next/image";

import Header from "../components/Header";
import Hero from "../components/Hero";
import Synopsis from "../components/Synopsis";
// import Roadmap from "../components/Roadmap";
import FAQ from "../components/FAQ";


export default function Home() {
  return (
    <div className="min-h-screen w-full bg-primary">
      <Head id="home">
        <title>Cryptids</title>
        <meta name="description" content="Part storybook fantasy, part science-fiction. Cryptids is a generative NFT art project of 11,111 unique mythical creatures. Created by @no__solo an @chrisusselljr."/>
        <link rel="icon" href="/favicon.svg" />

     
        <meta
          property="og:image"
          content="https://gateway.pinata.cloud/ipfs/QmThg99oeGNYSHChmbeGbG6282XZBfhgD2zn88Z7PKLdy1"
        />
       
        <script async src="https://cdn.splitbee.io/sb.js"></script>
        {/* <Script src="https://cdn.splitbee.io/sb.js"></Script> */}


        <link
        rel="preload"
        href="/fonts/Exo-Regular.woff"
        as="font"
        crossOrigin=""
        type="font/woff"
      />
      <link
        rel="preload"
        href="/fonts/Exo-Regular.woff2"
        as="font"
        crossOrigin=""
        type="font/woff2"
      />
      <link
        rel="preload"
        href="/fonts/YkarRegular.woff2"
        as="font"
        crossOrigin=""
        type="font/woff2"
      />
      <link
        rel="preload"
        href="/fonts/YkarRegular.woff"
        as="font"
        crossOrigin=""
        type="font/woff"
      />
      </Head>
        <Header />
        <Hero />
        <Synopsis />
        {/* <Roadmap /> */}
        <FAQ />
 
 
    </div>
  );
}
