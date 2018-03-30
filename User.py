from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import Helpers
class User:
    #Users public key
    public_key = None
    #Users private key
    private_key = None
    #Users name
    name = None
    #Temporary holding location for user's passcode
    passcode = None
    #The AES key for the web
    webkey = None
    #number of connected nodes
    nodeconnections = 0

    def createkeys(self):
        key = RSA.generate(2048)
        passcode = self.passcode
        self.private_key = key.exportKey('PEM', passphrase=passcode, pkcs=8, protection="scryptAndAES128-CBC")
        self.public_key = key.publickey().exportKey('PEM')
        public_out = open(self.name + "public.pem", "wb")
        public_out.write(self.public_key)
        self.writeprivatekey()
        self.passcode = None

    def writeprivatekey(self):
        aeskey = Helpers.genkey(self.passcode)
        cipher = AES.new(aeskey, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(self.private_key)
        file_out = open(self.name+"encryptedprivatekey.bin", "wb")
        [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
        file_out.close()

    def readprivatekey(self,passcode):
        file_in = open(self.name+"encryptedprivatekey.bin", "rb")
        nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
        key = Helpers.genkey(passcode)
        # let's assume that the key is somehow available again
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        try:
            data = cipher.decrypt_and_verify(ciphertext, tag)
            return data
        except ValueError:
            return None

    def createwebkey(self):
        aeskey = get_random_bytes(16*2)
        self.webkey = AES.new(aeskey, AES.MODE_EAX).hexdigest()

    def writewebkey(self):
        webkey_out = open("webkey.bin","wb")
        webkey_out.write(bytes(self.webkey,"utf-8"))

    def loadwebkey(self):
        webkey_in = open("webkey.bin","rb")
        self.webkey = webkey_in.read().decode("utf-8")

    def assignwebkey(self,key):
        self.webkey = key

    def encryptdatatosend(self,data):
        #TODO FUCK
        ciphertext, tag = self.webkey.encrypt_and_digest(data.decode("utf-8"))
        ret = []
        for x in (self.webkey.nonce, tag, ciphertext):
            ret.append(x)
        return ret

    def unencryptdatasent(self,data):
        nonce, tag, ciphertext = [data[x] for x in (16, 16, -1)]
        key = self.webkey
        # let's assume that the key is somehow available again
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        try:
            data = cipher.decrypt_and_verify(ciphertext, tag)
            print(data.decode("utf-8"))
        except ValueError:
            print("Data has been corrupted, or bad password")
    def __init__(self, name, passcode):
        self.name = name
        self.passcode = passcode