pygame.org website |build-status| |coverage-status|
===================================================

Pieces of the pygame website will be open sourced here.

Strategy is to bring in code one piece at a time, and clean it up as I go.


Contributing
============

Please discuss contributions first to avoid disapointment and rework.

Please see `contribution-guide.org <http://www.contribution-guide.org/>`_ and
`Python Code of Conduct <https://www.python.org/psf/codeofconduct/>`_ for
details on what we expect from contributors. Thanks!

The stack is something like: python 3.6, postgresql 9.6, Flask, py.test, sqlalchemy, alembic, gulp, ansible, node.


Quickstart
==========

Set up the required packages::

    python3.6 -m venv anenv
    . ./anenv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.dev.txt
    pip install -e .


For now yuicompressor is needed for css compression::

    brew install yuicompressor node
    apt-get install yui-compressor node


Environment setup
=================

cp example.env .env


Tool setup
==========

See setup.cfg for all tool config (pytest, coverage, etc).



Db setup instructions
=====================

postgresql 9.6

One database for testing, and another one for running the app.

We use alembic for db migrations. http://alembic.readthedocs.org/en/latest/


Set up the postgresql database::

    createdb pygame
    psql pygame -c "CREATE USER pygame WITH PASSWORD 'password';"
    psql pygame -c "GRANT ALL PRIVILEGES ON DATABASE pygame to pygame;"

We also create a database for running tests::

    createdb pygame_test
    psql pygame -c "CREATE USER pygame_test WITH PASSWORD 'password';"
    psql pygame_test -c "GRANT ALL PRIVILEGES ON DATABASE pygame_test to pygame_test;"


To upgrade to latest model changes do::

    alembic upgrade head


When you change a model make an alembic revision::

    alembic revision --autogenerate -m "Added a field for these reasons."

Then you will need to apply the change to your db (and commit the version file)::

    alembic upgrade head


testing with pytest
===================

http://docs.pytest.org/en/latest/

To run all unit tests and functional tests use::

    pytest

To watch for changes and rerun tests::

    ptw

Maybe you just want to test the wiki parts::

    pytest -k wiki


tests/unit/ are for unit tests.
tests/functional/ are for tests which would use flask and db.
tests/conftest.py is for test configuration.
tests/sqlpytestflask.py are some fixtures for db testing.

Unit tests and functional tests are kept separate, because functional tests can take a while longer to run.

We use various fixtures to make writing the tests easier and faster.


Running the webserver locally
=============================

can be done by using the executable pygameweb_front.


Templates with jinja2 and bootstrap
===================================

pygameweb/templates/

We use::

    * `Jinja2 <http://jinja.pocoo.org/>`_
    * `Flask-Bootstrap <https://pythonhosted.org/Flask-Bootstrap/basic-usage.html>`_
    * `Bootstrap <http://getbootstrap.com/>`_


Command line tools with click
=============================

We use click and setuptools entry points (in setup.py) for command line tools::

    * `click <http://click.pocoo.org/5/>`_
    * `entry points <https://packaging.python.org/distributing/#entry-points>`_

Note, when you add or change a command line tool, you need to `pip install -e .` again.

If you can, try not to use command line options at all. Have one command do one thing,
and make the defaults good, or use the pygameweb.config.


User login with Flask-security-fork
===================================

pygameweb.user
pygameweb/templates/security

Using::

    * `flask-security-fork <https://flask-security-fork.readthedocs.io/en/latest/quickstart.html>`_


Navigation with flask-nav
=========================

pygameweb.nav
pygameweb.page.models

Using::

    * `flask-nav <http://pythonhosted.org/flask-nav/>`_
    * `flask-bootstrap <https://pythonhosted.org/Flask-Bootstrap/nav.html>`_



Dashboard is an overview
========================

of all sorts of things happening in the pygame worlds around the interwebs.

https://pygame.org/dashboard

It's a 7000px wide webpage offering a summary of what's happening.

Projects people are working on,
videos folks are making,
tweets twits are... tweeting,
questions asked and answered.



To caching things we
====================

use `Flask-Caching <http://pythonhosted.org/Flask-Caching/>`_

pygameweb.cache
pygameweb.news.views


With with a @cache decorator, and/or markup in a template.



.. |build-status| image:: https://travis-ci.org/pygame/pygameweb.svg?branch=master
   :target: https://travis-ci.org/pygame/pygameweb
   :alt: Build status
.. |coverage-status| image:: https://coveralls.io/repos/github/pygame/pygameweb/badge.svg?branch=master
   :target: https://coveralls.io/github/pygame/pygameweb?branch=master
   :alt: Test coverage percentage
