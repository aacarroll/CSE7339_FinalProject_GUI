from Crypto import Random
from Crypto.Random import random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import Blowfish
import os
from shutil import copyfile

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def generateKey(password):
    #generate randomly generated key from master password
    salt = Random.new().read(8)
    iterations = 5000
    dkLen = 32
    key = PBKDF2(password, salt, dkLen = 32, count = iterations)
    return key

def encrypt (message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encryptFile(file_name, key):
    with open(file_name, 'rb') as file:
        plaintext = file.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".enc", 'wb') as file_out:
        file_out.write(enc)
    # copyfile(file_name+".enc", "encrypted")
    # copying file, intended for testing whether encrypt/decrypt was actually working
    os.remove(file_name) # remove old plaintext file
    if ".enc" in file_name + ".enc":
        os.rename(file_name + ".enc", file_name) #rename .enc file to the original filename
        #yes I tried doing the encryption in place, it was doing weird stuff.

def encryptKey(key_file, key):
    with open(key_file, 'rb') as file:
        plaintext = file.read()
    enc = encrypt_BlowFish(plaintext, key)
    with open(key_file + ".enc", 'wb') as file_out:
        file_out.write(enc)
    os.remove(key_file) # remove old plaintext file
    if ".enc" in key_file + ".enc":
        os.rename(key_file + ".enc", key_file) #rename .enc file to the original filename
        #yes I tried doing the encryption in place, it was doing weird stuff.

def encrypt_BlowFish(plaintext, key):
    cipher = Blowfish.new(key)
    return cipher.encrypt(plaintext)

def decrypt_Blowfish(ciphertext, key):
    cipher = Blowfish.new(key)
    key = cipher.decrypt(ciphertext)
    return key

def decryptFile(file_name, key):
    with open(file_name, 'rb') as file:
        ciphertext = file.read()
        print "success"
    dec = decrypt(ciphertext, key)
    with open(file_name,'wb') as file:
        file.write(dec)

def decryptKey(key_name, key):
    with open(key_name, 'rb') as file:
        ciphertext = file.read()
        print "success"
    dec = decrypt_Blowfish(ciphertext, key)
    return dec

def saveKey(txt_file, key):
    f = open(txt_file + '.key', 'w')
    f.write(key)
    f.close()



if __name__ == '__main__':
    password = "46xwzGJub4tlc0Qd@zeDs78Y"
    key = generateKey(password)
    txt_file = "include/test.txt"
    jpg_file = "include/test.jpg"
    #saveKey(txt_file, key)
    encryptFile(txt_file, key)
    saveKey(txt_file, key)
    encryptKey(txt_file + ".key",password)

    if txt_file + ".key":
        print "reading key from file"
        key = decryptKey(txt_file + ".key", password)
    decryptFile(txt_file, key)
    encryptFile(jpg_file, key)
    saveKey(jpg_file, key)
    encryptKey(jpg_file + ".key", password)
    if jpg_file + ".key":
        print "reading key from file"
        key = decryptKey(txt_file + ".key", password)
    decryptFile(jpg_file, key)
