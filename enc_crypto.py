import cryptography
from cryptography.fernet import Fernet

from datetime import datetime
import os 

key = Fernet.generate_key() # Store this key or get if you already have it
f = Fernet(key)

inputfile = "284.zip"
encfile = "284.encrypted"
outputfile = "d-284.zip"

#Encryption#######
s = datetime.now()

with open(inputfile, 'rb') as f:
    data = f.read()

fernet = Fernet(key)
encrypted = fernet.encrypt(data)

with open(encfile, 'wb') as f:
    f.write(encrypted)

e = datetime.now()
t = e - s
print('Encryption time : '+ str(t))


print(encfile)

#decryption######
s = datetime.now()

with open(encfile, 'rb') as f:
    data = f.read()

fernet = Fernet(key)
encrypted = fernet.decrypt(data)

with open(outputfile, 'wb') as f:
    f.write(encrypted)

e = datetime.now()
t = e - s
print('decryption time : '+ str(t))

