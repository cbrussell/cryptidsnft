const { ethers } = require("ethers");
const web3 = new InfuraProvider("rinkeby", process.env.WEB3_INFURA_PROJECT_ID)

const contract = require('../')