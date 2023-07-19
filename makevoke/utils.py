import re


def clean_ansi(value):
    """
    Remove ANSI code from a string (not bytes object).

    .. Note::
        Code has been stealed and adapted
        from: https://github.com/ewen-lbh/python-strip-ansi

    Arguments:
        value (string): A string for which to remove its included ANSI codes.

    Returns:
        string: Given value with all ANSI codes removed.
    """
    pattern = re.compile(r"\x1B\[\d+(;\d+){0,2}m")
    return pattern.sub("", value)
