from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import binascii
import Crypto.Random
import Helpers
import inspect
import logging
import Config

path = Config.path


class User:
    # Users public key
    public_key = None
    # Users private key
    private_key = None
    # Users name
    name = None
    # Temporary holding location for user's passcode
    passcode = None
    # The bytes for the webkey
    webkey = None
    # aes key creates from web key
    aeskey = None

    def __init__(self, name, passcode):
        func = inspect.currentframe().f_back.f_code
        self.name = name
        self.passcode = passcode
        logging.debug("Creating User {}".format(self.name))

    def __str__(self):
        return "{} - Pub {},Priv {},web {}".format(self.name, self.public_key, self.private_key, self.webkey)

    def createkeys(self):
        func = inspect.currentframe().f_back.f_code
        logging.debug("Creating keys for {}".format(self.name))
        key = RSA.generate(2048)
        passcode = self.passcode
        self.private_key = key.exportKey('PEM', passphrase=passcode, pkcs=8, protection="scryptAndAES128-CBC")
        self.public_key = key.publickey().exportKey('PEM')
        public_out = open(path + self.name + "public.pem", "wb")
        public_out.write(self.public_key)
        self.writeprivatekey()
        self.passcode = None

    def writeprivatekey(self):
        func = inspect.currentframe().f_back.f_code
        logging.debug("Writing keys for {} - {}".format(self.name, self.private_key))
        aeskey = Helpers.genkey(self.passcode)
        cipher = AES.new(aeskey, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(self.private_key)
        file_out = open(path + self.name + "encryptedprivatekey.bin", "wb")
        [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
        file_out.close()

    def readprivatekey(self, passcode):
        func = inspect.currentframe().f_back.f_code
        file_in = open(path + self.name + "encryptedprivatekey.bin", "rb")
        nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
        key = Helpers.genkey(passcode)
        # let's assume that the key is somehow available again
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        try:
            data = cipher.decrypt_and_verify(ciphertext, tag)
            self.private_key = data
            logging.debug("Reading keys for {} - {}".format(self.name, self.private_key))
            return data
        except ValueError:
            logging.debug("Error Reading keys ")
            return None

    def createwebkey(self):
        func = inspect.currentframe().f_back.f_code
        logging.debug("Creating web key for {}".format(self.name))
        self.webkey = Crypto.Random.get_random_bytes(16 * 2)

    def writewebkey(self):
        func = inspect.currentframe().f_back.f_code
        logging.debug("{} Writing web key as {}".format(self.name,self.webkey))
        webkey_out = open(path + "webkey.bin", "wb")
        webkey_out.write(self.webkey)

    def loadwebkey(self):
        func = inspect.currentframe().f_back.f_code
        webkey_in = open(path + "webkey.bin", "rb")
        self.webkey = webkey_in.read()
        logging.debug("{} Loading web key as {}".format(self.name, self.webkey))

    def assignwebkey(self, key):
        func = inspect.currentframe().f_back.f_code
        self.webkey = key
        logging.debug("{} Assigning web key as {}".format( self.name,self.webkey))

    def createaeskeyfromwebkey(self):
        self.aeskey = AES.new(self.webkey, AES.MODE_EAX)

    def encryptdatatosend(self, data):
        func = inspect.currentframe().f_back.f_code
        logging.debug("Encrypting data {} by {}".format(data, self.name))
        ciphertext, tag = self.aeskey.encrypt_and_digest(bytes(data, "utf-8"))
        logging.debug("nonce {} tag {} cipher {}".format(self.aeskey.nonce, tag, ciphertext))
        logging.debug("aeskey {}".format(self.aeskey))
        return (self.aeskey.nonce, tag, ciphertext)

    def unencryptdatasent(self, data):
        func = inspect.currentframe().f_back.f_code
        logging.debug("Decrypting data {} by {}".format(data, self.name))
        nonce, tag, ciphertext = data
        logging.debug("nonce {} tag {} cipher {}".format(nonce, tag, ciphertext))

        # let's assume that the key is somehow available again
        cipher = AES.new(self.aeskey, AES.MODE_EAX, nonce)
        message = cipher.decrypt_and_verify(ciphertext, tag)
        logging.debug("decrypted data is {}".format(data.decode("utf-8")))
        return message
