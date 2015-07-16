import doctest
import os
import sys


import epic
import epicbots.legacy as legacy
import epicbots.regressbot.regressbrain as regressbrain
import epicbots.svnbot.svnmuscle as svnmuscle


class SvnBrain:

    r"""Coordinate the work of the svnbot.svnmuscle"""

    @classmethod
    def think_svn(cls, args):

        r"""Say hello from the Svn Bot"""

        print()
        for tries in range(3):
            svnmuscle.SvnMuscle.move_svn(args)
        print()

    @classmethod
    def think_svn_backup(cls, args,
                         url='https://svnsdus.sandisk.com/svn/ess-fw-tools/branches/epic1407',
                         to_rev=1344,
                         filename='backup.dump'):

        r"""Say hello from the Svn Bot"""
        svnmuscle.SvnMuscle.move_svn_backup(args, url, to_rev, filename)

    @classmethod
    def think_svn_clean(cls, args):

        r"""Say hello from the Svn Bot"""

        svnmuscle.SvnMuscle.move_svn_clean(args, 'C:\\Users\\Public\\epic14')

    @classmethod
    def think_svn_hi(cls, args):

        r"""Say hello from the Svn Bot"""

        print()
        for tries in range(3):
            svnmuscle.SvnMuscle.move_svn_hi(args)
        print()

    @classmethod
    def think_svn_log(cls, args):

        r"""Say hello from the Svn Bot"""

        print()
        for tries in range(3):
            svnmuscle.SvnMuscle.move_svn_log(args)
        print()

    @classmethod
    def think_svn_regress(cls, args):

        r"""Test the Svn Bot"""

        if epic.args.verbose:
            epic.print('info: Svn Regress: Doctests')

        regressbrain.RegressBrain.think_regress_newnoun(botnoun='svn')

        #

        branch = 'https://svnsdus.sandisk.com/svn/HEMi2/branch/T3Bx'
        from_rev = 10799
        to_rev = 10950

        if epic.args.verbose:
            epic.print('info: Svn Regress: Test 1 of 2 of Get Xml')

        filename = svnmuscle.SvnMuscle.get_xml(branch, from_rev, to_rev)
        assert(os.path.exists(filename))

        if epic.args.verbose:
            epic.print('info: Svn Regress: Test 2 of 2 of Get Xml')

        filename = svnmuscle.SvnMuscle.get_xml(branch, from_rev, to_rev)
        assert(os.path.exists(filename))

        #DY FIXME We should be able to run a failed argument case
        #filename = svnmuscle.SvnMuscle.get_xml('', '')
        #assert(filename is None)

    @classmethod
    def think_svn_update(cls, args):

        r"""Say hello from the Svn Bot"""

        print()
        for tries in range(3):
            svnmuscle.SvnMuscle.move_svn_update(args)
        print()


def def_svnbrain_doctests():

    r"""
    Def SvnBrain Doctests

    >>> import epicbots.svnbot.svnbrain as svnbrain
    >>>

    ###
    ### Doctests of Think Svn ...
    ###

    >>> args = epic.space(crash=False, greetchars='you can say that again')
    >>> svnbrain.SvnBrain.think_svn(args)
    <BLANKLINE>
    info: Svn ...: you can say that again
    info: Svn ...: you ... again
    info: Svn ...: you can say that again
    <BLANKLINE>
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnbrain.SvnBrain.think_svn(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn ...: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Think Svn Backup
    ###

    >>> args = epic.space(crash=False, greetchars='you can say that again')
    >>> svnbrain.SvnBrain.think_svn_backup(args)
    info: Svn Backup: Done
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnbrain.SvnBrain.think_svn_backup(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn Backup: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Think Svn Clean
    ###

    >>> args = epic.space(crash=False, greetchars='you can say that again')
    >>> svnbrain.SvnBrain.think_svn_clean(args)
    info: Svn Clean: Done
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnbrain.SvnBrain.think_svn_clean(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn Clean: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Think Svn Hi
    ###

    >>> args = epic.space(crash=False, greetchars='you can say that again')
    >>> svnbrain.SvnBrain.think_svn_hi(args)
    <BLANKLINE>
    info: Svn Hi: you can say that again
    info: Svn Hi: you ... again
    info: Svn Hi: you can say that again
    <BLANKLINE>
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnbrain.SvnBrain.think_svn_hi(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn Hi: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Think Svn Log
    ###

    >>> args = epic.space(crash=False, greetchars='you can say that again')
    >>> svnbrain.SvnBrain.think_svn_log(args)
    <BLANKLINE>
    info: Svn Log: you can say that again
    info: Svn Log: you ... again
    info: Svn Log: you can say that again
    <BLANKLINE>
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnbrain.SvnBrain.think_svn_log(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn Log: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Think Svn Update
    ###

    >>> args = epic.space(crash=False, greetchars='you can say that again')
    >>> svnbrain.SvnBrain.think_svn_update(args)
    <BLANKLINE>
    info: Svn Update: you can say that again
    info: Svn Update: you ... again
    info: Svn Update: you can say that again
    <BLANKLINE>
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> svnbrain.SvnBrain.think_svn_update(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Svn Update: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Svn Brain
    ###

    >>> type(svnbrain.SvnBrain)
    <class 'type'>
    >>>

    """

