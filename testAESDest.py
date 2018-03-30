from Crypto.Cipher import AES
import Helpers
'''
AES
'''
file_in = open("encrypted.bin", "rb")
nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
key = Helpers.genkey("this is my password dude")
# let's assume that the key is somehow available again
cipher = AES.new(key, AES.MODE_EAX, nonce)
try:
    data = cipher.decrypt_and_verify(ciphertext, tag)
    print(data.decode("utf-8"))
except ValueError:
    print("Data has been corrupted, or bad password")
