# -*- coding: utf-8 -*-
import os
import os.path

import click

from .conf import GandiContextHelper


class GandiCLI(click.Group):
    """ Gandi command line utility."""

    def __init__(self, help=None):

        def set_debug(ctx, value):
            ctx.obj['verbose'] = value

        click.Group.__init__(self, help=help, params=[
            click.Option(['-v', '--verbose'],
                         help='Enable or disable verbose mode.',
                         is_flag=True,
                         default=False, callback=set_debug)
        ])

    def load_commands(self):
        """ Load cli commands from submodule """
        command_folder = os.path.join(os.path.dirname(__file__), '../commands')
        # print command_folder
        for filename in os.listdir(command_folder):
            if filename.endswith('.py') and '__init__' not in filename:
                submod = filename[:-3]
                module_name = 'gandi.cli.commands.' + submod
                # print module_name
                __import__(module_name, fromlist=[module_name])

    def invoke(self, ctx):
        ctx.obj = GandiContextHelper(verbose=ctx.obj['verbose'])
        click.Group.invoke(self, ctx)