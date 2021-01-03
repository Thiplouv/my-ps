#! /usr/bin/python3

# Import modules
import sys
import os

default_printing = ["PID","TTY","TIME","CMD"]

# Columns parameters
settings = [
    ["PID", "{:>5}"],
    ["PPID", "{:>5}"],
    ["CMD", "{:<27}"],
    ["COMMAND", "{:<27}"],
    ["TTY", "{:<8}"],
    ["TIME", "{:>8}"]
]

# Recover arguments for the option entered by user
def get_args(option) :
        pos = sys.argv.index(option) # Get option's position
        args = str(sys.argv[pos + 1]) # Convert string's content into capital letters 
        args = args.split(",") # Split the ','
        return args

# Generate column padding template
def generate_template(column_name):
    for i in range(len(settings)) :
        if settings[i][0] == column_name.upper() :
            return(settings[i][1])

# Verify presence of keyword in settings
def verif_keywords(keywords) :
    badkwd = []
    for word in keywords :
        if all(word.upper() != settings[i][0] for i in range(len(settings))) is True :
            badkwd.append(word)
    return badkwd

# Verify if the dirrectory exists
def isdir(path) :
    isdir = os.path.isdir(path)
    return isdir

# Recover column(s) name(s)
def get_clmn_names() :
    if "-o" in sys.argv :
        clmn_names = get_args("-o") # Recover args for '-o' option
        verif = verif_keywords(clmn_names) # Verify the keywords
        if len(verif) != 0 :
            for i in range(len(verif)) :
                print("error: unknown user-defined format specifier \"{:s}\"".format(verif[i]))
            print_usage()
            os._exit(0) # Kill the program
        else :
            return clmn_names
    else :
        clmn_names = []
        return clmn_names

# Recover the Process Identifier
def get_pid() :
    if "-p" in sys.argv :
        args = get_args("-p") # Recover args for '-p' option
        # NOTE : Only one PID is actually supported, so the pid is the first element of args
        if args[0].isdigit() is True : # PID must be an intenger
            pid = args[0] 
            path = "/proc/" + str(pid) # Create the path
            if int(args[0]) == 0 or int(args[0]) > 4194304 : # Process ID must be positive 
                                                             # NOTE : cf. /proc/sys/kernel/pid_max : Maximum value for PID is 4194304
                print("error : process ID out of range")
                print_usage()
                os._exit(0) # Kill the program
            if isdir(path) is True : # Verify if the folder exists
                return pid
            else :
                pid = ""
                return pid
        if int(args[0]) < 0 : # Process ID must be positive
            print("error : process ID out of range")
            print_usage()
            os._exit(0) # Kill the program
        else : # Process ID must be an integer
            print("error: process ID list syntax error")
            print_usage()
            os._exit(0) # Kill the program

# Recover the Parent Process Identifier
def get_ppid(pid) :
    path = '/proc/' + str(pid) + '/stat' # Create the path
    with open(path, "r") as stat : # Opens it (no close needed due to with statement)
        content = stat.read() # Read the content of the file
    content = content.split()
    ppid = int(content[3]) # cf. procfs manual page : PPID is the 4th element of stat file
    return ppid

# Display the columns names line 
def print_clmn_names(args) :
    for word in args :
        template = generate_template(word)
        print(template.format(word.upper()), end = " ")

# Display the rest of the table
def print_table(args) :
    if pid != "" : # If PID does not exists, only prints columns names
        for word in args :
            word = word.upper()
            template = generate_template(word)
            if word == "PID" :
                print(template.format(pid), end = " ")
            if word == "PPID" :
                print(template.format(get_ppid(pid)), end = " ")
            if word == "CMD" :
                print(template.format(""), end = " ")
            if word == "TTY" :
                print(template.format(""), end = " ")
            if word == "TIME" :
                print(template.format(""), end = " ")

# Check if the imputed arg is the last in the list
def isitlast(args, a) :
    for word in args :
        if word == args[len(args)-1] :
            last = word
    if a == last :
        return True
    else :
        return False

def print_usage() :
    print("\nUsage:")
    print(" ps [options]\n")
    print(" Try 'ps --help <simple|list|output|threads|misc|all>'")
    print("  or 'ps --help <s|l|o|t|m|a>'")
    print(" for additional help text.\n")
    print("For more details see ps(1).")

try :
    # Default printing if no argments were given by user
    if len(sys.argv) <= 2 :
        clmn_names = default_printing
    else :
        # Try to get the column(s) name(s)
        clmn_names = get_clmn_names()

    # Try to get the PID
    pid = get_pid()

    if pid is not None :
        if len(clmn_names) == 0 :
            clmn_names = default_printing
        
    else :
        pid = 1
    
    print_clmn_names(clmn_names)
    if pid != "" : # If PID does not exists, only prints columns names
        print()
    print_table(clmn_names)
    print()


# Print error message if command not used properly
except ValueError :
    print("Usage: ./myps.py options flag [arguments]")