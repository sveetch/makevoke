from invoke.exceptions import Exit

from colorama import Fore, Back, Style


# TODO: Fix output for ANSI code support on windows
# just_fix_windows_console()


class MakevokePrintOut:
    """
    This class implements all methods to print out text with styles using normalized
    ANSI codes.

    .. Note::
        ANSI code management may require to use a reset code that cannot be twice in
        a same output (like from ``print()``), once used in an output all ANSI code
        following are just ignored.

        Due to this, you may not be able to combine some styles.
    """
    HEADER_SURROUND = ("---> ", " <---")
    SUCCESS_SURROUND = ("  ", "  ")
    CRITICAL_SURROUND = ("  ", "  ")
    INDENT_STRING = "    "

    UnderlineAnsiCode = "\u001b[4m"
    BoldAnsiCode = "\u001b[1m"

    @classmethod
    def get_indent(cls, indent=0):
        """
        Compute indentation string from given level.

        Keyword Arguments:
            indent (integer): Indentation level to apply at start of the string. If
                higher than 0 it will repeat the indentation character from Makefile
                attribute ``INDENT_STRING``. Default to 0, there won't be any
                indentation.
        """
        return cls.INDENT_STRING * indent

    @classmethod
    def header(cls, msg):
        """
        Print a message in white on blue background and surrounded.

        Arguments:
            msg (string): A simple string to print out.
        """
        print()
        print(
            Back.BLUE + Style.BRIGHT + cls.HEADER_SURROUND[0] + str(msg) +
            cls.HEADER_SURROUND[1] + Style.RESET_ALL
        )
        print()

    @classmethod
    def info(cls, msg):
        """
        Print a message text in green.

        Arguments:
            msg (string): A simple string to print out.
        """
        print(Fore.GREEN + str(msg) + Style.RESET_ALL)

    @classmethod
    def title_info(cls, msg):
        """
        Print a message text in bold, green, underlined with a following empty line.

        Arguments:
            msg (string): A simple string to print out.
        """
        cls.info(cls.UnderlineAnsiCode + cls.BoldAnsiCode + msg)
        print()

    @classmethod
    def warning(cls, msg):
        """
        Print a message text in yellow.

        Arguments:
            msg (string): A simple string to print out.
        """
        print(Fore.YELLOW + str(msg) + Style.RESET_ALL)

    @classmethod
    def title_warning(cls, msg):
        """
        Print a message text in bold, yellow, underlined with a following empty line.

        Arguments:
            msg (string): A simple string to print out.
        """
        cls.warning(cls.UnderlineAnsiCode + cls.BoldAnsiCode + msg)
        print()

    @classmethod
    def error(cls, msg):
        """
        Print a message text in red.

        Arguments:
            msg (string): A simple string to print out.
        """
        print(Fore.RED + str(msg) + Style.RESET_ALL)

    @classmethod
    def title_error(cls, msg):
        """
        Print a message text in bold, red, underlined with a following empty line.

        Arguments:
            msg (string): A simple string to print out.
        """
        cls.error(cls.UnderlineAnsiCode + cls.BoldAnsiCode + msg)
        print()

    @classmethod
    def success(cls, msg):
        """
        Print a message in white on green background and surrounded with spaces.

        Arguments:
            msg (string): A simple string to print out.
        """

        print()
        print(
            Back.GREEN + Style.BRIGHT + cls.SUCCESS_SURROUND[0] + str(msg) +
            cls.SUCCESS_SURROUND[1] + Style.RESET_ALL
        )
        print()

    @classmethod
    def critical(cls, msg):
        """
        Print an error message in white on red backgroun then raise Exit() exception
        to ensure correct exit code.

        Arguments:
            msg (string): A simple string to print out.
        """

        print()
        print(
            Back.RED + Style.BRIGHT + cls.CRITICAL_SURROUND[0] + str(msg) +
            cls.CRITICAL_SURROUND[1] + Style.RESET_ALL
        )
        print()
        raise Exit()

    @classmethod
    def dotitem(cls, msg, indent=0):
        """
        Print a message with a leading dot.

        Arguments:
            msg (string): A simple string to print out.

        Keyword Arguments:
            indent (integer): Indentation level to apply at start of the string. If
                higher than 0 it will repeat the indentation character from Makefile
                attribute ``INDENT_STRING``. Default to 0, there won't be any
                indentation.
        """
        print(Fore.BLUE + cls.get_indent(indent) + "▪ " + Style.RESET_ALL + str(msg))

    @classmethod
    def treeitem(cls, msg, ends=False, indent=0):
        """
        Print a message prefixed with a Unicode character for a tree alike display.

        Arguments:
            msg (string): A simple string to print out.

        Keyword Arguments:
            indent (integer): Indentation level to apply at start of the string. If
                higher than 0 it will repeat the indentation character from Makefile
                attribute ``INDENT_STRING``. Default to 0, there won't be any
                indentation.
        """
        char = "├── " if not ends else "└── "
        print(Fore.BLUE + cls.get_indent(indent) + char + Style.RESET_ALL + str(msg))

    @classmethod
    def treelist(cls, items, indent=0):
        """
        Convenient method to use treeitem on each item of a list.

        Arguments:
            items (list): A list of strings to print out as tree items.

        Keyword Arguments:
            indent (integer): Indentation level to give to Makefile method
                ``treeitem``. Default to 0, there won't be any indentation.
        """
        total = len(items)

        for i, item in enumerate(items, start=1):
            cls.treeitem(item, ends=(i == total), indent=indent)

    @classmethod
    def yes_or_no(cls, value, colored=True):
        """
        Return a string depending the given value is true or false.

        Arguments:
            value (string): A simple string to print out.

        Keyword Arguments:
            colored (boolean): If True the returned string includes ANSI code to
                color the output. If False, there won't be any ANSI code. Default to
                True.

        Returns:
            string: Either the unicode character "✔" colored in green when value is
            True or "✖" colored in red if the value is False.
        """
        character = "✔" if value else "✖"

        if colored:
            return (Fore.GREEN if value else Fore.RED) + character + Style.RESET_ALL

        return character

    @classmethod
    def styleguide(cls):
        """
        This should demonstrate all available printout methods.
        """
        print("It is a sample 'print()'.")

        print("It is a sample 'print()' including '{}' from 'yes_or_no(True)'.".format(
            cls.yes_or_no(True)
        ))

        print("It is a sample 'print()' including '{}' from 'yes_or_no(False)'.".format(
            cls.yes_or_no(False)
        ))

        cls.info("It is an 'info' line including '{}' from 'yes_or_no(False)'.".format(
            cls.yes_or_no(False)
        ))

        cls.info((
            "It is an 'info' line including '{}' from "
            "'yes_or_no(False, colored=False)'."
        ).format(
            cls.yes_or_no(False, colored=False)
        ))

        cls.info((
            "{} 'info' line prefixed from 'yes_or_no(False)' (Ansi is broken)."
        ).format(
            cls.yes_or_no(False)
        ))

        cls.info((
            "'info' line suffixed from 'yes_or_no(False)'. {}"
        ).format(
            cls.yes_or_no(False)
        ))

        cls.header("This is a 'header'.")

        cls.title_info("This is a 'title_info' title.")

        cls.info("This is an 'info' line.")

        cls.title_warning("This is a 'title_warning' title.")

        cls.warning("This is a 'warning' line.")

        cls.title_error("This is a 'title_error' title.")

        cls.error("This is a 'error' line.")

        cls.dotitem("This is a 'dotitem' line.")

        cls.treeitem("This is a 'treeitem' line.")

        cls.treeitem("This is a 'treeitem' line with ends=True.", ends=True)

        cls.treelist(["First item with treelist", "Another one"])

        cls.success("This is a 'success' block.")

        try:
            cls.critical(
                "This is a 'critical' block (in real usage it will abort script)."
            )
        except Exit:
            pass
