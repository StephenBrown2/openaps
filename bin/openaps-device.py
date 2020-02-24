#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import sys, os, os.path
import argparse, argcomplete
import openaps

from openaps import cli
from openaps import devices


class ToolsApp(cli.ConfigApp):
    """
  openaps-device - Manage device configurations.

    show    - lists all known devices
    add     - add a new device
    remove  - remove a device
    """

    def configure_parser(self, parser):
        self.read_config()
        self.commands = devices.configure_commands(parser, parent=self)
        # parser.add_argument('name', default=None).completer = self.name_completer

    def name_completer(self, prefix, **kwargs):
        return []

    def run(self, args):
        # print(self.commands)
        self.selected = self.commands[args.command]
        self.commands[args.command](args, self)


if __name__ == "__main__":

    app = ToolsApp(None)
    app()
