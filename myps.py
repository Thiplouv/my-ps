#! /usr/bin/python3

# Import modules
import sys
import os

# Default printed template
default_columns = ["PID","TTY","TIME","COMM"]

# Columns formatting parameters
settings = [
#     code          header      format
    ["pid",         "PID",      "{:>5}"],
    ["ppid",        "PPID",     "{:>5}"],
    ["cmd",         "CMD",      "{:<27}"],
    ["command",     "COMMAND",  "{:<27}"],
    ["comm",        "COMM",     "{:<15}"], # NOTE : comm argument will have "COMMAND" header, but it is applied later.
    ["tname",       "TTY",      "{:<8}"],
    ["cputime",     "TIME",     "{:>8}"],
    ["cputimes",    "TIMES",    "{:>8}"]   # NOTE : cputimes argument will have "TIME" header, but it is applied later.
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

# Verify if the comm (The filename of the executable, in parentheses) contains spaces, and removes it
def verify_comm(content) :
    if str(content[2]).startswith("(") and str(content[2]).endswith(")") : # If comm is a single element, don't touch anything !
        return content
    else :
        for i in range(len(content)) :
            if content[i].startswith("(") :
                bgn = i # Begin for the join
            if content[i].endswith(")") :
                end = i+1 # End for the join
        content[bgn : end] = ["_sep_".join(content[bgn : end])]
        content[1] = content[1].replace("_sep_", " ") # Custom separator to avoid unwanted char deletion
        return content

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
    else : 
        clmn_names = default_columns
        return clmn_names

# Recover the Process Identifier
def get_ud_pids() :
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
    
    list_pids = sort_pids(list_pids)
    return list_pids

# Recover all current PIDs in /proc/
def get_all_pids() :
    list_pids = []
    with os.scandir("/proc/") as content : # NOTE : Combo between with() statement and scandir() to ensure that closing is fine
        for entry in content : # For each element in /proc/
            if entry.is_dir() is True : # Recover the files
                if entry.name.isdigit() is True : # Whose names are alphanumeric characters
                    list_pids.append(entry.name) # Add the PID to the list
    return list_pids

# Recover current terminal related processes
def get_cterm_pids() :
    list_pids = [] # Create final pids list
    current_pid = os.getpid() # Recover the current process id
    tty_nr = get_ttynr(current_pid) # Recovers it's tty_nr
    all_running = get_all_pids() # Recover all running processes ids

    for elem in all_running : # Recover the pids if the tty_nr values are sames
        if get_ttynr(elem) == tty_nr :
            list_pids.append(elem)

    list_pids = sort_pids(list_pids)
    return list_pids

# Sorts PIDs
def sort_pids(list_pids) :
    list_pids = [int(i) for i in list_pids] # Converts elements in ints
    list_pids.sort() # Sort them
    list_pids = [str(i) for i in list_pids] # Converts sorted elements in strings
    return list_pids

# Recover the Parent Process Identifier
def get_ppid(pid) :
    path = '/proc/' + str(pid) + '/stat' # Create the path
    with open(path, "r") as stat : # Opens it (no close needed due to with statement)
        content = stat.read() # Read the content of the file
    content = content.split()
    content = verify_comm(content) # Removes accidental spaces in comm (/proc/[pid]/stat[2nd elemnt])
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
    path = '/proc/' + str(pid) + '/stat' # Create the path
    with open(path, "r") as stat : # Open the file and read it
        content = stat.read()
        content = content.split() # This destroys the .read()'s line feed
        content = verify_comm(content)
        comm = content[1]
        comm = comm.replace("(", "").replace(")", "")
        return comm

# Recover the tty_nr value that is the controlling terminal of the process
def get_ttynr(pid) :
    path = '/proc/' + str(pid) + '/stat' # Create the path
    with open(path, "r") as stat : # Open the file and read it
        content = stat.read()
        content = content.split() # This destroys the .read()'s line feed
        content = verify_comm(content)
        tnum = content[6] # Recover tty_nr
        return tnum

# Recovers the TTY if it is not permissions restricted
def get_tname(pid) :
    path = '/proc/' + str(pid) + '/fd/0' # Create the path
    try :
        tname = os.readlink(path) # Processes can have tty's symbolics links in fd folder
        if "/dev/" in tname :
            tname = tname.removeprefix("/dev/")
        if tname == "null" :
            tname = "?"
    except PermissionError : # If the symbolic link is not readable, ps prints "?"
        tname = "?"
    return tname

# Recover cumulative CPU time in "[DD-]hh:mm:ss" format
def get_cputime(pid) :
    t = get_cputimes(pid)
#   NOTE : Job is not done yet :
    dd = int(t / (60 * 60 * 24)) # Days
    tmp1 = t - (dd * 24 * 60 * 60)
    hh = int(tmp1 / (60 * 60)) # Hours
    tmp2 = tmp1 - (hh * 60 * 60)
    mm = int(tmp2 / 60) # Minutes
    ss = tmp2 - (mm * 60) # Seconds
    if dd != 0 : # Decide if there is need to print days or not
        time = "{:02d}".format(dd) + ":" + "{:02d}".format(hh) + ":" + "{:02d}".format(mm) + ":" + "{:02d}".format(ss)
    else :
        time = "{:02d}".format(hh) + ":" + "{:02d}".format(mm) + ":" + "{:02d}".format(ss)
    return time

# Recover cumulative CPU time in seconds
def get_cputimes(pid) : 
    path = '/proc/' + str(pid) + '/stat' # Create the path
    hwc_freq = os.sysconf("SC_CLK_TCK") # Recover the Clock Ticks Speed from the system
    with open(path, "r") as stat : # Opens it (no close needed due to with statement)
        content = stat.read() # Read the content of the file
    content = content.split()
    content = verify_comm(content)
    utime = int(content[13]) / hwc_freq # cf. procfs man page : /proc/[pid]/stat section : utime
    stime = int(content[14]) / hwc_freq # cf. procfs man page : /proc/[pid]/stat section : stime
    t = int(utime + stime) # Complete time in seconds
    return t

# Display the columns names line 
def print_clmn_names(args) :
    for word in args :
        if word == "COMM" :
            template = generate_template(word.upper())
            print(template.format("COMMAND"), end = " ")
        else :
            if word == "TIMES" :
                template = generate_template(word.upper())
                print(template.format("TIME"), end = " ")
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
                print(template.format(get_cputime(pid)), end = " ")
            if word == "TIMES" :
                print(template.format(get_cputimes(pid)), end = " ")

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
    # Case where user displays some specifics pids
    if "-p" in sys.argv :
        list_pids = get_ud_pids()
        clmn_names = get_clmn_names()

    # Case where user displays all pids
    if "-e" in sys.argv :
        list_pids = get_all_pids()
        clmn_names = get_clmn_names()

    # All the other cases
    else :
        list_pids = get_cterm_pids()
        clmn_names = get_clmn_names()

    print_clmn_names(clmn_names)

    for pid in list_pids :
        
        if pid != "" : # If PID does not exists, only prints columns names
            print()
        print_table(clmn_names)
    print()


# Print error message if command not used properly
except ValueError :
    print("Usage: ./myps.py options flag [arguments]")