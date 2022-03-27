import React, { useState } from "react";
import Head from "next/head";
import Image from "next/image";
export default function MyApp() {


  return (
    <div id="team">
      <div className="flex flex-col items-center justify-center sm:px-0 px-6 z-20 py-5   bg-cryptid-5">
        <div className="md:pt-30 sm:pt-5">
          <h2 role="heading" className="element md:text-4xl selection:bg-cryptid-2 selection:text-gray-800 text-2xl mb-10 text-center font-bold  leading-10 text-white">
            The Team
          </h2>
          <div className="flex flex-wrap justify-center">
            <div className="px-7">
            <Image
              src='/images/24.png'
              width="300"
              height="300"
              unoptimized='true'
              alt="Blank Cryptid 1"
              className="self-center rounded-xl"
            />
            <p className=" text-white text-center text-lg leading-9 font-normal">
            <a href="https://twitter.com/chrisrusselljr" target="_blank" rel="noreferrer" className="hover:text-cryptid-3">@chrisrusselljr</a>
            </p>
            <p className=" text-white text-center text-lg leading-9 font-normal pb-10">
            Developer
            </p>
            </div>
            <div className="px-7">
            <Image
              src='/images/3.GIF'
              width="300"
              height="300"
              unoptimized='true'
              alt="Blank Cryptid 1"
              className="self-center rounded-xl"
            />
            <p className=" text-white text-center text-lg leading-9 font-normal">
            <a href="https://twitter.com/no__solo" target="_blank" rel="noreferrer"className="hover:text-cryptid-3">@NoSolo</a>
            </p>
            <p className=" text-white text-center text-lg leading-9 font-normal pb-10">
            Artist
            </p>
            </div>
            
            
            
          </div>
          
        

        </div>
      </div>

    </div>
  );
}