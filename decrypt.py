# aries program
# made by @srando
# version 1

from math import gcd
from Crypto.Util import number
# ^^^this kinda feels like cheating as the library offers
#	RSA encryption out of box
import fileinput
import os.path
import time
import sys

# TO DO:
# 1.) Fix file location input
# 2.) Upload to github
# 3.) Implement prime number thing
# 4.) create master file of file locations and implement
# 5.) Test and publish to github
# 6.) Create writeup?

# ENCRYPTION

# THIS function finds the 'e' value
def findE(phi, n):
	# NEXT: I must add something to make sure e is above
	#	 a certain threshold for more security
	# e number must be 1 < e < phi(n)
	#	so in our case the # must be (1, 6)
	e_range = range(2, phi)
	e = 0

	for num in e_range:
		# e number must be coprime with n & phi(n)
		#	(so 14 and 6)
		# could shorten to gcd(num, n) + gcd(num, phi) == 1
		#	because gcd will always be 1 at minimum (aka no 0 + 2)
		if gcd(num, n) == 1 and gcd(num, phi) == 1:
			e = num
			print("%d found!!!" % e)
			break;

	# e is released as part of the public key[0]
	return e

# THIS function finds the 'd' value
def findD(e, phi):
	# HAVE TO LEARN MORE ABOUT MULTIPLICATIVE INVERSE
	decryption_number = pow(e, -1, phi)
	return decryption_number

# THIS function turns a letter into an (int) ASCII code
def letterToNum(message):
	return ord(message)

# THIS function turns an (int) ASCII code into
def numToLetter(num):
	return chr(num)

# num_letter parameter means letterToNum must be used
def encrypt(num_letter, e, n):
	cipher_txt = pow(num_letter, e) % n
	#print(cipher_txt)
	return cipher_txt

def decrypt(cipher_txt, d, n):
	plain_txt = pow(int(cipher_txt), d) % n
	return plain_txt

# Current flow is encryptMessage(message)
#	-> encryptMessage goes through each letter in message and
#		uses letterToNum to convert before encrypting number
#		in encrypt(num_letter) function

# message parameter is the plaintext message
def encryptMessage(message, e, n):
	# This function goes letter by letter converting letter
	#	to number and then encrypting the number using the
	#	encrypt function and after adding to message list
	encrypted_message = []

	for i in range(0, len(message)):
		# print(message[i])
		temp_num = letterToNum(message[i])
		encrypted_message.append(str(encrypt(temp_num, e, n)))

	# NEED TO WORK ON ABSTRACTION OF FUNCTIONS (ADD TO CIPHER TEXT THINGIE)
	return encrypted_message
	
def decryptMessage(message, d, n):
	decrypted_message = []
	for i in range(0, len(message)):
		# print(message[i])
		decrypted_message.append(numToLetter(decrypt(message[i], d, n)))

	return decrypted_message

# MENU / FILE MANIPULATION

options = [">1 create new file", ">2 view/add/subtract from file [password needed]", ">3 exit the program"]

# Query with input everytime
#file_locaton = "C:/blah blah"

def findPrime(n):
	print("I should be finished!")
	return 5 # fix

def begin():
	aries = ("\n   _____ __________.______________ _________\n"
			"  /  _  \\\\______   \\   \\_   _____//   _____/\n"
			" /  /_\\  \\|       _/   ||    __)_ \\_____  \\ \n"
			"/    |    \\    |   \\   ||        \\/        \\\n"
			"\\____|__  /____|_  /___/_______  /_______  /\n"
			"        \\/       \\/            \\/        \\/")

	intro_blurb = ("\033[1;32;10m Welcome to \033[1;34;10m%s\033[1;32;10m\n"
		"This tool uses the RSA encryption scheme to encrypt\n"
		"  small messages such as numbers, notes, passwords, and links\n"
		"All encrypted data is saved into a physical file in the event\n"
		"  the program crashes or if the data is needed on a separate device\n"
		"\033[1;34;10mmade by @srando \033[1;36;10m(✿◠‿◠)\n"
		"\033[1;35;10mloading menu now...\n" % (aries)) # "aries"
	print(intro_blurb)

