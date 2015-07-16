import argparse
import os
import sys
import textwrap


import epic
import epicbots.legacy as legacy
import epicbots.argbot.argbrain as argbrain
import epicbots.argbot.argmuscle as argmuscle


class ArgFace:

    r"""Define dir(argbot.argface) and help(argbot.argface)"""

    @epic.mainmethod
    @staticmethod
    def epic_arg_debug(argv):

        r"""
        Epic Arg Debug = Trace the Arg Bot compiling Help Lines

        Usage: Epic Arg Debug [-p|-d|-a] [WORD [WORD ...]]

        Positional arguments:

            WORD    A word of command

        Optional arguments:

            -h, --help  Show this help message and exit

            -a, --args  Print the Parsed Args
            -p, --py    Print the Python of a Command Line Parser
            -d, --doc   Print more conventional Help Lines

        Test: Epic Arg Debug --help
        Test: Epic Arg Debug --py epic arg regress
        Test: Epic Arg Debug --py epic arg debug
        Test: Epic Arg Debug --doc epic arg debug
        Test: Epic Arg Debug --args -- epic arg debug --args

        Note: Default to print these help lines, if none of (-p|-d|-a) chosen.
        """

        parser = argparse.ArgumentParser(
            'Epic Arg Debug',
            description=r"Epic Arg Debug = Trace the work of the Arg Bot",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(r"""
                Test: Epic Arg Debug --help
                Test: Epic Arg Debug --py epic arg regress
                Test: Epic Arg Debug --py epic arg debug
                Test: Epic Arg Debug --doc epic arg debug
                Test: Epic Arg Debug --args epic arg debug

                Note: Default to print these help lines, if none of (-p|-d|-a) chosen.
                """),
            )

        outparser = parser.add_mutually_exclusive_group()
        if True:
            outparser.add_argument('-a', '--args', action='store_true',
                help=r"Print the Parsed Args",
                )
            outparser.add_argument('-p', '--py', action='store_true',
                help=r"Print the Python of a Command Line Parser",
                )
            outparser.add_argument('-d', '--doc', action='store_true',
                help=r"Print more conventional Help Lines",
                )

        parser.add_argument('words', metavar='WORD', nargs='*',
            help=r"A word of command",
            )

#       args = argmuscle.ArgMuscle.parse_args_per_doc() # PL FIXME

        args = parser.parse_args(argv[1:])

        args.help = None
        if not (args.py or args.doc or args.args):
            args.help = True

        echoes = []
        if args.py:
            echoes += ['--py']
        if args.doc:
            echoes += ['--doc']
        if args.args:
            echoes += ['--args']
        echoes += [(('"%s"' % word) if (' ' in word) else word) for word in args.words]
        args.echo = ' '.join(echoes)

        args.verb = 'Epic Arg Debug'

        if args.help:
            parser.print_help()
            sys.exit()

        argbrain.ArgBrain.arg_debug(args)

