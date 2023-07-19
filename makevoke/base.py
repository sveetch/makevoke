from pathlib import Path

from .exceptions import MakevokeContextError


class MakevokeBase:
    """
    Base implements context builder and command runner.
    """
    BASE_DIR = Path(".")
    ENABLED_CONTEXT_VARS = [
        "BASE_DIR",
    ]

    @classmethod
    def get_context(cls, extra=None):
        """
        Return Makefile context.

        Context is just a set of variables enabled from ``ENABLED_CONTEXT_VARS``
        attribute. All of these variables are expected to be set as Makefile attributes.

        Keyword Arguments:
            extra (dict): Optionnal dictionnary to add or override some items into the
                base context.

        Returns:
            dict: All enabled context variables.
        """
        extra = extra or {}

        unfound = [
            name
            for name in getattr(cls, "ENABLED_CONTEXT_VARS", [])
            if not hasattr(cls, name)
        ]
        if unfound:
            raise MakevokeContextError(
                (
                    "Some enabled context variables in 'ENABLED_CONTEXT_VARS' are not "
                    "defined as class attributes: {names}"
                ).format(
                    names=", ".join(unfound)
                )
            )

        invalid = [
            name
            for name in getattr(cls, "ENABLED_CONTEXT_VARS", [])
            if (not name.isupper() or name.startswith("_"))
        ]
        if invalid:
            raise MakevokeContextError(
                (
                    "Context variable names can not starts with '_' and must be "
                    "uppercase: {names}"
                ).format(
                    names=", ".join(invalid)
                )
            )

        context = {
            name: getattr(cls, name)
            for name in getattr(cls, "ENABLED_CONTEXT_VARS", [])
        }

        if extra:
            context.update(extra)

        return context

    @classmethod
    def run(cls, inv, commandline, extra=None, **kwargs):
        """
        Format given command line with Makefile context then run it with given
        'invoke' instance.

        Arguments:
            inv (invoke): Invoke instance.
            commandline (string): Command line with possible patterns for context
                variables.
            **kwargs: Any keyword arguments are passed to 'invoke' runner (except
            ``extra``).

        Keyword Arguments:
            extra (dict): A dictionnary for extra variable to pass into
                Makefile context. Default to an empty dict.

        Returns:
            invoke.runners.Result: Returned result from 'invoke' runner.
        """
        extra = extra or {}

        return inv.run(
            commandline.format(**cls.get_context(extra=extra)),
            **kwargs,
        )


class MakevokeVirtualEnvBase(MakevokeBase):
    """
    Base to set base context variables for a 'virtualenv' architecture.
    """
    BASE_DIR = Path(".")
    PYTHON_INTERPRETER = "python3"
    VENV_PATH = BASE_DIR / ".venv"
    BIN_PATH = VENV_PATH / "bin"
    PYTHON_BIN = BIN_PATH / "python"
    INVOKE_BIN = BIN_PATH / "invoke"
    ENABLED_CONTEXT_VARS = [
        "BASE_DIR",
        "BIN_PATH",
        "ENABLED_CONTEXT_VARS",
        "PYTHON_BIN",
        "PYTHON_INTERPRETER",
        "VENV_PATH",
    ]
