const path = require("path");

module.exports = {
  contracts_build_directory: path.join(__dirname, "build/contracts"),

  networks: {
    development: {
      host: "127.0.0.1",     // Localhost (default)
      port: 7545,            // Ganache default port
      network_id: "*",       // Matches any network ID
    },
  },

  compilers: {
    solc: {
      version: "0.8.0",     // Solidity compiler version
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  }
};
