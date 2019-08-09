import pyAesCrypt
from os import stat, remove
from datetime import datetime
# encryption/decryption buffer size
bufferSize = 64 * 1024
password = "pqwe23wd"
# encryption of file data.txt


inputfile = "284.zip"
encfile = "284.encrypted"
outputfile = "d-284.zip"


s = datetime.now()
with open(inputfile, "rb") as fIn:
	with open(encfile, "wb") as fOut:
		pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
e = datetime.now()
t = e - s
print('Encryption time : '+ str(t))

# get encrypted file size
encFileSize = stat(encfile).st_size
print(encFileSize) #prints file size# decryption of file data.aes

s = datetime.now()
with open(encfile, "rb") as fIn:
	with open(outputfile, "wb") as fOut:
		try:
			# decrypt file stream
			pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)
		except ValueError:
			# remove output file on error
			remove(encfile)

e = datetime.now()
t = e - s
print('decryption time : '+ str(t))