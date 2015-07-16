import argparse
import os
import re
import sys
import textwrap


import epic
import epicbots.legacy as legacy
import epicbots.pybot.pymuscle as pymuscle


SUPPRESS = '==SUPPRESS=='
_UNRECOGNIZED_ARGS_ATTR = '_unrecognized_args'


class ArgMuscle:

    r"""Make Command Line Args easy to parse as doc'ced by help"""

    prefix_chars = '-'

    @classmethod
    def parse_args_per_doc(cls, args=None, namespace=None, doc=None): #nl: kwargs like argparse.parse_args(args=None)

        r"""Parse Args, per a Docstring"""

        likeArgs = args
        if args is None:
            likeArgs = sys.argv[1:]

        likeDoc = doc
        if doc is None:
            likeDoc = epicbots.mainbot.mainface.MainFace._get_last_verb_func().__doc__

        the = ArgMuscle.rip_doc_to_bags(likeDoc)
        the.parser = ArgMuscle.compile_parser_from_bags(the)
        bag = the.parser.parse_args(args=likeArgs, namespace=namespace)

        assert('echo' not in dir(bag)) # PL FIXME: or set what the echo would be by default if the main .echo attribute deleted
        bag.echo = ArgMuscle.compile_echo_from_bags_and_args(the, bag)

        assert('verb' not in dir(bag)) # PL FIXME: recovery or friendly errors for args named echo or verb
        # PL FIXME: bag.verb

        return bag

    @classmethod
    def compile_parser_from_bags(cls, the):

        r"""Construct an argparse.ArgumentParser, per a Docstring"""

        parser = argparse.ArgumentParser(
            the.verb,
            description=the.purpose,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('\n'.join(the.etcs)),
            )

        for opt in the.opts:
            (thin, wide, help) = opt
            if opt == the.helpopt:
                continue

            parser.add_argument(thin, wide, action='store_true',
                help=help,
                )

        return parser

    @classmethod
    def compile_echo_from_bags_and_args(cls, the, args):

        r"""Echo Parsed Args, per a Docstring"""

        echo = the.verb

        if len(the.opts) <= 1:
            assert(the.opts == [the.helpopt])
        else:

            rows = []
            for opt in the.opts:
                (thin, wide, help) = opt
                if opt == the.helpopt:
                    continue

                if eval('args.%s' % wide[len('--'):]):
                    echo += (' %s' % wide)

        return echo

    @classmethod
    def rip_doc_to_pylines(cls, doc):

        r"""Rip Lines of Python that construct an ArgParse'r out of a Docstring"""

        the = ArgMuscle.rip_doc_to_bags(doc)
        ArgMuscle.reconcile_usage_with_opts(the)

        dent = (4 * ' ')

        pylines = []
        pylines += [r'''parser = argparse.ArgumentParser(''']
        pylines += [dent + (r''''%s',''' % the.verb)]
        pylines += [dent + (r'''description=r"%s",''' % the.purpose)] # pl fixme: wrong pylines for some kinds of quotation marks in help lines
        pylines += [dent + r'''formatter_class=argparse.RawDescriptionHelpFormatter,''']
        pylines += [dent + r'''epilog=textwrap.dedent(r"""''']
        if the.etcs:
            for etc in the.etcs:
                pylines += [dent + dent + etc]
        pylines += [dent + dent + r'''"""),''']
        pylines += [dent + r''')''']

        if len(the.opts) <= 1:
            assert(the.opts == [the.helpopt])
        else:

            pylines += [r'''''']

            rows = []
            for opt in the.opts:
                (thin, wide, help) = opt
                if opt == the.helpopt:
                    continue

                pylines += [r'''args = parser.add_argument( ...''']

        pylines += [r'''''']
        pylines += [r'''args = parser.parse_args(argv[1:])''']

        pylines += [r'''''']
        pylines += [r"""args.echo = '%s'""" % the.verb]

        if len(the.opts) <= 1:
            assert(the.opts == [the.helpopt])
        else:

            rows = []
            for opt in the.opts:
                (thin, wide, help) = opt
                if opt == the.helpopt:
                    continue

                pylines += [r'''if args.%s:''' % wide[len('--'):]]
                pylines += [dent + r"""args.echo += ' %s'""" % wide]

        return pylines

    @classmethod
    def rip_doc_to_doc(cls, doc):

        r"""Rip a more conventional Docstring out of a Docstring"""

        the = ArgMuscle.rip_doc_to_bags(doc)
        if False:
            ArgMuscle.reconcile_usage_with_opts(the)

        # Start up

        doclines = []

        doclines += [the.topline]
        doclines += ['']
        doclines += [the.usage]
        doclines += ['']

        # Visit each opt

        if the.opts:

            doclines += [the.optline]
            doclines += ['']

            rows = []
            for opt in the.opts:
                (thin, wide, help) = opt
                strflags = ('%s, %s' % (thin, wide))
                rows += [(strflags, help)]

            # Visit each column

            dent = (4 * ' ')
            minsep = (2 * ' ')

            colwidths = {}

            for row in rows:
                for (cx, col) in enumerate(row):
                    if cx not in colwidths:
                        colwidths[cx] = len(col)
                    elif len(col) > colwidths[cx]:
                        colwidths[cx] = len(col)

            dw = len(dent)
            sw = len(minsep)

            lencols = len(rows[0])
            for cx in range(lencols):
                cw = (colwidths[cx] + sw)
                colwidths[cx] = (dw * ((cw + (dw - 1)) // dw))

            # Print each row

            for row in rows:
                (strflags, help) = row

                lensep = (colwidths[0] - len(strflags))
                sep = (lensep * ' ')

                docline = (dent + strflags + sep + help)
                doclines += [docline]

        # Shut down

        if the.etcs:

            doclines += ['']
            doclines += the.etcs

        docstring = '\n'.join(doclines)
        return docstring

    @classmethod
    def reconcile_usage_with_opts(cls, the):

        r"""Resolve conflicts between the Usage line and Opt lines"""

        if not the.opts:
            the.opts += [the.helpopt]

        pass # PL FIXME: implement reconcile_usage_with_opts

    @classmethod
    def rip_doc_to_bags(cls, doc):

        r"""Rip an Abstract Syntax Tree, encoded as Bags of Bags of Bags, out of a Docstring"""

        assert(doc is not None)

        the = type('', (), {})()

        the.idoc = doc
        the.ichars = textwrap.dedent(the.idoc).strip()
        the.ilines = the.ichars.splitlines()
        the.iln = 1

        relwhat = sys.argv[0]
        spacedwhat = os.path.split(relwhat)[-1]
        the.what = ' '.join(spacedwhat.split())
        the.verb = the.what

        (_, the.noun) = the.what.split()[:2]
        the.purpose = ('Mess with the %s Bot' % the.noun)

        the.topline = ('%s = %s' % (the.what, the.purpose))
        the.usage = ('Usage: %s [-h]' % the.what)
        the.optline = 'Optional arguments:'
        the.opts = []
        the.etcs = []

        thin = '-h'
        wide = '--help'
        help = 'Show this help message and exit'
        the.helpopt = (thin, wide, help)

        ArgMuscle.take_topline(the)
        ArgMuscle.take_blank_ilines(the)
        ArgMuscle.take_usage(the)
        ArgMuscle.take_blank_ilines(the)
        ArgMuscle.take_opts(the)
        ArgMuscle.take_blank_ilines(the)
        ArgMuscle.take_trailing_ilines(the)
        ArgMuscle.take_blank_ilines(the)

        return the

    @classmethod
    def take_topline(cls, the):

        r"""Take the top help line, of Epic ~ = ~ form, detailing the purpose of the verb"""

        iline = ArgMuscle.peek_iline(the)
        if iline:
            sepped = (the.what + ' =')
            if iline.upper().startswith(sepped.upper()):
                the.verb = iline[:len(the.what)]
                the.topline = ArgMuscle.take_iline(the)
                the.purpose = iline[len(sepped):].strip()
            else:
                the.etcs += [ArgMuscle.take_iline(the)]

    @classmethod
    def take_usage(cls, the):

        r"""Take the Usage line"""

        iline = ArgMuscle.peek_iline(the)
        if iline:
            if iline.upper().startswith(('Usage: ' + the.verb).upper()):
                the.usage = ArgMuscle.take_iline(the)
            else:
                the.etcs += [ArgMuscle.take_iline(the)]

    @classmethod
    def take_opts(cls, the):

        r"""Take all the help lines of the Optional Arguments"""

        iline = ArgMuscle.peek_iline(the)
        if iline.upper() != 'Optional arguments:'.upper():
            return

        the.optline = ArgMuscle.take_iline(the)

        while True:

            ArgMuscle.take_blank_ilines(the)
            iline = ArgMuscle.peek_iline(the)
            matched = re.match(pattern=r'^(-[A-Za-z0-9]), (--[A-Za-z0-9]+) +([^ ].*)$', string=iline)
            if not matched:
                break

            thin = matched.group(1)
            wide = matched.group(2)
            help = matched.group(3)
            the.opts += [(thin, wide, help)]

            ArgMuscle.take_iline(the)
            # PL FIXME: publish the opts into rip_doc_to_doc etc.

    @classmethod
    def take_trailing_ilines(cls, the):

        r"""Take all remaining lines"""

        while True:
            iline = ArgMuscle.peek_iline(the)
            if iline is None:
                break
            the.etcs += [ArgMuscle.take_iline(the)]

        if len(the.etcs) > 2:

            infos = []
            infos += ['pl fixme: too many lines matched as all remaining lines']
            infos += ['pl fixme: too many lines matched as all remaining lines']
            infos += ['pl fixme: too many lines matched as all remaining lines']
            infos += ['']

            the.etcs = (infos + the.etcs)

    @classmethod
    def take_blank_ilines(cls, the):

        r"""Take zero or more blank lines"""

        while True:
            iline = ArgMuscle.peek_iline(the)
            if iline is not None:
                if not iline:
                    ArgMuscle.take_iline(the)
                    continue
            break

    @classmethod
    def take_iline(cls, the):

        r"""Take the next line, else None, and return a copy"""

        iline = ArgMuscle.peek_iline(the)
        ix = (the.iln - 1)
        if ix < len(the.ilines):
            assert(iline is not None)
            the.iln += 1

        return iline

    @classmethod
    def peek_iline(cls, the):

        r"""Make a copy of the next line, else None, but don't take it yet"""

        iline = None
        ix = (the.iln - 1)
        if ix < len(the.ilines):
            padded = the.ilines[ix]
            iline = padded.strip()

        return iline

    @classmethod
    def add_argument(cls, *args, **kwargs):
        """
        add_argument(dest, ..., name=value, ...)
        add_argument(option_string, option_string, ..., name=value, ...)
        """

        # if no positional args are supplied or only one is supplied and
        # it doesn't look like an option string, parse a positional
        # argument
        chars = cls.prefix_chars
        if not args or len(args) == 1 and args[0][0] not in chars:
            if args and 'dest' in kwargs:
                raise ValueError('dest supplied twice for positional argument')
            kwargs = cls._get_positional_kwargs(*args, **kwargs)

        # otherwise, we're adding an optional argument
        else:
            kwargs = cls._get_optional_kwargs(*args, **kwargs)

        # if no default was supplied, use the parser-level default
        if 'default' not in kwargs:
            dest = kwargs['dest']
            if dest in cls._defaults:
                kwargs['default'] = cls._defaults[dest]
            elif cls.argument_default is not None:
                kwargs['default'] = cls.argument_default

        # create the action object, and add it to the parser
        action_class = cls._pop_action_class(kwargs)
        if not _callable(action_class):
            raise ValueError('unknown action "%s"' % action_class)
        action = action_class(**kwargs)

        # raise an error if the action type is not callable
        type_func = cls._registry_get('type', action.type, action.type)
        if not _callable(type_func):
            raise ValueError('%r is not callable' % type_func)

        return cls._add_action(action)

    def add_argument_group(cls, *args, **kwargs):
        group = _ArgumentGroup(cls, *args, **kwargs)
        cls._action_groups.append(group)
        return group

    def add_mutually_exclusive_group(cls, **kwargs):
        group = _MutuallyExclusiveGroup(cls, **kwargs)
        cls._mutually_exclusive_groups.append(group)
        return group

    def _add_action(cls, action):
        # resolve any conflicts
        cls._check_conflict(action)

        # add to actions list
        cls._actions.append(action)
        action.container = cls

        # index the action by any option strings it has
        for option_string in action.option_strings:
            cls._option_string_actions[option_string] = action

        # set the flag if any option strings look like negative numbers
        for option_string in action.option_strings:
            if cls._negative_number_matcher.match(option_string):
                if not cls._has_negative_number_optionals:
                    cls._has_negative_number_optionals.append(True)

        # return the created action
        return action

    def _remove_action(cls, action):
        cls._actions.remove(action)

    def _add_container_actions(cls, container):
        # collect groups by titles
        title_group_map = {}
        for group in cls._action_groups:
            if group.title in title_group_map:
                msg = _('cannot merge actions - two groups are named %r')
                raise ValueError(msg % (group.title))
            title_group_map[group.title] = group

        # map each action to its group
        group_map = {}
        for group in container._action_groups:

            # if a group with the title exists, use that, otherwise
            # create a new group matching the container's group
            if group.title not in title_group_map:
                title_group_map[group.title] = cls.add_argument_group(
                    title=group.title,
                    description=group.description,
                    conflict_handler=group.conflict_handler)

            # map the actions to their new group
            for action in group._group_actions:
                group_map[action] = title_group_map[group.title]

        # add container's mutually exclusive groups
        # NOTE: if add_mutually_exclusive_group ever gains title= and
        # description= then this code will need to be expanded as above
        for group in container._mutually_exclusive_groups:
            mutex_group = cls.add_mutually_exclusive_group(
                required=group.required)

            # map the actions to their new mutex group
            for action in group._group_actions:
                group_map[action] = mutex_group

        # add all actions to this container or their group
        for action in container._actions:
            group_map.get(action, cls)._add_action(action)

    def _get_positional_kwargs(cls, dest, **kwargs):
        # make sure required is not specified
        if 'required' in kwargs:
            msg = _("'required' is an invalid argument for positionals")
            raise TypeError(msg)

        # mark positional arguments as required if at least one is
        # always required
        if kwargs.get('nargs') not in [OPTIONAL, ZERO_OR_MORE]:
            kwargs['required'] = True
        if kwargs.get('nargs') == ZERO_OR_MORE and 'default' not in kwargs:
            kwargs['required'] = True

        # return the keyword arguments with no option strings
        return dict(kwargs, dest=dest, option_strings=[])

    def _get_optional_kwargs(cls, *args, **kwargs):
        # determine short and long option strings
        option_strings = []
        long_option_strings = []
        for option_string in args:
            # error on strings that don't start with an appropriate prefix
            if not option_string[0] in cls.prefix_chars:
                msg = _('invalid option string %r: '
                        'must start with a character %r')
                tup = option_string, cls.prefix_chars
                raise ValueError(msg % tup)

            # strings starting with two prefix characters are long options
            option_strings.append(option_string)
            if option_string[0] in cls.prefix_chars:
                if len(option_string) > 1:
                    if option_string[1] in cls.prefix_chars:
                        long_option_strings.append(option_string)

        # infer destination, '--foo-bar' -> 'foo_bar' and '-x' -> 'x'
        dest = kwargs.pop('dest', None)
        if dest is None:
            if long_option_strings:
                dest_option_string = long_option_strings[0]
            else:
                dest_option_string = option_strings[0]
            dest = dest_option_string.lstrip(cls.prefix_chars)
            if not dest:
                msg = _('dest= is required for options like %r')
                raise ValueError(msg % option_string)
            dest = dest.replace('-', '_')

        # return the updated keyword arguments
        return dict(kwargs, dest=dest, option_strings=option_strings)

    def _pop_action_class(cls, kwargs, default=None):
        action = kwargs.pop('action', default)
        return cls._registry_get('action', action, action)

    def _get_handler(cls):
        # determine function from conflict handler string
        handler_func_name = '_handle_conflict_%s' % cls.conflict_handler
        try:
            return getattr(cls, handler_func_name)
        except AttributeError:
            msg = _('invalid conflict_resolution value: %r')
            raise ValueError(msg % cls.conflict_handler)

    def _check_conflict(cls, action):

        # find all options that conflict with this option
        confl_optionals = []
        for option_string in action.option_strings:
            if option_string in cls._option_string_actions:
                confl_optional = cls._option_string_actions[option_string]
                confl_optionals.append((option_string, confl_optional))

        # resolve any conflicts
        if confl_optionals:
            conflict_handler = cls._get_handler()
            conflict_handler(action, confl_optionals)

    def _handle_conflict_error(cls, action, conflicting_actions):
        message = _('conflicting option string(s): %s')
        conflict_string = ', '.join([option_string
                                     for option_string, action
                                     in conflicting_actions])
        raise ArgumentError(action, message % conflict_string)

    def _handle_conflict_resolve(cls, action, conflicting_actions):

        # remove all conflicting options
        for option_string, action in conflicting_actions:

            # remove the conflicting option
            action.option_strings.remove(option_string)
            cls._option_string_actions.pop(option_string, None)

            # if the option now has no option string, remove it from the
            # container holding it
            if not action.option_strings:
                action.container._remove_action(action)

class ArgumentError(Exception):
    """An error from creating or using an argument (optional or positional).

    The string value of this exception is the message, augmented with
    information about the argument that caused it.
    """

    def __init__(cls, argument, message):
        cls.argument_name = _get_action_name(argument)
        cls.message = message

    def __str__(cls):
        if cls.argument_name is None:
            format = '%(message)s'
        else:
            format = 'argument %(argument_name)s: %(message)s'
        return format % dict(message=cls.message,
                             argument_name=cls.argument_name)

def _get_action_name(argument):
    if argument is None:
        return None
    elif argument.option_strings:
        return  '/'.join(argument.option_strings)
    elif argument.metavar not in (None, SUPPRESS):
        return argument.metavar
    elif argument.dest not in (None, SUPPRESS):
        return argument.dest
    else:
        return None


class _AttributeHolder(object):
    """Abstract base class that provides __repr__.

    The __repr__ method returns a string in the format::
        ClassName(attr=name, attr=name, ...)
    The attributes are determined either by a class-level attribute,
    '_kwarg_names', or by inspecting the instance __dict__.
    """

    def __repr__(cls):
        type_name = type(cls).__name__
        arg_strings = []
        for arg in cls._get_args():
            arg_strings.append(repr(arg))
        for name, value in cls._get_kwargs():
            arg_strings.append('%s=%r' % (name, value))
        return '%s(%s)' % (type_name, ', '.join(arg_strings))

    def _get_kwargs(cls):
        return sorted(cls.__dict__.items())

    def _get_args(cls):
        return []


class Action(_AttributeHolder):
    """Information about how to convert command line strings to Python objects.

    Action objects are used by an ArgumentParser to represent the information
    needed to parse a single argument from one or more strings from the
    command line. The keyword arguments to the Action constructor are also
    all attributes of Action instances.

    Keyword Arguments:

        - option_strings -- A list of command-line option strings which
            should be associated with this action.

        - dest -- The name of the attribute to hold the created object(s)

        - nargs -- The number of command-line arguments that should be
            consumed. By default, one argument will be consumed and a single
            value will be produced.  Other values include:
                - N (an integer) consumes N arguments (and produces a list)
                - '?' consumes zero or one arguments
                - '*' consumes zero or more arguments (and produces a list)
                - '+' consumes one or more arguments (and produces a list)
            Note that the difference between the default and nargs=1 is that
            with the default, a single value will be produced, while with
            nargs=1, a list containing a single value will be produced.

        - const -- The value to be produced if the option is specified and the
            option uses an action that takes no values.

        - default -- The value to be produced if the option is not specified.

        - type -- The type which the command-line arguments should be converted
            to, should be one of 'string', 'int', 'float', 'complex' or a
            callable object that accepts a single string argument. If None,
            'string' is assumed.

        - choices -- A container of values that should be allowed. If not None,
            after a command-line argument has been converted to the appropriate
            type, an exception will be raised if it is not a member of this
            collection.

        - required -- True if the action must always be specified at the
            command line. This is only meaningful for optional command-line
            arguments.

        - help -- The help string describing the argument.

        - metavar -- The name to be used for the option's argument with the
            help string. If None, the 'dest' value will be used as the name.
    """

    def __init__(cls,
                 option_strings,
                 dest,
                 nargs=None,
                 const=None,
                 default=None,
                 type=None,
                 choices=None,
                 required=False,
                 help=None,
                 metavar=None):
        cls.option_strings = option_strings
        cls.dest = dest
        cls.nargs = nargs
        cls.const = const
        cls.default = default
        cls.type = type
        cls.choices = choices
        cls.required = required
        cls.help = help
        cls.metavar = metavar

    def _get_kwargs(cls):
        names = [
            'option_strings',
            'dest',
            'nargs',
            'const',
            'default',
            'type',
            'choices',
            'help',
            'metavar',
        ]
        return [(name, getattr(cls, name)) for name in names]

    def __call__(cls, parser, namespace, values, option_string=None):
        raise NotImplementedError(_('.__call__() not defined'))


class _StoreAction(Action):

    def __init__(cls,
                 option_strings,
                 dest,
                 nargs=None,
                 const=None,
                 default=None,
                 type=None,
                 choices=None,
                 required=False,
                 help=None,
                 metavar=None):
        if nargs == 0:
            raise ValueError('nargs for store actions must be > 0; if you '
                             'have nothing to store, actions such as store '
                             'true or store const may be more appropriate')
        if const is not None and nargs != OPTIONAL:
            raise ValueError('nargs must be %r to supply const' % OPTIONAL)
        super(_StoreAction, cls).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            const=const,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar)

    def __call__(cls, parser, namespace, values, option_string=None):
        setattr(namespace, cls.dest, values)


class _StoreConstAction(Action):

    def __init__(cls,
                 option_strings,
                 dest,
                 const,
                 default=None,
                 required=False,
                 help=None,
                 metavar=None):
        super(_StoreConstAction, cls).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=const,
            default=default,
            required=required,
            help=help)

    def __call__(cls, parser, namespace, values, option_string=None):
        setattr(namespace, cls.dest, cls.const)


