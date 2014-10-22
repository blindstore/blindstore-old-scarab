
# coding: utf-8

# In[1]:

import math
from random import randint, randrange

from gmpy2 import mpz, digits


# In[2]:

def params(s, l):
    return mpz(s), mpz((s + 3)*l), mpz(5*(s + 3)*l // 2)


# In[3]:

# Number of records
n = 10000000
# Bits required for query
l = int(math.log(n, 2)) + 1

print('l={}'.format(l))

# Generate Keygen params
# etha - size of sk
# gamma - size of pk and ciphertext
rho, etha, gamma = params(60, l)
rho, etha, gamma


# In[4]:

# Random odd number in range
p = mpz(randrange(2**(etha-1), 2**(etha), 2))


# In[5]:

# Random odd number in range
q = mpz(randrange(1, (2**gamma)//p, 2))


# In[6]:

# Public key
x = q * p
print('pk size (bytes):', x.bit_length() // 8)


# In[8]:

# Encrypt-decrypt
good = 0
for i in range(1000):
    # Random number in range
    q1 = mpz(randint(1, 2**gamma//p))
    # Random number in range
    r = mpz(randint(-2**rho, 2**rho))
    
    # Encryption
    m = mpz(0)
    c1 = (m + 2*r + q1*p) % x
    # Decryption
    m1 = c1 % p % 2
    if m == m1:
        good += 1
    
    # Encryption
    m = mpz(1)
    c2 = (m + 2*r + q1*p) % x
    # Decryption
    m2 = c2 % p % 2
    if m == m2:
        good += 1
        
    # Homo operation
    c3 = (c1 + c2) % x
    m3 = c3 % p % 2
    if m3 == 1:
        good += 1
        
    # Homo operation
    c3 = (c1 * c2) % x
    m3 = c3 % p % 2
    if m3 == 0:
        good += 1

print ('Ciphertext size (bytes):', c1.bit_length() * l // 8)
print ('Successful enc-decs:', good, '/ 4000')
assert good == 4000


# In[9]:

len(digits(c1, 62)) * 1024 * 5

