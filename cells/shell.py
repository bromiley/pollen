# -*- coding: utf-8 -*-
'''Python module to contain cmd shells and associated functions'''

# standard imports
import cmd
import sys
import os
import configparser

# thehive4py import(s)
from thehive4py.models import Case, CaseTask, CaseTaskLog

# local imports
from cells import config

class PollenCaseTaskCmd(cmd.Cmd):
    '''Case- and task-specific cmdloop'''
    def __init__(self, prompt, case_id, task_id):
        '''Class initialization'''
        # Bring in case and task variables. case_id isn't needed right now, but keeping just in case
        self.prompt = prompt
        self.case_id = case_id
        self.task_id = task_id
        self.api = config.get_api()
        self.doc_header = '\x1b[1mDocumented pollen commands for the task shell. Type \'help <command>\' for context.\x1b[0m'
        # Initialize
        super(PollenCaseTaskCmd, self).__init__()
    def do_log(self, arg):
        '''Insert a log entry for this task!'''
        print("Inserting the following log entry:\n\n{0}".format(arg))
        self.api.create_task_log(self.task_id, CaseTaskLog(message=arg))
    def do_logfile(self, arg):
        '''Insert a log file and a supporting file'''
        log_details = arg.split('&&')
        print("Inserting the following log entry:\n\n{0}\n\nAnd attaching the following file: {1}"
              .format(log_details[0], log_details[1]))
        self.api.create_task_log(self.task_id, CaseTaskLog(message=log_details[0],
                                                           file=log_details[1].lstrip()))
    def do_exit(self, *_):
        '''Exit back to the Case Pollen Shell'''
        return True
    def do_back(self, *_):
        '''Exit back to the Case Pollen Shell'''
        return True
    def do_clear(self, *_):
        '''Clear screen'''
        os.system('clear')

class PollenCaseCmd(cmd.Cmd):
    '''Case-specific cmdloop'''
    def __init__(self, prompt, case_id, case_name):
        '''Class initialization'''
        self.prompt = prompt
        self.case_id = case_id
        self.case_name = case_name
        self.doc_header = '\x1b[1mDocumented pollen commands for the case shell. Type \'help <command>\' for context.\x1b[0m'
        self.intro = '\nWelcome to the pollen case menu. Please type \x1b[1mhelp\x1b[0m to see what you can do here' 
        super(PollenCaseCmd, self).__init__()
    def do_newtask(self, *_):
        '''Create a new task within this case'''
        print("Let's create a new task within this case! The next few steps \
              will request some data from you: ")
        nt_title = input("Task Title: ")
        nt_description = input("Task Description: ")
        new_task = CaseTask(title=nt_title, description=nt_description)
        api = config.get_api()
        resp = api.create_case_task(self.case_id, new_task)
        if resp.status_code == 201:
            print("Successfully created task {0} with the case {1}.".format(nt_title,
                                                                            self.case_name))
    def do_tasks(self, *_):
        '''List the tasks from this particular case'''
        print("***** Task Details for Case: {0} *****".format(self.case_name))
        task_list = config.get_tasks(self.case_id, output_format="name_list")
        print("\nThere are currently {0} tasks.".format(len(task_list)))
        if task_list:
            print("\nTask Details:")
            for task in task_list:
                print("\tTask Title: {0} | Status: {1}".format(task[0], task[1]))
    def do_take(self, *_):
        '''Take on a particular task'''
        print("Please select a number to move to that task:\n# - Task Title")
        task_list = config.get_tasks(self.case_id, output_format="name_list", task_id=True)
        task_count = 0
        for task in task_list:
            print("{0} - {1}".format(task_count, task[0]))
            task_count += 1
        try:
            selected_task = int(input("Please select a value from 0-{0}. (Press Ctrl+C to exit) "
                                      .format(task_count-1)))
            if selected_task > task_count-1:
                print("\n{0} is not a valid number!! Please select a proper value\n"
                      .format(selected_task))
                self.do_take(None)
            PollenCaseTaskCmd(prompt=config.prompt_handler(which_prompt="task",
                                                           case=self.case_name,
                                                           task=task_list[selected_task][0]),
                              case_id=self.case_id,
                              task_id=task_list[selected_task][1]).cmdloop()
        except KeyboardInterrupt:
            pass
    def do_exit(self, *_):
        '''Exit back to the initial Pollen Shell'''
        return True
    def do_back(self, *_):
        '''Exit back to the initial Pollen Shell'''
        return True
    def do_clear(self, *_):
        '''Clear screen'''
        os.system('clear')

