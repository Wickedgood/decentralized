from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import Helpers

data = "This is some text"
data = bytes(data,"utf-8")

aeskey = get_random_bytes(16)

cipher = AES.new(aeskey, AES.MODE_EAX)


ciphertext, tag = cipher.encrypt_and_digest(data)

#file_out = open("encrypted.bin", "wb")
#[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
trip  = (cipher.nonce, tag, ciphertext)
#file_out.close()

#file_in = open("encrypted.bin", "rb")
#nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
noncez, tagz, ciphertextz = trip
keyz = Helpers.genkey("this is my password dude")
# let's assume that the key is somehow available again
cipherz = AES.new(aeskey, AES.MODE_EAX, noncez)
try:
    newdata = cipherz.decrypt_and_verify(ciphertextz, tagz)
    print(newdata.decode("utf-8"))
except ValueError:
    print("Data has been corrupted, or bad password")
