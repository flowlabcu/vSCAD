.. highlight:: shell

============
Installation
============


Stable release
--------------

To install vSCAD, run this command in your terminal:

.. code-block:: console

    $ pip install vSCAD

This is the preferred method to install vSCAD, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for vSCAD can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/njrovito/vSCAD

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/njrovito/vSCAD/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/njrovito/vSCAD
.. _tarball: https://github.com/njrovito/vSCAD/tarball/master

Dependencies
------------
Python library dependencies are listed in the `requirements.txt` file. To install them, run:

.. code-block:: console

    $ pip install -r requirements.txt

This package also requires OpenSCAD. OpenSCAD can be downloaded from the `OpenSCAD website <https://openscad.org/>`_.