import math
import os
import re
import subprocess
import sys


import epic
import epicbots.legacy as legacy
import epicbots.sessionbot.sessionmuscle as sessionmuscle


import xml.etree.ElementTree as xml_et


class SvnMuscle:

    r"""Talk with Svn Revision Control"""

    @staticmethod
    def fetch_svn_username(default=None):

        r"""Fetch the Username from the Svn credential most recently saved locally, else return the ElseVal."""

        # Find the Win %APPDATA% folder

        gotEnv_AppData = os.getenv('APPDATA', None)

        if gotEnv_AppData is None:
            return default

        # List the files of the folder of saved Svn credentials

        top = os.path.join(gotEnv_AppData, r'Subversion\auth\svn.simple') #nl: dir /b/s %APPDATA%\Subversion\auth\svn.simple
        sortables = []
        for there, wheres, whats in os.walk(top):
            for what in whats:
                filename = os.path.join(there, what)
                stats = os.stat(filename)
                sortables += [(stats.st_mtime, filename)]
            break

        # Find the freshest file

        if not sortables:
            return default

        sortables.sort()
        sortables.reverse()
        (mtime, filename) = sortables[0]

        # Fetch its Username

        fileBytes = open(filename, 'rb').read()
        fileChars = fileBytes.decode(encoding='UTF-8', errors='surrogateescape')

        fileLines = fileChars.splitlines()
        for (ix, fileLine) in enumerate(fileLines):
            if fileLine.strip().upper() == 'username'.upper():
                usernameKeyAt = ix
                usernameValAt = (ix + 2)
                if usernameValAt < len(fileLines):
                    return fileLines[usernameValAt].strip()

        # Else fail

        return default

    @classmethod
    def fetch_info(cls, branch):
        try:
#           output = subprocess.check_output(['svn', 'info', branch], stderr=subprocess.STDOUT, shell=True).decode()
#           output = os.popen('svn info %s' % branch).read()
            output = epic.check_output_chars(['svn', 'info', branch])
