#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import openaps
from openaps import cli
from openaps import alias
import sys


class AliasApp(cli.ConfigApp):
    """ openaps-alias - manage aliases

    """

    name = "alias"

    def configure_parser(self, parser):
        self.read_config()
        self.configure_aliases()
        # available = devices.get_device_map(self.config)

    def configure_aliases(self):
        self.commands = alias.AliasManagement(parent=self)
        self.commands.configure_commands(self.parser)

    def prolog(self):
        super(AliasApp, self).prolog()

    def epilog(self):
        super(AliasApp, self).epilog()

    def run(self, args):
        # print(self.commands)
        app = self.commands.selected(args)
        output = app(args, self)


if __name__ == "__main__":

    app = AliasApp(None)
    app()
