from pathlib import Path

import pytest

from invoke.exceptions import Exit

from makevoke.printout import MakevokePrintOut
from makevoke.validators import MakevokeArgValidator
from makevoke.utils import clean_ansi


class MakevokePrintoutValidator(MakevokeArgValidator, MakevokePrintOut):
    pass


@pytest.fixture(scope="function")
def basic_structure(tmp_path):
    """
    Create a basic file and directory structure for tests
    """
    structure = tmp_path / "basic"

    dir_foo = structure / "foo"
    dir_ping = structure / "ping"

    dir_foo.mkdir(parents=True)
    dir_ping.mkdir(parents=True)

    file_bar = dir_foo / "bar.txt"
    file_pong = dir_ping / "pong.txt"

    file_bar.write_text("Foobar!")
    file_pong.write_text("Ping! Pong!")

    return structure


def test_validate_path_failures_critical(capsys, basic_structure):
    """
    Method should fails with exception for empty path and non existing path.
    """
    # Expected to fail with empty path value
    with pytest.raises(Exit):
        MakevokePrintoutValidator.validate_path("", name="nope-path")

    captured = capsys.readouterr()
    assert clean_ansi(captured.out) == (
        "\n  Argument 'nope-path' is required  \n\n"
    )

    # Expected to fail with non existing path
    with pytest.raises(Exit):
        MakevokePrintoutValidator.validate_path(
            basic_structure / "nope",
            name="nope-path"
        )

    captured = capsys.readouterr()
    assert clean_ansi(captured.out) == (
        "\n  Argument 'nope-path' path does not exists: "
        "{}/nope  \n\n"
    ).format(basic_structure)


def test_validate_path_failures_nonblocking(capsys, basic_structure):
    """
    Method should fails without exception for empty path and non existing path.
    """
    # Empty path value with non blocking log level, return None without raising
    # exception
    result = MakevokePrintoutValidator.validate_path(
        "",
        name="nope-path",
        loglevel="error"
    )
    assert result is None
    captured = capsys.readouterr()
    assert clean_ansi(captured.out) == "Argument 'nope-path' is required\n"

    # Non existing path with non blocking log level, return False without raising
    # exception
    result = MakevokePrintoutValidator.validate_path(
        basic_structure / "nope",
        name="nope-path",
        loglevel="error"
    )
    assert result is False
    captured = capsys.readouterr()
    assert clean_ansi(captured.out) == (
        "Argument 'nope-path' path does not exists: {}/nope\n"
    ).format(basic_structure)


def test_validate_path_failures_custom_messages(capsys, basic_structure):
    """
    Method should fails without exception for empty path and non existing path.
    """
    # Empty path value with non blocking log level, return None without raising
    # exception
    result = MakevokePrintoutValidator.validate_path(
        "",
        name="nope-path",
        loglevel="error",
        error_empty=(
            "blip '{argname}' blop"
        ),
    )
    assert result is None
    captured = capsys.readouterr()
    assert clean_ansi(captured.out) == "blip 'nope-path' blop\n"

    # Non existing path with non blocking log level, return False without raising
    # exception
    result = MakevokePrintoutValidator.validate_path(
        basic_structure / "nope",
        name="nope-path",
        loglevel="error",
        error_doesnotexists=(
            "blap '{argname}' blup {dest}"
        ),
    )
    assert result is False
    captured = capsys.readouterr()
    assert clean_ansi(captured.out) == (
        "blap 'nope-path' blup {}/nope\n"
    ).format(basic_structure)


def test_validate_path_success(basic_structure):
    """
    Method should succeed for any existing path.
    """
    dir_foo = basic_structure / "foo"
    file_bar = dir_foo / "bar.txt"

    # Expected to work with existing directory path
    result = MakevokePrintoutValidator.validate_path(dir_foo, name="dir-foo")
    assert isinstance(result, Path) is True
    assert str(result) == str(dir_foo)

    # Expected to work with existing file path
    result = MakevokePrintoutValidator.validate_path(file_bar, name="file-bar")
    assert isinstance(result, Path) is True
    assert str(result) == str(file_bar)


def test_validate_dir_path(capsys, basic_structure):
    """
    Method should fails for empty, non existing, if path is a file and succeed for
    any existing directory path.
    """
    dir_foo = basic_structure / "foo"
    file_bar = dir_foo / "bar.txt"

    # Expected to fail with empty path value
    with pytest.raises(Exit):
        MakevokePrintoutValidator.validate_dir_path("", name="nope-path")

    # Expected to fail with non existing path
    with pytest.raises(Exit):
        MakevokePrintoutValidator.validate_dir_path(
            basic_structure / "nope",
            name="nope-path"
        )

    # Flush stdout
    capsys.readouterr()

    # Expected to work with existing directory path
    result = MakevokePrintoutValidator.validate_dir_path(dir_foo, name="dir-foo")
    assert isinstance(result, Path) is True
    assert str(result) == str(dir_foo)

    # Expected to work with existing file path
    with pytest.raises(Exit):
        MakevokePrintoutValidator.validate_dir_path(file_bar, name="file-bar")

    captured = capsys.readouterr()
    assert clean_ansi(captured.out) == (
        "\n  Argument 'file-bar' path is a file: {}  \n\n"
    ).format(file_bar)


def test_validate_file_path(capsys, basic_structure):
    """
    Method should fails for empty, non existing, if path is a file and succeed for
    any existing directory path.
    """
    dir_foo = basic_structure / "foo"
    file_bar = dir_foo / "bar.txt"

    # Expected to fail with empty path value
    with pytest.raises(Exit):
        MakevokePrintoutValidator.validate_file_path("", name="nope-path")

    # Expected to fail with non existing path
    with pytest.raises(Exit):
        MakevokePrintoutValidator.validate_file_path(
            basic_structure / "nope",
            name="nope-path"
        )

    # Flush stdout
    capsys.readouterr()

    # Expected to work with existing file path
    result = MakevokePrintoutValidator.validate_file_path(file_bar, name="file-bar")
    assert isinstance(result, Path) is True
    assert str(result) == str(file_bar)

    # Expected to work with existing directory path
    with pytest.raises(Exit):
        MakevokePrintoutValidator.validate_file_path(dir_foo, name="dir-foo")

    captured = capsys.readouterr()
    assert clean_ansi(captured.out) == (
        "\n  Argument 'dir-foo' path is a directory: {}  \n\n"
    ).format(dir_foo)
