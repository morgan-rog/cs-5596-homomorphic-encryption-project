# %%
# Imports
from operator import index
import time
import random
import numpy as np
from Pyfhel import Pyfhel

def import_data():
    smashed_data = np.load("smashed_data.npy")
    return smashed_data

def generate_random_index():
    index1 = random.randrange(0, 8)
    index2 = random.randrange(0, 64)
    index3 = random.randrange(0, 28)

    return (index1, index2, index3)

def get_random_array(the_data):
    index_tuple = generate_random_index()
    return the_data[index_tuple[0]][index_tuple[1]][index_tuple[2]]


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

data = import_data()
print("data shape: ", data.shape)

random_array = get_random_array(data)
print(random_array)
print(len(random_array))

# %%
# TO DO:
# access and encrypt 25% of the arrays in smashed_data
# ---> encrypt 3584 random arrays
# keep track of their location
