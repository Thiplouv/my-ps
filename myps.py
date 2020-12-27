#! /usr/bin/python3

import sys

args = str(sys.argv[2]).upper()
args = args.split(",")

def generate_template(column_name):
    settings = [
        ["PID", "{:>5}"],
        ["PPID", "{:>5}"],
        ["CMD", "{:<27}"]
    ]

    for i in range(len(settings)) :
        if settings[i][0] == column_name :
            return(settings[i][1])

try :
    if len(sys.argv) <= 2 :
        print("{:>5} {:<8} {:>8} {:<27}".format("PID","TTY","TIME","CMD"))
    if "-o" in sys.argv :
        if "PID" not in args and "PPID" not in args and "CMD" not in args :
            print("This program only supports \"PID\", \"PPID\" and \"CMD\" arguments for the moment")
        else :
            for word in args :
                template = generate_template(word)
                print(template.format(word), end = " ")
except ValueError :
    print("Usage: ./myps.py options flag [arguments]")