import Config
import binascii
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

###find public key through password and private key only
# key = RSA.import_key(adam.private_key, passphrase=secret_code)
# print(key.publickey().exportKey())

#Create the users and keys
xyfz = Config.xyfz
xyfz.createkeys()
adam = Config.adam
adam.createkeys()


#adam connects to xyfz
xyfz.createwebkey()
xyfz.writewebkey()
#prepare the data to be sent
data_src = xyfz.webkey

file_out = open("encrypted_data.bin", "wb")

recipient_key_src = RSA.import_key(adam.public_key)
session_key_src = get_random_bytes(16)

# Encrypt the session key with the public RSA key
cipher_rsa_src = PKCS1_OAEP.new(recipient_key_src)
file_out.write(cipher_rsa_src.encrypt(session_key_src))

# Encrypt the data with the AES session key
cipher_aes_src = AES.new(session_key_src, AES.MODE_EAX)
ciphertext_src, tag_src = cipher_aes_src.encrypt_and_digest(bytes(data_src,"utf-8"))
[file_out.write(x) for x in (cipher_aes_src.nonce, tag_src, ciphertext_src)]
file_out.close()
