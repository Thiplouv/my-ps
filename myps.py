#! /usr/bin/python3

import sys

args = str(sys.argv[2]).upper()
args = args.split(",")

settings = [
    ["PID", "{:>5}"],
    ["PPID", "{:>5}"],
    ["CMD", "{:<27}"],
    ["COMMAND", "{:<27}"],
    ["TTY", "{:<8}"],
    ["TIME", "{:>8}"]
]

def generate_template(column_name):
    for i in range(len(settings)) :
        if settings[i][0] == column_name :
            return(settings[i][1])

try :
    if len(sys.argv) <= 2 :
        print("{:>5} {:<8} {:>8} {:<27}".format("PID","TTY","TIME","CMD"))
    if "-o" in sys.argv :
        if "PID" not in args and "PPID" not in args and "CMD" not in args and "COMMAND" not in args and "TTY" not in args and "TIME" not in args :
            print("ps: {:s}: keyword not found".format(sys.argv[2]))
            print("ps: no valid keywords; valid keywords:\npid ppid cmd command tty time")
        else :
            for word in args :
                template = generate_template(word)
                print(template.format(word), end = " ")
except ValueError :
    print("Usage: ./myps.py options flag [arguments]")