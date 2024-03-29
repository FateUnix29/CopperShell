# Originially created by Copper/FateUnix29/Destiny. #


# Imports #

import colorama; from colorama import Fore as fore, Back as back    # This library is responsible for the colors of the output.
import time                                                         # This library is responsible for the timing of the program.
import os                                                           # This library is responsible for the operating system.
import shutil                                                       # This library is responsible for a few file or directory operations.
import sys                                                          # Kind of like 'os'.. Not really though.
import inspect                                                      # This library is used to get the arguments of a function.

print("Initialized imports.")

# Initialize Colorama

colorama.init()
print(f"{fore.BLUE}Initialized colors.")

# Constants #

located = os.path.realpath(os.path.dirname(__file__)) # The directory the script is located in.
cwd = os.getcwd() # The directory the script was ran from.
debug: bool = False # This is actually a fallback. Configure it in the config file.

print(f"{fore.BLUE}Initialized constants.")

# Global Variables #

term_dir = "Who the fuck knows?" # These two are also fallbacks.
user = "Huh?"
password = ""

conf_file_loc = os.path.join(located, "CopperShell.cfg")

# Configuration Settings #

shell_conf = {
    "username": "User",
    "start_dir": "C:",
    "password": "",
    "debug": False
}

print(f"{fore.LIGHTBLUE_EX}Initialized global variables.")

# Functions #

# Quite literally just because I'm lazy.
def cmd_syntax(command: str) -> str:
    return f"{fore.BLUE}{command}{fore.WHITE}:"

def error_syntax(error: str, details: str = "No special details provided.") -> str:
    return f"{back.RED}{fore.WHITE} ERROR: {back.RESET}{fore.RED} {error}: {details}{fore.RESET}"

def warning_syntax(warn: str, details: str = "No special details provided.") -> str:
    return f"{back.YELLOW}{fore.BLACK} ! {back.RESET}{fore.YELLOW} {warn}: {details}{fore.RESET}"

def notdoingthething(details: str = "No special details provided.") -> str:
    return f"{back.CYAN}{fore.WHITE}Not doing the thing.{back.RESET}{fore.YELLOW} Sorry not sorry. ({details})"


def manual_handler(page: str = ""):
    man_string = f"""{fore.YELLOW}Manual pages:{fore.WHITE}
'sorrynotsorry'     {fore.LIGHTRED_EX}(Error Type){fore.WHITE}
'help'              {fore.LIGHTBLUE_EX}(Command){fore.WHITE}
'man'               {fore.LIGHTBLUE_EX}(Command){fore.WHITE}
'config'            {fore.RED}(Administrative Command){fore.WHITE}
"""
    man_pages = {
        "sorrynotsorry": f"{fore.RED}sorrynotsorry{fore.WHITE}: {fore.CYAN}This error occurs when the case is so unexpected or rare that it should be outright impossible. Many of the error details given by this error reflect this.",
        "help": f"{fore.LIGHTBLUE_EX}help{fore.WHITE}: {fore.CYAN}Help information.",
        "man": f"{fore.LIGHTBLUE_EX}man (page){fore.WHITE}: {fore.CYAN}Manual pages, like the one you're looking at right now.",
        "config": f"{fore.RED}config (setting) (value){fore.WHITE}: {fore.CYAN}Configuration settings. Run it without arguments to see which settings you can modify and what they do.",
    }
    if page == "":
        print(man_string)
    else:
        if page in man_pages:
            print(man_pages[page])
        else:
            manpage = f"'{page}'"
            print(f"{warning_syntax('PageNotFound', f'The manual page {manpage} was not found.')}")

def write_config_file():
    try:
        with open(conf_file_loc, "w") as file:
            for setting in shell_conf:
                file.write(f"{setting} {shell_conf[setting]}\n")
        print(f"{fore.YELLOW}Successfully generated the shell configuration file ({conf_file_loc}).")
    except Exception as error:
        notdoingthething(f"Somehow failed during writing. Perhaps the script doesn't have sufficient permission? ({error})")

def read_config_file():
    if os.path.exists(conf_file_loc):
        try:
            with open(conf_file_loc, "r") as file:
                lines = file.readlines()
                # Newlines suck. Screw newlines. Death to newlines!
                if lines and (lines[-1].endswith("\n") or lines[-1].endswith("\r\n")):
                    lines[-1] = lines[-1].rstrip("\n\r")
                for lnum, line in enumerate(lines, start=1):
                    stripline = line.strip()
                    splitline = stripline.split(maxsplit=1)
                    if splitline[0] in shell_conf:
                        if len(splitline) >= 2:
                            if splitline[1] == "True": splitline[1] = True
                            if splitline[1] == "False": splitline[1] = False
                            shell_conf[splitline[0]] = splitline[1]
                        else:
                            shell_conf[splitline[0]] = ""
                    else:
                        print(f"{error_syntax('InvalidConfiguration', f'The shell configuration file ({conf_file_loc}), line {lnum} (starting from 1), contains an invalid configuration setting.')}")
                        sys.exit(1)
        except Exception as error:
            notdoingthething(f"Somehow failed during reading the configuration file. Perhaps the script doesn't have sufficient permission? ({error})")
    else:
        confnotfoundmsg = f'''The shell configuration file ({conf_file_loc}) was not found. It will be generated for you with default configurations.
The default configurations were already loaded in before this message, so you will be able to use them, even if writing the file fails.'''
        print(f"{warning_syntax('ConfigNotFound', confnotfoundmsg)}")
        write_config_file()

