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
    
    #str = ""
    #if "PID" in column_names :
    #    str += "{:>5}"
    #    if args[len(args)-1] != "PID" :
    #        str += " "
    #if "PPID" in column_names :
    #    str += "{:>5}"
    #    if args[len(args)-1] != "PPID" :
    #        str += " "
    #if "CMD" in column_names :
    #    str += "{:<27}"
    #    if args[len(args)-1] != "CMD" :
    #        str += " "
    #return str

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
            #for i in range(len(args)) :
            #    print(template.format(args[i], end = " "))
            
            #template = generate_template(args)
            #tbl = ""
            #for word in args :
            #    tbl += word
            #    if word != args[len(args)-1] :
            #        tbl += " "
            #print(template.format(*args, end=" "))
        
        #for word in args :
            #if word == "PID" or word == "PPID" or word == "CMD" :
            #    template = generate_template(args)
            #    print(template.format(str(args)))
            #else :
            #    print("This program only supports \"PID\", \"PPID\" and \"CMD\" arguments for the moment")

        #if "PID" in args and "PPID" in args and "CMD" in args :
        #    print("{:>5} {:5>} {:<27}".format(args[0], args[1], args[2]))
        #else :
            #print("This program only supports \"PID\", \"PPID\" and \"CMD\" arguments for the moment")

except ValueError :
    print("Usage: ./myps.py options flag [arguments]")