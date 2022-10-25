# %%
# Imports
from cgi import test
import numpy as np
from Pyfhel import Pyfhel

##################################################################
# %%
print("GENERATING PYFHEL CONTEXT AND KEY SETUP")
HE = Pyfhel()           # Creating empty Pyfhel object
ckks_params = {
    'scheme': 'CKKS',   # can also be 'ckks'
    'n': 2**14,         # Polynomial modulus degree. For CKKS, n/2 values can be
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

############################################################
# %%
data = np.array([0.36788154, 0.89863376, 0.88983678, 0.75110426], dtype=np.float64)
ptxt_x = HE.encodeFrac(data)
ctxt_x = HE.encryptPtxt(ptxt_x)

r_x = HE.decryptFrac(ctxt_x)
_r = lambda x: np.round(x, decimals=5)
print("   ->\tctxt_x --(decr)--> ", _r(r_x))


#################################################################
# %%
arr_x = np.array([0.1, 0.2, -0.3], dtype=np.float64)
ptxt_x = HE.encodeFrac(arr_x)
ctxt_x = HE.encryptPtxt(ptxt_x)

r_x = HE.decryptFrac(ctxt_x)
_r = lambda x: np.round(x, decimals=3)
print("   ->\tctxt_x --(decr)--> ", _r(r_x))
#################################################################
# %%
test_num = 7.7198091310427663
#test_num = 3
# %%
e_encode_num = HE.encodeFrac(test_num)
e_num = HE.encryptPtxt(e_encode_num)
print(e_num)
# %%
d_num = HE.decode(e_num)

print(d_num)
print(len(d_num))
# %%
print(type(0.7198091310427663))
#####################################################################

# %%
def encrypt_data(W):
    encrypted_data = [[HE.encrypt(num) for num in y] for y in W]
    return encrypted_data

encrypted_data = encrypt_data(new_array)
# %%
print(encrypted_data)
#print(len(encrypted_data))
# %%
def decrypt_data(W):
    decrypted_data = [[HE.decrypt(num) for num in y] for y in W]
    return decrypted_data

#%%
decrypted_data = decrypt_data(encrypted_data)
print(decrypted_data)


# %%
data = np.array([0.36788154, 0.89863376, 0.88983678, 0.75110426], dtype=np.float64)
data2 = np.array([0.45788154, 0.133333, 0.375586776, 0.98827266], dtype=np.float64)
ptxt_x = HE.encodeFrac(data)
ptxt_y = HE.encodeFrac(data2)
ctxt_x = HE.encryptPtxt(ptxt_x)
ctxt_y = HE.encryptPtxt(ptxt_y)

csum = ctxt_x + ctxt_y

# make for-loop of operations (multiplication, addition)
# one on plain text and one on cipher
# time, accuracy, put in excel sheet
# multithreading
# %%
r_x = HE.decryptFrac(ctxt_x)
csum_d = HE.decryptFrac(csum)
_r = lambda x: np.round(x, decimals=5)
print("   ->\tctxt_x --(decr)--> ", _r(r_x))

print("   ->\tcsum --(decr)--> ", _r(csum_d))


# %%
