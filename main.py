import argparse
from sys import argv
import os
import random
import json
import string
import time
from getpass import getpass
import urllib2
from urlparse import urlparse
import pyperclip

from PIL import Image
import stepic

import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


class Stegnographer:

    def __init__(self, key, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.key = key
        self.cipher = AESCipher(self.key)
        
        def get_md5_hash(k):
            m = hashlib.md5()
            m.update(k)
            md5_hash = m.hexdigest()
            return md5_hash

        try:
            already_encoded = stepic.decode(self.image)
            # print("already_encoded: {}".format(already_encoded))
            self.md5_hash = already_encoded[:32]
            # print("self.md5_hash: {}".format(self.md5_hash))
            self.passwords_dict = json.loads(already_encoded[32:])
        except ValueError:
            key_again = raw_input("Initializing the image, please re-enter your master password: ")
            if self.key != key_again:
                print("\n!!!! The passwords do not match !!!!\n")
                exit(0)
            self.md5_hash = get_md5_hash(self.key)
            self.passwords_dict = {}

        if self.md5_hash != get_md5_hash(self.key):
            print("\n!!!! Wrong password !!!!\n")
            exit(0)



    def save_to_image(self):
        try:
            data = self.md5_hash+json.dumps(self.passwords_dict)
        except ValueError:
            print('password_dict not a valid json')
            exit(0)
        stepic.encode_inplace(self.image, data)
        assert stepic.decode(self.image) == data

        self.image.save(self.image_path)
        print("\nChanges saved in the image!\n")

    def get_websites(self):
        return list(self.passwords_dict.keys())

    def get_usernames(self, website):
        accounts = self.passwords_dict.get(website, {})
        return list(accounts.keys())

    def get_password(self, website, username):
        password = self.passwords_dict.get(website, {}).get(username, None)
        password = self.cipher.decrypt(password)
        return password

    def new_account(self, website, username, password):
        self.passwords_dict.setdefault(website, {})

        if username in self.get_usernames(website):
            print('Error: Account already exists!')
            exit(0)

        encrypted_password = self.cipher.encrypt(password)
        self.passwords_dict[website][username] = encrypted_password

        self.save_to_image()

        pyperclip.copy(password)
        raw_input("The Password has been copied to clipboard, and will remain till you press enter / kill password manager")

    def change_password(self, website, username, password):

        if username not in self.get_usernames(website, {}):
            print('Error: Account not found!')
            exit(0)


        password = self.cipher.encrypt(password)
        self.passwords_dict[website][username] = password

        self.save_to_image()

    def delete_account(self, website, username, password):

        try:
            del self.passwords_dict[website][username]
        except KeyError:
            print ("Error: Account not found!")
            exit(0)

        self.save_to_image()

    def clear_all_data(self):
        data = '_'
        stepic.encode_inplace(self.image, data)
        self.image.save(self.image_path)


def generate_password(allowed, compulsory=[], passwordLength=15):
    """
    args:
        allowed: Set of allowed characters.
        compulsory: list of Sets: Need to choose at least one from each Set.
        passwordLength: length of the password required.

    returns:
        a random password satisfying the constraints
    """
    num_chars_possible = len(allowed)
    password = ''
    
    for x in range(passwordLength):
        password += random.choice(tuple(allowed))
    

    positions_for_compulsory = random.sample(range(passwordLength), len(compulsory))
    for compulsorySet in compulsory:
        # print(compulsorySet)
        chosen = random.choice(tuple(compulsorySet))
        # print(chosen)
        position = positions_for_compulsory.pop()
        password = password[:position] + chosen + password[position+1:]

    return password


def chooser(list_of_items, prompt):
    items = []
    for i, item in enumerate(list_of_items):
        items.append(item)
        print("{}\t{}".format(i+1, item))
    chosen_id = raw_input(prompt)
    try:
        chosen_id = int(chosen_id) - 1
        item = items[chosen_id]
    except (IndexError, ValueError):
        print("Invalid Choice!")
        exit(0)
    return item


def yes_or_no(prompt):
    while True:
        print(prompt)
        reply = raw_input().lower()
        if len(reply) > 0:
            reply = reply[0]
            if reply == 'y' or reply == 'n':
                return reply
        print("Invalid input: Enter y or n")


def handle_retr(stegnographer):

    website = chooser(stegnographer.get_websites(), "Choose Website: ")
    username = chooser(stegnographer.get_usernames(website), "Choose username: ")

    password = stegnographer.get_password(website, username)
    pyperclip.copy(password)
    raw_input("The Password has been copied to clipboard, and will remain till you press enter / kill password manager")
    


def get_website_name(url):
    if '//' not in url:
        url = 'http://{}'.format(url)
    
    try:
        req = urllib2.Request(url=url)
        resp = urllib2.urlopen(req, timeout=3)
    except urllib2.URLError:
        print("\nHandshake Operation timed out! Make sure you enter correct url.\n")
        exit(0)
    
    redirected_url = resp.geturl()
    website_name = urlparse(redirected_url).netloc
    return website_name


def handle_restrictions():
    is_at_least_one_of_both_cases_compulsory = yes_or_no("Is at least one character of upper case and one of lower case compulsory (y/n)?: ")
    is_at_least_one_numeral_compulsory = yes_or_no("Is at least one numeral compulsory (y/n)?: ")
    is_at_least_one_special_char_compulsory = yes_or_no("Is at least one special character compulsory (y/n)?: ")
    
    while True:
        maximum_length_of_password = raw_input("Maximum length of password (15 if not specified): ")
        try:
            maximum_length_of_password = int(maximum_length_of_password)
            if maximum_length_of_password >= 5:
                break
        except ValueError:
            print("Please enter a valid number from 5 to 15")

    maximum_length_of_password = min(15, maximum_length_of_password)

    allowed = set([ch for ch in string.printable if ch.isalnum()])
    compulsory = []
    if is_at_least_one_special_char_compulsory == 'y':
        compulsory.append(set(string.punctuation))
    if is_at_least_one_of_both_cases_compulsory == 'y':
        compulsory.append(set(string.ascii_lowercase))
        compulsory.append(set(string.ascii_uppercase))
    if is_at_least_one_numeral_compulsory == 'y':
        compulsory.append(set(string.digits))
    

    return allowed, compulsory, maximum_length_of_password


def handle_add_account(stegnographer):

    url = raw_input("Enter the website url: ")
    website_name = get_website_name(url)

    print("\nThe normalized website name is : {}".format(website_name))

    username = raw_input("\nEnter a username: ")

    reply = yes_or_no("Any password restrictions? (y or n)")

    if reply == 'y':
        allowed, compulsory, password_length = handle_restrictions()
    else:
        allowed = string.printable
        compulsory = []
        password_length = 15
    
    password = generate_password(allowed, compulsory, password_length)

    stegnographer.new_account(website_name, username, password)


def handle_change_password(stegnographer):
    #TODO: We need to make sure that no one who does not know the master password can change the password
    # Hence, implement the feature to also store SHA256 hash of the master password in the image file and compare them
    website = chooser(stegnographer.get_websites(), "Choose Website: ")
    username = chooser(stegnographer.get_usernames(website), "Choose username: ")
    pass



if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False, description=('PasswordManager'))
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Specify the Image and Master Password')
    parser.add_argument('--image', '-i', help='Stegnographed Image File - JPG, GIF, PNG, BMP')
    parser.add_argument('--option', '-o', help='retr: Retrieve Password, add: Add Password, change: Change Password')
    
    
    argv = argv[1:]
    args = parser.parse_args(argv)

    print("\n\t\t\tHello from PasswordManager \n")

    masterpassword = getpass('Enter the master password: ') 

    stegnographer = Stegnographer(masterpassword, args.image)

    if args.option == 'retr':
        handle_retr(stegnographer)
    elif args.option == 'add':
        handle_add_account(stegnographer)
    elif args.option == 'change':
        handle_change_password(stegnographer)
    elif args.option == 'clear_all_data':
        stegnographer.clear_all_data()
    else:
        print("Provide a valid option!")
        exit(0)