class _StoreTrueAction(_StoreConstAction):

    def __init__(cls,
                 option_strings,
                 dest,
                 default=False,
                 required=False,
                 help=None):
        super(_StoreTrueAction, cls).__init__(
            option_strings=option_strings,
            dest=dest,
            const=True,
            default=default,
            required=required,
            help=help)


class _StoreFalseAction(_StoreConstAction):

    def __init__(cls,
                 option_strings,
                 dest,
                 default=True,
                 required=False,
                 help=None):
        super(_StoreFalseAction, cls).__init__(
            option_strings=option_strings,
            dest=dest,
            const=False,
            default=default,
            required=required,
            help=help)


class _AppendAction(Action):

    def __init__(cls,
                 option_strings,
                 dest,
                 nargs=None,
                 const=None,
                 default=None,
                 type=None,
                 choices=None,
                 required=False,
                 help=None,
                 metavar=None):
        if nargs == 0:
            raise ValueError('nargs for append actions must be > 0; if arg '
                             'strings are not supplying the value to append, '
                             'the append const action may be more appropriate')
        if const is not None and nargs != OPTIONAL:
            raise ValueError('nargs must be %r to supply const' % OPTIONAL)
        super(_AppendAction, cls).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            const=const,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar)

    def __call__(cls, parser, namespace, values, option_string=None):
        items = _copy.copy(_ensure_value(namespace, cls.dest, []))
        items.append(values)
        setattr(namespace, cls.dest, items)


