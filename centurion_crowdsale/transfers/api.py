from web3 import HTTPProvider, Web3
from centurion_crowdsale.settings import DUCX_NETWORK, GAS_LIMIT, GAS_PRICE

w3 = Web3(HTTPProvider(DUCX_NETWORK['endpoint']))


def transfer_ducx(address, amount):
    tx_params = {
        'gas': GAS_LIMIT,
        'nonce': w3.eth.getTransactionCount(DUCX_NETWORK['address'], 'pending'),
        'gasPrice': GAS_PRICE,
        'to': w3.toChecksumAddress(address),
        'value': amount
    }
    signed_tx = w3.eth.account.signTransaction(tx_params, DUCX_NETWORK['private'])
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_hex = tx_hash.hex()
    return tx_hex
