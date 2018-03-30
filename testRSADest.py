from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import Config
import logging
import User
logging.debug("BEING RSADEST")
xyfz = User.User("xyfz", "This is my password")
adam = User.User("adam", "This is not xyfz password")
file_in = open(Config.path + "encrypted_data.bin", "rb")
passcode = "This is not xyfz password"
##BEGIN RSA DECRYPT
private_key = RSA.import_key(adam.readprivatekey(passcode), passcode)
enc_session_key, nonce, tag, ciphertext = \
    [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]
# Decrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)
# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)

data = cipher_aes.decrypt_and_verify(ciphertext, tag)
##END RSA DECRYPT

logging.debug("{}\n{}".format(xyfz,adam))
adam.assignwebkey(data)

adam.createaeskeyfromwebkey()
print(adam.aeskey.digest())
##LOAD EAS KEY
xyfz.readprivatekey("This is my password")
xyfz.loadwebkey()

xyfz.createaeskeyfromwebkey()
print(xyfz.aeskey.digest())
##SEND MESSAGE
message = "Hello there!"
message = xyfz.encryptdatatosend(message)
message = adam.unencryptdatasent(message)
logging.debug("END RSADEST")