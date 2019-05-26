#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""          _ _
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
import importlib.util as util

# thehive4py imports
from thehive4py.models import CaseTaskLog

# Local imports
from cells import config
from cells import shell

__author__ = "Matt Bromiley (@mbromileyDFIR)"
__license__ = "GNU Affero GPL3"
__version__ = "1.1 (Codename: Tsim Sha Tsui)"
__maintainer__ = "Matt Bromiley"
__status__ = "Production"

# Functions; note that the Cmd and Config functions are maintained in a separate file
def dat_ascii():
    '''Display pollen ASCII Art'''
    # Could potentially clean this up by making the pollen dust a variable
    print("""
             _ _            
 _ __ \x1b[1;33;40m*\x1b[0m ___ | | | ___ _ __  
| '_ \ / _ \| | |/ _ \ '_ \   \x1b[1;33;40m*\x1b[0m
| |_) | (_) | | |  __/ | | |
| .__/ \___/|_|_|\___|_| |_| \x1b[1;33;40m*\x1b[0m
|_|          \x1b[1;33;40m*\x1b[0m

Keeping the busy analysis bees busy!
""")

def cli_entry(entry=False, logfile=False):
    """Quick function to perform easy cmd insertions
    :param entry: Log entry to be inserted
    """
    task_id = config.get_config(config_format="cmdline")
    if not task_id:
        config.sneeze(error_message="Insert a log entry using the --log option, without an active case or task.",
                      error_fix="Run pollen with the --cmd option to set an active case and task.")
    if task_id:
        # Combine entry together
        entry = ' '.join(entry)
        # Logic to handle entries with or without file attachments
        if logfile:
            task_entry = CaseTaskLog(message=entry, file=str(logfile))
        else:
            task_entry = CaseTaskLog(message=entry)
        api = config.get_api()
        resp = api.create_task_log(task_id, task_entry)
        if resp.status_code == 201:
            print("Bzz Bzz Bzz...successfully inserted into task log. Happy analyzing!")

def check_config():
    """Quick function to check whether config is valid or not
    :return: whether config exists
    :rtype: boolean
    """
    # Very primitive but extremely crucial function
    # TODO: There's a lot of scenarios where config files are read; might distill these down
    config_check = configparser.ConfigParser()
    config_read = config_check.read('.pollen_config')
    if config_read:
        return True
    return False

def main():
    """Main Function. Includes argument parsing and config checker"""
    parser = argparse.ArgumentParser(prog="pollen.py",
                                     usage="%(prog)s [options]",
                                     add_help=False)
    # CLI Options
    group = parser.add_argument_group('CLI Options', 'CLI options for Pollen')
    group.add_argument("-c", "--cmd", help="Pollen Command-Line Module", action="store_true")
    group.add_argument("-l", "--log", help="Add log entry for configured case and task", nargs="+")
    group.add_argument("-lf", "--logfile", help="Attach a file to the corresponding log entry.")
    # Standard options override
    group = parser.add_argument_group('Standard Options')
    group.add_argument('-h', '--help', action="help", help="Show this help message and quit")
    # Display ascii art no matter what
    dat_ascii()
    # Much cleaner and more pythonic way to check if primary library exists
    if util.find_spec("thehive4py") is not None:
        args = parser.parse_args()
    else:
        print("Looks like you are missing TheHive4py! Please install it.")
        exit()

    # Testing to see if any options were provided
    if len(sys.argv) == 1:
        print("No options provided!\nTry running me with a -h option to see what I can do.")

    # Option to hop into cmdloop
    if args.cmd:
        if not check_config():
            shell.PollenCmd(config_present=False).cmdloop()
        shell.PollenCmd().cmdloop()
    # Option to insert log entry or log entry with a file
    if args.log:
        if args.logfile:
            cli_entry(entry=args.log, logfile=args.logfile)
        else:
            cli_entry(entry=args.log)
    # log files require log entries; the following ensures we have both
    if args.logfile and not args.log:
        config.sneeze(error_message="Upload a log file without a log entry",
                      error_fix="Retry your command with a -l or --log option")

if __name__ == "__main__":
    main()
