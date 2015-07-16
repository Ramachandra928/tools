import doctest
import os
import sys


import epic
import epicbots.legacy as legacy
import epicbots.textbot.textmuscle as textmuscle


class TextBrain:

    r"""Coordinate the work of the textbot.textmuscle"""

    @classmethod
    def think_text_paste(cls, args):

        r"""Say hello from the Text Bot"""

        print()
        for tries in range(3):
            textmuscle.TextMuscle.move_text_paste(args)
        print()


def def_textbrain_doctests():

    r"""
    Def TextBrain Doctests

    >>> import epicbots.textbot.textbrain as textbrain
    >>>

    ###
    ### Doctests of Think Text Paste
    ###

    >>> args = epic.space(crash=False, greetchars='you can say that again')
    >>> textbrain.TextBrain.think_text_paste(args)
    <BLANKLINE>
    info: Text Paste: you can say that again
    info: Text Paste: you ... again
    info: Text Paste: you can say that again
    <BLANKLINE>
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> textbrain.TextBrain.think_text_paste(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Text Paste: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Text Brain
    ###

    >>> type(textbrain.TextBrain)
    <class 'type'>
    >>>

    """

