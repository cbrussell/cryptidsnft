import Head from "next/head";
import Image from "next/image";

import Header from "../components/Header";
import Hero from "../components/Hero";


export default function Home() {
  return (
    <div className="min-h-screen w-full bg-primary">
      <link
            rel="preload"
            href="/fonts/YkarRegular.woff"
            as="font"
            crossOrigin=""
          />
      <Header />
      <Hero />
    </div>
  );
}
