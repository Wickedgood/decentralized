from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import Config
destinationuser = Config.adam
file_in = open("encrypted_data.bin", "rb")
passcode = "This is not xyfz password"
private_key = RSA.import_key(destinationuser.readprivatekey(passcode), passcode)

enc_session_key, nonce, tag, ciphertext = \
    [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

# Decrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)

# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt_and_verify(ciphertext, tag)
destinationuser.assignwebkey(data)

Config.xyfz.readprivatekey("This is my password")
Config.xyfz.loadwebkey()
message = "Hello there!"
message = Config.xyfz.encryptdatatosend(message)
print(Config.adam.unencryptdatasent(message))
