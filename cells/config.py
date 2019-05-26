# -*- coding: utf-8 -*-
'''Python module to contain configuration functions'''

# standard imports
import configparser
import os
import sys
import time

# thehive4py imports
from thehive4py.api import TheHiveApi
from thehive4py.exceptions import TheHiveException

CONFIG = configparser.ConfigParser()

# Function to handle and standardize pollen errors. This simple function allows for potential error
# messages and fixes to declared at the function level, allowing for better handling.
def sneeze(error_message, error_fix):
    """Simple function to standardize and print error messages
    :param error_message: The error message to display
    :param error_fix: The suggested fix for the error message
    :return: Printed lines with error message, fix, and script exit
    """
    print("**** ACHOO! POLLEN ERROR ****")
    print("You tried to: \x1b[1m{0}\x1b[0m\n".format(error_message))
    print("To resolve this error, please: {0}".format(error_fix))

# Function to restart script when changes are made, such as colors to terminal. 
# Note that this does require a 'chmod +x' on the script; described in error message
def restart_script():
    """Simple function to restart pollen and return to cmdshell
    :raises PermissionError: If the script has not be chmod +x
    """
    try:
        os.execl('./pollen.py', *sys.argv)
        # If script is not executable, error will be thrown
    except PermissionError:
        print("pollen cannot automatically restart; please manually restart the script.")
        print("You can have pollen auto-restart after config changes by setting chmod +x")
        exit()

# Function to handle prompts between the various shells
# I might move this to a separate formatting module soon, given the amount of formatting here
def prompt_handler(which_prompt=False, **kwargs):
    """Prompt Color Changer (this may facilitate additional features in the future)
    :param which_prompt: What type of prompt is being requested
    :type which_prompt: string or boolean
    :return: prompt with coloration
    :rtype: string
    :raises KeyError: if a color has not been defined (error is handled by function logic)
    """
    # Read config file and assign terminal_color
    CONFIG.read('.pollen_config')
    # Test for personalization first
    try:
        if CONFIG['Personalization']:
            term_color = CONFIG['Personalization']['term_color']
            label_color = CONFIG['Personalization']['label_color']
    # If no personalization options have been set, set to default terminal colors
    except KeyError:
        term_color = '\x1b[0m'
        label_color = '\x1b[0m'
    # If which_prompt exists, issue the correct response
    if which_prompt:
        if which_prompt == "config":
            return '{0}(pollen:{1}config)\x1b[0m '.format(term_color, label_color)
        if which_prompt == "case":
            case = kwargs.get('case')
            return '{0}(pollen) {1}case:{0}{2}\x1b[0m '.format(term_color, label_color, case)
        if which_prompt == "task":
            case = kwargs.get('case')
            task = kwargs.get('task')
            return "{0}(pollen) {1}case:{0}{2} {1}task:{0}{3}\x1b[0m ".format(term_color, label_color, case, task)
    # If which_prompt is False, this means it is the default pollen prompt
    return '{0}(pollen)\x1b[0m '.format(term_color)

def test_api(server, apikey):
    """Test API connectivity to TheHive
    :param server: Server IP address or URL
    :param apikey: API Key to connect to TheHive server
    :return: Connectivity status
    :rtype: boolean
    """
    # Basic API call; this happens quite frequently throughout the script, and was easier to model here.
    api_test = TheHiveApi(server, apikey)
    try:
        api_test.find_first()
    # TODO: Let's see if we can make this more TheHive exception specific
    except KeyError:
        print("WARNING: API Key failed\n")
        return False
    except TheHiveException:
        print("WARNING: Cannot reach hostname provided\n")
        return False
    return True

def server_config():
    """Collect TheHive server and API details, followed by a connectivity test. Users will now \
        also be asked if they want to store cmd-line options
    """
    hiveserver = input("\nPlease enter the address for TheHive server you want to connect to: ")
    hiveapi = input("Please enter the API key for that particular server: ")
    api_test = test_api(hiveserver, hiveapi)
    # First potential error using pollen; incorrect server and API details
    if not api_test:
        print("Uh-oh, something went wrong! Either I cannot reach the server or \
            that API key doesn't work.")
        print("Can you double-check and run config again?")
    # Check 
    if api_test:
        print("\nSuccessfully connected to TheHive at {0} !!".format(hiveserver))
        cmdline_choice = input("Would you like to configure an active case and task for \
                                quick cmdline usage? (Y/N) ")
        # TODO: There's a lot more y/n questions in this script than originally intended;
        # Move these to a function
        if not (cmdline_choice.lower() == "y" or cmdline_choice.lower() == "n"):
            print("Please enter a valid choice (Y/N)!")
        if cmdline_choice.lower() == "n":
            CONFIG['TheHive'] = {'server_url' : hiveserver, 'server_api' : hiveapi}
        if cmdline_choice.lower() == "y":
            pass
        with open('.pollen_config', 'a+') as configfile:
            CONFIG.write(configfile)

