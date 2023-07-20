import pytest

from colorama import Fore, Back, Style
from invoke.exceptions import Exit

from makevoke.printout import MakevokePrintOut
from makevoke.utils import clean_ansi


def test_get_indent():
    """
    Method should return correct computed indentation.
    """
    assert MakevokePrintOut.get_indent(0) == ""
    assert MakevokePrintOut.get_indent(1) == "    "
    assert MakevokePrintOut.get_indent(2) == "        "

    class CustomMakevoke(MakevokePrintOut):
        INDENT_STRING = "-"

    assert CustomMakevoke.get_indent(0) == ""
    assert CustomMakevoke.get_indent(4) == "----"


def test_yes_or_no():
    """
    Method should returns the right character depending value is True or False, and
    possibly colored with ANSI code depending 'colored' argument.
    """
    assert MakevokePrintOut.yes_or_no(True) == Fore.GREEN + "✔" + Style.RESET_ALL
    assert MakevokePrintOut.yes_or_no(False) == Fore.RED + "✖" + Style.RESET_ALL
    assert MakevokePrintOut.yes_or_no(True, colored=False) == "✔"
    assert MakevokePrintOut.yes_or_no(False, colored=False) == "✖"


def test_header_ansi(capsys):
    """
    Header block should be rendered as expected.

    NOTE: This will be the only test to check about ANSI codes to avoid messing tests
    for no real value.
    """
    MakevokePrintOut.header("Header")

    captured = capsys.readouterr()
    assert captured.out == (
        "\n" + Back.BLUE + Style.BRIGHT + "---> Header <---" + Style.RESET_ALL + "\n\n"
    )


@pytest.mark.parametrize("text, style, options, expected", [
    (
        "Info",
        "info",
        {},
        "Info\n",
    ),
    (
        "Warning",
        "warning",
        {},
        "Warning\n",
    ),
    (
        "Error",
        "error",
        {},
        "Error\n",
    ),
    (
        "Info title",
        "title_info",
        {},
        "Info title\n\n",
    ),
    (
        "Warning title",
        "title_warning",
        {},
        "Warning title\n\n",
    ),
    (
        "Error title",
        "title_error",
        {},
        "Error title\n\n",
    ),
    (
        "Success block",
        "success",
        {},
        "\n  Success block  \n\n",
    ),
    (
        "Dotitem line",
        "dotitem",
        {},
        "▪ Dotitem line\n",
    ),
    (
        "Dotitem line",
        "dotitem",
        {"indent": 1},
        "    ▪ Dotitem line\n",
    ),
    (
        "Treeitem line",
        "treeitem",
        {},
        "├── Treeitem line\n",
    ),
    (
        "Treeitem line",
        "treeitem",
        {"indent": 1},
        "    ├── Treeitem line\n",
    ),
    (
        "Treeitem line",
        "treeitem",
        {"ends": True},
        "└── Treeitem line\n",
    ),
    (
        "Treeitem line",
        "treeitem",
        {"ends": True, "indent": 1},
        "    └── Treeitem line\n",
    ),
    (
        ("One", "Two", "Three"),
        "treelist",
        {},
        "├── One\n├── Two\n└── Three\n",
    ),
    (
        ("One", "Two", "Three"),
        "treelist",
        {"indent": 1},
        "    ├── One\n    ├── Two\n    └── Three\n",
    ),
])
def test_basic_styles(capsys, text, style, options, expected):
    """
    All basic style methods should print out expected content. This is mostly about
    proper linebreaks and proper text content since we clean out all ANSI code from
    result before to assert.
    """
    if not options:
        getattr(MakevokePrintOut, style)(text)
    else:
        getattr(MakevokePrintOut, style)(text, **options)

    captured = capsys.readouterr()
    assert clean_ansi(captured.out) == expected


def test_critical(capsys):
    """
    Alike a basic style method but it should raise an Invoke 'Exit' exception.
    """
    with pytest.raises(Exit):
        MakevokePrintOut.critical("Critical block")

    captured = capsys.readouterr()
    assert clean_ansi(captured.out) == "\n  Critical block  \n\n"


def test_styleguide(capsys):
    """
    Method should output content using Makefile style methode without any error.
    """
    MakevokePrintOut.styleguide()

    captured = capsys.readouterr()
    assert len(clean_ansi(captured.out)) > 0