class PollenConfigCmd(cmd.Cmd):
    '''Sub-module to handle stats and TheHive configuration'''
    # Initialization; check for config file right at the beginning
    def __init__(self, prompt, config_found):
        '''Class initialization'''
        self.prompt = prompt
        self.config_found = config_found
        self.configparser = configparser.ConfigParser()
        self.doc_header = '\x1b[1mDocumented pollen config commands. Type \'help <command>\' for context.\x1b[0m'
        self.intro = 'Welcome to the pollen configuration menu. Please type \x1b[1mhelp\x1b[0m to see what you can do here' 
        super(PollenConfigCmd, self).__init__()
        # If config is found, display current settings
        if not config_found:
            ans = input("Config file not found; would you like to create it now? (y/n): ")
            if ans.lower() == 'y':
                config.server_config()
            else:
                print("Unfortunately, I cannot do anything without a config\nExiting now...")
                sys.exit()
    def do_cmdline(self, *_):
        '''Set the command-line case and task options'''
        # Start with case enumeration and selection
        print("Let's set predefined case details for the --log and --logfile options")
        case_list = config.get_cases(output_format="name_list", case_id=True)
        print("There are {0} open cases. Please select a number to move to that case:\n# - Case Title".format(len(case_list)))
        dracula = 0
        for case in case_list:
            print("{0} - {1}".format(dracula, case[0]))
            dracula += 1
        try:
            case_no = int(input("Case selection (0-{0}) (Press Ctrl+C to exit): "
                                .format(dracula-1)))
        except KeyboardInterrupt:
            pass
        selected_case_name = case_list[case_no][0]
        selected_case_id = case_list[case_no][1]
        # With case id selected, let's enumerate and select tasks
        print("\nNext, set predefined task details for the --log and --logfile options")
        task_list = config.get_tasks(selected_case_id, output_format="name_list", task_id=True)
        dracula = 0
        for task in task_list:
            print("{0} - {1}".format(dracula, task[0]))
            dracula += 1
        try:
            task_no = int(input("Please select a value from 0-{0}. (Press Ctrl+C to exit) "
                                .format(dracula-1)))
        except KeyboardInterrupt:
            pass
        selected_task_name = task_list[task_no][0]
        selected_task_id = task_list[task_no][1]
        self.configparser.read('.pollen_config')
        self.configparser.set('TheHive', 'case_name', selected_case_name)
        self.configparser.set('TheHive', 'case_id', selected_case_id)
        self.configparser.set('TheHive', 'task_name', selected_task_name)
        self.configparser.set('TheHive', 'task_id', selected_task_id)
        with open('.pollen_config', 'w') as configfile:
            self.configparser.write(configfile)

    def do_status(self, *_):
        '''Print the current status'''
        server_details = config.get_config(config_format="basic")
        print("\x1b[1m***** Pollen Configuration *****\x1b[0m")
        print("Current TheHive Configuration Details:")
        print("\tServer Address: {0}\n\tAPI Key: {1}"
              .format(server_details[0], server_details[1]))
        if len(server_details) == 4:
            print("\n\x1b[1mQuick insert command-line details:\x1b[0m")
            print("\tPre-configured case: {0}".format(server_details[2]))
            print("\tPre-configured task: {0}".format(server_details[3]))
        cases = config.get_cases(output_format="json_full", case_id=False)
        open_case_count = 0
        closed_case_count = 0
        for case in cases:
            if case['status'] == 'Open':
                open_case_count += 1
            else:
                closed_case_count += 1
        print("\n\x1b[1mCase Stats:\x1b[0m \n\t{0} Open Cases\n\t{1} Closed Cases"
              .format(open_case_count, closed_case_count))
    def do_stats(self, *_):
        '''Same thing as status; displays current stats'''
        self.do_status(None)
    def do_setserver(self, *_):
        '''Reconfigure TheHive server and/or API details'''
        config.server_config()
    def do_color(self, *_):
        '''Configure pollen terminal colors'''
        config.color_config()
    def do_exit(self, *_):
        '''Exit back to the default Pollen Shell'''
        return True
    def do_back(self, *_):
        '''Exit back to the default Pollen Shell'''
        return True
    def do_clear(self, *_):
        '''Clear screen'''
        os.system('clear')

class PollenCmd(cmd.Cmd):
    '''Base Pollen Cmdloop'''
    def __init__(self, config_present=True):
        '''Class initialization'''
        self.prompt = config.prompt_handler()
        self.config_present = config_present
        self.doc_header = '\x1b[1mDocumented pollen commands\x1b[0m'
        super(PollenCmd, self).__init__()
    def preloop(self):
        '''Preloop function to check for config file, and point user towards config'''
        if not self.config_present:
            PollenConfigCmd(prompt=config.prompt_handler(which_prompt="config"),
                            config_found=False).cmdloop()
    def do_newcase(self, *_):
        '''Create a new case within TheHive'''
        print("Let's create a new case! The next few steps will request some data from you.")
        nc_title = input("Case Title: ")
        nc_description = input("Case Description: ")
        new_case = Case(title=nc_title, description=nc_description)
        api = config.get_api()
        resp = api.create_case(new_case)
        if resp.status_code == 201:
            print("Successfully created case {0}!".format(nc_title))
    def do_config(self, *_):
        '''Switch into TheHive config mode'''
        PollenConfigCmd(prompt=config.prompt_handler(which_prompt="config"),
                        config_found=True).cmdloop()
    def do_case(self, *_):
        '''Switch to a case'''
        cases = config.get_cases(output_format="name_list", case_id=True)
        print("There are {0} open cases. Please select a number to move to that case:\n# - Case Title".format(len(cases)))
        case_count = 0
        for case in cases:
            print("{0} - {1}".format(case_count, case[0]))
            case_count += 1
        try:
            selected_case = int(input("Case selection (0-{0}) (Press Ctrl+C to exit): "
                                      .format(case_count-1)))
            PollenCaseCmd(prompt=config.prompt_handler(which_prompt="case", 
                                                       case=cases[selected_case][0]),
                          case_id=cases[selected_case][1],
                          case_name=cases[selected_case][0]).cmdloop()
        except KeyboardInterrupt:
            pass
    def do_exit(self, *_):
        '''Exit the Pollen Shell'''
        return True
    def do_clear(self, *_):
        '''Clear screen'''
        os.system('clear')

if __name__ == "__main__":
    pass
