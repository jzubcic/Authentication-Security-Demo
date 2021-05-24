# Authentication Security Demo

## Installation

After cloning the repo pycryptodome must be installed:  
  ``` pip install pycryptodome ```

## Usage

Adding users:  
  ```python usermgmt.py add <user>```  
  
Changing user's password:   
  ```python usermgmt.py passwd <user>```  
  
Forcing user to change password on next login:   
  ```python usermgmt.py forcepass <user>```  
  
Deleting users:   
  ```python usermgmt.py del <user>```  
  
  
Logging in:   
  ```python login.py <user>```  
  
  
## Description

Storing passwords is done by first adding salt to the password and then running it through PBKDF2 key derivation function. This prevents rainbow tables attacks and makes brute-forcing difficult, beacuse the PKDF2 function is computationally much slower than a regular cryptographic hash function. 
Passwords cannot be seen while being entered, new passwords must be different than old passwords upon being forced to changed them and there is a time delay between unsuccessful login attempts to further increase the difficulty of brute force attacks. 
