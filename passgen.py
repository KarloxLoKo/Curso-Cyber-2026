import secrets
import string

letters = string.ascii_letters
digits = string.digits
#special_chars = string.punctuation

alphabet = letters + digits # + special_chars

pwd_length = 6 # any number from 6 up

# pwd = ""
# for i in range(pwd_length):
	# pwd += "".join(secrets.choice(alphabet))
	
# print(pwd)

while True:
	pwd = ""
	for i in range(pwd_length):
		pwd += "".join(secrets.choice(alphabet))
		
	if sum(char in digits for char in pwd)>=2:
			break
print(pwd)
