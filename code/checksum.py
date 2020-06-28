import sys
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
def get_checksum(bytes_read):
    checksum = 0
    for c in bytes_read:
        checksum = checksum + c
    checksum = -(checksum % 256)
    return checksum

print(get_checksum())