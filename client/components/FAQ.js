import React, { useState } from "react";
import Head from "next/head";
export default function MyApp() {

  const [faq1, setFaq1] = useState(false);
  const [faq2, setFaq2] = useState(false);
  const [faq3, setFaq3] = useState(false);
  const [faq4, setFaq4] = useState(false);
  const [faq5, setFaq5] = useState(false);

  return (
    <div id="faq">
      <div className=" flex flex-col items-center justify-center sm:px-0 px-6 z-20 pb-32 bg-faq md:pt-5 sm:pt-5 ">
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
                  WL?
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
                  Our whitelist is now closed. 
                  <br></br>
                  <br></br>
                  The Pioneer Role was limited to new Discord Members who joined between November 30th 2021 and January 25th 2022.
                  All Pioneers are eligible to sign up for our Whitelist and reserve ONE (1) CRYPTID from our Whitelist Supply.
                  We appreciate our early supporters and aim to make this project&apos;s release accessible, low-stress, and distributed. 
      
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
                  WEN MINT?
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
                    Whitelist Sale: June 13th 2022, 10:00 AM PST / 1:00 PM EST<br></br><br></br>
                    *Public Sale: June 16th 2022, 4:00 PM PST / 7:00 PM EST <br></br><br></br>
                    Max Mint Per Wallet: 2 CRYPTIDS (EX. 1 WL, 1 Public Mint) <br></br><br></br>
                    <b>*Any unused whitelist mints will become available for the public sale.</b>

                    {/* <br></br>
                    <br></br>
                    The Whitelist Sale will run for 24 hours beginning 
                    Friday, March 25th 2022, 8:00 AM PST/11:00 AM EST. 
                    <br></br>
                    <br></br>The Public sale will beginning
                    Saturday March 26th 2022, 1:00 PM PST/4:00 PM EST. */}
                  </p>
                </li>
              </ul>
            )}
          </div>
          
          <div className="bg-white shadow rounded p-8 mt-8 cursor-pointer" onClick={() => setFaq4(!faq4)}>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-bold  uppercase text-lg leading-none text-gray-800">
                  SUPPLY?
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
                    Collection Size: 7,777<br></br>
                    Whitelist Supply: 7,000<br></br>
                    Team Supply: 777<br></br>
                    <br></br>
                    Mint Price: FREE (Or choose your own price) 
                    <br></br>Any contribiton to our project is greatly appreciated.
                  </p>
                </li>
              </ul>
            )}
          </div>

          <div className="bg-white shadow rounded p-8 mt-8 cursor-pointer" onClick={() => setFaq5(!faq5)}>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-bold  uppercase text-lg leading-none text-gray-800">
                  MARKETPLACE?
                </h2>
              </div>
              <button

                data-menu
                className="focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2 ring-offset-white cursor-pointer"
              >
                {faq5 ? (
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
            {faq5 && (
              <ul>
                <li>
                  <p className="text-lg leading-normal text-gray-600 mt-4 text-justify">
                    Trove by Treasure
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