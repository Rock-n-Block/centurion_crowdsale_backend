import requests
from decimal import Decimal
from pywallet.utils import Wallet, HDPrivateKey, HDKey
from pywallet.utils.bip32 import *
from pywallet.wallet import generate_mnemonic, create_address
from centurion_crowdsale.consts import DECIMALS
from centurion_crowdsale.payments.models import Payment
from centurion_crowdsale.settings_local import HD_ROOT_KEYS
from mywill_scanner.settings.settings_local import NETWORKS
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from http.client import RemoteDisconnected


class DucatusMainNet(object):
    NAME = "Ducatus Main Net"
    COIN = "DUC"
    SCRIPT_ADDRESS = 0x06  # int(0x06) = 6
    PUBKEY_ADDRESS = 0x31  # int(0x31) = 48
    SECRET_KEY = PUBKEY_ADDRESS + 128  # = int(0xb1) = 177
    EXT_PUBLIC_KEY = 0x0488B21E
    EXT_SECRET_KEY = 0x0488ADE4
    BIP32_PATH = "m/44'/0'/0'/"


class DucatusWallet(Wallet):

    @classmethod
    def get_network(self, network):
        return DucatusMainNet

    @classmethod
    def from_master_secret(cls, seed, network='ducatus'):
        network = DucatusWallet.get_network(network)
        seed = ensure_bytes(seed)
        # Given a seed S of at least 128 bits, but 256 is advised
        # Calculate I = HMAC-SHA512(key="Bitcoin seed", msg=S)
        I = hmac.new(b"Bitcoin seed", msg=seed, digestmod=sha512).digest()
        # Split I into two 32-byte sequences, IL and IR.
        I_L, I_R = I[:32], I[32:]
        # Use IL as master secret key, and IR as master chain code.
        return cls(private_exponent=long_or_int(hexlify(I_L), 16),
                   chain_code=long_or_int(hexlify(I_R), 16),
                   network=network)

    @classmethod  # @memoize
    def deserialize(cls, key, network="ducatus"):
        network = DucatusWallet.get_network(network)

        if len(key) in [78, (78 + 32)]:
            # we have a byte array, so pass
            pass
        else:
            key = ensure_bytes(key)
            if len(key) in [78 * 2, (78 + 32) * 2]:
                # we have a hexlified non-base58 key, continue!
                key = unhexlify(key)
            elif len(key) == 111:
                # We have a base58 encoded string
                key = base58.b58decode_check(key)
        # Now that we double checkd the values, convert back to bytes because
        # they're easier to slice
        version, depth, parent_fingerprint, child, chain_code, key_data = (
            key[:4], key[4], key[5:9], key[9:13], key[13:45], key[45:])

        version_long = long_or_int(hexlify(version), 16)
        exponent = None
        pubkey = None
        point_type = key_data[0]
        if not isinstance(point_type, six.integer_types):
            point_type = ord(point_type)
        if point_type == 0:
            # Private key
            if version_long != network.EXT_SECRET_KEY:
                raise incompatible_network_exception_factory(
                    network.NAME, network.EXT_SECRET_KEY,
                    version)
            exponent = key_data[1:]
        elif point_type in [2, 3, 4]:
            # Compressed public coordinates
            if version_long != network.EXT_PUBLIC_KEY:
                raise incompatible_network_exception_factory(
                    network.NAME, network.EXT_PUBLIC_KEY,
                    version)
            pubkey = PublicKey.from_hex_key(key_data, network=network)
            # Even though this was generated from a compressed pubkey, we
            # want to store it as an uncompressed pubkey
            pubkey.compressed = False
        else:
            raise ValueError("Invalid key_data prefix, got %s" % point_type)

        def l(byte_seq):
            if byte_seq is None:
                return byte_seq
            elif isinstance(byte_seq, six.integer_types):
                return byte_seq
            return long_or_int(hexlify(byte_seq), 16)

        return cls(depth=l(depth),
                   parent_fingerprint=l(parent_fingerprint),
                   child_number=l(child),
                   chain_code=l(chain_code),
                   private_exponent=l(exponent),
                   public_key=pubkey,
                   network=network)


def get_network():
    return DucatusMainNet