#           for line in output.split('\r\n'):
            for line in output.splitlines():
                if line.split():
                    [attribute, value] = line.split(': ')

                    # ---> NON trivial design choice warning <---
                    # The following line append every keyword/value pair read from svn info
                    # as properties of the class
                    setattr(cls, attribute.replace(' ', '_').lower(), value)

            assert(hasattr(cls, 'revision'))

        except subprocess.CalledProcessError:
            legacy.wprint('ERROR: Epic Svn: Try setting a valid branch URL') # 'ERROR:

    @classmethod
    def get_xml(cls, branch, from_rev, to_rev=None):
        return cls.get_log(branch, from_rev, to_rev, xml=True)

    @classmethod
    def get_log(cls, branch, from_rev, to_rev=None, xml=False):

        #Check if we can talk to SVN
        cls.fetch_info(branch)

        if to_rev is None:
            assert(hasattr(cls, 'revision'))
            to_rev = cls.revision

        try:
            #svn log  https://svnsdus.sandisk.com/svn/HEMi2/branch/T3C1 -r 10897:10936 --xml -v > T3C1_svn_n.xml
            command_line = ['svn', 'log', branch, '-r', str(from_rev) + ':' + str(to_rev)]
            if xml:
                command_line.append('--xml')
            output = subprocess.check_output(command_line, stderr=subprocess.STDOUT)
            payload = output.replace('\r\n'.encode(), '\n'.encode())

            if payload is not None:
                filename = cls.path + '-' + str(from_rev) + '-' + str(to_rev)

                if xml:
                    filename += '.xml'
                else:
                    filename += '.txt'

                with epic.open(filename, 'wb') as wb:
                    wb.write(payload)
                    return wb.name

            return None
        except subprocess.CalledProcessError:
            legacy.wprint('ERROR: Epic Svn: Try setting a valid branch URL') # 'ERROR:

    @classmethod
    def move_svn(cls, args):

        r"""Say hello from the Svn Bot"""

        if args.crash:
            sys.exit(['ERROR: Epic Svn ...: Raising an unhandled exception'])

        print('info: Svn ...:', args.greetchars)

    @classmethod
    def move_svn_backup(cls, args, url, to_rev, filename):

        r"""Say hello from the Svn Bot"""

        if args.crash:
            sys.exit(['ERROR: Epic Svn Backup: Raising an unhandled exception'])

        import os
        import subprocess
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        __filename = filename
        __absfilename = os.path.join(BASE_DIR, __filename)

        try:
            output_file = open(__absfilename, "wb")
            proc = subprocess.Popen(['svnrdump', 'dump', '--quiet', url, '--revision', str(to_rev)], stdin=subprocess.PIPE, stdout=output_file, shell=False)
            p = proc.communicate()[0]
            output_file.close()
            print('info: Svn Backup: Done')
        except:
            print('info: Svn Backup: Backup failed')

    @classmethod
    def move_svn_clean(cls, args, url):

        r"""Say hello from the Svn Bot"""

        if args.crash:
            sys.exit(['ERROR: Epic Svn Clean: Raising an unhandled exception'])

        import os
        import subprocess

        p = subprocess.Popen('svn cleanup', cwd = url)
        out, err = p.communicate()
        print('info: Svn Clean: Done')

    @classmethod
    def move_svn_hi(cls, args):

        r"""Say hello from the Svn Bot"""

        if args.crash:
            sys.exit(['ERROR: Epic Svn Hi: Raising an unhandled exception'])

        print('info: Svn Hi:', args.greetchars)

    @classmethod
    def move_svn_log(cls, args):

        r"""Say hello from the Svn Bot"""

        if args.crash:
            sys.exit(['ERROR: Epic Svn Log: Raising an unhandled exception'])

        print('info: Svn Log:', args.greetchars)

    @classmethod
    def move_svn_regress(cls, args):

        r"""Say hello from the Svn Bot"""

        if args.crash:
            sys.exit(['ERROR: Epic Svn Regress: Raising an unhandled exception'])

        print('info: Svn Regress:', args.greetchars)

    @classmethod
    def move_svn_update(cls, args):

        r"""Say hello from the Svn Bot"""

        if args.crash:
            sys.exit(['ERROR: Epic Svn Update: Raising an unhandled exception'])

        print('info: Svn Update:', args.greetchars)

    @staticmethod
    def parse_xml(filename):
        return SvnXmlParser(filename)


class SvnXmlParser(object):

    def __init__(self, filename):
        self.entries = []
        tree = xml_et.parse(filename)
        root = tree.getroot()
        log_entries = root.findall('logentry')
        for entry in log_entries:
            #self.entries.append(LogEntry(entry))
            self.entries.extend(LogEntry.parse_overloaded_log_entry(entry))

    def __contains__(self, key):
        keys = []
        for entry in self.entries:
            keys.append(entry.key)
        return key in keys


