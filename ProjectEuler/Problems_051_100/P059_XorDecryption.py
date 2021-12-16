"""

Each character on a computer is assigned a unique code and the preferred standard is ASCII (American Standard Code
for Information Interchange). For example, uppercase A = 65, asterisk = 42, and lowercase k = 107.

A modern encryption method is to take a text file, convert the bytes to ASCII, then XOR each byte with a given value,
taken from a secret key. The advantage with the XOR function is that using the same encryption key on the cipher text,
restores the plain text; for example, 65 XOR 42 = 107, then 107 XOR 42 = 65.

For unbreakable encryption, the key is the same length as the plain text message, and the key is made up of random
bytes. The user would keep the encrypted message and the encryption key in different locations, and without both
"halves", it is impossible to decrypt the message.

Unfortunately, this method is impractical for most users, so the modified method is to use a password as a key.
If the password is shorter than the message, which is likely, the key is repeated cyclically throughout the message.
The balance for this method is using a sufficiently long password key for security, but short enough to be memorable.

Your task has been made easy, as the encryption key consists of three lower case characters (a-z).
Using the knowledge that the plain text must contain common English characters (a-z, A-Z, 0 - 9), brackets (),
common symbols (;:,.'?-!) and spaces decrypt the message and find the key that is used to encrypt the message.

Note It is guaranteed that key is unique, is of size 3 and contains lower case english characters (a-z).


"""
from typing import List

lower = {code for code in range(ord('a'), ord('z') + 1)}
upper = {code for code in range(ord('A'), ord('Z') + 1)}
other = {ord(ch) for ch in " 0123456789();:,.'?-!"}
text_set = lower.union(upper).union(other)
text_set = {code for code in range(ord(' '), ord('~'))}
key_set = lower


def get_key(text: List[int]) -> int:
    for key in key_set:
        if all(ch ^ key in text_set for ch in text):
            return key
    return ord('!')


def find_code(text: List[int]) -> List[int]:
    k0 = text[::3]
    k1 = text[1::3]
    k2 = text[2::3]
    key = [get_key(k0), get_key(k1), get_key(k2)]
    code_sum = 0
    for ndx, letter in enumerate(text):
        code_sum += letter ^ key[ndx % 3]
    print(code_sum)
    return key


def hacker_main():
    n = int(input())
    text = list(map(int, input().split()))
    key = ''.join([chr(num) for num in find_code(text)])
    print(key)


def euler_main():
    with open('p059_cipher.txt', 'r') as f:
        text = list(map(int, f.readline().split(',')))
    key = ''.join([chr(num) for num in find_code(text)])
    print(key)


euler_main()
