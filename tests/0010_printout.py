import pytest

from colorama import Fore, Back, Style
from invoke.exceptions import Exit

from makevoke.printout import PrintOutAbstract
from makevoke.utils import clean_ansi


def test_get_indent():
    """
    Method should return correct computed indentation.
    """
    assert PrintOutAbstract.get_indent(0) == ""
    assert PrintOutAbstract.get_indent(1) == "    "
    assert PrintOutAbstract.get_indent(2) == "        "

    class CustomMakevoke(PrintOutAbstract):
        INDENT_STRING = "-"

    assert CustomMakevoke.get_indent(0) == ""
    assert CustomMakevoke.get_indent(4) == "----"


def test_yes_or_no():
    """
    Method should returns the right character depending value is True or False, and
    possibly colored with ANSI code depending 'colored' argument.
    """
    assert PrintOutAbstract.yes_or_no(True) == Fore.GREEN + "✔" + Style.RESET_ALL
    assert PrintOutAbstract.yes_or_no(False) == Fore.RED + "✖" + Style.RESET_ALL
    assert PrintOutAbstract.yes_or_no(True, colored=False) == "✔"
    assert PrintOutAbstract.yes_or_no(False, colored=False) == "✖"


def test_header_ansi(capsys):
    """
    Header block should be rendered as expected.

    NOTE: This will be the only test to check about ANSI codes to avoid messing tests
    for no real value.
    """
    PrintOutAbstract.header("Header")

    captured = capsys.readouterr()
    assert captured.out == (
        "\n" + Back.BLUE + Style.BRIGHT + "  Header  " + Style.RESET_ALL + "\n\n"
    )


@pytest.mark.parametrize("text, style, options, expected", [
    (
        "Info",
        "info",
        {},
        "Info\n",
    ),
    (
        "Info title",
        "title_info",
        {},
        "Info title\n\n",
    ),
    (
        "Info block",
        "block_info",
        {},
        "\n  Info block  \n\n",
    ),
    (
        "Success",
        "success",
        {},
        "Success\n",
    ),
    (
        "Success title",
        "title_success",
        {},
        "Success title\n\n",
    ),
    (
        "Success block",
        "block_success",
        {},
        "\n  Success block  \n\n",
    ),
    (
        "Warning",
        "warning",
        {},
        "Warning\n",
    ),
    (
        "Warning title",
        "title_warning",
        {},
        "Warning title\n\n",
    ),
    (
        "Warning block",
        "block_warning",
        {},
        "\n  Warning block  \n\n",
    ),
    (
        "Error",
        "error",
        {},
        "Error\n",
    ),
    (
        "Error title",
        "title_error",
        {},
        "Error title\n\n",
    ),
    (
        "Error block",
        "block_error",
        {},
        "\n  Error block  \n\n",
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
        getattr(PrintOutAbstract, style)(text)
    else:
        getattr(PrintOutAbstract, style)(text, **options)

    captured = capsys.readouterr()
    assert clean_ansi(captured.out) == expected


def test_critical(capsys):
    """
    Alike a basic style method but it should raise an Invoke 'Exit' exception.
    """
    with pytest.raises(Exit):
        PrintOutAbstract.critical("Critical block")

    captured = capsys.readouterr()
    assert clean_ansi(captured.out) == "\n  Critical block  \n\n"


def test_styleguide(capsys):
    """
    Method should output content using Makefile style methode without any error.
    """
    PrintOutAbstract.styleguide()

    captured = capsys.readouterr()
    assert len(clean_ansi(captured.out)) > 0
