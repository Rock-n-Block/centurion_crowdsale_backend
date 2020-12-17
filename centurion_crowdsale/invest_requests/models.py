from django.db import models
from centurion_crowdsale.settings import IS_TESTNET, HD_ROOT_KEYS
from bip32utils import BIP32Key
from eth_keys import keys
from centurion_crowdsale.bip32_ducatus import DucatusWallet


class InvestRequest(models.Model):
    project = models.ForeignKey('projects.CenturionProject', on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    duc_address = models.CharField(max_length=50)
    btc_address = models.CharField(max_length=50)
    eth_address = models.CharField(max_length=50)

    def generate_keys(self):
        eth_btc_root_public_key = HD_ROOT_KEYS['ETH-BTC']['public']
        root_key = BIP32Key.fromExtendedKey(eth_btc_root_public_key, public=True)
        child_key = root_key.ChildKey(self.id)

        self.btc_address = child_key.Address()
        self.eth_address = keys.PublicKey(child_key.K.to_string()).to_checksum_address().lower()

        duc_root_public_key = HD_ROOT_KEYS['DUC']['public']
        duc_root_key = DucatusWallet.deserialize(duc_root_public_key)
        self.duc_address = duc_root_key.get_child(self.id, is_prime=False).to_address()

        self.save()
