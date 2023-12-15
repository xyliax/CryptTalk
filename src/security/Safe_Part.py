import rsa
import random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import getPrime
# RSA Part
def generate_key_pair():
    # Generate a pair of public key and private key
    public_key, private_key = rsa.newkeys(2048)
    return public_key, private_key

def encrypt_with_public_key(public_key, message):
    # Encrypt the message using the public key
    encrypted_message = rsa.encrypt(message.encode(), public_key)
    return encrypted_message

def decrypt_with_private_key(private_key, encrypted_message):
    # Decrypt the encrypted message using the private key
    decrypted_message = rsa.decrypt(encrypted_message, private_key)
    return decrypted_message.decode()

# SHA 256 Hash Part
def sha256_hash(data):
    return  SHA256.new(data.encode()).digest()

# AES Part

def encrypt_with_aes(plaintext, password):
    # Generate a 256-bit key from the password using SHA-256, it is suitable for the AES algorithm
    key = sha256_hash(password) 
    # Create an AES cipher object with the key
    cipher = AES.new(key, AES.MODE_ECB) 
    padded_plaintext = pad(plaintext.encode(), AES.block_size) # AES.block_size = 128
    # Encrypt the plaintext and return the ciphertext
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext

def decrypt_with_aes(ciphertext, password):
    # Generate a 256-bit key from the password using SHA-256, it is suitable for the AES algorithm
    key = sha256_hash(password)
    # Create an AES cipher object with the key
    cipher = AES.new(key, AES.MODE_ECB)
    # Decrypt the ciphertext and return the plaintext
    plaintext = unpad(cipher.decrypt(ciphertext),AES.block_size).decode()
    return plaintext

# Diffie-Hellman Part
def fast_modular_exponentiation(a, b, p):  # A little trick to get the a^b mod c
    result = 1
    a = a % p
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % p
        a = (a * a) % p
        b = b // 2
    return result

def generate_prime_number(): # a function which is used to generate a prime number
    prime_bits = 2048  # the number of bits of a prime number
    prime = getPrime(prime_bits)
    return prime

def calculate_public_key(prime, generator, private_key):
    """
    Calculate the public key using the Diffie-Hellman algorithm.
    the generator is a primitive root of the prime.
    the private_key here is the X_a/ X_b in the textbook
    """
    return(fast_modular_exponentiation(generator, private_key, prime))

def calculate_shared_secret(prime, public_key, private_key):
    """
    Calculate the shared secret using the Diffie-Hellman algorithm.
    the public_key here is the Y_a/ Y_b in the textbook
    the private_key here is the X_a/ X_b in the textbook
    """
    return(fast_modular_exponentiation(public_key, private_key, prime))

def getgenerator_SK(prime) : # a function which is used to generate a generator and a private key
    return random.randomint(2,prime-1)

def get_numbers(string): # a function which can get all of the number in a string, and output an integer
  numbers = re.findall(r'\d+', string)
  concatenated_number = int(''.join(numbers))
  return concatenated_number

