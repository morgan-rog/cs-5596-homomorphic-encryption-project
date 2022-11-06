# %%
#### IMPORTS
import tenseal as ts
from operator import index
import csv
import time
import random
import numpy as np

#%%
##### FUNCTIONS
def import_data():
    smashed_data = np.load("smashed_data.npy")
    return smashed_data

def change_array_type_float64(the_array):
    updated_array = np.array(the_array, dtype=np.float64)
    return updated_array

def set_TS():
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.generate_galois_keys()
    context.global_scale = 2**40
    return ts, context

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
    enc_v1 = ts.ckks_vector(context, the_array)
    return enc_v1

def decrypt_array(encrypted_array):
    #_r = lambda x: np.round(x, decimals=5)
    decrypted_array = encrypted_array.decrypt()
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

#%%
#### GLOBAL
index_tracker = [] # to make sure there are no duplicate indexes
ts, context = set_TS()

##### MAIN
RANDOM_DATA_AMOUNT = 1500

# import data
data = import_data()
print("imported data shape: ", data.shape)

# Get random data and its location in smashed_data
random_data_with_location = fill_data_and_location_to_encrypt(data, RANDOM_DATA_AMOUNT)
# Create a list with only the data to be encrypted
random_data_only = fill_data_only_to_encrypt(random_data_with_location)
#print('random data: ', random_data_only[0])
######################################################################################
# ENCRYPTION
encrypt_start_time = time.time()
encrypted_data = encrypt_data_list(random_data_only)
encrypt_end_time = time.time()
encrypt_time = (encrypt_end_time-encrypt_start_time) * 10**3
#print('encrypted data: ', encrypted_data[0])
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
#print('decrypted data: ', decrypted_data[0])
print("Time to decrypt: ", decrypt_time, " ms")

# DECRYPTION ON OPERATED DATA
operated_decrypted_data = decrypt_data_list(operated_encrypted_data)
print('operated decrypted data: ', operated_decrypted_data[0])

# MEASURE AVERAGE DEVIATION
average_deviation = measure_average_deviation(operated_nonencrypted_data, operated_decrypted_data)
print('average deviation: ', average_deviation)

# %%
