
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate a new RSA key pair
key = RSA.generate(2048)

# Get the public key
public_key = key.publickey().export_key()

# Get the private key
private_key = key.export_key()

# Encrypt the string "love" using the public key
cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
encrypted_message = cipher_rsa.encrypt(b"love")

# Decrypt the encrypted message using the private key
cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
decrypted_message = cipher_rsa.decrypt(encrypted_message)

# Print the original string, encrypted message, and decrypted message
print("Original string:", "love")
print("Encrypted message:", encrypted_message)
print("Decrypted message:", decrypted_message.decode())

