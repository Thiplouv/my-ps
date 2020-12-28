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

def verif_keywords(keywords) :
    badkwd = []
    for word in keywords :
        if all(word != settings[i][0] for i in range(len(settings))) is True :
            badkwd.append(word)
    return badkwd

try :
    if len(sys.argv) <= 2 :
        print("{:>5} {:<8} {:>8} {:<27}".format("PID","TTY","TIME","CMD"))
    if "-o" in sys.argv :
        verif = verif_keywords(args)
        if len(verif) != 0 :
            for i in range(len(verif)) :
                print("ps: {:s}: keyword not found".format(verif[i]))
            print("ps: no valid keywords; valid keywords:\npid ppid cmd command tty time")
        else :
            for word in args :
                template = generate_template(word)
                print(template.format(word), end = " ")
except ValueError :
    print("Usage: ./myps.py options flag [arguments]")