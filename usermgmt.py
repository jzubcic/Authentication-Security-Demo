import sys
from getpass import getpass
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA512
from os import path
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode


def hash_salt_password(plain_password: str):
    salt = get_random_bytes(16)
    pbkdf = PBKDF2(plain_password, salt, 16, count=1000000, hmac_hash_module=SHA512)
    return pbkdf.hex() + ' ' + b64encode(salt).decode('utf-8')


def add_user(username: str):
    if path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                if line.split()[0] == username:
                    print("User with given username already exists.")
                    return
    password = getpass()
    while len(password) < 8:
        print("Password must be at least 8 characters long.")
        password = getpass()
    repeated_password = getpass("Repeat password: ")

    if password != repeated_password:
        print("User add failed. Password mismatch.")
        return

    hash_and_salt = hash_salt_password(password)
    with open('users.txt', 'a') as file:
        file.write(f'{username} {hash_and_salt}\n')
    print('User successfully added.')


def delete_user(username: str):
    successfully_deleted = False
    if path.exists('users.txt'):
        file = open('users.txt', 'r')
        lines = file.readlines()
        file.close()

        with open('users.txt', 'w') as users:
            for line in lines:
                if line.split()[0] != username:
                    users.write(line)
                else:
                    successfully_deleted = True

    print("User successfully removed." if successfully_deleted else "User does not exist.")


def change_password(username: str):
    if path.exists('users.txt'):
        lines = []
        with open('users.txt', 'r') as file:
            lines = file.readlines()
        found = False
        for i in range(len(lines)):
            if lines[i].split()[0] == username:
                password = getpass()
                repeated_password = getpass("Repeat password: ")
                if password != repeated_password:
                    print("Password change failed. Password mismatch.")
                    return
                lines[i] = username + ' ' + hash_salt_password(password)
                found = True
        if not found:
            print("User does not exist.")
            return

        with open('users.txt', 'w') as file:
            for line in lines:
                file.write(line.strip() + "\n")
        print("Password change successful.")
        return


def force_password_change(username: str):
    if path.exists('users.txt'):
        lines = []
        with open('users.txt', 'r') as file:
            lines = file.readlines()

        found = False
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
            if lines[i].split()[0] == username:
                if '!' not in lines[i]:
                    lines[i] += ' !'
                found = True

        if not found:
            print("User does not exist.")
            return

        with open('users.txt', 'w') as file:
            for line in lines:
                file.write(line.strip() + "\n")
        print("User will be requested to change password on next login.")
        return


def main():
    if len(sys.argv) != 3:
        print("Incorrect usage.")
        return
    if sys.argv[1] == 'add':
        add_user(sys.argv[2])
    elif sys.argv[1] == 'passwd':
        change_password(sys.argv[2])
    elif sys.argv[1] == 'forcepass':
        force_password_change(sys.argv[2])
    elif sys.argv[1] == 'del':
        delete_user(sys.argv[2])
        pass
    else:
        print("Invalid command, available commands are: 'add <username>', 'passwd <username>', "
              "'forcepass <username>' and 'del <username>'")


if __name__ == '__main__':
    main()