def readMasterFile(file_location):
	print("this should be fixed!")
	return False # fix

# THIS function sets up a new file (using format found in program notes)
def newFile():
	# NEED TO ADD A FIRST TIME PASSWORD SETUP WHERE HASH IS
	#	"BURNED" INTO FILE

	# Getting new file's name
	print("name of file?")
	filename = input()

	while True:
		# Getting new file's location
		#print("where to create new file (/file/path/)?")
		#file_location = input()

		file_location = "/Users/sethrossman/Downloads/"
		while os.path.isdir(file_location) != True:
			print("not a valid input")
			print("where to create new file (/file/path/)?")
			file_location = input()


		# Creating the file
		#	try/except may be unneeded
		try:
			new_file = open((file_location + filename), "w")
			break;
		except FileNotFoundError:
			print("ERROR: file not created !")

	# POSSIBLY MAKE FILE AFTER ALL ELSE (SECURITY?)

	# Checking if file exists
	if (os.path.isfile(file_location + filename) != True):
		print("ERROR: file not created")
	else:
		print("FILE CREATED AT %s" % (file_location + filename))

	#print("THIS IS WHERE WE DECIDE p & q")
	#^^^ GENERATE AND DISPLAY NUMBERS HERE
	# NOTE: figure out what p&q represent exactly
	#p = int(input())
	#q = int(input())
	# NOTE ^^^ I NEED TO MAKE INPUT checker aka conditionals
	#	(using typeof) (or isChar?()//isInt()?) and a while loop
	print("how many bits would you like the n prime # to be?")
	print("(recommended size is 1024)")
	bit_length = input()
	while bit_length.isnumeric() != True:
		print("not a valid input")
		print("how many bits would you like the p&q numbers to be?")
		print("(recommended size is 1024)")
		n = int(input())
	#p = number.getPrime(int(bit_length))
	#q = number.getPrime(int(bit_length))
	#p = 61
	#q = 53
	p = findPrime(n) # finish function
	w = findPrime(n) # finish function

	n = p * q # product of p * q // public key[1]
	phi = (p - 1) * (q - 1) # phi(n)

	# This may be unnecessary but freeing p & q
	del p
	del q

	# Encryption number
	e = findE(phi, n)
	print("Encryption number found > %d" % e)

	# Decryption number
	# SHOULD I FIND "d" LATER?
	d = findD(e, phi)
	print("Decryption number found > \033[1;31;10m%d" % d)

	# WRITE TO FILE PUBLIC KEY AT TOP IN FORMAT SPECIFIED IN NOTES
	# The public key is [e, n]
	new_file.write("[%d, %d]\n" % (e, n))
	print("\033[1;32;10mPublic Key is [%d, %d]" % (e, n))
	new_file.close() # closing file

	print("key variables:", end=" ")
	print([n, e, phi])

	# I need to return the file as well
	return [n, e, phi, (file_location + filename)]

# THIS function reads in the public key at top of file and rest of file
def processFile(file_location):
	# This is where the program reads first line of document for encryption scheme
	# ^^^SCRAPPED IDEA DUE TO ONE ENCRYTPION SCHEME^^^

	# We need to add some sort of symbol or character code to
	#	show when cohesive blocks stop and start

	file = open(file_location, "r")

	# Parsing
	public_key = file.readline()
	public_key = public_key[1:len(public_key) - 2]
	# ^^^ -2 because of /n newline
	public_key = public_key.split(", ")

	if (len(public_key) == 2):
		if (public_key[0].isnumeric() and public_key[1].isnumeric()):
			print("\033[1;34;10mKEYS CHECK OUT... \033[1;32;10mFILE FORMAT CORRECT")
	else:
		print("\033[1;31;10mFILE IN IMPROPER FORMAT\033[1;32;10m")
		return "FAILED"
		# DO SOMETHING HERE DO SOMETHING HERE

	# NOTE WE WILL HAVE TO CHANGE THIS TO NOT CAUSE ERRORS
	# WHEN FILE IS WRONG FORMAT
	public_key_e = public_key[0]
	public_key_n = public_key[1]
	print("\033[1;32;10m%s\033[1;36;10m%s" % ("Encryption number: ", public_key_e))
	print("\033[1;32;10m%s\033[1;33;10m%s" % ("Modulo number: ", public_key_n))

	line = file.readline()
	i = 0

	print("\033[1;32;10mfile encrypted\033[1;31;10m")
	while line:
		#print(str(i) + "| " + line)
		print(line)
		# ^^^ Potentially add line numbers like below
		line = file.readline()
		i = i + 1
	# Setting white color
	print("\033[1;32;10m", end="")
	file.close()
	return [int(public_key_e), int(public_key_n)]

