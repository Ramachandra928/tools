import os
import sys


import epic
import epicbots.legacy as legacy


class TextMuscle:

    r"""Make Texts easy to copy, paste, and transform"""

    @classmethod
    def is_title_or_camel(cls, chars):

        r"""Say chars are Title or CamelCase when every Split is led by Upper and then not all Upper"""

        shards = chars.split()
        for shard in shards:

            head = shard[0]
            if head.upper() != head.lower():
                if head != head.upper():
                    return False

            tail = shard[1:]
            if tail.upper() != tail.lower():
                if tail == tail.upper():
                    return False

        return True

    @classmethod
    def expanded_outlook_distribution(cls, args, distribution):
        r"""
        Epic text paste will clean expanded outlook distribution

        upto:
            Claire Weinan; Damian Yurzola; Dan Ayotte; Deepti Reddy;

        from:
            Claire Weinan <Claire.Weinan@sandisk.com>; Damian Yurzola <Damian.Yurzola@sandisk.com>;\
            Dan Ayotte <Dan.Ayotte@sandisk.com>; Deepti Reddy <Deepti.Reddy@sandisk.com>;
        """
        import re
        distribution = re.sub(r'(.)(<.*?>)', r'\1', distribution)

        print('info: Text Paste:', distribution)

    @classmethod
    def outlook_distribution_email(cls, args, distribution):
        r"""
        Epic text paste will clean expanded outlook distribution

        upto:
            Claire.Weinan@sandisk.com; Damian.Yurzola@sandisk.com; Dan.Ayotte@sandisk.com; Deepti.Reddy@sandisk.com;

        from:
            Claire Weinan <Claire.Weinan@sandisk.com>; Damian Yurzola <Damian.Yurzola@sandisk.com>;\
            Dan Ayotte <Dan.Ayotte@sandisk.com>; Deepti Reddy <Deepti.Reddy@sandisk.com>;
        """
        import re
        # Reg-ex explanation :
        # Match two groups . Group 1 is name and group 2 is email without '<' or '>'. Replace the match with
        # group two and a ';'. Strip away the blank space at the end. You are left with just the emails seperated with ';' .
        distribution = re.sub(r'(.*?)<(.*?)>', r'\2; ', distribution).strip()

        print('info: Text Paste:', distribution)

    @classmethod
    def sprocketus_url_text_paste(cls, args, sprocket_url):
        r"""
        Epic text paste will clean SprocketUs Url

        upto:
            http://sprocketus.sandisk.com/forms/Lists/2014TechConf/NewForm.aspx

        from:
            http://sprocketus.sandisk.com/forms/Lists/2014TechConf/NewForm.aspx?\
            Source=http%3A%2F%2Fsprocketus%2Esandisk%2Ecom%2Fforms%2FLists%2F2014TechConf%2FAllItems%2Easpx&RootFolder=
        """
        if args.crash:
            sys.exit(['ERROR: Epic Text Paste: Raising an unhandled exception'])

        url = ''
        if sprocket_url.find('?') != -1:
            url = sprocket_url.split('?')[0]

        print('info: Text Paste:', url)

    @classmethod
    def sprocket_url_text_paste(cls, args, sprocket_url):
        r"""
        Epic text paste will clean SprocketUs Url

        upto:
            SprocketUs Ess > Eng > Firmware > Kilimanjaro > ProjectDocuments > ProjectSpecificProcesses

        from:
            http://sprocketus.sandisk.com/ess/eng/firmware/Kilimanjaro/ProjectDocuments/Forms/AllItems.aspx?\
            RootFolder=%2Fess%2Feng%2Ffirmware%2FKilimanjaro%2FProjectDocuments%2FProjectSpecificProcesses&FolderCTID\
            =0x01200076329E748FFC6647A270806629BA50B7&View=%7B03BBD70B-352C-4642-A177-3AD90C8A7AA2%7D
        """
        if args.crash:
            sys.exit(['ERROR: Epic Text Paste: Raising an unhandled exception'])

        url = ''
        if sprocket_url.find('?') != -1:
            url = sprocket_url.split('?')[1]
            elements = url.split('&')[0]
            elem = elements.split("=")[1]
            elem_list = elem.split('%2F')
            url = 'SprocketUs ' + ' > '.join(elem_list[1:])

        print('info: Text Paste:', url)

    @classmethod
    def extra_space_text_paste(cls, args, link_url):
        r"""
        Epic text paste will remove extra space per charecter in given url.

        upto:
            Svn Info URL: https://svnsdus.sandisk.com/svn/HEMi12/Firmware/branches/Integration

        from:
            S v n   I n f o   U R L :   h t t p s : / / s v n s d u s . s a n d i s k . c o m / s v n / H E M i 1 2 / F i r m w a r e / b r a n c h e s / I n t e g r a t i o n
        """
        if args.crash:
            sys.exit(['ERROR: Epic Text Paste: Raising an unhandled exception'])

        import re
        link_url = re.sub(r'(.) ', r'\1', link_url)

        print('info: Text Paste:', link_url)

    @classmethod
    def move_text_paste(cls, args):

        r"""Say hello from the Text Bot"""

        if args.crash:
            sys.exit(['ERROR: Epic Text Paste: Raising an unhandled exception'])

        print('info: Text Paste:', args.greetchars)


