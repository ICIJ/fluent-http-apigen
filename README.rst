About
=====

.. image:: https://circleci.com/gh/ICIJ/fluent-http-apigen.png?style=shield&circle-token=0d24d3ece1add1d2d22cccafd04c0b0024550a20
   :alt: Circle CI
   :target: https://circleci.com/gh/ICIJ/fluent-http-apigen


This is a small tool to generate HTTP API documentation for https://github.com/CodeStory/fluent-http

It generates markdown and provides API documentation like https://github.com/ICIJ/datashare/wiki/Datashare-API

Use
---

Install with pip ::

   pip install fluent-http-apigen
   apigen ...

Develop
-------

To develop, just run::

    virtualenv --python=python3 venv
    source venv/bin/activate
    python setup.py develop
    pip install -e ".[dev]"
    nosetests

To release ::

    bumpversion --commit --tag --current-version `python setup.py --version` [major|minor|patch] setup.py
    git push origin master --tags
    python setup.py  sdist bdist_egg upload
