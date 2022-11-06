# %%
##### Imports
from operator import index
import csv
import time
import random
import numpy as np
from Pyfhel import Pyfhel

#%%
##### Functions
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
    HE.contextGen(**ckks_params)  # Generate context for ckks scheme
    HE.keyGen()             # Key Generation: generates a pair of public/secret keys
    HE.rotateKeyGen()
    return HE

def import_data():
    smashed_data = np.load("smashed_data.npy")
    return smashed_data

def generate_random_index():
    '''generates a random index for smashed_data and does not generate duplicates'''
    while(True):
        index1 = random.randrange(0, 8)
        index2 = random.randrange(0, 64)
        index3 = random.randrange(0, 28)
        # print("index generated: ", (index1, index2, index3))
        # print("index tracker: ", index_tracker)
        if((index1, index2, index3) not in index_tracker):
            index_tracker.append((index1, index2, index3))
            break

    return (index1, index2, index3)

def change_array_type_float64(the_array):
    updated_array = np.array(the_array, dtype=np.float64)
    return updated_array

def get_random_array_and_location(the_data):
    '''returns tuple that contains the random data and its location'''
    index_tuple = generate_random_index()
    random_array = the_data[index_tuple[0]][index_tuple[1]][index_tuple[2]]
    updated_random_array = change_array_type_float64(random_array)
    return (updated_random_array, index_tuple)

def fill_data_and_location_to_encrypt(the_data, amount_of_data):
    data_to_encrypt = []

    for i in range(amount_of_data):
        random_array_tuple = get_random_array_and_location(the_data)
        data_to_encrypt.append(random_array_tuple)

    return data_to_encrypt

def fill_data_only_to_encrypt(random_data_with_location):
    '''takes data with location list and creates a new list with the data-to-encrypt only'''
    data_to_encrypt_list = []
    for info in random_data_with_location:
        data_to_encrypt_list.append(info[0])

    return data_to_encrypt_list

def encrypt_array(the_array):
    ptxt_array = HE.encodeFrac(the_array)
    ctxt_array = HE.encryptPtxt(ptxt_array)
    return ctxt_array

def decrypt_array(encrypted_array):
    _r = lambda x: np.round(x, decimals=5)

    decrypted_array = HE.decryptFrac(encrypted_array)
    # slice the decrypted array
    decrypted_array = decrypted_array[0:23]
    # round the decrypted array
    #decrypted_array = _r(sliced_decrypted_array)

    return decrypted_array

def encrypt_data_list(data_list):
    encrypted_data_list = []
    for array in data_list:
        encrypted_data_list.append(encrypt_array(array))
    
    return encrypted_data_list

def decrypt_data_list(data_list):
    decrypted_data_list = []
    for array in data_list:
        decrypted_array = decrypt_array(array)
        decrypted_data_list.append(decrypted_array)
    
    return decrypted_data_list

def perform_simple_operation_on_data(the_data):
    #print(the_data[0])
    for count, data in enumerate(the_data):
        the_data[count] = data * 2

    #rint(the_data[0])
    return the_data

def measure_average_deviation(non_encrypted_data, decrypted_data):
    if (len(non_encrypted_data) != len(decrypted_data)):
        raise Exception("cannot measure deviation because arrays have different lengths")
    innaccuracy_sum = 0
    for x in range(len(non_encrypted_data)):
        for y in range(len(non_encrypted_data[x])):
            if decrypted_data[x][y] < 0:
                decrypted_data[x][y] = 0
            
            innaccuracy = abs(non_encrypted_data[x][y] - decrypted_data[x][y])
            innaccuracy_sum += innaccuracy

    average_deviation = (innaccuracy_sum / len(non_encrypted_data))
    return average_deviation

def output_data(library, encrypt_time, decrypt_time, operation_time, average_deviation):
    header = ['python library', 'encrypt time', 'decrypt time', 'time to perform operations', 'average deviation']
    data = [library, encrypt_time, decrypt_time, operation_time, average_deviation]
    with open('measurements.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(data)
    

# %%
##### Global variables
index_tracker = [] # to make sure there are no duplicate indexes

HE = set_HE()
print("1. printing the HE object: ")
print(HE)

# %%
##### Main
RANDOM_DATA_AMOUNT = 1500

# import data
data = import_data()
print("imported data shape: ", data.shape)

# Get random data and its location in smashed_data
random_data_with_location = fill_data_and_location_to_encrypt(data, RANDOM_DATA_AMOUNT)
# Create a list with only the data to be encrypted
random_data_only = fill_data_only_to_encrypt(random_data_with_location)

# ENCRYPTION
encrypt_start_time = time.time()
encrypted_data = encrypt_data_list(random_data_only)
encrypt_end_time = time.time()
encrypt_time = (encrypt_end_time-encrypt_start_time) * 10**3
print("Time to encrypt: ", encrypt_time, " ms")

# OPERATIONS ON NON-ENCRYPTED DATA
operated_nonencrypted_data = perform_simple_operation_on_data(random_data_only)
print('operated non encrypted data: ', operated_nonencrypted_data[0])

# OPERATIONS ON ENCRYPTED DATA
operations_start_time = time.time()
operated_encrypted_data = perform_simple_operation_on_data(encrypted_data)
operations_end_time = time.time()
operations_time = (operations_end_time-operations_start_time) * 10**3
print("Time for operation: ", operations_time, " ms")

# DECRYPTION
decrypt_start_time = time.time()
decrypted_data = decrypt_data_list(encrypted_data)
decrypt_end_time = time.time()
decrypt_time = (decrypt_end_time-decrypt_start_time) * 10**3
print("Time to decrypt: ", decrypt_time, " ms")

# DECRYPTION ON OPERATED DATA
operated_decrypted_data = decrypt_data_list(operated_encrypted_data)
print('operated decrypted data: ', operated_decrypted_data[0])

# MEASURE AVERAGE DEVIATION
average_deviation = measure_average_deviation(operated_nonencrypted_data, operated_decrypted_data)
print('average deviation: ', average_deviation)

output_data('Pyfhel', encrypt_time, decrypt_time, operations_time, average_deviation)

# print("Random data and location list: ", random_data_with_location)
# print("--- random data and location list length: ", len(random_data_with_location))

# print(random_data_only[0:2])
# print("random data length: ", len(random_data_only[0]))

# print(encrypted_data[0:2])

# print(decrypted_data[0:2])
# print("decrypted data length: ", len(decrypted_data[0]))

# %%
# TO DO:
# access and encrypt 25% of the arrays in smashed_data
# ---> encrypt 3584 random arrays
# keep track of their location
#
#
# track time to encrypt and decrypt --- save to a file
# track time to perform operations on encrypted data --- save to file
# try multithreading
# measure data inaccuracy

