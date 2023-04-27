import os
import sys
import math
import random
import random


if __name__ == "__main__":
    orig_stdout = sys.stdout
    w = open("positive.txt", "w")
    sys.stdout = w
    f = open("temp_positive.txt", encoding="ISO-8859-1")
    for line in f:
        if line.strip():
            two = line.split()
            print(two[1])
    sys.stdout = orig_stdout
    w.close()
    orig_stdout = sys.stdout
    w = open("negative.txt", "w")
    sys.stdout = w
    sofar = 0
    count = 0
    f = open("temp_negative.txt", encoding="ISO-8859-1")
    print("hi")
    for line in f:
        if line.strip():
            temp = random.choices(population = ["i", "n"], weights = [358/501, (1 - (358/501))])
            if temp[0] == "i" or ((501 - sofar) == (384 - count)):
                count += 1
                two = line.split()
                print(two[1])
            sofar += 1
    sys.stdout = orig_stdout
    w.close()
