# %%
# Imports
from operator import index
import time
import random
import numpy as np
from Pyfhel import Pyfhel

def set_HE():
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
    return HE

def import_data():
    smashed_data = np.load("smashed_data.npy")
    return smashed_data

def generate_random_index():
    index1 = random.randrange(0, 8)
    index2 = random.randrange(0, 64)
    index3 = random.randrange(0, 28)

    return (index1, index2, index3)

def change_array_type_float64(the_array):
    updated_array = np.array(the_array, dtype=np.float64)
    return updated_array

def get_random_array(the_data):
    '''returns tuple that contains the random data and its location'''
    index_tuple = generate_random_index()
    random_array = the_data[index_tuple[0]][index_tuple[1]][index_tuple[2]]
    updated_random_array = change_array_type_float64(random_array)
    return (updated_random_array, index_tuple)

def fill_data_and_location_to_encrypt(the_data, amount_of_data):
    data_to_encrypt = []

    for i in range(amount_of_data):
        random_array_tuple = get_random_array(the_data)
        data_to_encrypt.append(random_array_tuple)

    return data_to_encrypt

def fill_data_only_to_encrypt(data_with_location_list):
    '''takes data with location list and creates a new list with the data-to-encrypt only'''
    data_to_encrypt_list = []
    for info in data_with_location_list:
        data_to_encrypt_list.append(info[0])

    return data_to_encrypt_list

#%%
HE = set_HE()
print("1. printing the HE object: ")
print(HE)


data = import_data()
print("data shape: ", data.shape)

random_data_with_location = fill_data_and_location_to_encrypt(data, 30)


# %%
# TO DO:
# access and encrypt 25% of the arrays in smashed_data
# ---> encrypt 3584 random arrays
# keep track of their location
