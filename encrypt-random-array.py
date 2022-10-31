# %%
# Imports
import time
import numpy as np
from Pyfhel import Pyfhel

# %%
print("GENERATING PYFHEL CONTEXT AND KEY SETUP")
HE = Pyfhel()           # Creating empty Pyfhel object
ckks_params = {
    'scheme': 'CKKS',   # can also be 'ckks'
    'n': 2**15,         # Polynomial modulus degree. For CKKS, n/2 values can be
                        #  encoded in a single ciphertext.
                        #  Typ. 2^D for D in [10, 16]
    'scale': 2**30,     # All the encodings will use it for float->fixed point
                        #  conversion: x_fix = round(x_float * scale)
                        #  You can use this as default scale or use a different
                        #  scale on each operation (set in HE.encryptFrac)
    'qi_sizes': [60, 30, 30, 30, 60] # Number of bits of each prime in the chain.
                        # Intermediate values should be  close to log2(scale)
                        # for each operation, to have small rounding errors.
}
HE.contextGen(**ckks_params)  # Generate context for bfv scheme
HE.keyGen()             # Key Generation: generates a pair of public/secret keys
HE.rotateKeyGen()
print("1. printing the HE object: ")
print(HE)
#%%
def create_random_array(array_size):
    the_array = np.random.uniform(0.0, 5.0, size=array_size)
    return the_array

def encrypt_array(the_array):
    ptxt_array = HE.encodeFrac(the_array)
    ctxt_array = HE.encryptPtxt(ptxt_array)
    return ctxt_array

def decrypt_array(encrypted_array):
    decrypted_array = HE.decryptFrac(encrypted_array)
    return decrypted_array

#%%
data = create_random_array(1000)
print(data)
print(len(data))

start_time = time.time()
encrypted_data = encrypt_array(data)
end_time = time.time()
print("time to encrypt: ", (end_time-start_time) * 10**3, "ms")

start_time = time.time()
decrypted_array = decrypt_array(encrypted_data)
end_time = time.time()
print("time to decrypt: ", (end_time-start_time) * 10**3, "ms")