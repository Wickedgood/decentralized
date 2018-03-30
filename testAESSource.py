from Crypto.Cipher import AES
import Helpers
'''
AES
'''


data = "This is some text"
data = bytes(data,"utf-8")
password = "this is my password dude"
aeskey = Helpers.genkey(password)

cipher = AES.new(aeskey, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)

file_out = open("encrypted.bin", "wb")
[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
file_out.close()