def create_wallet(seed=None, children=1):
    if seed is None:
        seed = generate_mnemonic()

    net = get_network()
    wallet = {
        "coin": net.COIN,
        "seed": seed,
        "private_key": "",
        "public_key": "",
        "xprivate_key": "",
        "xpublic_key": "",
        "address": "",
        "wif": "",
        "children": []
    }

    my_wallet = DucatusWallet.from_master_secret(
        network='ducatus', seed=seed)

    print(my_wallet)

    # account level
    wallet["private_key"] = my_wallet.private_key.get_key().decode()
    wallet["public_key"] = my_wallet.public_key.get_key().decode()
    wallet["xprivate_key"] = my_wallet.serialize_b58(private=True)
    wallet["xpublic_key"] = my_wallet.serialize_b58(private=False)
    wallet["address"] = my_wallet.to_address()
    wallet["wif"] = my_wallet.export_to_wif()

    prime_child_wallet = my_wallet.get_child(0, is_prime=True)
    wallet["xpublic_key_prime"] = prime_child_wallet.serialize_b58(private=False)

    # prime children
    for child in range(children):
        child_wallet = my_wallet.get_child(child, is_prime=False, as_private=False)
        wallet["children"].append({
            "xpublic_key": child_wallet.serialize_b58(private=False),
            "address": child_wallet.to_address(),
            "path": "m/" + str(child),
            "bip32_path": net.BIP32_PATH + str(child_wallet.child_number),
        })

    return wallet


class DucatuscoreInterfaceException(Exception):
    pass


class DucatusAPI:
    def __init__(self):
        self.set_base_url()

    def set_base_url(self):
        self.base_url = f'https://ducapi.rocknblock.io/api/DUC/mainnet'

    def get_address_response(self, address):
        endpoint_url = f'{self.base_url}/address/{address}'
        res = requests.get(endpoint_url)
        if not res.ok:
            return [], False
        else:
            valid_json = len(res.json()) > 0
            if not valid_json:
                print('Address have no transactions and balance is 0', flush=True)
                return [], True

            return res.json(), True

    def get_address_unspent_all(self, address):
        inputs_of_address, response_ok = self.get_address_response(address)
        if not response_ok:
            return [], 0, False

        if response_ok and len(inputs_of_address) == 0:
            return inputs_of_address, 0, True

        inputs_value = 0
        unspent_inputs = []
        for input_tx in inputs_of_address:
            if not input_tx['spentTxid']:
                unspent_inputs.append({
                    'txid': input_tx['mintTxid'],
                    'vout': input_tx['mintIndex']
                })
                inputs_value += input_tx['value']

        return unspent_inputs, inputs_value, True

    def get_address_unspent_from_tx(self, address, tx_hash):
        inputs_of_address, response_ok = self.get_address_response(address)
        if not response_ok:
            return [], 0, False

        if response_ok and len(inputs_of_address) == 0:
            return inputs_of_address, 0, True

        # find vout
        vout = None
        input_value = 0
        for input_tx in inputs_of_address:
            if not input_tx['spentTxid'] and input_tx['mintTxid'] == tx_hash:
                vout = input_tx['mintIndex']
                input_value = input_tx['value']

        if vout is None:
            return [], 0, False

        input_params = [{'txid': tx_hash, 'vout': vout}]
        return input_params, input_value, True

    def get_return_address(self, tx_hash):
        endpoint_url = f'{self.base_url}/tx/{tx_hash}/coins'
        res = requests.get(endpoint_url)
        if not res.ok:
            return '', False
        else:
            tx_info = res.json()

        inputs_of_tx = tx_info['inputs']
        if len(inputs_of_tx) == 0:
            return '', False

        first_input = inputs_of_tx[0]
        return_address = first_input['address']

        address_found = False
        if return_address:
            address_found = True

        return return_address, address_found