class _AppendConstAction(Action):

    def __init__(cls,
                 option_strings,
                 dest,
                 const,
                 default=None,
                 required=False,
                 help=None,
                 metavar=None):
        super(_AppendConstAction, cls).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=const,
            default=default,
            required=required,
            help=help,
            metavar=metavar)

    def __call__(cls, parser, namespace, values, option_string=None):
        items = _copy.copy(_ensure_value(namespace, cls.dest, []))
        items.append(cls.const)
        setattr(namespace, cls.dest, items)


class _CountAction(Action):

    def __init__(cls,
                 option_strings,
                 dest,
                 default=None,
                 required=False,
                 help=None):
        super(_CountAction, cls).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            default=default,
            required=required,
            help=help)

    def __call__(cls, parser, namespace, values, option_string=None):
        new_count = _ensure_value(namespace, cls.dest, 0) + 1
        setattr(namespace, cls.dest, new_count)


class _HelpAction(Action):

    def __init__(cls,
                 option_strings,
                 dest=SUPPRESS,
                 default=SUPPRESS,
                 help=None):
        super(_HelpAction, cls).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(cls, parser, namespace, values, option_string=None):
        parser.print_help()
        parser.exit()


class _VersionAction(Action):

    def __init__(cls,
                 option_strings,
                 version=None,
                 dest=SUPPRESS,
                 default=SUPPRESS,
                 help="show program's version number and exit"):
        super(_VersionAction, cls).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)
        cls.version = version

    def __call__(cls, parser, namespace, values, option_string=None):
        version = cls.version
        if version is None:
            version = parser.version
        formatter = parser._get_formatter()
        formatter.add_text(version)
        parser.exit(message=formatter.format_help())


