from web3 import Web3

class Blockchain:
    def __init__(self):
        RPC_URL = "https://ethereum-sepolia.publicnode.com"
        CONTRACT_ADDRESS = " 0x778C5b10bFD70CF4628b8D7EEF20c4a060175298"

        ABI = [
            {
                "constant": False,
                "inputs": [
                    {"name": "timestamp", "type": "uint256"},
                    {"name": "user", "type": "string"},
                    {"name": "action", "type": "string"},
                    {"name": "data_hash", "type": "string"}
                ],
                "name": "addAuditLog",
                "outputs": [],
                "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]

        self.web3 = Web3(Web3.HTTPProvider(RPC_URL))
        if not self.web3.is_connected():
            raise ConnectionError("❌ Failed to connect to Ethereum node!")

        if not self.web3.is_address(CONTRACT_ADDRESS):
            raise ValueError("❌ Invalid contract address!")

        self.contract = self.web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

    def add_audit(self, timestamp, user, action, data_hash):
        print(f"Adding to blockchain: {user}, {action}, {timestamp}, {data_hash}")
