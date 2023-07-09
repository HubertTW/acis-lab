import sys
import codecs
import binascii
import random
import chardet


def strxor(a, b):  # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


def xor(a, b):
    if len(str(a)) > len(str(b)):
        return [x ^ y for (x, y) in zip(a[:len(str(b))], b)]
    else:
        return [x ^ y for (x, y) in zip(a, b[:len(str(a))])]


def hexToStr(arr):
    words = []
    for i in arr:
        words.append(' '.join([chr(int(''.join(c), 16)) for c in zip(i[0::2], i[1::2])]).replace(';', '\n- '))
    return words


def encrypt(key, msg):
    c = strxor(key, msg)
    print(c.encode('hex'))
    return c


def main():
    with open('ciphertexts.txt', 'r', encoding='UTF-8') as file:
        l = []

        line = file.readline()
        line = line.replace('\n', '')
        line = line.replace(' ', '')
        l.append(line)

        while line is not None and line != '':
            line = file.readline()
            line = line.replace('\n', '')
            line = line.replace(' ', '')
            l.append(line)
        file.close()

    MSGS = []
    start = 0
    for key, value in enumerate(l):
        if (value == '-'):
            MSGS.append(''.join(l[start:key]).lower())
            start = key + 1
    print(MSGS)
    words = hexToStr(MSGS)
    print(words)
    results = [strxor(words[-1], msg) for msg in words[:-1]]
    print(results)
    print("length is ", len(results))
    for i in results:
        print(chardet.detect(str.encode(i)))
        print(i)


if __name__ == '__main__':
    main()
