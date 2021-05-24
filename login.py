import sys
import time
from getpass import getpass
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from Crypto.Protocol.KDF import PBKDF2


def attempt_login(username: str):
    password = getpass()
    users = []
    with open('users.txt', 'r') as file:
        users = file.readlines()

    exists = False
    for i in range(len(users)):
        if users[i].split()[0] == username:
            exists = True
            salt = users[i].split()[2]
            pbkdf = PBKDF2(password, b64decode(salt), 16, count=1000000, hmac_hash_module=SHA512)
            delay = 0
            while pbkdf.hex() != users[i].split()[1]:
                print("Username or password incorrect.")
                time.sleep(delay)
                delay += 1
                password = getpass()
                pbkdf = PBKDF2(password, b64decode(salt), 16, count=1000000, hmac_hash_module=SHA512)
            if '!' in users[i]:
                new_password = getpass("New password: ")
                while len(new_password) < 8:
                    print("Password must be at least 8 characters long.")
                    new_password = getpass("New password: ")
                while new_password == password:
                    print("New password cannot be the same as old password.")
                    new_password = getpass("New password: ")
                    while len(new_password) < 8:
                        print ("Password must be at least 8 characters long.")
                        new_password = getpass("New password: ")
                repeated_new_password = getpass("Repeat new password: ")
                while new_password != repeated_new_password:
                    print("Password change failed. Password mismatch.")
                    return
                salt = get_random_bytes(16)
                pbkdf = PBKDF2(new_password, salt, 16, count=1000000, hmac_hash_module=SHA512)
                users[i] = username + ' ' + pbkdf.hex() + ' ' + b64encode(salt).decode('utf-8')
                with open('users.txt', 'w') as file:
                    for line in users:
                        file.write(line.strip() + "\n")
                print("Login successful.")
            else:
                print("Login successful.")
            break

    if not exists:
        print("Username or password incorrect.")
        attempt_login(username)
        return


def main():
    if len(sys.argv) == 2:
        attempt_login(sys.argv[1])
    else:
        print("Incorrect usage, please provide username as argument.")


if __name__ == '__main__':
    main()