class DucatuscoreInterface:
    endpoint = None
    settings = None

    def __init__(self):

        self.settings = NETWORKS['DUCATUS_MAINNET']
        self.setup_endpoint()
        self.rpc = AuthServiceProxy(self.endpoint)
        self.check_connection()

    def setup_endpoint(self):
        self.endpoint = 'http://{user}:{pwd}@{host}:{port}'.format(
            user=self.settings['user'],
            pwd=self.settings['password'],
            host=self.settings['host'],
            port=self.settings['port']
        )
        return

    def check_connection(self):
        block = self.rpc.getblockcount()
        if block and block > 0:
            return True
        else:
            raise Exception('Ducatus node not connected')

    def transfer(self, address, amount):
        try:
            value = amount / DECIMALS['DUC']
            print('try sending {value} DUC to {addr}'.format(value=value, addr=address))
            self.rpc.walletpassphrase(self.settings['wallet_password'], 30)
            res = self.rpc.sendtoaddress(address, value)
            print(res)
            return res
        except JSONRPCException as e:
            err = 'DUCATUS TRANSFER ERROR: transfer for {amount} DUC for {addr} failed' \
                .format(amount=amount, addr=address)
            print(err, flush=True)
            print(e, flush=True)
            raise DucatuscoreInterfaceException(err)

    def validate_address(self, address):
        for attempt in range(10):
            print('attempt', attempt, flush=True)
            try:
                rpc_response = self.rpc.validateaddress(address)
            except RemoteDisconnected as e:
                print(e, flush=True)
                rpc_response = False
            if not isinstance(rpc_response, bool):
                print(rpc_response, flush=True)
                break
        else:
            raise Exception(
                'cannot validate address with 10 attempts')

        return rpc_response['isvalid']

    def get_unspent(self, tx_hash, count):
        return self.rpc.gettxout(tx_hash, count)

    def get_fee(self):
        return self.rpc.getinfo()['relayfee']

    def get_unspent_input(self, tx_hash, payment_address):
        last_response = {}
        count = 0
        while isinstance(last_response, dict):
            rpc_response = self.get_unspent(tx_hash, count)
            last_response = rpc_response

            input_addresses = rpc_response['scriptPubKey']['addresses']
            if payment_address in input_addresses:
                return rpc_response, count

            count += 1

    def internal_transfer(self, tx_list, address_from, address_to, amount, private_key):
        print('start raw tx build', flush=True)
        print('tx_list', tx_list, 'from', address_from, 'to', address_to, 'amount', amount, flush=True)
        try:
            input_params = []
            for payment_hash in tx_list:
                unspent_input, input_vout_count = self.get_unspent_input(payment_hash, address_from)
                print('unspent input', unspent_input, flush=True)

                input_params.append({
                    'txid': payment_hash,
                    'vout': input_vout_count
                })

            transaction_fee = self.get_fee() * DECIMALS['DUC']
            send_amount = (Decimal(amount) - transaction_fee) / DECIMALS['DUC']

            print('input_params', input_params, flush=True)
            output_params = {address_to: send_amount}
            print('output_params', output_params, flush=True)

            tx = self.rpc.createrawtransaction(input_params, output_params)
            print('raw tx', tx, flush=True)

            signed = self.rpc.signrawtransaction(tx, None, [private_key])
            print('signed tx', signed, flush=True)

            tx_hash = self.rpc.sendrawtransaction(signed['hex'])
            print('tx', tx_hash, flush=True)

            return tx_hash

        except JSONRPCException as e:
            print('DUCATUS TRANSFER ERROR: transfer for {amount} DUC for {addr} failed'
                  .format(amount=amount, addr=address_to), flush=True
                  )
            print(e, flush=True)
            raise DucatuscoreInterfaceException(e)


def return_ducatus(payment_hash, amount):
    p = Payment.objects.get(tx_hash=payment_hash)

    duc_root_key = DucatusWallet.deserialize(HD_ROOT_KEYS['DUC']['private'])
    duc_child = duc_root_key.get_child(p.invest_request.id, is_prime=False)
    child_private = duc_child.export_to_wif().decode()

    duc_api = DucatusAPI()
    duc_rpc = DucatuscoreInterface()

    raw_fee = duc_rpc.get_fee()
    fee = raw_fee * DECIMALS['DUC']
    raw_send_amount = amount - fee
    send_amount = Decimal(raw_send_amount) / DECIMALS['DUC']

    input_params, input_value, response_ok = duc_api.get_address_unspent_from_tx(p.invest_request.duc_address,
                                                                                 p.tx_hash)
    if not response_ok:
        print('fail to fetch input param', flush=True)
        return

    print('input_params', input_params, flush=True)

    return_address, response_ok = duc_api.get_return_address(p.tx_hash)
    if not response_ok:
        print('fail to fetch return address', flush=True)
        return

    if return_address == p.invest_request.duc_address:
        print('returning address is equal to receive address, cancelling return to avoid loop')
        return

    output_params = {return_address: send_amount}
    if amount < input_value:
        output_params[p.invest_request.duc_address] = (input_value - fee - raw_send_amount) / DECIMALS['DUC']

    print('output_params', output_params, flush=True)

    tx = duc_rpc.rpc.createrawtransaction(input_params, output_params)
    print('raw tx', tx, flush=True)

    signed = duc_rpc.rpc.signrawtransaction(tx, None, [child_private])
    print('signed tx', signed, flush=True)

    tx_hash = duc_rpc.rpc.sendrawtransaction(signed['hex'])
    print('tx', tx_hash, flush=True)
    print('receive address was:', p.invest_request.duc_address, flush=True)