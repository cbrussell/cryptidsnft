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
        <Header />
        <Hero />
        <Synopsis />
        {/* <Roadmap /> */}
        <FAQ />
 
    </div>
  );
}
