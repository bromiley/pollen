# -*- coding: utf-8 -*-
'''Python module to contain cmd shells and associated functions'''

# standard imports
import cmd
import sqlite3
import sys
import os
import configparser

# thehive4py imports
from thehive4py.api import TheHiveApi
from thehive4py.exceptions import TheHiveException
from thehive4py.models import Case, CaseTask, CaseTaskLog

# local imports
from cells import config

class PollenCaseTaskCmd(cmd.Cmd):
    '''Case- and task-specific cmdloop'''
    def __init__(self, prompt, case_id, task_id):
        # Bring in case and task variables. case_id isn't needed right now, but keeping just in case
        self.prompt = prompt
        self.case_id = case_id
        self.task_id = task_id
        self.api = config.get_api()
        # Initialize
        super(PollenCaseTaskCmd, self).__init__()
    def do_log(self, arg):
        '''Insert a log entry for this task!'''
        print("Inserting the following log entry:\n\n{0}".format(arg))
        self.api.create_task_log(self.task_id, CaseTaskLog(message=arg))
    def do_logfile(self, arg):
        '''Insert a log file and a supporting file'''
        log_details = arg.split('&&')
        print("Inserting the following log entry:\n\n{0}\n\nAnd attaching the following file: {1}".format(log_details[0], log_details[1]))
        self.api.create_task_log(self.task_id, CaseTaskLog(message=log_details[0], file=log_details[1].lstrip()))
    def do_exit(self, arg):
        '''Exit back to the Case Pollen Shell'''
        return True
    def do_back(self, arg):
        '''Exit back to the Case Pollen Shell'''
        return True
    def do_clear(self, arg):
        '''Clear screen'''
        os.system('clear')

class PollenCaseCmd(cmd.Cmd):
    '''Case-specific cmdloop'''
    def __init__(self, prompt, case_id, case_name):
        self.prompt = prompt
        self.case_id = case_id
        self.case_name = case_name
        super(PollenCaseCmd, self).__init__()
    def do_newtask(self, arg):
        '''Create a new task within this case'''
        print("Let's create a new task within this case! The next few steps will request some data from you: ")
        nt_title = input("Task Title: ")
        nt_description = input("Task Description: ")
        nt = CaseTask(title=nt_title, description=nt_description)
        api = config.get_api()
        resp = api.create_case_task(self.case_id, nt)
        if resp.status_code == 201:
            print("Successfully created task {0} with the case {1}.".format(nt_title, self.case_name))
    def do_tasks(self, arg):
        '''List the tasks from this particular case'''
        print("***** Task Details for Case: {0} *****".format(self.case_name))
        task_list = config.get_tasks(self.case_id, format="name_list")
        print("\nThere are currently {0} tasks.".format(len(task_list)))
        if len(task_list) > 0:
            print("\nTask Details:")
            for task in task_list:
                print("\tTask Title: {0} | Status: {1}".format(task[0], task[1]))
    def do_take(self, arg):
        '''Take on a particular task'''
        print("Please select a task number to move to that task:\n# - Task Title")
        task_list = config.get_tasks(self.case_id, format="name_list", task_id=True)
        task_count = 0
        for task in task_list:
            print("{0} - {1}".format(task_count, task[0]))
            task_count += 1
        try:
            selected_task = int(input("Please select a value from 0-{0}. (Press Ctrl+C to exit) ".format(task_count-1)))
            if selected_task > task_count-1:
                print("\n{0} is not a valid number!! Please select a proper value\n".format(selected_task))
                self.do_take(None)
            PollenCaseTaskCmd(prompt='(pollen) (case: {0}) (task: {1}) '.format(self.case_name, task_list[selected_task][0]), case_id=self.case_id, task_id=task_list[selected_task][1]).cmdloop()
        except KeyboardInterrupt:
            pass
    def do_exit(self, arg):
        '''Exit back to the initial Pollen Shell'''
        return True
    def do_back(self, arg):
        '''Exit back to the initial Pollen Shell'''
        return True
    def do_clear(self, arg):
        '''Clear screen'''
        os.system('clear')

