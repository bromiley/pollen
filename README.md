![Pollen Logo](files/pollen-logo-small.png)

## pollen: A command-line tool for interacting with TheHive

Introducing pollen, a command-line tool for interacting with TheHive!

[TheHive](https://thehive-project.org/) is a fantastic scalable, open-source Security IR Platform to help manage security incidents and investigations. I've used TheHive on multiple enagements and with multiple clients to help keep track of assignments, tasks, and findings on various investigations. However, up until now, much of the interaction with TheHive has been via the browser. 

Seeing as I'm doing most of my work in the command-line, I wanted a tool that allowed me to stay within the terminal and quickly go from findings to notes and task logs. So, I built pollen!

Pollen allows for granular interaction with TheHive without needing to open the web browser. Current features include:

* Creating and interacting with cases
* Creating and interacting with tasks
* Storing task logs
* Storing task logs with file attachments

Shortly, I'll be adding in the following:

* Observable creation and retrieval
* Alert handling

See something else you'd like to have? Drop me a note or submit an issue, and I'd be happy to check it out. Furthermore, if you are a user of TheHive and pollen helps make your life easier, I'd love to hear about how!

## Installation

At the moment (2019-05-16), pollen only supports the command-line mode (additional features are arriving shortly). pollen can be installed and run by simply cloning this repository, and running the following:

```bash
pip3 install -r requirements.txt
python3 pollen.py -c
```

If it's your first time running pollen, you should be prompted with the following:

```
             _ _
 _ __ * ___ | | | ___ _ __
| '_ \ / _ \| | |/ _ \ '_ \   *
| |_) | (_) | | |  __/ | | |
| .__/ \___/|_|_|\___|_| |_| *
|_|          *

Keeping the busy analysis bees busy!

Config file not found; would you like to create it now? (y/n):
```

The script will walk you through setting up the config file. All you need is your Hive address and API key. And then, you're off to the races!

## Usage

For usage of pollen, check out the [wiki](https://github.com/bromiley/pollen/wiki).