class _SubParsersAction(Action):

    class _ChoicesPseudoAction(Action):

        def __init__(cls, name, aliases, help):
            metavar = dest = name
            if aliases:
                metavar += ' (%s)' % ', '.join(aliases)
            sup = super(_SubParsersAction._ChoicesPseudoAction, cls)
            sup.__init__(option_strings=[], dest=dest, help=help,
                        metavar=metavar)

    def __init__(cls,
                 option_strings,
                 prog,
                 parser_class,
                 dest=SUPPRESS,
                 help=None,
                 metavar=None):

        cls._prog_prefix = prog
        cls._parser_class = parser_class
        cls._name_parser_map = {}
        cls._choices_actions = []

        super(_SubParsersAction, cls).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=PARSER,
            choices=cls._name_parser_map,
            help=help,
            metavar=metavar)

    def add_parser(cls, name, **kwargs):
        # set prog from the existing prefix
        if kwargs.get('prog') is None:
            kwargs['prog'] = '%s %s' % (cls._prog_prefix, name)

        aliases = kwargs.pop('aliases', ())

        # create a pseudo-action to hold the choice help
        if 'help' in kwargs:
            help = kwargs.pop('help')
            choice_action = cls._ChoicesPseudoAction(name, aliases, help)
            cls._choices_actions.append(choice_action)

        # create the parser and add it to the map
        parser = cls._parser_class(**kwargs)
        cls._name_parser_map[name] = parser

        # make parser available under aliases also
        for alias in aliases:
            cls._name_parser_map[alias] = parser

        return parser

    def _get_subactions(cls):
        return cls._choices_actions

    def __call__(cls, parser, namespace, values, option_string=None):
        parser_name = values[0]
        arg_strings = values[1:]

        # set the parser name if requested
        if cls.dest is not SUPPRESS:
            setattr(namespace, cls.dest, parser_name)

        # select the parser
        try:
            parser = cls._name_parser_map[parser_name]
        except KeyError:
            tup = parser_name, ', '.join(cls._name_parser_map)
            msg = _('unknown parser %r (choices: %s)' % tup)
            raise ArgumentError(cls, msg)

        # parse all the remaining options into the namespace
        # store any unrecognized options on the object, so that the top
        # level parser can decide what to do with them
        namespace, arg_strings = parser.parse_known_args(arg_strings, namespace)
        if arg_strings:
            vars(namespace).setdefault(_UNRECOGNIZED_ARGS_ATTR, [])
            getattr(namespace, _UNRECOGNIZED_ARGS_ATTR).extend(arg_strings)


def _ensure_value(namespace, name, value):
    if getattr(namespace, name, None) is None:
        setattr(namespace, name, value)
    return getattr(namespace, name)


def def_argbot_doctests():

    r"""
    Def ArgBot Doctests

    >>> import epicbots.argbot.argmuscle as argmuscle
    >>>

    >>> 1 + 2
    3
    >>>
    """

