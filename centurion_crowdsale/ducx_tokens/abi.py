DRC20_TOKEN_ABI = '''
[
   {
      "name":"CONTINUE_MINTING",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"getFreezing",
      "type":"function",
      "inputs":[
         {
            "name":"_addr",
            "type":"address"
         },
         {
            "name":"_index",
            "type":"uint256"
         }
      ],
      "outputs":[
         {
            "name":"_release",
            "type":"uint64"
         },
         {
            "name":"_balance",
            "type":"uint256"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"mintingFinished",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"approve",
      "type":"function",
      "inputs":[
         {
            "name":"_spender",
            "type":"address"
         },
         {
            "name":"_value",
            "type":"uint256"
         }
      ],
      "outputs":[
         {
            "name":"",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"mintAndFreeze",
      "type":"function",
      "inputs":[
         {
            "name":"_to",
            "type":"address"
         },
         {
            "name":"_amount",
            "type":"uint256"
         },
         {
            "name":"_until",
            "type":"uint64"
         }
      ],
      "outputs":[
         {
            "name":"",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"initialized",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"actualBalanceOf",
      "type":"function",
      "inputs":[
         {
            "name":"_owner",
            "type":"address"
         }
      ],
      "outputs":[
         {
            "name":"balance",
            "type":"uint256"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"totalSupply",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"uint256"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"TOKEN_NAME",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"string"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"TOKEN_SYMBOL",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"string"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"freezeTo",
      "type":"function",
      "inputs":[
         {
            "name":"_to",
            "type":"address"
         },
         {
            "name":"_amount",
            "type":"uint256"
         },
         {
            "name":"_until",
            "type":"uint64"
         }
      ],
      "outputs":[

      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"unpause",
      "type":"function",
      "inputs":[

      ],
      "outputs":[

      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"mint",
      "type":"function",
      "inputs":[
         {
            "name":"_to",
            "type":"address"
         },
         {
            "name":"_amount",
            "type":"uint256"
         }
      ],
      "outputs":[
         {
            "name":"",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"burn",
      "type":"function",
      "inputs":[
         {
            "name":"_value",
            "type":"uint256"
         }
      ],
      "outputs":[

      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"TOKEN_DECIMAL_MULTIPLIER",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"uint256"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"TOKEN_DECIMALS",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"uint256"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"releaseAll",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"tokens",
            "type":"uint256"
         }
      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"paused",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"decreaseApproval",
      "type":"function",
      "inputs":[
         {
            "name":"_spender",
            "type":"address"
         },
         {
            "name":"_subtractedValue",
            "type":"uint256"
         }
      ],
      "outputs":[
         {
            "name":"",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"releaseOnce",
      "type":"function",
      "inputs":[

      ],
      "outputs":[

      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"balanceOf",
      "type":"function",
      "inputs":[
         {
            "name":"_owner",
            "type":"address"
         }
      ],
      "outputs":[
         {
            "name":"balance",
            "type":"uint256"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"renounceOwnership",
      "type":"function",
      "inputs":[

      ],
      "outputs":[

      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"TARGET_USER",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"address"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"finishMinting",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"pause",
      "type":"function",
      "inputs":[

      ],
      "outputs":[

      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"owner",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"address"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"PAUSED",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"freezingCount",
      "type":"function",
      "inputs":[
         {
            "name":"_addr",
            "type":"address"
         }
      ],
      "outputs":[
         {
            "name":"count",
            "type":"uint256"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"TOKEN_DECIMALS_UINT8",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"",
            "type":"uint8"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"increaseApproval",
      "type":"function",
      "inputs":[
         {
            "name":"_spender",
            "type":"address"
         },
         {
            "name":"_addedValue",
            "type":"uint256"
         }
      ],
      "outputs":[
         {
            "name":"",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"freezingBalanceOf",
      "type":"function",
      "inputs":[
         {
            "name":"_owner",
            "type":"address"
         }
      ],
      "outputs":[
         {
            "name":"balance",
            "type":"uint256"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"allowance",
      "type":"function",
      "inputs":[
         {
            "name":"_owner",
            "type":"address"
         },
         {
            "name":"_spender",
            "type":"address"
         }
      ],
      "outputs":[
         {
            "name":"",
            "type":"uint256"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"view"
   },
   {
      "name":"transferOwnership",
      "type":"function",
      "inputs":[
         {
            "name":"_newOwner",
            "type":"address"
         }
      ],
      "outputs":[

      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "type":"constructor",
      "inputs":[

      ],
      "payable":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"Initialized",
      "type":"event",
      "inputs":[

      ],
      "anonymous":false
   },
   {
      "name":"Pause",
      "type":"event",
      "inputs":[

      ],
      "anonymous":false
   },
   {
      "name":"Unpause",
      "type":"event",
      "inputs":[

      ],
      "anonymous":false
   },
   {
      "name":"Burn",
      "type":"event",
      "inputs":[
         {
            "name":"burner",
            "type":"address",
            "indexed":true
         },
         {
            "name":"value",
            "type":"uint256",
            "indexed":false
         }
      ],
      "anonymous":false
   },
   {
      "name":"Mint",
      "type":"event",
      "inputs":[
         {
            "name":"to",
            "type":"address",
            "indexed":true
         },
         {
            "name":"amount",
            "type":"uint256",
            "indexed":false
         }
      ],
      "anonymous":false
   },
   {
      "name":"MintFinished",
      "type":"event",
      "inputs":[

      ],
      "anonymous":false
   },
   {
      "name":"OwnershipRenounced",
      "type":"event",
      "inputs":[
         {
            "name":"previousOwner",
            "type":"address",
            "indexed":true
         }
      ],
      "anonymous":false
   },
   {
      "name":"OwnershipTransferred",
      "type":"event",
      "inputs":[
         {
            "name":"previousOwner",
            "type":"address",
            "indexed":true
         },
         {
            "name":"newOwner",
            "type":"address",
            "indexed":true
         }
      ],
      "anonymous":false
   },
   {
      "name":"Freezed",
      "type":"event",
      "inputs":[
         {
            "name":"to",
            "type":"address",
            "indexed":true
         },
         {
            "name":"release",
            "type":"uint64",
            "indexed":false
         },
         {
            "name":"amount",
            "type":"uint256",
            "indexed":false
         }
      ],
      "anonymous":false
   },
   {
      "name":"Released",
      "type":"event",
      "inputs":[
         {
            "name":"owner",
            "type":"address",
            "indexed":true
         },
         {
            "name":"amount",
            "type":"uint256",
            "indexed":false
         }
      ],
      "anonymous":false
   },
   {
      "name":"Approval",
      "type":"event",
      "inputs":[
         {
            "name":"owner",
            "type":"address",
            "indexed":true
         },
         {
            "name":"spender",
            "type":"address",
            "indexed":true
         },
         {
            "name":"value",
            "type":"uint256",
            "indexed":false
         }
      ],
      "anonymous":false
   },
   {
      "name":"Transfer",
      "type":"event",
      "inputs":[
         {
            "name":"from",
            "type":"address",
            "indexed":true
         },
         {
            "name":"to",
            "type":"address",
            "indexed":true
         },
         {
            "name":"value",
            "type":"uint256",
            "indexed":false
         }
      ],
      "anonymous":false
   },
   {
      "name":"name",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"_name",
            "type":"string"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"pure"
   },
   {
      "name":"symbol",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"_symbol",
            "type":"string"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"pure"
   },
   {
      "name":"decimals",
      "type":"function",
      "inputs":[

      ],
      "outputs":[
         {
            "name":"_decimals",
            "type":"uint8"
         }
      ],
      "payable":false,
      "constant":true,
      "stateMutability":"pure"
   },
   {
      "name":"transferFrom",
      "type":"function",
      "inputs":[
         {
            "name":"_from",
            "type":"address"
         },
         {
            "name":"_to",
            "type":"address"
         },
         {
            "name":"_value",
            "type":"uint256"
         }
      ],
      "outputs":[
         {
            "name":"_success",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   },
   {
      "name":"transfer",
      "type":"function",
      "inputs":[
         {
            "name":"_to",
            "type":"address"
         },
         {
            "name":"_value",
            "type":"uint256"
         }
      ],
      "outputs":[
         {
            "name":"_success",
            "type":"bool"
         }
      ],
      "payable":false,
      "constant":false,
      "stateMutability":"nonpayable"
   }
]
'''