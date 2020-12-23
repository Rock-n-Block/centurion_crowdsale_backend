from django.db import models
from web3 import Web3, HTTPProvider
from centurion_crowdsale.settings import DUCX_NETWORK, GAS_LIMIT
from centurion_crowdsale.ducx_tokens.abi import DRC20_TOKEN_ABI

w3 = Web3(HTTPProvider(DUCX_NETWORK['endpoint']))


class DucxToken(models.Model):
    contract_address = models.CharField(max_length=100)
    decimals = models.IntegerField()
    symbol = models.CharField(max_length=10)
    deploy_block = models.BigIntegerField()

    def transfer(self, address, amount):
        tx_params = {
            'nonce': w3.eth.getTransactionCount(DUCX_NETWORK['address'], 'pending'),
            'gasPrice': w3.eth.gasPrice,
            'gas': GAS_LIMIT,
        }
        initial_tx = self.contract.functions.transfer(Web3.toChecksumAddress(address), amount).buildTransaction(tx_params)
        signed_tx = w3.eth.account.signTransaction(initial_tx, DUCX_NETWORK['private'])
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_hex = tx_hash.hex()
        return tx_hex

    def holders(self):
        event = self.contract.events.Transfer()
        event_filter = event.createFilter(fromBlock=self.deploy_block,
                                          toBlock=w3.eth.getBlock('latest')['number'])
        events = event_filter.get_all_entries()
        addresses = set()
        for event in events:
            addresses.add(event['args']['from'])
            addresses.add(event['args']['to'])
        addresses.remove('0x0000000000000000000000000000000000000000')
        addresses.remove(DUCX_NETWORK['address'])
        return addresses

    def balances(self):
        balances = {}
        for address in self.holders():
            balance = self.contract.functions.balanceOf(address).call()
            if balance != 0:
                balances[address] = balance
        return balances

    @property
    def contract(self):
        return w3.eth.contract(address=self.contract_address, abi=DRC20_TOKEN_ABI)