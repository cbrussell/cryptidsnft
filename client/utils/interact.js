import { Contract, utils} from "ethers";
import { useCall, useContractCall } from "@usedapp/core"
import cryptidTokenNFT from "../../contract/build/deployments/42161/0x5A39174e7F2B669a51Ec179eF49b3eca7ddB96AB.json";
import { ContractAddress } from '../data/contract';

const { abi: cryptidTokenABI } = cryptidTokenNFT;

const cryptidTokenNFTInterface = new utils.Interface(cryptidTokenABI);

const nftContract = new Contract(ContractAddress, cryptidTokenNFTInterface)

export function GetTotalSaleSupply() {
  const { value, error } =  useCall({ 
    contract: nftContract, 
    method: "totalSaleSupply", 
  }) ?? {};
  if (error) {
    console.error(error.message)
    return undefined;
  } else {
    return value?.[0]
  }
}

export function GetTotalSupply() {
  const { value, error } =  useCall({ 
    contract: nftContract, 
    method: "totalSupply", 
    args: [],
  }) ?? {};
  if (error) {
    console.error(error.message)
    return undefined;
  } else {
    return value?.[0]
  }
}

export function Verify(account, proof) {
  const { value, error } =  useCall({ 
    contract: nftContract, 
    method: "verify", 
    args: [account, proof],
  }) ?? {};
  if (error) {
    console.error(error.message)
    return undefined;
  } else {
    return value?.[0]
  }
}

export function CheckIfClaimed(account) {
  const { value, error } =  useCall({ 
    contract: nftContract, 
    method: "claimed", 
    args: [account],
  }) ?? {};
  if (error) {
    console.error(error.message)
    return undefined;
  } else {
    return  value?.[0].toNumber()
  }
}

export function GetStage() {
  const { value, error } =  useCall({ 
    contract: nftContract, 
    method: "stage", 
    args: [],
  }) ?? {};
  if (error) {
    console.error(error.message)
    return undefined;
  } else {
    return value?.[0]
  }
}

export function GetOwner() {
  const { value, error } =  useCall({ 
    contract: nftContract, 
    method: "owner", 
    args: [],
  }) ?? {};
  if (error) {
    console.error(error.message)
    return undefined;
  } else {
    return value?.[0]
  }
}