def modify_config_file(setting: str, value: str):
    if setting != "":
        if value != "":
            if setting in shell_conf:
                shell_conf[setting] = value
                write_config_file()
                read_config_file()
                print(f"{fore.GREEN}Successfully modified the shell configuration file.")
            else:
                strvalue = f"'{value}'"
                print(f"{warning_syntax('ConfigSettingNotFound', f'The configuration value specified was not found in the shell configuration file. ({strvalue})')}")
        else:
            strvalue = f"'{setting}'"
            print(f"{warning_syntax('BlankConfigValue', f'You have wrote a blank value to setting {strvalue}. This is not an error, but it could be a mistake.')}")
            if setting in shell_conf:
                shell_conf[setting] = value
                write_config_file()
                read_config_file()
                print(f"{fore.GREEN}Successfully modified the shell configuration file.")
            else:
                strvalue = f"'{value}'"
                print(f"{warning_syntax('ConfigSettingNotFound', f'The configuration value specified was not found in the shell configuration file. ({strvalue})')}")
    else:
        print(f"""The settings you can modify are:
{fore.LIGHTGREEN_EX}username (string){fore.WHITE}: Your name in the terminal. {fore.YELLOW}If modified, may require a restart.{fore.WHITE}
{fore.LIGHTGREEN_EX}start_dir (string){fore.WHITE}: The directory you start in. {fore.RED}If modified, will require a restart.{fore.WHITE}
{fore.LIGHTGREEN_EX}password (string){fore.WHITE}: The password for the shell. You need to enter this to access it. {fore.RED}If modified, will require a restart.{fore.WHITE}
{fore.LIGHTGREEN_EX}debug (bool){fore.WHITE}: Debug mode. If modified, {fore.YELLOW}may require a restart.{fore.WHITE}""")

print(f"{fore.YELLOW}Initialized functions.")

# Since this string is so large, it's rather hard to read if we put it directly in stdcommandset. It may also be useful to access elsewhere.

help_string = f"""{fore.YELLOW}Help Information:{fore.WHITE}
{fore.GREEN}Capitalization does not matter. Commands will automatically be ran as if you typed them in lower case, no matter what.
{cmd_syntax("help")} Show this help information.
{cmd_syntax("exit")} Exit this shell.
{cmd_syntax("cd")} Change directory to one specified. Uses your actual filesystem.
{cmd_syntax("ls")} List the contents of the current directory. Directories in blue, files in white, executable files in green, and hidden files (use -a) in yellow.
{cmd_syntax("config")} Configure this shell, such as setting the username or password.
{cmd_syntax("clear")} Clear the screen.
{cmd_syntax("man")} Show information on specific things, such as commands, or even different types of outputs from the shell."""



print(f"{fore.YELLOW}Initialized help.")



# Declare the standard command set. Anything that isn't special enough to require it's own specific functionality are here.
stdcommandset = {
    "help": lambda: print(help_string),
    "invalid": lambda: print(f"{fore.RED}Invalid command. run {fore.BLUE}help{fore.RED} to see the list of commands."),
    "exit": lambda: sys.exit(0),
    "man": lambda page = "": manual_handler(page),
    "config": lambda setting = "", value = "": modify_config_file(setting, value),
}

print(f"{fore.GREEN}Initialized command set.")
print(f"{fore.BLUE}Reading configuration file..")

read_config_file()
user = shell_conf["username"]
term_dir = shell_conf["start_dir"]
password = shell_conf["password"]
debug = shell_conf["debug"]
print(f"{fore.GREEN}Read configuration file.")

# "You shall not pass!" Check
if password != "":
    tries = 5
    triesvar = "tries"
    while True:
        if tries <= 1:
            triesvar = "try"
        if tries == 0:
            print(f"{error_syntax('BadPassword', 'You have ran out of attempts. Exiting.')}")
            sys.exit(1)
        userpass = input(f"{warning_syntax('PasswordWarning', f'This shell is password protected. Please enter your password to continue. You have {tries} {triesvar}).')} > {fore.LIGHTBLUE_EX}")
        userpass = userpass.strip()
        if userpass == password:
            print(f"{fore.LIGHTGREEN_EX}Password accepted. Continuing...")
            break
        else:
            print(f"{fore.RED}Incorrect password.")
            tries -= 1

print(f"{fore.LIGHTGREEN_EX}Welcome to CopperShell!")
print()

# Main loop

while True:
    userinp = input(f"{fore.GREEN}{user}{fore.WHITE} | {fore.LIGHTBLUE_EX}{term_dir}{fore.WHITE} > ")
    if debug: print(f"DEBUG: userinp: {userinp}")
    userstrip = userinp.strip()
    if debug: print(f"DEBUG: userstrip: {userstrip}")
    usersplit = userstrip.split()
    if debug: print(f"DEBUG: usersplit: {usersplit}")
    if debug: print(f"DEBUG: usersplit[0]: {usersplit[0]}")
    
    if usersplit[0] in stdcommandset:
        sig = inspect.signature(stdcommandset[usersplit[0]])
        params = sig.parameters
        total_params = len(params)
        default_params = sum(1 for p in params.values() if p.default is not inspect.Parameter.empty)
        
        if len(usersplit) - 1 > total_params:
            print(f"{error_syntax('InvalidArguments', 'Too many arguments provided.')}")
            continue
        
        non_default_args_needed = total_params - default_params
        if len(usersplit) - 1 < non_default_args_needed:
            print(f"{error_syntax('InvalidArguments', 'Not enough arguments provided.')}")
            continue
        
        stdcommandset[usersplit[0]](*usersplit[1:])
    else:
        stdcommandset["invalid"]()