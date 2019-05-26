![Pollen Logo](files/pollen-logo-small.png)

# pollen: A command-line tool for interacting with TheHive

## Current Version: 1.1 (Codename: Tsim Sha Tsui)

[![GitHub issues](https://img.shields.io/github/issues/bromiley/pollen.svg?style=for-the-badge)](https://github.com/bromiley/pollen/issues)

---

Welcome to pollen, a command-line tool for interacting with TheHive!

[TheHive](https://thehive-project.org/) is a fantastic scalable, open-source Security IR Platform to help manage security incidents and investigations. I've used TheHive on multiple enagements and with multiple clients to help keep track of assignments, tasks, and findings on various investigations. However, up until now, much of the interaction with TheHive has been via the browser. 

Pollen allows for granular interaction with TheHive without needing to open the web browser. Current features include:

* Creating and interacting with cases
* Creating and interacting with tasks
* Storing task logs
* Storing task logs with file attachments
* Command-line log and log w/ file uploading

See something else you'd like to have? Drop me a note or submit an issue, and I'd be happy to check it out. Furthermore, if you are a user of TheHive and pollen helps make your life easier, I'd love to hear about how!

---

## Installation

pollen can be installed and run by simply cloning this repository, and running:

```bash
pip3 install -r requirements.txt
python3 pollen.py -c
```

If it's your first time running pollen, you should be prompted with the following:

```text
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

### [OPTIONAL]

Pollen also has some script features that can restart the script and autoload new settings. If you'd like to enable these, do a quick `chmod +x pollen.py`.

---

## Usage

For usage of pollen, check out the [wiki](https://github.com/bromiley/pollen/wiki).

---

## Changelog

### Version 1.1 - Codename: Tsim Sha Tsui [2019-05-26]

Updates:

* Added in the command-line `--log (-l)` and `--logfile (-lf)` capabilities that allow for direct CLI task logs and file uploads!
* Enhanced config options
* Pollen now has personalized color options available
* Cleaned up some syntax for better linting scorez.
* Better comments, documentation, and function usage.
* Better handling of the prompt, error messages, help menus, etc.
* Updated README
* Updated Wiki

### Version 1.0 - Codename: BBQ [2019-05-16]

Initial release! This version of pollen includes:

* Command shell capabilities to interact with TheHive
* Configuration options
* Case and task building
* Case and task selection
* Log and log w/ file upload options
