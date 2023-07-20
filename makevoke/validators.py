from pathlib import Path


class MakevokeArgValidator:
    """
    This class implements some useful common methods to validate arguments.

    Since it depends on printout methods, it requires to be associated with a class
    which implements printout methods like in ``MakevokePrintOut``, either you use this
    class or implement it with another printer solution.
    """
    @classmethod
    def validate_path(
        cls,
        value,
        name="value",
        loglevel="critical",
        error_empty=(
            "Argument '{argname}' is required"
        ),
        error_doesnotexists=(
            "Argument '{argname}' path does not exists: {dest}"
        ),
    ):
        """
        Validate given path value is not empty and does exists.

        Arguments:
            value (string): A filesystem path.

        Keyword Arguments:
            name (string): Name to use in error message, defaut to 'value'.
            loglevel (string): The Makevoke method to use for print out error message.
                It must be a valid printout method like 'error' or 'warning'. Default
                to 'critical' which will also abort command (opposed to other methods).
            error_empty (string): Message to use if value is empty.
            error_doesnotexists (string): Message to use if value path does not exists.

        Returns:
            Path or boolean: Returns the coerced path to a Path object if validated.
            Returns None if value is empty. Returns False if path either does not
            exists or is a file.
        """
        if not value:
            getattr(cls, loglevel)(error_empty.format(argname=name))
            return None

        value = Path(value)

        if not value.exists():
            getattr(cls, loglevel)(
                error_doesnotexists.format(argname=name, dest=value)
            )
            return False

        return value

    @classmethod
    def validate_dir_path(
        cls,
        value,
        name="value",
        loglevel="critical",
        error_empty=(
            "Argument '{argname}' is required"
        ),
        error_doesnotexists=(
            "Argument '{argname}' path does not exists: {dest}"
        ),
        error_isfile=(
            "Argument '{argname}' path is a file: {dest}"
        ),
    ):
        """
        Validate given path value is not empty, does exists and is a directory.

        Arguments:
            value (string): A directory path.

        Keyword Arguments:
            name (string): Name to use in error message, defaut to 'value'.
            loglevel (string): The Makevoke method to use for print out error message.
                It must be a valid printout method like 'error' or 'warning'. Default
                to 'critical' which will also abort command (opposed to other methods).
            error_empty (string): Message to use if value is empty.
            error_doesnotexists (string): Message to use if value path does not exists.
            error_isfile (string): Message to use if value path is a file.

        Returns:
            Path or boolean: Returns the coerced path if validated. Returns None if
            value is empty. Returns False if path either does not exists or is a file.
        """
        value = cls.validate_path(
            value,
            name=name,
            loglevel=loglevel,
            error_empty=error_empty,
            error_doesnotexists=error_doesnotexists,
        )

        if value.is_file():
            getattr(cls, loglevel)(error_isfile.format(argname=name, dest=value))
            return False

        return value

    @classmethod
    def validate_file_path(
        cls,
        value,
        name="value",
        loglevel="critical",
        error_empty=(
            "Argument '{argname}' is required"
        ),
        error_doesnotexists=(
            "Argument '{argname}' path does not exists: {dest}"
        ),
        error_isdir=(
            "Argument '{argname}' path is a directory: {dest}"
        ),
    ):
        """
        Validate given path value is not empty, does exists and is a file.

        Arguments:
            value (string): A file path.

        Keyword Arguments:
            name (string): Name to use in error message, defaut to 'value'.
            loglevel (string): The Makevoke method to use for print out error message.
                It must be a valid printout method like 'error' or 'warning'. Default
                to 'critical' which will also abort command (opposed to other methods).
            error_empty (string): Message to use if value is empty.
            error_doesnotexists (string): Message to use if value path does not exists.
            error_isdir (string): Message to use if value path is a directory.

        Returns:
            Path or boolean: Returns the coerced path if validated. Returns None if
            value is empty. Returns False if path either does not exists or is a file.
        """
        value = cls.validate_path(
            value,
            name=name,
            loglevel=loglevel,
            error_empty=error_empty,
            error_doesnotexists=error_doesnotexists,
        )

        if value.is_dir():
            getattr(cls, loglevel)(error_isdir.format(argname=name, dest=value))
            return False

        return value
