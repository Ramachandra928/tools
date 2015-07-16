import argparse
import os
import platform
import re
import sys
import textwrap


import epic
import epicbots.legacy as legacy
import epicbots.svnbot.svnbrain as svnbrain


class SvnFace:

    r"""Define dir(svnbot.svnface) and help(svnbot.svnface)"""

    @epic.mainmethod
    @staticmethod
    def epic_svn(argv):

        r"""
        Epic Svn ... = Do more with Svn's

        Usage: Epic Svn ... [-h] [-c] GREETING

        Positional arguments:

            GREETING    Chars to print

        Optional arguments:

            -h, --help      Show this help message and exit
            -c, --crash     Demo raising an unhandled exception

        Test: Epic Svn ... --help
        Test: Epic Svn ...
        Test: Epic Svn ... Wazzup
        Test: Epic Svn ... "What's up?"
        Test: Epic Svn ... --crash
        """

        parser = argparse.ArgumentParser(
            'Epic Svn ...',
            description=r"Epic Svn ... = Do more with Svn's",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(r"""
                Test: Epic Svn ... --help
                Test: Epic Svn ...
                Test: Epic Svn ... Wazzup
                Test: Epic Svn ... "What's up?"
                Test: Epic Svn ... --crash
                """),
            )
        parser.add_argument('greetchars', metavar='GREETING', nargs='?', default='Look, Epic Svn ... was here.',
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

        print('info: Epic Svn ...: Got args as if: Epic Svn ...', args.echo)

        return svnbrain.SvnBrain.think_svn(args)

    @epic.mainmethod
    @staticmethod
    def epic_svn_backup(argv):

        r"""
        Epic Svn Backup = Do more with Svn's

        Usage: Epic Svn Backup [-h] [-c] GREETING

        Positional arguments:

            GREETING    Chars to print

        Optional arguments:

            -h, --help      Show this help message and exit
            -c, --crash     Demo raising an unhandled exception

        Test: Epic Svn Backup --help
        Test: Epic Svn Backup
        Test: Epic Svn Backup Wazzup
        Test: Epic Svn Backup "What's up?"
        Test: Epic Svn Backup --crash
        """

        parser = argparse.ArgumentParser(
            'Epic Svn Backup',
            description=r"Epic Svn Backup = Do more with Svn's",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(r"""
                Test: Epic Svn Backup --help
                Test: Epic Svn Backup
                Test: Epic Svn Backup Wazzup
                Test: Epic Svn Backup "What's up?"
                Test: Epic Svn Backup --crash
                """),
            )
        parser.add_argument('greetchars', metavar='GREETING', nargs='?', default='Look, Epic Svn Backup was here.',
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

        print('info: Epic Svn Backup: Got args as if: Epic Svn Backup', args.echo)

        return svnbrain.SvnBrain.think_svn_backup(args)

    @epic.mainmethod
    @staticmethod
    def epic_svn_clean(argv):

        r"""
        Epic Svn Clean = Do more with Svn's

        Usage: Epic Svn Clean [-h] [-c] GREETING

        Positional arguments:

            GREETING    Chars to print

        Optional arguments:

            -h, --help      Show this help message and exit
            -c, --crash     Demo raising an unhandled exception

        Test: Epic Svn Clean --help
        Test: Epic Svn Clean
        Test: Epic Svn Clean Wazzup
        Test: Epic Svn Clean "What's up?"
        Test: Epic Svn Clean --crash
        """

        parser = argparse.ArgumentParser(
            'Epic Svn Clean',
            description=r"Epic Svn Clean = Do more with Svn's",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(r"""
                Test: Epic Svn Clean --help
                Test: Epic Svn Clean
                Test: Epic Svn Clean Wazzup
                Test: Epic Svn Clean "What's up?"
                Test: Epic Svn Clean --crash
                """),
            )
        parser.add_argument('greetchars', metavar='GREETING', nargs='?', default='Look, Epic Svn Clean was here.',
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

        print('info: Epic Svn Clean: Got args as if: Epic Svn Clean', args.echo)

        return svnbrain.SvnBrain.think_svn_clean(args)

    @epic.mainmethod
    @staticmethod
    def epic_svn_getlog(argv):

        r"""
        Epic Svn GetLog = Pull a Txt file of the Svn Log entries from BRANCH since FROMREV

        See also: Epic Svn Get Log --help
        """

        parser = argparse.ArgumentParser('Epic Svn GetLog',
            description=r"Pull a Txt file of the Svn Log entries from BRANCH since FROMREV",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(r"""
                Test: Epic Svn GetLog https://svnsdus.sandisk.com/svn/HEMi2/branch/T3Bx 10799 --to 10950
                Test: Epic Svn GetLog --xml https://svnsdus.sandisk.com/svn/HEMi2/branch/T3Bx 10799 --to 10950
                """),
            )
        parser.add_argument('branch', metavar='BRANCH', help='Svn Branch')
        parser.add_argument('from_rev', metavar='FROMREV', help='First log rev to download')
        parser.add_argument('-t', '--to', dest='to_rev', metavar='TOREV', default=None, help='Last log rev to download (else stop with Head rev)')
        parser.add_argument('-x', '--xml', action='store_true', default=False, help='Pull Xml instead of Txt')

        parsed_args = parser.parse_args(argv[1:])

        filename = svnmuscle.SvnMuscle.get_log(
            parsed_args.branch,
            parsed_args.from_rev,
            parsed_args.to_rev,
            xml=parsed_args.xml,
            )

        if filename is not None:
            print('\nSuccess!!!\nTo view the log:', 'start', 'iexplore', filename)
            return
        sys.exit(['\nFailure!!!\nSeems the Svnbot could not find either the url or the version\nYou are more than welcome to try again'])

    @epic.mainmethod
    @staticmethod
    def epic_svn_hi(argv):

        r"""
        Epic Svn Hi = Do more with Svn's

        Usage: Epic Svn Hi [-h] [-c] GREETING

        Positional arguments:

            GREETING    Chars to print

        Optional arguments:

            -h, --help      Show this help message and exit
            -c, --crash     Demo raising an unhandled exception

        Test: Epic Svn Hi --help
        Test: Epic Svn Hi
        Test: Epic Svn Hi Wazzup
        Test: Epic Svn Hi "What's up?"
        Test: Epic Svn Hi --crash
        """

        parser = argparse.ArgumentParser(
            'Epic Svn Hi',
            description=r"Epic Svn Hi = Do more with Svn's",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(r"""
                Test: Epic Svn Hi --help
                Test: Epic Svn Hi
                Test: Epic Svn Hi Wazzup
                Test: Epic Svn Hi "What's up?"
                Test: Epic Svn Hi --crash
                """),
            )
        parser.add_argument('greetchars', metavar='GREETING', nargs='?', default='Look, Epic Svn Hi was here.',
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

        print('info: Epic Svn Hi: Got args as if: Epic Svn Hi', args.echo)

        return svnbrain.SvnBrain.think_svn_hi(args)

    @epic.mainmethod
    @staticmethod
    def epic_svn_log(argv):

        r"""
        Epic Svn Log = Do more with Svn's

        Usage: Epic Svn Log [-h] [-c] GREETING

        Positional arguments:

            GREETING    Chars to print

        Optional arguments:

            -h, --help      Show this help message and exit
            -c, --crash     Demo raising an unhandled exception

        Test: Epic Svn Log --help
        Test: Epic Svn Log
        Test: Epic Svn Log Wazzup
        Test: Epic Svn Log "What's up?"
        Test: Epic Svn Log --crash
        """

        parser = argparse.ArgumentParser(
            'Epic Svn Log',
            description=r"Epic Svn Log = Do more with Svn's",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(r"""
                Test: Epic Svn Log --help
                Test: Epic Svn Log
                Test: Epic Svn Log Wazzup
                Test: Epic Svn Log "What's up?"
                Test: Epic Svn Log --crash
                """),
            )
        parser.add_argument('greetchars', metavar='GREETING', nargs='?', default='Look, Epic Svn Log was here.',
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

        print('info: Epic Svn Log: Got args as if: Epic Svn Log', args.echo)

        return svnbrain.SvnBrain.think_svn_log(args)

    @epic.mainmethod
    @staticmethod
    def epic_svn_regress(argv):

        r"""
        Epic Svn Regress = Test the Svn Bot

        Usage: Epic Svn Regress [-h]

        Optional arguments:

            -h, --help  Show this help message and exit

        Test: Epic Svn Regress --help
        """

        parser = argparse.ArgumentParser(
            'Epic Svn Regress',
            description=r"Test the Svn Bot",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(r"""
                Test: Epic Svn Regress --help
                """),
            )

        args = parser.parse_args(argv[1:])
        args.echo = ' '.join([])
        if False:
            print('info: Epic Svn Regress: Got args as if: Epic Svn Regress', args.echo)

        svnbrain.SvnBrain.think_svn_regress(args)

    @epic.mainmethod
    @staticmethod
    def epic_svn_update(argv):

        r"""
        Epic Svn Update = Do more with Svn's

        Usage: Epic Svn Update [-h] [-c] GREETING

        Positional arguments:

            GREETING    Chars to print

        Optional arguments:

            -h, --help      Show this help message and exit
            -c, --crash     Demo raising an unhandled exception

        Test: Epic Svn Update --help
        Test: Epic Svn Update
        Test: Epic Svn Update Wazzup
        Test: Epic Svn Update "What's up?"
        Test: Epic Svn Update --crash
        """

        parser = argparse.ArgumentParser(
            'Epic Svn Update',
            description=r"Epic Svn Update = Do more with Svn's",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(r"""
                Test: Epic Svn Update --help
                Test: Epic Svn Update
                Test: Epic Svn Update Wazzup
                Test: Epic Svn Update "What's up?"
                Test: Epic Svn Update --crash
                """),
            )
        parser.add_argument('greetchars', metavar='GREETING', nargs='?', default='Look, Epic Svn Update was here.',
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

        print('info: Epic Svn Update: Got args as if: Epic Svn Update', args.echo)

        return svnbrain.SvnBrain.think_svn_update(args)


def def_svnface_doctests():

    r"""

    >>> import epicbots.svnbot.svnface as svnface
    >>>

    >>> # RR PL FIXME: svn checkout to a new folder in __epic-trash__/
    >>> # RR PL FIXME: do all the svn tests there

    >>> gotcwd = os.path.abspath(os.getcwd()) #nl: abspath of getcwd might be spec'ed as unneeded
    >>>

    >>> if os.path.exists(os.path.join(essi_folder, r'.svn')):
    ...     os.chdir(essi_folder)
    ... elif os.path.exists(os.path.join(essi_folder, os.path.join('mfg', r'.svn'))):
    ...     os.chdir(os.path.join(essi_folder, os.path.join('mfg')))
    >>>

    ###
    ### Doctests of Epic Svn ...
    ###

    >>> if epic.args.verbose:
    ...     epic.print('info: Svn Regress: Doctest of Epic Svn', file=sys.__stdout__)
    ...
    >>>

    >>> cmds = {}
    >>> if not sys.platform.startswith('win'):
    ...     cmds['Linux']= (r'python3 %s/essi12/mfg/essi.py --quiet --force Svn' % os.getenv('HOME'))
    >>> cmds['Windows']= r'py.exe -3 C:\Users\Public\Essi12\Mfg\Essi.py --quiet --force Svn'
    >>> ochars = epic.check_output_chars(cmds[platform.system()])
    >>> ochars = ochars.replace(r'Svn Extern: X       unique_customer\tools\dell_dup\release' + '\n', '')
    >>> hit = re.search(pattern=r'info: Essi Svn: Network Service of Svn Log running slow: [0-9]+ seconds per call\n', string=ochars)
    >>> if hit:
    ...     print(hit.group().strip(), file=sys.__stdout__)
    ...     ochars = re.sub(pattern=r'info: Essi Svn: Network Service of Svn Log running slow: [0-9]+ seconds per call\n', repl='', string=ochars)
    >>>

    >>> olines = ochars.strip().splitlines()
    >>> len(olines) if (len(olines) == 6) else print('\n'.join(str(item) for item in enumerate(olines)))
    6
    >>> print(olines[0])
    Svn Status: --- LIBRARY CLEAN ---
    >>> print(olines[1])
    SvnVersion: ...
    >>> print(olines[2])
    Svn Url: https://svnsdus.sandisk.com/svn/HEMi12/Firmware/branches/Essi...
    >>> print(olines[3])
    Last Changed Rev: ... | ... | ...-...-... ...:...:... ... (..., ... ... ...)
    >>> print(olines[4])
    When: ... ...-...-... ...:...:... ...:...
    >>> print(olines[5])
    Where: ...
    >>>

    ###
    ### Doctests of Epic Svn Backup
    ###

    >>> if epic.args.verbose:
    ...     epic.print('info: Svn Regress: Doctest of Epic Svn Backup', file=sys.__stdout__)
    ...
    >>>

    >>>

    ###
    ### Doctests of Epic Svn Clean
    ###

    >>> if epic.args.verbose:
    ...     epic.print('info: Svn Regress: Doctest of Epic Svn Clean', file=sys.__stdout__)
    ...
    >>>

    >>>

    ###
    ### Doctests of Epic Svn Hi
    ###

    >>> if epic.args.verbose:
    ...     epic.print('info: Svn Regress: Doctest of Epic Svn Hi', file=sys.__stdout__)
    ...
    >>>

    >>> if not sys.platform.startswith('win'):
    ...     cmds['Linux']= (r'python3 %s/essi12/mfg/essi.py --quiet --force Svn Hi' % os.getenv('HOME'))
    >>> cmds['Windows']= r'py.exe -3 C:\Users\Public\Essi12\Mfg\Essi.py --quiet --force Svn Hi'
    >>> ochars = epic.check_output_chars(cmds[platform.system()])
    >>> ochars = ochars.replace(r'Svn Extern: X       unique_customer\tools\dell_dup\release' + '\r\n', '')
    >>> ochars = re.sub(pattern='^info: Essi Svn: Network Service of Svn Log running slow: [0-9]+ seconds per call$', repl='', string=ochars)
    >>>

    >>> olines = ochars.strip().splitlines()
    >>> olines = [oline.strip() for oline in olines if oline.startswith('info: Essi Svn Hi: As if:')]
    >>> print('\n'.join(olines).lower())
    info: essi svn hi: as if: ...essi --quiet --force svn backup
    info: essi svn hi: as if: ...essi --quiet --force svn update
    info: essi svn hi: as if: ...essi --quiet --force svn log
    info: essi svn hi: as if: ...essi --quiet --force svn clean
    >>>

    ###
    ### Doctests of Epic Svn Log
    ###

    >>> if epic.args.verbose:
    ...     epic.print('info: Svn Regress: Doctest of Epic Svn Log', file=sys.__stdout__)
    ...
    >>>

    >>>

    ###
    ### Doctests of Epic Svn Update
    ###

    >>> if epic.args.verbose:
    ...     epic.print('info: Svn Regress: Doctest of Epic Svn Update', file=sys.__stdout__)
    ...
    >>>

    >>>

    ###
    ###
    ###

    >>> os.chdir(gotcwd) #nl: yea chdir, not setcwd
    >>>

    """


if True:

    if not sys.platform.startswith('win'):
        essi_folder = os.path.join(os.getenv('HOME'), r'essi12')
        essi_file = r'mfg/essi.cmd'

    if sys.platform.startswith('win'):
        essi_folder = r'C:\Users\Public\Essi12'
        essi_file = r'Mfg\Essi.cmd'

    if not os.path.exists(os.path.join(essi_folder, essi_file)):

        def def_svnface_doctests():

            r"""
            Def SvnFace Doctests

            >>> import epicbots.svnbot.svnface as svnface
            >>>

            >>> epic.print('info: Epic Install: Exp Sndk Hemi Essi Got None', file=sys.__stdout__)
            >>>

            """


not_yet_implemented = True
if not_yet_implemented:

    class SvnFace:

        @epic.mainmethod
        @staticmethod
        def epic_svn(argv):
            sys.stdout.write(epic.check_output_chars('epic12 svn'.split() + argv[1:]))
            sys.stdout.flush()

        @epic.mainmethod
        @staticmethod
        def epic_svn_backup(argv):
            sys.stdout.write(epic.check_output_chars('epic12 svn backup'.split() + argv[1:]))
            sys.stdout.flush()

        @epic.mainmethod
        @staticmethod
        def epic_svn_clean(argv):
            sys.stdout.write(epic.check_output_chars('epic12 svn clean'.split() + argv[1:]))
            sys.stdout.flush()

        @epic.mainmethod
        @staticmethod
        def epic_svn_help(cls):
            raise NotImplementedError()

        @epic.mainmethod
        @staticmethod
        def epic_svn_hi(argv):
            sys.stdout.write(epic.check_output_chars('epic12 svn'.split() + argv[1:]))
            sys.stdout.flush()
            sys.stdout.write(epic.check_output_chars('epic12 svn backup'.split() + argv[1:]))
            sys.stdout.flush()
            sys.stdout.write(epic.check_output_chars('svn update'.split() + argv[1:]))
            sys.stdout.flush()
            sys.stdout.write(epic.check_output_chars('epic12 svn log'.split() + argv[1:]))
            sys.stdout.flush()
            sys.stdout.write(epic.check_output_chars('epic12 svn clean'.split() + argv[1:]))
            sys.stdout.flush()

        @epic.mainmethod
        @staticmethod
        def epic_svn_log(argv):
            sys.stdout.write(epic.check_output_chars('epic12 svn log'.split() + argv[1:]))
            sys.stdout.flush()

        @epic.mainmethod
        @staticmethod
        def epic_svn_regress(cls):
#           regressbrain.RegressBrain.think_regress_newnoun(botnoun='svn')
            raise NotImplementedError()

        @epic.mainmethod
        @staticmethod
        def epic_svn_update(argv):
            sys.stdout.write(epic.check_output_chars('epic12 svn update'.split() + argv[1:]))
            sys.stdout.flush()

