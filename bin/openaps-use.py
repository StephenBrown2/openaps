#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argparse
import sys

import argcomplete
import openaps
from openaps import cli, devices, uses
from openaps.reports import reporters
from openaps.reports.report import Report


class Output(reporters.Reporter):
    def __init__(self, args, formatter, task):
        ""
        self.task = task
        self.report = Report(
            name=self.__class__.__name__,
            reporter=args.format,
            device=args.device,
            use=args.use,
        )
        self.method = formatter
        self.output = args.output


class UseToolApp(cli.ConfigApp):
    """ openaps-use - use a registered device

  Once a device is registered in openaps.ini, it can be used.
    """

    name = "use"

    def configure_parser(self, parser):
        self.read_config()
        available = devices.get_device_map(self.config)
        self.devices = available
        self.reporters = reporters.get_reporter_map()
        choices = sorted(list(available.keys()))
        self.parser.add_argument(
            "--format", choices=list(self.reporters.keys()), default="json"
        )
        self.parser.add_argument("--output", type=argparse.FileType("w"), default="-")
        self.parser.add_argument(
            "--version",
            action="version",
            version="{} {}".format("%(prog)s", openaps.__version__),
        )

        self.configure_devices()

    def configure_devices(self):
        self.commands = uses.UseDeviceCommands(self.devices, parent=self)
        self.commands.configure_commands(self.parser)

    def prolog(self):
        super().prolog()

    def epilog(self):
        super().epilog()

    def run(self, args):
        # print(self.inputs)
        app = self.commands.selected(args)
        task = app.method.selected(args)
        reporter = Output(args, self.reporters.get(args.format), task)
        output = app(args, self)
        reporter(output)


if __name__ == "__main__":

    app = UseToolApp(None)
    app()
