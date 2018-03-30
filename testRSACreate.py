import Config
import binascii
import User
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import logging
logging.debug("BEING RSACREATE")
###find public key through password and private key only
# key = RSA.import_key(adam.private_key, passphrase=secret_code)
# print(key.publickey().exportKey())

#Create the users and keys

xyfz = User.User("xyfz", "This is my password")
adam = User.User("adam", "This is not xyfz password")
xyfz.createkeys()
adam.createkeys()


#adam connects to xyfz
xyfz.createwebkey()
xyfz.writewebkey()
#prepare the data to be sent
data_src = xyfz.webkey

file_out = open(Config.path+"encrypted_data.bin", "wb")
##BEGIN RSA ENCRYPTION
session_key_src = get_random_bytes(16)
# Encrypt the session key with the public RSA key
cipher_rsa_src = PKCS1_OAEP.new(RSA.import_key(adam.public_key))
file_out.write(cipher_rsa_src.encrypt(session_key_src))

# Encrypt the data with the AES session key
cipher_aes_src = AES.new(session_key_src, AES.MODE_EAX)
ciphertext_src, tag_src = cipher_aes_src.encrypt_and_digest(data_src)
[file_out.write(x) for x in (cipher_aes_src.nonce, tag_src, ciphertext_src)]
file_out.close()
##END RSA ENCRYPTION
logging.debug("END RSACREATE")
