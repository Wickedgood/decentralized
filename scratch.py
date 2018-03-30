from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import binascii
import Crypto.Random
import Helpers
aeskey = Crypto.Random.get_random_bytes(16*2)
#print(binascii.b2a_hex(aeskey).decode("utf-8"))
webkey = AES.new(aeskey, AES.MODE_EAX)
print(binascii.b2a_hex(webkey.digest()).decode("utf-8"))
#print(binascii.b2a_hex(aeskey).decode("utf-8"))