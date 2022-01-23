import React, { useState } from "react";
import Head from "next/head";
export default function MyApp() {
   
  const [faq1, setFaq1] = useState(false);
  const [faq2, setFaq2] = useState(false);
  const [faq3, setFaq3] = useState(false);
  const [faq4, setFaq4] = useState(false);

  return (
    <div id="faq">
      <div className=" flex flex-col items-center justify-center sm:px-0 px-6 z-20 pb-32 bg-faq md:pt-30 sm:pt-5 ">
        <div className="py-20 md:py-30 lg:py-32 ">
          <h1
            role="heading"
            className=" md:text-4xl text-2xl leading-10 element text-white"
          >
            FAQ
          </h1>
        </div>
        <div className="lg:w-1/2 md:w-8/12 sm:w-9/12 w-full">
          <div className="bg-white shadow rounded p-8 cursor-pointer" onClick={() => setFaq1(!faq1)}>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-bold uppercase text-lg leading-none cursor-pointer text-gray-800" >
                  What are Cryptids?
                </h2>
              </div>
              <button
                className="focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2 ring-offset-white cursor-pointer"
              >
                {faq1 ? (
                  <svg
                    role="button"
                    aria-label="close dropdown"
                    width="10"
                    height="6"
                    viewBox="0 0 10 6"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M1 5L5 1L9 5"
                      stroke="#4B5563"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                ) : (
                  <svg
                    width="10"
                    role="button"
                    aria-label="open dropdown"
                    height="6"
                    viewBox="0 0 10 6"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M1 1L5 5L9 1"
                      stroke="#4B5563"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"

                    />
                  </svg>
                )}
              </button>
            </div>

            {faq1 && (
              <ul className="">
                <li>
                  <p className="text-lg leading-normal text-gray-600 mt-4 text-justify">
                  Cryptids are the first known inhabitants of the Metaverse. Only recently proven to exist and even more recently began to be understood. 
                  Cryptids choose their appearance by looking into our faded memories. To one, a wolf; a fox to another. To some, a form enitrely unknown.  
                   
                  <br></br>
                  <br></br>
            
                  Only through deeper exploration into Nos Atomos can we discover the true nature of CRYPTIDS...
                  </p>
                </li>
              </ul>
            )}
          </div>
          <div className="bg-white shadow rounded p-8 mt-8 cursor-pointer" onClick={() => {
                  setFaq2(!faq2);
                }}>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-bold  uppercase text-lg leading-none text-gray-800 cursor-pointer">
                  Who are the Pioneers?
                </h2>
              </div>
              <button
                
                data-menu
                className="focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2 ring-offset-white cursor-pointer"
              >
                {faq2 ? (
                  <svg
                    role="button"
                    aria-label="close dropdown"
                    width="10"
                    height="6"
                    viewBox="0 0 10 6"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M1 5L5 1L9 5"
                      stroke="#4B5563"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                ) : (
                  <svg
                    width="10"
                    role="button"
                    aria-label="open dropdown"
                    height="6"
                    viewBox="0 0 10 6"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M1 1L5 5L9 1"
                      stroke="#4B5563"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                )}
              </button>
            </div>
            {faq2 && (
              <ul>
                <li>
                  <p className="text-lg leading-normal text-gray-600 mt-4 text-justify">
                    {`The Pioneers represent the first wave explorers to Nos Atomos. Escaping the unfavorable
                    conditions of Terra, they've bought a one-way ticket with hopes to find a better
                    future in the Metaverse.`}
                  </p>
                </li>
              </ul>
            )}
          </div>
          <div className="bg-white shadow rounded p-8 mt-8 cursor-pointer" onClick={() => {
                  setFaq3(!faq3);
                }}>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-bold  uppercase text-lg leading-none text-gray-800">
                  Who are the Metanauts?
                </h2>
              </div>
              <button
                
                data-menu
                className="focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2 ring-offset-white cursor-pointer"
              >
                {faq3 ? (
                  <svg
                    role="button"
                    aria-label="close dropdown"
                    width="10"
                    height="6"
                    viewBox="0 0 10 6"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M1 5L5 1L9 5"
                      stroke="#4B5563"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                ) : (
                  <svg
                    width="10"
                    role="button"
                    aria-label="open dropdown"
                    height="6"
                    viewBox="0 0 10 6"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M1 1L5 5L9 1"
                      stroke="#4B5563"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                )}
              </button>
            </div>
            {faq3 && (
              <ul>
                <li>
                  <p className="text-lg leading-normal text-gray-600 mt-4 text-justify">
                    The Metanauts are a private scientific entity, capable of entering and exiting the
                    Metaverse at yearly cycles. Original a clandestine entity, the Metanauts now share their lands
                    with the Pioneers, despite their best attempts to guard their discovery.
                  </p>
                </li>
              </ul>
            )}
          </div>
          <div className="bg-white shadow rounded p-8 mt-8 cursor-pointer" onClick={() => setFaq4(!faq4)}>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-bold  uppercase text-lg leading-none text-gray-800">
                  Where is Nos Atomos?
                </h2>
              </div>
              <button
                
                data-menu
                className="focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2 ring-offset-white cursor-pointer"
              >
                {faq4 ? (
                  <svg
                    role="button"
                    aria-label="close dropdown"
                    width="10"
                    height="6"
                    viewBox="0 0 10 6"
                    fill="none"
                    
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M1 5L5 1L9 5"
                      stroke="#4B5563"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                ) : (
                  <svg
                    width="10"
                    role="button"
                    aria-label="open dropdown"
                    height="6"
                    viewBox="0 0 10 6"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M1 1L5 5L9 1"
                      stroke="#4B5563"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                )}
              </button>
            </div>
              {faq4 && (
                <ul>
                  <li>
                    <p className="text-lg leading-normal text-gray-600 mt-4 text-justify">
                      Nos Atomos is the first settled Metaversal Zone, chosen by the Metanauts due to its abundant resources and 
                      proximity to the Kármán Gate. Intially thought be uninhabited, the Pioneers have discovered evidence 
                      of prior civilizations.
                    </p>
                  </li>
                </ul>
              )}
          </div>
        </div>
      </div>
    </div>
  );
}