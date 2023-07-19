#!/usr/bin/env python
"""
A script to launch a livereload server to watch and rebuild documentation
on some sources changes.

You need to have project with development requirements to use it.

Once launched, server will be available on port 8002, like: ::

    http://localhost:8002/

Borrowed from: ::

    https://livereload.readthedocs.io/en/latest/#script-example-sphinx

"""
from pathlib import Path

from livereload import Server, shell

DOC_PATH = Path(__file__).parents[0].resolve()
PROJECT_PATH = DOC_PATH.parent

server = Server()

# Watch documents
server.watch("docs/*.rst", shell("make html", cwd="docs"))
server.watch("docs/*/**.rst", shell("make html", cwd="docs"))

# Watch code sources
server.watch("makevoke/*.py", shell("make html", cwd="docs"))
server.watch("makevoke/*/**.py", shell("make html", cwd="docs"))

# Serve built documentation
server.serve(root=DOC_PATH / "_build/html", port=8002, host="0.0.0.0", debug=True)
