from pathlib import Path

import pytest

from invoke import MockContext, Result

from makevoke.base import MakevokeBase
from makevoke.exceptions import MakevokeContextError


def test_base_get_context():
    """
    Method get_context is pretty basic and should return all enabled context variables.
    """
    assert MakevokeBase.get_context() == {"BASE_DIR": Path(".")}

    class CustomMakevoke(MakevokeBase):
        YEP = True
        ENABLED_CONTEXT_VARS = MakevokeBase.ENABLED_CONTEXT_VARS + ["YEP"]

    assert CustomMakevoke.get_context() == {"BASE_DIR": Path("."), "YEP": True}


def test_base_get_context_error():
    """
    Method get_context should return an explicit exceptions for required enabled
    context variables when they don't exist.
    """
    class ErroneousMakevoke(MakevokeBase):
        ENABLED_CONTEXT_VARS = ["BASE_DIR", "NOPE"]

    with pytest.raises(MakevokeContextError) as excinfo:
        ErroneousMakevoke.get_context()

    assert str(excinfo.value) == (
        "Some enabled context variables in 'ENABLED_CONTEXT_VARS' are not defined "
        "as class attributes: NOPE"
    )

    class ErroneousMakevoke(MakevokeBase):
        niet = "nein"
        _PRIVATE = "no"
        ENABLED_CONTEXT_VARS = ["BASE_DIR", "_PRIVATE", "niet"]

    with pytest.raises(MakevokeContextError) as excinfo:
        ErroneousMakevoke.get_context()

    assert str(excinfo.value) == (
        "Context variable names can not starts with '_' and must be uppercase: "
        "_PRIVATE, niet"
    )


def test_base_run():
    """
    Very basic test around Makevoke 'run' method since Invoke only provide Mocking
    stuff to test it.
    """
    class ListingMakevoke(MakevokeBase):
        LS_BIN = "ls"
        ENABLED_CONTEXT_VARS = ["BASE_DIR", "LS_BIN"]

    assert ListingMakevoke.get_context() == {"BASE_DIR": Path("."), "LS_BIN": "ls"}

    # Register mocked up response for expected commands
    invoke_context = MockContext(run={
        "ls": Result("listing basic"),
        "ls -l": Result("listing list"),
    })

    # Simple usage with a pretty basic command coming from Makevoke context variables
    runned = ListingMakevoke.run(invoke_context, "{LS_BIN}")
    assert runned.command == "ls"
    assert runned.stdout == "listing basic"

    # Add usage of extra context to add to command
    runned = ListingMakevoke.run(
        invoke_context,
        "{LS_BIN} {args}",
        extra={"args": "-l"}
    )
    assert runned.command == "ls -l"
    assert runned.stdout == "listing list"
