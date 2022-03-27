import Head from "next/head";
import Image from "next/image";

import Header from "../components/Header";
import Hero from "../components/Hero";
import Synopsis from "../components/Synopsis";
import Team from "../components/Team";
import FAQ from "../components/FAQ";
import Footer from "../components/Footer";


export default function Home() {
  return (
    <div className="min-h-screen w-full bg-primary">
        <Header />
        <Hero />
        <Synopsis />
        <Team />
        <FAQ />
        <Footer />
    </div>
  );
}