def def_textmuscle_doctests():

    r"""
    Def TextMuscle Doctests

    >>> import epicbots.textbot.textmuscle as textmuscle
    >>>

    ###
    ### Doctests of Move Text Paste
    ###

    >>> args = epic.space(crash=False, greetchars='a greeting')
    >>> textmuscle.TextMuscle.move_text_paste(args)
    info: Text Paste: ...greet...
    >>>

    >>> args = epic.space(crash=True, greetchars='a greeting')
    >>> textmuscle.TextMuscle.move_text_paste(args)
    Traceback (most recent call last):
    ...
    SystemExit: ['ERROR: Epic Text Paste: Raising an unhandled exception']
    >>>

    ###
    ### Doctests of Text Muscle
    ###

    >>> type(textmuscle.TextMuscle)
    <class 'type'>
    >>>

    >>> textmuscle.TextMuscle.is_title_or_camel('lower case')
    False
    >>> textmuscle.TextMuscle.is_title_or_camel('Sentence case')
    False
    >>> textmuscle.TextMuscle.is_title_or_camel(' Title Case ')
    True
    >>> textmuscle.TextMuscle.is_title_or_camel('CamelCase')
    True
    >>> textmuscle.TextMuscle.is_title_or_camel('UPPER CASE')
    False
    >>>

    >>> textmuscle.TextMuscle.is_title_or_camel('lowerCamelCase')
    False
    >>> textmuscle.TextMuscle.is_title_or_camel('-- Obscured By Dashes --')
    True
    >>>

    >>> args = epic.space(crash=False)
    >>> distribution = 'Claire Weinan <Claire.Weinan@sandisk.com>; Damian Yurzola <Damian.Yurzola@sandisk.com>; Dan Ayotte <Dan.Ayotte@sandisk.com>;'
    >>> textmuscle.TextMuscle.expanded_outlook_distribution(args, distribution)
    info: Text Paste: Claire Weinan ; Damian Yurzola ; Dan Ayotte ;
    >>>

    >>> args = epic.space(crash=False)
    >>> sprocket_url = 'http://sprocketus.sandisk.com/forms/Lists/2014TechConf/NewForm.aspx?Source=http%3A%2F%2Fsprocketus%2Esandisk%2Ecom%2Fforms%2FLists%2F2014TechConf%2FAllItems%2Easpx&RootFolder='
    >>> textmuscle.TextMuscle.sprocketus_url_text_paste(args, sprocket_url)
    info: Text Paste: http://sprocketus.sandisk.com/forms/Lists/2014TechConf/NewForm.aspx
    >>>

    >>> args = epic.space(crash=False)
    >>> sprocket_url = 'http://sprocketus.sandisk.com/ess/eng/firmware/Kilimanjaro/ProjectDocuments/Forms/AllItems.aspx?RootFolder=%2Fess%2Feng%2Ffirmware%2FKilimanjaro%2FProjectDocuments%2FProjectSpecificProcesses&FolderCTID=0x01200076329E748FFC6647A270806629BA50B7&View=%7B03BBD70B-352C-4642-A177-3AD90C8A7AA2%7D'
    >>> textmuscle.TextMuscle.sprocket_url_text_paste(args, sprocket_url)
    info: Text Paste: SprocketUs ess > eng > firmware > Kilimanjaro > ProjectDocuments > ProjectSpecificProcesses
    >>>

    >>> args = epic.space(crash=False)
    >>> link_url = 'S v n   I n f o   U R L :   h t t p s : / / s v n s d u s . s a n d i s k . c o m / s v n / H E M i 1 2 / F i r m w a r e / b r a n c h e s / I n t e g r a t i o n'
    >>> textmuscle.TextMuscle.extra_space_text_paste( args, link_url)
    info: Text Paste: Svn Info URL: https://svnsdus.sandisk.com/svn/HEMi12/Firmware/branches/Integration
    >>>

    """