# Hashed T/F rm , hashed <- ask in loop
def viewFile(file_location, n):

	### Create global color profile variables ex."\033[1;32;10m"
	while True:
		print("\033[1;35;10mview file encrypted (e), decrypted (d), or exit (x)?")
		print("\033[1;32;10mviewing choice? >> ", end="")
		choice = input()

		if choice == "e":
			file = open(file_location, "r")
			# just print off encrypted file lines
			print_file = file_location.split("/")
			print("\033[1;32;10mprinting '\033[1;33;10m%s\033[1;32;10m' (encrypted)" % print_file[len(print_file) - 1])

			# DOUBLECHECK THIS
			line = file.readline()
			# repeated so public key part is skipped
			line = file.readline()

			# /Users/sethrossman/Downloads/pls-work-yaypls-work-yay

			# Setting white color and black background
			print("\033[1;37;10m", end="")

			i = 1 # line number
			k = 0
			while line:
				line = line.split(" ")
				print(str(i) + "| ", end="")
				for block in line:
					# adding line numbers every 25 numbers
					if k % 10 == 0 and k != 0:
						i = i + 1
						print()
						print(str(i) + "| ", end="")
						time.sleep(0.02)
					k = k + 1
					print(block, end=" ")
				line = file.readline()
				i = i + 1
			print()

			file.close()
		elif choice == "d":
			file = open(file_location, "r")
			# print the decrypted file lines
			print("\033[1;35;10mwhat is the decryption number?")
			# Setting green as color
			print("\033[1;32;10m", end="")
			d = input()
			while d.isnumeric() != True:
				print("\033[1;35;10mwhat is the decryption number? >> ", end="")
				d = input()
			print_file = file_location.split("/")
			print("\033[1;32;10mprinting file '\033[1;33;10m%s\033[1;32;10m' (decrypted)" % print_file[len(print_file) - 1])

			# skipping past the public key line of file
			line = file.readline()
			#print(line)

			file_content = file.read()
			file_content = file_content.split(" ")
			#print(file_content)

			# Deleting space list item caused by split
			if file_content[len(file_content) - 1] == "":
				file_content.pop(-1)

			#print(file_content)

			decrypted_message = decryptMessage(file_content, int(d), n)
			#print(decrypted_message)

			# Setting white color
			print("\033[1;37;10m", end="")

			i = 1 # line number
			k = 0
			print(str(i) + "| ", end="")
			for letter in decrypted_message:
				# adding line numbers every 25 numbers
				#if letter == "\n" or letter == "\r\n":
				# ^^^was not working as 
				if k % 10 == 0 and k != 0:
					time.sleep(0.01)
				if k % 45 == 0 and k != 0:
					i = i + 1
					print()
					print(str(i) + "| ", end="")
				k = k + 1
				print(letter, end="")
			print()

			# might be unneeded but...
			del d

			file.close()
		elif choice == "x":
			return
		else:
			print("not a valid input.. please try again")

