#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""          _ _
 _ __ * ___ | | | ___ _ __
| '_ \ / _ \| | |/ _ \ '_ \   *
| |_) | (_) | | |  __/ | | |
| .__/ \___/|_|_|\___|_| |_| *
|_|          *

Bringing you and TheHive closer together!
pollen - A tool to bridge the gap between your command line and TheHive

Pollen allows an analyst to insert case and task data directly from the
command-line, without needing to go back and forth between the browser.

Please use github.com/bromiley/pollen to track issues, releases, and other
project-related details.
"""

# Standard imports
import argparse
import sys
import configparser

# Test for thehive4api
try:
    from thehive4py.api import TheHiveApi
    from thehive4py.exceptions import TheHiveException
except ImportError:
    print("Looks like you are missing TheHive4py. Please install it (you can \
        use the requirements.txt file to help out).")

# Local Pollen imports
from cells import shell

__author__ = "Matt Bromiley (@mbromileyDFIR)"
__license__ = "GNU Affero GPL3"
__version__ = "1.0"
__maintainer__ = "Matt Bromiley"
__status__ = "Production"

# Functions; note that the Cmd functions are maintained in a separate file
def dat_ascii():
    '''Display pollen ASCII Art'''
    print("""
             _ _            
 _ __ * ___ | | | ___ _ __  
| '_ \ / _ \| | |/ _ \ '_ \   *
| |_) | (_) | | |  __/ | | |
| .__/ \___/|_|_|\___|_| |_| *
|_|          *

Keeping the busy analysis bees busy!
""")

def check_config():
    """Quick function to check whether config is valid or not"""
    config = configparser.ConfigParser()
    config_read = config.read('.pollen_config')
    if config_read:
        return True
    else:
        return False

def main():
    """Main Function. Includes argument parsing and config checker"""
    parser = argparse.ArgumentParser(prog="pollen.py",
                                     usage="%(prog)s [options]",
                                     add_help=False)
    # Main config options
    #group = parser.add_argument_group('Config Options', 'Configuration options for Pollen')
    #group.add_argument("--config", help="Configure pollen", action="store_true")
    #group.add_argument("--status", help="Pollen Status", action="store_true")
    # CLI Options
    group = parser.add_argument_group('CLI Options', 'CLI options for Pollen')
    group.add_argument("-c", "--cmd", help="Pollen Command-Line Module", action="store_true")
    #group.add_argument("-l", "--log", help="Add log entry for configured case and task", action="store_true")
    # Standard options override
    group = parser.add_argument_group('Standard Options')
    group.add_argument('-h', '--help', action="help", help="Show this help message and quit")

    args = parser.parse_args()

    # Testing to see if any options were provided
    if len(sys.argv) == 1:
        dat_ascii()
        print("No options provided!\nTry running me with a -h option to see what I can do.")

    # Option to hop into cmdloop
    if args.cmd:
        dat_ascii()
        if not check_config():
            shell.PollenCmd(config_present=False).cmdloop()
        shell.PollenCmd().cmdloop()

if __name__ == "__main__":
    main()
