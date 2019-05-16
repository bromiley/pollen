# -*- coding: utf-8 -*-
'''Python module to contain configuration functions'''

# standard imports
import configparser

# thehive4py imports
from thehive4py.api import TheHiveApi
from thehive4py.exceptions import TheHiveException

config = configparser.ConfigParser()

def test_api(server, apikey):
    """ Test API connectivity to TheHive
    :param server: Server IP address or URL
    :param apikey: API Key to connect to TheHive server
    :return: Connectivity status
    """
    test_api = TheHiveApi(server, apikey)
    try:
        test_api.find_first()
    except KeyError:
        print("WARNING: API Key failed\n")
        return False
    except TheHiveException:
        print("WARNING: Cannot reach hostname provided\n")
        return False
    return True

def server_config():
    ''' Collect TheHive server and API details, followed by a connectivity test '''
    hiveserver = input("\nPlease enter the address for TheHive server you want to connect to: ")
    hiveapi = input("Please enter the API key for that particular server: ")
    api_test = test_api(hiveserver, hiveapi)
    if not api_test:
        print("Uh-oh, something went wrong! Either I cannot reach the server or that API key doesn't work.")
        print("Can you double-check and run config again?")
    if api_test:
        print("\nSuccessfully connected to TheHive at {0} !!".format(hiveserver))
        config['TheHive'] = {'server_url' : hiveserver,
                             'server_api' : hiveapi}
        with open('.pollen_config', 'w') as configfile:
            config.write(configfile)

def get_config():
    config.read('.pollen_config')
    server_details = config['TheHive']
    return server_details['server_url'], server_details['server_api']

def get_api():
    server_details = get_config()
    api = TheHiveApi(server_details[0], server_details[1])
    return api

def get_cases(format, case_id=False):
    """Quick function to grab case names and provide to CLI
    :param format: The data format requested
    :param case_id: Whether to include the case_id in the output
    """
    api = get_api()
    case_list = []
    cases = api.find_cases().json()
    if format == "json_full":
        return cases
    if format == "name_list":
        for case in cases:
            if case['status'] == 'Open':
                if case_id:
                    case_list.append([case['title'], case['id']])
                else:
                    case_list.append(case['title'])
        return case_list

def get_tasks(case_id, format, task_id=False):
    """Quick function to grab task names and return to CLI
    Quick function to grab case names and provide to CLI
    :param case_id: TheHive case ID for the case of interest
    :param format: The data format requested
    :param task_id: Whether to include the case_id in the output
    """
    api = get_api()
    task_list = []
    tasks = api.get_case_tasks(case_id).json()
    if format == "json_full":
        return tasks
    if format == "name_list":
        for task in tasks:
            if task_id:
                task_list.append([task['title'], task['id']])
            else:
                task_list.append([task['title'], task['status']])
        return task_list
