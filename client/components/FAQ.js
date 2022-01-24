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
                  Will there be a whitelist?
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
                    All Pioneers will have the opportunity to claim their FIRST WAVE badge (whitelist).
                    Once the available allotment of Pioneers roles are distributed, whitelist will only be 
                    possible through contests, community events, and lore/art contributions.  
      
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
                  Which network will CRYPTIDS be available and when?
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
                    Arbitrum, May 2022.
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
                className="focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2 ring-offset-white"
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
                    The Metanauts are the four Team Members developing CRYPTIDS. 
                    Nosolo (art), Crussell (dev), Sentella (social media), and Grove (lore). 
                    
                  </p>
                </li>
              </ul>
            )}
          </div>
          <div className="bg-white shadow rounded p-8 mt-8 cursor-pointer" onClick={() => setFaq4(!faq4)}>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-bold  uppercase text-lg leading-none text-gray-800">
                  What is the total supply and mint cost?
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
                    8,888 total supply, 0.08 ETH
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