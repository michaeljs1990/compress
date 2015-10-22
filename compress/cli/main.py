#!/usr/bin/env python
from docopt import docopt
from inspect import getdoc

from ..generate import GenerateCommand

def main():
    command = CompressCommand()
    command.run()

class CompressCommand():
    """
    Generate docker compose files for complex environments.
    Usage:
      docker-compress generate [--file-out FILE_OUT]
      docker-compress version
    Options:
      -f, --file FILE           Specify an alternate compress file (default: docker-compress.yml)
      --verbose                 Show more output
      -v, --version             Print version and exit
    Commands:
      generate           Generate a new docker-compose.yml file
      version            Show the Docker-Compose version information
    """

    def run(self):
        doc = getdoc(self)
        arguments = docopt(doc)
        generate = arguments.get('generate')
        if generate:
            genCmd = GenerateCommand(arguments)
            genCmd.run()
