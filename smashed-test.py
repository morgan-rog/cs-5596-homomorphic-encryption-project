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

# %%
print("ARRAY INFO")
smashed_data = np.load("smashed_data.npy")
print("Printing array: \n", smashed_data)
print("Shape of the array: ", smashed_data.shape)
# %%

the_data = np.array(smashed_data, dtype=np.float64)
print(the_data.shape)

# ravel_data = the_data.ravel()
# print(ravel_data)
# print(len(ravel_data))


# %%
def encrypt_data(the_data):
    encrypted_data = []
    count = 0
    try:
        for x in the_data:
            for y in x:
                for z in y:
                    count += 1
                    print("---------------------")
                    z_array = np.array(z, dtype=np.float64)
                    print(z_array)
                    ptxt_z = HE.encodeFrac(z_array)
                    ctxt_z = HE.encryptPtxt(ptxt_z)
                    encrypted_data.append(ctxt_z)
                    print(encrypted_data)
                    print("---------------------")
                    # time.sleep(1)
                    if count == 5:
                        raise StopIteration
    except StopIteration:
        pass

    return count
    # return encrypted_data

encrypted_data = encrypt_data(smashed_data)
print(encrypted_data)
# %%
data = np.array(smashed_data[0][0], dtype=np.float64)
print("data: ", data)
print(len(data))
ptxt_x = HE.encodeFrac(data)
ctxt_x = HE.encryptPtxt(ptxt_x)

r_x = HE.decryptFrac(ctxt_x)
_r = lambda x: np.round(x, decimals=5)
print("   ->\tctxt_x --(decr)--> ", _r(r_x))


# %%
for i in range(2):
    new_data = data * 2

print(new_data)

new_data = ctxt_x**2


r_x = HE.decryptFrac(ctxt_x)
#r_mult = HE.decryptFrac(ctxt_mult)
r_new_data = HE.decryptFrac(new_data)

_r = lambda x: np.round(x, decimals=5)
print("   ->\tctxt_x --(decr)--> ", _r(r_x))
#print("   ->\tctxt_mult --(decr)--> ", _r(r_mult))
print("   ->\tcnew_data --(decr)--> ", _r(r_new_data))
# %%
# make for-loop of operations (multiplication, addition)
# one on plain text and one on cipher
# time, accuracy, put in excel sheet
# multithreading