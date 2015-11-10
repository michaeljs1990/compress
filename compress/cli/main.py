"""
This is the entrypoint to the compress CLI. All argument
parsing is done in this file and then passed to the proper
command to carry out the required work.
"""
#!/usr/bin/env python
from docopt import docopt
from inspect import getdoc

from compress.generate import GenerateCommand
from compress.logger import Logger

class CompressCommand(object):
    """
    Generate docker compose files for complex environments.
    Usage:
        docker-compress <COMMAND> [--file-in FILE_IN]

    Options:
        --file-in        Specify an alternate compress file (default: docker-compress.yml)
        --verbose        Show debug output

    Commands:
        generate           Generate a new docker-compose.yml file
        version            Show the docker-compress version information
    """

    def __init__(self):
        doc = getdoc(self)
        arguments = docopt(doc)
        cmd = arguments.get('<COMMAND>')
        if cmd == "generate":
            gen_cmd = GenerateCommand(arguments)
            gen_cmd.run()
        if cmd == "version":
            print "0.2.0"

def main():
    """
    Script entrypoint as defined in setup.py
    """
    Logger.configure()
    CompressCommand()
