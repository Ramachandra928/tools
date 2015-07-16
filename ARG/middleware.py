import doctest
import os
import sys


import epic
import epicbots.legacy as legacy
import epicbots.argbot.argmuscle as argmuscle


class ArgBrain:

    r"""Coordinate the work of the argbot.argmuscle"""

    @classmethod
    def arg_debug(cls, args):

        r"""Trace the Arg Bot compiling Help Lines"""

        if True: #PL FIXME: link with verb
            likeDoc = epicbots.argbot.argface.ArgFace.epic_arg_debug.__doc__

        dent = (4 * ' ')

        if args.doc:
            print('info: Epic Arg Debug: Doc Lines:')
            print()
            for docline in argmuscle.ArgMuscle.rip_doc_to_doc(likeDoc).splitlines():
                print(dent + docline)

        if args.py:
            print('info: Epic Arg Debug: Py Lines:')
            print()
            for pyline in argmuscle.ArgMuscle.rip_doc_to_pylines(likeDoc):
                print(dent + pyline)

        if args.args:
            print('info: Epic Arg Debug: Arg Lines:')
            print()
            print(dent + 'argparse.Namespace(')
            vals = vars(args)
            for name in sorted(vals):
                print(dent + dent + name + '=' + repr(vals[name]) + ',')
            print(dent + ')')

        print()

