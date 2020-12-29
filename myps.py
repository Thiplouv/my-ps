#! /usr/bin/python3

# Import modules
import sys

# Columns parameters
settings = [
    ["PID", "{:>5}"],
    ["PPID", "{:>5}"],
    ["CMD", "{:<27}"],
    ["COMMAND", "{:<27}"],
    ["TTY", "{:<8}"],
    ["TIME", "{:>8}"]
]

# Generate column padding template
def generate_template(column_name):
    for i in range(len(settings)) :
        if settings[i][0] == column_name :
            return(settings[i][1])

# Verify presence of keyword in settings
def verif_keywords(keywords) :
    badkwd = []
    for word in keywords :
        if all(word != settings[i][0] for i in range(len(settings))) is True :
            badkwd.append(word)
    return badkwd

try :
    # Default printing if no argments were given
    if len(sys.argv) <= 2 :
        print("{:>5} {:<8} {:>8} {:<27}".format("PID","TTY","TIME","CMD"))
    # Formatting option
    if "-o" in sys.argv :
        # Get -o arguments position and split ',' 
        pos = sys.argv.index("-o")
        args = str(sys.argv[pos + 1]).upper()
        args = args.split(",")
        verif = verif_keywords(args)
        if len(verif) != 0 :
            for i in range(len(verif)) :
                print("ps: {:s}: keyword not found".format(verif[i]))
            print("ps: no valid keywords; valid keywords:\npid ppid cmd command tty time")
        else :
            for word in args :
                template = generate_template(word)
                print(template.format(word), end = " ")
# Print error message if command not used properly
except ValueError :
    print("Usage: ./myps.py options flag [arguments]")