class PollenConfigCmd(cmd.Cmd):
    '''Sub-module to handle stats and TheHive configuration'''
    # Initialization; check for config file right at the beginning
    def __init__(self, prompt, config_found):
        self.prompt = prompt
        self.config_found = config_found
        self.configparser = configparser.ConfigParser()
        super(PollenConfigCmd, self).__init__()
        # If config is found, display current settings
        if not config_found:
            ans = input("Config file not found; would you like to create it now? (y/n): ")
            
            if ans.lower() == 'y':
                config.server_config()
            else:
                print("Unfortunately, I cannot do anything without a config\nExiting now...")
                sys.exit()
   
    def do_status(self, arg):
        ''' Print the current status '''
        server_details = config.get_config()
        print("Current TheHive Server: {0}\nCurrent TheHive API Key: {1}".format(server_details[0], server_details[1]))
        cases = config.get_cases(format="json_full", case_id=False)
        open_case_count = 0
        closed_case_count = 0
        for case in cases:
            if case['status'] == 'Open':
                open_case_count += 1
            else:
                closed_case_count +=1
        print("Case Stats: \n\t{0} Open Cases\n\t{1} Closed Cases".format(open_case_count, closed_case_count))

    def do_stats(self, arg):
        '''Same thing as status; displays current stats'''
        self.do_status(None)

    def do_reconfigure(self, arg):
        '''Reconfigure TheHive server and/or API details'''
        config.server_config()
    
    def do_exit(self, arg):
        '''Exit back to the Case Pollen Shell'''
        return True
    
    def do_back(self, arg):
        '''Exit back to the Case Pollen Shell'''
        return True

    def do_clear(self, arg):
        '''Clear screen'''
        os.system('clear')

class PollenCmd(cmd.Cmd):
    ''' Base Pollen Cmdloop '''
    def __init__(self, config_present=True):
        '''Init function to check for config and create prompt'''
        self.prompt = '(pollen) '
        self.config_present = config_present
        super(PollenCmd, self).__init__()
    
    def preloop(self):
        '''Preloop function to check for config file, and point user towards config'''
        if not self.config_present:
            PollenConfigCmd(prompt='(pollen:config) ', config_found=False).cmdloop()
    
    def do_newcase(self, arg):
        '''Create a new case within TheHive'''
        #Check if the config file exists first
        print("Let's create a new case! The next few steps will request some data from you. Hit Enter to accept any defaults: ")
        nc_title = input("Case Title: ")
        nc_description = input("Case Description: ")
        nc = Case(title=nc_title, description=nc_description)
        api = config.get_api()
        resp = api.create_case(nc)
        if resp.status_code == 201:
            print("Successfully created case {0}!".format(nc_title))
    
    def do_config(self, arg):
        '''Switch into TheHive config mode'''
        PollenConfigCmd(prompt='(pollen:config) ', config_found=True).cmdloop()
    
    def do_case(self, arg):
        '''Switch to a case'''
        #Check if the config file exists first
        cases = config.get_cases(format="name_list", case_id=True)
        print("There are {0} open cases:".format(len(cases)))
        case_count = 0
        for case in cases:
            print("{0} - {1}".format(case_count, case[0]))
            case_count += 1
        try:
            selected_case = int(input("Case selection (0-{0}) [Ctrl+C to exit]: ".format(case_count-1)))
            PollenCaseCmd(prompt='(pollen) (case: {0}) '.format(cases[selected_case][0]), case_id=cases[selected_case][1], case_name=cases[selected_case][0], ).cmdloop()
        except KeyboardInterrupt:
            pass

    def do_exit(self, arg):
        '''Exit the Pollen Shell'''
        return True

    def do_clear(self, arg):
        '''Clear screen'''
        os.system('clear')

if __name__ == "__main__":
    pass