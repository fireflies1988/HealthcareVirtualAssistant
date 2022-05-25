import sys


def writeFile(key):
    try:
        with open("key.txt", 'w', encoding='utf-8') as f:
            f.write(key)
    finally:
        f.close()


def readFile():
    a = ""
    f = open("key.txt", 'r', encoding='utf-8')
    a = f.readline()
    return a


def checkFile():
    a = readFile()
    if a and a.strip():
        # myString is not None AND myString is not empty or blank
        return True
        # myString is None OR myString is empty or blank
    return False