def color_config():
    """Allow the analyst to set some custom color schemes for pollen"""
    # KISS; nothing fancy.
    color_list = [
        ["Black", "\x1b[1;30;40m"],
        ["Red", "\x1b[1;31;40m"],
        ["Green", "\x1b[1;32;40m"],
        ["Yellow", "\x1b[1;33;40m"],
        ["Blue", "\x1b[1;34;40m"],
        ["Magenta", "\x1b[1;35;40m"],
        ["Cyan", "\x1b[1;36;40m"],
        ["White", "\x1b[1;37;40m"],
        ["Terminal Default", "\x1b[0m"]
    ]
    CONFIG.read('.pollen_config')
    i = 0
    # The following while statement allows the color selector to repeat if user tries silly input
    while True:
        for color_name, color_code in color_list:
            print('{0} - {1}{2}\x1b[0m'.format(i, color_code, color_name))
            i += 1
        try:
            term_color = int(input("Please select from one of the following to change your pollen " \
                                   "shell color [0-{0}]: ".format(len(color_list)-1)))
        except ValueError:
            print("Please enter a valid integer!")
            break
        try:
            label_color = int(input("Please select from one of the following to change your pollen item color [0-{0}]: "
                                    .format(len(color_list)-1)))
        except ValueError:
            print("Please enter a valid integer!")
            break
        print("\x1b[1mYour shell will look like this:\x1b[0m {0}(pollen) {1}case: {0}case_name {1}task: {0}task_name\x1b[0m"
              .format(color_list[term_color][1], color_list[label_color][1]))
        color_selection = input("Please confirm this color combination [y/n]: ")
        if not (color_selection.lower() == "y" or color_selection.lower() == "n"):
            print("Please enter a valid selection!")
        if color_selection.lower() == "n":
            i = 0
            return False
        # As long as we have sufficient values, label and term colors are set, and the script restarts itself.
        if color_selection.lower() == "y":
            # Ignore error if Personalization exists, which means we are simply updating colors
            try:
                CONFIG.add_section("Personalization")
            except configparser.DuplicateSectionError:
                pass
            CONFIG.set("Personalization", "term_color", color_list[term_color][1])
            CONFIG.set("Personalization", "label_color", color_list[label_color][1])
            with open('.pollen_config', 'w') as configfile:
                CONFIG.write(configfile)
            print("Restarting pollen in 2 seconds...")
            time.sleep(2)
            # Quick reminder that the following does depend on 'chmod +x'
            restart_script()

def get_config(config_format):
    """Import config settings. Dropping in logic to check for cmdline options or not
    :param config_format: Variable to determine what type of format should be returned
    :type cmdline: string
    :return: TheHive configuration details
    :rtype: list
    :raises KeyError: If TheHive server is reachable/exists (error is handled by function logic)
    """
    CONFIG.read('.pollen_config')
    hive_details = CONFIG['TheHive']
    if config_format == "cmdline":
        try:
            if CONFIG['TheHive']['case_id']:
                return str(hive_details['task_id'])
        except KeyError:
            return False
    if config_format == "basic":
        try:
            if hive_details['case_name']:
                return hive_details['server_url'], hive_details['server_api'], hive_details['case_name'], hive_details['task_name']
        except KeyError:
            return hive_details['server_url'], hive_details['server_api']

def get_api():
    """Establish API
    :return: thehive api connector
    :rtype: TheHiveApi
    """
    server_details = get_config(config_format="basic")
    api = TheHiveApi(server_details[0], server_details[1])
    return api

def get_cases(output_format, case_id=False):
    """Quick function to grab case names and provide to CLI
    :param output_format: The data format requested
    :type output_format: string
    :param case_id: Whether to include the case_id in the output
    :type case_id: boolean
    :return: thehive case list in a specified format
    :rtype: list
    """
    # TODO: Might rework this to be more config friendly
    api = get_api()
    case_list = []
    cases = api.find_cases().json()
    if output_format == "json_full":
        return cases
    if output_format == "name_list":
        for case in cases:
            if case['status'] == 'Open':
                if case_id:
                    case_list.append([case['title'], case['id']])
                else:
                    case_list.append(case['title'])
        return case_list

def get_tasks(case_id, output_format, task_id=False):
    """Quick function to grab task names and return to CLI
    :param case_id: TheHive case ID for the case of interest
    :type case_id: string
    :param output_format: The data format requested
    :type output_format: string
    :param task_id: Whether to include the case_id in the output
    :type task_id: boolean
    :return: thehive task list in a specified format
    :rtype: list
    """
    # TODO: Might rework this to be more config friendly
    api = get_api()
    task_list = []
    tasks = api.get_case_tasks(case_id).json()
    if output_format == "json_full":
        return tasks
    if output_format == "name_list":
        for task in tasks:
            if task_id:
                task_list.append([task['title'], task['id']])
            else:
                task_list.append([task['title'], task['status']])
        return task_list
