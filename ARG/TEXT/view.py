import argparse
import os
import sys
import textwrap


import epic
import epicbots.legacy as legacy
import epicbots.textbot.textbrain as textbrain


class TextFace:

    r"""Define dir(textbot.textface) and help(textbot.textface)"""

    @epic.mainmethod
    @staticmethod
    def epic_text_paste(argv):

        r"""
        Epic Text Paste = Do more with Text's

        Usage: Epic Text Paste [-h] [-c] GREETING

        Positional arguments:

            GREETING    Chars to print

        Optional arguments:

            -h, --help      Show this help message and exit
            -c, --crash     Demo raising an unhandled exception

        Test: Epic Text Paste --help
        Test: Epic Text Paste
        Test: Epic Text Paste Wazzup
        Test: Epic Text Paste "What's up?"
        Test: Epic Text Paste --crash
        """

        parser = argparse.ArgumentParser(
            'Epic Text Paste',
            description=r"Epic Text Paste = Do more with Text's",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(r"""
                Test: Epic Text Paste --help
                Test: Epic Text Paste
                Test: Epic Text Paste Wazzup
                Test: Epic Text Paste "What's up?"
                Test: Epic Text Paste --crash
                """),
            )
        parser.add_argument('greetchars', metavar='GREETING', nargs='?', default='Look, Epic Text Paste was here.',
            help=r"Chars to print",
            )
        parser.add_argument('-c', '--crash', action='store_true',
            help=r"Demo raising an unhandled exception",
            )

        args = parser.parse_args(argv[1:])

        echoes = []
        if args.crash:
            echoes += ['--crash']
        echoes += ['"%s"' % args.greetchars]
        args.echo = ' '.join(echoes)

        print('info: Epic Text Paste: Got args as if: Epic Text Paste', args.echo)

        return textbrain.TextBrain.think_text_paste(args)


def def_textface_doctests():

    r"""
    Def TextFace Doctests

    >>> import epicbots.textbot.textface as textface
    >>>

    ###
    ### Doctests of Epic Text Paste
    ###

    >>> argv = ['Epic Text Paste', 'you can say that again']
    >>> textface.TextFace.epic_text_paste(argv)
    info: Epic Text Paste: Got args as if: Epic Text Paste "you can say that again"
    <BLANKLINE>
    info: Text Paste: you can say that again
    info: Text Paste: you can say that again
    info: Text Paste: you can say that again
    <BLANKLINE>
    >>>

    >>> argv = ['Epic Text Paste', '--crash']
    >>> textface.TextFace.epic_text_paste(argv)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Text Paste: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Text Face
    ###

    >>> type(textface.TextFace)
    <class 'type'>
    >>>

    """

