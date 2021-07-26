from web3 import Web3, WebsocketProvider, HTTPProvider

w3 = Web3(HTTPProvider("HTTP://127.0.0.1:7545"))
contract = {
    'address': "0x560a99A9E230371E7177504169db120842c48800",
    'abi': '''[
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "name": "_pub_key",
          "type": "address"
        },
        {
          "indexed": false,
          "name": "_name",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "name": "_timestamp",
          "type": "uint256"
        }
      ],
      "name": "Account_Creation",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "name": "_pub_key",
          "type": "address"
        },
        {
          "indexed": false,
          "name": "_pk",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "name": "_name",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "name": "_timestamp",
          "type": "uint256"
        }
      ],
      "name": "Product_Registration_Update",
      "type": "event"
    },
    {
      "inputs": [],
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "gas": 1169400,
      "inputs": [
        {
          "name": "_password",
          "type": "bytes32"
        }
      ],
      "name": "get_secret_key",
      "outputs": [
        {
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1432177,
      "inputs": [
        {
          "name": "_name",
          "type": "bytes32"
        },
        {
          "name": "_secret_key",
          "type": "string"
        },
        {
          "name": "_password",
          "type": "bytes32"
        }
      ],
      "name": "register_company_account",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "gas": 1331,
      "inputs": [],
      "name": "get_company_account_name",
      "outputs": [
        {
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1938063,
      "inputs": [
        {
          "name": "_pk",
          "type": "bytes32"
        },
        {
          "name": "_name",
          "type": "bytes32"
        },
        {
          "name": "_category",
          "type": "bytes32"
        },
        {
          "name": "_release_year",
          "type": "uint256"
        },
        {
          "name": "_price",
          "type": "uint256"
        },
        {
          "name": "_country",
          "type": "bytes32"
        },
        {
          "name": "_description",
          "type": "string"
        },
        {
          "name": "_serial_lists",
          "type": "uint256[10]"
        }
      ],
      "name": "register_product",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "gas": 763754314,
      "inputs": [
        {
          "name": "_target_product_pk",
          "type": "bytes32"
        },
        {
          "name": "_name",
          "type": "bytes32"
        },
        {
          "name": "_category",
          "type": "bytes32"
        },
        {
          "name": "_price",
          "type": "uint256"
        },
        {
          "name": "_description",
          "type": "string"
        }
      ],
      "name": "update_product",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "gas": 2695118,
      "inputs": [
        {
          "name": "_arr",
          "type": "bytes32[1000]"
        }
      ],
      "name": "get_list_of_products",
      "outputs": [
        {
          "name": "",
          "type": "bytes32[1000]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 28022747,
      "inputs": [
        {
          "name": "_pk",
          "type": "bytes32"
        }
      ],
      "name": "get_product_prop",
      "outputs": [
        {
          "name": "",
          "type": "bytes32[2]"
        },
        {
          "name": "",
          "type": "uint256"
        },
        {
          "name": "",
          "type": "uint256"
        },
        {
          "name": "",
          "type": "bytes32"
        },
        {
          "name": "",
          "type": "string"
        },
        {
          "name": "",
          "type": "uint256[10]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1162180,
      "inputs": [],
      "name": "get_first_product",
      "outputs": [
        {
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1163400,
      "inputs": [],
      "name": "get_last_product",
      "outputs": [
        {
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1358,
      "inputs": [],
      "name": "contract_owner",
      "outputs": [
        {
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]'''
}

pid = w3.eth.contract(address=contract['address'], abi=contract['abi'])
