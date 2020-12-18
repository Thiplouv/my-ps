#! /usr/bin/python3

import sys

try :
    if len(sys.argv) <= 2 :
        print("{:>5} {:<8} {:>8} {:<27}".format("PID","TTY","TIME","CMD"))
    if "-o" in sys.argv :
        args = str(sys.argv[2]).upper()
        args = args.split(",")

        for word in args :
            if word == "PID" or word == "PPID" or word == "CMD" :
                print("{:>5} ".format(word))
            else :
                print("This program only supports \"PID\", \"PPID\" and \"CMD\" arguments for the moment")

        #if "PID" in args and "PPID" in args and "CMD" in args :
        #    print("{:>5} {:5>} {:<27}".format(args[0], args[1], args[2]))
        #else :
            #print("This program only supports \"PID\", \"PPID\" and \"CMD\" arguments for the moment")

except ValueError :
    print("Usage: ./myps.py options flag [arguments]")