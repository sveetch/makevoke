PYTHON_INTERPRETER=python3

VENV_PATH=.venv

FLAKE_BIN=$(VENV_PATH)/bin/flake8
PIP_BIN=$(VENV_PATH)/bin/pip
PYTEST_BIN=$(VENV_PATH)/bin/pytest
PYTHON_BIN=$(VENV_PATH)/bin/python
SPHINX_RELOAD_BIN=$(PYTHON_BIN) docs/sphinx_reload.py
TOX_BIN=$(VENV_PATH)/bin/tox
TWINE_BIN=$(VENV_PATH)/bin/twine

PACKAGE_NAME=makevoke
PACKAGE_SLUG=`echo $(PACKAGE_NAME) | tr '-' '_'`
APPLICATION_NAME=makevoke

help:
	@echo "Please use `make <target>' where <target> is one of"
	@echo
	@echo "  venv                      -- to install virtual environment with virtualenv"
	@echo "  install-backend           -- to install or update backend requirements with Pip (you need to have used 'venv' or 'install' task before)"
	@echo "  install                   -- to install everything with virtualenv and Pip"
	@echo "  freeze-dependencies       -- to write a frozen.txt file with installed dependencies versions"
	@echo
	@echo "  clean                     -- to clean EVERYTHING (Warning)"
	@echo "  clean-doc                 -- to remove documentation builds"
	@echo "  clean-install             -- to clean Python side installation"
	@echo "  clean-pycache             -- to remove all __pycache__, this is recursive from current directory"
	@echo
	@echo "  docs                      -- to build documentation"
	@echo "  livedocs                  -- to run livereload server to rebuild documentation on source changes"
	@echo
	@echo "  flake                     -- to launch Flake8 checking"
	@echo "  test                      -- to launch base test suite using Pytest"
	@echo "  tox                       -- to launch tests for every Tox environments"
	@echo "  quality                   -- to launch Flake8 checking, tests suites, documentation building, freeze dependancies and check release"
	@echo
	@echo "  check-release             -- to check package release before uploading it to PyPi"
	@echo "  release                   -- to release package for latest version on PyPi (once release has been pushed to repository)"
	@echo

clean-pycache:
	@echo ""
	@echo "==== Clear Python cache ===="
	@echo ""
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-install:
	@echo ""
	@echo "==== Clear installation ===="
	@echo ""
	rm -Rf $(VENV_PATH)
	rm -Rf $(PACKAGE_SLUG).egg-info
.PHONY: clean-install

clean-doc:
	@echo ""
	@echo "==== Clear documentation ===="
	@echo ""
	rm -Rf docs/_build
.PHONY: clean-doc

clean: clean-doc clean-install clean-pycache
.PHONY: clean

venv:
	@echo ""
	@echo "==== Install virtual environment ===="
	@echo ""
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
.PHONY: venv

install-backend:
	@echo ""
	@echo "==== Install backend requirements ===="
	@echo ""
	$(PIP_BIN) install -e .[dev,quality,doc]
.PHONY: install-backend

install: venv install-backend
	@echo ""
	@echo "==== Install everything for development ===="
	@echo ""
.PHONY: install

docs:
	@echo ""
	@echo "==== Build documentation ===="
	@echo ""
	cd docs && make html
.PHONY: docs

livedocs:
	@echo ""
	@echo "==== Watching documentation sources ===="
	@echo ""
	$(SPHINX_RELOAD_BIN)
.PHONY: livedocs

flake:
	@echo ""
	@echo "==== Flake ===="
	@echo ""
	$(FLAKE_BIN) --show-source $(APPLICATION_NAME) tests
.PHONY: flake

test:
	@echo ""
	@echo "==== Tests ===="
	@echo ""
	$(PYTEST_BIN) -vv tests/
.PHONY: test

freeze:
	@echo ""
	@echo "==== Freeze dependencies versions ===="
	@echo ""
	$(PYTHON_BIN) freezer.py
.PHONY: freeze

build-package:
	@echo ""
	@echo "==== Build package ===="
	@echo ""
	rm -Rf dist
	$(PYTHON_BIN) setup.py sdist
.PHONY: build-package

release: build-package
	@echo ""
	@echo "==== Release ===="
	@echo ""
	$(TWINE_BIN) upload dist/*
.PHONY: release

check-release: build-package
	@echo ""
	@echo "==== Check package ===="
	@echo ""
	$(TWINE_BIN) check dist/*
.PHONY: check-release

tox:
	@echo ""
	@echo "==== Launch all Tox environments ===="
	@echo ""
	$(TOX_BIN)
.PHONY: tox

quality: test flake docs check-release freeze
	@echo ""
	@echo "♥ ♥ Everything should be fine ♥ ♥"
	@echo ""
.PHONY: quality
