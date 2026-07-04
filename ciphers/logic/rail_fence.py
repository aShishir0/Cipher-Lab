"""
Rail Fence Cipher
-----------------
A classical transposition cipher. Characters of the plaintext are written
diagonally in a zig-zag pattern across a number of "rails" (rows), then
read off row by row to produce the ciphertext.

Example (key = 3), plaintext "HELLOWORLD":

H . . . O . . . R . .
. E . L . W . L . D .
. . L . . . O . . . .

Reading row by row gives the ciphertext: "HORELWLDLO"
"""


def rail_fence_encrypt(text: str, key: int) -> str:
    """Encrypt `text` using a Rail Fence cipher with `key` rails."""
    if key <= 1:
        return text

    fence = [[] for _ in range(key)]
    rail = 0
    direction = 1  # +1 moves down the rails, -1 moves up

    for char in text:
        fence[rail].append(char)
        if rail == 0:
            direction = 1
        elif rail == key - 1:
            direction = -1
        rail += direction

    return "".join("".join(row) for row in fence)


def rail_fence_decrypt(cipher: str, key: int) -> str:
    """Decrypt a Rail Fence ciphertext that was encrypted with `key` rails."""
    if key <= 1:
        return cipher

    # Step 1: figure out which rail each position in the plaintext belongs to
    # by simulating the same zig-zag walk used during encryption.
    rail_pattern = []
    rail = 0
    direction = 1
    for _ in range(len(cipher)):
        rail_pattern.append(rail)
        if rail == 0:
            direction = 1
        elif rail == key - 1:
            direction = -1
        rail += direction

    # Step 2: the ciphertext is the concatenation of each rail's characters
    # in order. Sort the original positions by rail number to know how many
    # characters belong to each rail and in what original order.
    indices_sorted_by_rail = sorted(range(len(cipher)), key=lambda i: rail_pattern[i])

    plaintext = [""] * len(cipher)
    for cipher_index, original_index in enumerate(indices_sorted_by_rail):
        plaintext[original_index] = cipher[cipher_index]

    return "".join(plaintext)
