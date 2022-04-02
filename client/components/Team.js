import React, { useState } from "react";
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
              <video width="300" height="300" alt="Crussell Cryptid" className="self-center rounded-xl" autoPlay loop muted playsInline>
                <source src="/videos/2.mp4" type="video/mp4" />
              </video>

              <p className=" text-white text-center text-lg leading-9 font-normal">
                <a href="https://twitter.com/chrisrusselljr" target="_blank" rel="noreferrer" className="hover:text-cryptid-3">@Crussell</a>
              </p>
              <p className=" text-white text-center text-lg leading-9 font-normal pb-10">
                Developer
              </p>
            </div>
            <div className="px-7">
             
              <video width="300" height="300" alt="Nosolo Cryptid" className="self-center rounded-xl" autoPlay loop muted playsInline>
                <source src="/videos/9.mp4" type="video/mp4" />
              </video>
              <p className=" text-white text-center text-lg leading-9 font-normal">
                <a href="https://twitter.com/no__solo" target="_blank" rel="noreferrer" className="hover:text-cryptid-3">@NoSolo</a>
              </p>
              <p className=" text-white text-center text-lg leading-9 font-normal pb-10">
                Artist
              </p>
            </div>
            <div className="px-7">
              <video width="300" height="300" alt="Sentella Cryptid" className="self-center rounded-xl" autoPlay loop muted playsInline>
                <source src="/videos/20.mp4" type="video/mp4" />
              </video>
            
              <p className=" text-white text-center text-lg leading-9 font-normal">
                <a href="https://twitter.com/sen_tella" target="_blank" rel="noreferrer" className="hover:text-cryptid-3">@Sentella</a>
              </p>
              <p className=" text-white text-center text-lg leading-9 font-normal pb-10">
                Marketing Director
              </p>
            </div>

            <div className="px-7">
             
              <video width="300" height="300" alt="Grove Cryptid" className="self-center rounded-xl" autoPlay loop muted playsInline>
                <source src="/videos/7.mp4" type="video/mp4" />
              </video>
              <p className=" text-white text-center text-lg leading-9 font-normal">
                @Grove
              </p>
              <p className=" text-white text-center text-lg leading-9 font-normal pb-10">
                Lore Master
              </p>
            </div>



          </div>



        </div>
      </div>

    </div>
  );
}