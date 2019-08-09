
import cryptography
from cryptography.fernet import Fernet
# key = b'1408' # Use one of the methods to get a key (it must be the same when decrypting)

key = Fernet.generate_key()


input_file = '/root/pjlogin/fus-3/fus/tree.jpeg'
output_file = '/root/pjlogin/fus-3/fus/tree.encrypted'

with open(input_file, 'rb') as f:
    data = f.read()

fernet = Fernet(key)
encrypted = fernet.encrypt(data)

with open(output_file, 'wb') as f:
    f.write(encrypted)

# You can delete input_file if you want



new_file = '/root/pjlogin/fus-3/fus/newtree.jpeg'
key_file = '/root/pjlogin/fus-3/fus/secrets.txt'

with open(output_file, 'rb') as f:
    data = f.read()

fernet = Fernet(key)
encrypted = fernet.decrypt(data)

with open(new_file, 'wb') as f:
    f.write(encrypted)

# You can delete input_file if you want

with open(key_file,'wb') as f:
    f.write(key)