def addToFile(file_location, public_key):
	print("what to add to file?")
	text_to_add = input()
	print("\033[1;35;10mconfirm (y) \033[1;32;10m'\033[1;33;10m%s\033[1;32;10m'\033[1;32;10m?" % text_to_add)
	confirmation = input()
	while (confirmation == "y") != True:
		print("\033[1;35;10mconfirm (y) \033[1;32;10m'\033[1;33;10m%s\033[1;32;10m'?" % text_to_add)
		confirmation = input()
	print("\033[1;32;10madded '\033[1;33;10m%s\033[1;32;10m' to '\033[1;33;10m%s\033[1;32;10m'" % (text_to_add, file_location))

	#print("decryption key(needed for security)?")
	# NEED TO FIX ^^^ maybe save a hash of d on file when being made
	if confirmation == "y":
		file = open(file_location, "a")
		encrypted_message = encryptMessage(text_to_add, public_key[0], public_key[1])
		complete_message = ""
		for block in encrypted_message:
			complete_message += block + " "
		file.write(complete_message)
		file.close()
	else:
		return

def subtractFromFile(file_location, public_key):
	viewFile(file_location)
	print("What text do you want to remove from the file?")
	text_to_remove = input()
	print("COMING SOON")

def quitProgram():
	print("\033[1;36;10m(づ｡◕‿‿◕｡)づ \033[1;35;10mThank you for using decrypt!")
	sys.exit("exiting now...")

def editFile():
	#print("file location (/file/path/file)?")
	#file_location = input()
	# ^^^ this line

	# NOTE FOR DEBUGGING WE HAVE COMMENTED ABOVE STATEMENT
	#file_location = "/Users/sethrossman/Downloads/pls-work-yaypls-work-yay"

	print("enter filename >> ", end="")
	filename = input()
	file_location = "/Users/sethrossman/Downloads/" + filename

	if (os.path.isfile(file_location) != True):
		print("FILE NOT FOUND")

	public_key = processFile(file_location)

	if (public_key == "FAILED"):
		print("file was not in the correct format\n"
			"\033[1;31;10mbacking out to menu now...\033[1;32;10m", end="")
		return

	while True:
		print("choose operation to make on the file...")
		print("\033[1;35;10m>1 view file (hashed or unhashed)")
		print(">2a (write) add to file")
		print(">2s (remove) subtract from file")
		print(">3 (exit) exit to main menu\033[1;32;10m")
		print("(nested) menu option? >> ", end="")
		choice = input()

		if choice == "1":
			viewFile(file_location, public_key[1])
		elif choice == "2a":
			addToFile(file_location, public_key)
		elif choice == "2s":
			subtractFromFile(file_location, public_key)
		elif choice == "3":
			print("exiting to main menu...")
			return
		else:
			print("not a valid input.. please try again")

# MAIN FUNCTION

def main():
	print("\033[1;32;10mWelcome to the \033[1;34;10maries\033[1;32;10m secure Rolodex")

	# Run a test using a simple arbitrary value to
	#	test if program is working correctly
	assert("blah" == "blah")

	# DEBUG STATEMENT
	#print(os.path.abspath(os.getcwd()))

	# NOTE: 'menu_option_selected != True' used to be there
	#	but now while True is because we want the program
	#	to be an endless loop till the user quits
	while True:
		# Displaying options
		for option in options:
			print("\033[1;35;10m" + option)
		choice = input("\033[1;32;10mmenu option? >> ")

		if choice == "":
			print("no choice selected... please try again")
		else:
			# HEREEEE
			if choice.isnumeric() == True:
				print("\033[1;32;10m'%s' selected" % (options[int(choice) - 1]))
		if choice == "1":
			#print("DEBUG >> %s SELECTED" % (options[0]))

			# GO TO SUBMENU (1) FUNCTION
			print("\033[1;32;10m") # newline
			encrypt_data = newFile()
			print() # newline

		elif choice == "2":
			#print("DEBUG >> %s SELECTED" % (options[1]))

			# GO TO SUBMENU (2) FUNCTION
			print("\033[1;32;10m", end="") # color change
			editFile()
			print() # newline

		elif choice == "3":
			#print("DEBUG >> %s SELECTED" % (options[2]))

			# GO TO SUBMENU (3) FUNCTION
			print("\033[1;32;10m") # newline
			quitProgram()
			print() # newline
		else:
			print("not a valid input.. please try again")

if __name__ == '__main__':
	begin()
	main()