class LogEntry(object):

    def __init__(self, node, key = None, revision = None):
        text = node.find('msg').text
        self.payload = text

        if key == None and revision == None:
            lines_list = text.split('\n')
            for line in lines_list:
                if line.find('JIRA Number:') > -1:
                    text = line.split(':')[-1].strip()

                    #print(text.split())

                    if text.find('-') < 0:
                        print("The key should follow: XXXX-#### however it looks more like:", text)
                        print("Need to implement something fo fix bad inputs from bad engineers:", node.find('author').text)
                        raise NotImplementedError('ERROR: Epic Svn Muscle: Class LogEntry: NotImplementedError')

                    break
            self.key = text
            self.revision = node.attrib['revision']

        else:
            self.key = key
            self.revision = revision

    @classmethod
    def _compile_patterns(cls):
        cls.COMPILED_PATTERNS = {
            re.compile('[A-Z]{1,15}-[0-9]{1,5}|[a-z]{1,15}-[0-9]{1,5}'): cls._clean_dash,
            re.compile('[A-Z]{1,15}_[0-9]{1,5}|[a-z]{1,15}_[0-9]{1,5}'): cls._clean_underscore,
            re.compile('[A-Z]{1,15} [0-9]{1,5}|[a-z]{1,15} [0-9]{1,5}'): cls._clean_space,
            re.compile('[A-Z]{1,15}[0-9]{1,5}|[a-z]{1,15}[0-9]{1,5}'): cls._clean_no_space,
            }

    @classmethod
    def parse_overloaded_log_entry(cls, node):

        if hasattr(cls, 'COMPILED_PATTERNS') == False:
            cls._compile_patterns()

        entries = []

        text = node.find('msg').text
        lines_list = text.split('\n')
        for line in lines_list:
            if line.find('JIRA Number:') > -1:

                #text = line.split(':')[-1].strip()

                text = line

                if text.find('EVER-4150') > -1:
                    print(text)
                #print(text)
                #text = 'EVER-1234; KILI-1; KILI 96;CARLOS_78 pedro-30 jacinto-whey5698 tralala 20'

                for compiled_pattern in cls.COMPILED_PATTERNS:
                    entries.extend(cls._find_entries_by_re(text, compiled_pattern))

        #print(entries)
        output = []
        for entry in entries:
            output.append(LogEntry(node, key = entry, revision = node.attrib['revision']))

        return(output)

        #return [LogEntry(node)]

    @classmethod
    def _find_entries_by_re(cls, text, compiled_pattern):
        entries = compiled_pattern.findall(text.upper())
        #print(entries, cls.COMPILED_PATTERNS[compiled_pattern])
        clean_up_method = cls.COMPILED_PATTERNS[compiled_pattern]
        cleaned_up_entries = clean_up_method(entries)
        #print(cleaned_up_entries)

        return cleaned_up_entries

    @classmethod
    def _clean_dash(cls, entries):
        clean_entries = []
        for entry in entries:
            clean_entries.append(entry.upper())
        return clean_entries

    @classmethod
    def _clean_underscore(cls, entries):
        clean_entries = []
        for entry in entries:
            clean_entries.append(entry.replace('_', '-').upper())
        return clean_entries

    @classmethod
    def _clean_space(cls, entries):
        clean_entries = []
        for entry in entries:
            clean_entries.append(entry.replace(' ', '-').upper())
        return clean_entries

    @classmethod
    def _clean_no_space(cls, entries):
        clean_entries = []
        for entry in entries:
            letters = re.search('[A-Z]{1,15}|[a-z]{1,15}', entry)
            numbers = re.search('[0-9]{1,5}', entry)
            clean_entries.append(letters.group().upper() + '-' + numbers.group())
        return clean_entries


def def_svnmuscle_doctests():

    r"""
    Def SvnMuscle Doctests

    >>> import epicbots.svnbot.svnmuscle as svnmuscle
    >>>

    ###
    ### Doctests of Move Svn ...
    ###

    >>> args = epic.space(crash=False, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn(args)
    info: Svn ...: ...greet...
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn ...: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Move Svn Backup
    ###

    >>> args = epic.space(crash=False, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn_backup(args, 'https://svnsdus.sandisk.com/svn/ess-fw-tools/branches/epic1407', 1344, 'backup.dump')
    info: Svn Backup: Done
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn_backup(args, 'https://svnsdus.sandisk.com/svn/ess-fw-tools/branches/epic1407', 1344, 'backup.dump')
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn Backup: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Move Svn Clean
    ###

    >>> args = epic.space(crash=False, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn_clean(args, 'C:\\Users\\Public\\epic14')
    info: Svn Clean: Done
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn_clean(args, 'C:\\Users\\Public\\epic14')
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn Clean: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Move Svn Hi
    ###

    >>> args = epic.space(crash=False, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn_hi(args)
    info: Svn Hi: ...greet...
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn_hi(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn Hi: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Move Svn Log
    ###

    >>> args = epic.space(crash=False, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn_log(args)
    info: Svn Log: ...greet...
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn_log(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn Log: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Move Svn Regress
    ###

    >>> args = epic.space(crash=False, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn_regress(args)
    info: Svn Regress: ...greet...
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn_regress(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn Regress: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Move Svn Update
    ###

    >>> args = epic.space(crash=False, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn_update(args)
    info: Svn Update: ...greet...
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnmuscle.SvnMuscle.move_svn_update(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn Update: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Svn Muscle
    ###

    >>> type(svnmuscle.SvnMuscle)
    <class 'type'>
    >>>

    """

