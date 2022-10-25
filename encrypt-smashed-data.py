# %%
# Imports
import numpy as np
from Pyfhel import Pyfhel

# %%
print("ARRAY INFO")
print("1. load in data from smashed_data.npy")
smashed_data = np.load("smashed_data.npy")

print("2. Printing array: \n", smashed_data)

# %%
print("3. shape of the array: ", smashed_data.shape)
# %%
print("GENERATING PYFHEL CONTEXT AND KEY SETUP")
HE = Pyfhel()
HE.contextGen(scheme='bfv', n=2**14, t_bits=20)
HE.keyGen()
print("1. printing the HE object: ")
print(HE)

# %%
print(smashed_data[0][0][0][0])
print(smashed_data[0][0][0])
print(smashed_data[0][0])

# %%
for x in smashed_data:
    for y in x:
        for z in y:
            for num in z:
                print("---------------------")
                print(num)
                encrypted_num = HE.encrypt(num)
                print(encrypted_num)
                decrypted_num = HE.decrypt(encrypted_num)
                print(decrypted_num)
                print(len(decrypted_num))
                print("---------------------")
                break
            break
        break
    break
# %%
for x in smashed_data:
    for y in x:
        for z in y:
            print("---------------------")
            print(z)
            encrypted_z = HE.encrypt(z)
            print(encrypted_z)
            decrypted_z = HE.decrypt(encrypted_z)
            print(decrypted_z)
            print(len(decrypted_z))
            print("---------------------")
            break
        break
    break

# %%
def encrypt_data(W):
    encrypted_data = [[[HE.encrypt(z) for z in y] for y in x] for x in W]
    return encrypted_data

encryptedData = encrypt_data(smashed_data)
print(encryptedData.shape)
# %%
