#! /usr/bin/python3

# Import modules
import sys
import os

# Default printed template
default_printing = ["PID","TTY","TIME","CMD"]

# Columns formatting parameters
settings = [
#     code       header      format
    ["pid",     "PID",      "{:>5}"],
    ["ppid",    "PPID",     "{:>5}"],
    ["cmd",     "CMD",      "{:<27}"],
    ["command", "COMMAND",  "{:<27}"],
    ["comm",    "COMM",     "{:<15}"], # NOTE : comm argument will have "COMMAND" header, but it is applied later.
    ["tname",   "TTY",      "{:<8}"],
    ["time",    "TIME",     "{:>8}"]
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
        if settings[i][0] == column_name.lower() :
            return(settings[i][2])
        if settings[i][1] == column_name.upper() :
            return(settings[i][2])

# Verify presence of keyword in settings
def verif_keywords(keywords) :
    badkwd = []
    for word in keywords :
        if all(word.lower() != settings[i][0] for i in range(len(settings))) is True :
            badkwd.append(word)
    return badkwd

# Function to truncate the printed string if arguments width is longer than column width
def verify_width(word) :
    template = generate_template(word) # Read the original template
    width = ""
    template = list(template) # Convert string to list

    # Export the original width from the original template
    for elem in template :
        if elem.isdigit() is True :
            width += elem

    # Adaptive argument width recognition (due to != files locations)
    if word == "CMD" or word == "COMMAND" or word == "ARGS" :
        data = get_cmdline(pid)
    if word == "COMM" :
        data = get_comm(pid)

    if len(data) > int(width) : # Compare the two widths and truncate argument if needed the lowest one
        data = data[:int(width)]
    
    return data

# Verify if the dirrectory exists
def isdir(path) :
    isdir = os.path.isdir(path)
    return isdir

# Recover column(s) name(s)
def get_clmn_names() :
    clmn_names = []
    if "-o" in sys.argv :
        args = get_args("-o") # Recover args for '-o' option
        verif = verif_keywords(args) # Verify the keywords
        if len(verif) != 0 :
            for i in range(len(verif)) :
                print("error: unknown user-defined format specifier \"{:s}\"".format(verif[i]))
            print_usage()
            os._exit(0) # Kill the program
        else :
            for word in args :
                for i in range(len(settings)) :
                    if settings[i][0] == word.lower() :
                        clmn_names.append(settings[i][1])
            return clmn_names
#   NOTE : This section need to be remooved when TTY and TIME functions will be supported
    if "-o" not in sys.argv and "-p" in sys.argv :
        clmn_names.append("PID")
        return clmn_names
    else :
        return clmn_names

# Recover the Process Identifier
def get_pid() :
    if "-p" in sys.argv :
        args = get_args("-p") # Recover args for '-p' option
        list_pids = [] # Create the list of processes identifiers returned
        for elem in args : # For each pid in the list gived by user
            if elem.lstrip("-").isdigit() is True : # PID must be an alphanumeric character
#                                                     NOTE : use of lstrip() is mandatory, otherwise isdigit() consider negatives number as non digit due to "-"
                if int(elem) <= 0 or int(elem) > 4194304 : # Process ID must be between 1 and 4194304
#                                                            NOTE : cf. /proc/sys/kernel/pid_max : Maximum value for PID is 4194304
                    print("error : process ID out of range")
                    print_usage()
                    os._exit(0) # Kill the program

                else :
                    path = "/proc/" + str(elem) # Create the path
                    if isdir(path) is True : # Verify if the folder exists
                        list_pids.append(elem) # Add the PID to the list

            else : # Process ID must be an integer
                print("error: process ID list syntax error")
                print_usage()
                os._exit(0) # Kill the program

        return list_pids

# Recover the Parent Process Identifier
def get_ppid(pid) :
    path = '/proc/' + str(pid) + '/stat' # Create the path
    with open(path, "r") as stat : # Opens it (no close needed due to with statement)
        content = stat.read() # Read the content of the file
    content = content.split()
    ppid = int(content[3]) # cf. procfs manual page : PPID is the 4th element of stat file
    return ppid

# Recover the complete command line for the process ID. (cf. procfs manual)
def get_cmdline(pid) :
    path = '/proc/' + str(pid) + '/cmdline' # Create the path
    with open(path, "r") as cmdline : # Open the file and read it
        content = cmdline.read()
    content = content.split("\0") # cf. procfs manual : "The command-line arguments appear in this file 
#                                                         as a set of strings separated by null bytes ('\0')"
    content.pop() # Remove last elem of the list (empty elem due to final '\00')
    command = ""
    command = " ".join(content) # Create the final string for printing
    if len(command) == 0 :
        command = "[" + get_comm(pid) + "]"
    return command

# Recover the process's comm value—that is, the command name associated with the process. (cf. procfs manual)
def get_comm(pid) :
    path = '/proc/' + str(pid) + '/comm' # Create the path
    with open(path, "r") as comm_file : # Open the file and read it
        content = comm_file.read()
        content = content.split() # This destroys the .read()'s line feed
        comm = content[0]
        return comm

# Recovers the TTY if it is not permissions restricted
def get_tname(pid) :
    path = '/proc/' + str(pid) + '/fd/0' # Create the path
    try :
        tname = os.readlink(path) # Processes can have tty's symbolics links in fd folder
        if "/dev/" in tname :
            tname = tname.removeprefix("/dev/")
    except PermissionError : # If the symbolic link is not readable, ps prints "?"
        tname = "?"
    return tname

# Display the columns names line 
def print_clmn_names(args) :
    for word in args :
        if word == "COMM" :
            template = generate_template(word.upper())
            print(template.format("COMMAND"), end = " ")
        else :
            template = generate_template(word.upper())
            print(template.format(word.upper()), end = " ")

# Display the rest of the table
def print_table(args) :
    if pid != "" : # If PID does not exists, only prints columns names
        for word in args :
            word = word.upper()
            template = generate_template(word.upper())
            if word == "PID" :
                print(template.format(pid), end = " ")
            if word == "PPID" :
                print(template.format(get_ppid(pid)), end = " ")
            if word == "CMD" or word == "COMMAND" or word == "ARGS" :
                data = verify_width(word)
                print(template.format(data), end = " ")
            if word == "COMM" :
                data = verify_width(word)
                print(template.format(data), end = " ")
            if word == "TTY" :
                print(template.format(get_tname(pid)), end = " ")
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

# Shortcut function to print the usage help message from the official ps tool
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

    list_pids = get_pid()

    print_clmn_names(clmn_names)

    for pid in list_pids :
        
        if pid is not None :
            if len(clmn_names) == 0 :
                clmn_names = default_printing
            
        else :
            pid = 1
        
        if pid != "" : # If PID does not exists, only prints columns names
            print()
        print_table(clmn_names)
    print()


# Print error message if command not used properly
except ValueError :
    print("Usage: ./myps.py options flag [arguments]")